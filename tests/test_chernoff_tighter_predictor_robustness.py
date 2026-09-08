"""Tests for H-B2-1x: robustness follow-up to H-B2-1w's K(A) exponent (~1.94 on 20 points) --
does it hold with a 4x larger training set and 95% confidence intervals, on a genuinely fresh
held-out set?"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260908-chernoff-neuralode-nd-tighter-predictor-robustness"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1x_run", _HERE / "run.py")
robustness = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(robustness)

_CACHED_RESULT = None


def _cached_run():
    """cmd_run() computes K(A) fresh for 60 expanded-TRAIN + 30 TEST matrices (~15-20s each) --
    cache across tests, same fix as H-B2-1s/1u/1v/1w's _cached_run helper."""
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = robustness.cmd_run()
    return _CACHED_RESULT


def test_expanded_train_has_80_rows_with_correct_seed_provenance():
    train = robustness.build_expanded_train_data()
    assert len(train) == 80  # 40 seeds x 2 N_DIM
    seeds_seen = {r["seed"] for r in train}
    assert seeds_seen == set(range(300, 340))


def test_expanded_train_k_estimate_matches_h_b2_1u_exactly_for_the_overlapping_seeds():
    train = robustness.build_expanded_train_data()
    row = next(r for r in train if r["seed"] == 301 and r["n_dim"] == 50)
    assert abs(row["k_estimate"] - 261.74496644295306) < 1e-6


def test_fresh_test_seed_range_has_zero_overlap_with_every_prior_range_in_the_arc():
    prior_ranges = [
        set(range(0, 40)),
        set(range(40, 100)),
        set(range(0, 60)),
        set(range(100, 160)),
        set(range(300, 340)),
        set(range(400, 415)),
    ]
    this_range = set(range(robustness.TEST_SEED_START, robustness.TEST_SEED_END))
    for prior in prior_ranges:
        assert this_range.isdisjoint(prior)
    assert robustness.TEST_SEED_START == 420


def test_ols_with_se_recovers_known_relationship_and_reasonable_uncertainty():
    """Positive control: fit y = 2 + 3*x1 - 1*x2 + small noise; OLS must recover coefficients
    close to the truth, and the TRUE coefficients must fall inside the reported 95% CI."""
    rng = np.random.default_rng(0)
    n = 200
    x1 = rng.uniform(1, 10, size=n)
    x2 = rng.uniform(1, 10, size=n)
    noise = rng.normal(0, 0.1, size=n)
    y = 2 + 3 * x1 - 1 * x2 + noise
    x = np.column_stack([np.ones_like(x1), x1, x2])
    coeffs, se = robustness._fit_ols_with_se(x, y)
    true_coeffs = np.array([2, 3, -1])
    assert np.allclose(coeffs, true_coeffs, atol=0.1)
    ci_low = coeffs - 1.96 * se
    ci_high = coeffs + 1.96 * se
    assert np.all(ci_low <= true_coeffs) and np.all(true_coeffs <= ci_high)


def test_cmd_run_produces_expected_shapes_and_verdict():
    result = _cached_run()
    assert result["config"]["n_train"] == 80
    assert result["config"]["n_test"] == 30
    assert len(result["fitted_coefficients"]) == 3
    assert len(result["standard_errors"]) == 3
    assert result["verdict"] in (
        "K_SQUARED_PATTERN_ROBUST",
        "EXPONENT_UNCERTAIN_INCLUDES_LINEAR",
        "EXPONENT_SHIFTED_AWAY_FROM_2",
    )


def test_verdict_matches_the_ci_bracket_logic():
    result = _cached_run()
    if result["ci_brackets_2"] and not result["ci_brackets_1"]:
        assert result["verdict"] == "K_SQUARED_PATTERN_ROBUST"
    elif result["ci_brackets_1"]:
        assert result["verdict"] == "EXPONENT_UNCERTAIN_INCLUDES_LINEAR"
    else:
        assert result["verdict"] == "EXPONENT_SHIFTED_AWAY_FROM_2"


def test_ci_is_well_formed():
    result = _cached_run()
    for lo, hi in zip(result["ci_95_low"], result["ci_95_high"]):
        assert lo <= hi
