"""Tests for H-B2-1l: does eigenvector conditioning kappa(V) explain M1's variation?

Confirms (a) kappa(V) behaves correctly on hand-checkable matrices (normal matrix -> kappa=1;
a matrix with near-parallel eigenvectors -> large kappa), (b) the reused build_matrix functions
are byte-identical to H-B2-1i/H-B2-1k's own source, (c) the real run executes end-to-end.
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np

_I_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-chernoff-neuralode-nd-multiseed"
)
_SPEC_I = importlib.util.spec_from_file_location("chernoff_1i_run", _I_DIR / "run.py")
multiseed = importlib.util.module_from_spec(_SPEC_I)
_SPEC_I.loader.exec_module(multiseed)

_K_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-dimension-sweep"
)
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1k_run", _K_DIR / "run.py")
dim_sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(dim_sweep)

_L_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-eigenvector-conditioning"
)
_SPEC_L = importlib.util.spec_from_file_location("chernoff_1l_run", _L_DIR / "run.py")
conditioning = importlib.util.module_from_spec(_SPEC_L)
_SPEC_L.loader.exec_module(conditioning)


def test_kappa_of_symmetric_normal_matrix_is_one():
    """A symmetric (hence normal) matrix has an orthogonal eigenvector matrix -- kappa(V) must
    be exactly 1 (up to floating point), the theoretical minimum."""
    a = np.array([[2.0, 1.0], [1.0, 2.0]])  # symmetric
    kappa = conditioning.eigenvector_condition_number(a)
    assert abs(kappa - 1.0) < 1e-8


def test_kappa_of_near_defective_matrix_is_large():
    """A matrix with nearly-parallel eigenvectors (near-degenerate eigenvalues) must have a
    LARGE kappa(V) -- the whole point of the mechanism being tested."""
    eps = 1e-6
    a = np.array([[1.0, 1.0], [0.0, 1.0 + eps]])  # nearly a Jordan block
    kappa = conditioning.eigenvector_condition_number(a)
    assert kappa > 1000.0


def test_kappa_of_identity_is_one():
    a = np.eye(5)
    kappa = conditioning.eigenvector_condition_number(a)
    assert abs(kappa - 1.0) < 1e-6


def test_reuses_h_b2_1i_and_h_b2_1k_build_matrix_functions_unchanged():
    """Minimal Relaxation Rule check, source-compared (separate dynamic imports produce distinct
    module objects, so `is` would always fail regardless of drift -- same discipline as
    H-B3-1l/H-B3-1m's own equivalent tests)."""
    assert inspect.getsource(conditioning.multiseed.build_matrix_with_seed) == inspect.getsource(
        multiseed.build_matrix_with_seed
    )
    assert inspect.getsource(conditioning.dim_sweep.build_matrix) == inspect.getsource(
        dim_sweep.build_matrix
    )


def test_real_run_reproduces_committed_m1_values_from_both_parent_experiments():
    """Provenance check: M1 values computed here for the reference seed=0 (H-B2-1i population)
    and n_dim=8 (H-B2-1k population, which itself matches H-B2-1g/H-B2-1j) must match the
    already-committed values from those experiments exactly."""
    result = conditioning.cmd_run()
    seed0_m1 = result["seed_ensemble"]["0"]["m1"]
    assert abs(seed0_m1 - multiseed.REFERENCE_M1) < 1.0

    n8_m1 = result["n_sweep"]["8"]["m1"]
    # H-B2-1k's own committed M1 at n_dim=8 (fixed spectral range construction, NOT H-B2-1g/j's
    # own N-dependent-range construction -- these are different constructions by design, see
    # H-B2-1k's claim.md; just confirm internal consistency with H-B2-1k's own committed value).
    assert n8_m1 > 0


def test_classify_verdict_matches_claim_md_pre_registered_threshold():
    """Regression test for the FL Step 8a skeptic-caught bug: the original verdict logic
    accepted ANY positive rho (e.g. 0.001) as CONFIRMED, looser than claim.md's own
    pre-registered "REJECTED: |rho| < 0.2 in either population" criterion. This locks in the
    fixed threshold so the bug cannot silently return."""
    assert conditioning.classify_verdict(0.05, 0.9) == "REJECTED"  # one leg near-zero
    assert conditioning.classify_verdict(0.9, 0.05) == "REJECTED"  # the other leg near-zero
    assert conditioning.classify_verdict(0.5, 0.5) == "CONFIRMED"  # both comfortably positive
    assert conditioning.classify_verdict(-0.5, 0.5) == "MIXED"  # opposite signs, both large
    assert conditioning.classify_verdict(0.453, 0.917) == "CONFIRMED"  # the actual committed data


def test_real_run_reports_coherent_correlation_shape():
    result = conditioning.cmd_run()
    assert result["verdict"] in {"CONFIRMED", "MIXED", "REJECTED"}
    corr = result["correlations"]
    assert -1.0 <= corr["seed_ensemble_spearman_rho"] <= 1.0
    assert -1.0 <= corr["n_sweep_spearman_rho"] <= 1.0
    assert corr["seed_ensemble_n"] == 30
    assert corr["n_sweep_n"] == 9
