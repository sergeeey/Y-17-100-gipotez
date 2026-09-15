"""Negative / injected-error control for rba_decomposition_test.py.

The two mandatory identities (bulk, delta-I) are the only things standing between
"the decomposition was computed correctly" and "a plausible-looking number".  A
check that cannot FAIL is not a check, so this script deliberately plants five
errors of exactly the kind that would otherwise pass silently, and records
whether each gate fires.

  E1 off-by-one in the orbit index used for cos(2 pi j k / n)   -> bulk gate
  E2 p normalised by 1 instead of (1-w_0)                       -> bulk gate
  E3 tau replaced by w_0 (missing the 1/(1-w_0))                -> bulk gate
  E4 wrong prefactor (q instead of q+1) in the delta-I identity -> delta-I gate
  E5 u_j computed as p_child (embedding forgotten)              -> delta-I gate

A planted error is CAUGHT if the corresponding identity error exceeds 1e-9
(the report's own stated target).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rba_decomposition_test as R

HERE = Path(__file__).resolve().parent
TOL = 1e-9


def one_case(n, seed, method="highs-ipm"):
    m = (n - 1) // 2
    q = m // 2
    F = m - q
    rng = np.random.default_rng(seed)
    lp = R.ReducedLP(n, method=method)
    S = np.sort(rng.choice(np.arange(1, m + 1), size=q, replace=False))
    w, _st, _, _, _ = lp.solve(S)
    p, w0 = R.p_from_w(w)
    supp = np.nonzero(p)[0]
    pk = p[supp]
    s2 = float(pk @ pk)
    I_S = q * s2
    tau = w0 / (1.0 - w0)
    free = np.setdiff1d(np.arange(1, m + 1), S)

    def bulk_err(orbit, pvec, tau_):
        C = lp.cosval[np.outer(free, orbit) % n]
        mj = C @ pvec
        Aj = (C @ (pvec * pvec)) - mj * float(pvec @ pvec)
        obs = float(((tau_ + mj) * Aj).mean())
        pred = (n / (4.0 * F)) * (float((pvec ** 3).sum()) - float(pvec @ pvec) ** 2)
        return abs(obs - pred)

    out = {"n": n, "seed": seed}
    out["baseline_bulk_err"] = bulk_err(supp + 1, pk, tau)
    out["E1_offbyone_orbit"] = bulk_err(supp, pk, tau)                 # orbit index off by one
    raw = p[supp] * (1.0 - w0)
    out["E2_missing_normalisation"] = bulk_err(supp + 1, raw, tau)     # p not normalised
    out["E3_tau_as_w0"] = bulk_err(supp + 1, pk, float(w0))            # tau mis-defined

    # delta-I identity, baseline and two planted errors
    j = int(rng.choice(free))
    wc, _, _, _, _ = lp.solve(np.sort(np.append(S, j)))
    pc, _ = R.p_from_w(wc)
    u = pc - p
    ip = float(p @ u)
    un = float(u @ u)
    I_child = (q + 1) * float(pc @ pc)
    out["baseline_deltaI_err"] = abs((I_child - I_S) - (I_S / q + 2 * (q + 1) * ip + (q + 1) * un))
    out["E4_wrong_prefactor_q"] = abs((I_child - I_S) - (I_S / q + 2 * q * ip + q * un))
    ip_b, un_b = float(p @ pc), float(pc @ pc)
    out["E5_u_not_differenced"] = abs(
        (I_child - I_S) - (I_S / q + 2 * (q + 1) * ip_b + (q + 1) * un_b)
    )
    return out


def main():
    rows = [one_case(n, 90210 + n) for n in (127, 251, 509, 1021)]
    verdict = {}
    for k in ("E1_offbyone_orbit", "E2_missing_normalisation", "E3_tau_as_w0",
              "E4_wrong_prefactor_q", "E5_u_not_differenced"):
        verdict[k] = {"caught_in": sum(1 for r in rows if r[k] > TOL), "of": len(rows),
                      "min_planted_error": min(r[k] for r in rows)}
    base = {"max_baseline_bulk_err": max(r["baseline_bulk_err"] for r in rows),
            "max_baseline_deltaI_err": max(r["baseline_deltaI_err"] for r in rows)}
    out = {"tolerance": TOL, "cases": rows, "planted_error_detection": verdict,
           "baseline": base,
           "all_caught": all(v["caught_in"] == v["of"] for v in verdict.values()),
           "baseline_clean": base["max_baseline_bulk_err"] < TOL
                             and base["max_baseline_deltaI_err"] < TOL}
    (HERE / "metrics").mkdir(exist_ok=True)
    (HERE / "metrics" / "rba_negative_control.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
