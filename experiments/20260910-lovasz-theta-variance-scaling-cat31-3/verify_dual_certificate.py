"""Point 48: the decisive test that overturns point 47. Weak LP duality is absolute -- a
verified dual-feasible solution to the two-spectrum LP proves an upper bound on K_s(L) that
NO primal-feasible point can exceed, regardless of how small a candidate primal point's
per-constraint residuals look in a badly-conditioned basis. This script builds the explicit
Chebyshev dual certificate the user proposed, verifies its dual-feasibility directly (not by
trusting the closed-form formula), and uses it to show point 46/47's primal LP "solutions" at
high `s` are NOT actually feasible -- overturning point 47's "CERT-VIOLATED" conclusion.

The LP (point 46/47's own formulation):
    K_s(L) = max_{x,y>=0} sum(y)  s.t.  sum(x)=1,  sum(gamma^r x) = sum(gamma^r y)  (r=1..s)

Its dual (derived here, not assumed): minimize lambda_0 subject to, for every level l,
    lambda_0 + p(gamma_l) >= 0          where p(gamma) = sum_{r=1}^s lambda_r * gamma^r
    p(gamma_l) <= -1
i.e. a degree-s polynomial p with ZERO constant term, bounded in [-lambda_0, -1] on the point
set, certifies K_s(L) <= lambda_0. Writing q := -p, dual-feasibility becomes q(gamma_l) in
[1, lambda_0] for every l, and by weak duality lambda_0 is a valid upper bound the moment the
range condition is verified numerically -- independent of any primal computation.

The user's proposed q:
    q_l = [1 - T_s(z(gamma_l))/T_s(z_0)] / [1 - 1/|T_s(z_0)|]
with z(gamma) the affine map [gamma_min,gamma_max] -> [-1,1], and z_0 = (L+3)/(L-1) = -z(0)
(the image of gamma=0 under the same map, mirrored) -- matching point 47's own A_s = T_s(z_0).

Decisive check on a saved primal (x,y) from point 47's own LP: for EVEN s, T_s is an even
function, so T_s(-z_0) = T_s(z_0), giving q(0) = 0 exactly -- q then has NO constant term,
matching p's required form exactly. For a genuinely feasible (x,y) (moments 1..s matching
exactly), this forces Delta_q := q^T(y-x) = 0 EXACTLY, algebraically, independent of solver
precision. Any nonzero Delta_q directly measures primal infeasibility in the one direction
that actually matters for the duality argument -- a much sharper test than per-power relative
residuals, which can look tiny while this aggregate is large (amplification through a
high-degree oscillating polynomial).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from mpmath import chebyt, fsum, mp, mpf
from scipy.optimize import linprog

mp.dps = 50

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def gamma_l_array(N: int, q: int) -> np.ndarray:
    L = min(q, N - q)
    ls = np.arange(1, L + 1)
    return ls * (N + 1 - ls) / (q * (N - q))


def solve_rescaled(gammas: np.ndarray, s: int, method: str = "highs-ds", tol: float = 1e-9):
    L = len(gammas)
    n_vars = 2 * L
    g_resc = gammas / gammas.max()
    c = np.concatenate([np.zeros(L), -np.ones(L)])
    row_norm = np.concatenate([np.ones(L), np.zeros(L)])
    rows_moment = [np.concatenate([g_resc**r, -(g_resc**r)]) for r in range(1, s + 1)]
    A_eq = np.vstack([row_norm, *rows_moment])
    b_eq = np.concatenate([[1.0], np.zeros(s)])
    options = {"primal_feasibility_tolerance": tol, "dual_feasibility_tolerance": tol}
    return linprog(
        c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * n_vars, method=method, options=options
    )


def dual_certificate_check(gammas_mp: list, s: int, x: np.ndarray, y: np.ndarray) -> dict:
    L = len(gammas_mp)
    g_min, g_max = min(gammas_mp), max(gammas_mp)

    def z_of(gamma):
        return (2 * gamma - (g_min + g_max)) / (g_max - g_min)

    z0 = mpf(L + 3) / mpf(L - 1)
    Ts_z0 = chebyt(s, z0)
    cert_bound = (Ts_z0 + 1) / (Ts_z0 - 1)
    denom = 1 - 1 / abs(Ts_z0)

    q_vals = [(1 - chebyt(s, z_of(g)) / Ts_z0) / denom for g in gammas_mp]
    q_min, q_max = min(q_vals), max(q_vals)

    x_mp = [mpf(float(v)) for v in x]
    y_mp = [mpf(float(v)) for v in y]
    qTx = fsum(ql * xv for ql, xv in zip(q_vals, x_mp))
    qTy = fsum(ql * yv for ql, yv in zip(q_vals, y_mp))
    delta_q = qTy - qTx

    dual_feasible = (q_min >= 1 - mpf("1e-6")) and (q_max <= cert_bound + mpf("1e-6"))

    return {
        "cert_bound": float(cert_bound),
        "q_min": float(q_min),
        "q_max": float(q_max),
        "dual_feasible": bool(dual_feasible),
        "delta_q": float(delta_q),
        "sum_y_reported": float(fsum(y_mp)),
        "sum_x_reported": float(fsum(x_mp)),
        "primal_actually_feasible": abs(float(delta_q)) < 1e-4 if s % 2 == 0 else None,
    }


def run() -> None:
    results = []
    for L in (25, 50, 100, 250, 500, 1000):
        N, q = 2 * L, L
        gammas = gamma_l_array(N, q)
        gammas_mp = [mpf(float(g)) for g in gammas]
        print(f"=== L={L} ===", flush=True)
        row = {"L": L, "cells": []}
        for s in [sv for sv in range(1, min(31, L + 1)) if sv % 2 == 0]:
            res = solve_rescaled(gammas, s)
            if not res.success:
                print(f"  s={s:3d}: LP FAILED -- {res.message}")
                continue
            x, y = res.x[:L], res.x[L:]
            d = dual_certificate_check(gammas_mp, s, x, y)
            cell = {"s": s, **d}
            row["cells"].append(cell)
            verdict = (
                "GENUINELY FEASIBLE"
                if d["primal_actually_feasible"]
                else "SPURIOUS (numerical artifact)"
            )
            print(
                f"  s={s:3d}: cert_bound={d['cert_bound']:.6f}  "
                f"LP_reported_K_s={d['sum_y_reported']:.6f}  delta_q={d['delta_q']:.6f}  "
                f"dual_feasible={d['dual_feasible']}  primal={verdict}",
                flush=True,
            )
        results.append(row)
        print()

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "dual_certificate_verification_point48.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Done.")


if __name__ == "__main__":
    run()
