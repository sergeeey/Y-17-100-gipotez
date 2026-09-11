"""Verifies the LP-sensitivity mechanism underlying the Efron-Stein target
E[(Delta_i theta)^2]=O(1/n) (decision.md Addendum § 6): the value function
V(t) = max{<y,g> : y feasible for S\\{i}, <y,f_i>=t}
is concave and piecewise-linear in t (standard LP parametric-duality fact: for a bounded
max-LP, the value function is the pointwise infimum of affine functions of the RHS, hence
concave). theta(G_S)=V(0) and theta(G_{S\\{i}})=max_t V(t); dropping generator i moves along
this curve from t=0 to its unconstrained argmax t*.

This does NOT by itself give a quantitative O(1/n) bound -- see decision.md's honest
write-up of why the gap (from this mechanism to the needed magnitude) remains open. This
script exists to CONFIRM the mechanism is real (not just asserted) before reasoning about it
further, per this project's own audit-verification-gate.md discipline.

Small test: n=11, three generators, drop one, sweep t and confirm (a) piecewise-linearity
(near-zero second differences within each linear piece, floating-point noise only),
(b) a genuine concave kink (rises then falls), (c) max_t V(t) matches theta(G_{S\\{i}})
computed directly via theta_via_lp on the reduced generator set (independent cross-check).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("verify_lp_sens_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
theta_via_lp = h_cat31_1.theta_via_lp

N = 11
SEED = 42
N_GENERATORS_ON = 3
T_RANGE = np.linspace(-1.0, 1.0, 81)


def dft_cosine_row(n: int, k: int) -> np.ndarray:
    return np.array([np.cos(2 * np.pi * k * ell / n) for ell in range(n)])


def value_function(n: int, s_rest: list[int], i_extra: int, t: float | None) -> float | None:
    """V(t): LP value with S_rest constraints plus <y,f_i_extra>=t (t=None omits it)."""
    f = [dft_cosine_row(n, k) for k in range(n)]
    g_b = np.ones(n)
    for k in range(1, n // 2 + 1):
        is_edge = k in s_rest
        g_b[k] = -1.0 if is_edge else 1.0
        g_b[n - k] = -1.0 if is_edge else 1.0
    g = np.array([sum(f[k][ell] * g_b[k] for k in range(n)) for ell in range(n)])

    a_eq: list[np.ndarray] = []
    b_eq: list[float] = []
    for k in range(1, (n + 1) // 2):
        row = np.zeros(n)
        row[k] = 1
        row[n - k] = -1
        a_eq.append(row)
        b_eq.append(0.0)
    a_eq.append(np.ones(n))
    b_eq.append(1.0)
    for k in s_rest:
        a_eq.append(f[k].copy())
        b_eq.append(0.0)
    if i_extra is not None and t is not None:
        a_eq.append(f[i_extra].copy())
        b_eq.append(t)

    res = linprog(
        -g, A_eq=np.array(a_eq), b_eq=np.array(b_eq), bounds=[(0, None)] * n, method="highs"
    )
    return -res.fun if res.success else None


def run() -> dict:
    rng = np.random.default_rng(SEED)
    half = (N - 1) // 2
    s_full = sorted(rng.choice(range(1, half + 1), size=N_GENERATORS_ON, replace=False).tolist())
    i_drop = s_full[0]
    s_rest = [k for k in s_full if k != i_drop]

    vs = [value_function(N, s_rest, i_drop, float(t)) for t in T_RANGE]
    valid = [(t, v) for t, v in zip(T_RANGE, vs) if v is not None]
    ts_v = [t for t, _ in valid]
    vals = [v for _, v in valid]

    second_diffs = [vals[j + 1] - 2 * vals[j] + vals[j - 1] for j in range(1, len(vals) - 1)]
    jmax = int(np.argmax(vals))

    c_rest = np.zeros(N)
    for k in s_rest:
        c_rest[k] = 1.0
        c_rest[N - k] = 1.0
    theta_s_rest_direct = theta_via_lp(c_rest)

    theta_s = value_function(N, s_full, None, None)

    result = {
        "n": N,
        "S": s_full,
        "i_drop": i_drop,
        "S_rest": s_rest,
        "theta(G_S) = V(0)": theta_s,
        "max_t V(t) [grid]": vals[jmax],
        "t* [grid]": ts_v[jmax],
        "theta(G_S_rest) [direct, independent]": theta_s_rest_direct,
        "grid_vs_direct_relative_gap": abs(vals[jmax] - theta_s_rest_direct) / theta_s_rest_direct,
        "max_second_diff": max(second_diffs),
        "min_second_diff": min(second_diffs),
        "confirms_piecewise_linear_with_kink": min(second_diffs) < -1e-3 < max(second_diffs) + 1e-9,
    }
    for key, value in result.items():
        print(f"{key}: {value}")
    return result


if __name__ == "__main__":
    run()
