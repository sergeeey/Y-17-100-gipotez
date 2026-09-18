"""Outer search over stepsizes, with the PEP used only as an inner evaluator.

ARCHITECTURE NOTE (load-bearing, not incidental).  The stepsizes are never SDP
variables.  Making ``eta_k`` a variable inside the same PEP would multiply an
unknown stepsize by an unknown gradient, i.e. introduce bilinear terms and
destroy convexity of the relaxation -- the resulting number would not be a
worst case at all.  So: the PEP (``pep_core.GDPep``) takes a *fixed numeric*
schedule and returns the exact worst case; all search over schedules happens in
this module, in an ordinary non-convex optimiser on top of that evaluator.

Two search modes:

* ``optimize_per_horizon`` -- one free schedule per horizon, no coupling.  This
  is the ALREADY-PUBLISHED setting (Das Gupta et al.), used here only as the
  positive control and as the object of the adversarial prefix check.
* ``optimize_prefix_consistent`` -- ONE master schedule; horizon ``N`` is scored
  on ``master[:N]``.  Different horizons cannot receive different schedules
  because there is only one array; the constraint is structural, not a
  convention that could be violated by accident.
"""

from __future__ import annotations

import numpy as np
from pep_core import GDPep
from scipy.optimize import minimize

H_MIN = 1e-3
H_MAX = 60.0


class PepCache:
    """One GDPep instance per (n, objective); construction is not free."""

    def __init__(self, objective: str = "R"):
        self.objective = objective
        self._peps: dict[int, GDPep] = {}
        self.n_solves = 0

    def pep(self, n: int) -> GDPep:
        if n not in self._peps:
            self._peps[n] = GDPep(n, self.objective)
        return self._peps[n]

    def value(self, h: np.ndarray, want_grad: bool = False):
        self.n_solves += 1
        return self.pep(len(h)).solve(np.asarray(h, dtype=float), want_grad=want_grad)


def optimize_per_horizon(
    n: int,
    cache: PepCache,
    starts: list[np.ndarray],
    maxiter: int = 300,
) -> dict:
    """Minimise log R_n over a FREE schedule of length n (no prefix coupling)."""

    def fun(h: np.ndarray):
        res = cache.value(h, want_grad=True)
        if not np.isfinite(res.value) or res.value <= 0:
            return 1e6, np.zeros_like(h)
        return float(np.log(res.value)), res.grad / res.value

    best = None
    for s in starts:
        x0 = np.clip(np.asarray(s, dtype=float), H_MIN, H_MAX)
        out = minimize(
            fun,
            x0,
            jac=True,
            method="L-BFGS-B",
            bounds=[(H_MIN, H_MAX)] * n,
            options={"maxiter": maxiter, "ftol": 1e-14, "gtol": 1e-10},
        )
        val = float(np.exp(out.fun))
        if best is None or val < best["value"]:
            best = {
                "value": val,
                "schedule": np.clip(out.x, H_MIN, H_MAX).tolist(),
                "nit": int(out.nit),
                "message": str(out.message),
            }
    assert best is not None
    return best


def _minimax_logratio(
    master: np.ndarray,
    horizons: list[int],
    baselines: dict[int, float],
    cache: PepCache,
    beta: float,
) -> tuple[float, np.ndarray]:
    """Smoothed max over horizons of log(R_N(master[:N]) / baseline_N).

    log-sum-exp smoothing with parameter ``beta``: as beta grows this converges
    to the true max, which is what the pre-registered "at EVERY n" PASS rule
    needs.  The reported PASS/FAIL is always computed from the exact per-horizon
    ratios, never from this smoothed surrogate.
    """
    logs = []
    grads = []
    for n in horizons:
        res = cache.value(master[:n], want_grad=True)
        if not np.isfinite(res.value) or res.value <= 0:
            return 1e6, np.zeros_like(master)
        logs.append(np.log(res.value) - np.log(baselines[n]))
        g = np.zeros_like(master)
        g[:n] = res.grad / res.value
        grads.append(g)
    logs_arr = np.array(logs)
    m = float(np.max(logs_arr))
    w = np.exp(beta * (logs_arr - m))
    w = w / w.sum()
    val = m + float(np.log(np.sum(np.exp(beta * (logs_arr - m)))) / beta)
    grad = np.einsum("i,ij->j", w, np.array(grads))
    return val, grad


def optimize_prefix_consistent(
    horizons: list[int],
    baselines: dict[int, float],
    cache: PepCache,
    starts: list[np.ndarray],
    betas: tuple[float, ...] = (20.0, 80.0, 300.0),
    maxiter: int = 200,
) -> dict:
    """Minimise the worst-over-horizons ratio to the baseline, ONE master schedule."""
    k = max(horizons)
    best = None
    for s in starts:
        x = np.clip(np.asarray(s, dtype=float)[:k].copy(), H_MIN, H_MAX)
        if x.size < k:  # pad short starts with the last value
            x = np.concatenate([x, np.full(k - x.size, x[-1] if x.size else 1.0)])
        for beta in betas:
            out = minimize(
                lambda h, b=beta: _minimax_logratio(h, horizons, baselines, cache, b),
                x,
                jac=True,
                method="L-BFGS-B",
                bounds=[(H_MIN, H_MAX)] * k,
                options={"maxiter": maxiter, "ftol": 1e-14, "gtol": 1e-10},
            )
            x = np.clip(out.x, H_MIN, H_MAX)
        ratios = {n: float(cache.value(x[:n]).value / baselines[n]) for n in horizons}
        worst = max(ratios.values())
        if best is None or worst < best["worst_ratio"]:
            best = {
                "worst_ratio": worst,
                "train_ratios": ratios,
                "master": x.tolist(),
            }
    assert best is not None
    return best


def fit_power_law(ns: list[int], vals: list[float], offset: int = 0) -> dict:
    """Least-squares fit of log(val) = a + b log(n + offset); returns b and its SE."""
    x = np.log(np.array(ns, dtype=float) + offset)
    y = np.log(np.array(vals, dtype=float))
    amat = np.vstack([np.ones_like(x), x]).T
    coef, _res, _, _ = np.linalg.lstsq(amat, y, rcond=None)
    pred = amat @ coef
    dof = max(len(x) - 2, 1)
    sigma2 = float(np.sum((y - pred) ** 2) / dof)
    cov = sigma2 * np.linalg.inv(amat.T @ amat)
    return {
        "exponent": float(coef[1]),
        "stderr": float(np.sqrt(cov[1, 1])),
        "intercept": float(coef[0]),
        "r2": float(1 - np.sum((y - pred) ** 2) / max(np.sum((y - y.mean()) ** 2), 1e-30)),
    }
