"""run.py — H-B2-1b: does the Theorem-3.1 / K_j=0 mechanism (verified in H-B2-1's 1D correction)
still give a tight, order-matching bound for a genuinely 2D matrix Chernoff block?

A = P @ diag(-1, -2) @ P.T, symmetric, two distinct real eigenvalues -- P a rotation so A has
off-diagonal coupling in the standard basis (a genuine matrix, not a relabeled scalar pair), but
remains exactly diagonalizable by an ORTHOGONAL matrix, keeping the 2-norm analysis exact:
    ||f(A)||_2 = max(|f(lambda_1)|, |f(lambda_2)|)   for any polynomial f and symmetric A.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

EIGENVALUES = np.array([-1.0, -2.0])
THETA = 0.6  # rotation angle (radians) -- arbitrary, chosen so A is genuinely off-diagonal
P = np.array([[np.cos(THETA), -np.sin(THETA)], [np.sin(THETA), np.cos(THETA)]])  # orthogonal
A = P @ np.diag(EIGENVALUES) @ P.T
X0 = np.array([1.0, 1.0])


def block_order1(h: float) -> np.ndarray:
    return np.eye(2) + h * A


def block_order2(h: float) -> np.ndarray:
    hA = h * A
    return np.eye(2) + hA + hA @ hA / 2.0


def analytic_solution(t: float, x0: np.ndarray = X0) -> np.ndarray:
    """e^{tA} x0 = P diag(e^{lambda_1 t}, e^{lambda_2 t}) P.T x0 (exact, via eigendecomposition)."""
    return P @ np.diag(np.exp(EIGENVALUES * t)) @ P.T @ x0


def iterate_block(block_fn, t: float, n: int, x0: np.ndarray = X0) -> np.ndarray:
    h = t / n
    F = block_fn(h)
    return np.linalg.matrix_power(F, n) @ x0


def empirical_order(block_fn, t: float, n_values: np.ndarray) -> tuple[float, np.ndarray]:
    exact = analytic_solution(t)
    errors = np.array(
        [np.linalg.norm(iterate_block(block_fn, t, int(n)) - exact) for n in n_values]
    )
    log_n = np.log(n_values.astype(float))
    log_err = np.log(errors)
    slope, _ = np.polyfit(log_n, log_err, 1)
    return float(-slope), errors


def m2_condition_holds_both_eigenvalues(block_scalar_fn, t: float, n: int) -> bool:
    """M2 condition (K_j=0, M2=1, w=0) requires |f_m(lambda*h)| <= 1 for the block's SCALAR
    polynomial applied to EVERY eigenvalue -- checks the FASTER eigenvalue (-2) too, which the 1D
    test (only eigenvalue -1) could never reveal."""
    h = t / n
    return all(abs(block_scalar_fn(lam * h)) <= 1.0 for lam in EIGENVALUES)


def block_order1_scalar(h: float) -> float:
    return 1.0 + h


def block_order2_scalar(h: float) -> float:
    return 1.0 + h + h**2 / 2.0


def theorem_3_1_bound_matrix(t: float, n: int, m: int, a_power_m1_x0_norm: float) -> float:
    """Same K_j=0 mechanism as H-B2-1's 1D correction, generalized: bound = M1*M2*t^(m+1) /
    ((m+1)!*n^m) * ||A^(m+1) x0||_2, with M1=1 (||e^{tA}||_2 = e^{lambda_1 t} <= 1 for t>=0,
    lambda_1=-1 the slower/dominant eigenvalue) and M2=1 IF m2_condition_holds_both_eigenvalues."""
    import math

    return (t ** (m + 1)) / (math.factorial(m + 1) * n**m) * a_power_m1_x0_norm


def cmd_run() -> dict:

    T = 1.0
    N_VALUES = np.array([50, 100, 200, 400, 800, 1600, 3200, 6400])

    blocks = {
        "order1": (block_order1, block_order1_scalar, 1),
        "order2": (block_order2, block_order2_scalar, 2),
    }

    results = {}
    for label, (block_fn, block_scalar_fn, m) in blocks.items():
        order_est, errors = empirical_order(block_fn, T, N_VALUES)
        a_power = np.linalg.matrix_power(A, m + 1) @ X0
        a_power_norm = float(np.linalg.norm(a_power))
        per_n = {}
        all_m2_ok = True
        all_bound_holds = True
        for n, err in zip(N_VALUES, errors, strict=True):
            n = int(n)
            m2_ok = m2_condition_holds_both_eigenvalues(block_scalar_fn, T, n)
            all_m2_ok = all_m2_ok and m2_ok
            bound = theorem_3_1_bound_matrix(T, n, m, a_power_norm)
            holds = bool(err <= bound)
            all_bound_holds = all_bound_holds and holds
            per_n[n] = {
                "true_error": float(err),
                "theorem_3_1_bound": bound,
                "bound_holds": holds,
                "efficiency_true_over_bound": float(err) / bound,
                "m2_condition_holds_both_eigenvalues": m2_ok,
            }
        results[label] = {
            "m": m,
            "chernoff_guaranteed_order_simple_1d_formula": float(m - 1),
            "empirical_order_estimate": order_est,
            "a_power_m1_x0_norm": a_power_norm,
            "per_n": per_n,
            "all_n_m2_condition_holds": all_m2_ok,
            "all_n_bound_holds": all_bound_holds,
        }

    all_ok = all(r["all_n_bound_holds"] and r["all_n_m2_condition_holds"] for r in results.values())
    out = {
        "config": {
            "eigenvalues": EIGENVALUES.tolist(),
            "rotation_theta": THETA,
            "x0": X0.tolist(),
            "t": T,
            "n_values": N_VALUES.tolist(),
        },
        "results": results,
        "theorem_3_1_mechanism_holds_in_2d": all_ok,
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
