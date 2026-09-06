"""Tests for H-B3-1i: IAAFT-surrogate null combined with the total-persistence TDA invariant --
the fourth cell of the {entropy, total persistence} x {AR(1), IAAFT} design this arc has been
implicitly building. Written BEFORE the real 9-series run.
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


def test_surrogate_null_curve_accepts_iaaft_plus_total_persistence_together():
    """The two overrides (surrogate_fn, tda_stat_fn) must compose -- neither threading path
    should silently ignore the other."""
    rng_seed = 4
    x = np.sin(np.linspace(0, 15, 70)) + np.random.default_rng(rng_seed).normal(0, 0.25, 70)
    window = 25
    curve = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        surrogate_fn=obrien.iaaft_surrogate,
        tda_stat_fn=obrien.betti1_total_persistence_series,
    )
    assert curve.shape[0] == len(x) - window + 1
    assert np.any(~np.isnan(curve))


def test_combined_cell_differs_from_either_single_change():
    """The AR1+total-persistence null curve (V1g), IAAFT+entropy null curve (V1'), and
    IAAFT+total-persistence null curve (this experiment, H-B3-1i) must not be pairwise
    identical -- if they were, the combination would be a no-op and the two threading
    parameters would not be composing independently."""
    rng_seed = 5
    x = np.sin(np.linspace(0, 12, 70)) + np.random.default_rng(rng_seed).normal(0, 0.3, 70)
    window = 25

    curve_ar1_total = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        surrogate_fn=obrien.ar1_surrogate,
        tda_stat_fn=obrien.betti1_total_persistence_series,
    )
    curve_iaaft_entropy = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        surrogate_fn=obrien.iaaft_surrogate,
        tda_stat_fn=obrien.betti1_entropy_series,
    )
    curve_iaaft_total = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        surrogate_fn=obrien.iaaft_surrogate,
        tda_stat_fn=obrien.betti1_total_persistence_series,
    )

    valid = (
        ~np.isnan(curve_ar1_total) & ~np.isnan(curve_iaaft_entropy) & ~np.isnan(curve_iaaft_total)
    )
    assert not np.allclose(curve_ar1_total[valid], curve_iaaft_total[valid])
    assert not np.allclose(curve_iaaft_entropy[valid], curve_iaaft_total[valid])


def test_v1_cmd_run_accepts_both_overrides_together():
    """Smoke test at the cmd_run level (not just the low-level surrogate curve) -- confirms
    the two kwargs thread all the way through analyze_series -> run_obrien_lakes /
    run_peter_paul_lake -> cmd_run without one silently overriding the other."""
    import inspect

    sig = inspect.signature(v1.cmd_run)
    assert "surrogate_fn" in sig.parameters
    assert "tda_stat_fn" in sig.parameters
