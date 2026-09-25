# ruff: noqa: E501
"""A1: does the closed form  min_s LB(k,r,s) = r^2 + s* + 1,  s* = ceil(2kr/(r^2+1)),  hold exactly, and where does it fail?

LB(k,r,s) = r^2 + max(s, 2kr - s r^2) + max(1, k^2 - C(s,2) r^2)   (decision.md C-LB, h2_ext.lb).
Pure integer arithmetic, no sampling. Reports, for r = 2..12 and every k in 1..220:
  * mismatches between the exact minimum over s in 1..2kr and the closed form (and their share),
  * the first d = k + r with min_s LB < d (the size where the dimension test can first fire),
  * whether the test keeps firing for every larger d up to the scan limit (monotonicity of the threshold).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
KMAX = 220


def lb(k: int, r: int, s: int) -> int:
    return r * r + max(s, 2 * k * r - s * r * r) + max(1, k * k - (s * (s - 1) // 2) * r * r)


def exact_min(k: int, r: int) -> tuple[int, int]:
    best = None
    arg = 0
    for s in range(1, 2 * k * r + 1):
        v = lb(k, r, s)
        if best is None or v < best:
            best, arg = v, s
    return best, arg


def main() -> None:
    out = []
    for r in range(2, 13):
        mism = []
        first_d = None
        fires = {}
        for k in range(1, KMAX + 1):
            d = k + r
            m, s_arg = exact_min(k, r)
            s_star = math.ceil(2 * k * r / (r * r + 1))
            closed = r * r + s_star + 1
            if m != closed:
                mism.append((k, m, closed, s_arg, s_star))
            fires[d] = m < d
            if first_d is None and m < d:
                first_d = d
        persists = all(fires[d] for d in fires if d >= (first_d or 10**9))
        # mismatches are only interesting where they matter for firing
        # WHY: an earlier draft filtered "near the threshold" by d, which also caught tiny k; the meaningful split is k < r
        # (blocks A_i are k x r, so k < r is degenerate) versus k >= r.
        near = [x for x in mism if x[0] >= r]
        out.append(
            {
                "r": r,
                "first_d_test_can_fire": first_d,
                "scan_limit_d": KMAX + r,
                "threshold_persists": persists,
                "n_closed_form_mismatches_over_k1_to_220": len(mism),
                "mismatches_with_k_ge_r": near,
                "first_5_mismatches_k_exact_closed_sarg_sstar": mism[:5],
            }
        )
        print(
            f"r={r:<2} d*={first_d} persists={persists} closed-form mismatches={len(mism)} "
            f"mismatches with k>=r={len(near)}"
        )
    (HERE / "closed_form_check.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
