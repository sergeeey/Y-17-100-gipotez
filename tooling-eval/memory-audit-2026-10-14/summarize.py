"""One command that prints every number quoted in REPORT.md (reads results_*.json; recomputes pointer totals).

Run: python summarize.py [--write results_summary.json]
"""

from __future__ import annotations

import argparse
import json
import math
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import audit_state as A  # noqa: E402
import memlib as ml  # noqa: E402


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - m) / d, 3), round((c + m) / d, 3))


def pointer_totals(stores: dict[str, str]) -> dict:
    commits: set[str] = set()
    paths: set[str] = set()
    for text in stores.values():
        commits |= ml.commit_refs(text)
        paths |= {v for t, v in ml._typed_matches(text) if t == "path" and A.usable_path(v)}
    bad_c = [h for h in commits if not A.hash_resolves(h)]
    bad_p = [p for p in paths if not A.path_resolves(p)]
    return {
        "commit_refs": len(commits),
        "commit_dangling": len(bad_c),
        "paths": len(paths),
        "path_dangling": len(bad_p),
        "pointer_accuracy": round(
            1 - (len(bad_c) + len(bad_p)) / max(1, len(commits) + len(paths)), 4
        ),
        "dangling": sorted(bad_c + bad_p),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write")
    a = ap.parse_args()
    out: dict = {}
    c = json.load(open(HERE / "results_compaction.json", encoding="utf-8"))
    s = c["replay_summary"]
    out["M1"] = {
        "inputs": s["n_inputs"],
        "prod": s["prod"],
        "alt_a": s["alt_a"],
        "alt_b": s["alt_b"],
        "prod_lost_share": round(1 - s["prod"]["retention_pooled"], 4),
        "alt_a_lost_share": round(1 - s["alt_a"]["retention_pooled"], 4),
        "alt_b_lost_share": round(1 - s["alt_b"]["retention_pooled"], 4),
        "alt_a_loss_reduction": round(
            1 - (1 - s["alt_a"]["retention_pooled"]) / (1 - s["prod"]["retention_pooled"]), 3
        ),
        "alt_b_loss_reduction": round(
            1 - (1 - s["alt_b"]["retention_pooled"]) / (1 - s["prod"]["retention_pooled"]), 3
        ),
        "alt_a_bytes_vs_prod": round(s["alt_a"]["bytes_mean"] / s["prod"]["bytes_mean"], 3),
        "alt_b_bytes_vs_prod": round(s["alt_b"]["bytes_mean"] / s["prod"]["bytes_mean"], 3),
        "prod_pass2_retention": s["prod_pass2_retention_mean_vs_original"],
        "alt_b_pass2_retention": s["alt_b_pass2_retention_mean_vs_original"],
        "prod_second_pass_changes_file_share": s["prod_second_pass_changes_file_share"],
        "alt_b_idempotent_all": s["alt_b_idempotent_all"],
        "observed_events": {
            "n": c["observed_events"]["n_events"],
            "mean_retention": round(
                st.mean(e["retention"] for e in c["observed_events"]["events"]), 3
            ),
            "min_retention": min(e["retention"] for e in c["observed_events"]["events"]),
            "verdict_tokens_lost": sum(e["verdict_lost"] for e in c["observed_events"]["events"]),
            "verdict_tokens_total": sum(e["verdict_total"] for e in c["observed_events"]["events"]),
        },
        "crash_scan": c["crash_scan"],
    }
    d = json.load(open(HERE / "results_delivery.json", encoding="utf-8"))
    o = d["outputs"]
    out["M2"] = {
        "hook_outputs": len(o),
        "bytes_min_median_max": [
            min(x["bytes"] for x in o),
            int(st.median(x["bytes"] for x in o)),
            max(x["bytes"] for x in o),
        ],
        "activeContext_offsets": sorted({x["offset_of_activeContext"] for x in o}),
        "activeContext_bytes_visible_max": max(
            x["activeContext_bytes_visible_in_window"] for x in o
        ),
        "facts": len(d["facts"]),
        "digest_bytes": d["digest_bytes"],
        **{
            k: round(st.mean(x[k]["share"] for x in o), 3)
            for k in (
                "before_window",
                "before_full_output",
                "after_A_digest_first_window",
                "after_B_digest_after_banner_window",
            )
        },
    }
    for lab in ("before", "after"):
        r = json.load(open(HERE / f"results_state_{lab}.json", encoding="utf-8"))
        cnt = r["gold_accuracy"]["counts"]
        k = cnt.get("CORRECT", 0)
        n = k + cnt.get("STALE", 0) + cnt.get("CONFLICT", 0)
        out[f"M3_{lab}"] = {
            "counts": cnt,
            "accuracy": r["gold_accuracy"]["accuracy_present"],
            "wilson95": wilson(k, n),
            "n": n,
            "flags": r["integrity"]["flags_by_type"],
            "layout": r["layout"],
            "mutation": {
                kk.split(" ")[0]: [v["injected"], v["detected"]] for kk, v in r["mutation"].items()
            },
        }
    out["pointers_before"] = pointer_totals(A.load_stores(HERE / "snapshots" / "before"))
    out["pointers_after"] = pointer_totals(A.load_stores())
    txt = json.dumps(out, indent=1, ensure_ascii=False, default=str)
    print(txt)
    if a.write:
        Path(a.write).write_text(txt, encoding="utf-8")


if __name__ == "__main__":
    main()
