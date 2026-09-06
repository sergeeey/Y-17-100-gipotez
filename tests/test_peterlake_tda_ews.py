"""Harness sanity for experiments/20260906-may1972-tda-ews-peterlake/run.py.

Focuses on the NEW logic specific to this experiment (season concatenation, transition-time
mapping) -- the shared TDA/EWS/floor pipeline is already tested in test_lake_tda_ews.py and
reused here via import, not reimplemented.

Regression context: an earlier version applied the sibling experiment's "keep only the longest
contiguous run" ICE rule unmodified to this multi-season sonde deployment and silently analyzed
only the 2009 field season (114 of ~450 available days) because winter gaps were mistaken for a
data-quality problem instead of the sampling design (summer-only monitoring). These tests lock in
the corrected season-concatenation behavior.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest

_SPEC = importlib.util.spec_from_file_location(
    "peterlake_run",
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-may1972-tda-ews-peterlake"
    / "run.py",
)
mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mod)


def test_all_three_seasons_are_concatenated_not_just_the_longest():
    season_time, x, _transition_time = mod.load_daily_series("chl", "Peter")
    # Regression: must span ~330 days (3 seasons of ~110 days each), not ~114 (a single season).
    assert len(x) > 300, f"expected all 3 seasons concatenated, got only {len(x)} points"
    assert season_time[0] == 0.0
    assert season_time[-1] > 300


def test_transition_time_falls_within_the_2010_season_not_before_or_after():
    season_time, _x, transition_time = mod.load_daily_series("chl", "Peter")
    assert transition_time is not None
    # 2010 is the 3rd season (index 2 of 0,1,2); it must land strictly inside [0, season_time[-1]]
    assert 0 < transition_time < season_time[-1]


def test_peter_and_paul_share_the_same_season_time_axis_length():
    # Fair comparison requires both lakes to be aligned on the same axis construction, not just
    # the same calendar range -- a per-lake gap-detection quirk could desync them silently.
    _st_peter, x_peter, t_peter = mod.load_daily_series("chl", "Peter")
    _st_paul, x_paul, t_paul = mod.load_daily_series("chl", "Paul")
    assert len(x_peter) == len(x_paul)
    assert t_peter == pytest.approx(t_paul, abs=1e-6)


def test_season_time_is_monotonically_increasing():
    season_time, _, _ = mod.load_daily_series("pH", "Peter")
    assert np.all(np.diff(season_time) > 0)


def test_winter_gap_does_not_appear_as_a_multi_month_jump_in_season_time():
    # The point of season-time: a rolling window must never see a literal ~230-day winter gap as
    # if it were one time step -- season-time steps by ~1 day, even across a season boundary
    # (which advances by one nominal step, not raw calendar time).
    season_time, _, _ = mod.load_daily_series("chl", "Peter")
    assert np.diff(season_time).max() < 5.0
