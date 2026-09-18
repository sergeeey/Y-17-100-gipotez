"""Confirms the LP-found descent direction actually improves worst_ratio at a small step.

The LP (local_minimax_lp.py) found a first-order descent direction with t=-0.219 <0.
First-order guarantees only hold for infinitesimally small steps -- confirm it directly
on the real (non-linearized) worst_ratio objective at decreasing step sizes.
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

    lp_result = json.loads(
        (Path(__file__).parent / "metrics" / "local_minimax_lp.json").read_text()
    )
    d = np.array(lp_result["direction"])

    baseline_worst, _ = worst_ratio(cache, zl, base)
    print(f"baseline: worst_ratio={baseline_worst:.9f}")

    results = []
    for sign, sign_label in ((1.0, "+d"), (-1.0, "-d")):
        for step in (0.1, 0.03, 0.01, 0.003, 0.001, 0.0003, 0.0001):
            candidate = zl + sign * step * d
            w, arg = worst_ratio(cache, candidate, base)
            improvement = baseline_worst - w
            print(
                f"{sign_label} step={step:<8} worst_ratio={w:.9f}  "
                f"(improvement={improvement:+.9f})  binding n={arg}"
            )
            results.append({"sign": sign_label, "step": step, "worst_ratio": w, "argmax_n": arg})

    out = {"baseline_worst_ratio": baseline_worst, "steps": results}
    (Path(__file__).parent / "metrics" / "verify_lp_direction.json").write_text(
        json.dumps(out, indent=2)
    )


if __name__ == "__main__":
    main()
