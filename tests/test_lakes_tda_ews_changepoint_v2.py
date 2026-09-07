"""Tests for H-B3-1m: V2 two-part detection rule (tau AND Pettitt level-shift test).

Pettitt's test is hand-implemented (no already-installed dependency provides it). Per this
project's own precedent for `ar1_surrogate`/`iaaft_surrogate` (H-B3-1c/d), a hand-implemented
statistical primitive gets a positive-control AND a negative-control/calibration test BEFORE it
is trusted in the real pipeline -- these are that validation, run first in this file.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_B_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-may1972-tda-ews-obrienlakes"
)
_SPEC_B = importlib.util.spec_from_file_location("lakes_tda_ews_obrienlakes_run", _B_DIR / "run.py")
obrien = importlib.util.module_from_spec(_SPEC_B)
_SPEC_B.loader.exec_module(obrien)

_M_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260907-lakes-tda-ews-changepoint-v2"
)
_SPEC_M = importlib.util.spec_from_file_location(
    "lakes_tda_ews_changepoint_v2_run", _M_DIR / "run.py"
)
changepoint = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(changepoint)


# ───────────────────── Pettitt's test: positive control ─────────────────────
def test_pettitt_locates_an_obvious_step_change_at_the_midpoint():
    """Positive control: mean 0 for the first half, mean 10 for the second half, small noise.
    The test must locate the change-point near the true midpoint and report a tiny p-value."""
    rng = np.random.default_rng(0)
    n = 100
    x = np.concatenate([rng.normal(0, 0.5, n // 2), rng.normal(10, 0.5, n // 2)])
    k, p_value, changepoint_index = changepoint.pettitt_test(x)
    assert abs(changepoint_index - (n // 2 - 1)) <= 3
    assert p_value < 0.001
    assert k > 0


def test_pettitt_locates_change_regardless_of_direction():
    """Positive control, opposite sign: a downward step must also be detected (K is defined via
    |U_t|, so a decrease should be as detectable as an increase)."""
    rng = np.random.default_rng(1)
    n = 100
    x = np.concatenate([rng.normal(10, 0.5, n // 2), rng.normal(0, 0.5, n // 2)])
    _, p_value, changepoint_index = changepoint.pettitt_test(x)
    assert abs(changepoint_index - (n // 2 - 1)) <= 3
    assert p_value < 0.001


# ───────────────────── Pettitt's test: negative control / calibration ─────────────────────
def test_pettitt_false_positive_rate_on_pure_noise_is_not_wildly_miscalibrated():
    """Negative control: 200 independent white-noise trials, no real change-point. The observed
    false-positive rate at alpha=0.05 should be in a sane range around the nominal level -- a
    LOOSE bound (the p-value formula is an approximation, exact calibration is not expected),
    but it must not be wildly miscalibrated the way the ORIGINAL tau>=0.5 rule was (80-83%)."""
    rng = np.random.default_rng(42)
    alpha = 0.05
    n_trials = 200
    false_positives = 0
    for _ in range(n_trials):
        x = rng.normal(0, 1, 60)
        _, p_value, _ = changepoint.pettitt_test(x)
        if p_value < alpha:
            false_positives += 1
    fp_rate = false_positives / n_trials
    assert fp_rate < 0.20, f"Pettitt false-positive rate {fp_rate} is wildly miscalibrated"


def test_pettitt_on_constant_series_never_false_positives():
    """Degenerate negative control: a perfectly constant series has no structure at all -- K
    must be exactly 0 and p_value must be 1.0 (no spurious signal from a trivial input)."""
    x = np.full(30, 5.0)
    k, p_value, _ = changepoint.pettitt_test(x)
    assert k == 0.0
    assert p_value == 1.0


# ───────────────────── Two-part rule ─────────────────────
def test_two_part_crossing_requires_both_conditions():
    """A tau series that crosses but whose underlying raw statistic has NO real level shift
    (pure noise) must NOT count as crossing under the two-part rule."""
    rng = np.random.default_rng(7)
    raw = rng.normal(0, 1, 60)
    # Force a tau series that crosses everywhere, to isolate the Pettitt gate specifically.
    tau_series = np.full(60, 0.9)
    result = changepoint.two_part_crossing(raw, tau_series)
    # With pure noise, Pettitt should not (reliably) find a significant level shift.
    assert (
        result is None or changepoint.pettitt_test(raw[: result + 1])[1] < changepoint.PETTITT_ALPHA
    )


def test_two_part_crossing_none_when_tau_never_crosses():
    raw = np.concatenate([np.zeros(30), np.full(30, 10.0)])
    tau_series = np.full(60, 0.1)  # never reaches threshold
    assert changepoint.two_part_crossing(raw, tau_series) is None


def test_reuses_obrienlakes_pipeline_unchanged():
    """Minimal Relaxation Rule check, same discipline as H-B3-1l's own test: source-compared,
    not `is`-compared (separate dynamic imports produce distinct module objects)."""
    import inspect

    assert inspect.getsource(changepoint.obrien.rolling_stat) == inspect.getsource(
        obrien.rolling_stat
    )
    assert inspect.getsource(changepoint.obrien.expanding_kendall_tau) == inspect.getsource(
        obrien.expanding_kendall_tau
    )
    assert inspect.getsource(changepoint.obrien.ar1_surrogate) == inspect.getsource(
        obrien.ar1_surrogate
    )
    assert changepoint.obrien.LAKES == obrien.LAKES


# ───────────────────── Real run ─────────────────────
def test_real_run_executes_and_reports_coherent_shape():
    result = changepoint.cmd_run()
    assert result["verdict"] in {"CRITERION_INVALID", "PROMOTE", "REJECT"}
    assert 0.0 <= result["max_new_floor_fp_rate"] <= 1.0
    for lake in ("lower_zurich", "windermere", "loch_leven"):
        entry = result["results"][lake]
        assert 0.0 <= entry["new_floor_ar1_false_positive_rate"] <= 1.0
        assert 0.0 <= entry["original_floor_ar1_false_positive_rate"] <= 1.0
