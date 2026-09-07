"""run.py — H-B2-1j: does the Theorem 3.1 bound stay valid and order-matching at N_DIM=50
(vs the N_DIM<=8 tested in every prior H-B2-1* experiment)? LAB.md's own named open item.

Identical construction pattern to H-B2-1f/g (one positive eigenvalue, many negative, random
upper-triangular coupling, same seed) except N_DIM (8 -> 50) and the correspondingly extended
eigenvalue spectrum -- the ONE assumption changed, per Minimal Relaxation Rule. COUPLING_MAGNITUDE
and SEED are held at H-B2-1g's own values for direct comparability.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

N_DIM = 50
EIGENVALUES = np.concatenate([[0.5], np.linspace(-1.0, -50.0, N_DIM - 1)])
W = 0.5
SEED = 0  # matches every prior H-B2-1* experiment
COUPLING_MAGNITUDE = (
    15.0  # matches H-B2-1g's own tested value -- the ONE changed assumption is N_DIM
)

_rng = np.random.default_rng(SEED)
A = np.diag(EIGENVALUES)
_coupling = _rng.uniform(-COUPLING_MAGNITUDE, COUPLING_MAGNITUDE, size=(N_DIM, N_DIM))
A = A + np.triu(_coupling, k=1)
X0 = np.ones(N_DIM)


def is_normal(matrix: np.ndarray, tol: float = 1e-6) -> bool:
    return np.allclose(matrix @ matrix.T, matrix.T @ matrix, atol=tol)


def block_order1(h: float) -> np.ndarray:
    return np.eye(N_DIM) + h * A


def block_order2(h: float) -> np.ndarray:
    hA = h * A
    return np.eye(N_DIM) + hA + hA @ hA / 2.0


def analytic_solution(t: float, x0: np.ndarray = X0) -> np.ndarray:
    return expm(t * A) @ x0


def iterate_block(block_fn, t: float, n: int, x0: np.ndarray = X0) -> np.ndarray:
    h = t / n
    f = block_fn(h)
    return np.linalg.matrix_power(f, n) @ x0


def empirical_order(block_fn, t: float, n_values: np.ndarray) -> tuple[float, np.ndarray]:
    exact = analytic_solution(t)
    errors = np.array(
        [np.linalg.norm(iterate_block(block_fn, t, int(n)) - exact) for n in n_values]
    )
    log_n = np.log(n_values.astype(float))
    log_err = np.log(errors)
    slope, _ = np.polyfit(log_n, log_err, 1)
    return float(-slope), errors


def measure_m1_with_w(t_max: float, w: float, n_grid: int = 1000) -> float:
    ts = np.linspace(t_max / n_grid, t_max, n_grid)
    ratios = [np.linalg.norm(expm(t * A), ord=2) / np.exp(w * t) for t in ts]
    return float(max(ratios))


def measure_m2_with_w(block_fn, t: float, n: int, w: float) -> float:
    h = t / n
    f = block_fn(h)
    sample_ks = sorted(
        set(list(range(1, min(50, n) + 1)) + list(range(50, n + 1, max(1, n // 50))))
    )
    ratios = [
        np.linalg.norm(np.linalg.matrix_power(f, k), ord=2) / np.exp(k * w * h) for k in sample_ks
    ]
    return float(max(ratios))


def theorem_3_1_bound(
    t: float, n: int, m: int, m1: float, m2: float, w: float, a_power_m1_x0_norm: float
) -> float:
    return (
        (m1**2 * m2 * t ** (m + 1) * math.exp(w * t))
        / (math.factorial(m + 1) * n**m)
        * a_power_m1_x0_norm
    )


def cmd_run() -> dict:
    t = 1.0
    n_values = np.array([50, 100, 200, 400, 800, 1600, 3200, 6400])

    m1 = measure_m1_with_w(t, W)

    blocks = {"order1": (block_order1, 1), "order2": (block_order2, 2)}
    results = {}
    for label, (block_fn, m) in blocks.items():
        order_est, errors = empirical_order(block_fn, t, n_values)
        a_power = np.linalg.matrix_power(A, m + 1) @ X0
        a_power_norm = float(np.linalg.norm(a_power))
        per_n = {}
        all_bound_holds = True
        for n, err in zip(n_values, errors, strict=True):
            n = int(n)
            m2 = measure_m2_with_w(block_fn, t, n, W)
            bound = theorem_3_1_bound(t, n, m, m1, m2, W, a_power_norm)
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
            "n_dim": N_DIM,
            "eigenvalues_summary": {
                "max": float(EIGENVALUES.max()),
                "min": float(EIGENVALUES.min()),
                "n_eigenvalues": len(EIGENVALUES),
            },
            "seed": SEED,
            "coupling_magnitude": COUPLING_MAGNITUDE,
            "is_normal": is_normal(A),
            "w": W,
            "measured_m1": m1,
            "m1_at_n8_strong_coupling_h_b2_1g": 158.93114443726702,
            "t": t,
            "n_values": n_values.tolist(),
        },
        "results": results,
        "mechanism_holds_at_n50": all(r["all_n_bound_holds"] for r in results.values()),
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
