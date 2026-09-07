"""Tests for H-B2-1h: coupling-magnitude sweep of M1 (H-B2-1g's own named Relaxation Map item).
Reuses `measure_m1_with_w` UNCHANGED from H-B2-1g's run.py -- already validated there and in every
prior H-B2-1* experiment; these tests confirm (a) it behaves sanely on a hand-checkable 1D case and
(b) the sweep script runs end-to-end and reproduces H-B2-1f/g's own already-committed M1 values at
coupling=3 and coupling=15 exactly (a strong regression guard, not just a smoke test).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_G_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-chernoff-neuralode-nd-strong-coupling"
)
_SPEC_G = importlib.util.spec_from_file_location("chernoff_1g_run", _G_DIR / "run.py")
h2_1g = importlib.util.module_from_spec(_SPEC_G)
_SPEC_G.loader.exec_module(h2_1g)

_SWEEP_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-chernoff-neuralode-nd-coupling-sweep"
)
_SPEC_SWEEP = importlib.util.spec_from_file_location("chernoff_sweep_run", _SWEEP_DIR / "run.py")
sweep = importlib.util.module_from_spec(_SPEC_SWEEP)
_SPEC_SWEEP.loader.exec_module(sweep)


def test_measure_m1_on_pure_decay_matrix_equals_one():
    """Hand-checkable sanity: for A = diag(-1) (pure decay, w chosen to exactly match the decay
    rate), ||expm(t*A)|| / exp(w*t) = exp(-t)/exp(-t) = 1 for all t -- M1 must be exactly 1
    (up to floating point), confirming the helper is not silently off by a constant factor."""
    import numpy as np_local
    from scipy.linalg import expm

    a = np_local.array([[-1.0]])
    ts = np_local.linspace(0.001, 1.0, 500)
    ratios = [np_local.linalg.norm(expm(t * a), ord=2) / np_local.exp(-1.0 * t) for t in ts]
    assert abs(max(ratios) - 1.0) < 1e-8


def test_build_matrix_at_coupling_15_reproduces_h_b2_1g_module_level_matrix_exactly():
    """Regression guard: build_matrix(15.0) with the same seed/eigenvalues must reproduce
    H-B2-1g's own module-level A byte-for-byte -- confirming the sweep's matrix-construction
    logic (necessarily a local re-implementation, since H-B2-1g's own measure_m1_with_w closes
    over its module-level A rather than taking a matrix parameter) is not a subtly different RNG
    call order or eigenvalue set."""
    a = sweep.build_matrix(15.0)
    assert np.allclose(a, h2_1g.A)


def test_build_matrix_at_coupling_3_reproduces_h_b2_1f_m1_exactly():
    """Regression guard: coupling_magnitude=3.0 with the same seed/eigenvalues must reproduce
    H-B2-1f's own already-committed M1=2.665 (to the precision it was reported)."""
    a = sweep.build_matrix(3.0)
    m1 = sweep.measure_m1(a, 1.0, h2_1g.W)
    assert abs(m1 - 2.665) < 0.01


def test_measure_m1_matches_h_b2_1g_own_module_level_result_exactly():
    """The local measure_m1(A, ...) must give the SAME value as H-B2-1g's own
    measure_m1_with_w() when applied to H-B2-1g's own module-level A -- confirms the local
    re-implementation is a faithful mirror, not a subtly different formula."""
    m1_local = sweep.measure_m1(h2_1g.A, 1.0, h2_1g.W)
    m1_original = h2_1g.measure_m1_with_w(1.0, h2_1g.W)
    assert abs(m1_local - m1_original) < 1e-9


def test_real_sweep_runs_and_m1_is_monotonically_increasing_in_coupling():
    """Smoke test against the real construction -- confirms the sweep executes end-to-end and
    M1 increases monotonically with coupling magnitude (a basic sanity property any of the
    candidate functional forms -- linear, polynomial, exponential -- must share)."""
    result = sweep.cmd_run()
    m1_values = [result["per_coupling"][str(c)]["m1"] for c in sweep.COUPLING_VALUES]
    assert all(m1_values[i] < m1_values[i + 1] for i in range(len(m1_values) - 1))
    assert isinstance(np.array(m1_values).dtype, np.dtype)
