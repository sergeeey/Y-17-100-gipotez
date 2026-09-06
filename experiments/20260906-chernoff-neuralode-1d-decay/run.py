"""run.py — H-B2-1: does the Chernoff-rate theorem (Galkin & Remizov 2021, Theorem 1.2 /
formula (2)) give an informative bound on the empirical error of a 1D linear ResNet/Euler
block approximating dx/dt = -x, compared to the exact analytic solution?

PIPELINE (pure functions):
    block_order1, block_order2, iterate_block, analytic_solution, chernoff_guaranteed_order
EXPERIMENT (verdicts):
    cmd_run

Design pre-registered in claim.md BEFORE running:
  - f(x) = -x, x0 = 1, generator a = -1 (matches the semigroup e^{-t})
  - order-1 block: s1(h) = 1 - h (matches e^{-h} Taylor to order m=1 exactly, remainder O(h^2))
  - order-2 block: s2(h) = 1 - h + h^2/2 (matches e^{-h} Taylor to order m=2 exactly,
    remainder O(h^3))
  - true empirical order estimated via log-log linear regression of |error| vs n, n in a geometric
    range chosen to avoid both under-resolved (too few steps) and floating-point-noise-dominated
    (too many steps, error below ~1e-13) regimes
  - Chernoff-guaranteed order per formula (2): o(1/n^{m-1}) -- i.e. GUARANTEED order is (m-1), a
    number we compare directly against the empirically estimated order
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

X0 = 1.0
A = -1.0  # generator: dx/dt = A*x = -x


def block_order1(h: float) -> float:
    """s1(h) = 1 + A*h -- standard forward-Euler ResNet block. Matches e^{A*h} Taylor to order m=1
    (remainder is O(h^2), i.e. o(h^1)); Chernoff hypothesis check: s1(0)=1, s1'(0)=A. [VERIFIED
    against Theorem 1.2's own hypotheses, claim.md FL Step -4]."""
    return 1.0 + A * h


def block_order2(h: float) -> float:
    """s2(h) = 1 + A*h + (A*h)^2/2 -- a second-order (RK2-like) residual block. Matches e^{A*h}
    Taylor to order m=2 (remainder O(h^3), i.e. o(h^2))."""
    return 1.0 + A * h + (A * h) ** 2 / 2.0


def analytic_solution(t: float, x0: float = X0) -> float:
    return x0 * np.exp(A * t)


def iterate_block(block, t: float, n: int, x0: float = X0) -> float:
    """Apply the block n times with step h=t/n: block(t/n)^n * x0."""
    h = t / n
    return x0 * (block(h) ** n)


def chernoff_guaranteed_order(m: int) -> float:
    """Formula (2), Galkin & Remizov 2021, p.6: s(t/n)^n = e^{ta} + o(1/n^{m-1}). The GUARANTEED
    decay order of the error is therefore (m-1) (e.g. m=1 -> order 0, i.e. no rate at all beyond
    qualitative convergence; m=2 -> order 1)."""
    return float(m - 1)


def empirical_order(block, t: float, n_values: np.ndarray) -> tuple[float, np.ndarray]:
    """Log-log linear regression of |error| vs n over n_values. Returns (estimated order,
    errors). Order is reported as a POSITIVE number (error ~ C / n^order), matching
    chernoff_guaranteed_order's convention, so the two are directly comparable."""
    exact = analytic_solution(t)
    errors = np.array([abs(iterate_block(block, t, int(n)) - exact) for n in n_values])
    log_n = np.log(n_values.astype(float))
    log_err = np.log(errors)
    slope, _intercept = np.polyfit(log_n, log_err, 1)
    return float(-slope), errors


# ───────────────────────────── EXPERIMENT ─────────────────────────────
def cmd_run() -> dict:
    T_VALUES = [1.0, 3.0]
    # n range: large enough to see the asymptotic rate, small enough that float64 rounding (error
    # floor ~1e-15 relative) doesn't yet dominate the m=2 block's much faster-decaying error.
    N_VALUES = np.array([50, 100, 200, 400, 800, 1600, 3200, 6400])

    results = {}
    for T in T_VALUES:
        for label, block, m in (("order1", block_order1, 1), ("order2", block_order2, 2)):
            order_est, errors = empirical_order(block, T, N_VALUES)
            guaranteed = chernoff_guaranteed_order(m)
            results[f"T={T}_{label}"] = {
                "m": m,
                "chernoff_guaranteed_order": guaranteed,
                "empirical_order_estimate": order_est,
                "errors_by_n": {int(n): float(e) for n, e in zip(N_VALUES, errors, strict=True)},
                # "bound_informative": true iff the theorem's guaranteed order is within tolerance
                # of (or better than) the true empirical order -- i.e. the bound is NOT looser than
                # reality by more than the pre-registered MCID tolerance.
                "order_gap_empirical_minus_guaranteed": order_est - guaranteed,
                "bound_informative": (order_est - guaranteed) <= 0.15,
            }

    all_informative = all(r["bound_informative"] for r in results.values())
    verdict = "PASS" if all_informative else "KILLED"

    out = {
        "config": {
            "x0": X0,
            "generator_a": A,
            "n_values": N_VALUES.tolist(),
            "t_values": T_VALUES,
            "mcid_slope_tolerance": 0.15,
        },
        "results": results,
        "all_bounds_informative": all_informative,
        "verdict": verdict,
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
