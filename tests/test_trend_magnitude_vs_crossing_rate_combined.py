"""Tests for the pooled trend-magnitude/AC1 vs crossing-rate check (H-B3-1h decision.md
Addendum 5) -- combines Paul lake's and Peter lake's own within-lake comparisons."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_MOD_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-lakes-tda-ews-invariant-conjunction"
)
_SPEC = importlib.util.spec_from_file_location(
    "trend_magnitude_combined", _MOD_DIR / "trend_magnitude_vs_crossing_rate_combined.py"
)
mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mod)


def test_pools_exactly_six_series_from_both_lakes():
    result = mod.main()
    assert set(result["per_series"].keys()) == {
        "Paul_chl",
        "Paul_pH",
        "Paul_doSat",
        "Peter_chl",
        "Peter_pH",
        "Peter_doSat",
    }


def test_crossing_rate_values_match_the_committed_cross_tabulation():
    """Regression guard: CROSSING_RATE hardcoded values must match the already-verified
    cross-tabulation in decision.md's CORRECTION ADDENDUM, not be re-typed incorrectly."""
    assert mod.CROSSING_RATE == {
        "Paul_chl": 3,
        "Paul_pH": 3,
        "Paul_doSat": 7,
        "Peter_chl": 6,
        "Peter_pH": 4,
        "Peter_doSat": 6,
    }


def test_both_correlations_are_not_statistically_significant_at_n6():
    """Regression guard on the already-documented, honest result (decision.md Addendum 5): with
    only 6 data points pooling both lakes, neither correlation reaches significance -- this test
    protects against silently reporting a false positive on a future data change."""
    result = mod.main()
    assert result["trend_vs_crossing_rate"]["confirmed_at_0.05"] is False
    assert result["ac1_vs_crossing_rate_pooled_6"]["confirmed_at_0.05"] is False
