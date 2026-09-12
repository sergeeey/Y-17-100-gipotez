"""Exam 3, stage 1: test the tail-concentration reformulation the user proposed (2026-09-12,
instead of jumping straight to a geometric-decay hypothesis E_l ~ A*rho^l for individual levels).

Define, for the Johnson-slice spectral decomposition C_q = sum_l E_l (l=1..min(q,N-q)):

    R_r := sum_{l>=r} E_l                     (the true remaining tail after removing l<r)
    D_r := sum_{l>=r} gamma_l * E_l            (its swap-Dirichlet contribution)

Poincare (since gamma_l is increasing in l, gamma_r is the SMALLEST gap among the remaining
levels): R_r <= D_r/gamma_r, with equality iff ALL remaining tail energy sits at exactly l=r.
The question this script asks -- NOT whether individual E_l decay geometrically, but whether the
Poincare bound applied to the TAIL becomes an increasingly tight approximation as r grows and as
n grows:

    tail_tightness_r(n) := R_r / (D_r/gamma_r)   (in [0,1], =1 means the tail bound is exact)

No new heavy computation needed -- every quantity is already inside the already-verified,
already-committed metrics/l4_ladder_bound_analytic.json (point 21):

    tail_tightness_1 = C_q / naive_bound                  (already tabulated as naive_tightness)
    tail_tightness_2 = (C_q-E_1) / (two_term_bound-E_1)
    tail_tightness_3 = (C_q-E_1-E_2) / (three_term_bound-E_1-E_2)
    tail_tightness_4 = (C_q-E_1-E_2-E_3) / (four_term_bound-E_1-E_2-E_3)

This is the SAME quantity as the already-tabulated naive/two/three/four_term_tightness values
only for r=1 (naive_tightness); for r>=2 it strips away the exact-known prefix to isolate how
tight Poincare is SPECIFICALLY on the tail, rather than on the whole C_q (where the exact prefix
terms dilute the picture). If tail_tightness_r -> 1 as r grows (for fixed n) AND does not degrade
with n (for fixed r) -- that is the uniform-in-n concentration signal the user is asking about.
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def per_layer_tail_tightness(row: dict) -> dict:
    c_q = row["C_q"]
    e1, e2, e3 = row["E1"], row["E2"], row["E3"]

    r1 = c_q
    d1_over_g1 = row["naive_bound"]

    r2 = c_q - e1
    d2_over_g2 = row["two_term_bound"] - e1

    r3 = c_q - e1 - e2
    d3_over_g3 = row["three_term_bound"] - e1 - e2

    r4 = c_q - e1 - e2 - e3
    d4_over_g4 = row["four_term_bound"] - e1 - e2 - e3

    def safe_ratio(num: float, den: float) -> float | None:
        if den <= 0:
            return None
        return num / den

    return {
        "q": row["q"],
        "N": row["N"],
        "C_q": c_q,
        "tail_tightness_1": safe_ratio(r1, d1_over_g1),
        "tail_tightness_2": safe_ratio(r2, d2_over_g2),
        "tail_tightness_3": safe_ratio(r3, d3_over_g3),
        "tail_tightness_4": safe_ratio(r4, d4_over_g4),
        "R_1": r1,
        "R_2": r2,
        "R_3": r3,
        "R_4": r4,
        "D_over_gamma_1": d1_over_g1,
        "D_over_gamma_2": d2_over_g2,
        "D_over_gamma_3": d3_over_g3,
        "D_over_gamma_4": d4_over_g4,
    }


def aggregate_tail_tightness(n: int, per_layer: list[dict]) -> dict:
    """C_q-weighted aggregate, same weighting convention as check_l4_ladder_bound_analytic.py's
    aggregate() -- weight by the binomial probability of landing in layer q under uniform S.
    Aggregates R_r and D_r/gamma_r SEPARATELY (weighted sums of numerator/denominator), then
    takes one ratio at the end -- avoids reconstructing D_r/gamma_r by dividing back through a
    possibly-zero per-layer tail_tightness value."""
    total_r = {r: 0.0 for r in range(1, 5)}
    total_d = {r: 0.0 for r in range(1, 5)}
    for row in per_layer:
        big_n = row["N"]
        q = row["q"]
        w_q = comb(big_n, q) / (2**big_n)
        for r in range(1, 5):
            total_r[r] += w_q * row[f"R_{r}"]
            total_d[r] += w_q * row[f"D_over_gamma_{r}"]
    out = {"n": n}
    for r in range(1, 5):
        out[f"tail_tightness_{r}"] = total_r[r] / total_d[r] if total_d[r] > 0 else None
    return out


if __name__ == "__main__":
    ladder = json.load(open(METRICS / "l4_ladder_bound_analytic.json", encoding="utf-8"))
    per_n_layers = {}
    agg_summary = []
    for n_str, rows in ladder["per_layer"].items():
        n = int(n_str)
        per_layer = [per_layer_tail_tightness(r) for r in rows]
        per_n_layers[n] = per_layer
        agg = aggregate_tail_tightness(n, per_layer)
        agg_summary.append(agg)
        print(
            f"n={n:3d}  tail1={agg['tail_tightness_1']:.4f}  tail2={agg['tail_tightness_2']:.4f}  "
            f"tail3={agg['tail_tightness_3']:.4f}  tail4={agg['tail_tightness_4']:.4f}"
        )

    print("\n=== Trend across n, per tail level r ===")
    for r in range(1, 5):
        vals = [(a["n"], a[f"tail_tightness_{r}"]) for a in agg_summary]
        print(f"  r={r}: " + "  ".join(f"n={n}:{v:.4f}" for n, v in vals))

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "tail_concentration_ratio.json", "w", encoding="utf-8") as f:
        json.dump({"per_layer": per_n_layers, "aggregate": agg_summary}, f, indent=2)
