"""Zero-cost (no new LP solves) Hamming-layer decomposition of the exact small-n data,
per direct user request -- the free step before implementing necklace-orbit reduction.

For each Hamming layer q=0..m-1, computes (over all S with |S|=q and i not in S):
    mu_q = E[X | |S|=q]
    A_q  = E[delta_i | |S|=q]      where delta_i(S) = X(S) - X(S union {i}) >= 0 (monotonicity)
    C_q  = Var(delta_i | |S|=q)

Exact identity checked: A_q = mu_q - mu_{q+1} (telescoping).
Decomposes E[delta_i^2 | q] = A_q^2 + C_q into a "density-curvature" part (A_q^2) and a
"shape-heterogeneity" part (C_q) -- distinguishing which mechanism drives the residual
second moment, per the user's own framing.

Reuses the same exact enumeration as check_exact_enumeration_small_n.py / check_exact_walsh_
decomposition.py (recomputed here since neither script saved the full theta array to disk).
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


h_cat31_1 = _load_module("hamming_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
theta_via_lp = h_cat31_1.theta_via_lp

N_VALUES = [9, 11, 13, 15, 17, 19, 21, 23, 25]
PRIMES = {11, 13, 17, 19, 23}


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


def popcount(x: int) -> int:
    return bin(x).count("1")


def run_one_n(n: int) -> dict:
    m = (n - 1) // 2
    n_subsets = 1 << m
    theta = np.empty(n_subsets)
    for mask in range(n_subsets):
        theta[mask] = theta_via_lp_robust(build_c(n, mask, m))
    if np.any(np.isnan(theta)):
        raise RuntimeError(f"n={n}: unresolved NaN")
    x = np.log(theta / np.sqrt(n))

    layer_sum = np.zeros(m + 1)
    layer_count = np.zeros(m + 1, dtype=np.int64)
    for mask in range(n_subsets):
        q = popcount(mask)
        layer_sum[q] += x[mask]
        layer_count[q] += 1
    mu = layer_sum / layer_count  # mu_q = E[X | |S|=q]

    # A_q, C_q: average/variance of delta_i(S)=X(S)-X(S u {i}) over S with |S|=q, i not in S.
    a_q_sum = np.zeros(m)
    a_q_sq_sum = np.zeros(m)
    a_q_count = np.zeros(m, dtype=np.int64)
    min_delta = float("inf")
    for mask in range(n_subsets):
        q = popcount(mask)
        if q >= m:
            continue
        for bit in range(m):
            if not (mask & (1 << bit)):
                delta = x[mask] - x[mask | (1 << bit)]
                a_q_sum[q] += delta
                a_q_sq_sum[q] += delta**2
                a_q_count[q] += 1
                min_delta = min(min_delta, delta)

    a_q = a_q_sum / a_q_count
    e_delta_sq = a_q_sq_sum / a_q_count
    c_q = e_delta_sq - a_q**2

    telescoping_gap = float(np.max(np.abs(a_q - (mu[:m] - mu[1 : m + 1]))))

    result = {
        "n": n,
        "m": m,
        "is_prime": n in PRIMES,
        "mu_q": mu.tolist(),
        "A_q": a_q.tolist(),
        "C_q": c_q.tolist(),
        "E_delta_sq_q": e_delta_sq.tolist(),
        "telescoping_identity_max_gap": telescoping_gap,
        "min_delta_i_observed": min_delta,
        "monotonicity_holds": bool(min_delta >= -1e-9),
    }
    print(
        f"n={n:3d} prime={result['is_prime']!s:5} telescoping_gap={telescoping_gap:.2e} "
        f"min_delta={min_delta:.2e} monotone={result['monotonicity_holds']}",
        flush=True,
    )
    print(
        f"    A_q (density curvature, by layer q=0..{m - 1}): " + ", ".join(f"{v:.4f}" for v in a_q)
    )
    print(
        f"    C_q (shape heterogeneity, by layer q=0..{m - 1}): "
        + ", ".join(f"{v:.5f}" for v in c_q)
    )
    return result


def run() -> dict:
    rows = [run_one_n(n) for n in N_VALUES]
    return {"rows": rows}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "hamming_layer_decomposition.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
