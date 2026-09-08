"""Tests for H-B2-1w: does a K(A)-based log-linear model predict M1 better than the naive
Kreiss ceiling or the arc's own established alpha_eps-only correlational predictor?"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260908-chernoff-neuralode-nd-tighter-predictor-m1"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1w_run", _HERE / "run.py")
predictor = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(predictor)

_CACHED_RESULT = None


def _cached_run():
    """cmd_run() computes K(A) fresh for 30 TEST matrices (~15-20s each) -- cache across tests,
    same fix as H-B2-1s/1u/1v's _cached_run helper."""
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = predictor.cmd_run()
    return _CACHED_RESULT


def test_train_data_reused_unchanged_from_h_b2_1u_and_h_b2_1t():
    train = predictor.build_train_data()
    assert len(train) == 20  # 10 seeds x 2 N_DIM
    for row in train:
        assert row["seed"] in range(300, 310)
        assert row["n_dim"] in (40, 50)
        assert row["k_estimate"] > 0
        assert row["m1"] > 0
        assert row["alpha_eps"] is not None


def test_train_k_estimate_matches_h_b2_1u_exactly_for_seed301_n50():
    train = predictor.build_train_data()
    row = next(r for r in train if r["seed"] == 301 and r["n_dim"] == 50)
    assert abs(row["k_estimate"] - 261.74496644295306) < 1e-6


def test_test_seed_range_has_zero_overlap_with_every_prior_range_in_the_arc():
    prior_ranges = [
        set(range(0, 40)),
        set(range(40, 100)),
        set(range(0, 60)),
        set(range(100, 160)),
        set(range(300, 340)),
    ]
    this_range = set(range(predictor.TEST_SEED_START, predictor.TEST_SEED_END))
    for prior in prior_ranges:
        assert this_range.isdisjoint(prior)
    assert predictor.TEST_SEED_START == 400


def test_ols_recovers_known_linear_relationship():
    """Positive control: fit y = 2 + 3*x1 - 1*x2 exactly (no noise), OLS must recover the exact
    coefficients."""
    rng = np.random.default_rng(0)
    x1 = rng.uniform(1, 10, size=20)
    x2 = rng.uniform(1, 10, size=20)
    y = 2 + 3 * x1 - 1 * x2
    x = np.column_stack([np.ones_like(x1), x1, x2])
    coeffs = predictor._fit_ols(x, y)
    assert np.allclose(coeffs, [2, 3, -1], atol=1e-8)


def test_rmse_is_zero_for_perfect_prediction():
    pred = np.array([1.0, 2.0, 3.0])
    actual = np.array([1.0, 2.0, 3.0])
    assert predictor._rmse(pred, actual) == 0.0


def test_cmd_run_produces_30_test_points_and_three_rmse_values():
    result = _cached_run()
    assert result["config"]["n_train"] == 20
    assert result["config"]["n_test"] == 30
    assert set(result["rmse_on_log_m1_test"].keys()) == {
        "k_model",
        "alpha_only_model",
        "naive_ceiling",
    }
    for rmse in result["rmse_on_log_m1_test"].values():
        assert rmse >= 0


def test_verdict_is_one_of_the_three_pre_registered_outcomes():
    result = _cached_run()
    assert result["verdict"] in (
        "K_MODEL_WINS",
        "NEITHER_MODEL_BEATS_CEILING",
        "K_MODEL_DOES_NOT_ADD_VALUE",
    )


def test_verdict_matches_the_actual_rmse_ordering():
    """The verdict field must be a mechanical, verifiable function of the RMSE numbers -- lock
    this down so a future edit can't silently decouple the label from the data."""
    result = _cached_run()
    rmses = result["rmse_on_log_m1_test"]
    best = min(rmses, key=rmses.get)
    if best == "k_model":
        assert result["verdict"] == "K_MODEL_WINS"
    elif best == "naive_ceiling":
        assert result["verdict"] == "NEITHER_MODEL_BEATS_CEILING"
    else:
        assert result["verdict"] == "K_MODEL_DOES_NOT_ADD_VALUE"
