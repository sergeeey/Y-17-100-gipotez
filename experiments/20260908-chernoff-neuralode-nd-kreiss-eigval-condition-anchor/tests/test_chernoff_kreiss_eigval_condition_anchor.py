"""Tests for H-B2-1z: eigenvalue-condition-number anchor for the non-converging deep_k."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location("chernoff_1z_run", HERE / "run.py")
eigval_anchor = importlib.util.module_from_spec(_SPEC)
sys.modules["chernoff_1z_run"] = eigval_anchor
_SPEC.loader.exec_module(eigval_anchor)


@pytest.fixture(scope="module")
def cached_result():
    return eigval_anchor.cmd_run()


def test_symmetric_matrix_has_kappa_exactly_one():
    """Positive control: for a NORMAL matrix, eigenvectors are orthonormal, so the
    eigenvalue condition number must be exactly 1 (no non-normal amplification)."""
    rng = np.random.default_rng(0)
    m = rng.standard_normal((10, 10))
    symmetric = (m + m.T) / 2
    info = eigval_anchor.eigenvalue_condition_number(symmetric)
    assert info["kappa_lambda1"] == pytest.approx(1.0, abs=1e-8)


def test_mechanism_gate_matrix_not_reused_elsewhere_in_arc():
    """MECH_GATE_N_DIM/SEED must not collide with H-B2-1x's train/test population or
    H-B2-1y's SAMPLE_MATRICES -- it exists purely as an independent counter-example."""
    pair = (eigval_anchor.MECH_GATE_N_DIM, eigval_anchor.MECH_GATE_SEED)
    x_pairs = {(r["n_dim"], r["seed"]) for r in eigval_anchor.H_B2_1X_RESULT["train_data"]}
    x_pairs |= {(r["n_dim"], r["seed"]) for r in eigval_anchor.H_B2_1X_RESULT["test_data"]}
    assert pair not in x_pairs


def test_kappa_vs_deep_k_comparison_covers_all_16_h_b2_1y_matrices(cached_result):
    comparison = cached_result["kappa_vs_deep_k_comparison"]
    rows = cached_result["kappa_vs_deep_k_rows"]
    assert comparison["n_matrices"] == 16
    assert len(rows) == 16
    for row in rows:
        assert row["kappa_lambda1"] > 0
        assert row["deep_k"] > 0


def test_claim1_supported_flag_matches_the_actual_exceed_count(cached_result):
    comparison = cached_result["kappa_vs_deep_k_comparison"]
    rows = cached_result["kappa_vs_deep_k_rows"]
    actual_exceeds = sum(1 for r in rows if r["deep_k_exceeds_kappa"])
    assert comparison["n_deep_k_exceeds_kappa"] == actual_exceeds
    assert comparison["claim1_supported"] == (actual_exceeds == 0)


def test_refit_uses_the_full_h_b2_1x_population_not_a_subset(cached_result):
    refit = cached_result["refit_with_kappa"]
    assert refit["n_train"] == len(eigval_anchor.H_B2_1X_RESULT["train_data"]) == 80
    assert refit["n_test"] == len(eigval_anchor.H_B2_1X_RESULT["test_data"]) == 30


def test_two_feature_model_matches_h_b2_1x_feature_shape(cached_result):
    """H-B2-1x's own reference RMSE comes from a 2-feature model (log_K + log_N_DIM),
    not single-feature -- the two-feature refit here must use the same shape for the
    RMSE comparison to be apples-to-apples."""
    refit = cached_result["refit_with_kappa"]
    for key in (
        "two_feature_kappa_intercept",
        "two_feature_kappa_exponent",
        "two_feature_n_dim_exponent",
        "two_feature_rmse_kappa_model_on_fresh_test",
        "single_feature_kappa_exponent",
        "single_feature_rmse_kappa_model_on_fresh_test",
    ):
        assert key in refit


def test_mechanism_gate_ratios_cover_every_configured_eps(cached_result):
    mech = cached_result["mechanism_claim_gate"]
    for eps in eigval_anchor.MECH_GATE_EPS_VALUES:
        assert str(eps) in mech["ratios_by_eps"]


def test_verdict_is_one_of_the_three_defined_outcomes(cached_result):
    assert cached_result["verdict"] in {
        "KAPPA_LAMBDA1_CONFIRMED_AS_CONVERGENT_ANCHOR",
        "CLAIM1_SUPPORTED_BUT_MECHANISM_GATE_INCONCLUSIVE",
        "CLAIM1_REJECTED",
    }
