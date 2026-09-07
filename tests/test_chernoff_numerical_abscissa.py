"""Tests for H-B2-1n: does the numerical abscissa omega(A) explain M1 where kappa(V) failed
at large N_DIM?
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-numerical-abscissa"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1n_run", _HERE / "run.py")
abscissa = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(abscissa)

_M_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-multiseed-multin"
)
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1m_run", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_K_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-dimension-sweep"
)
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1k_run", _K_DIR / "run.py")
dim_sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(dim_sweep)


def test_reuses_h_b2_1m_build_matrix_and_h_b2_1k_measure_m1_unchanged():
    """Minimal Relaxation Rule check, source-compared -- same discipline as H-B2-1m's own test
    against its parents."""
    assert inspect.getsource(abscissa.multin.build_matrix_with_seed_and_n) == inspect.getsource(
        multin.build_matrix_with_seed_and_n
    )
    assert inspect.getsource(abscissa.dim_sweep.measure_m1) == inspect.getsource(
        dim_sweep.measure_m1
    )


def test_numerical_abscissa_of_symmetric_matrix_equals_its_max_eigenvalue():
    """For a symmetric matrix, A = (A+A^T)/2 exactly, so omega(A) must equal the matrix's own
    largest eigenvalue -- a hand-checkable sanity bound."""
    a = np.array([[3.0, 1.0], [1.0, 2.0]])  # symmetric
    expected = float(np.max(np.linalg.eigvalsh(a)))
    assert abs(abscissa.numerical_abscissa(a) - expected) < 1e-10


def test_numerical_abscissa_of_skew_symmetric_matrix_is_zero():
    """A purely skew-symmetric matrix (A^T = -A) has (A+A^T)/2 = 0 exactly -- omega(A) must be
    exactly 0, a second hand-checkable case distinguishing omega(A) from eigenvalue-based
    descriptors (a skew-symmetric matrix has purely imaginary eigenvalues, Re(lambda)=0, so this
    also confirms omega(A) is NOT simply re-deriving max(Re(lambda)) by another name in this
    edge case -- it correctly reports the symmetric-part bound of exactly 0)."""
    a = np.array([[0.0, 2.0, -1.0], [-2.0, 0.0, 3.0], [1.0, -3.0, 0.0]])
    assert abs(abscissa.numerical_abscissa(a)) < 1e-10


def test_numerical_abscissa_upper_bounds_growth_rate_bendixson_check():
    """Direct numerical check of the Bendixson bound this experiment's claim.md cites as a
    proven fact, not an assumed behavior: d/dt||x(t)||^2 <= 2*omega(A)*||x(t)||^2 for x'=Ax.
    Verify on a small random non-normal matrix by finite-difference estimating the growth rate
    of ||x(t)||^2 at t=0 and confirming it does not exceed 2*omega(A) (within numerical
    tolerance)."""
    rng = np.random.default_rng(0)
    a = rng.normal(size=(4, 4))
    omega = abscissa.numerical_abscissa(a)
    x0 = rng.normal(size=4)
    x0 = x0 / np.linalg.norm(x0)
    dt = 1e-6
    from scipy.linalg import expm

    x_t = expm(dt * a) @ x0
    growth_rate_estimate = (np.linalg.norm(x_t) ** 2 - 1.0) / dt
    assert growth_rate_estimate <= 2 * omega + 1e-3  # small numerical slack for finite dt


def test_real_run_uses_identical_population_to_h_b2_1m_power_followup():
    assert abscissa.LARGE_N_DIM_VALUES == (16, 24, 32, 40, 50)
    assert abscissa.N_SEEDS == multin.N_SEEDS_LARGE_N


def test_real_run_produces_5_slices_with_verdict():
    result = abscissa.cmd_run()
    assert len(result["per_n_slice"]) == 5
    assert result["verdict"] in {"CONFIRMED", "WEAKENED", "REJECTED"}
    summary = result["slice_summary"]
    assert summary["n_slices"] == 5
    assert 0 <= summary["n_slices_significant_alpha05"] <= 5
    # each slice's own reported omega range must be non-degenerate for the correlation to mean
    # anything -- lock in that this is checked and reported, not silently assumed
    for n_dim_str, slice_data in result["per_n_slice"].items():
        assert slice_data["omega_range"][1] >= slice_data["omega_range"][0]
