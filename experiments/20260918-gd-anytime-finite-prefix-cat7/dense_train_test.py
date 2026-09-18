"""STRONGEST-CASE variant: train the prefix-consistent schedule on EVERY horizon.

The pre-registered main test trains on a sparse horizon set and scores a disjoint one,
so a FAIL there confounds two different causes:

  (i) no prefix-consistent schedule can beat the benchmark by 5% everywhere, or
  (ii) one might exist, but optimising on six horizons does not find it.

This run removes (ii) by making the training set *every* horizon 2..24, i.e. exactly
the quantity the PASS rule cares about (the worst ratio over all tested n) is what the
optimiser minimises.  There is no unseen horizon left, so a FAIL here is a statement
about the constraint, not about generalisation.

It is a SEPARATE, post-registration run and is reported as such; it does not replace
the pre-registered train/test result.

Run:  python dense_train_test.py
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
HORIZONS = list(range(2, K + 1))
PASS_RATIO = 1.0 / 1.05


def main() -> None:
    cache = PepCache("R")
    zl = np.array(zldc_anytime_schedule(K))
    base = {n: float(cache.value(zl[:n]).value) for n in HORIZONS}
    print("benchmark computed", flush=True)

    starts = [zl, np.array(silver_prefix(K)), np.array(constant_schedule(K, 1.5))]
    t0 = time.time()
    best = optimize_prefix_consistent(
        HORIZONS, base, cache, starts, betas=(30.0, 150.0), maxiter=30
    )
    master = np.array(best["master"])
    ratios = {n: float(cache.value(master[:n]).value / base[n]) for n in HORIZONS}
    worst = max(ratios.values())
    n_meeting = [n for n, r in ratios.items() if r <= PASS_RATIO]

    report = {
        "note": "post-registration strongest-case run: every horizon is a training horizon",
        "K": K,
        "horizons": HORIZONS,
        "pass_ratio_threshold": PASS_RATIO,
        "ratios": {str(n): round(v, 6) for n, v in ratios.items()},
        "worst_ratio": worst,
        "best_ratio": min(ratios.values()),
        "mean_ratio": float(np.mean(list(ratios.values()))),
        "horizons_meeting_5pct": n_meeting,
        "n_horizons_meeting_5pct": len(n_meeting),
        "n_horizons_total": len(HORIZONS),
        "horizons_worse_than_benchmark": [n for n, r in ratios.items() if r > 1.0],
        "VERDICT": "PASS" if worst <= PASS_RATIO else "FAIL",
        "master_schedule": [round(float(v), 6) for v in master],
        "zldc_prefix": [round(float(v), 6) for v in zl],
        "seconds": round(time.time() - t0, 1),
        "total_pep_solves": cache.n_solves,
    }
    (OUT / "dense_train_test.json").write_text(json.dumps(report, indent=2))
    print(
        json.dumps(
            {
                k: v
                for k, v in report.items()
                if k not in ("ratios", "master_schedule", "zldc_prefix")
            },
            indent=2,
        )
    )
    for n in HORIZONS:
        print(f"  n={n:>3} ratio={ratios[n]:.4f} {'OK' if ratios[n] <= PASS_RATIO else ''}")


if __name__ == "__main__":
    main()
