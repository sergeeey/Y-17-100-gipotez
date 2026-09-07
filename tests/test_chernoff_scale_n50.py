"""Tests for H-B2-1j: does the Theorem 3.1 bound stay valid/order-matching at N_DIM=50?

Confirms (a) the construction is a faithful dimensional extension of H-B2-1f/g's own pattern
(hand-checkable properties), (b) the real run executes end-to-end and reports a coherent shape.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_J_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260907-chernoff-neuralode-nd-scale"
)
_SPEC_J = importlib.util.spec_from_file_location("chernoff_1j_run", _J_DIR / "run.py")
scale = importlib.util.module_from_spec(_SPEC_J)
_SPEC_J.loader.exec_module(scale)


def test_eigenvalue_spectrum_has_one_positive_and_n_minus_1_negative():
    """Matches every prior H-B2-1* construction: one growing mode, the rest decaying."""
    assert scale.N_DIM == 50
    assert len(scale.EIGENVALUES) == 50
    assert scale.EIGENVALUES[0] == 0.5
    assert np.all(scale.EIGENVALUES[1:] < 0)
    assert scale.EIGENVALUES.min() == -50.0


def test_matrix_a_is_upper_triangular_plus_diagonal_perturbation():
    """A = diag(eigenvalues) + strictly-upper-triangular coupling -- lower triangle (excluding
    diagonal) must be exactly zero, matching H-B2-1f/g's own construction."""
    lower = np.tril(scale.A, k=-1)
    assert np.allclose(lower, 0.0)
    assert np.allclose(np.diag(scale.A), scale.EIGENVALUES)


def test_block_order1_and_order2_reduce_to_identity_at_h_zero():
    assert np.allclose(scale.block_order1(0.0), np.eye(scale.N_DIM))
    assert np.allclose(scale.block_order2(0.0), np.eye(scale.N_DIM))


def test_empirical_order_of_order1_scheme_is_near_1_on_a_simple_diagonal_case():
    """Sanity check on the empirical_order machinery itself, independent of the real 50-dim A:
    a diagonal-only system's order-1 (forward Euler) scheme must show order close to 1."""
    diag_only = np.diag([-1.0, -2.0])
    n_dim_local = 2
    x0_local = np.ones(n_dim_local)

    def block1(h: float) -> np.ndarray:
        return np.eye(n_dim_local) + h * diag_only

    def analytic(t: float) -> np.ndarray:
        from scipy.linalg import expm as expm_local

        return expm_local(t * diag_only) @ x0_local

    n_values = np.array([50, 100, 200, 400, 800])
    errors = np.array(
        [
            np.linalg.norm(
                np.linalg.matrix_power(block1(1.0 / int(n)), int(n)) @ x0_local - analytic(1.0)
            )
            for n in n_values
        ]
    )
    slope, _ = np.polyfit(np.log(n_values.astype(float)), np.log(errors), 1)
    assert abs(-slope - 1.0) < 0.15


def test_real_run_executes_and_reports_coherent_shape():
    result = scale.cmd_run()
    assert result["config"]["n_dim"] == 50
    assert isinstance(result["mechanism_holds_at_n50"], bool)
    for label in ("order1", "order2"):
        entry = result["results"][label]
        assert entry["empirical_order_estimate"] > 0
        assert isinstance(entry["all_n_bound_holds"], bool)
        for n_entry in entry["per_n"].values():
            assert n_entry["theorem_3_1_bound"] > 0
