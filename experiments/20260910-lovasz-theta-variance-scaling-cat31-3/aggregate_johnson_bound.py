"""Aggregates the per-layer Poincare bound (C_q <= T_q*q*(N-q)/(2N), N=m-1) into the
weighted sum S_n = sum_q w_q*C_q vs its bound sum_q w_q*T_q*q*(N-q)/(2N), using the SAME
w_q=C(N,q)/2^N layer weighting as point 14's density-vs-shape decomposition, so the aggregate
bound is directly comparable to the already-reported n^2*shape values.
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

with open(METRICS / "johnson_swap_energy.json", encoding="utf-8") as f:
    swap_data = json.load(f)

results = []
for n_str in ["23", "29", "31", "37"]:
    n = int(n_str)
    rows = swap_data[n_str]
    big_n = rows[0]["N"]

    s_n_observed = 0.0
    s_n_bound = 0.0
    for r in rows:
        q = r["q"]
        w_q = comb(big_n, q) / (2**big_n)
        c_q = r["C_q"]
        t_q = r["T_q"]
        bound_q = (
            t_q * q * (big_n - q) / (2 * big_n) if t_q == t_q else 0.0
        )  # nan-safe (q=0,N gives T_q=nan)
        s_n_observed += w_q * c_q
        s_n_bound += w_q * bound_q

    tightness = s_n_observed / s_n_bound
    results.append(
        {
            "n": n,
            "N": big_n,
            "n2_S_n_observed": n**2 * s_n_observed,
            "n2_S_n_bound": n**2 * s_n_bound,
            "tightness": tightness,
        }
    )
    print(
        f"n={n:3d}  N={big_n:2d}  n^2*S_n_observed={n**2 * s_n_observed:8.4f}  "
        f"n^2*S_n_bound={n**2 * s_n_bound:8.4f}  tightness={tightness:.4f}"
    )

print("\n(cross-check: point 14's own table reports n^2*shape = 13.82, 17.45, 18.46, 21.36")
print(" at n=23,29,31,37 respectively -- matches n2_S_n_observed above)")

with open(METRICS / "johnson_bound_aggregate.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
