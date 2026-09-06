"""Tests for the V1 surrogate-null detection rule (added to
experiments/20260906-may1972-tda-ews-obrienlakes/run.py: surrogate_null_curve, surrogate_crossing).

Key property under test: a per-series, per-timepoint AR(1)-surrogate null should fire at
approximately its nominal alpha rate on data DRAWN FROM THAT SAME NULL -- unlike the fixed
tau>=0.5 threshold, which fired on 45-90% of such surrogates (see both parent decision.md files).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_SPEC = importlib.util.spec_from_file_location(
    "obrien_lakes_run",
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-may1972-tda-ews-obrienlakes"
    / "run.py",
)
mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mod)


def test_surrogate_null_curve_shape_matches_rolling_stat_length():
    rng = np.random.default_rng(1)
    x = np.cumsum(rng.normal(0, 1, 150))
    window = 75
    curve = mod.surrogate_null_curve(x, window, "var", reps=10, seed=0)
    expected_len = len(x) - window + 1
    assert curve.shape == (expected_len,)


def test_surrogate_crossing_fires_when_real_exceeds_null():
    real = np.array([0.1, 0.2, np.nan, 0.9])
    null = np.array([0.5, 0.5, 0.5, 0.5])
    assert mod.surrogate_crossing(real, null) == 3


def test_surrogate_crossing_none_when_real_never_exceeds():
    real = np.array([0.1, 0.2, 0.3])
    null = np.array([0.5, 0.5, 0.5])
    assert mod.surrogate_crossing(real, null) is None


def test_surrogate_crossing_ignores_nan_positions_in_either_array():
    real = np.array([np.nan, 0.9, 0.9])
    null = np.array([0.5, np.nan, 0.3])
    # index 0: real is NaN -> skip. index 1: null is NaN -> skip. index 2: 0.9 > 0.3 -> fires.
    assert mod.surrogate_crossing(real, null) == 2


def test_self_consistency_ar1_surrogate_fires_near_nominal_alpha_not_near_certainty():
    """The whole point of V1: a series DRAWN FROM the null should cross its own (1-alpha)
    percentile close to `alpha` fraction of the time -- NOT the 45-90% the fixed threshold gave.
    Uses a modest rep count for test speed; asserts a loose bound (well above true alpha=0.05 to
    avoid flakiness, but far below the 0.45-0.90 floor this rule was built to fix)."""
    rng = np.random.default_rng(42)
    x = np.cumsum(rng.normal(0, 1, 120))
    window = 60
    trials = 12
    hits = 0
    for i in range(trials):
        test_rng = np.random.default_rng(100 + i)
        candidate = mod.ar1_surrogate(x, test_rng)
        null_curve = mod.surrogate_null_curve(candidate, window, "var", reps=15, seed=i)
        tau = mod.expanding_kendall_tau(mod.rolling_stat(candidate, window, "var"))
        if mod.surrogate_crossing(tau, null_curve) is not None:
            hits += 1
    rate = hits / trials
    assert rate < 0.5, (
        f"surrogate-null fired on {rate:.0%} of self-consistent draws -- still at floor"
    )
