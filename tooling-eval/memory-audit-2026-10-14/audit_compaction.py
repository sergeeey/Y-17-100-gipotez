"""M1: compaction fact retention — real history replay, PROD vs ALT-A vs ALT-B.

Run:  python audit_compaction.py [--stride 4] [--out results_compaction.json]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import statistics as st
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import memlib as ml  # noqa: E402

REPO = HERE.parents[1]
ACTIVE_REL = ".claude/memory/activeContext.md"
HOOKS = Path.home() / ".claude" / "hooks"


def git(*args: str) -> tuple[str, int]:
    r = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return r.stdout, r.returncode


def load_prod():
    sys.path.insert(0, str(HOOKS))
    spec = importlib.util.spec_from_file_location("pre_compact_prod", HOOKS / "pre_compact.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def prod_compact_with_archive(mod, text: str) -> tuple[str, str]:
    """Run the hook on a temp copy; return (active text, text of everything it archived under history/)."""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "activeContext.md"
        p.write_text(text, encoding="utf-8")
        changed = mod._create_progressive_summary(p)
        arch = (
            "".join(
                x.read_text(encoding="utf-8") for x in sorted((Path(d) / "history").glob("*.md"))
            )
            if (Path(d) / "history").exists()
            else ""
        )
        return (p.read_text(encoding="utf-8") if changed else text), arch


def prod_compact(mod, text: str) -> str:
    return prod_compact_with_archive(mod, text)[0]


def versions() -> list[tuple[str, str]]:
    out, _ = git("log", "--format=%H %cs", "--reverse", "--", ACTIVE_REL)
    return [tuple(x.split(" ", 1)) for x in out.strip().splitlines() if x.strip()]


def show(h: str) -> str:
    out, rc = git("show", f"{h}:{ACTIVE_REL}")
    return out if rc == 0 else ""


def n_bytes(s: str) -> int:
    return len(s.encode("utf-8"))


def eligible(text: str, tail: int = 20) -> bool:
    _, secs = ml.parse_sections(text)
    for head, lines in secs:
        if any(head.startswith(p) for p in ml.NEVER_SUMMARIZE_PREFIXES):
            continue
        body = [x for x in lines]
        while body and not body[-1].strip():
            body.pop()
        if len(body) > tail:
            return True
    return False


def verdict_loss(old: str, new: str) -> tuple[int, int]:
    a = {x for x in ml.extract_anchors(old) if x.startswith("verdict:")}
    b = {x for x in ml.extract_anchors(new) if x.startswith("verdict:")}
    return len(a - b), len(a)


def replay(stride: int) -> dict:
    mod = load_prod()
    vs = versions()
    rows = []
    for i, (h, d) in enumerate(vs):
        if i % stride:
            continue
        old = show(h)
        if not old or not eligible(old):
            continue
        prod = prod_compact(mod, old)
        alt_a = ml.compact_text(old, verbatim_lines=20, anchored=True)
        alt_b = ml.compact_text(old, verbatim_bytes=12000, anchored=True)
        row = {"commit": h[:7], "date": d, "bytes_old": n_bytes(old)}
        for name, new in (("prod", prod), ("alt_a", alt_a), ("alt_b", alt_b)):
            r = ml.retention(old, new)
            vl, vn = verdict_loss(old, new)
            row[name] = {
                "bytes": n_bytes(new),
                "retention": round(r["retention"], 4),
                "n_old": r["n_old"],
                "lost": len(r["lost"]),
                "verdict_lost": vl,
                "verdict_total": vn,
            }
        prod2 = prod_compact(mod, prod)
        row["prod_pass2_retention_vs_original"] = round(ml.retention(old, prod2)["retention"], 4)
        row["prod_pass2_bytes"] = n_bytes(prod2)
        row["prod_summary_lines"] = prod.count("[summarized]")
        # idempotency of ALT-B: second pass must not grow and must not lose anchors
        alt_b2 = ml.compact_text(alt_b, verbatim_bytes=12000, anchored=True)
        row["alt_b_idem"] = {
            "grew": n_bytes(alt_b2) > n_bytes(alt_b),
            "extra_lost": len(ml.extract_anchors(alt_b) - ml.extract_anchors(alt_b2)),
        }
        row["alt_b_pass2_retention_vs_original"] = round(ml.retention(old, alt_b2)["retention"], 4)
        rows.append(row)
    return {"n_inputs": len(rows), "rows": rows}


def crash_scan() -> dict:
    """How often would production's unguarded strptime in _section_is_newest_first crash on real history?"""
    mod = load_prod()
    n_versions = n_crash = 0
    crash_commits = []
    for h, _d in versions():
        text = show(h)
        if not text:
            continue
        n_versions += 1
        _, secs = ml.parse_sections(text)
        crashed = False
        for head, lines in secs:
            if any(head.startswith(p) for p in ml.NEVER_SUMMARIZE_PREFIXES):
                continue
            body = list(lines)
            while body and not body[-1].strip():
                body.pop()
            if len(body) <= mod.VERBATIM_TAIL:
                continue
            try:
                mod._section_is_newest_first(body)
            except Exception:
                crashed = True
        if crashed:
            n_crash += 1
            crash_commits.append(h[:7])
    return {"n_versions": n_versions, "n_would_crash": n_crash, "sample": crash_commits[:5]}


def observed_events() -> dict:
    """Real production events: consecutive commits where the count of '[summarized]' lines rises."""
    vs = versions()
    prev = ""
    events = []
    for h, d in vs:
        cur = show(h)
        if prev and cur.count("[summarized]") > prev.count("[summarized]"):
            r = ml.retention(prev, cur)
            vl, vn = verdict_loss(prev, cur)
            events.append(
                {
                    "commit": h[:7],
                    "date": d,
                    "retention": round(r["retention"], 4),
                    "n_old": r["n_old"],
                    "lost": len(r["lost"]),
                    "verdict_lost": vl,
                    "verdict_total": vn,
                    "bytes_old": n_bytes(prev),
                    "bytes_new": n_bytes(cur),
                    "lost_sample": r["lost"][:8],
                }
            )
        prev = cur
    return {"n_events": len(events), "events": events}


def summarize(res: dict) -> dict:
    rows = res["rows"]

    def agg(name: str, key: str) -> float:
        return st.mean(r[name][key] for r in rows)

    def pooled(name: str) -> float:
        kept = sum(r[name]["n_old"] - r[name]["lost"] for r in rows)
        tot = sum(r[name]["n_old"] for r in rows)
        return kept / tot if tot else 1.0

    def vpool(name: str) -> float:
        lost = sum(r[name]["verdict_lost"] for r in rows)
        tot = sum(r[name]["verdict_total"] for r in rows)
        return 1 - (lost / tot) if tot else 1.0

    out = {"n_inputs": res["n_inputs"]}
    for name in ("prod", "alt_a", "alt_b"):
        out[name] = {
            "retention_pooled": round(pooled(name), 4),
            "retention_mean": round(agg(name, "retention"), 4),
            "verdict_retention_pooled": round(vpool(name), 4),
            "bytes_mean": round(agg(name, "bytes")),
        }
    out["prod_pass2_retention_mean_vs_original"] = round(
        st.mean(r["prod_pass2_retention_vs_original"] for r in rows), 4
    )
    out["alt_b_pass2_retention_mean_vs_original"] = round(
        st.mean(r["alt_b_pass2_retention_vs_original"] for r in rows), 4
    )
    out["prod_second_pass_changes_file_share"] = round(
        sum(
            r["prod_pass2_bytes"] != r["bytes_old"] and r["prod_pass2_bytes"] != r["prod"]["bytes"]
            for r in rows
        )
        / len(rows),
        3,
    )
    out["prod_second_pass_mean_growth_bytes"] = round(
        st.mean(r["prod_pass2_bytes"] - r["prod"]["bytes"] for r in rows), 1
    )
    out["bytes_old_mean"] = round(st.mean(r["bytes_old"] for r in rows))
    out["alt_b_over_prod_bytes"] = round(out["alt_b"]["bytes_mean"] / out["prod"]["bytes_mean"], 3)
    out["alt_b_idempotent_all"] = all(
        (not r["alt_b_idem"]["grew"]) and r["alt_b_idem"]["extra_lost"] == 0 for r in rows
    )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stride", type=int, default=4)
    ap.add_argument("--out", default=str(HERE / "results_compaction.json"))
    a = ap.parse_args()
    res = replay(a.stride)
    summ = summarize(res)
    ev = observed_events()
    cs = crash_scan()
    full = {
        "replay_summary": summ,
        "replay_rows": res["rows"],
        "observed_events": ev,
        "crash_scan": cs,
    }
    print("crash_scan:", cs)
    Path(a.out).write_text(json.dumps(full, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summ, indent=1))
    if ev["events"]:
        rets = [e["retention"] for e in ev["events"]]
        print(
            f"observed production events: n={ev['n_events']} mean retention={st.mean(rets):.3f} "
            f"min={min(rets):.3f} verdict tokens lost={sum(e['verdict_lost'] for e in ev['events'])}"
            f"/{sum(e['verdict_total'] for e in ev['events'])}"
        )


if __name__ == "__main__":
    main()
