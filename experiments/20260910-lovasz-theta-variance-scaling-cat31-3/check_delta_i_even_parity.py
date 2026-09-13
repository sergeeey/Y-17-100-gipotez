"""Route A (symmetry): NEW theorem candidate, directly derived from point 11's ALREADY-PROVEN
antisymmetry theorem (X_hat(S)=0 for even |S|, from X(-eps)=-X(eps)) via the classical Boolean-
function discrete-derivative Fourier identity: for f: {+-1}^m -> R,
    D_i f(eps) := (f(eps with eps_i=1) - f(eps with eps_i=-1)) / 2
has Fourier expansion (D_i f)_hat(T) = f_hat(T union {i})  for T subseteq [m]\\{i}.

Since delta_i(S) := X(S) - X(S union {i}) = 2 * D_i X (in this project's own bit=1<->sign=-1
convention, verified in check_exact_walsh_decomposition.py), and X_hat(S)=0 whenever |S| is
EVEN, it follows that (D_i X)_hat(T) = X_hat(T union {i}) can only be nonzero when |T union {i}|
is ODD, i.e. |T| is EVEN. So delta_i's OWN Fourier spectrum (as a function of the remaining
m-1 coordinates) should be confined to EVEN-degree sets T -- the DUAL parity to X itself.

This script verifies this DIRECTLY on exact data (not trusting the algebra alone): computes X's
full exact array via theta_via_lp (same machinery as check_exact_walsh_decomposition.py), then
computes delta_0's own array directly (fixing i=0) and its own independent Walsh-Hadamard
transform over the remaining m-1 coordinates -- comparing the empirical even/odd-level weight
split against the theoretical prediction (weight~0 at ODD levels of delta_i, weight~0 at EVEN
levels was already proven for X itself).
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


h_cat31_1 = _load_module("delta_i_parity_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
theta_via_lp = h_cat31_1.theta_via_lp

N_VALUES = [9, 11, 13, 15, 17, 19, 21]  # keep modest: 2^(m-1) theta calls per n, m=(n-1)//2


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

    # bit=1 <-> sign=-1 (generator ON). i=0 (bit index 0) is the derivative direction.
    # delta_0(S) = X(eps with bit0=0, i.e. sign=+1) - X(eps with bit0=1, i.e. sign=-1)
    #            = x[mask with bit0=0] - x[mask with bit0=1], for each of the 2^(m-1) "rest" masks.
    half = n_subsets // 2
    delta0 = np.empty(half)
    for rest_mask in range(half):
        # rest_mask encodes bits 1..m-1 directly (bit0 is separate)
        mask_off = rest_mask << 1  # bit0 = 0
        mask_on = mask_off | 1  # bit0 = 1
        delta0[rest_mask] = x[mask_off] - x[mask_on]

    transform = (
        fwht(delta0) / half
    )  # delta0_hat(T) for T subseteq {1,...,m-1}, encoded by rest_mask

    level_weight = np.zeros(m)  # levels 0..m-1 (delta0 lives on m-1 remaining coordinates)
    for rest_mask in range(half):
        level_weight[popcount(rest_mask)] += transform[rest_mask] ** 2

    total_energy = float(np.sum(level_weight))
    even_energy = float(np.sum(level_weight[0::2]))
    odd_energy = float(np.sum(level_weight[1::2]))
    even_fraction = even_energy / total_energy if total_energy > 0 else float("nan")
    tail_beyond_level2 = float(np.sum(level_weight[4:]))
    tail_beyond_level2_fraction = (
        tail_beyond_level2 / total_energy if total_energy > 0 else float("nan")
    )

    result = {
        "n": n,
        "m": m,
        "total_energy_delta0": total_energy,
        "even_level_energy": even_energy,
        "odd_level_energy": odd_energy,
        "even_fraction": even_fraction,
        "level_weights": level_weight.tolist(),
        "predicted_odd_energy_should_be_zero": odd_energy,
        "tail_beyond_level2_fraction": tail_beyond_level2_fraction,
    }
    print(
        f"n={n:3d} m={m:2d} total={total_energy:.6f} even={even_energy:.6f} "
        f"odd={odd_energy:.6e} even_frac={even_fraction:.10f}",
        flush=True,
    )
    return result


def run() -> dict:
    rows = [run_one_n(n) for n in N_VALUES]
    return {"rows": rows}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "delta_i_even_parity_check.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
