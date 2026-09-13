"""Point 46: the TRUE worst-case moment-ambiguity factor K_s(L), replacing point 45's sampled
"max observed" with a rigorous two-spectrum LP (per direct user correction: point 45's number
was a sampled maximum over a handful of families + 500 random draws, NOT a proven worst case --
this closes that gap exactly, not approximately).

Two-spectrum formulation: for a normalized "true" spectrum x (sum x_l=1) and an "adversarial"
spectrum y sharing the same first s raw moments as x, the worst-case ambiguity factor is

    K_s(L) := max_{x,y>=0} sum_l y_l
              s.t. sum_l x_l = 1,
                   sum_l gamma_l^r x_l = sum_l gamma_l^r y_l   for r=1..s

This is a single LP in 2L variables (x and y jointly) with s+1 equality constraints -- still
tiny even at L=1000 (2000 variables, 21 constraints for s=20). Because x is normalized inside
the LP itself (sum x_l=1), this sidesteps point 45's own scale-invariance concern entirely (no
separate rescaling needed, no floating-point tolerance surprises at extreme scales) and gives a
PROVEN worst case (checkable via the LP's own primal-dual gap to machine precision), not a
sampled lower bound.

Second experiment: for s=1..20 and several grid sizes L, compute K_s(L) and extract
s_1.1(L) := min{s : K_s(L)<=1.1} and s_2(L) := min{s : K_s(L)<=2} -- directly answering "how
many moments are needed as L grows" rather than treating six as special. Growth of s_*(L) with
L (bounded / O(log L) / power-law) determines whether Priority C's fixed-moment-order route
is viable at all as n->infinity (L=min(q,N-q)=Theta(n)).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def gamma_l_array(N: int, q: int) -> np.ndarray:
    L = min(q, N - q)
    ls = np.arange(1, L + 1)
    return ls * (N + 1 - ls) / (q * (N - q))


def worst_case_K_s(gammas: np.ndarray, s: int) -> dict:
    """Solve the two-spectrum LP for K_s(L). Variables: [x_1..x_L, y_1..y_L]."""
    L = len(gammas)
    n_vars = 2 * L

    # Objective: maximize sum(y) => minimize -sum(y)
    c = np.concatenate([np.zeros(L), -np.ones(L)])

    # Constraint 1: sum(x) = 1
    row_norm = np.concatenate([np.ones(L), np.zeros(L)])
    # Constraints 2..s+1: sum(gamma^r * x) - sum(gamma^r * y) = 0
    rows_moment = [np.concatenate([gammas**r, -(gammas**r)]) for r in range(1, s + 1)]
    A_eq = np.vstack([row_norm, *rows_moment])
    b_eq = np.concatenate([[1.0], np.zeros(s)])

    res = linprog(
        c,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=[(0, None)] * n_vars,
        method="highs",
    )
    if not res.success:
        return {"success": False, "message": res.message}
    K_s = -res.fun
    x_opt = res.x[:L]
    y_opt = res.x[L:]
    active_x = [int(i) + 1 for i, v in enumerate(x_opt) if v > 1e-9 * max(x_opt.max(), 1e-30)]
    active_y = [int(i) + 1 for i, v in enumerate(y_opt) if v > 1e-9 * max(y_opt.max(), 1e-30)]
    return {
        "success": True,
        "K_s": float(K_s),
        "active_x_levels": active_x,
        "active_y_levels": active_y,
    }


def run_K_s_vs_s(L_values: list[int], s_max: int = 20) -> list[dict]:
    results = []
    for L in L_values:
        N = 2 * L  # arbitrary; only gamma_l's SHAPE matters for this geometry-only question,
        # matching point 45's own convention of using N=2L, q=L for synthetic grids
        q = L
        gammas = gamma_l_array(N, q)
        row = {"L": L, "N": N, "q": q, "K_s": {}, "failure_at_s": None, "failure_message": None}
        s_1_1 = None
        s_2 = None
        for s in range(1, min(s_max, L) + 1):
            res = worst_case_K_s(gammas, s)
            if not res["success"]:
                row["failure_at_s"] = s
                row["failure_message"] = res.get("message")
                print(f"  L={L}: LP FAILED at s={s}: {res.get('message')}", flush=True)
                break
            row["K_s"][s] = res["K_s"]
            if s_1_1 is None and res["K_s"] <= 1.1:
                s_1_1 = s
            if s_2 is None and res["K_s"] <= 2.0:
                s_2 = s
        row["max_s_computed"] = max(row["K_s"].keys()) if row["K_s"] else 0
        row["s_1.1"] = s_1_1
        row["s_2.0"] = s_2
        results.append(row)
        k_str = ", ".join(f"K_{s}={v:.3f}" for s, v in row["K_s"].items())
        print(
            f"L={L:5d}: s_1.1={s_1_1} s_2.0={s_2}  [{k_str}]",
            flush=True,
        )
    return results


def run_real_grid_check() -> list[dict]:
    """Sanity/comparison: compute the TRUE K_6 for the 7 real (N,q) grids used throughout this
    experiment, and compare against point 45's sampled 'max observed' numbers at matching L."""
    with open(METRICS / "higher_moments_M1_M6.json", encoding="utf-8") as f:
        rows = sorted(json.load(f)["rows"], key=lambda r: r["n"])
    results = []
    for r in rows:
        N, q = r["N"], r["q"]
        gammas = gamma_l_array(N, q)
        res = worst_case_K_s(gammas, 6)
        results.append({"n": r["n"], "N": N, "q": q, "L": len(gammas), "K_6_true": res["K_s"]})
        print(f"n={r['n']:3d} L={len(gammas):3d}: true K_6 = {res['K_s']:.4f}", flush=True)
    return results


def run() -> None:
    print("=== True K_6 on the 7 real experiment grids (vs point 45's sampled numbers) ===")
    real_results = run_real_grid_check()

    print("\n=== K_s(L) matrix, s=1..20, geometry-only synthetic grids ===")
    L_values = [5, 10, 25, 50, 100, 250, 500, 1000]
    scaling_results = run_K_s_vs_s(L_values, s_max=20)

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "worst_case_moment_ambiguity_lp.json", "w", encoding="utf-8") as f:
        json.dump(
            {"real_grids": real_results, "scaling": scaling_results},
            f,
            indent=2,
        )


if __name__ == "__main__":
    run()
    print("\nDone.", flush=True)
