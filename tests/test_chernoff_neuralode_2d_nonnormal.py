"""Unit tests for H-B2-1c (non-normal matrix generalization). Written BEFORE trusting the
comparison, same discipline as H-B2-1/H-B2-1b.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-chernoff-neuralode-2d-nonnormal"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_nn_run", _HERE / "run.py")
nn = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(nn)


def test_a_is_genuinely_non_normal():
    assert not nn.is_normal(nn.A)


def test_a_has_the_claimed_eigenvalues():
    eigvals = np.sort(np.linalg.eigvals(nn.A).real)
    assert np.allclose(eigvals, [-2.0, -1.0])


def test_zero_coupling_would_be_normal():
    diag_only = np.array([[-1.0, 0.0], [0.0, -2.0]])
    assert nn.is_normal(diag_only)


def test_analytic_solution_at_zero_is_x0():
    assert np.allclose(nn.analytic_solution(0.0), nn.X0)


def test_transient_growth_is_measurable():
    """The whole point of this experiment: M1 should exceed 1, evidencing real transient growth
    (if it doesn't, C=10 isn't inducing the phenomenon this test is designed to probe)."""
    m1 = nn.measure_m1(1.0)
    assert m1 > 1.5, f"M1={m1}: expected measurable transient growth for C={nn.C}, got too little"


def test_positive_control_convergence():
    t = 1.0
    exact = nn.analytic_solution(t)
    err_small_n = np.linalg.norm(nn.iterate_block(nn.block_order1, t, 10) - exact)
    err_large_n = np.linalg.norm(nn.iterate_block(nn.block_order1, t, 20000) - exact)
    assert err_large_n < err_small_n
    assert err_large_n < 1e-2


def test_negative_control_wrong_sign_matrix_does_not_converge():
    def wrong_block(h):
        return np.eye(2) + h * (-nn.A)

    t = 1.0
    exact_decay = nn.analytic_solution(t)
    result = nn.iterate_block(wrong_block, t, 10000)
    assert np.linalg.norm(result - exact_decay) > 1.0


def test_empirical_order_recovers_known_rates():
    n_values = np.array([400, 800, 1600, 3200, 6400])
    order1_est, _ = nn.empirical_order(nn.block_order1, 1.0, n_values)
    order2_est, _ = nn.empirical_order(nn.block_order2, 1.0, n_values)
    assert 0.8 < order1_est < 1.2, f"order-1 empirical order {order1_est} not near 1"
    assert order2_est > order1_est + 0.4, "order-2 should decay meaningfully faster"
