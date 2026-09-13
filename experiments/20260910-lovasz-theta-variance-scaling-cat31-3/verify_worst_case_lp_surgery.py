"""Point 47 (surgery correction of Point 46): direct test of an explicit external claim that
Point 46's "s(L) unbounded within s<=20" conclusion is a numerical artifact of monomial-basis
ill-conditioning, and that a Chebyshev dual certificate proves

    K_s(L) <= (A_s+1)/(A_s-1),   A_s = T_s((L+3)/(L-1))

giving s_2(L) = O(sqrt(L)) (specifically s_2(100)=7, s_2(250)=10, s_2(500)=14, s_2(1000)=20).

This script:
  1. Reformulates the Point 46 two-spectrum LP on a rescaled monomial basis (gamma / gamma_max)
     -- mathematically IDENTICAL feasible region to the raw-monomial LP (dividing constraint row
     r by gamma_max^r does not change the "=0" equation), but avoids the gross row-magnitude
     mismatch that made the naive Chebyshev-basis attempt (verify_chebyshev_conditioning.py,
     scratchpad) return spurious "Unbounded" -- that attempt is independently diagnosed as
     containing a real formulation bug (even-degree Chebyshev polynomials carry a nonzero T_0
     "sum(y)" term that the plain rows-1..s constraint set does not pin down, so it does NOT
     enforce the same moment-matching condition as the monomial rows -- this is a change of the
     constraint SET, not a conditioning fix, and its results must not be used).
  2. Cross-checks the optimum with TWO different linprog methods (highs-ds, highs-ipm) at every
     (L, s) cell -- disagreement is recorded explicitly, never silently resolved.
  3. Computes the Chebyshev certificate bound (A_s+1)/(A_s-1) for direct comparison.
  4. Checks K_{s+1} <= K_s monotonicity (diagnostic only -- the true optimum must be
     non-increasing in s, so an observed increase flags solver sub-optimality, not a
     mathematical violation).
  5. Any LP failure is recorded as INCONCLUSIVE for that cell, never silently substituted or
     treated as a threshold value (Oracle Adequacy Gate discipline).

Feasibility of the reported optimum is independently re-checked in 50-digit precision
(mpmath) for a representative subset of cells (every L, at s=1 as a sanity anchor and at the
largest s reached) -- full mpmath verification at every cell would be prohibitively slow, but
the anchor points are enough to establish whether "returned feasible" claims from HiGHS are
trustworthy at this L/s range (see decision.md Point 47 for the full argument).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from mpmath import fsum, mp, mpf
from numpy.polynomial import chebyshev as C
from scipy.optimize import linprog

mp.dps = 50

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

L_VALUES = [25, 50, 100, 250, 500, 1000]
S_MAX = 30
METHODS = ["highs-ds", "highs-ipm"]


def gamma_l_array(N: int, q: int) -> np.ndarray:
    L = min(q, N - q)
    ls = np.arange(1, L + 1)
    return ls * (N + 1 - ls) / (q * (N - q))


TIGHT_TOL = 1e-9


def solve_rescaled(gammas: np.ndarray, s: int, method: str, tol: float | None = TIGHT_TOL) -> dict:
    """Solve the rescaled-monomial two-spectrum LP. Default uses a tightened HiGHS feasibility
    tolerance (1e-9) -- empirically found (verify_ipm_feasibility.py /
    check_tolerance_sensitivity.py, scratchpad) to make highs-ds and highs-ipm CONVERGE to the
    same value to 6+ significant digits at cells where the default tolerance leaves them
    disagreeing by up to 40%. This is treated as the trustworthy regime; default-tolerance
    disagreement is itself evidence that a value should not be reported without this
    tightening."""
    L = len(gammas)
    n_vars = 2 * L
    g_resc = gammas / gammas.max()
    c = np.concatenate([np.zeros(L), -np.ones(L)])
    row_norm = np.concatenate([np.ones(L), np.zeros(L)])
    rows_moment = [np.concatenate([g_resc**r, -(g_resc**r)]) for r in range(1, s + 1)]
    A_eq = np.vstack([row_norm, *rows_moment])
    b_eq = np.concatenate([[1.0], np.zeros(s)])
    options = {}
    if tol is not None:
        options = {"primal_feasibility_tolerance": tol, "dual_feasibility_tolerance": tol}
    res = linprog(
        c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * n_vars, method=method, options=options
    )
    if not res.success:
        return {"success": False, "message": res.message}
    return {"success": True, "K_s": float(-res.fun), "x": res.x[:L], "y": res.x[L:]}


def chebyshev_certificate_bound(L: int, s: int) -> float:
    x = (L + 3) / (L - 1)
    coeffs = np.zeros(s + 1)
    coeffs[s] = 1.0
    A_s = C.chebval(x, coeffs)
    return float((A_s + 1) / (A_s - 1))


def high_precision_feasibility_check(
    gammas: np.ndarray, x: np.ndarray, y: np.ndarray, s: int
) -> dict:
    gammas_mp = [mpf(float(g)) for g in gammas]
    x_mp = [mpf(float(v)) for v in x]
    y_mp = [mpf(float(v)) for v in y]
    max_rel = mpf(0)
    for r in range(1, s + 1):
        mx = fsum(g**r * xv for g, xv in zip(gammas_mp, x_mp))
        my = fsum(g**r * yv for g, yv in zip(gammas_mp, y_mp))
        scale = max(abs(mx), abs(my), mpf(1e-300))
        rel = abs(mx - my) / scale
        max_rel = max(max_rel, rel)
    return {
        "max_rel_residual": float(max_rel),
        "sum_x": float(fsum(x_mp)),
        "min_x": float(min(x_mp)) if x_mp else None,
        "min_y": float(min(y_mp)) if y_mp else None,
    }


def run() -> None:
    results = []
    for L in L_VALUES:
        N, q = 2 * L, L
        gammas = gamma_l_array(N, q)
        print(f"=== L={L} ===", flush=True)
        row = {"L": L, "N": N, "q": q, "cells": []}
        prev_best = None
        s_max_this_L = min(S_MAX, L)
        for s in range(1, s_max_this_L + 1):
            cell = {"s": s}
            per_method = {}
            for method in METHODS:
                res = solve_rescaled(gammas, s, method)
                if not res["success"]:
                    per_method[method] = {"success": False, "message": res["message"]}
                else:
                    per_method[method] = {"success": True, "K_s": res["K_s"]}
                    if s == 1 or s == s_max_this_L:
                        hp = high_precision_feasibility_check(gammas, res["x"], res["y"], s)
                        per_method[method]["high_precision_check"] = hp
            cell["per_method"] = per_method
            succeeded = {m: v["K_s"] for m, v in per_method.items() if v["success"]}
            cell["cert_bound"] = chebyshev_certificate_bound(L, s)
            if not succeeded:
                cell["status"] = "INCONCLUSIVE"
                cell["K_s_lower_bound"] = None
            else:
                lo, hi = min(succeeded.values()), max(succeeded.values())
                agree = (hi - lo) < 1e-3 * max(hi, 1e-12)
                cell["method_agreement"] = agree
                if agree:
                    # Methods converged (tight tolerance) -- this is the trustworthy regime.
                    cell["status"] = "OK"
                    cell["K_s_validated"] = 0.5 * (lo + hi)
                    cell["K_s_lower_bound"] = cell["K_s_validated"]
                else:
                    # Methods disagree even at tight tolerance: per Oracle Adequacy Gate /
                    # "failure -> INCONCLUSIVE, never a threshold" -- do NOT report an exact
                    # K_s. Still report the achieved MIN as a conservative, verified lower
                    # bound (both values are independently feasible per the LP solve; the
                    # smaller one is the safer claim), and flag the disagreement explicitly.
                    cell["status"] = "INCONCLUSIVE-METHOD-DISAGREE"
                    cell["K_s_lower_bound"] = lo
            if cell["K_s_lower_bound"] is not None:
                cell["cert_violated"] = cell["K_s_lower_bound"] > cell["cert_bound"] * 1.001
                if prev_best is not None:
                    cell["monotone_ok"] = cell["K_s_lower_bound"] <= prev_best + 1e-6
                prev_best = cell["K_s_lower_bound"]
            row["cells"].append(cell)
            k_str = (
                f"{cell['K_s_lower_bound']:.4f}"
                if cell["K_s_lower_bound"] is not None
                else "INCONCLUSIVE"
            )
            viol = " CERT-VIOLATED" if cell.get("cert_violated") else ""
            agree_flag = "" if cell.get("method_agreement", True) else " METHOD-DISAGREE"
            print(
                f"  s={s:3d}: K_s={k_str} [{cell['status']}]  "
                f"cert_bound={cell['cert_bound']:.4f}{viol}{agree_flag}",
                flush=True,
            )
        results.append(row)
        print()

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "worst_case_lp_surgery_point47.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Done.")


if __name__ == "__main__":
    run()
