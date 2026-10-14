"""Evaluate the PATCHED PRODUCTION hook (proposed/pre_compact_patched.py) against the original on the same real history.

This closes the 'my reimplementation != the deployable code' gap: same replay inputs as audit_compaction.py,
but the compactor under test is the actual hook module with the minimal diff applied.

Run: python audit_patched_hook.py [--stride 4]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import statistics as st
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import audit_compaction as ac  # noqa: E402
import memlib as ml  # noqa: E402

PATCHED = HERE / "proposed" / "pre_compact_patched.py"


def load_patched():
    sys.path.insert(0, str(ac.HOOKS))  # for `from lib.discovery import ...`
    spec = importlib.util.spec_from_file_location("pre_compact_patched", PATCHED)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(mod, text: str) -> str:
    return ac.prod_compact(mod, text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stride", type=int, default=4)
    ap.add_argument("--repo", help="evaluate on ANOTHER project's history (out-of-sample)")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    if a.repo:
        ac.REPO = Path(a.repo)
    orig, pat = ac.load_prod(), load_patched()
    rows = []
    for i, (h, d) in enumerate(ac.versions()):
        if i % a.stride:
            continue
        old = ac.show(h)
        if not old or not ac.eligible(old):
            continue
        o1 = run(orig, old)
        p1, p1_arch = ac.prod_compact_with_archive(pat, old)
        p2 = run(pat, p1)
        o2 = run(orig, o1)
        ro, rp = ml.retention(old, o1), ml.retention(old, p1)
        rp_total = ml.retention(old, p1 + "\n" + p1_arch)
        vl_o, vn = ac.verdict_loss(old, o1)
        vl_p, _ = ac.verdict_loss(old, p1)
        rows.append(
            {
                "commit": h[:7],
                "date": d,
                "bytes_old": ac.n_bytes(old),
                "orig_bytes": ac.n_bytes(o1),
                "pat_bytes": ac.n_bytes(p1),
                "orig_n_old": ro["n_old"],
                "orig_lost": len(ro["lost"]),
                "pat_lost": len(rp["lost"]),
                "pat_lost_total": len(rp_total["lost"]),
                "orig_verdict_lost": vl_o,
                "pat_verdict_lost": vl_p,
                "verdict_total": vn,
                "orig_idempotent": o2 == o1,
                "pat_idempotent": p2 == p1,
                "pat_pass2_retention": round(ml.retention(old, p2)["retention"], 4),
                "orig_pass2_retention": round(ml.retention(old, o2)["retention"], 4),
            }
        )
    n = len(rows)
    half = n // 2

    def pooled(rs, k):
        return round(1 - sum(r[k] for r in rs) / sum(r["orig_n_old"] for r in rs), 4)

    out = {
        "inputs": n,
        "retention_pooled": {
            "orig": pooled(rows, "orig_lost"),
            "patched": pooled(rows, "pat_lost"),
            "patched_active_plus_archive": pooled(rows, "pat_lost_total"),
        },
        "retention_first_half": {
            "orig": pooled(rows[:half], "orig_lost"),
            "patched": pooled(rows[:half], "pat_lost"),
        },
        "retention_second_half": {
            "orig": pooled(rows[half:], "orig_lost"),
            "patched": pooled(rows[half:], "pat_lost"),
        },
        "bytes_mean": {
            "orig": round(st.mean(r["orig_bytes"] for r in rows)),
            "patched": round(st.mean(r["pat_bytes"] for r in rows)),
            "input": round(st.mean(r["bytes_old"] for r in rows)),
        },
        "verdict_tokens_lost": {
            "orig": sum(r["orig_verdict_lost"] for r in rows),
            "patched": sum(r["pat_verdict_lost"] for r in rows),
            "of": sum(r["verdict_total"] for r in rows),
        },
        "second_pass_leaves_file_unchanged_share": {
            "orig": round(sum(r["orig_idempotent"] for r in rows) / n, 3),
            "patched": round(sum(r["pat_idempotent"] for r in rows) / n, 3),
        },
        "pass2_retention_mean_vs_original": {
            "orig": round(st.mean(r["orig_pass2_retention"] for r in rows), 4),
            "patched": round(st.mean(r["pat_pass2_retention"] for r in rows), 4),
        },
    }
    # guard behaviours
    bad = (
        "# t\n\n## S\n- first 2026-09-39 entry\n"
        + "\n".join(f"- e{i}" for i in range(25))
        + "\n- last 2026-09-01 end\n"
    )
    guard = {}
    for name, mod in (("orig", orig), ("patched", pat)):
        try:
            run(mod, bad)
            guard[name] = "no crash"
        except Exception as e:
            guard[name] = f"CRASH {type(e).__name__}"
    out["malformed_date"] = guard
    # trim archives instead of deleting
    src = (HERE / "snapshots" / "before" / "activeContext.md").read_text(encoding="utf-8")
    trim = {}
    for name, mod in (("orig", orig), ("patched", pat)):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "activeContext.md"
            p.write_text(src, encoding="utf-8")
            removed = mod._trim_old_entries(p, max_age_days=24)  # emulates 2026-12-19 (+66 days)
            arch = (
                list((Path(t) / "history").glob("trimmed-*.md"))
                if (Path(t) / "history").exists()
                else []
            )
            archived = "".join(x.read_text(encoding="utf-8") for x in arch)
            lost = (
                ml.extract_anchors(src)
                - ml.extract_anchors(p.read_text(encoding="utf-8"))
                - ml.extract_anchors(archived)
            )
            trim[name] = {
                "sections_removed": removed,
                "archive_files": len(arch),
                "anchors_lost_after_trim": len(lost),
            }
    out["trim_at_plus_66d"] = trim
    Path(HERE / f"results_patched_hook{a.tag}.json").write_text(
        json.dumps({"summary": out, "rows": rows}, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
