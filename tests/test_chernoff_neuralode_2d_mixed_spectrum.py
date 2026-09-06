"""Unit tests for H-B2-1d (mixed-sign spectrum: one growing, one decaying eigenvalue). Written
BEFORE trusting the comparison, same discipline as the rest of the H-B2-1* family.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-chernoff-neuralode-2d-mixed-spectrum"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_mix_run", _HERE / "run.py")
mix = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mix)


def test_eigenvalues_are_genuinely_mixed_sign():
    assert mix.EIGENVALUES[0] > 0
    assert mix.EIGENVALUES[1] < 0


def test_m1_is_exactly_one_for_w_equal_growing_eigenvalue():
    """Exact-argument check (module docstring): for symmetric A with w = growing eigenvalue,
    M1 = sup ||e^{tA}||/e^{wt} should come out to (very close to) 1.0."""
    m1 = mix.measure_m1_with_w(1.0, mix.W)
    assert abs(m1 - 1.0) < 1e-6


def test_m2_is_close_to_one_for_both_blocks():
    """Same exact-argument logic extended to the finite-n propagator: positive-Taylor-terms
    truncation underestimates e^x for x>0, so M2 should also come out very close to 1."""
    for block_fn in (mix.block_order1, mix.block_order2):
        m2 = mix.measure_m2_with_w(block_fn, 1.0, 1000, mix.W)
        assert m2 <= 1.0 + 1e-6, f"M2={m2} exceeds 1 -- exact-argument claim violated"


def test_analytic_solution_at_zero_is_x0():
    assert np.allclose(mix.analytic_solution(0.0), mix.X0)


def test_positive_control_convergence():
    t = 1.0
    exact = mix.analytic_solution(t)
    err_small_n = np.linalg.norm(mix.iterate_block(mix.block_order1, t, 10) - exact)
    err_large_n = np.linalg.norm(mix.iterate_block(mix.block_order1, t, 20000) - exact)
    assert err_large_n < err_small_n
    assert err_large_n < 1e-2


def test_negative_control_flipped_sign_diverges_from_true_solution():
    def wrong_block(h):
        return np.eye(2) + h * (-mix.A)  # flips growth<->decay

    t = 1.0
    exact = mix.analytic_solution(t)
    result = mix.iterate_block(wrong_block, t, 10000)
    assert np.linalg.norm(result - exact) > 1.0


def test_empirical_order_recovers_known_rates():
    n_values = np.array([400, 800, 1600, 3200, 6400])
    order1_est, _ = mix.empirical_order(mix.block_order1, 1.0, n_values)
    order2_est, _ = mix.empirical_order(mix.block_order2, 1.0, n_values)
    assert 0.8 < order1_est < 1.2, f"order-1 empirical order {order1_est} not near 1"
    assert order2_est > order1_est + 0.4, "order-2 should decay meaningfully faster"
