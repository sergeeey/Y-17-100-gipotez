"""Tests for H-B3-1r -- per-season robustness check on H-B3-1q's own pooled coherence pattern."""

import importlib.util
import json
from pathlib import Path

import pytest

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def run_module():
    return _load_module("h_b3_1r_run_under_test", EXPERIMENT_DIR / "run.py")


@pytest.fixture(scope="module")
def metrics_data():
    path = EXPERIMENT_DIR / "metrics" / "run.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_verdict_is_rejected_for_season_robustness(metrics_data):
    assert metrics_data["verdict"] == "REJECTED-FOR-SEASON-ROBUSTNESS"
    assert metrics_data["all_seasons_show_peter_more_consistent"] is False
    assert metrics_data["pattern_strengthens_toward_2010"] is False


def test_2008_ties_rather_than_favoring_peter(metrics_data):
    v = metrics_data["season_verdicts"]["2008"]
    assert v["peter_n_positive"] == v["paul_n_positive"]
    assert v["peter_more_consistent"] is False


def test_2009_matches_h_b3_1q_pooled_pattern(metrics_data):
    v = metrics_data["season_verdicts"]["2009"]
    assert v["peter_n_positive"] == 3
    assert v["peter_more_consistent"] is True


def test_2010_weaker_than_2009_not_stronger(metrics_data):
    """The key robustness failure: the documented transition-completion year (2010) shows a
    LOWER Peter positive-count than 2009, not a higher one -- opposite of the intensification
    a genuine tracking signal should show."""
    v2009 = metrics_data["season_verdicts"]["2009"]
    v2010 = metrics_data["season_verdicts"]["2010"]
    assert v2010["peter_n_positive"] < v2009["peter_n_positive"]


def test_all_three_seasons_present(metrics_data):
    assert set(metrics_data["season_verdicts"].keys()) == {"2008", "2009", "2010"}
    assert set(metrics_data["per_season_results"].keys()) == {"2008", "2009", "2010"}


def test_each_season_has_both_lakes_and_three_pairs(metrics_data):
    for year_data in metrics_data["per_season_results"].values():
        assert set(year_data.keys()) == {"Peter", "Paul"}
        for lake_data in year_data.values():
            assert len(lake_data["pairs"]) == 3


def test_daily_series_for_season_only_returns_requested_year(run_module):
    """Sanity check: the per-season loader must not silently leak data from adjacent years."""
    x_2008 = run_module.daily_series_for_season("pH", "Peter", 2008)
    x_2009 = run_module.daily_series_for_season("pH", "Peter", 2009)
    assert len(x_2008) > 0
    assert len(x_2009) > 0
    # 2008 is a shorter field season than 2009/2010 in this dataset (partial first year)
    assert len(x_2008) != len(x_2009) or len(x_2008) < 120


def test_2009_correlations_match_committed_values(metrics_data):
    pairs = {
        (r["var1"], r["var2"]): r
        for r in metrics_data["per_season_results"]["2009"]["Peter"]["pairs"]
    }
    assert pairs[("chl", "pH")]["rho"] == pytest.approx(0.8402, abs=0.001)
    assert pairs[("pH", "doSat")]["rho"] == pytest.approx(0.7469, abs=0.001)
