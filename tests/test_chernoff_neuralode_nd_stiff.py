"""Unit tests for H-B2-1f (N=8 dimensional scale-up). Written BEFORE trusting the comparison,
same discipline as the rest of the H-B2-1* family.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-chernoff-neuralode-nd-stiff"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_nd_run", _HERE / "run.py")
nd = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(nd)


def test_dimension_is_8():
    assert nd.N_DIM == 8
    assert nd.A.shape == (8, 8)


def test_a_is_genuinely_non_normal():
    assert not nd.is_normal(nd.A)


def test_a_has_the_claimed_eigenvalues_on_diagonal():
    # Upper-triangular -- eigenvalues are exactly the diagonal entries.
    eigvals = np.sort(np.linalg.eigvals(nd.A).real)
    assert np.allclose(eigvals, np.sort(nd.EIGENVALUES))


def test_analytic_solution_at_zero_is_x0():
    assert np.allclose(nd.analytic_solution(0.0), nd.X0)


def test_positive_control_convergence():
    t = 1.0
    exact = nd.analytic_solution(t)
    err_small_n = np.linalg.norm(nd.iterate_block(nd.block_order1, t, 10) - exact)
    err_large_n = np.linalg.norm(nd.iterate_block(nd.block_order1, t, 20000) - exact)
    assert err_large_n < err_small_n


def test_negative_control_flipped_sign_diverges():
    def wrong_block(h):
        return np.eye(nd.N_DIM) + h * (-nd.A)

    t = 1.0
    exact = nd.analytic_solution(t)
    result = nd.iterate_block(wrong_block, t, 10000)
    assert np.linalg.norm(result - exact) > 1.0


def test_empirical_order_recovers_known_rates():
    n_values = np.array([800, 1600, 3200, 6400])
    order1_est, _ = nd.empirical_order(nd.block_order1, 1.0, n_values)
    order2_est, _ = nd.empirical_order(nd.block_order2, 1.0, n_values)
    assert 0.6 < order1_est < 1.4, f"order-1 empirical order {order1_est} not near 1"
    assert order2_est > order1_est, "order-2 should decay faster than order-1"
