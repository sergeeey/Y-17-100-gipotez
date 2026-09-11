"""Single-generator sensitivity diagnostic for H-CAT31-3 (Efron-Stein target).

Tests the concrete, cheap, falsifiable numerical proxy for a bounded-differences /
Efron-Stein argument: for a random dense circulant graph G on n vertices, flip ONE
generator bit i (toggling both mirrored edges c[i], c[n-i] together, since that pair is
controlled by a single random bit -- see sample_circulant_neighbors) and measure

    Delta_i_theta = theta(G) - theta(G^(i))
    Delta_i_X     = log(theta(G)/sqrt(n)) - log(theta(G^(i))/sqrt(n))

The Efron-Stein bound Var(X_n) <= (1/4) sum_i E[(Delta_i X)^2] motivates checking whether
n^2 * E[(Delta_i X)^2] stabilizes as n grows (which is what a clean O(1/n) single-generator
influence, summed over m ~ n/2 generators, would require to give Var(X_n) = O(1/n)).

IMPORTANT CALIBRATION NOTE (per this session's own explicit user-caught overclaim on
2026-09-10 for H-CAT31-3's main decision.md -- same discipline applies here): a prior
external analysis claimed this sensitivity question was "already investigated by Faure's
earlier work and left unresolved." That specific claim could NOT be verified from a
primary source (ResearchGate returned 403); it is [WEAK]-sourced (search-engine paraphrase
only), not [VERIFIED]. This script tests the underlying MATHEMATICAL question on its own
merits -- it does not rely on, or need, that provenance claim to be true.

n is NOT restricted to primes here (128/512/1536 are all powers of 2 / 2*3), so the
multiplicative-group transitivity argument that would make all generator influences
identical does not strictly apply. To average out potential heterogeneity across
generator indices without a large cost increase, each replicate tests a FIXED small set
of 3 generator indices (spread across the available range) rather than one fixed index,
and the reported influence is the mean over both replicates and indices.

Reuses sample_circulant_neighbors/theta_via_lp from H-CAT31-1 UNCHANGED.
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

RNG_SEED_BASE = 333000  # distinct from 31000 / 331000 / 332000 used elsewhere in this arc


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("h_cat31_3_sens_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
theta_via_lp = h_cat31_1.theta_via_lp

# (n, reps) -- kept modest since each rep now costs 1 + len(test_indices) theta_via_lp calls.
N_REPS = [(128, 60), (512, 60), (1536, 25)]


def flip_generator(c: np.ndarray, i: int) -> np.ndarray:
    """Return a copy of c with generator bit i toggled (both mirrored edges c[i],c[n-i])."""
    n = len(c)
    c2 = c.copy()
    c2[i] = 1.0 - c2[i]
    c2[n - i] = 1.0 - c2[n - i]
    return c2


def run() -> dict:
    rows = []
    for n, reps in N_REPS:
        half = (n - 1) // 2
        test_indices = sorted({1, max(1, half // 3), max(1, 2 * half // 3)})
        t0 = time.time()
        delta_theta_sq = []
        delta_x_sq = []
        for rep in range(reps):
            seed = RNG_SEED_BASE + n * 1000 + rep
            c = sample_circulant_neighbors(n, 0.5, seed)
            theta0 = theta_via_lp(c)
            x0 = np.log(theta0 / np.sqrt(n))
            for i in test_indices:
                c_flip = flip_generator(c, i)
                theta1 = theta_via_lp(c_flip)
                x1 = np.log(theta1 / np.sqrt(n))
                delta_theta_sq.append((theta0 - theta1) ** 2)
                delta_x_sq.append((x0 - x1) ** 2)
        elapsed = time.time() - t0

        delta_theta_sq = np.array(delta_theta_sq)
        delta_x_sq = np.array(delta_x_sq)
        mean_dtheta2 = float(delta_theta_sq.mean())
        se_dtheta2 = float(delta_theta_sq.std(ddof=1) / np.sqrt(len(delta_theta_sq)))
        mean_dx2 = float(delta_x_sq.mean())
        se_dx2 = float(delta_x_sq.std(ddof=1) / np.sqrt(len(delta_x_sq)))

        # Efron-Stein-style sum over ~half generators (assuming rough homogeneity across i,
        # which is exactly what test_indices partially checks -- see per-index breakdown).
        efron_stein_bound_on_var_X = 0.25 * half * mean_dx2

        rows.append(
            {
                "n": n,
                "half_m": half,
                "reps": reps,
                "test_indices": test_indices,
                "n_samples": len(delta_theta_sq),
                "mean_delta_theta_sq": mean_dtheta2,
                "se_delta_theta_sq": se_dtheta2,
                "n_times_mean_delta_theta_sq": n * mean_dtheta2,
                "mean_delta_x_sq": mean_dx2,
                "se_delta_x_sq": se_dx2,
                "n_sq_times_mean_delta_x_sq": (n**2) * mean_dx2,
                "efron_stein_bound_on_var_X": efron_stein_bound_on_var_X,
                "elapsed_seconds": elapsed,
            }
        )
        print(
            f"n={n:5d} half_m={half:5d} reps={reps:3d} idx={test_indices} "
            f"E[dtheta^2]={mean_dtheta2:.4f}+-{se_dtheta2:.4f} "
            f"n*E[dtheta^2]={n * mean_dtheta2:.3f} "
            f"E[dX^2]={mean_dx2:.6e}+-{se_dx2:.2e} n^2*E[dX^2]={(n**2) * mean_dx2:.4f} "
            f"ES_bound_VarX={efron_stein_bound_on_var_X:.6f} elapsed={elapsed:.1f}s",
            flush=True,
        )
    return {"rows": rows}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "single_generator_sensitivity.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
