"""Tests for H-B7-29 -- FGFR3_stimulus asymmetry contrast test vs H-B7-27/28's EGFR_stimulus."""

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
    return _load_module("h_b7_29_run_under_test", EXPERIMENT_DIR / "run.py")


@pytest.fixture(scope="module")
def metrics_data():
    path = EXPERIMENT_DIR / "metrics" / "run.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_verdict_is_confirmed(metrics_data):
    assert metrics_data["verdict"] == "CONFIRMED"
    assert metrics_data["n_conditions_tested"] == 10
    assert metrics_data["all_asymmetry_confirmed"] is True


def test_flip_node_is_fgfr3_stimulus(metrics_data):
    assert metrics_data["flip_node"] == "FGFR3_stimulus"


def test_isomorphism_fails_for_every_condition(metrics_data):
    """The whole point of this contrast test: unlike EGFR_stimulus, this flip must NEVER
    be a graph isomorphism, for any of the 10 conditions."""
    for r in metrics_data["results"]:
        assert r["isomorphism_confirmed"] is False
        assert r["isomorphism"]["node_set_bijection"] is False
        assert r["asymmetry_confirmed_this_condition"] is True


def test_flipped_graph_size_differs_from_original_for_every_condition(metrics_data):
    """Cap-independent check: the flipped graph's size alone (even truncated) must differ
    from the original -- this alone rules out a bijection without needing an exact count."""
    for r in metrics_data["results"]:
        assert r["size_alone_rules_out_bijection"] is True
        assert r["n_states_flipped_capped"] != r["n_states_original"]
        assert r["n_states_flipped_capped"] > r["n_states_original"]


def test_state_cap_hit_is_reported_honestly_not_treated_as_exact(metrics_data):
    """Every condition hit STATE_CAP -- exact violation counts must be None (not fabricated),
    per FL Step 2a: BLOCKED-INFRASTRUCTURE on the exact count is not evidence against the claim,
    but it must also never be silently reported as if it were a verified exact number."""
    assert metrics_data["n_hit_state_cap"] == 10
    for r in metrics_data["results"]:
        assert r["flipped_hit_cap"] is True
        assert r["n_fgfr3_false_in_flipped_graph"] is None


def test_asymmetry_contrasts_with_h_b7_27s_own_egfr_stimulus_result(metrics_data):
    """The actual asymmetry claim, checked directly against H-B7-27's own committed data:
    for the SAME (branch, k) pairs, flip(EGFR_stimulus) [H-B7-27] IS an isomorphism while
    flip(FGFR3_stimulus) [this experiment] is NOT -- a real cross-experiment contrast, not
    just an internal self-consistency check."""
    h27_path = (
        EXPERIMENT_DIR.parent
        / "20260910-remy-tumorigenesis-branch-isomorphism-h27"
        / "metrics"
        / "run.json"
    )
    h27_data = json.loads(h27_path.read_text(encoding="utf-8"))
    h27_by_k = {r["k"]: r for r in h27_data["results"]}

    contrasts_checked = 0
    for r in metrics_data["results"]:
        h27_r = h27_by_k.get(r["k"])
        if h27_r is None:
            continue
        assert h27_r["isomorphism"]["isomorphism_confirmed"] is True, (
            f"k={r['k']}: H-B7-27's own EGFR_stimulus flip must be confirmed isomorphic"
        )
        assert r["isomorphism_confirmed"] is False, (
            f"k={r['k']}: this experiment's FGFR3_stimulus flip must NOT be isomorphic"
        )
        contrasts_checked += 1
    assert contrasts_checked == 10  # k=1..5 x both branches


def test_original_graph_sizes_match_h_b7_26s_own_committed_values(metrics_data):
    h26_path = (
        EXPERIMENT_DIR.parent
        / "20260910-remy-tumorigenesis-exact-absorption-h26"
        / "metrics"
        / "run.json"
    )
    h26_data = json.loads(h26_path.read_text(encoding="utf-8"))
    h26_by_cond = {(r["branch"], r["k"]): r for r in h26_data["results"]}

    for r in metrics_data["results"]:
        key = (r["branch"], r["k"])
        if key in h26_by_cond:
            assert r["n_states_original"] == h26_by_cond[key]["n_states_in_graph"]


def test_build_phi_targets_fgfr3_stimulus_not_egfr_stimulus(run_module):
    node_names = ["A", "EGFR_stimulus", "FGFR3_stimulus", "B"]
    phi = run_module.build_phi(node_names, "FGFR3_stimulus")
    state = (True, False, True, False)
    flipped = phi(state)
    assert flipped == (True, False, False, False)
    assert flipped != run_module.build_phi(node_names, "EGFR_stimulus")(state)
