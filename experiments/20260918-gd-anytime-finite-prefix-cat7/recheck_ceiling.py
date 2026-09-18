"""Independent re-check of the ceiling at the horizons where it decides an argument.

``ceiling.py`` walks horizons in increasing order and warm-starts each one from the
previous optimum.  That is efficient but it makes neighbouring results correlated: a
bad local optimum propagates forward.  The first run produced a non-monotone sequence
(n=16 -> 0.9330, n=19 -> 0.9748), and the n=19 value is load-bearing -- if it is real,
the pre-registered 5% margin is out of reach at n=19 for *any* schedule under this
search, which changes what the main test's FAIL at that horizon means.

So the suspicious horizons are re-optimised from scratch with many diverse, mutually
unrelated starts and no warm-start chain.  A number that survives that is trustworthy
at the level a local search can deliver; a number that drops was a stuck local optimum.

Run:  python recheck_ceiling.py
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

HORIZONS = [15, 19, 23]
MAXITER = 120


def diverse_starts(n: int, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    zl = np.array(zldc_anytime_schedule(n))
    return [
        zl,
        np.array(silver_prefix(n)),
        np.array(constant_schedule(n, 1.0)),
        np.array(constant_schedule(n, 1.9)),
        np.array(constant_schedule(n, 3.0)),
        np.clip(zl * rng.uniform(0.5, 1.8, size=n), 0.05, 40.0),
        np.clip(rng.uniform(0.5, 6.0, size=n), 0.05, 40.0),
        np.clip(np.linspace(1.0, 6.0, n) * rng.uniform(0.8, 1.2, size=n), 0.05, 40.0),
    ]


def main() -> None:
    cache = PepCache("R")
    rows = {}
    for n in HORIZONS:
        zl = np.array(zldc_anytime_schedule(n))
        base = float(cache.value(zl).value)
        t0 = time.time()
        best = optimize_per_horizon(n, cache, diverse_starts(n, 1000 + n), maxiter=MAXITER)
        rows[n] = {
            "R_n_ceiling_recheck": best["value"],
            "R_n_benchmark": base,
            "ceiling_ratio_recheck": best["value"] / base,
            "max_improvement_factor": base / best["value"],
            "reaches_5pct_margin": bool(best["value"] / base <= 1.0 / 1.05),
            "n_starts": 8,
            "schedule": [round(float(v), 6) for v in best["schedule"]],
            "seconds": round(time.time() - t0, 1),
        }
        print(
            f"n={n:>3} ceiling_recheck={rows[n]['ceiling_ratio_recheck']:.4f} "
            f"(x{rows[n]['max_improvement_factor']:.3f}) "
            f"5%-reachable={rows[n]['reaches_5pct_margin']} ({rows[n]['seconds']}s)",
            flush=True,
        )

    report = {
        "method": "8 diverse cold starts per horizon, no warm-start chain",
        "maxiter": MAXITER,
        "per_horizon": {str(n): rows[n] for n in HORIZONS},
    }
    (OUT / "ceiling_recheck.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
