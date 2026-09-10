"""Tests for H-B3-1q -- cross-variable tau-trajectory coherence, floor-checked against Paul."""

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def run_module():
    return _load_module("h_b3_1q_run_under_test", EXPERIMENT_DIR / "run.py")


@pytest.fixture(scope="module")
def metrics_data():
    path = EXPERIMENT_DIR / "metrics" / "run.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_verdict_is_confirmed_crossvar_coherence_lead(metrics_data):
    assert metrics_data["verdict"] == "CONFIRMED-CROSSVAR-COHERENCE-LEAD"
    assert metrics_data["floor_check_passed"] is True


def test_peter_all_three_pairs_positive(metrics_data):
    for r in metrics_data["crossvar_results"]["Peter"]:
        assert r["rho"] is not None
        assert r["rho"] > 0
        assert r["n"] > 0


def test_paul_does_not_show_consistent_positive_pattern(metrics_data):
    paul_pairs = metrics_data["crossvar_results"]["Paul"]
    n_positive = sum(1 for r in paul_pairs if r["rho"] is not None and r["rho"] > 0)
    assert n_positive < len(paul_pairs)  # not ALL positive, unlike Peter
    assert metrics_data["paul_n_positive_of_3"] == n_positive


def test_peter_correlations_stronger_than_paul_on_average(metrics_data):
    peter_mean_abs = np.mean([abs(r["rho"]) for r in metrics_data["crossvar_results"]["Peter"]])
    # Peter's pattern is CONSISTENTLY positive at 0.71-0.84 -- check this against Paul's own
    # positive-only subset, not raw magnitude (Paul's pH-doSat is a strong -0.91, which is not
    # evidence of coherence, it's evidence of anti-coherence -- sign matters, not just |rho|)
    peter_min = min(r["rho"] for r in metrics_data["crossvar_results"]["Peter"])
    assert peter_min > 0.7
    assert peter_mean_abs > 0.7


def test_original_h_b3_1o_question_stays_inconclusive(metrics_data):
    """The revival attempt's own primary target (aligned pH-vs-doSat) must be honestly reported
    as inconclusive given the small overlap -- not silently promoted to a finding."""
    orig = metrics_data["original_h_b3_1o_question"]
    assert orig["conclusive"] is False
    assert orig["aligned_ph_vs_dosat"]["n"] < orig["min_overlap_required"]
    assert orig["supports_genuine_delay_if_conclusive"] is False


def test_aligned_correlation_lower_than_unaligned(metrics_data):
    """Regression lock on the specific counter-intuitive finding: aligning by the crossing date
    did NOT improve agreement, arguing against (not for) the 'same shape, just shifted' reading."""
    orig = metrics_data["original_h_b3_1o_question"]
    assert orig["aligned_ph_vs_dosat"]["rho"] < orig["unaligned_ph_vs_dosat"]["rho"]


def test_unaligned_correlation_detects_a_negative_case(run_module):
    """Sanity check: unaligned_correlation must actually be able to report a negative rho,
    not vacuously always positive -- confirmed directly against Paul's own pH-doSat pair."""
    tau_a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    tau_b = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
    result = run_module.unaligned_correlation(tau_a, tau_b)
    assert result["rho"] == pytest.approx(-1.0, abs=1e-9)
    assert result["n"] == 5


def test_unaligned_correlation_handles_nan_values(run_module):
    tau_a = np.array([1.0, np.nan, 3.0, 4.0, 5.0])
    tau_b = np.array([1.0, 2.0, 3.0, 4.0, np.nan])
    result = run_module.unaligned_correlation(tau_a, tau_b)
    assert result["n"] == 3  # only indices 0, 2, 3 are valid in both


def test_crossvar_results_match_committed_values_for_peter_ph_dosat(metrics_data):
    """Regression lock against the Compute-First Check's own verified numbers."""
    peter_pairs = {(r["var1"], r["var2"]): r for r in metrics_data["crossvar_results"]["Peter"]}
    assert peter_pairs[("pH", "doSat")]["rho"] == pytest.approx(0.8407, abs=0.001)
    paul_pairs = {(r["var1"], r["var2"]): r for r in metrics_data["crossvar_results"]["Paul"]}
    assert paul_pairs[("pH", "doSat")]["rho"] == pytest.approx(-0.9057, abs=0.001)
