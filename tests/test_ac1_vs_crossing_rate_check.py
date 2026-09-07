"""Tests for the population-wide AC1-vs-crossing-rate check (H-B3-1h decision.md Addendum 4)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_MOD_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-lakes-tda-ews-invariant-conjunction"
)
_SPEC = importlib.util.spec_from_file_location(
    "ac1_vs_crossing_rate_check", _MOD_DIR / "ac1_vs_crossing_rate_check.py"
)
mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mod)


def test_acf_lag1_helper_matches_known_ar1_coefficient():
    rng = np.random.default_rng(0)
    phi = 0.6
    n = 5000
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + rng.normal(0, 1)
    assert abs(mod.acf_lag1(x) - phi) < 0.03


def test_real_check_runs_and_reports_all_nine_series():
    result = mod.main()
    assert set(result["per_series"].keys()) == set(mod.CROSSING_RATE_OUT_OF_7.keys())
    # Regression guard on the documented, already-verified result direction (decision.md
    # Addendum 4): direction negative, not statistically significant at n=9.
    assert result["spearman_rho_ac1_vs_crossing_rate"] < 0
    assert result["spearman_p"] > 0.05
    assert result["prediction_confirmed"] is False
