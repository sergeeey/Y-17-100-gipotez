"""Positive-control analysis: pool every per-horizon optimum, and be explicit about
how much of the fitted exponent is optimiser quality rather than mathematics.

The pre-registered run (``pep_unconstrained_baseline.py``, n in {10,20,30,40,50})
completed, but its large-n points are not optima:

    n=10  ratio 0.9145  168 it  ABNORMAL exit
    n=20  ratio 0.8407  300 it  hit maxiter
    n=30  ratio 0.9806  106 it  "converged"
    n=40  ratio 0.9976    3 it  ABNORMAL exit   <- 3 iterations is not an optimisation
    n=50  ratio 0.9856   41 it  "converged"

n=30/40/50 come from the same warm-start chain whose sticking was independently
demonstrated at n=15 (cold starts moved the ceiling 0.9490 -> 0.9198), and they were
never cold-started.  "Converged" does not mean "good": n=30 and n=50 converged to ratios
of 0.98, far off the 0.87-0.93 band that cold-started optimisation produces at n <= 23.

So this script reports the fit several ways -- all horizons pooled, the pre-registered
run alone, and only the cold-start-verified range -- and states plainly how far apart
they are.  The spread between defensible fits, not any one fit's standard error, is the
honest uncertainty on the exponent.

Run:  python positive_control_analysis.py
"""

from __future__ import annotations

import json
import re
import warnings
from pathlib import Path

import numpy as np
from optimizer import fit_power_law
from pep_core import GDPep, zldc_anytime_schedule

warnings.filterwarnings("ignore")

OUT = Path(__file__).parent / "metrics"
LITERATURE_EXPONENT = -1.178  # Das Gupta et al., empirical, n <= 50, no stated uncertainty


def main() -> None:
    bench: dict[int, float] = {}

    def b(n: int) -> float:
        if n not in bench:
            bench[n] = float(GDPep(n, "R").solve(np.array(zldc_anytime_schedule(n))).value)
        return bench[n]

    best: dict[int, tuple[float, str]] = {}

    def add(n: int, val: float, src: str) -> None:
        if n not in best or val < best[n][0]:
            best[n] = (val, src)

    for line in (OUT / "ceiling_warmstart_partial.log").read_text().splitlines():
        m = re.match(r"n=\s*(\d+) ceiling_ratio=([\d.]+)", line.strip())
        if m:
            n = int(m.group(1))
            add(n, float(m.group(2)) * b(n), "ceiling_warmstart_chain")
    for k, v in json.loads((OUT / "ceiling_recheck.json").read_text())["per_horizon"].items():
        add(int(k), v["R_n_ceiling_recheck"], "ceiling_8_cold_starts")
    pc = json.loads((OUT / "positive_control.json").read_text())
    for k, v in pc["per_horizon_optimum"].items():
        add(int(k), v["value"], f"positive_control(nit={v['nit']})")

    ns = sorted(best)
    rows = [
        {
            "n": n,
            "R_n": best[n][0],
            "benchmark": b(n),
            "ratio": best[n][0] / b(n),
            "source": best[n][1],
        }
        for n in ns
    ]

    # Filter stated on PROVENANCE, not on values -- deliberately, so it cannot be a
    # residual-based exclusion dressed up as a quality criterion.  Cold-start
    # verification was only ever performed at n <= 23 (recheck_ceiling.py), and the
    # warm-start chain's sticking was demonstrated there (n=15: 0.9490 -> 0.9198).
    # n = 30, 40, 50 lie outside that verified range and were reached ONLY through the
    # chain, so they are upper bounds on R_n, not optima.  Nothing about their ratios
    # enters this rule.
    #
    # An earlier version of this filter used "ratio < 0.95", which wrongly dropped n=19
    # -- a horizon that WAS cold-started with 8 starts and whose high ratio (0.9673) is a
    # real property of that horizon, not under-optimisation.  Corrected here.
    COLD_START_VERIFIED_MAX_N = 23
    converged = [n for n in ns if n <= COLD_START_VERIFIED_MAX_N]

    fits = {
        "all_horizons_vs_N": fit_power_law(ns, [best[n][0] for n in ns], offset=0),
        "converged_only_vs_N": fit_power_law(converged, [best[n][0] for n in converged], offset=0),
        "converged_only_vs_N_plus_1": fit_power_law(
            converged, [best[n][0] for n in converged], offset=1
        ),
        "preregistered_run_only_vs_N": pc["fit_vs_N_steps"],
        "preregistered_run_only_vs_N_plus_1": pc["fit_vs_N_plus_1_iterates"],
    }

    # WHY compare only same-convention fits: the "vs N+1 iterates" variants differ by an
    # index convention, not by data quality, so pooling them would inflate the spread for
    # the wrong reason.
    same_conv = [k for k in fits if not k.endswith("_plus_1")]
    exps = [fits[k]["exponent"] for k in same_conv]
    spread = float(max(exps) - min(exps))
    max_se = float(max(fits[k]["stderr"] for k in same_conv))
    report = {
        "literature_exponent": LITERATURE_EXPONENT,
        "per_horizon_best_known": rows,
        "cold_start_verified_horizons_used": converged,
        "excluded_horizons": [n for n in ns if n not in converged],
        "exclusion_rule": (
            "provenance-based: n > 23 was never cold-started, so those points are upper "
            "bounds on R_n rather than optima.  No value-based criterion is used."
        ),
        "fits": fits,
        "exponent_spread_same_convention": spread,
        "largest_single_fit_stderr": max_se,
        "spread_over_stderr": round(spread / max_se, 1),
        "honest_uncertainty_note": (
            f"The spread across same-convention fits is {spread:.3f}, i.e. "
            f"{spread / max_se:.1f}x the largest individual fit's standard error "
            f"({max_se:.3f}).  The fitted exponent is dominated by per-horizon optimiser "
            "quality, not by the underlying mathematics, so no single value should be "
            "quoted as an estimate of the per-horizon-optimal rate, and the formal "
            "standard errors understate the real uncertainty."
        ),
        "positive_control_verdict": (
            "PASS on its actual function -- the harness finds schedules up to 15.9% better "
            "than the published anytime benchmark (n=20, ratio 0.8407) and 8.6% better at "
            "n=10 -- but it does NOT cleanly reproduce the literature's -1.178 exponent, "
            "because under-optimisation at large n biases the fit toward flatness."
        ),
    }
    (OUT / "positive_control_analysis.json").write_text(json.dumps(report, indent=2))

    print(f"{'n':>4} {'R_n':>13} {'ratio':>8}  source")
    for r in rows:
        print(f"{r['n']:>4} {r['R_n']:13.6e} {r['ratio']:8.4f}  {r['source']}")
    print(f"\ncold-start-verified horizons used: {converged}")
    print(f"excluded (never cold-started): {report['excluded_horizons']}")
    for k, f in fits.items():
        print(f"  {k:<36} {f['exponent']:+.4f} +/- {f['stderr']:.4f}  r2={f['r2']:.5f}")
    print(
        f"\nspread (same convention): {spread:.4f} = {report['spread_over_stderr']}x largest stderr"
    )
    print(report["honest_uncertainty_note"])


if __name__ == "__main__":
    main()
