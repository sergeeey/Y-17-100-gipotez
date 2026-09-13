"""Point 37: does X (log-normalized Lovasz theta as a function of which generators are "on")
show submodularity or at least a sign bias in its mixed second differences?

Per the external re-plan's own prioritization, this is the cheapest genuinely NEW direction
left in this experiment: instead of another universal Johnson-graph/spectral inequality, check
whether X itself has Lovasz-specific second-order structure that could directly control
delta_i's variation.

Delta_i Delta_j X(S) := X(S) - X(S union {i}) - X(S union {j}) + X(S union {i,j})
for S not containing i or j. X is submodular iff this is <=0 everywhere (diminishing returns:
adding j helps X decrease -- recall X is a NEGATIVE-ish quantity via log-normalization -- less
once i is already present). Computed EXACTLY from the already-available full x array (reusing
solve_orbit_reduced's own output -- no new theta-solves needed), over ALL S not containing a
sampled (i,j) pair, for several n already computed elsewhere in this experiment.
"""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_spec = importlib.util.spec_from_file_location(
    "necklace_mod_submod", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)


def mixed_second_diff_all_pairs(x: np.ndarray, m: int, n_pairs: int, seed: int = 0):
    """Sample n_pairs distinct (i,j) generator-bit pairs (bits 0..m-1, i<j) and compute
    Delta_i Delta_j X(S) exactly over ALL S (subsets of the remaining m-2 bits)."""
    rng = random.Random(seed)
    all_bits = list(range(m))
    pairs = set()
    max_pairs = m * (m - 1) // 2
    n_pairs = min(n_pairs, max_pairs)
    while len(pairs) < n_pairs:
        i, j = rng.sample(all_bits, 2)
        pairs.add((min(i, j), max(i, j)))

    results = []
    for i, j in pairs:
        rest_bits = [b for b in all_bits if b not in (i, j)]
        n_rest = len(rest_bits)
        diffs = np.empty(1 << n_rest)
        for idx in range(1 << n_rest):
            base = 0
            for k, b in enumerate(rest_bits):
                if idx & (1 << k):
                    base |= 1 << b
            S = base
            Si = base | (1 << i)
            Sj = base | (1 << j)
            Sij = base | (1 << i) | (1 << j)
            diffs[idx] = x[S] - x[Si] - x[Sj] + x[Sij]
        results.append({"i": i, "j": j, "diffs": diffs})
    return results


def run_one(n: int, n_pairs: int = 10, seed: int = 0):
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))

    pair_results = mixed_second_diff_all_pairs(x, m, n_pairs, seed=seed)

    all_diffs = np.concatenate([pr["diffs"] for pr in pair_results])
    frac_nonpositive = float(np.mean(all_diffs <= 0))
    frac_negative_strict = float(np.mean(all_diffs < -1e-12))
    mean_diff = float(np.mean(all_diffs))
    std_diff = float(np.std(all_diffs))
    max_diff = float(np.max(all_diffs))
    min_diff = float(np.min(all_diffs))
    mean_abs = float(np.mean(np.abs(all_diffs)))
    second_moment = float(np.mean(all_diffs**2))

    per_pair = [
        {
            "i": pr["i"],
            "j": pr["j"],
            "frac_nonpositive": float(np.mean(pr["diffs"] <= 0)),
            "mean": float(np.mean(pr["diffs"])),
            "std": float(np.std(pr["diffs"])),
        }
        for pr in pair_results
    ]

    result = {
        "n": n,
        "m": m,
        "n_pairs_sampled": len(pair_results),
        "n_S_per_pair": len(pair_results[0]["diffs"]) if pair_results else 0,
        "frac_nonpositive": frac_nonpositive,
        "frac_negative_strict": frac_negative_strict,
        "mean_diff": mean_diff,
        "std_diff": std_diff,
        "max_diff": max_diff,
        "min_diff": min_diff,
        "mean_abs_diff": mean_abs,
        "second_moment": second_moment,
        "per_pair": per_pair,
    }
    print(
        f"n={n:3d} m={m:2d}  pairs={len(pair_results)}  frac(Delta<=0)={frac_nonpositive:.4f}  "
        f"mean={mean_diff:.6f}  std={std_diff:.6f}  range=[{min_diff:.6f},{max_diff:.6f}]  "
        f"E[Delta^2]={second_moment:.3e}",
        flush=True,
    )
    return result


def run(n_values: list[int], n_pairs: int = 10):
    rows = [run_one(n, n_pairs=n_pairs) for n in n_values]
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "submodularity_check.json", "w", encoding="utf-8") as f:
        json.dump({"rows": rows}, f, indent=2)
    return rows


if __name__ == "__main__":
    run([23, 29, 31, 37, 41])
