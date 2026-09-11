"""Sixth angle on the Efron-Stein O(1/n) upper bound, per direct user request to try yet
another angle: EXACT Walsh-Hadamard (Fourier-over-{+-1}^m) decomposition of X_n, using the
same exhaustive small-n data as check_exact_enumeration_small_n.py (no new LP solves needed
beyond recomputing theta for each subset -- theta itself is not saved by that script).

Rather than estimating "how much of Var(X_n) is first-order" via noisy regression (point 2,
Q-proxy diagnostic, Monte Carlo R^2), this computes the EXACT level-by-level Fourier weight

    W^k[X] = sum_{|S|=k} X_hat(S)^2 ,   k = 0, 1, ..., m

via the Fast Walsh-Hadamard Transform on the (2^m)-entry EXACT population of X values. This
answers, exactly (not by sampling), the question the Efron-Stein upper bound hinges on: how
much of Var(X_n) = sum_{k>=1} W^k[X] sits at level 1 (which the Cauchy-Schwarz lower bound in
point 7 already controls) versus levels k>=2 (uncontrolled, the missing piece for O(1/n)).

Self-check: Parseval's identity requires sum_k W^k[X] = E[X^2] exactly (not approximately) --
used here as a correctness check on the transform itself, not merely trusted.
"""

from __future__ import annotations

import importlib.util
import json
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


h_cat31_1 = _load_module("walsh_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
theta_via_lp = h_cat31_1.theta_via_lp

N_VALUES = [9, 11, 13, 15, 17, 19, 21, 23, 25]  # same set as check_exact_enumeration_small_n.py


def theta_via_lp_robust(c: np.ndarray) -> float:
    val = theta_via_lp(c)
    if not np.isnan(val):
        return val
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


def fwht(a: np.ndarray) -> np.ndarray:
    """In-place fast Walsh-Hadamard transform (+1/-1 convention). Returns UNNORMALIZED
    transform; caller divides by len(a) to get the actual Fourier coefficients X_hat(S)."""
    a = a.astype(np.float64).copy()
    h = 1
    n = len(a)
    while h < n:
        for i in range(0, n, h * 2):
            x = a[i : i + h].copy()
            y = a[i + h : i + 2 * h].copy()
            a[i : i + h] = x + y
            a[i + h : i + 2 * h] = x - y
        h *= 2
    return a


def popcount(x: int) -> int:
    return bin(x).count("1")


def run_one_n(n: int) -> dict:
    m = (n - 1) // 2
    n_subsets = 1 << m
    theta = np.empty(n_subsets)
    for mask in range(n_subsets):
        c = build_c(n, mask, m)
        theta[mask] = theta_via_lp_robust(c)
    if np.any(np.isnan(theta)):
        raise RuntimeError(f"n={n}: unresolved NaN in theta array")
    x = np.log(theta / np.sqrt(n))

    # WHT expects the array indexed by mask where bit i = "generator i is ON" (z_i=1).
    # Standard +-1 FWHT computes X_hat(S)*2^m = sum_mask x[mask] * prod_{i in S} (-1)^{bit_i(mask)}
    # i.e. treats bit=1 as sign -1 -- exactly what the recursive-doubling algorithm above does.
    transform = fwht(x) / n_subsets  # now transform[S] = X_hat(S) for S encoded as bitmask

    parseval_lhs = float(np.sum(transform**2))
    parseval_rhs = float(np.mean(x**2))
    parseval_ok = bool(abs(parseval_lhs - parseval_rhs) < 1e-9)

    level_weight = np.zeros(m + 1)
    for mask in range(n_subsets):
        level_weight[popcount(mask)] += transform[mask] ** 2

    var_x = float(np.sum(level_weight[1:]))  # Parseval: Var(X) = sum_{k>=1} W^k[X]
    w1_fraction = float(level_weight[1] / var_x) if var_x > 0 else float("nan")
    w_ge2_fraction = float(1 - w1_fraction) if var_x > 0 else float("nan")

    result = {
        "n": n,
        "m": m,
        "parseval_check_passed": parseval_ok,
        "parseval_lhs": parseval_lhs,
        "parseval_rhs": parseval_rhs,
        "exact_Var_X": var_x,
        "level_weights": level_weight.tolist(),
        "level1_fraction_of_Var": w1_fraction,
        "level_ge2_fraction_of_Var": w_ge2_fraction,
        "n_times_level1_weight": n * float(level_weight[1]),
        "n_times_level_ge2_weight": n * float(np.sum(level_weight[2:])),
    }
    print(
        f"n={n:3d} m={m:2d} Parseval_OK={parseval_ok} Var_X={var_x:.6f} "
        f"W1_frac={w1_fraction:.4f} W_ge2_frac={w_ge2_fraction:.4f} "
        f"n*W1={result['n_times_level1_weight']:.4f} "
        f"n*W_ge2={result['n_times_level_ge2_weight']:.4f}",
        flush=True,
    )
    # Report only the first few individual higher levels to keep output bounded.
    for k in range(2, min(m, 4) + 1):
        print(
            f"    level {k}: exact weight={level_weight[k]:.6f}  n*weight={n * level_weight[k]:.4f}"
        )
    return result


def run() -> dict:
    rows = [run_one_n(n) for n in N_VALUES]
    return {"rows": rows}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "exact_walsh_decomposition.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
