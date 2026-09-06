"""Tests for H-B3-1g's new TDA invariant (total persistence) and its threading through the
shared surrogate-null machinery. Written BEFORE the real 9-series run.
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


def test_total_persistence_is_nonnegative():
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, 60)
    series = obrien.betti1_total_persistence_series(x, window=20)
    valid = series[~np.isnan(series)]
    assert np.all(valid >= 0)


def test_total_persistence_differs_from_entropy_in_general():
    """Sanity: the two invariants should NOT be simply rescaled copies of each other (they
    capture different aspects -- shape vs magnitude of the persistence diagram)."""
    rng = np.random.default_rng(1)
    x = np.sin(np.linspace(0, 20, 80)) + rng.normal(0, 0.3, 80)
    entropy_series = obrien.betti1_entropy_series(x, window=30)
    total_series = obrien.betti1_total_persistence_series(x, window=30)
    valid = ~np.isnan(entropy_series) & ~np.isnan(total_series)
    # if they were perfectly rank-correlated in this case that's fine, but they must not be
    # numerically identical (that would mean the new function is a no-op copy of the old one)
    assert not np.allclose(entropy_series[valid], total_series[valid])


def test_surrogate_null_curve_accepts_tda_stat_fn_override():
    rng_seed = 2
    x = np.random.default_rng(rng_seed).normal(0, 1, 60)
    window = 20
    curve_entropy = obrien.surrogate_null_curve(
        x, window, "betti", reps=3, seed=rng_seed, tda_stat_fn=obrien.betti1_entropy_series
    )
    curve_total = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        tda_stat_fn=obrien.betti1_total_persistence_series,
    )
    assert curve_entropy.shape == curve_total.shape
    valid = ~np.isnan(curve_entropy) & ~np.isnan(curve_total)
    assert not np.allclose(curve_entropy[valid], curve_total[valid])


def test_v1_analyze_series_accepts_tda_stat_fn_override():
    rng = np.random.default_rng(3)
    x = np.sin(np.linspace(0, 10, 60)) + rng.normal(0, 0.2, 60)
    t_axis = np.arange(60, dtype=float)
    result = v1.analyze_series(
        x, window=30, time_axis=t_axis, tda_stat_fn=obrien.betti1_total_persistence_series
    )
    assert "tda_betti_crossing" in result
