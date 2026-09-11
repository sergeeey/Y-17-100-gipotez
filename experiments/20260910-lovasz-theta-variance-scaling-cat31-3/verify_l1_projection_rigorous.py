"""Rigorous, diagonalization-free verification of the l=1 (degree-1) projection of delta on the
Johnson slice, per a pasted external analysis's proposed algebraic check. Removes eigenvalue-
grouping ambiguity from the trust chain entirely: instead of comparing point 15b's closed-form
Energy_l1 against check_johnson_eigenspace_decomposition.py's diagonalization+grouping result,
this constructs the ACTUAL projection function P_1(f) and verifies its defining properties
directly against the raw exact delta data:

  1. E[(P_1 f)^2] == Energy_l1 (the closed-form scalar from verify_marginal_effect_l1_predictor.py)
  2. E[(f - P_1 f) * x_j] ~= 0 for every ground element j (orthogonality of the residual to the
     degree-1 subspace -- this is what "P_1 f is really the orthogonal projection" MEANS)

Specifically re-checks the two layers that showed ~1% discrepancy in the earlier numerical
pseudo-inverse approach (n=29,q=5 and n=31,q=2) to settle whether that was diagonalization-
grouping noise (this experiment's hypothesis) or a real formula issue.
"""

from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

necklace_mod = importlib.util.spec_from_file_location(
    "necklace_mod_proj", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)


def rigorous_check(n: int, q_values: list[int] | None = None) -> None:
    m = (n - 1) // 2
    ground = list(range(1, m))
    big_n = len(ground)

    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x_arr = np.log(theta_full / np.sqrt(n))
    n_subsets = 1 << m
    delta = np.empty(n_subsets)
    for mask in range(n_subsets):
        if mask & 1:
            continue
        delta[mask] = x_arr[mask] - x_arr[mask | 1]

    layers = q_values if q_values is not None else range(1, big_n)
    for q in layers:
        subsets = list(combinations(ground, q))
        masks = np.array([sum(1 << b for b in s) for s in subsets])
        f = delta[masks]
        c_q = float(np.var(f))
        v = len(subsets)

        big_x = np.zeros((v, big_n))
        for row_idx, s in enumerate(subsets):
            big_x[row_idx, [ground.index(g) for g in s]] = 1.0
        p_in = q / big_n
        x_centered = big_x - p_in

        f_centered = f - f.mean()
        mu = x_centered.T @ f_centered / v
        energy_closed_form = float(np.sum(mu**2) * big_n * (big_n - 1) / (q * (big_n - q)))

        # build the ACTUAL projection function: c_j = mu_j * N(N-1)/(q(N-q)), P1f = X_centered @ c
        c = mu * big_n * (big_n - 1) / (q * (big_n - q))
        p1f = x_centered @ c  # shape (v,), the actual projected function values

        energy_direct = float(np.mean(p1f**2))  # E[(P_1 f)^2]

        residual = f_centered - p1f
        # orthogonality: E[(f - P_1 f) * x_j] for every ground element j
        orth = (x_centered.T @ residual) / v
        max_orth_violation = float(np.max(np.abs(orth)))

        match_energy = abs(energy_direct - energy_closed_form) < 1e-9
        print(
            f"n={n:3d} q={q:2d}/{big_n:2d}  C_q={c_q:.6f}  "
            f"closed_form_energy={energy_closed_form:.8f}  "
            f"direct_E[(P1f)^2]={energy_direct:.8f}  match={match_energy}  "
            f"max|orthogonality_violation|={max_orth_violation:.2e}",
            flush=True,
        )


if __name__ == "__main__":
    print("=== n=23, all layers ===")
    rigorous_check(23)
    print("\n=== n=29, focus on previously-discrepant q=5 (and neighbors) ===")
    rigorous_check(29, q_values=[4, 5, 6])
    print("\n=== n=31, focus on previously-discrepant q=2 (and neighbors) ===")
    rigorous_check(31, q_values=[1, 2, 3])
