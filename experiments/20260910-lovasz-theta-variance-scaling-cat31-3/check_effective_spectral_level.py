"""Exam 3, stage 2: the "effective spectral level" reformulation the user derived (2026-09-12)
from stage 1's tail_tightness data -- independently re-verified below before being trusted
(audit-verification-gate.md: the user's own "VERIFIED" is this session's "INFERRED" until an
independent computation confirms it).

Derivation (re-checked, not assumed): since gamma_l = l(N+1-l)/(q(N-q)) (already the swap-walk
gap formula used throughout points 15-21), the q(N-q) factor cancels in t_r := R_r/(D_r/gamma_r):

    1/t_r = [ sum_{l>=r} l(N+1-l)*E_l ] / [ r(N+1-r) * sum_{l>=r} E_l ]

i.e. 1/t_r is the tail's E_l-weighted average of l(N+1-l), normalized to 1 at the boundary value
r(N+1-r). Defining the "effective spectral level" l_eff via l_eff(N+1-l_eff) = r(N+1-r)/t_r
(the SAME quadratic, solved for the smaller root near r rather than the mirror root near N+1-r)
turns the abstract tightness ratio into a single number with a direct physical reading: "the
tail behaves, on average, as if its mass sat at level l_eff instead of exactly at level r".

At r=4, using the already-verified aggregate tail_tightness_4 from metrics/tail_concentration_
ratio.json (point 22): l_eff grows only 4.00 -> 4.72 (n=23 -> 47), NOT diverging toward the
available spectral range's own ceiling (which grows from big_n=10 to big_n=22 over the same
range) -- i.e. the residual mass beyond l=1,2,3 stays LOCALIZED near the bottom of the tail,
not spreading toward high l as the available range widens.

This reframes the target for a uniform-in-n statement: NOT tail_tightness_r(n)->1 (which fails
at fixed r=4, point 22), but the much weaker and plausibly-provable

    sum_{l>=4} l(N+1-l)*E_l  <=  C * N * sum_{l>=4} E_l      (uniform C, i.e. l_eff = O(N))

or even the stronger (not yet tested) l_eff = O(log N) / O(1), which the data below is checked
against via a log-log growth-rate fit -- reported with appropriate epistemic weight (7 data
points is a trend, not a proof of the asymptotic growth CLASS).
"""

from __future__ import annotations

import json
from math import log, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def l_eff(r: int, big_n: int, t_r: float) -> float | None:
    """Solve l(N+1-l) = r(N+1-r)/t_r for the root near r (not the mirror root near N+1-r)."""
    if t_r is None or t_r <= 0:
        return None
    target = r * (big_n - r + 1) / t_r
    np1 = big_n + 1
    disc = np1 * np1 - 4 * target
    if disc < 0:
        return None
    return (np1 - sqrt(disc)) / 2


def growth_rate_fit(ns: list[int], deltas: list[float]) -> dict:
    """Rough log-log style diagnostics for how (l_eff - r) grows with big_n -- NOT a rigorous
    regression (only 7 points), just enough to distinguish 'roughly bounded', 'roughly log(N)',
    'roughly sqrt(N)', 'roughly linear in N' by eye, reported as [WEAK] evidence only."""
    out = []
    for n, delta in zip(ns, deltas):
        out.append(
            {
                "big_n": n,
                "delta_l_eff": delta,
                "delta_over_log_n": delta / log(n) if n > 1 and delta is not None else None,
                "delta_over_sqrt_n": delta / sqrt(n) if delta is not None else None,
                "delta_over_n": delta / n if delta is not None else None,
            }
        )
    return {"points": out}


if __name__ == "__main__":
    tail_data = json.load(open(METRICS / "tail_concentration_ratio.json", encoding="utf-8"))
    agg = {a["n"]: a for a in tail_data["aggregate"]}

    ladder = json.load(open(METRICS / "l4_ladder_bound_analytic.json", encoding="utf-8"))
    big_n_by_n = {int(n_str): rows[0]["N"] for n_str, rows in ladder["per_layer"].items()}

    results = {}
    for r in [1, 2, 3, 4]:
        rows = []
        for n in sorted(agg):
            big_n = big_n_by_n[n]
            t_r = agg[n][f"tail_tightness_{r}"]
            leff = l_eff(r, big_n, t_r)
            rows.append(
                {
                    "n": n,
                    "N": big_n,
                    "t_r": t_r,
                    "l_eff": leff,
                    "delta": (leff - r) if leff else None,
                }
            )
            d = leff - r
            print(f"r={r}  n={n:3d}  N={big_n:3d}  t_r={t_r:.4f}  l_eff={leff:.3f}  delta={d:.3f}")
        results[r] = rows

    print("\n=== Growth-rate diagnostics for r=4 (delta = l_eff - 4) ===")
    r4_rows = [row for row in results[4] if row["delta"] is not None]
    fit = growth_rate_fit([row["N"] for row in r4_rows], [row["delta"] for row in r4_rows])
    for pt in fit["points"]:
        print(
            f"  N={pt['big_n']:3d}  delta={pt['delta_l_eff']:.3f}  "
            f"delta/log(N)={pt['delta_over_log_n']:.4f}  "
            f"delta/sqrt(N)={pt['delta_over_sqrt_n']:.4f}  delta/N={pt['delta_over_n']:.5f}"
        )

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "effective_spectral_level.json", "w", encoding="utf-8") as f:
        json.dump({"per_r": results, "r4_growth_fit": fit}, f, indent=2)
