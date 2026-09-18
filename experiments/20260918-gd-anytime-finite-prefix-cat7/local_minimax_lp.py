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
project's own _minimax_logratio formulation).

CAVEAT, found by a reviewer pass and confirmed by direct finite-difference measurement
(see verify_lp_direction.py's follow-up and decision.md's Addendum): this LP's t<0/t~=0
dichotomy is a valid first-order test ONLY where every R_n is differentiable at h=zl[:n].
At ZLDC specifically, 5 of 23 horizons (n=3,9,13,17,21) are measured to have a genuine
kink (one-sided derivatives D+(d) and D-(d) both positive, i.e. NOT opposite in sign) --
the envelope-theorem gradient PepCache returns is one arbitrary element of a non-trivial
subdifferential at those horizons, not a true gradient. At a kink, "t<0" does NOT imply a
genuine descent direction exists (confirmed: the direction found here failed on direct
execution in both signs, see verify_lp_direction.py), and "t~=0" would not imply
stationarity either -- the correct first-order test at a kink needs the convex hull of
the FULL subdifferential at each kinked horizon, not one arbitrary dual solution's
gradient. Treat this script's own printed conclusion and its JSON output's
"is_locally_stationary" field as informative only when no kink is present at the
candidate point -- check with a D+/D- one-sided-derivative probe first.
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
    d_star = res.x[:K]

    # Smoothness pre-check (added after a reviewer pass + FD measurement found this
    # missing): probe D+(d)+D-(d) at each horizon along the found direction. Nonzero
    # sum means that horizon's R_n is kinked along d, and the LP's dichotomy below is
    # not a valid first-order test there.
    eps = 1e-5
    kinked_horizons = []
    for n in HORIZONS:
        base_val = float(cache.value(zl[:n]).value)
        plus = float(cache.value(zl[:n] + eps * d_star[:n]).value)
        minus = float(cache.value(zl[:n] - eps * d_star[:n]).value)
        d_plus = (np.log(plus) - np.log(base_val)) / eps
        d_minus = (np.log(base_val) - np.log(minus)) / eps
        if abs(d_plus + (-d_minus)) > 0.5 * max(abs(d_plus), abs(-d_minus), 1e-9):
            kinked_horizons.append(n)

    print(f"LP status: {res.message}")
    print(f"optimal t (min achievable max-gradient-directional-derivative): {res.fun:.9e}")
    print(f"smoothness pre-check along found direction -- kinked horizons: {kinked_horizons}")

    if kinked_horizons:
        print(
            "=> SMOOTHNESS PRECONDITION FAILS at the horizons above. The t<0/t~=0\n"
            "   dichotomy below is NOT a valid first-order test at this point -- do\n"
            "   NOT read either branch as a settled local-optimality verdict."
        )
    if res.fun < -1e-8:
        print(
            "   (raw LP result: a direction with negative max-directional-derivative\n"
            "   was found; only a genuine descent direction if no horizon above is kinked)"
        )
        print(f"   direction (first 8 coords): {d_star[:8]}")
    else:
        print(
            "   (raw LP result: no negative-max-directional-derivative direction found;\n"
            "   only implies stationarity if no horizon above is kinked)"
        )

    out = {
        "lp_status": res.message,
        "optimal_t": float(res.fun),
        "kinked_horizons": kinked_horizons,
        "is_locally_stationary": (bool(res.fun >= -1e-8) if not kinked_horizons else None),
        "direction": d_star.tolist() if res.fun < -1e-8 else None,
        "note": (
            "is_locally_stationary is None when kinked_horizons is non-empty: the "
            "first-order LP test is invalid at a kink and neither branch of the "
            "dichotomy may be read as a verdict there."
        ),
    }
    out_path = Path(__file__).parent / "metrics" / "local_minimax_lp.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"\nwritten to {out_path}")


if __name__ == "__main__":
    main()
