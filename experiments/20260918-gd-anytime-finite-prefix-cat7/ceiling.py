"""CEILING for the main test -- what is even achievable before prefix-consistency.

Floor-Ceiling discipline (this project's own pearl registry, 2026-08-30/2026-09-02):
a negative result is uninterpretable without an ARM-CEILING -- a competitor allowed
to cheat in exactly the way the hypothesis forbids.

Here the ceiling is the per-horizon optimum: at each tested horizon n, the best
POSSIBLE R_n over ALL length-n schedules, with no cross-horizon coupling at all.
Any prefix-consistent schedule is a feasible point of that unconstrained problem,
so

    ratio_prefix(n)  >=  ratio_ceiling(n)   for every n,

and the pre-registered 5% PASS is unreachable at any n where the ceiling itself is
weaker than 5%.  Without this number, a FAIL cannot be attributed to the prefix
constraint rather than to the benchmark simply being near-optimal at that horizon.

Run:  python ceiling.py
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import numpy as np
from optimizer import PepCache, optimize_per_horizon
from pep_core import constant_schedule, silver_prefix, zldc_anytime_schedule

warnings.filterwarnings("ignore")

OUT = Path(__file__).parent / "metrics"
OUT.mkdir(exist_ok=True)

HORIZONS = [4, 5, 7, 8, 11, 12, 15, 16, 19, 20, 23, 24]  # N_train u N_test of pre_registration.md


def main() -> None:
    cache = PepCache("R")
    zl = np.array(zldc_anytime_schedule(max(HORIZONS)))
    rows = {}
    prev: np.ndarray | None = None
    for n in HORIZONS:
        base = float(cache.value(zl[:n]).value)
        starts = [zl[:n].copy(), np.array(silver_prefix(n)), np.array(constant_schedule(n, 1.5))]
        if prev is not None and prev.size < n:
            starts.insert(0, np.concatenate([prev, np.full(n - prev.size, float(prev[-1]))]))
        t0 = time.time()
        best = optimize_per_horizon(n, cache, starts, maxiter=250)
        prev = np.array(best["schedule"])
        rows[n] = {
            "R_n_ceiling": best["value"],
            "R_n_benchmark_zldc": base,
            "ceiling_ratio": best["value"] / base,
            "max_possible_improvement_factor": base / best["value"],
            "ceiling_reaches_5pct_margin": bool(best["value"] / base <= 1.0 / 1.05),
            "schedule": [round(float(v), 6) for v in prev],
            "seconds": round(time.time() - t0, 1),
        }
        print(
            f"n={n:>3} ceiling_ratio={rows[n]['ceiling_ratio']:.4f} "
            f"(max improvement x{rows[n]['max_possible_improvement_factor']:.3f}) "
            f"5%-reachable={rows[n]['ceiling_reaches_5pct_margin']}",
            flush=True,
        )

    report = {
        "horizons": HORIZONS,
        "per_horizon": {str(n): rows[n] for n in HORIZONS},
        "worst_ceiling_ratio": max(r["ceiling_ratio"] for r in rows.values()),
        "all_horizons_5pct_reachable": all(r["ceiling_reaches_5pct_margin"] for r in rows.values()),
        "horizons_where_5pct_unreachable": [
            n for n in HORIZONS if not rows[n]["ceiling_reaches_5pct_margin"]
        ],
        "total_pep_solves": cache.n_solves,
    }
    (OUT / "ceiling.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "per_horizon"}, indent=2))


if __name__ == "__main__":
    main()
