"""Tests for H-B3-1p: symmetric classical-peak-selection rule recomputation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location("chernoff_1p_run", HERE / "run.py")
symmetric = importlib.util.module_from_spec(_SPEC)
sys.modules["chernoff_1p_run"] = symmetric
_SPEC.loader.exec_module(symmetric)


@pytest.fixture(scope="module")
def cached_result():
    return symmetric.cmd_run()


def test_negative_controls_unchanged_under_symmetric_rule(cached_result):
    """Windermere and Loch Leven already used the symmetric 'earliest of two' rule in
    H-B3-1l -- recomputing them here must reproduce EXACTLY the same stored values, not a
    coincidentally close number. This is the experiment's own internal consistency check."""
    checks = cached_result["negative_controls_consistency_check"]
    assert checks["windermere"]["match"] is True
    assert checks["loch_leven"]["match"] is True


def test_lower_zurich_classical_peak_becomes_ac1_under_symmetric_rule(cached_result):
    """The pearl's own falsifiable prediction: under the symmetric rule,
    classical_peak_date_used should become AC1's peak date (1999.25), not var's (2004.67)."""
    lz = cached_result["results"]["lower_zurich"]
    assert lz["classical_peak_date_used_symmetric"] == pytest.approx(1999.25, abs=1e-6)
    assert lz["classical_ac1_peak_date"] == pytest.approx(1999.25, abs=1e-6)


def test_tda_is_later_than_classical_under_symmetric_rule(cached_result):
    lz = cached_result["results"]["lower_zurich"]
    assert lz["tda_betti_peak_date"] > lz["classical_peak_date_used_symmetric"]
    assert lz["peak_lead_months_tda_minus_classical_symmetric"] < 0


def test_verdict_inverts_from_confirmed_to_rejected(cached_result):
    assert cached_result["original_verdict_h_b3_1l"] == "CONFIRMED"
    assert cached_result["verdict_under_symmetric_rule"] == "REJECTED"
    assert cached_result["verdict_inverted"] is True


def test_pearl_prediction_confirmed_flag_matches_the_actual_numbers(cached_result):
    """Cross-check the boolean flag itself against the raw numbers it's derived from, so a
    future edit to cmd_run() can't silently desync the flag from reality."""
    lz = cached_result["results"]["lower_zurich"]
    expected = (
        lz["classical_peak_date_used_symmetric"] == pytest.approx(1999.25, abs=1e-6)
        and lz["tda_betti_peak_date"] > lz["classical_peak_date_used_symmetric"]
        and cached_result["verdict_under_symmetric_rule"] == "REJECTED"
    )
    assert cached_result["pearl_prediction_confirmed"] == expected


def test_transition_still_recorded_for_lower_zurich_even_though_unused_for_selection(
    cached_result,
):
    """The documented transition date must still be present in the output (used for the
    distance-to-transition diagnostic columns) even though it's no longer used to SELECT
    which classical statistic wins -- losing it entirely would be a silent regression."""
    lz = cached_result["results"]["lower_zurich"]
    assert lz["documented_transition"] == pytest.approx(2002.0, abs=1e-6)
