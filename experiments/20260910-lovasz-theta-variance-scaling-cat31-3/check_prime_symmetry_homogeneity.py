"""Prime-n generator-homogeneity diagnostic (Mechanism Development Mode, continued).

Tests a concrete, checkable claim from an external AI analysis (NOT trusted at face value,
independently re-verified above in decision.md's Addendum): for PRIME n, the multiplicative
group Z_n^x acts transitively on the m=(n-1)/2 generator indices (since a is a unit mod n
iff gcd(a,n)=1, i.e. all of 1..n-1 for prime n, and multiplication by a unit permutes the
generator-pair set {1,...,m} up to relabeling +/- pairs). This graph automorphism argument
predicts that for prime n, the single-generator sensitivity E[(Delta_i X)^2] should be
(nearly) IDENTICAL across index i -- whereas for composite n (as tested throughout this
whole H-CAT31-3 sensitivity arc: 128, 512, 1536, 3000, ALL composite), no such symmetry
argument applies, so heterogeneity across i is structurally expected, not just noise.

This script checks that prediction directly: prime n=127 (close to the already-tested
composite n=128, for comparable scale) vs composite n=128 itself, sampling 7 spread-out
generator indices per replicate (vs the 3 used in the main sensitivity script) and reporting
the across-index coefficient of variation (CV = std/mean) of the per-index mean
E[(Delta_i X)^2] -- prediction: CV(prime) << CV(composite) if the symmetry argument has
real, detectable force at this scale (not guaranteed -- n=127 is small, so per-index
estimates are themselves noisy; this is a first, cheap, directional reading, not a
definitive test).

Reuses sample_circulant_neighbors/theta_via_lp from H-CAT31-1 UNCHANGED.
"""

from __future__ import annotations

import importlib.util
import json
import time
from math import gcd
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"

RNG_SEED_BASE = 334000  # distinct from 31000/331000/332000/333000 used elsewhere in this arc


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("h_cat31_3_primesym_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
theta_via_lp = h_cat31_1.theta_via_lp


def is_prime(k: int) -> bool:
    if k < 2:
        return False
    for d in range(2, int(k**0.5) + 1):
        if k % d == 0:
            return False
    return True


def flip_generator(c: np.ndarray, i: int) -> np.ndarray:
    n = len(c)
    c2 = c.copy()
    c2[i] = 1.0 - c2[i]
    c2[n - i] = 1.0 - c2[n - i]
    return c2


N_CASES = [(127, True), (128, False)]  # (n, is_prime) -- 127 is prime, 128 = 2^7
REPS = 150


def spread_indices(half: int, k: int = 7) -> list[int]:
    idx = sorted({max(1, round(j * half / k)) for j in range(1, k + 1)})
    return [i for i in idx if 1 <= i <= half]


def run() -> dict:
    rows = []
    for n, expected_prime in N_CASES:
        assert is_prime(n) == expected_prime, f"n={n} primality mismatch"
        half = (n - 1) // 2
        indices = spread_indices(half, 7)
        # sanity: for prime n, every i in 1..half must be coprime to n (true whenever n prime
        # and 1<=i<n) -- gcd check is a cheap positive control on the symmetry precondition.
        if expected_prime:
            assert all(gcd(i, n) == 1 for i in indices)

        t0 = time.time()
        per_index_sq: dict[int, list[float]] = {i: [] for i in indices}
        for rep in range(REPS):
            seed = RNG_SEED_BASE + n * 1000 + rep
            c = sample_circulant_neighbors(n, 0.5, seed)
            theta0 = theta_via_lp(c)
            x0 = np.log(theta0 / np.sqrt(n))
            for i in indices:
                c_flip = flip_generator(c, i)
                theta1 = theta_via_lp(c_flip)
                x1 = np.log(theta1 / np.sqrt(n))
                per_index_sq[i].append((x0 - x1) ** 2)
        elapsed = time.time() - t0

        per_index_mean = {i: float(np.mean(v)) for i, v in per_index_sq.items()}
        per_index_se = {
            i: float(np.std(v, ddof=1) / np.sqrt(len(v))) for i, v in per_index_sq.items()
        }
        means = np.array(list(per_index_mean.values()))
        cv = float(means.std(ddof=1) / means.mean()) if means.mean() > 0 else float("nan")

        rows.append(
            {
                "n": n,
                "is_prime": expected_prime,
                "half_m": half,
                "reps": REPS,
                "indices": indices,
                "per_index_mean_delta_x_sq": per_index_mean,
                "per_index_se": per_index_se,
                "across_index_mean": float(means.mean()),
                "across_index_std": float(means.std(ddof=1)),
                "across_index_cv": cv,
                "elapsed_seconds": elapsed,
            }
        )
        print(
            f"n={n:4d} prime={expected_prime} indices={indices} "
            f"across_index_mean={means.mean():.6e} across_index_CV={cv:.4f} "
            f"elapsed={elapsed:.1f}s",
            flush=True,
        )
        for i in indices:
            print(
                f"    i={i:4d} E[dX^2]={per_index_mean[i]:.6e} +- {per_index_se[i]:.2e}",
                flush=True,
            )
    return {"rows": rows}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "prime_symmetry_homogeneity.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
