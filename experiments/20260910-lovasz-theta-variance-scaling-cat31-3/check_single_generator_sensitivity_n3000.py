"""Extension of check_single_generator_sensitivity.py to n=3000 -- same logic, isolated
run since n=3000 is expensive (~43s/theta_via_lp call, 4 calls/rep here). Reduced reps
(8, vs 25-60 at smaller n) to keep this affordable (~4*43*8 ~= 1376s). Merged into
metrics/single_generator_sensitivity.json by the write-up step, not by this script.
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"

RNG_SEED_BASE = 333000  # SAME base as check_single_generator_sensitivity.py

N, REPS = 3000, 8


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("h_cat31_3_sens3000_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
theta_via_lp = h_cat31_1.theta_via_lp


def flip_generator(c: np.ndarray, i: int) -> np.ndarray:
    n = len(c)
    c2 = c.copy()
    c2[i] = 1.0 - c2[i]
    c2[n - i] = 1.0 - c2[n - i]
    return c2


def run() -> dict:
    half = (N - 1) // 2
    test_indices = sorted({1, max(1, half // 3), max(1, 2 * half // 3)})
    t0 = time.time()
    delta_theta_sq = []
    delta_x_sq = []
    for rep in range(REPS):
        seed = RNG_SEED_BASE + N * 1000 + rep
        c = sample_circulant_neighbors(N, 0.5, seed)
        theta0 = theta_via_lp(c)
        x0 = np.log(theta0 / np.sqrt(N))
        for i in test_indices:
            c_flip = flip_generator(c, i)
            theta1 = theta_via_lp(c_flip)
            x1 = np.log(theta1 / np.sqrt(N))
            delta_theta_sq.append((theta0 - theta1) ** 2)
            delta_x_sq.append((x0 - x1) ** 2)
    elapsed = time.time() - t0

    delta_theta_sq = np.array(delta_theta_sq)
    delta_x_sq = np.array(delta_x_sq)
    mean_dtheta2 = float(delta_theta_sq.mean())
    se_dtheta2 = float(delta_theta_sq.std(ddof=1) / np.sqrt(len(delta_theta_sq)))
    mean_dx2 = float(delta_x_sq.mean())
    se_dx2 = float(delta_x_sq.std(ddof=1) / np.sqrt(len(delta_x_sq)))
    efron_stein_bound_on_var_X = 0.25 * half * mean_dx2

    row = {
        "n": N,
        "half_m": half,
        "reps": REPS,
        "test_indices": test_indices,
        "n_samples": len(delta_theta_sq),
        "mean_delta_theta_sq": mean_dtheta2,
        "se_delta_theta_sq": se_dtheta2,
        "n_times_mean_delta_theta_sq": N * mean_dtheta2,
        "mean_delta_x_sq": mean_dx2,
        "se_delta_x_sq": se_dx2,
        "n_sq_times_mean_delta_x_sq": (N**2) * mean_dx2,
        "efron_stein_bound_on_var_X": efron_stein_bound_on_var_X,
        "elapsed_seconds": elapsed,
    }
    print(
        f"n={N:5d} half_m={half:5d} reps={REPS:3d} idx={test_indices} "
        f"E[dtheta^2]={mean_dtheta2:.4f}+-{se_dtheta2:.4f} n*E[dtheta^2]={N * mean_dtheta2:.3f} "
        f"E[dX^2]={mean_dx2:.6e}+-{se_dx2:.2e} n^2*E[dX^2]={(N**2) * mean_dx2:.4f} "
        f"ES_bound_VarX={efron_stein_bound_on_var_X:.6f} elapsed={elapsed:.1f}s",
        flush=True,
    )
    return row


if __name__ == "__main__":
    row = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "single_generator_sensitivity_n3000.json", "w", encoding="utf-8") as f:
        json.dump(row, f, indent=2)
    print(json.dumps(row, indent=2))
