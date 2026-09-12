"""Persisted, re-runnable verification for check_l2_analytic_projection.py's docstring claim
(flagged by reviewer agent 2026-09-12: the claim of exact-diagonalization + zero-residual
verification existed only as an unpersisted in-session check, not as a repo artifact -- per
audit-verification-gate.md, a claim's own [VERIFIED] is the next reader's [INFERRED] unless the
check is actually in the repo to re-run).

Two independent checks, both against artifacts already on disk (no new expensive diagonalization
run here -- metrics/johnson_eigenspace_decomposition.json already persists exact diagonalization
+ projection results for n=23,29,31 from point 15a's work):

1. Exact-diagonalization cross-check (n=23,29,31): for each (q,N) layer in
   metrics/johnson_eigenspace_decomposition.json, identify the l=1 and l=2 eigenspace energies by
   matching against the Eberlein eigenvalue formula lambda_j=(q-j)(N-q-j)-j (verified 34/34 exact
   in point 15's own work), then compare against e1_closed_form/e2_analytic computed fresh from
   the same theta data via check_l2_analytic_projection.py's functions.

2. Zero-residual unit test (all 7 tested n): at q=2 and q=N-2, min(q,N-q)=2 means l=1,2 are the
   ONLY nontrivial levels, so E1+E2 must equal C_q exactly. Reads the already-committed
   metrics/l3_ladder_bound_analytic.json (which carries E1,E2,C_q per layer from the same
   e1_closed_form/e2_analytic functions) rather than recomputing.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

analytic_mod_spec = importlib.util.spec_from_file_location(
    "l2_analytic_for_verify", HERE / "check_l2_analytic_projection.py"
)
l2a = importlib.util.module_from_spec(analytic_mod_spec)
analytic_mod_spec.loader.exec_module(l2a)

necklace_mod = importlib.util.spec_from_file_location(
    "necklace_mod_verify_l2", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)


def _mu_e_and_pairs(n: int, q: int) -> tuple[int, np.ndarray, np.ndarray, list[tuple[int, int]]]:
    """Rebuild mu_e/mu_pairs for one (n, q) layer -- mirrors
    check_l2_analytic_projection.l2_energy_per_layer's inner loop body for a single q, so the
    analytic E1/E2 fed into this check come from the exact same code path as production use."""
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

    subsets = list(combinations(ground, q))
    masks = np.array([sum(1 << b for b in s) for s in subsets])
    f = delta[masks]
    v = len(subsets)
    f_centered = f - f.mean()

    big_e = np.zeros((v, big_n))
    for row_idx, s in enumerate(subsets):
        big_e[row_idx, [ground.index(g) for g in s]] = 1.0

    mu_e = big_e.T @ f_centered / v
    m_full = (big_e * f_centered[:, None]).T @ big_e / v
    pairs = list(combinations(range(big_n), 2))
    mu_pairs = np.array([m_full[a, b] for a, b in pairs])
    return big_n, mu_e, mu_pairs, pairs


def check_against_diagonalization(tol: float = 1e-9) -> list[dict]:
    eig_data = json.load(open(METRICS / "johnson_eigenspace_decomposition.json", encoding="utf-8"))
    rows = []
    for n_str, layers in eig_data.items():
        n = int(n_str)
        for layer in layers:
            q, big_n = layer["q"], layer["N"]
            d = q * (big_n - q)

            def eberlein_energy(j: int) -> float | None:
                if j > 0 and (q - j < 0 or big_n - q - j < 0):
                    return None
                lam_theory = ((q - j) * (big_n - q - j) - j) / d
                for lvl in layer["levels"]:
                    if abs(lvl["lambda"] - lam_theory) < 1e-6:
                        return lvl["energy"]
                return None

            e1_diag = eberlein_energy(1)
            e2_diag = eberlein_energy(2)
            if e1_diag is None and e2_diag is None:
                continue

            _, mu_e, mu_pairs, pairs = _mu_e_and_pairs(n, q)
            e1_formula = l2a.e1_closed_form(big_n, q, mu_e)
            e2_formula = l2a.e2_analytic(big_n, q, mu_pairs, pairs)

            row = {
                "n": n,
                "q": q,
                "N": big_n,
                "e1_diag": e1_diag,
                "e1_formula": e1_formula,
                "e1_match": (abs(e1_diag - e1_formula) < tol if e1_diag is not None else None),
                "e2_diag": e2_diag,
                "e2_formula": e2_formula,
                "e2_match": (abs(e2_diag - e2_formula) < tol if e2_diag is not None else None),
            }
            rows.append(row)
            print(
                f"  n={n:3d} q={q:2d}  E1: diag={row['e1_diag']} formula={e1_formula:.10f} "
                f"match={row['e1_match']}  E2: diag={row['e2_diag']} formula={e2_formula:.10f} "
                f"match={row['e2_match']}",
                flush=True,
            )
    return rows


def check_zero_residual(tol: float = 1e-9) -> list[dict]:
    ladder = json.load(open(METRICS / "l3_ladder_bound_analytic.json", encoding="utf-8"))
    rows = []
    for n_str, layers in ladder["per_layer"].items():
        for layer in layers:
            q, big_n = layer["q"], layer["N"]
            if q not in (2, big_n - 2):
                continue
            e1, e2, c_q = layer["E1"], layer["E2"], layer["C_q"]
            residual = abs(e1 + e2 - c_q)
            rows.append(
                {
                    "n": int(n_str),
                    "q": q,
                    "N": big_n,
                    "E1": e1,
                    "E2": e2,
                    "C_q": c_q,
                    "residual": residual,
                    "zero_residual_holds": residual < tol,
                }
            )
    return rows


if __name__ == "__main__":
    print("=== Check 1: analytic E1/E2 vs exact diagonalization (n=23,29,31) ===")
    diag_rows = check_against_diagonalization()
    diag_violations = [r for r in diag_rows if r["e1_match"] is False or r["e2_match"] is False]

    print("\n=== Check 2: zero-residual unit test E1+E2=C_q at q in {2,N-2} (all 7 n) ===")
    zr_rows = check_zero_residual()
    for r in zr_rows:
        holds = r["zero_residual_holds"]
        print(f"  n={r['n']:3d} q={r['q']:2d}  residual={r['residual']:.3e}  holds={holds}")
    zr_violations = [r for r in zr_rows if not r["zero_residual_holds"]]

    out = {
        "diagonalization_check": diag_rows,
        "diagonalization_violations": diag_violations,
        "zero_residual_check": zr_rows,
        "zero_residual_violations": zr_violations,
    }
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l2_analytic_verification.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"\nDiagonalization violations: {len(diag_violations)}/{len(diag_rows)}")
    print(f"Zero-residual violations:   {len(zr_violations)}/{len(zr_rows)}")
