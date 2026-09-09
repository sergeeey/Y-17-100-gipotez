"""run.py -- H-B2-4: multi-seed x multi-N grid with a permutation-test criterion, replacing
H-B2-1k's own single-seed sign-change test (found CRITERION_INVALID -- passed by pure noise with
probability ~0.999994 for 9 points). H-B2-1k's own kill_criterion field named this exact fix,
verbatim: "needs a multi-seed x multi-N grid with a permutation-test criterion instead."

Reuses SPECTRAL_RANGE/N_DIM_VALUES/COUPLING_MAGNITUDE/T_MAX/W and measure_m1's own formula
byte-identical from H-B2-1k; build_matrix is generalized to take seed as a parameter (H-B2-1k's
own version hardcoded SEED=0).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

SPECTRAL_RANGE = (-50.0, -1.0)
POSITIVE_EIGENVALUE = 0.5
W = 0.5
COUPLING_MAGNITUDE = 15.0
T_MAX = 1.0

N_DIM_VALUES = (3, 4, 8, 12, 16, 24, 32, 40, 50)
N_SEEDS = 30
N_PERMUTATIONS = 2000
PERMUTATION_SEED = 240000


def build_matrix(n_dim: int, seed: int) -> np.ndarray:
    """Byte-identical to H-B2-1k's own build_matrix, except `seed` is now a parameter instead of
    the module-level hardcoded SEED=0."""
    eigenvalues = np.concatenate(
        [[POSITIVE_EIGENVALUE], np.linspace(SPECTRAL_RANGE[0], SPECTRAL_RANGE[1], n_dim - 1)]
    )
    rng = np.random.default_rng(seed)
    a = np.diag(eigenvalues)
    coupling = rng.uniform(-COUPLING_MAGNITUDE, COUPLING_MAGNITUDE, size=(n_dim, n_dim))
    return a + np.triu(coupling, k=1)


def measure_m1(a: np.ndarray, t_max: float, w: float, n_grid: int = 1000) -> float:
    """Byte-identical formula to every prior H-B2-1* experiment's own M1 measurement."""
    ts = np.linspace(t_max / n_grid, t_max, n_grid)
    ratios = [np.linalg.norm(expm(t * a), ord=2) / np.exp(w * t) for t in ts]
    return float(max(ratios))


def sign_change_count(values: np.ndarray) -> int:
    diffs = np.diff(values)
    signs = np.sign(diffs)
    signs = signs[signs != 0]  # ties don't count as a change either direction
    if len(signs) < 2:
        return 0
    return int(np.sum(signs[1:] != signs[:-1]))


def cmd_run() -> dict:
    n_n = len(N_DIM_VALUES)
    m1_grid = np.empty((N_SEEDS, n_n))  # rows=seeds, cols=N_DIM_VALUES index
    for seed in range(N_SEEDS):
        for j, n_dim in enumerate(N_DIM_VALUES):
            a = build_matrix(n_dim, seed)
            m1_grid[seed, j] = measure_m1(a, T_MAX, W)

    mean_m1 = m1_grid.mean(axis=0)
    observed_sign_changes = sign_change_count(mean_m1)

    rng = np.random.default_rng(PERMUTATION_SEED)
    null_counts = np.empty(N_PERMUTATIONS)
    for p in range(N_PERMUTATIONS):
        permuted_grid = np.empty_like(m1_grid)
        for seed in range(N_SEEDS):
            perm = rng.permutation(n_n)
            permuted_grid[seed] = m1_grid[seed, perm]
        permuted_mean = permuted_grid.mean(axis=0)
        null_counts[p] = sign_change_count(permuted_mean)

    p_value = float(np.mean(null_counts >= observed_sign_changes))
    verdict = "CONFIRMED" if p_value < 0.05 else "REJECTED"

    out = {
        "claim": "H-B2-4 -- multi-seed x permutation-test criterion for M1(N_DIM) "
        "non-monotonicity, fixing H-B2-1k's own identified CRITERION_INVALID flaw",
        "n_dim_values": list(N_DIM_VALUES),
        "n_seeds": N_SEEDS,
        "n_permutations": N_PERMUTATIONS,
        "mean_m1_by_n_dim": {str(n): float(v) for n, v in zip(N_DIM_VALUES, mean_m1)},
        "per_seed_m1_grid": m1_grid.tolist(),
        "observed_sign_changes": observed_sign_changes,
        "null_sign_changes_mean": float(null_counts.mean()),
        "null_sign_changes_p95": float(np.percentile(null_counts, 95)),
        "p_value": p_value,
        "verdict": verdict,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps({k: v for k, v in out.items() if k != "per_seed_m1_grid"}, indent=2, default=str)
    )
    return out


if __name__ == "__main__":
    cmd_run()
