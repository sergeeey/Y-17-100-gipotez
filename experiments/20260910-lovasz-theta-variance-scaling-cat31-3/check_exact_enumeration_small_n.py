"""Fifth angle on the Efron-Stein O(1/n) upper bound: EXACT (exhaustive, not Monte Carlo)
enumeration at small odd n, per direct user request to try a genuinely different approach
after 4 proof/reformulation attempts (decision.md points 6, 8, 9) all hit the same LP
vertex-stability wall.

Instead of another abstract argument, or noisy large-n sampling, this computes the TRUE
population Var(X_n) and the TRUE population Efron-Stein sum EXACTLY, for small n, by
enumerating ALL 2^m generator subsets (m=(n-1)/2), not a random sample of them. Since
p=0.5 makes every subset equally likely, this gives ground truth with ZERO sampling noise --
a fundamentally different kind of evidence than anything gathered so far (which was all
either Monte Carlo at large n, or abstract worst-case LP bounds).

Cost: one theta_via_lp solve per subset (2^m total), all reused via array lookup for the
Efron-Stein sum (Delta_i theta for any subset S and index i is just theta[S] - theta[S XOR
bit i], both already computed) -- no extra LP solves needed for the sensitivity sum itself.

Reuses theta_via_lp from H-CAT31-1 UNCHANGED.
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("exact_enum_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
theta_via_lp = h_cat31_1.theta_via_lp

N_VALUES = [9, 11, 13, 15, 17, 19, 21, 23, 25]  # odd, per the paper's own def:rand_circ

N_NAN_FALLBACKS = 0  # counts how often the highs-ipm fallback below was needed -- a
# substrate-level finding (default 'highs' simplex hits a numerically-ambiguous status for
# a small number of exact-degenerate subsets; 'highs-ipm' resolves them cleanly), logged
# rather than silently worked around, per Substrate Gate discipline.


def theta_via_lp_robust(c: np.ndarray) -> float:
    """theta_via_lp with a fallback to the interior-point HiGHS method when the default
    simplex method returns NaN (observed at n=21, generators {6,7,9}: default 'highs'
    reports an ambiguous/unrecognized status while 'highs-ipm' solves cleanly, theta=6.3297).
    This is a genuine solver-numerics issue on a small number of exact-degenerate subsets in
    exhaustive enumeration, not evidence about the underlying claim (Substrate Gate)."""
    global N_NAN_FALLBACKS
    val = theta_via_lp(c)
    if not np.isnan(val):
        return val
    N_NAN_FALLBACKS += 1
    n = len(c)
    j = np.arange(n).reshape(-1, 1)
    k = np.arange(n).reshape(1, -1)
    re_f = np.cos(-2 * np.pi * j * k / n)
    a_eq_rows = []
    b_eq = []
    e0 = np.zeros(n)
    e0[0] = 1.0
    a_eq_rows.append(e0)
    b_eq.append(1.0)
    for kk in range(1, (n - 1) // 2 + 1):
        row = np.zeros(n)
        row[kk] = 1.0
        row[n - kk] = -1.0
        a_eq_rows.append(row)
        b_eq.append(0.0)
    for kk in range(1, n):
        if c[kk] > 0.5:
            row = np.zeros(n)
            row[kk] = 1.0
            a_eq_rows.append(row)
            b_eq.append(0.0)
    res = linprog(
        c=-np.ones(n),
        A_ub=-re_f,
        b_ub=np.zeros(n),
        A_eq=np.array(a_eq_rows),
        b_eq=np.array(b_eq),
        bounds=(None, None),
        method="highs-ipm",
    )
    return -res.fun if res.success else float("nan")


def build_c(n: int, mask: int, m: int) -> np.ndarray:
    c = np.zeros(n)
    for bit in range(m):
        if mask & (1 << bit):
            k = bit + 1
            c[k] = 1.0
            c[n - k] = 1.0
    return c


def run_one_n(n: int) -> dict:
    m = (n - 1) // 2
    n_subsets = 1 << m
    t0 = time.time()

    theta = np.empty(n_subsets)
    for mask in range(n_subsets):
        c = build_c(n, mask, m)
        theta[mask] = theta_via_lp_robust(c)
    n_nan_remaining = int(np.sum(np.isnan(theta)))
    if n_nan_remaining:
        raise RuntimeError(
            f"n={n}: {n_nan_remaining} subset(s) unsolved even after highs-ipm fallback -- "
            "Substrate Gate: do not silently drop these from the exact population computation"
        )
    x = np.log(theta / np.sqrt(n))

    mean_x = float(x.mean())
    var_x = float(np.mean((x - mean_x) ** 2))  # exact population variance, ddof=0 (all 2^m
    # subsets are the ENTIRE population at p=0.5, not a sample -- ddof=0 is correct here)

    es_sum = 0.0
    for bit in range(m):
        flipped = np.array([x[mask ^ (1 << bit)] for mask in range(n_subsets)])
        es_sum += float(np.mean((x - flipped) ** 2))
    es_bound = 0.25 * es_sum

    elapsed = time.time() - t0
    result = {
        "n": n,
        "m": m,
        "n_subsets_exact": n_subsets,
        "exact_mean_X": mean_x,
        "exact_Var_X": var_x,
        "exact_ES_sum": es_sum,
        "exact_ES_bound": es_bound,
        "n_times_exact_Var_X": n * var_x,
        "n_times_exact_ES_bound": n * es_bound,
        "ES_bound_over_Var_X": es_bound / var_x if var_x > 0 else float("nan"),
        "elapsed_seconds": elapsed,
    }
    print(
        f"n={n:3d} m={m:2d} subsets={n_subsets:5d} exact_Var_X={var_x:.6f} "
        f"n*Var_X={n * var_x:.4f} exact_ES_bound={es_bound:.6f} n*ES_bound={n * es_bound:.4f} "
        f"ratio={result['ES_bound_over_Var_X']:.3f} elapsed={elapsed:.1f}s",
        flush=True,
    )
    return result


def run() -> dict:
    rows = [run_one_n(n) for n in N_VALUES]
    print(f"\nhighs-ipm fallback needed {N_NAN_FALLBACKS} time(s) total across all subsets/n.")
    return {"rows": rows, "n_ipm_fallbacks_total": N_NAN_FALLBACKS}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "exact_enumeration_small_n.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
