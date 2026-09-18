"""MAIN TEST (FL step 6): prefix-consistent schedule vs the ZLDC anytime benchmark.

Pre-registered in ``pre_registration.md``:
    K = 24, N_train = {4,8,12,16,20,24}, N_test = {5,7,11,15,19,23},
    PASS iff R_n(candidate[:n]) / R_n(zldc[:n]) <= 1/1.05 at EVERY tested n.

Prefix-consistency is structural: there is exactly ONE ``master`` array of length K,
and horizon n is always scored on ``master[:n]``.  No per-horizon schedule object
exists anywhere in this file, so the Das Gupta per-horizon trap is unreachable by
construction rather than by convention.

Run:  python pep_prefix_search.py
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import numpy as np
from optimizer import PepCache, optimize_prefix_consistent
from pep_core import constant_schedule, silver_prefix, zldc_anytime_schedule

warnings.filterwarnings("ignore")

OUT = Path(__file__).parent / "metrics"
OUT.mkdir(exist_ok=True)

K = 24
N_TRAIN = [4, 8, 12, 16, 20, 24]
N_TEST = [5, 7, 11, 15, 19, 23]
MARGIN = 1.05
PASS_RATIO = 1.0 / MARGIN


def benchmark_values(horizons: list[int], cache: PepCache) -> dict[int, float]:
    zldc = np.array(zldc_anytime_schedule(max(horizons)))
    return {n: float(cache.value(zldc[:n]).value) for n in horizons}


def evaluate(master: np.ndarray, base: dict[int, float], cache: PepCache) -> dict:
    rows = {}
    for n, b in base.items():
        val = float(cache.value(master[:n]).value)
        rows[n] = {"R_n": val, "benchmark": b, "ratio": val / b}
    return rows


def main() -> None:
    cache = PepCache("R")
    all_h = sorted(set(N_TRAIN + N_TEST))
    base_all = benchmark_values(all_h, cache)
    base_train = {n: base_all[n] for n in N_TRAIN}

    rng = np.random.default_rng(7)
    zl = np.array(zldc_anytime_schedule(K))
    starts = [
        zl,
        np.array(silver_prefix(K)),
        np.array(constant_schedule(K, 1.5)),
        np.array(constant_schedule(K, 2.5)),
        np.clip(zl * rng.uniform(0.6, 1.6, size=K), 0.05, 50.0),
    ]

    # WHY this budget: one function evaluation costs ~5-18 s (six exact SDP solves, the
    # n=24 one alone ~2.3 s single-threaded).  The originally coded 5 starts x 3 betas x
    # 60 iterations was measured at ~6 h and was cut here.  The budget is a SEARCH
    # parameter, not part of the pre-registered design -- horizons, the 5% margin and the
    # PASS rule are unchanged -- and it only makes a PASS harder to find, never easier.
    t0 = time.time()
    best = optimize_prefix_consistent(
        N_TRAIN, base_train, cache, starts, betas=(30.0, 150.0), maxiter=35
    )
    elapsed = time.time() - t0

    master = np.array(best["master"])
    per_n = evaluate(master, base_all, cache)

    train_ratios = {n: per_n[n]["ratio"] for n in N_TRAIN}
    test_ratios = {n: per_n[n]["ratio"] for n in N_TEST}
    pass_train = all(r <= PASS_RATIO for r in train_ratios.values())
    pass_test = all(r <= PASS_RATIO for r in test_ratios.values())

    report = {
        "pre_registered": {
            "K": K,
            "N_train": N_TRAIN,
            "N_test": N_TEST,
            "margin": MARGIN,
            "pass_ratio_threshold": PASS_RATIO,
        },
        "benchmark": "Zhang-Lee-Du-Chen anytime schedule (arXiv:2411.17668), exact reconstruction",
        "master_schedule": best["master"],
        "zldc_prefix_K": zl.tolist(),
        "per_horizon": {str(n): per_n[n] for n in all_h},
        "worst_train_ratio": max(train_ratios.values()),
        "worst_test_ratio": max(test_ratios.values()),
        "best_ratio_anywhere": min(r["ratio"] for r in per_n.values()),
        "PASS_train": bool(pass_train),
        "PASS_test": bool(pass_test),
        "VERDICT": "PASS" if (pass_train and pass_test) else "FAIL",
        "seconds": round(elapsed, 1),
        "total_pep_solves": cache.n_solves,
    }
    (OUT / "prefix_search.json").write_text(json.dumps(report, indent=2))
    print(
        json.dumps(
            {
                k: report[k]
                for k in (
                    "worst_train_ratio",
                    "worst_test_ratio",
                    "best_ratio_anywhere",
                    "PASS_train",
                    "PASS_test",
                    "VERDICT",
                    "seconds",
                    "total_pep_solves",
                )
            },
            indent=2,
        )
    )
    for n in all_h:
        tag = "train" if n in N_TRAIN else "test "
        r = per_n[n]
        print(
            f"  n={n:>3} [{tag}] R_n={r['R_n']:.4e} "
            f"bench={r['benchmark']:.4e} ratio={r['ratio']:.4f}"
        )


if __name__ == "__main__":
    main()
