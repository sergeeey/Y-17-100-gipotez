"""Cheapest differentiating test: the benchmark's own free parameter.

Everything else in this experiment perturbs ZLDC numerically, and every such
perturbation loses (see ``local_optimality_probe.py``).  But the ZLDC construction has
a genuine structural degree of freedom the perturbation probes cannot reach: the
parameter ``c`` in ``k_j = floor(2 * 2^{cj})``.  The paper fixes ``c = log2 rho`` because
that maximises the ASYMPTOTIC exponent ``(c + log2 rho)/(c + 1)``; nothing says it is
the best choice at ``n <= 24``.

Varying ``c`` yields a different, still prefix-consistent, still strictly positive,
still anytime-by-construction schedule -- i.e. it explores a direction the local probe
structurally cannot, at a cost of one worst-ratio evaluation per value of ``c``.

Run:  python c_sweep.py
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import numpy as np
from optimizer import PepCache
from pep_core import LOG2_RHO, zldc_anytime_schedule

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

    cs = [0.5, 0.7, 0.9, 1.0, 1.1, 1.2, LOG2_RHO, 1.35, 1.5, 1.8, 2.2, 3.0, 5.0]
    rows = []
    t0 = time.time()
    for c in cs:
        sched = np.array(zldc_anytime_schedule(K, c=c))
        ratios = {n: float(cache.value(sched[:n]).value / base[n]) for n in HORIZONS}
        worst = max(ratios.values())
        argmax = max(ratios, key=lambda n: ratios[n])
        rows.append(
            {
                "c": c,
                "is_paper_value": abs(c - LOG2_RHO) < 1e-12,
                "identical_to_benchmark": bool(np.allclose(sched, zl, atol=1e-9)),
                "worst_ratio": worst,
                "argmax_n": argmax,
                "best_ratio": min(ratios.values()),
                "n_horizons_beating_benchmark": sum(1 for r in ratios.values() if r < 1.0),
                "n_horizons_meeting_5pct": sum(1 for r in ratios.values() if r <= PASS_RATIO),
                "first_10": [round(float(v), 5) for v in sched[:10]],
            }
        )
        print(
            f"  c={c:<8.5f} worst={worst:10.4f} at n={argmax:<3} "
            f"best={rows[-1]['best_ratio']:.4f} "
            f"beat={rows[-1]['n_horizons_beating_benchmark']}/{len(HORIZONS)} "
            f"meet5%={rows[-1]['n_horizons_meeting_5pct']}",
            flush=True,
        )

    best_row = min(rows, key=lambda r: r["worst_ratio"])
    report = {
        "paper_value_of_c": LOG2_RHO,
        "horizons": HORIZONS,
        "rows": rows,
        "best_c_by_worst_ratio": best_row["c"],
        "best_worst_ratio": best_row["worst_ratio"],
        "any_c_meets_5pct_everywhere": bool(best_row["worst_ratio"] <= PASS_RATIO),
        "seconds": round(time.time() - t0, 1),
    }
    (OUT / "c_sweep.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
