"""Verification script for point 44 (skeptic-fallback review finding): is U_6 (the truncated-
moment LP's maximization result, which R_s/point 44's whole conclusion rests on) a genuine,
solver-independent quantity, or could it be a numerical-conditioning artifact?

Two checks:
1. n=29 (L=6=s): the moment-equality system is SQUARE (6 equations, 6 unknowns) -- if the
   Vandermonde-like matrix A[r,l]=gamma_l^r is invertible, there is a UNIQUE feasible spectrum,
   and U_6 must equal that unique point's sum exactly (up to floating point). Solved directly
   via numpy.linalg.solve (bypassing the LP solver entirely) and compared against the committed
   script's own LP result.
2. n=47 (L=11, the most under-determined case in this experiment's range): U_6 compared across
   three different scipy.optimize.linprog methods (highs, highs-ds, highs-ipm) -- genuine
   agreement across independent algorithms is strong evidence U_6 itself is not a solver
   artifact (a SEPARATE, unrelated finding from this same review pass: the companion L_s
   (minimize direction) DID show a ~4e-6 discrepancy at n=29's exact point, evidently a
   solver-side artifact specific to that direction -- this does NOT affect U_s/R_s, which is
   all point 44's conclusion depends on).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent

lp_spec = importlib.util.spec_from_file_location(
    "lp_mod_robustness", HERE / "check_truncated_moment_lp_bound.py"
)
lpmod = importlib.util.module_from_spec(lp_spec)
lp_spec.loader.exec_module(lpmod)


def check_exact_square_system(rows: dict, n: int) -> None:
    row = rows[n]
    N, q = row["N"], row["q"]
    gammas = lpmod.gamma_l_array(N, q)
    L = len(gammas)
    moments = [row[f"M{r}"] for r in range(1, 7)]
    print(f"n={n}: N={N} q={q} L={L} (square system iff L==6)", flush=True)

    A = np.vstack([gammas**r for r in range(1, 7)])
    b = np.array(moments)
    cond = np.linalg.cond(A)
    E_exact = np.linalg.solve(A, b)
    C_q_exact = float(np.sum(E_exact))
    print(f"  cond(A) = {cond:.3e}, all E_l >= 0: {np.all(E_exact >= -1e-12)}")
    print(f"  C_q via direct solve = {C_q_exact:.12f}, reported C_q = {row['C_q']:.12f}")
    print(f"  |direct_solve - reported| = {abs(C_q_exact - row['C_q']):.3e}")

    res = lpmod.solve_moment_lp(gammas, moments, maximize=True)
    print(f"  LP (highs) U_6 = {res['value']:.12f}")
    print(f"  |LP - direct_solve| = {abs(res['value'] - C_q_exact):.3e}", flush=True)


def check_solver_method_robustness(rows: dict, n: int) -> None:
    row = rows[n]
    N, q = row["N"], row["q"]
    gammas = lpmod.gamma_l_array(N, q)
    L = len(gammas)
    moments = [row[f"M{r}"] for r in range(1, 7)]
    A_eq = np.vstack([gammas**r for r in range(1, 7)])
    b_eq = np.array(moments)

    default = lpmod.solve_moment_lp(gammas, moments, maximize=True)["value"]
    ds = -linprog(-np.ones(L), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * L, method="highs-ds").fun
    ipm = -linprog(
        -np.ones(L), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * L, method="highs-ipm"
    ).fun
    spread = max(default, ds, ipm) - min(default, ds, ipm)
    print(f"n={n}: L={L} (under-determined, L>6)", flush=True)
    print(f"  U_6: highs={default:.10f} highs-ds={ds:.10f} highs-ipm={ipm:.10f}")
    print(f"  spread across methods = {spread:.3e}, C_q actual = {row['C_q']:.10f}", flush=True)


if __name__ == "__main__":
    with open(HERE / "metrics" / "higher_moments_M1_M6.json", encoding="utf-8") as f:
        all_rows = {r["n"]: r for r in json.load(f)["rows"]}

    print("=== Check 1: exact square system (n=29, L=6=s) ===", flush=True)
    check_exact_square_system(all_rows, 29)

    print("\n=== Check 2: solver-method robustness (n=47, L=11>s=6) ===", flush=True)
    check_solver_method_robustness(all_rows, 47)
