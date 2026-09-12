"""Exam 2, stage B: exact E_3 at the q=3,N-3 boundary layers, via the SAME zero-residual trick
used for E_2 at q=2,N-2 (point 18's decisive resolution) -- extended one rung, not re-derived
from scratch.

At q=3 (or q=N-3), min(q,N-q)=3, so the Johnson-scheme eigenspace decomposition has ONLY
l=1,2,3 -- no V_4 or higher exists at that layer. Combined with verify_l2_projection_rigorous.py's
now-verified fact that h(S)=f_centered(S)-P_1(S)-P_2(S) is EXACTLY orthogonal to V_0,V_1,V_2 (to
~1e-17), this gives an EXACT identity at these boundary layers:

    C_q = E_1 + E_2 + Var(h)   ALWAYS (spectral decomposition -- true at every q)
    Var(h) = E_3 + E_4 + ...   ALWAYS
    at q=3,N-3: only l=1,2,3 exist  =>  Var(h) = E_3 exactly, no higher-order contamination

So E_3 = C_q - E_1 - E_2 at q=3,N-3 requires NO new triple-centering formula -- it falls out of
what verify_l2_projection_rigorous.py already proved. This is deliberately NOT an attempt at the
general interior-layer E_3(q) formula (which needs triple-centering, a genuinely harder
derivation, flagged as the higher-risk part of Exam 2) -- it is the cheapest differentiating test
for Exam 2's actual question: does the ladder's excess-growth-halving pattern (91.3pp -> 69.3pp
-> 32.8pp from naive -> two-term -> three-term, per decision.md point 18) continue at a fourth
rung, using E_3 values that are exact, not approximated.

Cross-validated against exact diagonalization (n=23,29,31) via metrics/johnson_eigenspace_
decomposition.json, matching the l=3 eigenspace by the Eberlein formula lambda_j=(q-j)(N-q-j)-j
at j=3 (same pattern used by verify_l2_analytic_against_diagonalization.py for j=1,2).
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
    "necklace_mod_l3boundary", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)

l2a_spec = importlib.util.spec_from_file_location(
    "l2_analytic_for_l3boundary", HERE / "check_l2_analytic_projection.py"
)
l2a = importlib.util.module_from_spec(l2a_spec)
l2a_spec.loader.exec_module(l2a)


def e3_at_boundary(n: int) -> list[dict]:
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

    pairs = list(combinations(range(big_n), 2))
    rows = []
    for q in sorted({3, big_n - 3}):
        if q < 3 or big_n - q < 3:
            continue  # V_3 doesn't exist / layer too small
        subsets = list(combinations(ground, q))
        masks = np.array([sum(1 << b for b in s) for s in subsets])
        f = delta[masks]
        c_q = float(np.var(f))
        v = len(subsets)
        f_centered = f - f.mean()

        big_e = np.zeros((v, big_n))
        for row_idx, s in enumerate(subsets):
            big_e[row_idx, [ground.index(g) for g in s]] = 1.0
        x_centered = big_e - q / big_n

        mu_e = big_e.T @ f_centered / v
        c1 = mu_e * big_n * (big_n - 1) / (q * (big_n - q))
        p1f = x_centered @ c1
        e1 = float(np.mean(p1f**2))

        m_full = (big_e * f_centered[:, None]).T @ big_e / v
        mu_pairs = np.array([m_full[a, b] for a, b in pairs])
        e2 = l2a.e2_analytic(big_n, q, mu_pairs, pairs)

        lam2 = (
            q
            * (q - 1)
            * (big_n - q)
            * (big_n - q - 1)
            / (big_n * (big_n - 1) * (big_n - 2) * (big_n - 3))
        )
        s_row = np.zeros(big_n)
        for (a, b), mu in zip(pairs, mu_pairs):
            s_row[a] += mu
            s_row[b] += mu
        big_s = float(np.sum(mu_pairs))
        r = np.array(
            [
                mu_pairs[i]
                - (s_row[a] + s_row[b]) / (big_n - 2)
                + 2 * big_s / ((big_n - 1) * (big_n - 2))
                for i, (a, b) in enumerate(pairs)
            ]
        )
        d_coef = r / lam2
        big_e_pair = np.zeros((v, len(pairs)))
        for i, (a, b) in enumerate(pairs):
            big_e_pair[:, i] = big_e[:, a] * big_e[:, b]
        y_ab = (
            big_e_pair
            - (q - 1)
            / (big_n - 2)
            * (big_e[:, [a for a, b in pairs]] + big_e[:, [b for a, b in pairs]])
            + q * (q - 1) / ((big_n - 1) * (big_n - 2))
        )
        p2f = y_ab @ d_coef

        h = f_centered - p1f - p2f
        var_h = float(np.mean(h**2))
        e3_via_var_h = var_h
        e3_via_subtraction = c_q - e1 - e2
        residual_at_boundary = abs(e3_via_var_h - e3_via_subtraction)

        rows.append(
            {
                "n": n,
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "E1": e1,
                "E2": e2,
                "E3_via_var_h": e3_via_var_h,
                "E3_via_subtraction": e3_via_subtraction,
                "boundary_residual": residual_at_boundary,
                "E3_frac_of_Cq": e3_via_var_h / c_q if c_q > 0 else float("nan"),
            }
        )
        print(
            f"n={n:3d} q={q:2d}/{big_n:2d}  C_q={c_q:.8f}  E1={e1:.8f}  E2={e2:.8f}  "
            f"E3(var_h)={e3_via_var_h:.8f}  E3(subtract)={e3_via_subtraction:.8f}  "
            f"boundary_residual={residual_at_boundary:.2e}  "
            f"E3/C_q={e3_via_var_h / c_q:.4f}",
            flush=True,
        )
    return rows


def cross_check_diagonalization(rows: list[dict], tol: float = 1e-9) -> list[dict]:
    """For n in {23,29,31}, match E3 against the l=3 eigenspace energy from the already-persisted
    exact diagonalization (metrics/johnson_eigenspace_decomposition.json)."""
    eig_data = json.load(open(METRICS / "johnson_eigenspace_decomposition.json", encoding="utf-8"))
    out = []
    for row in rows:
        n_str = str(row["n"])
        if n_str not in eig_data:
            continue
        q, big_n = row["q"], row["N"]
        d = q * (big_n - q)
        j = 3
        if q - j < 0 or big_n - q - j < 0:
            continue
        lam_theory = ((q - j) * (big_n - q - j) - j) / d
        layer = next((lyr for lyr in eig_data[n_str] if lyr["q"] == q), None)
        if layer is None:
            continue
        e3_diag = None
        for lvl in layer["levels"]:
            if abs(lvl["lambda"] - lam_theory) < 1e-6:
                e3_diag = lvl["energy"]
                break
        match = abs(e3_diag - row["E3_via_var_h"]) < tol if e3_diag is not None else None
        out.append(
            {
                "n": row["n"],
                "q": q,
                "e3_diag": e3_diag,
                "e3_formula": row["E3_via_var_h"],
                "match": match,
            }
        )
        e3_formula = row["E3_via_var_h"]
        print(
            f"  n={row['n']:3d} q={q:2d}  E3_diag={e3_diag}  E3_formula={e3_formula:.10f}  "
            f"match={match}"
        )
    return out


if __name__ == "__main__":
    all_rows = []
    for n in [23, 29, 31, 37, 41, 43, 47]:
        print(f"\n--- n={n} ---")
        all_rows.extend(e3_at_boundary(n))

    print("\n=== Cross-check against exact diagonalization (n=23,29,31) ===")
    diag_rows = cross_check_diagonalization(all_rows)

    boundary_violations = [r for r in all_rows if r["boundary_residual"] > 1e-9]
    diag_violations = [r for r in diag_rows if r["match"] is False]

    out = {
        "e3_boundary": all_rows,
        "diagonalization_cross_check": diag_rows,
        "boundary_violations": boundary_violations,
        "diagonalization_violations": diag_violations,
    }
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l3_boundary_energy.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"\nBoundary (Var(h)==C_q-E1-E2) violations: {len(boundary_violations)}/{len(all_rows)}")
    print(f"Diagonalization violations: {len(diag_violations)}/{len(diag_rows)}")
