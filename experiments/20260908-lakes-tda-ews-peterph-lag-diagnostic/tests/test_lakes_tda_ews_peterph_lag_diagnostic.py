"""Tests for H-B3-1o: Peter pH lag diagnostic (half-rise-date metric + positive control gate)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location("chernoff_1o_run", HERE / "run.py")
lag_diag = importlib.util.module_from_spec(_SPEC)
sys.modules["chernoff_1o_run"] = lag_diag
_SPEC.loader.exec_module(lag_diag)


@pytest.fixture(scope="module")
def cached_result():
    return lag_diag.cmd_run()


def test_half_rise_date_on_synthetic_step_function():
    """Independent hand-checkable case: a series that jumps from 0 to 10 exactly halfway
    through the window should have its half-rise date at (or right after) the jump."""
    dates = np.arange(0, 20, dtype=float)
    series = np.concatenate([np.zeros(10), np.full(10, 10.0)])
    hr = lag_diag.half_rise_date(series, dates)
    assert hr == pytest.approx(10.0, abs=1e-9)


def test_half_rise_date_on_monotone_ramp_is_at_true_midpoint():
    """A perfectly linear ramp from 0 to 100 over dates 0..100 should have its half-rise
    date very close to 50 (the true midpoint) -- sanity check independent of any lake data."""
    dates = np.linspace(0, 100, 101)
    series = np.linspace(0, 100, 101)
    hr = lag_diag.half_rise_date(series, dates)
    assert hr == pytest.approx(50.0, abs=1.0)


def test_half_rise_date_returns_none_for_constant_series():
    dates = np.arange(0, 10, dtype=float)
    series = np.full(10, 5.0)
    assert lag_diag.half_rise_date(series, dates) is None


def test_ph_stored_crossings_match_h_b3_1g_exactly(cached_result):
    """Reused values (classical/tda crossings for Peter pH and doSat) must match H-B3-1g's
    own committed metrics/run.json exactly -- Minimal Relaxation Rule, not re-derived."""
    ph = cached_result["primary"]
    assert ph["ph_classical_crossing"] == pytest.approx(218.0027397260917, abs=1e-6)
    assert ph["ph_tda_crossing"] == pytest.approx(318.0054794521577, abs=1e-6)


def test_verdict_is_one_of_three_defined_outcomes(cached_result):
    assert cached_result["verdict"] in {
        "METRIC_UNRELIABLE",
        "ARTIFACT_HYPOTHESIS_SUPPORTED",
        "GENUINE_DELAY_HYPOTHESIS_SUPPORTED",
    }


def test_verdict_is_metric_unreliable_when_gate_fails(cached_result):
    """Cross-check the pre-registered gate logic: if the positive control gate did not
    pass, the verdict MUST be METRIC_UNRELIABLE regardless of how suggestive the primary
    numbers look -- this is the specific discipline this experiment is built to enforce."""
    gate = cached_result["positive_control"]
    if not gate["gate_passes"]:
        assert cached_result["verdict"] == "METRIC_UNRELIABLE"


def test_gate_distance_computed_correctly(cached_result):
    gate = cached_result["positive_control"]
    expected = abs(gate["dosat_half_rise_date"] - gate["dosat_tda_crossing"])
    assert gate["dosat_gate_distance_days"] == pytest.approx(expected, abs=1e-9)
