"""Independent re-verification of every number that reaches the verdict.

Standing discipline in this project: a number is not reported until it has been
recomputed by a different route.  Here the main test's `R_n` values -- candidate and
benchmark alike -- are recomputed with **PEPit**, which builds and canonicalises its
own SDP from its own interpolation code, sharing nothing with `pep_core.py` except the
numeric stepsizes.

Also re-derives the PASS/FAIL verdict from the PEPit numbers alone, so the verdict is
not inherited from the run that produced it.

Run (after pep_prefix_search.py):  python verify_main_numbers.py
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
from pep_core import GDPep

warnings.filterwarnings("ignore")

OUT = Path(__file__).parent / "metrics"
PASS_RATIO = 1.0 / 1.05


def pepit_rn(gammas: list[float]) -> float:
    from PEPit import PEP
    from PEPit.functions import SmoothConvexFunction

    problem = PEP()
    func = problem.declare_function(SmoothConvexFunction, L=1.0)
    xs = func.stationary_point()
    fs = func(xs)
    x0 = problem.set_initial_point()
    problem.set_initial_condition((x0 - xs) ** 2 <= 1.0)
    x = x0
    for g in gammas:
        x = x - g * func.gradient(x)
    problem.set_performance_metric(func(x) - fs)
    return float(problem.solve(verbose=0))


def main() -> None:
    src = json.loads((OUT / "prefix_search.json").read_text())
    master = np.array(src["master_schedule"])
    zldc = np.array(src["zldc_prefix_K"])
    n_train = src["pre_registered"]["N_train"]
    n_test = src["pre_registered"]["N_test"]
    horizons = sorted(set(n_train + n_test))

    rows = {}
    for n in horizons:
        cand_p = pepit_rn(list(master[:n]))
        bench_p = pepit_rn(list(zldc[:n]))
        cand_c = float(GDPep(n, "R").solve(master[:n]).value)
        bench_c = float(GDPep(n, "R").solve(zldc[:n]).value)
        reported = src["per_horizon"][str(n)]
        rows[n] = {
            "candidate_pepit": cand_p,
            "candidate_cvxpy": cand_c,
            "candidate_reported": reported["R_n"],
            "benchmark_pepit": bench_p,
            "benchmark_cvxpy": bench_c,
            "benchmark_reported": reported["benchmark"],
            "ratio_pepit": cand_p / bench_p,
            "ratio_reported": reported["ratio"],
            "max_rel_disagreement": max(
                abs(cand_p - cand_c) / cand_c,
                abs(bench_p - bench_c) / bench_c,
                abs(cand_c - reported["R_n"]) / max(reported["R_n"], 1e-30),
                abs(bench_c - reported["benchmark"]) / max(reported["benchmark"], 1e-30),
            ),
            "verdict_flips": bool(
                (cand_p / bench_p <= PASS_RATIO) != (reported["ratio"] <= PASS_RATIO)
            ),
        }
        print(
            f"n={n:>3} ratio_pepit={rows[n]['ratio_pepit']:.5f} "
            f"ratio_reported={rows[n]['ratio_reported']:.5f} "
            f"max_rel_disagreement={rows[n]['max_rel_disagreement']:.2e} "
            f"flips={rows[n]['verdict_flips']}",
            flush=True,
        )

    verdict_pepit = "PASS" if all(r["ratio_pepit"] <= PASS_RATIO for r in rows.values()) else "FAIL"
    report = {
        "per_horizon": {str(n): rows[n] for n in horizons},
        "max_rel_disagreement_overall": max(r["max_rel_disagreement"] for r in rows.values()),
        "any_verdict_flip": any(r["verdict_flips"] for r in rows.values()),
        "VERDICT_from_pepit_alone": verdict_pepit,
        "VERDICT_reported_by_main_run": src["VERDICT"],
        "VERDICTS_AGREE": bool(verdict_pepit == src["VERDICT"]),
    }
    (OUT / "verify_main_numbers.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "per_horizon"}, indent=2))


if __name__ == "__main__":
    main()
