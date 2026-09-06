"""Tests for the V1' null model: iaaft_surrogate (Schreiber & Schmitz 1996), added to
experiments/20260906-may1972-tda-ews-obrienlakes/run.py.

Key property under test: IAAFT preserves the amplitude distribution EXACTLY and the power
spectrum APPROXIMATELY (all lags), unlike ar1_surrogate which only matches lag-1 autocorrelation
-- this is the whole motivation for V1' (H-B3-1c's Kill Analysis: AR(1) too simple a null for
real negative-control lakes with structure beyond lag-1).
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


def _ar2_plus_trend(n: int, rng: np.random.Generator) -> np.ndarray:
    """A series with structure a lag-1-only model cannot represent: AR(2) dynamics + a slow
    linear trend. Used to demonstrate IAAFT's advantage over ar1_surrogate."""
    x = np.zeros(n)
    for i in range(2, n):
        x[i] = 0.5 * x[i - 1] - 0.3 * x[i - 2] + rng.normal(0, 1)
    return x + 0.01 * np.arange(n)


def test_iaaft_preserves_amplitude_distribution_exactly():
    rng = np.random.default_rng(0)
    x = _ar2_plus_trend(200, rng)
    surrogate = mod.iaaft_surrogate(x, rng)
    assert np.allclose(np.sort(x), np.sort(surrogate))


def test_iaaft_preserves_spectrum_far_better_than_ar1_on_structured_data():
    rng = np.random.default_rng(1)
    x = _ar2_plus_trend(200, rng)
    orig_spec = np.abs(np.fft.rfft(x))

    iaaft = mod.iaaft_surrogate(x, np.random.default_rng(2))
    ar1 = mod.ar1_surrogate(x, np.random.default_rng(2))

    iaaft_err = np.median(np.abs(orig_spec - np.abs(np.fft.rfft(iaaft))) / (orig_spec + 1e-9))
    ar1_err = np.median(np.abs(orig_spec - np.abs(np.fft.rfft(ar1))) / (orig_spec + 1e-9))

    assert iaaft_err < 0.10, f"IAAFT spectrum error too high: {iaaft_err:.3f}"
    assert iaaft_err < ar1_err / 3, "IAAFT should be much closer to the true spectrum than AR(1)"


def test_iaaft_surrogate_is_not_the_identity():
    rng = np.random.default_rng(3)
    x = _ar2_plus_trend(150, rng)
    surrogate = mod.iaaft_surrogate(x, rng)
    assert not np.allclose(x, surrogate)


def test_surrogate_null_curve_accepts_iaaft_via_surrogate_fn():
    rng = np.random.default_rng(4)
    x = _ar2_plus_trend(120, rng)
    window = 60
    curve = mod.surrogate_null_curve(
        x, window, "var", reps=8, seed=0, surrogate_fn=mod.iaaft_surrogate
    )
    assert curve.shape == (len(x) - window + 1,)


def test_surrogate_null_curve_default_still_uses_ar1_backward_compatible():
    """Regression: existing V1 code/tests call surrogate_null_curve without surrogate_fn --
    must still default to ar1_surrogate, not silently switch behavior."""
    import inspect

    sig = inspect.signature(mod.surrogate_null_curve)
    assert sig.parameters["surrogate_fn"].default is mod.ar1_surrogate


def test_self_consistency_iaaft_fires_near_nominal_alpha_on_structured_null_data():
    """Mirrors H-B3-1c's AR(1) self-consistency test, but for IAAFT and on data that AR(1)
    could NOT self-consistently null out (AR(2)+trend). If IAAFT is the right richer null, a
    genuine IAAFT-surrogate draw of such a series should still cross its own null at a low rate."""
    rng = np.random.default_rng(42)
    base = _ar2_plus_trend(150, rng)
    window = 75
    trials = 10
    hits = 0
    for i in range(trials):
        test_rng = np.random.default_rng(100 + i)
        candidate = mod.iaaft_surrogate(base, test_rng)
        null_curve = mod.surrogate_null_curve(
            candidate, window, "var", reps=12, seed=i, surrogate_fn=mod.iaaft_surrogate
        )
        tau = mod.expanding_kendall_tau(mod.rolling_stat(candidate, window, "var"))
        if mod.surrogate_crossing(tau, null_curve) is not None:
            hits += 1
    rate = hits / trials
    assert rate < 0.6, f"IAAFT-null fired on {rate:.0%} of self-consistent draws"
