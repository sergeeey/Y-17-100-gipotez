"""INDEPENDENT verification that the reconstructed benchmark really is ZLDC's schedule.

The benchmark is the single load-bearing external object in this experiment: if the
reconstruction of ``phi``/``concat``/``k_j`` is wrong, every ratio in the main test is
meaningless.  Matching the paper's prose is not enough, so the reconstruction is
checked against three of the paper's own *consequences*, each computed by a route that
does not reuse the reconstruction's arithmetic:

1. **Primitivity (Definition 2)** — a PEP with a different objective.  A schedule is
   primitive iff `A_k(f_k-f*) + C_k||g_k||^2 + 0.5||x_k-x*||^2 <= 0.5||x_1-x*||^2`
   over the whole function class.  A wrong join stepsize breaks this.  Checked for the
   silver schedules `s_bar_i` (Lemma 6) and for the ZLDC partial concatenations
   `s_hat_i` at their own endpoints (Lemma 4).
2. **Endpoint rate (eq. 38a)** — primitivity implies `f_k - f* <= ||x_1-x*||^2 / A_k`.
   Checked directly against the exact PEP worst case.
3. **Lemma 7 lower bound on the aggregate stepsize** — `A_{t+1} >= t^{(c+log2 rho)/(c+1)} / 36`
   for every `t`, a purely arithmetic property of the construction that a mis-specified
   `k_j` would violate.

A negative control is included: the SAME primitivity test applied to schedules that are
NOT primitive, to confirm the test can fail at all.

Run:  python verify_benchmark_reconstruction.py
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path

import numpy as np
from pep_core import (
    LOG2_RHO,
    RHO,
    GDPep,
    constant_schedule,
    silver_schedule,
    zldc_anytime_schedule,
    zldc_concat_endpoints,
)

warnings.filterwarnings("ignore")

OUT = Path(__file__).parent / "metrics"
OUT.mkdir(exist_ok=True)
TOL = 1e-6  # absolute slack allowed on the 0.5 primitivity bound


def primitivity_row(name: str, h: list[float]) -> dict:
    n = len(h)
    pep = GDPep(n, "R")
    lhs = pep.solve_primitivity(np.array(h))
    a_k = float(sum(h))
    rn = float(pep.solve(np.array(h)).value)
    return {
        "name": name,
        "n_steps": n,
        "A_k": a_k,
        "primitivity_lhs_max": lhs,
        "primitivity_bound": 0.5,
        "is_primitive": bool(lhs <= 0.5 + TOL),
        "slack": 0.5 - lhs,
        "R_n": rn,
        "endpoint_rate_bound_1_over_A": 1.0 / a_k if a_k > 0 else float("inf"),
        "endpoint_rate_holds": bool(rn <= 1.0 / a_k + TOL) if a_k > 0 else False,
    }


def main() -> None:
    rows_silver = [primitivity_row(f"silver_order_{i}", silver_schedule(i)) for i in range(1, 6)]

    n_max = 100
    sched = zldc_anytime_schedule(n_max)
    ends = zldc_concat_endpoints(n_max)
    rows_zldc = [primitivity_row(f"zldc_s_hat_len_{t}", sched[:t]) for t in ends if t <= 40]

    # Negative controls: schedules that must FAIL the primitivity test, so that a
    # universal PASS cannot be an artefact of a test that accepts everything.
    rows_neg = [
        primitivity_row("NEGCTRL_constant_h3_len7", constant_schedule(7, 3.0)),
        primitivity_row("NEGCTRL_silver3_last_step_perturbed", [*silver_schedule(3)[:-1], 9.0]),
    ]
    # Not a negative control: small constant steps ARE primitive (the potential
    # inequality is satisfied for h <= 2).  Recorded separately so the table is not
    # misread as a failed rejection.
    rows_pos_extra = [
        primitivity_row("EXPECTED_PRIMITIVE_constant_h1_len7", constant_schedule(7, 1.0))
    ]

    # Lemma 7: A_{t+1} >= t^{(c+log2 rho)/(c+1)} / 36  for all t
    c = LOG2_RHO
    expo = (c + math.log2(RHO)) / (c + 1.0)
    lemma7 = []
    for t in (1, 2, 5, 10, 20, 40, 60, 99):
        a_t1 = float(sum(sched[:t]))
        bound = (t**expo) / 36.0
        lemma7.append(
            {"t": t, "A_t_plus_1": a_t1, "lemma7_bound": bound, "holds": bool(a_t1 >= bound)}
        )

    report = {
        "exponent_check": {
            "2*log2rho/(1+log2rho)": 2 * LOG2_RHO / (1 + LOG2_RHO),
            "paper_quoted": 1.119,
        },
        "lemma7_exponent_(c+log2rho)/(c+1)": expo,
        "silver_primitivity": rows_silver,
        "zldc_partial_concatenation_primitivity": rows_zldc,
        "negative_controls": rows_neg,
        "expected_primitive_extra": rows_pos_extra,
        "lemma7_aggregate_stepsize": lemma7,
        "verdicts": {
            "all_silver_primitive": all(r["is_primitive"] for r in rows_silver),
            "all_zldc_endpoints_primitive": all(r["is_primitive"] for r in rows_zldc),
            "all_endpoint_rates_hold": all(
                r["endpoint_rate_holds"] for r in rows_silver + rows_zldc
            ),
            "negative_controls_rejected": all(not r["is_primitive"] for r in rows_neg),
            "lemma7_holds": all(r["holds"] for r in lemma7),
        },
    }
    report["RECONSTRUCTION_VERIFIED"] = (
        all(v for k, v in report["verdicts"].items() if k != "negative_controls_rejected")
        and report["verdicts"]["negative_controls_rejected"]
    )

    (OUT / "benchmark_reconstruction.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report["verdicts"], indent=2))
    print("RECONSTRUCTION_VERIFIED:", report["RECONSTRUCTION_VERIFIED"])
    for r in rows_silver + rows_zldc + rows_neg + rows_pos_extra:
        print(
            f"  {r['name']:<28} A_k={r['A_k']:8.3f} lhs_max={r['primitivity_lhs_max']:.6f} "
            f"primitive={r['is_primitive']}  R_n={r['R_n']:.5e} <= 1/A={r['endpoint_rate_holds']}"
        )


if __name__ == "__main__":
    main()
