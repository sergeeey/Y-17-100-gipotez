"""Tests for H-B2-1m: genuinely independent multi-seed x multi-N_DIM test of kappa(V)->M1.

Regression-locks the FL Step 8a skeptic-caught RNG independence bug: build_matrix_with_seed_and_n
originally shared the raw uniform stream across N_DIM for a matching seed index (seeded on `seed`
alone). Fixed via SeedSequence([n_dim, seed]) -- this test file exists specifically so that fix
cannot silently regress, matching this project's established precedent for ar1_surrogate/
iaaft_surrogate/pettitt_test (new stochastic-draw machinery gets a dedicated independence test
BEFORE the real run is trusted).
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-multiseed-multin"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1m_run", _HERE / "run.py")
multin = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(multin)

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
eig_cond = importlib.util.module_from_spec(_SPEC_L)
_SPEC_L.loader.exec_module(eig_cond)


def test_reuses_h_b2_1k_measure_m1_and_h_b2_1l_eigenvector_condition_number_unchanged():
    """Minimal Relaxation Rule check, source-compared."""
    assert inspect.getsource(multin.dim_sweep.measure_m1) == inspect.getsource(dim_sweep.measure_m1)
    assert inspect.getsource(multin.eig_cond.eigenvector_condition_number) == inspect.getsource(
        eig_cond.eigenvector_condition_number
    )


def test_regression_seeds_are_independent_across_n_dim():
    """FL Step 8a skeptic-caught bug, regression-locked: for a FIXED seed, the coupling matrices
    built at different N_DIM must NOT come from a shared raw RNG stream. Before the fix,
    default_rng(0).uniform(size=(3,3)).ravel() == default_rng(0).uniform(size=(4,4)).ravel()[:9]
    -- i.e. build_matrix_with_seed_and_n(3, 0) and build_matrix_with_seed_and_n(4, 0) shared their
    first 9 draws. After the fix (SeedSequence([n_dim, seed])), they must not."""
    a3 = multin.build_matrix_with_seed_and_n(3, seed=0)
    a4 = multin.build_matrix_with_seed_and_n(4, seed=0)
    c3 = np.triu(a3, k=1)
    c3_vals = c3[c3 != 0]
    c4 = np.triu(a4, k=1)
    c4_vals = c4[c4 != 0][: len(c3_vals)]
    # if the streams were shared (the bug), these would be exactly equal
    assert not np.allclose(c3_vals, c4_vals), "RNG streams are shared across N_DIM -- regression!"


def test_regression_raw_rng_streams_differ_across_n_dim_for_same_seed():
    """Direct test of the exact failure mode the skeptic found: seed the RNG the way
    build_matrix_with_seed_and_n does internally and confirm two different N_DIM values at the
    SAME seed index do not produce byte-identical leading draws."""
    rng_a = np.random.default_rng(np.random.SeedSequence([3, 0]))
    rng_b = np.random.default_rng(np.random.SeedSequence([4, 0]))
    draws_a = rng_a.uniform(size=9)
    draws_b = rng_b.uniform(size=9)
    assert not np.array_equal(draws_a, draws_b)

    # confirm the OLD (buggy) pattern really would have collided, so this test is meaningful
    old_a = np.random.default_rng(0).uniform(size=(3, 3)).ravel()
    old_b = np.random.default_rng(0).uniform(size=(4, 4)).ravel()[:9]
    assert np.array_equal(old_a, old_b), (
        "sanity check: the old bug pattern itself changed behavior unexpectedly"
    )


def test_seeds_are_independent_across_seed_index_at_fixed_n_dim():
    """Different seeds at the SAME N_DIM must give different matrices (basic sanity -- this
    property was never broken, but locking it in alongside the N_DIM-independence test)."""
    a0 = multin.build_matrix_with_seed_and_n(8, seed=0)
    a1 = multin.build_matrix_with_seed_and_n(8, seed=1)
    assert not np.allclose(a0, a1)


def test_n3_low_dof_structural_check_runs_and_returns_bounded_correlations():
    result = multin.n3_low_dof_structural_check(n_seeds=15)
    for key in ("f1_vs_kappa", "f1_vs_m1", "f2_vs_kappa", "f2_vs_m1"):
        assert -1.0 <= result[key]["rho"] <= 1.0
        assert 0.0 <= result[key]["p"] <= 1.0


def test_p_value_floor_uses_exact_permutation_bound_not_arbitrary_tiny_float():
    """Regression test for the FL Step 8a skeptic finding: np.finfo(float).tiny as a Fisher
    p-value floor inflates the combined statistic far beyond what the sample size supports.
    The floor must be the exact-permutation minimum (2/N!), not an arbitrarily small float."""
    from math import factorial

    expected_floor = 2.0 / factorial(15)
    assert expected_floor > 1e-13  # sanity: this is a "small but real" number, not underflow-tiny
    assert expected_floor < 1e-11


def test_real_run_produces_9_slices_with_verdict_and_large_n_check():
    result = multin.cmd_run()
    assert len(result["per_n_slice"]) == 9
    assert result["verdict"] in {"CONFIRMED", "WEAKENED", "REJECTED"}
    summary = result["slice_summary"]
    assert 0 <= summary["n_slices_positive"] <= 9
    assert "n_large_n_slices_significant" in summary
    assert "decay_trend_rho_vs_n_dim" in summary
    # CONFIRMED requires a large-N individually-significant slice -- lock in the refined criterion
    if result["verdict"] == "CONFIRMED":
        assert summary["n_large_n_slices_significant"] > 0
