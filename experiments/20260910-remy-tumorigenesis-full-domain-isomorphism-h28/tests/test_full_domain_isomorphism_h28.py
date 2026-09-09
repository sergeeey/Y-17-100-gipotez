"""Tests for H-B7-28 -- full-domain (k=1..40) extension of the branch isomorphism mechanism."""

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
def metrics_data():
    path = EXPERIMENT_DIR / "metrics" / "run.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_verdict_is_confirmed(metrics_data):
    assert metrics_data["verdict"] == "CONFIRMED"
    assert metrics_data["n_conditions_tested"] == 40
    assert metrics_data["n_ok"] == 40
    assert metrics_data["n_blocked_infrastructure"] == 0


def test_covers_h_b7_22s_own_full_domain(metrics_data):
    """k must range exactly 1..40, matching H-B7-22's own originally-tested domain."""
    ks = sorted(r["k"] for r in metrics_data["results"])
    assert ks == list(range(1, 41))


def test_all_isomorphisms_confirmed_across_full_domain(metrics_data):
    for r in metrics_data["results"]:
        assert r["status"] == "OK"
        assert r["isomorphism"]["isomorphism_confirmed"] is True
        assert r["phi_release_1_equals_release_2"] is True


def test_zero_exception_invariant_holds_across_full_domain(metrics_data):
    total_states_checked = 0
    for r in metrics_data["results"]:
        for branch_key in ("invariant_branch_1", "invariant_branch_2"):
            inv = r[branch_key]
            assert inv["n_fgfr3_false"] == 0
            assert inv["n_grb2_true"] == 0
            assert inv["n_egfr_true"] == 0
            assert inv["invariant_holds"] is True
            total_states_checked += inv["n_states"]
    assert total_states_checked == metrics_data["n_states_scanned"]
    assert total_states_checked > 4000  # sanity: this must be a real, non-trivial sweep


def test_corollary_matches_across_full_domain(metrics_data):
    for r in metrics_data["results"]:
        assert r["corollary_escape_probability_matches"] is True
        assert r["exact_escape_probability_branch_1"] == pytest.approx(
            r["exact_escape_probability_branch_2"], abs=1e-9
        )


def test_k1_to_5_matches_h_b7_27s_own_committed_values(metrics_data):
    """Regression lock: the k=1..5 subset must reproduce H-B7-27's own already-confirmed numbers."""
    h27_path = (
        EXPERIMENT_DIR.parent
        / "20260910-remy-tumorigenesis-branch-isomorphism-h27"
        / "metrics"
        / "run.json"
    )
    h27_data = json.loads(h27_path.read_text(encoding="utf-8"))
    h27_by_k = {r["k"]: r for r in h27_data["results"]}

    for r in metrics_data["results"]:
        if r["k"] not in h27_by_k:
            continue
        h27_r = h27_by_k[r["k"]]
        assert r["exact_escape_probability_branch_1"] == pytest.approx(
            h27_r["exact_escape_probability_branch_1"], abs=1e-9
        )
        assert r["exact_escape_probability_branch_2"] == pytest.approx(
            h27_r["exact_escape_probability_branch_2"], abs=1e-9
        )


def test_schedule_robust_region_k_ge_5_gives_trivial_graphs(metrics_data):
    """H-B7-22 classified k>=5 as SCHEDULE_ROBUST -- graphs there should be small/trivial."""
    for r in metrics_data["results"]:
        if r["k"] >= 5:
            assert r["exact_escape_probability_branch_1"] == 1.0
            assert r["exact_escape_probability_branch_2"] == 1.0
