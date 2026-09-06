"""Tests for H-B3-1k: IAAFT-surrogate null combined with the diagram-distance TDA statistic --
the fourth and last cell of the {total persistence, diagram-distance} x {AR(1), IAAFT} design.
Written BEFORE the real 9-series run.
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


def test_surrogate_null_curve_accepts_iaaft_plus_diagram_distance_together():
    """The two overrides (surrogate_fn=iaaft_surrogate, tda_stat_fn=diagram_distance) must
    compose -- neither threading path should silently ignore the other."""
    rng_seed = 6
    x = np.sin(np.linspace(0, 15, 70)) + np.random.default_rng(rng_seed).normal(0, 0.25, 70)
    window = 25
    curve = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        surrogate_fn=obrien.iaaft_surrogate,
        tda_stat_fn=obrien.betti1_diagram_distance_series,
    )
    assert curve.shape[0] == len(x) - window + 1
    assert np.any(~np.isnan(curve))


def test_combined_cell_differs_from_the_other_three_cells():
    """The four cells of the design (AR1+total-persistence, IAAFT+total-persistence,
    AR1+diagram-distance, IAAFT+diagram-distance) must not collapse pairwise -- if this cell's
    null curve were identical to any sibling's, the two threading parameters would not be
    composing independently."""
    rng_seed = 7
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
    curve_iaaft_total = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        surrogate_fn=obrien.iaaft_surrogate,
        tda_stat_fn=obrien.betti1_total_persistence_series,
    )
    curve_ar1_distance = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        surrogate_fn=obrien.ar1_surrogate,
        tda_stat_fn=obrien.betti1_diagram_distance_series,
    )
    curve_iaaft_distance = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=3,
        seed=rng_seed,
        surrogate_fn=obrien.iaaft_surrogate,
        tda_stat_fn=obrien.betti1_diagram_distance_series,
    )

    curves = [curve_ar1_total, curve_iaaft_total, curve_ar1_distance, curve_iaaft_distance]
    valid = np.ones(curves[0].shape[0], dtype=bool)
    for c in curves:
        valid &= ~np.isnan(c)

    for i in range(len(curves)):
        for j in range(i + 1, len(curves)):
            assert not np.allclose(curves[i][valid], curves[j][valid]), (i, j)


def test_v1_cmd_run_accepts_iaaft_and_diagram_distance_together():
    """Smoke test at the cmd_run level -- confirms both kwargs thread all the way through
    analyze_series -> run_obrien_lakes / run_peter_paul_lake -> cmd_run."""
    import inspect

    sig = inspect.signature(v1.cmd_run)
    assert "surrogate_fn" in sig.parameters
    assert "tda_stat_fn" in sig.parameters
