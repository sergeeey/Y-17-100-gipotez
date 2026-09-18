"""Exact local-minimax stationarity test at ZLDC via a linear program on real gradients.

The skeptic's hand-derived descent direction (skeptic_descent_check.py) was tried and
did NOT improve worst_ratio -- it made it worse. That result alone does not settle
whether ZLDC is a genuine local minimax point: a single failed direction only rules out
that one direction, and a hand-derived finite step is not the same as a first-order
optimality certificate.

The correct test (also proposed by the skeptic, not yet run): use the code's own
analytic gradients (PepCache(..., want_grad=True)) at every horizon, and solve

    min_{d, t}  t
    s.t.        grad_n . d <= t   for all n in 2..24
                -1 <= d_k <= 1    for all k

using log R_n (so the minimax objective is additive in gradients, matching the
project's own _minimax_logratio formulation). If the optimal t < 0 (beyond solver
tolerance), a genuine first-order descent direction exists and ZLDC is NOT a local
minimax stationary point of the log-ratio objective -- full stop, no hand arithmetic.
If t ~= 0, ZLDC is a genuine KKT/Clarke-stationary point for this objective.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from optimizer import PepCache
from pep_core import zldc_anytime_schedule
from scipy.optimize import linprog

K = 24
HORIZONS = list(range(2, K + 1))


def main() -> None:
    cache = PepCache("R")
    zl = np.array(zldc_anytime_schedule(K))

    # d/dh log R_n(h) = grad_R_n(h) / R_n(h), evaluated at h = zl[:n]
    grad_rows = []
    for n in HORIZONS:
        res = cache.value(zl[:n], want_grad=True)
        g_log = np.zeros(K)
        g_log[:n] = res.grad / res.value
        grad_rows.append(g_log)
    G = np.array(grad_rows)  # shape (len(HORIZONS), K)

    n_h = len(HORIZONS)
    # variables: [d_0..d_{K-1}, t], minimize t
    c = np.zeros(K + 1)
    c[-1] = 1.0

    # constraints: G @ d - t <= 0  ->  [G, -1] @ [d;t] <= 0
    A_ub = np.hstack([G, -np.ones((n_h, 1))])
    b_ub = np.zeros(n_h)

    bounds = [(-1.0, 1.0)] * K + [(None, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    print(f"LP status: {res.message}")
    print(f"optimal t (min achievable max-gradient-directional-derivative): {res.fun:.9e}")
    if res.fun < -1e-8:
        print(
            "=> a genuine first-order descent direction EXISTS.\n"
            "   ZLDC is NOT locally minimax-stationary."
        )
        d_star = res.x[:K]
        print(f"   direction (first 8 coords): {d_star[:8]}")
    else:
        print("=> no first-order descent direction exists (within solver tolerance).")
        print("   ZLDC IS a genuine local minimax-stationary point for this objective.")

    out = {
        "lp_status": res.message,
        "optimal_t": float(res.fun),
        "is_locally_stationary": bool(res.fun >= -1e-8),
        "direction": res.x[:K].tolist() if res.fun < -1e-8 else None,
    }
    out_path = Path(__file__).parent / "metrics" / "local_minimax_lp.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"\nwritten to {out_path}")


if __name__ == "__main__":
    main()
