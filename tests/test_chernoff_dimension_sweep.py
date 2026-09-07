"""Tests for H-B2-1k: is M1(N_DIM) monotonic at a FIXED spectral range?

Confirms (a) the construction correctly holds spectral range fixed while N varies (hand-checkable
properties), (b) measure_m1 matches the formula used throughout every prior H-B2-1* experiment,
(c) the real sweep runs end-to-end and reports a coherent shape.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_K_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-dimension-sweep"
)
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1k_run", _K_DIR / "run.py")
sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(sweep)


def test_build_matrix_holds_spectral_range_fixed_across_n_dim():
    """The whole point of this experiment: min/max eigenvalue must be the SAME regardless of
    n_dim (unlike H-B2-1j's own convention, where the range itself scaled with N)."""
    for n_dim in (3, 8, 50):
        a = sweep.build_matrix(n_dim)
        eigenvalues = np.diag(a)
        assert eigenvalues[0] == sweep.POSITIVE_EIGENVALUE
        assert np.isclose(eigenvalues[1:].min(), sweep.SPECTRAL_RANGE[0])
        assert np.isclose(eigenvalues[1:].max(), sweep.SPECTRAL_RANGE[1])


def test_build_matrix_at_n_dim_2_places_single_negative_eigenvalue_at_range_start():
    """Documented edge case (see claim.md): with only 1 negative eigenvalue, linspace's own
    num=1 behavior returns just the range start, not a meaningful 'span'. N=2 is deliberately
    excluded from the real sweep for this reason -- this test locks in WHY, so the exclusion
    isn't silently forgotten if someone is tempted to re-add N=2 later."""
    a = sweep.build_matrix(2)
    eigenvalues = np.diag(a)
    assert eigenvalues[1] == sweep.SPECTRAL_RANGE[0]
    assert 2 not in sweep.N_DIM_VALUES


def test_build_matrix_shape_matches_n_dim():
    for n_dim in (3, 4, 50):
        a = sweep.build_matrix(n_dim)
        assert a.shape == (n_dim, n_dim)


def test_build_matrix_is_upper_triangular_plus_diagonal():
    a = sweep.build_matrix(10)
    lower = np.tril(a, k=-1)
    assert np.allclose(lower, 0.0)


def test_measure_m1_on_pure_decay_matrix_equals_one():
    """Hand-checkable sanity, same as prior H-B2-1* test suites: for A=diag(-1), M1 must be
    exactly 1 (w chosen to exactly match the decay rate)."""
    a = np.array([[-1.0]])
    m1 = sweep.measure_m1(a, 1.0, -1.0)
    assert abs(m1 - 1.0) < 1e-8


def test_is_monotonic_detects_strictly_increasing_and_decreasing():
    assert sweep.is_monotonic(np.array([1.0, 2.0, 3.0, 4.0]))
    assert sweep.is_monotonic(np.array([4.0, 3.0, 2.0, 1.0]))


def test_is_monotonic_detects_non_monotonic_sequence():
    assert not sweep.is_monotonic(np.array([1.0, 5.0, 2.0, 8.0]))
    assert not sweep.is_monotonic(np.array([5.0, 1.0, 8.0, 2.0]))


def test_real_sweep_runs_and_reports_coherent_shape():
    result = sweep.cmd_run()
    assert result["verdict"] in {"CONFIRMED", "REJECTED"}
    assert len(result["m1_sequence"]) == len(sweep.N_DIM_VALUES)
    assert len(result["consecutive_diffs"]) == len(sweep.N_DIM_VALUES) - 1
    assert all(v > 0 for v in result["m1_sequence"])
    assert result["is_monotonic"] == (result["verdict"] == "REJECTED")
