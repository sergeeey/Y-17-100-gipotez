"""run.py — H-B2-1c: does the Theorem-3.1/K_j=0 mechanism survive a NON-NORMAL matrix, where
transient growth (Kreiss matrix theorem territory) breaks the symmetric shortcut used in H-B2-1b
(||f(A)||_2 = max|f(lambda_i)|)?

A = [[-1, c], [0, -2]]: upper-triangular, eigenvalues -1 and -2 (same as H-B2-1b), but non-normal
for c != 0 (A @ A.T != A.T @ A). M1 and M2 are determined NUMERICALLY here (direct operator-norm
measurement via scipy.linalg.expm and matrix powers), not assumed to be 1 as in the symmetric case.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

C = 10.0  # off-diagonal coupling -- large enough to induce meaningful transient growth
A = np.array([[-1.0, C], [0.0, -2.0]])
X0 = np.array([1.0, 1.0])


def is_normal(matrix: np.ndarray, tol: float = 1e-9) -> bool:
    return np.allclose(matrix @ matrix.T, matrix.T @ matrix, atol=tol)


def block_order1(h: float) -> np.ndarray:
    return np.eye(2) + h * A


def block_order2(h: float) -> np.ndarray:
    hA = h * A
    return np.eye(2) + hA + hA @ hA / 2.0


def block_order1_matrix(h: float) -> np.ndarray:
    return block_order1(h)


def block_order2_matrix(h: float) -> np.ndarray:
    return block_order2(h)


def analytic_solution(t: float, x0: np.ndarray = X0) -> np.ndarray:
    """Exact via scipy's matrix exponential (no eigenvector-diagonalization shortcut used, since
    that shortcut is exactly what's invalid to LEAN ON for non-normal A -- expm is the honest,
    general computation)."""
    return expm(t * A) @ x0


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


def measure_m1(t_max: float, n_grid: int = 2000) -> float:
    """Numerically measure sup_{t in (0, t_max]} ||e^{tA}||_2 (operator/spectral norm) -- the
    HONEST way to get M1 for a non-normal A, no eigenvalue shortcut."""
    ts = np.linspace(t_max / n_grid, t_max, n_grid)
    norms = [np.linalg.norm(expm(t * A), ord=2) for t in ts]
    return float(max(norms))


def measure_m2(block_fn, t: float, n: int, k_max: int | None = None) -> float:
    """Numerically measure sup_{k=1..k_max} ||F(h)^k||_2 for h=t/n -- the honest way to get M2,
    no eigenvalue shortcut. k_max defaults to n (the actual range used in the Chernoff product)."""
    h = t / n
    F = block_fn(h)
    k_max = k_max or n
    # ||F^k||_2 for a 2x2 matrix: check at a geometric sample of k (monotonic-ish decay expected
    # after any transient, sampling densely at small k where transient growth would show up).
    sample_ks = sorted(
        set(list(range(1, min(50, k_max) + 1)) + list(range(50, k_max + 1, max(1, k_max // 50))))
    )
    norms = [np.linalg.norm(np.linalg.matrix_power(F, k), ord=2) for k in sample_ks]
    return float(max(norms))


def theorem_3_1_bound(
    t: float, n: int, m: int, m1: float, m2: float, a_power_m1_x0_norm: float
) -> float:
    """CORRECTED 2026-09-06 (found while writing H-B2-1d): formula (13) has an M1^2 factor, not
    M1 -- C_{m+1}(t) = K_{m+1}(t)e^{-wt} + M1/(m+1)! (Lemma 3.3's bound on e^{tL}'s OWN Taylor
    remainder) is itself multiplied by the outer M1*M2 prefactor. With K_{m+1}=0 and w=0:
    bound = M1*M2*t^(m+1)/n^m * (M1/(m+1)!) * ||A^(m+1)x0|| = M1^2*M2*t^(m+1)/((m+1)!*n^m)*||...||.
    Invisible in H-B2-1/H-B2-1b (M1=1 there, so M1^2=M1) but real here (M1~2.563)."""
    return (m1**2 * m2 * t ** (m + 1)) / (math.factorial(m + 1) * n**m) * a_power_m1_x0_norm


def cmd_run() -> dict:
    T = 1.0
    N_VALUES = np.array([50, 100, 200, 400, 800, 1600, 3200, 6400])

    # M1 is a property of e^{tA} alone -- independent of n, measure once for the whole T range.
    m1 = measure_m1(T)

    blocks = {"order1": (block_order1_matrix, 1), "order2": (block_order2_matrix, 2)}
    results = {}
    for label, (block_fn, m) in blocks.items():
        order_est, errors = empirical_order(block_fn, T, N_VALUES)
        a_power = np.linalg.matrix_power(A, m + 1) @ X0
        a_power_norm = float(np.linalg.norm(a_power))
        per_n = {}
        all_bound_holds = True
        for n, err in zip(N_VALUES, errors, strict=True):
            n = int(n)
            m2 = measure_m2(block_fn, T, n)
            bound = theorem_3_1_bound(T, n, m, m1, m2, a_power_norm)
            holds = bool(err <= bound)
            all_bound_holds = all_bound_holds and holds
            per_n[n] = {
                "true_error": float(err),
                "measured_m2": m2,
                "theorem_3_1_bound": bound,
                "bound_holds": holds,
                "efficiency_true_over_bound": float(err) / bound,
            }
        results[label] = {
            "m": m,
            "empirical_order_estimate": order_est,
            "a_power_m1_x0_norm": a_power_norm,
            "per_n": per_n,
            "all_n_bound_holds": all_bound_holds,
        }

    out = {
        "config": {
            "A": A.tolist(),
            "coupling_c": C,
            "is_normal": is_normal(A),
            "measured_m1": m1,
            "x0": X0.tolist(),
            "t": T,
            "n_values": N_VALUES.tolist(),
        },
        "results": results,
        "mechanism_holds_for_nonnormal_A": all(r["all_n_bound_holds"] for r in results.values()),
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
