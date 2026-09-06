"""Unit tests for H-B2-1g (N=8, strong coupling). Written BEFORE trusting the comparison, same
discipline as the rest of the H-B2-1* family.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-chernoff-neuralode-nd-strong-coupling"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_strong_run", _HERE / "run.py")
strong = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(strong)


def test_coupling_magnitude_is_5x_h_b2_1f():
    assert strong.COUPLING_MAGNITUDE == 15.0


def test_eigenvalues_unchanged_from_h_b2_1f():
    eigvals = np.sort(np.linalg.eigvals(strong.A).real)
    expected = np.sort(np.array([0.5, -1.0, -2.0, -3.0, -4.0, -5.0, -6.0, -8.0]))
    assert np.allclose(eigvals, expected)


def test_a_is_genuinely_non_normal():
    assert not strong.is_normal(strong.A)


def test_analytic_solution_at_zero_is_x0():
    assert np.allclose(strong.analytic_solution(0.0), strong.X0)


def test_positive_control_convergence():
    t = 1.0
    exact = strong.analytic_solution(t)
    err_small_n = np.linalg.norm(strong.iterate_block(strong.block_order1, t, 10) - exact)
    err_large_n = np.linalg.norm(strong.iterate_block(strong.block_order1, t, 20000) - exact)
    assert err_large_n < err_small_n


def test_negative_control_flipped_sign_diverges():
    def wrong_block(h):
        return np.eye(strong.N_DIM) + h * (-strong.A)

    t = 1.0
    exact = strong.analytic_solution(t)
    result = strong.iterate_block(wrong_block, t, 10000)
    assert np.linalg.norm(result - exact) > 1.0
