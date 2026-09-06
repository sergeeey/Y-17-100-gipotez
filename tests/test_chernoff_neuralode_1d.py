"""Unit tests for H-B2-1 (Chernoff <-> Neural-ODE/ResNet bridge, 1D linear decay toy).

Written BEFORE trusting the final comparison, per this project's discipline: verify the harness
(positive/negative controls) independently of the actual claim being tested.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-chernoff-neuralode-1d-decay"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_run", _HERE / "run.py")
chernoff = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(chernoff)


def test_analytic_solution_known_values():
    assert chernoff.analytic_solution(0.0) == chernoff.X0
    assert abs(chernoff.analytic_solution(1.0) - np.exp(-1.0)) < 1e-12


def test_blocks_satisfy_chernoff_hypothesis_s0_equals_1():
    assert chernoff.block_order1(0.0) == 1.0
    assert chernoff.block_order2(0.0) == 1.0


def test_blocks_have_correct_derivative_at_zero_matching_generator():
    """Numerically confirm s'(0) = A for both blocks -- the third Chernoff hypothesis
    (Theorem 1.2)."""
    eps = 1e-6
    deriv1 = (chernoff.block_order1(eps) - chernoff.block_order1(0.0)) / eps
    deriv2 = (chernoff.block_order2(eps) - chernoff.block_order2(0.0)) / eps
    assert abs(deriv1 - chernoff.A) < 1e-4
    assert abs(deriv2 - chernoff.A) < 1e-4


def test_positive_control_iterate_block_converges_to_analytic_solution():
    """As n grows, block(t/n)^n * x0 must approach x0*e^{-t} (Chernoff's own basic theorem)."""
    t = 1.0
    exact = chernoff.analytic_solution(t)
    err_small_n = abs(chernoff.iterate_block(chernoff.block_order1, t, 10) - exact)
    err_large_n = abs(chernoff.iterate_block(chernoff.block_order1, t, 10000) - exact)
    assert err_large_n < err_small_n
    assert err_large_n < 1e-3


def test_negative_control_wrong_sign_block_does_not_converge_to_decay_solution():
    """A block with the WRONG generator (s(h)=1+h, i.e. growth not decay) must NOT converge to the
    decay solution -- confirms iterate_block doesn't spuriously match regardless of input."""

    def wrong_block(h):
        return 1.0 + h  # generator +1, not -1

    t = 1.0
    exact_decay = chernoff.analytic_solution(t)
    result = chernoff.iterate_block(wrong_block, t, 10000)
    assert abs(result - exact_decay) > 1.0  # e^{+1} vs e^{-1}, should differ by ~5


def test_chernoff_guaranteed_order_formula():
    """Pins formula (2), Galkin & Remizov 2021: guaranteed order = m - 1."""
    assert chernoff.chernoff_guaranteed_order(1) == 0.0
    assert chernoff.chernoff_guaranteed_order(2) == 1.0
    assert chernoff.chernoff_guaranteed_order(3) == 2.0


def test_empirical_order_recovers_known_textbook_rates():
    """Self-consistency / positive control for the regression machinery itself: the standard
    (order-1) Euler block is textbook-known to have GLOBAL error O(1/n); the order-2 block should
    show a materially faster decay. If this test fails, the regression harness itself is broken --
    unrelated to whether the Chernoff bound is informative (that's a separate, later question)."""
    n_values = np.array([200, 400, 800, 1600, 3200, 6400])
    order1_est, _ = chernoff.empirical_order(chernoff.block_order1, 1.0, n_values)
    order2_est, _ = chernoff.empirical_order(chernoff.block_order2, 1.0, n_values)
    assert 0.85 < order1_est < 1.15, f"order-1 block empirical order {order1_est} not near 1"
    assert order2_est > order1_est + 0.5, (
        f"order-2 block ({order2_est}) should decay meaningfully faster than order-1 ({order1_est})"
    )
