"""Tests for H-B3-1j's new TDA statistic (diagram-to-baseline-diagram distance) and its
threading through the shared surrogate-null machinery. Written BEFORE the real 9-series run.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_OBRIEN_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-may1972-tda-ews-obrienlakes"
)
_SPEC = importlib.util.spec_from_file_location("obrien_run", _OBRIEN_DIR / "run.py")
obrien = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(obrien)

_V1_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-lakes-tda-ews-surrogate-null-v1"
)
_SPEC_V1 = importlib.util.spec_from_file_location("v1_run", _V1_DIR / "run.py")
v1 = importlib.util.module_from_spec(_SPEC_V1)
_SPEC_V1.loader.exec_module(v1)

_PETER_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-may1972-tda-ews-peterlake"
)
_SPEC_PETER = importlib.util.spec_from_file_location("peterlake_run", _PETER_DIR / "run.py")
peter = importlib.util.module_from_spec(_SPEC_PETER)
_SPEC_PETER.loader.exec_module(peter)


def test_diagram_distance_is_nonnegative_and_zero_at_reference():
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, 60)
    series = obrien.betti1_diagram_distance_series(x, window=20)
    valid = series[~np.isnan(series)]
    assert np.all(valid >= 0)
    # the first valid window is its OWN reference -- distance to itself must be exactly 0
    first_valid_idx = np.where(~np.isnan(series))[0][0]
    assert series[first_valid_idx] == 0.0


def test_diagram_distance_differs_from_scalar_summaries():
    """Sanity: a genuinely different statistic family should not be a rescaled copy of either
    prior invariant."""
    rng = np.random.default_rng(1)
    x = np.sin(np.linspace(0, 20, 80)) + rng.normal(0, 0.3, 80)
    entropy_series = obrien.betti1_entropy_series(x, window=30)
    total_series = obrien.betti1_total_persistence_series(x, window=30)
    distance_series = obrien.betti1_diagram_distance_series(x, window=30)
    valid = ~np.isnan(entropy_series) & ~np.isnan(total_series) & ~np.isnan(distance_series)
    assert not np.allclose(entropy_series[valid], distance_series[valid])
    assert not np.allclose(total_series[valid], distance_series[valid])


def test_bottleneck_metric_option_differs_from_wasserstein():
    rng = np.random.default_rng(2)
    x = np.sin(np.linspace(0, 15, 70)) + rng.normal(0, 0.25, 70)
    wasserstein_series = obrien.betti1_diagram_distance_series(x, window=25, metric="wasserstein")
    bottleneck_series = obrien.betti1_diagram_distance_series(x, window=25, metric="bottleneck")
    valid = ~np.isnan(wasserstein_series) & ~np.isnan(bottleneck_series)
    # both are legitimate distances (non-negative), but should not be numerically identical
    assert np.all(wasserstein_series[valid] >= 0)
    assert np.all(bottleneck_series[valid] >= 0)
    assert not np.allclose(wasserstein_series[valid], bottleneck_series[valid])


def test_surrogate_null_curve_accepts_diagram_distance_tda_stat_fn():
    rng_seed = 3
    x = np.random.default_rng(rng_seed).normal(0, 1, 60)
    window = 20
    curve = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        tda_stat_fn=obrien.betti1_diagram_distance_series,
    )
    assert curve.shape[0] == len(x) - window + 1
    assert np.any(~np.isnan(curve))


def test_v1_analyze_series_accepts_diagram_distance_override():
    rng = np.random.default_rng(4)
    x = np.sin(np.linspace(0, 10, 60)) + rng.normal(0, 0.2, 60)
    t_axis = np.arange(60, dtype=float)
    result = v1.analyze_series(
        x, window=30, time_axis=t_axis, tda_stat_fn=obrien.betti1_diagram_distance_series
    )
    assert "tda_betti_crossing" in result


def test_diagram_distance_on_real_peter_dosat_data_does_not_crash():
    """Reviewer-flagged gap (code review of the H-B3-1j commit): the 5 tests above only exercise
    the new statistic on synthetic sine+noise data; the real 9-series numbers in
    metrics/run.json were verified only by manual re-derivation, not a regression test. This
    threads the real Peter doSat series (the one whose lead is this experiment's headline
    finding) through the actual pipeline functions with a SMALL rep count (2, not the real run's
    20) -- fast enough for the unit suite, still catches real-data wiring/shape bugs a
    synthetic-only test could miss."""
    _season_time, x, _transition_time = peter.load_daily_series("doSat", "Peter")
    n = len(x)
    window = round(obrien.WINDOW_FRAC * n)
    window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)

    stat = obrien.betti1_diagram_distance_series(x, window)
    assert stat.shape[0] == n - window + 1
    assert np.any(~np.isnan(stat))

    tau = obrien.expanding_kendall_tau(stat)
    null_curve = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=2,
        seed=0,
        tda_stat_fn=obrien.betti1_diagram_distance_series,
    )
    assert null_curve.shape == tau.shape
    # crossing may or may not occur with only 2 surrogate reps -- this test checks the pipeline
    # runs end-to-end on real data without error, not a specific crossing outcome
    obrien.surrogate_crossing(tau, null_curve)
