"""POSITIVE CONTROL (controls.md): reproduce the published per-horizon result.

Das Gupta, Van Parys & Ryu (Math. Program. 2024) minimised R_n over ALL schedules
separately for each n <= 50 and reported a decay of roughly O(n^{-1.178}).  That is
a NON-anytime result -- the schedule is retuned per horizon -- and it is used here
only to check that this PEP harness can find good schedules at all.  If the fitted
exponent is nowhere near -1.178 the harness is untrustworthy and nothing downstream
means anything.

Also emits, for reference at the same horizons, R_n of the three published fixed
schedules (constant h=1, silver prefix, ZLDC anytime prefix).

Run:  python pep_unconstrained_baseline.py
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import numpy as np
from optimizer import PepCache, fit_power_law, optimize_per_horizon
from pep_core import GDPep, constant_schedule, silver_prefix, zldc_anytime_schedule

warnings.filterwarnings("ignore")

OUT = Path(__file__).parent / "metrics"
OUT.mkdir(exist_ok=True)

HORIZONS = [10, 20, 30, 40, 50]
# WHY a decreasing iteration budget: PEP solve cost grows ~n^3.5 here (0.01 s at
# n=10, 12.8 s at n=50).  A flat budget would spend the whole session on n=50.
MAXITER = {10: 400, 20: 300, 30: 200, 40: 150, 50: 120}


def reference_values() -> dict:
    rows = {}
    for n in HORIZONS:
        pep = GDPep(n, "R")
        rows[n] = {
            "constant_h1": float(pep.solve(np.array(constant_schedule(n, 1.0))).value),
            "silver_prefix": float(pep.solve(np.array(silver_prefix(n))).value),
            "zldc_anytime": float(pep.solve(np.array(zldc_anytime_schedule(n))).value),
        }
    return rows


def main() -> None:
    cache = PepCache("R")
    results = {}
    prev: np.ndarray | None = None

    for n in HORIZONS:
        starts: list[np.ndarray] = [
            np.array(zldc_anytime_schedule(n)),
            np.array(silver_prefix(n)),
            np.array(constant_schedule(n, 1.5)),
        ]
        if prev is not None:
            # warm start: previous optimum padded to the new length
            pad = np.full(n - prev.size, float(prev[-1]))
            starts.insert(0, np.concatenate([prev, pad]))
        if n >= 30:
            starts = starts[:2]  # budget: keep the warm start plus one cold start

        t0 = time.time()
        best = optimize_per_horizon(n, cache, starts, maxiter=MAXITER[n])
        best["seconds"] = round(time.time() - t0, 1)
        best["n_starts"] = len(starts)
        results[n] = best
        prev = np.array(best["schedule"])
        print(f"n={n}  R_n={best['value']:.6e}  ({best['seconds']}s, {best['nit']} it)", flush=True)

    ns = HORIZONS
    vals = [results[n]["value"] for n in ns]
    report = {
        "horizons": ns,
        "per_horizon_optimum": {str(n): results[n] for n in ns},
        "reference_schedules": {str(k): v for k, v in reference_values().items()},
        "fit_vs_N_steps": fit_power_law(ns, vals, offset=0),
        "fit_vs_N_plus_1_iterates": fit_power_law(ns, vals, offset=1),
        "literature_target_exponent": -1.178,
        "total_pep_solves": cache.n_solves,
    }
    (OUT / "positive_control.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if "fit" in k}, indent=2))


if __name__ == "__main__":
    main()
