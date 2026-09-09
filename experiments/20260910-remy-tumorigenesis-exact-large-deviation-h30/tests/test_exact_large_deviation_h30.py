"""Tests for H-B7-30 -- honest re-assessment of the large-deviation fit on exact probabilities."""

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
    return _load_module("h_b7_30_run_under_test", EXPERIMENT_DIR / "run.py")


@pytest.fixture(scope="module")
def metrics_data():
    path = EXPERIMENT_DIR / "metrics" / "run.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_verdict_is_confirmed_for_hypothesis_b(metrics_data):
    """The honest finding: exactness does NOT rescue the data-geometry limitation."""
    assert metrics_data["verdict"] == "CONFIRMED"
    assert metrics_data["hypothesis_b_geometry_problem_persists_confirmed"] is True
    assert metrics_data["hypothesis_a_exactness_helps_confirmed"] is False


def test_r_squared_essentially_unchanged_from_original_report(metrics_data):
    """r^2 with exact numbers must stay close to the original Monte-Carlo-based r^2=0.8913 --
    if exactness materially helped, this delta would be large."""
    fit = metrics_data["fit_primary_pnr_step"]
    assert fit["r_squared"] == pytest.approx(0.8929, abs=0.001)
    assert abs(metrics_data["delta_r_squared_vs_original_report"]) < 0.05


def test_only_three_distinct_pnr_step_values(metrics_data):
    """Locks in the exact data-geometry limitation the user's own original critique identified --
    exact probabilities do not add new distinct x-values."""
    fit = metrics_data["fit_primary_pnr_step"]
    assert fit["n"] == 4
    assert fit["n_distinct_x"] == 3


def test_alternative_axes_do_not_fit_better_than_pnr_step(metrics_data):
    """Robustness check: neither alternative candidate x-axis beats PNR-step on this sample."""
    fit_pnr = metrics_data["fit_primary_pnr_step"]
    fit_ntrans = metrics_data["fit_alternative_n_transient"]
    fit_esta = metrics_data["fit_alternative_expected_steps_to_absorption"]
    assert fit_ntrans["r_squared"] < fit_pnr["r_squared"]
    assert fit_esta["r_squared"] < fit_pnr["r_squared"]


def test_vast_majority_of_full_domain_is_trivial(metrics_data):
    """36/40 of H-B7-22's own originally-tested k values give exact_escape_probability=1.0 --
    zero log-probability information, regardless of measurement precision."""
    assert metrics_data["n_total_conditions_in_full_h_b7_22_domain"] == 40
    assert metrics_data["n_trivial_conditions_in_full_h_b7_22_domain"] == 36
    assert metrics_data["n_nontrivial_conditions_in_full_h_b7_22_domain"] == 4


def test_per_k_detail_matches_committed_h_b7_28_values(metrics_data):
    expected = {
        1: 0.06886574074074076,
        2: 0.1377314814814815,
        3: 0.18518518518518517,
        4: 0.3333333333333333,
    }
    for entry in metrics_data["per_k_detail"]:
        assert entry["exact_escape_probability"] == pytest.approx(expected[entry["k"]], abs=1e-9)


def test_pnr_step_values_match_committed_h_b7_24_values(metrics_data):
    expected_pnr = {1: 5, 2: 4, 3: 4, 4: 2}
    for entry in metrics_data["per_k_detail"]:
        assert entry["pnr_step"] == expected_pnr[entry["k"]]


def test_linreg_helper_produces_perfect_fit_on_a_perfect_line(run_module):
    """Sanity check on the linreg implementation itself, independent of any project data."""
    xs = [1.0, 2.0, 3.0, 4.0]
    ys = [2.0, 4.0, 6.0, 8.0]  # y = 2x exactly
    result = run_module.linreg(xs, ys)
    assert result["r_squared"] == pytest.approx(1.0, abs=1e-9)
    assert result["slope"] == pytest.approx(2.0, abs=1e-9)
    assert result["n_distinct_x"] == 4


def test_linreg_helper_detects_a_weak_fit(run_module):
    """Sanity check: linreg must actually be able to report a LOW r^2, not always near-perfect."""
    xs = [1.0, 2.0, 3.0, 4.0]
    ys = [5.0, 1.0, 8.0, 2.0]  # no real linear relationship
    result = run_module.linreg(xs, ys)
    assert result["r_squared"] < 0.3
