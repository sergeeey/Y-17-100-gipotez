# ruff: noqa: E501
"""Gate 13: first size d*(r) where the proven lower bound on dim V-perp stops forbidding dim V-perp < d,
for r = 2..12, plus comparison with the asymptotic estimate derived by hand.

lb(k,r,s) = r^2 + max(s, 2kr - s r^2) + max(1, k^2 - C(s,2) r^2),  d = k + r   (h2_ext.lb, proven).
Asymptotics (hand derivation, NOT a theorem): balancing s = 2kr - s r^2 gives s = 2kr/(r^2+1), and for
large k the third term is 1 (when C(s,2) r^2 >= k^2 - 1), so lb ~ r^2 + 1 + 2kr/(r^2+1), which is < k + r
iff k > (r^2 - r + 1)(r^2 + 1)/(r - 1)^2.  Integrality of s and the third-term constraint shift the true
first k upward, so the estimate is a LOWER estimate of k*, compared numerically below.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def lb(k: int, r: int, s: int) -> int:
    return r * r + max(s, 2 * k * r - s * r * r) + max(1, k * k - (s * (s - 1) // 2) * r * r)


def first_d(r: int) -> tuple[int, int, int]:
    for k in range(2, 4000):
        d = k + r
        best = min((lb(k, r, s), s) for s in range(1, 2 * k * r + 1))
        if best[0] < d:
            return d, k, best[1]
    raise RuntimeError("not found")


def main() -> int:
    rows = []
    for r in range(2, 13):
        d, k, s = first_d(r)
        est = (r * r - r + 1) * (r * r + 1) / (r - 1) ** 2
        rows.append(
            {
                "r": r,
                "d_star": d,
                "k_star": k,
                "s_at_min": s,
                "k_asymptotic_estimate": est,
                "ratio_k_over_estimate": k / est,
            }
        )
        print(f"r={r}: d*={d} k*={k} s={s} estimate k>{est:.1f} ratio={k / est:.3f}")
    (HERE / "metrics" / "gate13_threshold_formula.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
