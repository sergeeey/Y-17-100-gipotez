"""Independent verification of a 7th-angle external analysis's claims (NOT trusted at face
value -- everything below is re-derived/re-checked against this project's own exact small-n
data, per audit-verification-gate.md), per direct user request to keep pushing on O(1/n).

Three claims checked:

1. Sharpened Efron-Stein via the proven vanishing-even-levels theorem (decision.md point 11):
   since W_{2j}=0 exactly, B_n - W_1 = sum_{k odd>=3} k*W_k >= 3*sum_{k odd>=3} W_k
   = 3*(V_n - W_1), giving V_n <= (B_n + 2*W_1)/3 -- a real algebraic tightening of the
   standard Efron-Stein bound V_n<=B_n. Checked directly against the exact level_weights
   already computed in exact_walsh_decomposition.json (no new LP solves).

2. For PRIME n, the level-1 Cauchy-Schwarz lower bound (decision.md point 7) becomes an
   EQUALITY: W_1 = M_n'(1/2)^2/(4m). Re-derived independently: the prime-n symmetry theorem
   (decision.md point 4) already proves theta(G_S)=theta(G_{aS}) for units a, which extends
   (not just for single-generator flips but for the FULL vector) to X(pi_a . epsilon) =
   X(epsilon) identically -- forcing X_hat({i}) equal across the single Z_n^x-orbit, i.e. all
   i for prime n. Equal singleton coefficients is exactly the Cauchy-Schwarz equality
   condition (proportionality). Verified here by recomputing theta arrays at each PRIME n in
   9..25 (11,13,17,19,23) and computing the individual level-1 coefficients directly (not just
   their squared sum, which check_exact_walsh_decomposition.py did not save separately).

3. Claim that the PRIME-ONLY subsequence of n*V_n, n*W_1, kappa_n=B_n/W_1 is still rising
   (not stabilizing) over 11..23, unlike the mixed (prime+composite) n=21,23,25 reading that
   looked like a plateau. Checked directly from the same recomputed data.
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


h_cat31_1 = _load_module("verify7_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
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
        raise RuntimeError(f"n={n}: unresolved NaN")
    x = np.log(theta / np.sqrt(n))
    transform = fwht(x) / n_subsets  # X_hat(S), indexed by bitmask S

    level_weight = np.zeros(m + 1)
    level_b = np.zeros(m + 1)  # sum of k*W_k contributions, per k
    for mask in range(n_subsets):
        k = popcount(mask)
        level_weight[k] += transform[mask] ** 2
        level_b[k] += k * transform[mask] ** 2

    var_x = float(np.sum(level_weight[1:]))
    b_n = float(np.sum(level_b[1:]))  # = Efron-Stein bound quantity (sum_S |S| X_hat(S)^2)
    w1 = float(level_weight[1])

    # Claim 1: V_n <= (B_n + 2*W_1)/3
    sharpened_bound = (b_n + 2 * w1) / 3
    claim1_holds = bool(var_x <= sharpened_bound + 1e-9)

    # c_1 = sum_i X_hat({i}) -- individual level-1 coefficients (mask has exactly one bit set)
    c1 = float(sum(transform[1 << bit] for bit in range(m)))
    mnprime_half = 2 * c1  # M_n'(1/2) = 2*c_1, derived earlier this session (point 7)

    # Claim 2 (prime n only): W_1 == M_n'(1/2)^2/(4m) exactly
    w1_from_identity = mnprime_half**2 / (4 * m)
    claim2_gap = abs(w1 - w1_from_identity)

    # Individual singleton coefficients -- check they're all equal (prime-n symmetry)
    singleton_coeffs = [transform[1 << bit] for bit in range(m)]
    singleton_spread = float(max(singleton_coeffs) - min(singleton_coeffs))

    kappa_n = b_n / w1 if w1 > 0 else float("nan")

    result = {
        "n": n,
        "m": m,
        "is_prime": n in PRIMES,
        "exact_Var_X": var_x,
        "exact_B_n": b_n,
        "exact_W1": w1,
        "sharpened_bound_(B_n+2W1)/3": sharpened_bound,
        "claim1_V_n_leq_sharpened_bound": claim1_holds,
        "c1_sum_singleton_coeffs": c1,
        "M_n_prime_half": mnprime_half,
        "W1_from_identity_Mnprime_sq_over_4m": w1_from_identity,
        "claim2_abs_gap_W1_vs_identity": claim2_gap,
        "singleton_coeff_spread(max-min)": singleton_spread,
        "kappa_n": kappa_n,
        "n_times_Var_X": n * var_x,
        "n_times_W1": n * w1,
    }
    print(
        f"n={n:3d} prime={result['is_prime']!s:5} Var_X={var_x:.6f} <= "
        f"sharpened_bound={sharpened_bound:.6f} [{'OK' if claim1_holds else 'FAIL'}] | "
        f"W1={w1:.6f} vs identity={w1_from_identity:.6f} gap={claim2_gap:.2e} "
        f"singleton_spread={singleton_spread:.2e} | kappa_n={kappa_n:.4f} "
        f"n*Var_X={n * var_x:.4f} n*W1={n * w1:.4f}",
        flush=True,
    )
    return result


def run() -> dict:
    rows = [run_one_n(n) for n in N_VALUES]
    prime_rows = [r for r in rows if r["is_prime"]]
    print("\n--- PRIME-ONLY subsequence (n*Var_X, n*W1, kappa_n) ---")
    for r in prime_rows:
        print(
            f"  n={r['n']:3d}  n*Var_X={r['n_times_Var_X']:.4f}  n*W1={r['n_times_W1']:.4f}  "
            f"kappa_n={r['kappa_n']:.4f}"
        )
    return {"rows": rows}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "verify_seventh_angle.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
