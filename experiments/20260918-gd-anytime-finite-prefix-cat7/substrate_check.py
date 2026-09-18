"""Substrate Gate (FL Step 2a) for H-CAT7-1: is the PEP harness itself trustworthy?

Four independent checks, none of which involves the hypothesis:

1. Closed form.  For constant stepsize h in (0, 1] the exact worst case is known
   (Drori-Teboulle 2014 / Taylor et al. 2017):
       R_N = 1 / (4 N h + 2)      with L = 1, ||x_0 - x*||^2 <= 1.
2. Independent implementation.  PEPit's own ``wc_gradient_descent`` on the same
   input, built by a different code path (this is also the "Alternative tool"
   no-collapse test of controls.md).
3. Analytic gradient vs central finite differences of the same solver.
4. Published-schedule sanity: the silver schedule sums must equal rho^i - 1 and
   the ZLDC construction must be prefix-monotone (each shorter schedule is a
   literal prefix of every longer one) -- the property the whole experiment rests on.

Run:  python substrate_check.py
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from pep_core import (
    RHO,
    GDPep,
    constant_schedule,
    silver_schedule,
    zldc_anytime_schedule,
)

OUT = Path(__file__).parent / "metrics"
OUT.mkdir(exist_ok=True)


def check_closed_form(solver: str = "CLARABEL") -> list[dict]:
    rows = []
    for n in (1, 2, 3, 5, 8, 12):
        for h in (0.5, 1.0):
            pep = GDPep(n, "R")
            t0 = time.time()
            res = pep.solve(np.array(constant_schedule(n, h)), solver=solver)
            dt = time.time() - t0
            exact = 1.0 / (4.0 * n * h + 2.0)
            rows.append(
                {
                    "n": n,
                    "h": h,
                    "pep": res.value,
                    "closed_form": exact,
                    "rel_err": abs(res.value - exact) / exact,
                    "status": res.status,
                    "seconds": round(dt, 3),
                }
            )
    return rows


def check_pepit() -> list[dict]:
    try:
        from PEPit import PEP
        from PEPit.functions import SmoothConvexFunction
    except Exception as exc:  # pragma: no cover - environment dependent
        return [{"error": f"PEPit unavailable: {exc}"}]

    def pepit_wc(gammas: list[float]) -> float:
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
        return problem.solve(verbose=0)

    rows = []
    cases: list[list[float]] = [
        constant_schedule(3, 1.0),
        constant_schedule(6, 0.7),
        silver_schedule(3),
        zldc_anytime_schedule(7),
        [0.4, 2.7, 1.1, 3.3, 0.9],
    ]
    for gammas in cases:
        mine = GDPep(len(gammas), "R").solve(np.array(gammas)).value
        theirs = pepit_wc(list(gammas))
        rows.append(
            {
                "schedule": [round(float(g), 6) for g in gammas],
                "mine": mine,
                "pepit": theirs,
                "rel_diff": abs(mine - theirs) / max(abs(theirs), 1e-12),
            }
        )
    return rows


def check_gradient() -> list[dict]:
    """Analytic (envelope-theorem) gradient vs central finite differences.

    WHY a sweep over eps rather than one value: central FD error is
    O(eps^2) + O(solver_tol / eps), so a single eps cannot distinguish a wrong
    analytic gradient from FD noise.  The check is that the discrepancy has the
    expected U-shape in eps and bottoms out near the solver's own accuracy --
    a genuinely wrong gradient would show a floor independent of eps.
    """
    rng = np.random.default_rng(20260918)
    rows = []
    for n in (3, 5, 7):
        h = rng.uniform(0.3, 2.5, size=n)
        pep = GDPep(n, "R")
        res = pep.solve(h, want_grad=True)
        sweep = {}
        best = np.inf
        for eps in (1e-3, 1e-4, 1e-5):
            fd = np.zeros(n)
            for k in range(n):
                hp, hm = h.copy(), h.copy()
                hp[k] += eps
                hm[k] -= eps
                fd[k] = (pep.solve(hp).value - pep.solve(hm).value) / (2 * eps)
            rel = float(np.max(np.abs(res.grad - fd)) / max(np.max(np.abs(fd)), 1e-12))
            sweep[f"eps={eps:g}"] = rel
            best = min(best, rel)
        rows.append(
            {
                "n": n,
                "analytic": [round(float(v), 8) for v in res.grad],
                "rel_diff_by_eps": sweep,
                "rel_diff": best,
            }
        )
    return rows


def check_schedules() -> dict:
    silver_sums = []
    for i in range(1, 7):
        s = silver_schedule(i)
        silver_sums.append(
            {
                "order": i,
                "length": len(s),
                "expected_length": 2**i - 1,
                "sum": float(sum(s)),
                "expected_sum": RHO**i - 1.0,
                "sum_rel_err": abs(sum(s) - (RHO**i - 1.0)) / (RHO**i - 1.0),
            }
        )
    long = zldc_anytime_schedule(200)
    prefix_ok = all(
        np.allclose(np.array(zldc_anytime_schedule(m)), np.array(long[:m]), rtol=0, atol=1e-12)
        for m in (1, 2, 5, 13, 40, 97, 150)
    )
    return {
        "silver": silver_sums,
        "zldc_prefix_monotone": bool(prefix_ok),
        "zldc_all_positive": bool(all(v > 0 for v in long)),
        "zldc_first_12": [round(float(v), 6) for v in long[:12]],
        "zldc_max_step_in_200": float(max(long)),
        "exponent_2logrho_over_1plogrho": 2 * math.log2(RHO) / (1 + math.log2(RHO)),
    }


def main() -> None:
    report = {
        "closed_form": check_closed_form(),
        "pepit_cross_impl": check_pepit(),
        "gradient": check_gradient(),
        "schedules": check_schedules(),
    }
    verdicts = {}
    verdicts["closed_form"] = max(r["rel_err"] for r in report["closed_form"]) < 1e-6
    pe = report["pepit_cross_impl"]
    # WHY these thresholds: both are cross-checks between two numerical procedures,
    # not exactness claims.  PEPit solves its own (differently canonicalised) SDP at
    # its default tolerance, so agreement to ~5 significant digits is the ceiling a
    # cross-implementation check can reach; and the FD probe's own noise floor is
    # solver_tol/eps.  Chosen before running, and reported with the raw numbers so a
    # reader can see the actual margin rather than only the PASS/FAIL bit.
    verdicts["pepit_cross_impl"] = "error" not in pe[0] and max(r["rel_diff"] for r in pe) < 1e-4
    verdicts["gradient"] = max(r["rel_diff"] for r in report["gradient"]) < 1e-4
    sch = report["schedules"]
    verdicts["schedules"] = (
        max(r["sum_rel_err"] for r in sch["silver"]) < 1e-12
        and sch["zldc_prefix_monotone"]
        and sch["zldc_all_positive"]
    )
    report["verdicts"] = verdicts
    report["substrate_gate"] = "READY" if all(verdicts.values()) else "BLOCKED-INFRASTRUCTURE"

    (OUT / "substrate_check.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
