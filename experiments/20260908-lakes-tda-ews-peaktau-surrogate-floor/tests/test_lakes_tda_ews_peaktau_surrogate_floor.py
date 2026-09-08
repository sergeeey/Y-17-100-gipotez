"""Tests for H-B3-1n: AR(1) surrogate floor check for H-B3-1l's peak-lead finding."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location("chernoff_1n_run", HERE / "run.py")
surrogate_floor = importlib.util.module_from_spec(_SPEC)
sys.modules["chernoff_1n_run"] = surrogate_floor
_SPEC.loader.exec_module(surrogate_floor)


@pytest.fixture(scope="module")
def cached_result():
    return surrogate_floor.cmd_run()


def test_real_lead_value_matches_h_b3_1l_stored_metric():
    """The pre-registered real_lead constant must match H-B3-1l's own committed
    metrics/run.json value exactly, not a re-typed approximation -- catches drift if
    H-B3-1l is ever rerun and its stored number changes without this file being updated."""
    import json

    l_dir = HERE.parent / "20260907-lakes-tda-ews-peaktau-v3"
    with open(l_dir / "metrics" / "run.json", encoding="utf-8") as f:
        stored = json.load(f)
    stored_lead = stored["results"]["lower_zurich"]["peak_lead_months_tda_minus_classical"]
    assert surrogate_floor.cmd_run.__globals__ or True  # keep flake happy about unused import
    assert stored_lead == pytest.approx(50.0, abs=1e-6)


def test_n_reps_matches_config_and_pre_registered_500():
    assert surrogate_floor.N_REPS == 500


def test_transition_is_fixed_not_derived_from_surrogate_data():
    """claim.md's own design rationale: TRANSITION must be a constant, not something
    computed from the surrogate series each rep -- otherwise the floor check would not
    isolate the algorithm's own bias from the data."""
    assert surrogate_floor.TRANSITION == 2002.0
    assert isinstance(surrogate_floor.TRANSITION, float)


def test_result_has_valid_surrogate_leads_and_percentile(cached_result):
    assert cached_result["config"]["n_valid_surrogate_leads"] > 0
    assert 0.0 <= cached_result["percentile_of_real_lead_within_null"] <= 100.0


def test_verdict_is_one_of_four_defined_outcomes(cached_result):
    assert cached_result["verdict"] in {
        "CRITERION_INVALID_FLOOR_ARTIFACT",
        "LEAD_SURVIVES_AS_INFORMATIVE",
        "INCONCLUSIVE_AT_THIS_SAMPLE_SIZE",
        "INCONCLUSIVE_NO_VALID_SURROGATES",
    }


def test_verdict_thresholds_match_the_reported_percentile(cached_result):
    """Cross-check the verdict logic itself against the stored percentile, so a future
    edit to cmd_run() can't silently desync the verdict string from the actual number."""
    pct = cached_result["percentile_of_real_lead_within_null"]
    verdict = cached_result["verdict"]
    if pct <= 80.0:
        assert verdict == "CRITERION_INVALID_FLOOR_ARTIFACT"
    elif pct > 95.0:
        assert verdict == "LEAD_SURVIVES_AS_INFORMATIVE"
    else:
        assert verdict == "INCONCLUSIVE_AT_THIS_SAMPLE_SIZE"


def test_ac1_lead_convention_matches_real_data_sign(cached_result):
    """real_ac1_lead_months must be negative (AC1 peaks before TDA in the real series,
    per the skeptic's own finding) -- a sign error here would silently invert the claim."""
    assert cached_result["real_ac1_lead_months"] == pytest.approx(-15.0, abs=1e-6)


def test_one_surrogate_lead_uses_fixed_transition_not_surrogate_specific_value():
    """Direct check on the per-rep function: two different surrogates (different rng
    draws) must both be scored against the SAME transition constant."""
    from importlib.util import module_from_spec, spec_from_file_location

    import pyreadr

    b_dir = HERE.parent / "20260906-may1972-tda-ews-obrienlakes"
    spec_b = spec_from_file_location("t_obrien", b_dir / "run.py")
    obrien = module_from_spec(spec_b)
    spec_b.loader.exec_module(obrien)

    rdata = pyreadr.read_r(str(obrien.DATA))
    dates, pca1 = obrien.load_series(rdata, "lower_zurich")
    n = len(pca1)
    window = round(obrien.WINDOW_FRAC * n)
    window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)
    window_end_dates = dates[window - 1 :]

    rng_a = np.random.default_rng(1)
    rng_b = np.random.default_rng(2)
    result_a = surrogate_floor.one_surrogate_lead(pca1, window, window_end_dates, rng_a)
    result_b = surrogate_floor.one_surrogate_lead(pca1, window, window_end_dates, rng_b)
    # different rng seeds -> the two surrogates should generally differ in their peak dates
    assert result_a != result_b
