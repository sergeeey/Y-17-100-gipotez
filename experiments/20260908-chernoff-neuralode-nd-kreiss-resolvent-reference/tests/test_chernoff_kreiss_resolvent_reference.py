"""Tests for H-B2-2: direct resolvent-norm reference K(A), no pseudopy."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location("chernoff_2_run", HERE / "run.py")
resolvent_ref = importlib.util.module_from_spec(_SPEC)
sys.modules["chernoff_2_run"] = resolvent_ref
_SPEC.loader.exec_module(resolvent_ref)


@pytest.fixture(scope="module")
def cached_result():
    return resolvent_ref.cmd_run()


def test_positive_control_seed_314_matches_the_audit_and_independent_recheck():
    """External audit found K(A-shifted)>=108.838 for N=40,seed=314; this session's own
    independent script (scratchpad, not reused here) found 108.868. This experiment's
    combined kappa+floored-line-search reference must reproduce that same order and value,
    not a coincidentally different number."""
    import importlib.util as ilu

    m_dir = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
    spec_m = ilu.spec_from_file_location("t_multin", m_dir / "run.py")
    multin = ilu.module_from_spec(spec_m)
    spec_m.loader.exec_module(multin)

    a = multin.build_matrix_with_seed_and_n(40, 314)
    info = resolvent_ref.resolvent_reference_k(a)
    assert info["k_ref"] == pytest.approx(108.87, abs=0.5)
    assert info["line_search_dominates"] is True


def test_two_by_two_hand_derived_case_matches_kappa_when_no_interior_maximum():
    """For A=[[a,b],[0,d]] the analytic kappa(a)=sqrt(1+(b/(a-d))^2) is the exact answer
    (H-B2-1z's own hand-derived check) -- for THIS simple 2x2 case there is no interior
    eps where the ratio exceeds kappa (single non-dominant eigenvalue, no clustering), so
    K_ref should equal kappa(lambda_1) here, not be dragged up by the line search."""
    a, d, b = 0.5, -1.0, 2.0
    matrix = np.array([[a, b], [0.0, d]])
    hand_derived = math.sqrt(1 + (b / (a - d)) ** 2)
    info = resolvent_ref.resolvent_reference_k(matrix)
    assert info["kappa_lambda1"] == pytest.approx(hand_derived, abs=1e-6)
    assert info["k_ref"] == pytest.approx(hand_derived, rel=1e-3)


def test_k_ref_never_less_than_kappa_lambda1(cached_result):
    """K_ref = max(kappa, line_search) by construction -- must never undershoot kappa."""
    for row in cached_result["train_rows"] + cached_result["test_rows"]:
        assert row["k_ref"] >= row["kappa_lambda1"] - 1e-9


def test_dominance_is_a_real_minority_not_zero_not_everything(cached_result):
    """Sanity bound on the population-level finding: the pre-check (7 matrices, 1 exception)
    predicted this would be a real but minority phenomenon, not universal and not absent."""
    summary = cached_result["dominance_summary"]
    assert summary["n_total"] == 110
    assert 0 < summary["n_line_search_dominates"] < summary["n_total"]
    assert summary["fraction_dominates"] < 0.3, "line-search dominance should be a minority"


def test_refit_uses_full_population_both_feature_shapes(cached_result):
    refit = cached_result["refit_with_k_ref"]
    for key in (
        "single_feature_exponent",
        "single_feature_rmse_on_fresh_test",
        "two_feature_kref_exponent",
        "two_feature_n_dim_exponent",
        "two_feature_rmse_on_fresh_test",
    ):
        assert key in refit
    assert cached_result["config"]["n_train"] == 80
    assert cached_result["config"]["n_test"] == 30


def test_line_search_floor_does_not_silently_clip_a_real_interior_maximum():
    """For a matrix where the line search DOES dominate (seed=314), the found x_star must
    sit comfortably above X_FLOOR, not pinned at the floor -- pinning at the floor would
    mean the search never actually found an interior maximum, just hit its own boundary."""
    import importlib.util as ilu

    m_dir = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
    spec_m = ilu.spec_from_file_location("t2_multin", m_dir / "run.py")
    multin = ilu.module_from_spec(spec_m)
    spec_m.loader.exec_module(multin)

    a = multin.build_matrix_with_seed_and_n(40, 314)
    alpha = float(np.max(np.linalg.eigvals(a).real))
    search = resolvent_ref.line_search_floored(a, alpha)
    assert not search["near_floor"]
    assert search["x_star"] > 100 * resolvent_ref.X_FLOOR
