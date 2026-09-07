"""Tests for the Paul lake within-lake variable comparison (H-B3-1h decision.md Addendum 3)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_MOD_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-lakes-tda-ews-invariant-conjunction"
)
_SPEC = importlib.util.spec_from_file_location(
    "paul_lake_variable_comparison", _MOD_DIR / "paul_lake_variable_comparison.py"
)
mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mod)


def test_acf_lag1_of_pure_ar1_matches_its_own_coefficient():
    """Hand-checkable synthetic sanity check: a pure AR(1) process x[t] = phi*x[t-1] + noise
    should have empirical ACF lag-1 close to phi, before trusting the ACF helper on real data."""
    rng = np.random.default_rng(0)
    phi = 0.8
    n = 5000
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + rng.normal(0, 1)
    result = mod.acf(x, 3)
    assert abs(result[0] - phi) < 0.03


def test_acf_of_white_noise_is_near_zero():
    rng = np.random.default_rng(1)
    x = rng.normal(0, 1, 5000)
    result = mod.acf(x, 3)
    assert all(abs(v) < 0.05 for v in result)


def test_real_paul_lake_comparison_runs_and_reports_expected_shape():
    """Smoke test against the real data file -- confirms all 3 variables load and the reported
    ranking (doSat lowest ACF lag-1, pH strongest trend) matches the already-verified finding."""
    result = mod.main()
    per_var = result["per_variable"]
    assert set(per_var.keys()) == {"chl", "pH", "doSat"}
    # Regression guard on the already-verified, documented finding (decision.md Addendum 3):
    # pH has the strongest trend magnitude, doSat has the lowest lag-1 autocorrelation.
    trend_by_var = {v: abs(per_var[v]["spearman_trend_rho"]) for v in per_var}
    assert max(trend_by_var, key=trend_by_var.get) == "pH"
    acf1_by_var = {v: per_var[v]["acf_lag1_3"][0] for v in per_var}
    assert min(acf1_by_var, key=acf1_by_var.get) == "doSat"


def test_count_seasons_finds_real_gaps_not_a_constant_one():
    """Regression test for a reviewer-caught bug: the original approx_n_seasons heuristic
    diffed `season_time`, whose own gap-bridging logic (peterlake/run.py's own
    median_gap_bridge_days) deliberately compresses every season boundary to a single nominal
    step -- indistinguishable from a normal daily increment -- so the old heuristic silently
    returned 1 for every series, always. count_seasons must find the real multi-season structure
    (Paul lake spans 2008-2010 field seasons, per peterlake/run.py's own INCLUDED_SEASONS) by
    re-deriving gaps from the raw decimal-year axis instead."""
    n = mod.count_seasons("chl", "Paul")
    assert n > 1, "count_seasons must not silently collapse to the old constant-1 bug"
    assert n <= len(mod.peter.INCLUDED_SEASONS)
