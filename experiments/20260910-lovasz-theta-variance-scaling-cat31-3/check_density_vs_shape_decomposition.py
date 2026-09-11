"""Localizes the O(1/n) obstruction, per direct user request: decompose

    E[delta^2] = sum_q w_q * (A_q^2 + C_q) = sum_q w_q*A_q^2  +  sum_q w_q*C_q
                                              ^^^^^^^^^^^^^^^     ^^^^^^^^^^^^
                                              "density" part      "shape" part

where w_q = C(m-1,q)/2^(m-1) is the actual probability of landing in Hamming layer q when
picking a uniform random S not containing a fixed i, A_q=E[delta|q], C_q=Var(delta|q),
delta(S)=X(S)-X(S union {i}) (this project's own recomputed decrement, reused unchanged).

B_n = (m/4)*E[delta^2] (already-established identity, decision.md point 12), so

    n^2 * sum_q w_q*A_q^2   vs   n^2 * sum_q w_q*C_q

directly answers which piece drives the growth of n*B_n (hence kappa_n, hence how far V_n is
from a clean C/n law) -- the density-curvature piece (already looking ~O(1) per the
density-response experiment, decision.md point 5) or the shape-heterogeneity piece.

Uses the ALREADY-VALIDATED necklace-orbit-reduction method (check_necklace_orbit_reduction.py,
cross-validated to 8.88e-14 against exhaustive n=23) for ALL prime n in this run, including the
smaller ones (9..25), for internal consistency (same code path throughout, not mixing the
earlier exhaustive-enumeration script with this one).
"""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_mod = importlib.util.spec_from_file_location(
    "necklace_mod", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)

PRIME_N = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


def popcount(x: int) -> int:
    return bin(x).count("1")


def run_one_n(n: int) -> dict:
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))
    n_subsets = 1 << m

    # delta(S) for fixed i=0 (bit 0), over all S not containing bit 0 -- by the already-proved
    # prime-n symmetry (point 4), the choice of which single i is used doesn't matter (A_q, C_q
    # are the same for every i by symmetry); using i=0 only avoids redundant work.
    a_q_sum = np.zeros(m)
    a_q_sq_sum = np.zeros(m)
    a_q_count = np.zeros(m, dtype=np.int64)
    for mask in range(n_subsets):
        if mask & 1:
            continue  # bit 0 must be absent from S
        q = popcount(mask)
        delta = x[mask] - x[mask | 1]
        a_q_sum[q] += delta
        a_q_sq_sum[q] += delta**2
        a_q_count[q] += 1

    a_q = a_q_sum / a_q_count
    e_delta_sq_q = a_q_sq_sum / a_q_count
    c_q = e_delta_sq_q - a_q**2

    w_q = np.array([comb(m - 1, q) / (2 ** (m - 1)) for q in range(m)])
    density_part = float(np.sum(w_q * a_q**2))
    shape_part = float(np.sum(w_q * c_q))
    e_delta_sq_total = density_part + shape_part  # = E[delta^2] overall
    b_n_check = (m / 4) * e_delta_sq_total  # should match B_n from point-7/12 identity

    result = {
        "n": n,
        "m": m,
        "density_part_sum_wq_Aq2": density_part,
        "shape_part_sum_wq_Cq": shape_part,
        "n2_times_density_part": n**2 * density_part,
        "n2_times_shape_part": n**2 * shape_part,
        "shape_fraction_of_Edelta2": shape_part / e_delta_sq_total
        if e_delta_sq_total > 0
        else float("nan"),
        "B_n_from_this_decomposition": b_n_check,
    }
    print(
        f"n={n:3d} m={m:2d} n^2*density={result['n2_times_density_part']:.4f} "
        f"n^2*shape={result['n2_times_shape_part']:.4f} "
        f"shape_frac={result['shape_fraction_of_Edelta2']:.4f} "
        f"B_n_check={b_n_check:.6f}",
        flush=True,
    )
    return result


def run() -> dict:
    rows = [run_one_n(n) for n in PRIME_N]
    print("\n--- summary: n^2*density_part vs n^2*shape_part across prime n ---")
    for r in rows:
        print(
            f"  n={r['n']:3d}  n^2*density={r['n2_times_density_part']:.4f}  "
            f"n^2*shape={r['n2_times_shape_part']:.4f}"
        )
    return {"rows": rows}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "density_vs_shape_decomposition.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
