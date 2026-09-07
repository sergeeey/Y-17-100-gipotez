"""Tests for the Peter lake within-lake variable comparison (H-B3-1h decision.md Addendum 5) --
the out-of-sample replicate of the Paul lake comparison (Addendum 3)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_MOD_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-lakes-tda-ews-invariant-conjunction"
)
_SPEC = importlib.util.spec_from_file_location(
    "peter_lake_variable_comparison", _MOD_DIR / "peter_lake_variable_comparison.py"
)
mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mod)


def test_reuses_paul_lakes_analyze_function_unchanged():
    """Minimal Relaxation Rule check: this experiment should reuse `analyze` verbatim (only the
    lake name argument changes), not reimplement it."""
    assert mod.analyze is mod.paul_mod.analyze


def test_real_peter_lake_comparison_runs_and_reports_expected_shape():
    """Smoke test against the real data file -- confirms all 3 variables load and the documented
    finding (decision.md Addendum 5: pH has the strongest trend AND the lowest ACF lag-1 is NOT
    the pattern here -- pH has the HIGHEST ACF lag-1, matching its role as the most persistent,
    least noisy variable, consistent with it also having the strongest trend)."""
    result = mod.main()
    per_var = result["per_variable"]
    assert set(per_var.keys()) == {"chl", "pH", "doSat"}
    # Regression guard on the already-verified, documented finding (decision.md Addendum 5):
    # pH has the strongest trend magnitude of all 3 Peter lake variables.
    trend_by_var = {v: abs(per_var[v]["spearman_trend_rho"]) for v in per_var}
    assert max(trend_by_var, key=trend_by_var.get) == "pH"
    # And the highest lag-1 autocorrelation (opposite ranking from Paul lake's doSat/pH roles --
    # a genuinely different lake, not a mechanical copy of the same numbers).
    acf1_by_var = {v: per_var[v]["acf_lag1_3"][0] for v in per_var}
    assert max(acf1_by_var, key=acf1_by_var.get) == "pH"
