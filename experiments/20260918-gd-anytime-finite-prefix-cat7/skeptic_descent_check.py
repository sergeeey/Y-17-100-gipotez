"""Independent execution of the skeptic's proposed explicit descent direction.

The skeptic (FL Step 8a dispatch, 2026-09-18) hand-derived a perturbation that should
strictly improve worst_ratio below 1.0, using closed forms verified by hand (not
executed). This script runs it with the project's own PEP evaluator to get a real,
executed answer instead of trusting hand arithmetic either way.

Skeptic's proposed direction: delta_k = -d for odd k, delta_k = +(d+u) for even k,
with d=0.01, u=0.005 (additive, in absolute stepsize units, applied to zldc).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from optimizer import PepCache
from pep_core import zldc_anytime_schedule

K = 24
HORIZONS = list(range(2, K + 1))


def worst_ratio(cache: PepCache, h: np.ndarray, base: dict[int, float]) -> tuple[float, int]:
    worst, arg = -np.inf, -1
    for n in HORIZONS:
        r = float(cache.value(h[:n]).value / base[n])
        if r > worst:
            worst, arg = r, n
    return worst, arg


def main() -> None:
    cache = PepCache("R")
    zl = np.array(zldc_anytime_schedule(K))
    base = {n: float(cache.value(zl[:n]).value) for n in HORIZONS}

    baseline_worst, baseline_arg = worst_ratio(cache, zl, base)
    print(f"baseline (ZLDC itself): worst_ratio={baseline_worst:.9f} at n={baseline_arg}")

    d, u = 0.01, 0.005
    delta = np.array([(-d if k % 2 == 1 else (d + u)) for k in range(K)])
    candidate = zl + delta
    cand_worst, cand_arg = worst_ratio(cache, candidate, base)
    print(f"skeptic direction:      worst_ratio={cand_worst:.9f} at n={cand_arg}")
    print("predicted by skeptic:   worst_ratio~=0.9989")
    print(f"improvement over ZLDC:  {baseline_worst - cand_worst:.9f}")

    result = {
        "baseline_worst_ratio": baseline_worst,
        "baseline_argmax_n": baseline_arg,
        "candidate_worst_ratio": cand_worst,
        "candidate_argmax_n": cand_arg,
        "d": d,
        "u": u,
        "verdict": (
            "SKEPTIC_CONFIRMED_local_optimum_falsified"
            if cand_worst < baseline_worst
            else "SKEPTIC_DIRECTION_DID_NOT_IMPROVE"
        ),
    }
    out = Path(__file__).parent / "metrics" / "skeptic_descent_check.json"
    out.write_text(json.dumps(result, indent=2))
    print(f"\nverdict: {result['verdict']}")
    print(f"written to {out}")


if __name__ == "__main__":
    main()
