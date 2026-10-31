"""Recheck the N cells closest to the threshold with the current interval_cells.cell_bound.

WHY: interval_cells.py used to set lambda_K from the MIDPOINT of its arb enclosure (float(lam_h) > 0).
The corrected rule uses the UPPER bound. This script reruns the cells with the smallest stored slack
and checks that every rigorous B_up is still below s_target and that no B_up moved relative to the
stored value. Writes metrics/recheck_closest_leaves.json.

Usage: python -I code/recheck_closest_leaves.py [N]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PHASE4 = os.path.normpath(os.path.join(HERE, ".."))
TOP = os.path.join(PHASE4, "metrics", "interval_top1000.json")
OUT = os.path.join(PHASE4, "metrics", "recheck_closest_leaves.json")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    sys.path.insert(0, HERE)
    import interval_cells as ivl

    rows = sorted(json.load(open(TOP, encoding="utf-8"))["rows"], key=lambda r: r["slack"])[:n]
    still_below = 0
    max_increase = 0.0
    max_abs_change = 0.0
    for r in rows:
        res = ivl.cell_bound(r["cell"])
        b_new = float(res["B_up"])
        if ivl.s_target > res["B_up"]:
            still_below += 1
        max_increase = max(max_increase, b_new - r["B_up"])
        max_abs_change = max(max_abs_change, abs(b_new - r["B_up"]))
    out = {
        "cells_rechecked": len(rows),
        "still_below_s_target": still_below,
        "max_increase_of_B_up": max_increase,
        "max_abs_change_of_B_up": max_abs_change,
        "min_stored_slack": rows[0]["slack"],
        "s_target": float(ivl.s_target),
        "verdict": "UNCHANGED" if still_below == len(rows) and max_increase <= 1e-12 else "CHANGED",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
