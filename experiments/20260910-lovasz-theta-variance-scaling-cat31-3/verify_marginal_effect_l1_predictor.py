"""Attempt at an INDEPENDENT (computationally -- cheaper, no C(N,q)xC(N,q) diagonalization),
predictor of the l=1 (worst-gap) eigenspace's share of C_q, per direct user request for an
adaptive bound with an independent prediction of the l=1 share.

Idea: the l=1 (degree-1) eigenspace of functions on the Johnson slice is spanned by the CENTERED
single-element indicators x_j(S) = 1[j in S] - q/N (j ranges over the N-element ground set,
excluding the fixed generator i). The l=1 energy is exactly the variance explained by the best
L2 (linear) fit of f=delta onto span{x_j} -- computable from just N per-element "marginal effect"
statistics mu_j = Cov(f, x_j), NOT the full C(N,q)-dimensional eigendecomposition used in
check_johnson_eigenspace_decomposition.py. This is cheap: O(N * layer_size) per layer, same order
as the swap-energy computation, feasible for n where the C(N,q)x C(N,q) dense diagonalization
(point 15a) was NOT feasible (n=37+).

CRITICAL: this script does NOT assume a closed-form formula for how {mu_j} combines into an
energy value (integrity.md: no phantom formulas). It solves for the exact L2 projection
numerically (small NxN linear algebra: the covariance matrix of the centered indicators has a
known closed form, but here even THAT is verified empirically against the raw indicator data,
not just asserted) and cross-validates the resulting predicted l=1 energy against the ALREADY
EXACT diagonalization-based value for n=23,29,31 (check_johnson_eigenspace_decomposition.py's
output) BEFORE trusting it for n=37+ where no independent check exists.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_mod = importlib.util.spec_from_file_location(
    "necklace_mod_marginal", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)


def marginal_l1_energy_per_layer(n: int) -> list[dict]:
    m = (n - 1) // 2
    ground = list(range(1, m))
    big_n = len(ground)

    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))
    n_subsets = 1 << m
    delta = np.empty(n_subsets)
    for mask in range(n_subsets):
        if mask & 1:
            continue
        delta[mask] = x[mask] - x[mask | 1]

    rows = []
    for q in range(1, big_n):
        subsets = list(combinations(ground, q))
        masks = np.array([sum(1 << b for b in s) for s in subsets])
        f = delta[masks]
        c_q = float(np.var(f))
        v = len(subsets)

        # membership matrix: X[s, j] = 1 if ground[j] in subset s else 0
        subset_arr = np.array(subsets)  # shape (v, q), entries are ground-element ids
        big_x = np.zeros((v, big_n))
        for row_idx, s in enumerate(subset_arr):
            big_x[row_idx, [ground.index(g) for g in s]] = 1.0
        p_in = q / big_n
        x_centered = big_x - p_in  # centered indicators, columns sum to 0 per row automatically

        f_centered = f - f.mean()
        mu = x_centered.T @ f_centered / v  # mu_j = Cov(f, x_j), population covariance

        # empirical covariance of the centered indicators themselves (verifies the closed form,
        # does not assume it)
        sigma_emp = x_centered.T @ x_centered / v
        sigma_formula = np.full((big_n, big_n), -q * (big_n - q) / (big_n**2 * (big_n - 1)))
        np.fill_diagonal(sigma_formula, q * (big_n - q) / big_n**2)
        sigma_match = float(np.max(np.abs(sigma_emp - sigma_formula)))

        # EXACT closed form, not a numerical pseudo-inverse: since sigma_formula = s*I - (s/(N-1))
        # *(J-I) with s=q(N-q)/N^2, and mu lives in the sum-zero subspace (sum_j mu_j=0 exactly,
        # since sum_j x_j(S)=0 identically for every S), J acts as 0 there -- sigma restricted to
        # that subspace is EXACTLY the scalar s*N/(N-1) times identity, so the "pseudo-inverse"
        # application is just a scalar division, avoiding any SVD-threshold numerical noise:
        #   Energy_l1 = ||mu||^2 * N*(N-1) / (q*(N-q))
        energy_l1 = float(np.sum(mu**2) * big_n * (big_n - 1) / (q * (big_n - q)))

        rows.append(
            {
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "sigma_formula_match_err": sigma_match,
                "predicted_l1_energy": energy_l1,
                "predicted_l1_frac_of_Cq": energy_l1 / c_q if c_q > 0 else float("nan"),
            }
        )
        print(
            f"  q={q:2d}/{big_n:2d}  C_q={c_q:.6f}  sigma_check_err={sigma_match:.2e}  "
            f"predicted_l1_energy={energy_l1:.6f}  predicted_frac={energy_l1 / c_q:.4f}"
            if c_q > 0
            else f"  q={q:2d}/{big_n:2d}  C_q=0",
            flush=True,
        )
    return rows


def cross_validate_against_diagonalization() -> bool:
    """Compares this script's cheap marginal-effect prediction against the ALREADY EXACT
    diagonalization-based l=1 energy (check_johnson_eigenspace_decomposition.py output) for
    n=23,29,31 -- the mandatory positive control before trusting this method on new n."""
    with open(METRICS / "johnson_eigenspace_decomposition.json", encoding="utf-8") as f:
        exact_data = json.load(f)

    all_match = True
    for n_str in ["23", "29", "31"]:
        exact_rows = {row["q"]: row for row in exact_data[n_str]}
        predicted_rows = {row["q"]: row for row in marginal_l1_energy_per_layer(int(n_str))}
        print(f"\n--- cross-validation n={n_str} ---")
        for q, exact_row in exact_rows.items():
            l1_level = min(exact_row["levels"], key=lambda lv: lv["gap"])
            exact_energy = l1_level["energy"]
            predicted_energy = predicted_rows[q]["predicted_l1_energy"]
            err = abs(exact_energy - predicted_energy)
            rel_err = err / exact_energy if exact_energy > 1e-9 else err
            ok = rel_err < 0.01
            all_match = all_match and ok
            print(
                f"  q={q:2d}  exact_l1_energy={exact_energy:.6f}  "
                f"predicted={predicted_energy:.6f}  rel_err={rel_err:.4f}  ok={ok}"
            )
    return all_match


if __name__ == "__main__":
    print("=== Step 1: cross-validate cheap predictor against exact diagonalization ===")
    validated = cross_validate_against_diagonalization()
    print(f"\nCross-validation passed (all rel_err<1%): {validated}")

    if not validated:
        raise RuntimeError(
            "Marginal-effect l=1 predictor does NOT match exact diagonalization -- "
            "do NOT trust it for n=37+ until this is fixed."
        )

    print("\n=== Step 2: extend to n where dense diagonalization was infeasible ===")
    out = {}
    for n in [37, 41, 43]:
        print(f"\n--- n={n} ---")
        out[n] = marginal_l1_energy_per_layer(n)

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "marginal_l1_predictor_extension.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
