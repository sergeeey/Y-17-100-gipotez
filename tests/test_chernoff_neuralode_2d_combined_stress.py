"""Unit tests for H-B2-1e (combined non-normal + mixed-sign stress test). Written BEFORE
trusting the comparison, same discipline as the rest of the H-B2-1* family.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-chernoff-neuralode-2d-combined-stress"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_combined_run", _HERE / "run.py")
combined = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(combined)


def test_a_is_genuinely_non_normal():
    assert not combined.is_normal(combined.A)


def test_a_has_mixed_sign_eigenvalues():
    eigvals = np.sort(np.linalg.eigvals(combined.A).real)
    assert np.allclose(eigvals, [-2.0, 0.5])


def test_analytic_solution_at_zero_is_x0():
    assert np.allclose(combined.analytic_solution(0.0), combined.X0)


def test_transient_effect_is_measurable():
    """M1 should exceed the naive eigenvalue-only prediction (e^{0.5*1}=1.65 at t=1, so M1
    ratio relative to that baseline > 1 indicates real combined transient+growth effect)."""
    m1 = combined.measure_m1_with_w(1.0, combined.W)
    assert m1 > 1.0, f"M1={m1}: expected measurable combined effect beyond pure eigenvalue growth"


def test_positive_control_convergence():
    t = 1.0
    exact = combined.analytic_solution(t)
    err_small_n = np.linalg.norm(combined.iterate_block(combined.block_order1, t, 10) - exact)
    err_large_n = np.linalg.norm(combined.iterate_block(combined.block_order1, t, 20000) - exact)
    assert err_large_n < err_small_n
    assert err_large_n < 1e-1


def test_negative_control_flipped_sign_diverges():
    def wrong_block(h):
        return np.eye(2) + h * (-combined.A)

    t = 1.0
    exact = combined.analytic_solution(t)
    result = combined.iterate_block(wrong_block, t, 10000)
    assert np.linalg.norm(result - exact) > 1.0


def test_empirical_order_recovers_known_rates():
    n_values = np.array([800, 1600, 3200, 6400])
    order1_est, _ = combined.empirical_order(combined.block_order1, 1.0, n_values)
    order2_est, _ = combined.empirical_order(combined.block_order2, 1.0, n_values)
    assert 0.7 < order1_est < 1.3, f"order-1 empirical order {order1_est} not near 1"
    assert order2_est > order1_est + 0.3, "order-2 should decay meaningfully faster"
