"""Unit tests for H-B2-1b (2D matrix generalization of H-B2-1). Written BEFORE trusting the
comparison, same discipline as H-B2-1's own tests.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-chernoff-neuralode-2d-matrix"
)
_SPEC = importlib.util.spec_from_file_location("chernoff2d_run", _HERE / "run.py")
c2d = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(c2d)


def test_rotation_matrix_is_orthogonal():
    assert np.allclose(c2d.P @ c2d.P.T, np.eye(2))


def test_a_has_the_claimed_eigenvalues():
    eigvals = np.sort(np.linalg.eigvalsh(c2d.A))
    assert np.allclose(eigvals, np.sort(c2d.EIGENVALUES))


def test_a_is_symmetric_and_genuinely_off_diagonal():
    assert np.allclose(c2d.A, c2d.A.T)
    assert abs(c2d.A[0, 1]) > 1e-6  # not accidentally diagonal in the standard basis


def test_analytic_solution_at_zero_is_x0():
    assert np.allclose(c2d.analytic_solution(0.0), c2d.X0)


def test_positive_control_convergence():
    t = 1.0
    exact = c2d.analytic_solution(t)
    err_small_n = np.linalg.norm(c2d.iterate_block(c2d.block_order1, t, 10) - exact)
    err_large_n = np.linalg.norm(c2d.iterate_block(c2d.block_order1, t, 10000) - exact)
    assert err_large_n < err_small_n
    assert err_large_n < 1e-3


def test_negative_control_wrong_sign_matrix_does_not_converge():
    def wrong_block(h):
        return np.eye(2) + h * (-c2d.A)  # flips both eigenvalues to growth

    t = 1.0
    exact_decay = c2d.analytic_solution(t)
    result = c2d.iterate_block(wrong_block, t, 10000)
    assert np.linalg.norm(result - exact_decay) > 1.0


def test_m2_condition_detects_fast_eigenvalue_violation():
    # h=t/n large enough that the FAST eigenvalue (-2) pushes |1+lambda*h| past 1 while the slow
    # one (-1) might not yet -- this is exactly the scenario the matrix case can reveal that the
    # 1D test (single eigenvalue) cannot.
    assert not c2d.m2_condition_holds_both_eigenvalues(c2d.block_order1_scalar, 3.0, 1)  # h=3
    assert c2d.m2_condition_holds_both_eigenvalues(c2d.block_order1_scalar, 1.0, 100)  # h=0.01


def test_empirical_order_recovers_known_rates_in_2d():
    n_values = np.array([200, 400, 800, 1600, 3200, 6400])
    order1_est, _ = c2d.empirical_order(c2d.block_order1, 1.0, n_values)
    order2_est, _ = c2d.empirical_order(c2d.block_order2, 1.0, n_values)
    assert 0.85 < order1_est < 1.15, f"order-1 2D block empirical order {order1_est} not near 1"
    assert order2_est > order1_est + 0.5, "order-2 2D block should decay meaningfully faster"
