"""run.py -- H-B7-30: does replacing Monte Carlo escape-probability estimates with EXACT
probabilities (H-B7-26/28's own committed values) change the strength/interpretability of the
large-deviation-style fit log(P_escape) ~ -c*PNR_step, relative to the original informal report's
own r^2=0.8913?

Directly executes the user's own explicit priority item 4, deferred through H-B7-27/28/29 while
the branch-isomorphism mechanism thread was held per the user's own explicit instruction.

Reads only already-committed metrics/run.json files from H-B7-24, H-B7-26, H-B7-28 -- does not
re-run any simulation, since all the exact numbers needed already exist as committed artifacts.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
METRICS = HERE / "metrics"

H24_PATH = BASE / "20260910-remy-tumorigenesis-point-of-no-return-h24" / "metrics" / "run.json"
H26_PATH = BASE / "20260910-remy-tumorigenesis-exact-absorption-h26" / "metrics" / "run.json"
H28_PATH = BASE / "20260910-remy-tumorigenesis-full-domain-isomorphism-h28" / "metrics" / "run.json"

ORIGINAL_REPORT_R_SQUARED = 0.8913  # H9-A's own informal Monte-Carlo-based fit, for comparison


def linreg(xs: list[float], ys: list[float]) -> dict:
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    varx = sum((x - mx) ** 2 for x in xs)
    vary = sum((y - my) ** 2 for y in ys)
    slope = cov / varx if varx else float("nan")
    r = cov / math.sqrt(varx * vary) if varx and vary else float("nan")
    return {
        "n": n,
        "n_distinct_x": len(set(xs)),
        "slope": slope,
        "r": r,
        "r_squared": r * r,
    }


def cmd_run() -> dict:
    h24_data = json.loads(H24_PATH.read_text(encoding="utf-8"))
    h26_data = json.loads(H26_PATH.read_text(encoding="utf-8"))
    h28_data = json.loads(H28_PATH.read_text(encoding="utf-8"))

    pnr_by_cond = {
        (r["branch"], r["k"]): r["point_of_no_return_step"] for r in h24_data["per_state_results"]
    }
    h26_by_cond = {(r["branch"], r["k"]): r for r in h26_data["results"]}
    h28_by_k = {r["k"]: r for r in h28_data["results"]}

    # Primary axis: PNR-step, using branch_1's own exact values (branch_2 is isomorphic per
    # H-B7-27/28, so using both would not add independent information)
    xs_pnr: list[float] = []
    ys_log: list[float] = []
    per_k_detail = []
    for k in (1, 2, 3, 4):
        p = h28_by_k[k]["exact_escape_probability_branch_1"]
        pnr = pnr_by_cond[("branch_1", k)]
        logp = math.log(p)
        xs_pnr.append(pnr)
        ys_log.append(logp)
        per_k_detail.append({"k": k, "exact_escape_probability": p, "log_p": logp, "pnr_step": pnr})

    fit_pnr = linreg(xs_pnr, ys_log)

    # Alternative axes, as robustness checks (per claim.md's own stated design)
    xs_ntrans: list[float] = []
    xs_esta: list[float] = []
    ys_log_alt: list[float] = []
    for k in (1, 2, 3, 4):
        r26 = h26_by_cond[("branch_1", k)]
        p = r26["exact_escape_probability"]
        xs_ntrans.append(r26["n_transient"])
        xs_esta.append(r26["expected_steps_to_absorption"])
        ys_log_alt.append(math.log(p))

    fit_ntrans = linreg(xs_ntrans, ys_log_alt)
    fit_esta = linreg(xs_esta, ys_log_alt)

    # count how many of H-B7-22's own 40 originally-tested k values are non-trivial
    # (exact_escape_probability != 1.0) vs trivial
    n_nontrivial = sum(
        1 for r in h28_data["results"] if r["exact_escape_probability_branch_1"] != 1.0
    )
    n_trivial = len(h28_data["results"]) - n_nontrivial

    delta_r_squared = fit_pnr["r_squared"] - ORIGINAL_REPORT_R_SQUARED

    # Kill Criterion evaluation, per claim.md
    hypothesis_a_confirmed = fit_pnr["r_squared"] > 0.95 or fit_pnr["n_distinct_x"] >= 8
    hypothesis_b_confirmed = (
        abs(delta_r_squared) < 0.05 and fit_pnr["n_distinct_x"] <= 4 and n_nontrivial <= 4
    )

    verdict = (
        "CONFIRMED"
        if hypothesis_b_confirmed and not hypothesis_a_confirmed
        else ("CONFIRMED-HYPOTHESIS-A" if hypothesis_a_confirmed else "CRITERION_INVALID")
    )

    out = {
        "claim": "H-B7-30 -- exact probabilities do not rescue the large-deviation fit's own "
        "data-geometry limitation (few distinct PNR-step values, small effective sample size); "
        "the original r^2 was never a Monte Carlo noise artifact",
        "original_report_r_squared": ORIGINAL_REPORT_R_SQUARED,
        "fit_primary_pnr_step": fit_pnr,
        "fit_alternative_n_transient": fit_ntrans,
        "fit_alternative_expected_steps_to_absorption": fit_esta,
        "delta_r_squared_vs_original_report": delta_r_squared,
        "n_nontrivial_conditions_in_full_h_b7_22_domain": n_nontrivial,
        "n_trivial_conditions_in_full_h_b7_22_domain": n_trivial,
        "n_total_conditions_in_full_h_b7_22_domain": len(h28_data["results"]),
        "hypothesis_a_exactness_helps_confirmed": hypothesis_a_confirmed,
        "hypothesis_b_geometry_problem_persists_confirmed": hypothesis_b_confirmed,
        "verdict": verdict,
        "per_k_detail": per_k_detail,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
