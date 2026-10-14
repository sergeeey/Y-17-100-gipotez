"""Tests for the memory-audit toolkit. Run: python -m pytest tooling-eval/memory-audit-2026-10-14/test_memlib.py -q

Three groups: (1) anchors/retention, (2) the anchor-preserving compactor, (3) REPRODUCTIONS of defects found in the
production hook (documented as tests: they pass while the defect exists, so a fix of the hook will turn them red and
tell you to update the audit) plus digest/detector checks.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import memlib as ml  # noqa: E402

REPO = HERE.parents[1]
HOOKS = Path.home() / ".claude" / "hooks"
SNAP = HERE / "snapshots" / "before" / "activeContext.md"


def _prod():
    if not (HOOKS / "pre_compact.py").exists():
        pytest.skip("production pre_compact.py not available")
    sys.path.insert(0, str(HOOKS))
    spec = importlib.util.spec_from_file_location("pre_compact_prod_t", HOOKS / "pre_compact.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _prod_compact(mod, text: str) -> str:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "a.md"
        p.write_text(text, encoding="utf-8")
        changed = mod._create_progressive_summary(p)
        return p.read_text(encoding="utf-8") if changed else text


def _doc(n: int = 28, extra: str = "") -> str:
    entries = "\n".join(
        f"- entry {i} commit abcdef{i % 9}1 2026-09-{1 + i % 27:02d} experiments/x{i}/decision.md H-B7-{i} KILLED"
        for i in range(n)
    )
    return f"# t\n\n## Log\n{entries}\n{extra}\n## Decision log\n- keep me verbatim\n"


# ------------------------------------------------------------------ group 1: anchors
def test_anchors_basic_types():
    a = ml.extract_anchors(
        "commit `5ddba97` 2026-10-14 H-CAT56-2 Point 64 experiments/a/decision.md 0.9126 FALSIFIED 2502.16227"
    )
    for k in (
        "hash:5ddba97",
        "date:2026-10-14",
        "hid:H-CAT56-2",
        "point:Point 64",
        "path:experiments/a/decision.md",
        "num:0.9126",
        "verdict:FALSIFIED",
        "arxiv:2502.16227",
    ):
        assert k in a


def test_numeric_ratio_is_not_a_path_and_timestamp_has_a_date():
    a = ml.extract_anchors(
        "ratios 1.890/2.025/2.001 and 3.9e-12/1.75e; modified: 2026-09-08T08:38:14Z"
    )
    assert not [x for x in a if x.startswith("path:")]
    assert "date:2026-09-08" in a


def test_commit_refs_exclude_sha256_uuid_and_ellipsis():
    t = "sha256 `2b425b7d…c57a` id 1d8443cd-ffe1-43e0-bdb5-efd0ebc5eada and archive sha256 35b70e1a... but commit `5ddba97`"
    assert ml.commit_refs(t) == {"5ddba97"}


def test_retention_identity_and_loss():
    t = "commit 5ddba97 on 2026-10-14 KILLED"
    assert ml.retention(t, t)["retention"] == 1.0
    r = ml.retention(t, "commit on 2026-10-14")
    assert 0 < r["retention"] < 1 and "hash:5ddba97" in r["lost"]


# ------------------------------------------------------------------ group 2: compactor
@pytest.mark.parametrize("kw", [{"verbatim_bytes": 300}, {"verbatim_lines": 20}])
def test_compactor_idempotent(kw):
    a = ml.compact_text(_doc(), **kw)
    assert ml.compact_text(a, **kw) == a


@pytest.mark.parametrize("kw", [{"verbatim_bytes": 300}, {"verbatim_lines": 20}])
def test_compactor_keeps_anchors_and_verdicts(kw):
    t = _doc(40)
    a = ml.compact_text(t, **kw)
    assert ml.retention(t, a)["retention"] >= 0.95
    assert not {x for x in ml.extract_anchors(t) if x.startswith("verdict:")} - ml.extract_anchors(
        a
    )


def test_compactor_leaves_protected_sections_and_never_crashes_on_bad_dates():
    t = (
        "# t\n\n## Decision log\n- 2026-09-39 weird\n"
        + "\n".join(f"- d{i}" for i in range(40))
        + "\n\n## Log\n- 2026-09-39 x\n"
        + "\n".join(f"- e{i} 2026-09-0{1 + i % 8}" for i in range(30))
        + "\n- last 2026-09-01\n"
    )
    a = ml.compact_text(t, verbatim_lines=5)
    assert "## Decision log\n- 2026-09-39 weird\n- d0" in a  # protected, verbatim
    assert a == ml.compact_text(a, verbatim_lines=5)


def test_each_summary_is_its_own_line():
    t = ml.compact_text(_doc(60), verbatim_lines=5)
    n_sum = t.count("[summarized]")
    assert n_sum >= 50  # one per entry, not one for the whole block


# ------------------------------------------------------------------ group 3: production defects (reproductions)
def test_prod_collapses_consecutive_bullets_into_one_line():
    m = _prod()
    out = _prod_compact(m, _doc(40))
    assert (
        out.count("[summarized]") == 1
    )  # 20 older bullets -> ONE line (blank-line chunking never splits them)
    assert (
        ml.retention(_doc(40), out)["retention"]
        < ml.retention(_doc(40), ml.compact_text(_doc(40)))["retention"]
    )


def test_prod_crashes_on_malformed_date_in_a_long_section():
    m = _prod()
    bad = (
        "# t\n\n## S\n- first 2026-09-39 entry\n"
        + "\n".join(f"- e{i}" for i in range(25))
        + "\n- last 2026-09-01 end\n"
    )
    with pytest.raises(ValueError):
        _prod_compact(m, bad)
    assert ml.compact_text(bad)  # ours degrades gracefully


@pytest.mark.skipif(not SNAP.exists(), reason="snapshot missing")
def test_prod_is_not_idempotent_on_real_snapshot_and_loses_more_on_pass2():
    m = _prod()
    t = SNAP.read_text(encoding="utf-8")
    p1 = _prod_compact(m, t)
    p2 = _prod_compact(m, p1)
    assert p2 != p1  # each PreCompact pass keeps rewriting the file
    assert ml.retention(t, p2)["retention"] <= ml.retention(t, p1)["retention"]
    a1 = ml.compact_text(t, verbatim_bytes=12000)
    assert ml.compact_text(a1, verbatim_bytes=12000) == a1
    assert ml.retention(t, a1)["retention"] > ml.retention(t, p1)["retention"]


# ------------------------------------------------------------------ group 4: digest + detector
def _git(*a):
    return subprocess.run(
        ["git", *a], cwd=REPO, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def test_digest_within_budget_and_matches_independent_recomputation():
    import digest as dg

    d = dg.build_digest(REPO)
    assert len(d.encode("utf-8")) <= 1500
    assert f"HEAD {_git('rev-parse', '--short', 'HEAD')}" in d
    assert f"git: {_git('branch', '--show-current')} " in d
    blocks = re.split(
        r"\n  - id: ", (REPO / "registry" / "graph.yaml").read_text(encoding="utf-8")
    )[1:]
    n_hyp = sum(1 for b in blocks if re.search(r"\n\s+type:\s*hypothesis\b", b))
    assert f"registry: {n_hyp} hypotheses" in d


def test_detector_g3_sees_emphasised_claim_and_g4_superseded_marker():
    import audit_state as A

    stores = {
        "activeContext.md": "Email NOT SENT. [SUPERSEDED 2026-09-23: email SENT]\n`EMAIL: SENT`",
        "auto/MEMORY.md": "- [x](x.md) — left UNCOMMITTED in hooks repo pending user go-ahead",
        "auto/x.md": "now **committed** in the hooks repo as 2dca838",
    }
    rows = {r["id"]: r for r in A.gold_claims(stores)}
    assert rows["G3"]["verdict"] == "CONFLICT"  # index says uncommitted, body says committed
    assert rows["G4"]["verdict"] == "CORRECT"  # the superseded line is neutralised


def test_detector_known_limit_literal_quote_counts_as_a_claim():
    """Documented limitation (same class as the repo's [AVOID x7] mention-vs-assertion): a quoted phrase is a claim."""
    import audit_state as A

    stores = {
        "activeContext.md": "we found the line 'Email NOT SENT' stale; `EMAIL: SENT`",
        "auto/MEMORY.md": "",
    }
    rows = {r["id"]: r for r in A.gold_claims(stores)}
    assert rows["G4"]["verdict"] == "CONFLICT"


# ------------------------------------------------------------------ group 5: the PATCHED production hook (proposed/)
PATCHED = HERE / "proposed" / "pre_compact_patched.py"


def _patched():
    if not PATCHED.exists():
        pytest.skip("run make_patched_hook.py first")
    sys.path.insert(0, str(HOOKS))
    spec = importlib.util.spec_from_file_location("pre_compact_patched_t", PATCHED)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.skipif(not SNAP.exists(), reason="snapshot missing")
def test_patched_hook_is_idempotent_and_keeps_anchors_on_real_snapshot():
    m = _patched()
    t = SNAP.read_text(encoding="utf-8")
    p1 = _prod_compact(m, t)
    assert _prod_compact(m, p1) == p1
    assert ml.retention(t, p1)["retention"] >= 0.95


def test_patched_hook_survives_malformed_date_and_does_not_fold_bullets():
    m = _patched()
    bad = (
        "# t\n\n## S\n- first 2026-09-39 entry\n"
        + "\n".join(f"- e{i} abcdef{i % 9}1" for i in range(25))
        + "\n- last 2026-09-01 end\n"
    )
    out = _prod_compact(m, bad)  # must not raise
    assert (
        out.count("[summarized]") >= 5
    )  # one summary per older bullet, not one for the whole block


def test_patched_hook_trim_archives_instead_of_deleting():
    m = _patched()
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "activeContext.md"
        p.write_text(
            "# T\n\n## Old\n- 2025-01-01 decision abcdef12 experiments/x/decision.md\n\n## New\n- 2099-01-01 keep\n",
            encoding="utf-8",
        )
        removed = m._trim_old_entries(p, max_age_days=90)
        assert removed == 1 and "## Old" not in p.read_text(encoding="utf-8")
        arch = list((Path(d) / "history").glob("trimmed-*.md"))
        assert arch and "abcdef12" in arch[0].read_text(encoding="utf-8")


# ------------------------------------------------------------------ group 6: findings of the independent review (iteration 1)
def test_digest_never_reports_none_when_unpushed_state_is_unknown():
    """Review P1-1: a branch without upstream must read 'unknown', not 'none'."""
    import digest as dg

    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.email=a@b",
                "-c",
                "user.name=t",
                "commit",
                "-q",
                "--allow-empty",
                "-m",
                "x",
            ],
            cwd=d,
            check=True,
        )
        line, unpushed = dg.git_line(Path(d))
    assert "unpushed: unknown" in line and "unpushed: none" not in line and unpushed == []


def test_digest_empty_u2_log_is_not_vacuously_no_reply():
    """Review P2-3: all([]) is True; an empty log proves nothing."""
    from datetime import date

    import digest as dg

    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "outreach").mkdir()
        (Path(d) / "outreach" / "U2_WAIT_LOG.md").write_text(
            "Clock started: **2026-09-23**\n", encoding="utf-8"
        )
        assert "reply on file: unknown" in dg.u2_line(Path(d), date(2026, 10, 14))


def test_ground_truth_failures_become_unknown_not_a_verdict(monkeypatch):
    """Review P2-4: a git/network error must not turn a claim CORRECT or STALE (real gold_claims(), patched truth)."""
    import audit_state as A

    monkeypatch.setattr(A, "truth_pushed", lambda h: "unknown")
    monkeypatch.setattr(A, "truth_mo_published", lambda: "unknown")
    stores = {
        "activeContext.md": "Committed `25776d4`, pushed. MathOverflow https://mathoverflow.net/questions/1",
        "auto/MEMORY.md": "",
    }
    rows = {r["id"]: r for r in A.gold_claims(stores)}
    assert rows["G1"]["verdict"] == "UNVERIFIED" and rows["G2"]["verdict"] == "UNVERIFIED"
    assert (
        A.accuracy([r for r in rows.values() if r["id"] in {"G1", "G2"}])["accuracy_present"]
        is None
    )


def test_patched_trim_survives_blocked_archive_dir_and_keeps_sections():
    """Review P2-1: archive I/O failure must neither crash the hook nor delete anything."""
    m = _patched()
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "history").write_text("i am a file, not a directory", encoding="utf-8")
        p = Path(d) / "activeContext.md"
        body = "# T\n\n## Old\n- 2025-01-01 decision abcdef12\n\n## New\n- 2099-01-01 keep\n"
        p.write_text(body, encoding="utf-8")
        assert m._trim_old_entries(p, max_age_days=90) == 0
        assert p.read_text(encoding="utf-8") == body


def test_patched_trim_first_archives_original_text_not_summaries():
    """Review P2-2: stale AND long section -> archive must hold the verbatim lines."""
    m = _patched()
    src = (
        "# T\n\n## Old\n"
        + "\n".join(
            f"- 2025-01-0{1 + i % 9} entry{i} abcdef{i % 9}1 longtext " + "x" * 200
            for i in range(30)
        )
        + "\n"
    )
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "activeContext.md"
        p.write_text(src, encoding="utf-8")
        assert m._trim_old_entries(p, max_age_days=90) == 1
        arch = next((Path(d) / "history").glob("trimmed-*.md")).read_text(encoding="utf-8")
        assert "[summarized]" not in arch and "entry29" in arch and "x" * 200 in arch
    main_src = PATCHED.read_text(encoding="utf-8")
    body = main_src[main_src.index("def main():") :]
    assert body.index("_trim_old_entries(active)") < body.index(
        "_create_progressive_summary(active)"
    )


# ------------------------------------------------------------------ group 7: findings of the independent review (iteration 2)
@pytest.mark.parametrize("newest_first", [True, False])
def test_cap_pointer_does_not_flip_order_detection_and_second_pass_is_stable(newest_first):
    """Review N1 (P1): a dated pointer line made the next pass compact the newest verbatim entries."""
    m = _patched()
    days = list(range(1, 29)) * 8
    days = sorted(days, reverse=newest_first)[:200]
    entries = [
        f"- 2026-09-{d:02d} entry{i} abcdef{i % 9}1 experiments/x{i}/decision.md " + "x" * 400
        for i, d in enumerate(days)
    ]
    src = "# T\n\n## S\n" + "\n".join(entries) + "\n"
    p1 = _prod_compact(m, src)
    assert "moved verbatim to history/compacted-" in p1, "cap must trigger for this test to mean anything"
    assert m._section_is_newest_first(p1.splitlines()) == newest_first
    p2 = _prod_compact(m, p1)
    assert p2 == p1
    verbatim = [x for x in p1.splitlines() if x.startswith("- 2026") and "x" * 400 in x]
    assert len(verbatim) >= 15
