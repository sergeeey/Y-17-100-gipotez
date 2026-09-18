"""Is ZLDC a local minimax optimum, or did the dense optimiser simply stall?

``dense_train_test.py`` -- trained on EVERY horizon 2..24 -- returned a master schedule
whose ratio to the benchmark is 1.0000000 at every single horizon, i.e. it came back
with the benchmark itself.  That is exactly the shape of result that has to be
distinguished from an optimiser failure before it is reported as a finding.

So the neighbourhood of ZLDC is probed directly, without any optimiser in the loop:

* **uniform scaling** ``lambda * zldc`` -- the one-parameter family the sparse run's
  solution actually lived in (it was ZLDC inflated by ~3.4% of total mass);
* **random directions** -- multiplicative perturbations at two step sizes;
* **single-coordinate** perturbations -- +-5% on one stepsize at a time.

For each candidate the reported quantity is the WORST ratio over horizons 2..24, which
is precisely the objective the dense run was minimising.  If no probe gets below 1.0,
ZLDC is a local minimax optimum of that objective at this resolution and the dense
result is a finding, not a stall.  If some probe does get below 1.0, the dense run
stalled and its result must be withdrawn.

Run:  python local_optimality_probe.py
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import numpy as np
from optimizer import PepCache
from pep_core import zldc_anytime_schedule

warnings.filterwarnings("ignore")

OUT = Path(__file__).parent / "metrics"
OUT.mkdir(exist_ok=True)

K = 24
HORIZONS = list(range(2, K + 1))


def main() -> None:
    cache = PepCache("R")
    zl = np.array(zldc_anytime_schedule(K))
    base = {n: float(cache.value(zl[:n]).value) for n in HORIZONS}

    def worst_ratio(h: np.ndarray) -> tuple[float, int]:
        worst, arg = -np.inf, -1
        for n in HORIZONS:
            r = float(cache.value(h[:n]).value / base[n])
            if r > worst:
                worst, arg = r, n
        return worst, arg

    t0 = time.time()
    probes = []

    for lam in (0.90, 0.95, 0.98, 0.99, 0.995, 1.005, 1.01, 1.02, 1.05, 1.10):
        w, arg = worst_ratio(lam * zl)
        probes.append({"kind": "uniform_scale", "param": lam, "worst_ratio": w, "argmax_n": arg})
        print(f"  scale {lam:<6} worst_ratio={w:.6f} at n={arg}", flush=True)

    rng = np.random.default_rng(20260918)
    for eps in (0.01, 0.05):
        for i in range(8):
            pert = zl * (1.0 + eps * rng.standard_normal(K))
            pert = np.clip(pert, 1e-3, 60.0)
            w, arg = worst_ratio(pert)
            probes.append(
                {
                    "kind": "random_direction",
                    "param": eps,
                    "trial": i,
                    "worst_ratio": w,
                    "argmax_n": arg,
                }
            )
        print(f"  random eps={eps}: done", flush=True)

    for k in (0, 1, 2, 8, 12, 16, 20, 23):
        for sgn in (-1.0, 1.0):
            pert = zl.copy()
            pert[k] *= 1.0 + 0.05 * sgn
            w, arg = worst_ratio(pert)
            probes.append(
                {"kind": "single_coord", "index": k, "sign": sgn, "worst_ratio": w, "argmax_n": arg}
            )
    print("  coordinate probes done", flush=True)

    below = [p for p in probes if p["worst_ratio"] < 1.0 - 1e-9]
    report = {
        "horizons": HORIZONS,
        "n_probes": len(probes),
        "probes": probes,
        "min_worst_ratio_over_probes": min(p["worst_ratio"] for p in probes),
        "n_probes_below_1": len(below),
        "probes_below_1": below,
        "CONCLUSION": (
            "ZLDC is a LOCAL MINIMAX OPTIMUM at this resolution -- no probe improved the "
            "worst-case ratio; the dense run's result is a finding, not a stall."
            if not below
            else "DENSE RUN STALLED -- a probe beat ZLDC; withdraw the dense result."
        ),
        "seconds": round(time.time() - t0, 1),
    }
    (OUT / "local_optimality_probe.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "probes"}, indent=2))


if __name__ == "__main__":
    main()
