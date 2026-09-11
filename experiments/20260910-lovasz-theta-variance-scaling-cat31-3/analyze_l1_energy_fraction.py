"""Follow-up to check_johnson_eigenspace_decomposition.py: specifically extracts the l=1
level's (the PROVEN worst-gap eigenspace, gap=N/(q(N-q)) from point 15) share of C_q's
variance, across all q and both tested n. If this fraction is small and roughly consistent,
it suggests a real STRUCTURAL suppression of the worst-gap eigenspace -- analogous to point
11's proved vanishing-even-Fourier-levels theorem on the Boolean cube -- not just noise.
"""

import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

with open(METRICS / "johnson_eigenspace_decomposition.json", encoding="utf-8") as f:
    data = json.load(f)

for n_str, rows in data.items():
    n = int(n_str)
    print(f"\n--- n={n} ---")
    for row in rows:
        q = row["q"]
        big_n = row["N"]
        expected_gap_l1 = big_n / (q * (big_n - q))
        # l=1 is the level with the SMALLEST gap (worst, provably matches N/(q(N-q)))
        l1_level = min(row["levels"], key=lambda lv: lv["gap"])
        matches_formula = abs(l1_level["gap"] - expected_gap_l1) < 1e-4
        print(
            f"  q={q:2d}/{big_n:2d}  l1_gap_observed={l1_level['gap']:.4f}  "
            f"l1_gap_formula={expected_gap_l1:.4f}  match={matches_formula}  "
            f"l1_frac_of_Cq={l1_level['frac_of_var']:.4f}"
        )

    # aggregate: what fraction of the WEIGHTED S_n (point-14 style w_q) sits in l=1 vs rest?
    total_w = 0.0
    l1_weighted = 0.0
    for row in rows:
        q = row["q"]
        big_n = row["N"]
        w_q = comb(big_n, q) / (2**big_n)
        l1_level = min(row["levels"], key=lambda lv: lv["gap"])
        total_w += w_q * row["C_q"]
        l1_weighted += w_q * l1_level["frac_of_var"] * row["C_q"]
    print(
        f"  AGGREGATE: fraction of weighted S_n sitting in l=1 (worst-gap) level = "
        f"{l1_weighted / total_w:.4f}"
    )
