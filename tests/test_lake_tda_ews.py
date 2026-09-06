"""Harness sanity for experiments/20260906-may1972-tda-ews-obrienlakes/run.py.

NOT the scientific controls (those are the two negative-control lakes inside run.py itself).
These check the pipeline's own arithmetic: embedding shape, rolling-stat correctness, tau
threshold-crossing logic, ICE gap-exclusion -- on tiny synthetic series with hand-computable
answers, and on the real Lower Zurich series for the gap-exclusion regression documented in
decision.md.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest

_SPEC = importlib.util.spec_from_file_location(
    "lake_tda_ews",
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-may1972-tda-ews-obrienlakes"
    / "run.py",
)
mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mod)


def test_takens_embed_shape_and_values():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    cloud = mod.takens_embed(x, dim=3, delay=1)
    assert cloud.shape == (3, 3)
    assert np.array_equal(cloud[0], [1.0, 2.0, 3.0])
    assert np.array_equal(cloud[-1], [3.0, 4.0, 5.0])


def test_takens_embed_too_short_raises():
    with pytest.raises(ValueError, match="too short"):
        mod.takens_embed(np.array([1.0, 2.0]), dim=3, delay=1)


def test_rolling_var_hand_computed():
    x = np.array([1.0, 2.0, 3.0, 4.0, 10.0])
    out = mod.rolling_stat(x, window=3, kind="var")
    assert out[0] == pytest.approx(np.var([1.0, 2.0, 3.0], ddof=1))
    assert out[-1] == pytest.approx(np.var([3.0, 4.0, 10.0], ddof=1))


def test_expanding_kendall_tau_perfect_increasing_series():
    # A perfectly monotone increasing statistic should reach tau=1.0 as soon as enough points exist.
    stat = np.arange(20.0)
    tau = mod.expanding_kendall_tau(stat, min_points=5)
    assert np.isnan(tau[:4]).all()
    assert tau[4:] == pytest.approx(1.0)


def test_first_crossing_finds_first_index_above_threshold():
    tau = np.array([np.nan, 0.1, 0.3, 0.6, 0.9])
    assert mod.first_crossing(tau, threshold=0.5) == 3
    assert mod.first_crossing(np.array([0.1, 0.2]), threshold=0.5) is None


def test_ice_gap_exclusion_keeps_longest_contiguous_run():
    # Regression: Lower Zurich has 3 real gaps > 2x median monthly spacing; the pipeline must
    # keep the LONGEST contiguous run, not silently bridge or use the whole (gappy) series.
    dates, pca1 = mod.load_series(mod.pyreadr.read_r(str(mod.DATA)), "lower_zurich")
    assert dates[0] == pytest.approx(1991.6666666666667, abs=1e-6)
    assert dates[-1] == pytest.approx(2005.0, abs=1e-6)
    assert len(dates) == len(pca1) == 161
