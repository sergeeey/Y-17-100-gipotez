"""Cheap preliminary read of the main test, as insurance against the full run's cost.

Same pre-registered horizons and same PASS rule as ``pep_prefix_search.py``, but a
much smaller optimiser budget.  It is NOT the experiment's answer: a smaller budget can
only make a PASS harder to find, so a FAIL here is weaker than the full run's FAIL and a
PASS here would be a genuine witness.  Reported separately, never merged into the main
result file.

Run:  python quick_probe.py
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
PASS_RATIO = 1.0 / 1.05


def main() -> None:
    cache = PepCache("R")
    zl = np.array(zldc_anytime_schedule(K))
    horizons = sorted(set(N_TRAIN + N_TEST))
    base = {n: float(cache.value(zl[:n]).value) for n in horizons}
    print("benchmark values computed", flush=True)

    starts = [zl, np.array(silver_prefix(K)), np.array(constant_schedule(K, 1.5))]
    t0 = time.time()
    best = optimize_prefix_consistent(
        N_TRAIN, {n: base[n] for n in N_TRAIN}, cache, starts, betas=(50.0,), maxiter=25
    )
    master = np.array(best["master"])
    ratios = {n: float(cache.value(master[:n]).value / base[n]) for n in horizons}
    verdict = "PASS" if all(r <= PASS_RATIO for r in ratios.values()) else "FAIL"
    report = {
        "note": "reduced-budget probe, not the pre-registered main result",
        "ratios": {str(n): round(v, 6) for n, v in ratios.items()},
        "worst_train_ratio": max(ratios[n] for n in N_TRAIN),
        "worst_test_ratio": max(ratios[n] for n in N_TEST),
        "best_ratio_anywhere": min(ratios.values()),
        "VERDICT": verdict,
        "master_schedule": [round(float(v), 6) for v in master],
        "seconds": round(time.time() - t0, 1),
    }
    (OUT / "quick_probe.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "master_schedule"}, indent=2))


if __name__ == "__main__":
    main()
