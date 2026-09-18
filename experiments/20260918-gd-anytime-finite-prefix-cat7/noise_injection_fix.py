"""Corrected noise-injection no-collapse test.

BUG FOUND AND FIXED (2026-09-18): in ``no_collapse_tests.py`` the start list is built as
five candidates and then truncated with ``[:n_starts]``.  With the budget reduction to
``n_starts = 2`` the truncation cut off exactly the two RANDOMISED starts, leaving
``[zldc, silver_prefix]`` -- which do not depend on ``seed`` at all.  The two
"noise_injection_seed_a/b" cases were therefore bit-identical computations, and their
matching numbers (worst_train 0.9714 / worst_test 3.4498 in both) were a tautology, not
evidence of stability.  A test that cannot vary is not a test.

This run does what that case was supposed to do: ONLY randomised starts, three
genuinely different seeds, same horizons and same PASS rule.

Run:  python noise_injection_fix.py
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import numpy as np
from optimizer import PepCache, optimize_prefix_consistent
from pep_core import zldc_anytime_schedule

warnings.filterwarnings("ignore")

OUT = Path(__file__).parent / "metrics"
OUT.mkdir(exist_ok=True)

K = 24
N_TRAIN = [4, 8, 12, 16, 20, 24]
N_TEST = [5, 7, 11, 15, 19, 23]
PASS_RATIO = 1.0 / 1.05
SEEDS = (101, 202, 303)


def main() -> None:
    cache = PepCache("R")
    zl = np.array(zldc_anytime_schedule(K))
    horizons = sorted(set(N_TRAIN + N_TEST))
    base = {n: float(cache.value(zl[:n]).value) for n in horizons}

    cases = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        starts = [
            np.clip(zl * rng.uniform(0.6, 1.6, size=K), 0.05, 50.0),
            np.clip(zl * rng.uniform(0.4, 2.2, size=K), 0.05, 50.0),
        ]
        t0 = time.time()
        best = optimize_prefix_consistent(
            N_TRAIN,
            {n: base[n] for n in N_TRAIN},
            cache,
            starts,
            betas=(40.0, 150.0),
            maxiter=20,
        )
        master = np.array(best["master"])
        ratios = {n: float(cache.value(master[:n]).value / base[n]) for n in horizons}
        cases.append(
            {
                "seed": seed,
                "starts": "randomised only (the bug's fix: no deterministic start in the list)",
                "ratios": {str(n): round(v, 5) for n, v in ratios.items()},
                "worst_train_ratio": max(ratios[n] for n in N_TRAIN),
                "worst_test_ratio": max(ratios[n] for n in N_TEST),
                "VERDICT": "PASS" if all(ratios[n] <= PASS_RATIO for n in horizons) else "FAIL",
                "mass_vs_benchmark": float(master.sum() / zl.sum()),
                "seconds": round(time.time() - t0, 1),
            }
        )
        print(
            f"  seed={seed} {cases[-1]['VERDICT']} "
            f"worst_train={cases[-1]['worst_train_ratio']:.4f} "
            f"worst_test={cases[-1]['worst_test_ratio']:.4f} "
            f"mass={cases[-1]['mass_vs_benchmark']:.4f}x ({cases[-1]['seconds']}s)",
            flush=True,
        )

    verdicts = {c["seed"]: c["VERDICT"] for c in cases}
    report = {
        "supersedes": (
            "no_collapse_tests.py cases noise_injection_seed_a/b (void: identical starts)"
        ),
        "cases": cases,
        "all_verdicts_identical": len(set(verdicts.values())) == 1,
        "verdicts": verdicts,
        "distinct_results": len({tuple(c["ratios"].values()) for c in cases}) > 1,
    }
    (OUT / "noise_injection_fixed.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}, indent=2))


if __name__ == "__main__":
    main()
