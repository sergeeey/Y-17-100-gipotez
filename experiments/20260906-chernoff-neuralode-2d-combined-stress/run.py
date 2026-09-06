"""run.py — H-B2-1e: combined stress test -- does the Theorem-3.1/K_j=0 mechanism survive
non-normality AND a mixed-sign spectrum SIMULTANEOUSLY (H-B2-1c and H-B2-1d each tested one
complication alone)?

A = [[0.5, 10], [0, -2]]: upper-triangular (non-normal, same coupling as H-B2-1c), eigenvalues
+0.5 (growth) and -2 (decay), same as H-B2-1d. No symmetry shortcut available -- M1/M2 measured
numerically via scipy.linalg.expm and matrix powers, exactly as in H-B2-1c, but now with w>0 as
in H-B2-1d.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

C = 10.0
A = np.array([[0.5, C], [0.0, -2.0]])
W = 0.5  # matches the growing eigenvalue, same choice as H-B2-1d
X0 = np.array([1.0, 1.0])


def is_normal(matrix: np.ndarray, tol: float = 1e-9) -> bool:
    return np.allclose(matrix @ matrix.T, matrix.T @ matrix, atol=tol)


def block_order1(h: float) -> np.ndarray:
    return np.eye(2) + h * A


def block_order2(h: float) -> np.ndarray:
    hA = h * A
    return np.eye(2) + hA + hA @ hA / 2.0


def analytic_solution(t: float, x0: np.ndarray = X0) -> np.ndarray:
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


def measure_m1_with_w(t_max: float, w: float, n_grid: int = 2000) -> float:
    ts = np.linspace(t_max / n_grid, t_max, n_grid)
    ratios = [np.linalg.norm(expm(t * A), ord=2) / np.exp(w * t) for t in ts]
    return float(max(ratios))


def measure_m2_with_w(block_fn, t: float, n: int, w: float) -> float:
    h = t / n
    F = block_fn(h)
    sample_ks = sorted(
        set(list(range(1, min(50, n) + 1)) + list(range(50, n + 1, max(1, n // 50))))
    )
    ratios = [
        np.linalg.norm(np.linalg.matrix_power(F, k), ord=2) / np.exp(k * w * h) for k in sample_ks
    ]
    return float(max(ratios))


def theorem_3_1_bound(
    t: float, n: int, m: int, m1: float, m2: float, w: float, a_power_m1_x0_norm: float
) -> float:
    """M1^2*M2 prefactor (corrected form, see H-B2-1c's own correction note) times e^{wt}."""
    return (
        (m1**2 * m2 * t ** (m + 1) * math.exp(w * t))
        / (math.factorial(m + 1) * n**m)
        * a_power_m1_x0_norm
    )


def cmd_run() -> dict:
    T = 1.0
    N_VALUES = np.array([50, 100, 200, 400, 800, 1600, 3200, 6400])

    m1 = measure_m1_with_w(T, W)

    blocks = {"order1": (block_order1, 1), "order2": (block_order2, 2)}
    results = {}
    for label, (block_fn, m) in blocks.items():
        order_est, errors = empirical_order(block_fn, T, N_VALUES)
        a_power = np.linalg.matrix_power(A, m + 1) @ X0
        a_power_norm = float(np.linalg.norm(a_power))
        per_n = {}
        all_bound_holds = True
        for n, err in zip(N_VALUES, errors, strict=True):
            n = int(n)
            m2 = measure_m2_with_w(block_fn, T, n, W)
            bound = theorem_3_1_bound(T, n, m, m1, m2, W, a_power_norm)
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
            "w": W,
            "measured_m1": m1,
            "x0": X0.tolist(),
            "t": T,
            "n_values": N_VALUES.tolist(),
        },
        "results": results,
        "mechanism_holds_combined_stress": all(r["all_n_bound_holds"] for r in results.values()),
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
