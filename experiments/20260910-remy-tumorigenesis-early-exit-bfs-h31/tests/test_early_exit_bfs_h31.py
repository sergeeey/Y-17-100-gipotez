"""Tests for H-B7-31 -- early-exit BFS as a genuine cheap FRAGILE-side discriminator."""

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
    return _load_module("h_b7_31_run_under_test", EXPERIMENT_DIR / "run.py")


@pytest.fixture(scope="module")
def metrics_data():
    path = EXPERIMENT_DIR / "metrics" / "run.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_verdict_is_confirmed(metrics_data):
    assert metrics_data["verdict"] == "CONFIRMED"
    assert metrics_data["n_conditions_tested"] == 10
    assert metrics_data["n_fragile"] == 8
    assert metrics_data["n_robust"] == 2


def test_all_fragile_conditions_exceed_savings_bar(metrics_data):
    for r in metrics_data["results"]:
        if r["classification"] == "SCHEDULE_FRAGILE":
            assert r["savings_fraction"] is not None
            assert r["savings_fraction"] > metrics_data["savings_bar"]
            assert r["savings_fraction"] > 0.8  # actual observed range is 0.84-0.90


def test_no_false_positives_on_robust_conditions(metrics_data):
    """The honest asymmetry: ROBUST conditions must never falsely show both fates reachable --
    early exit is not achievable there, by construction of the underlying dynamics."""
    for r in metrics_data["results"]:
        if r["classification"] == "SCHEDULE_ROBUST":
            assert len(r["fates_seen"]) <= 1
            assert r["n_visited_at_early_exit"] is None
            assert r["savings_fraction"] is None


def test_classification_matches_h_b7_22s_own_established_pattern(metrics_data):
    """k=1..4 must be FRAGILE, k=5 must be ROBUST, matching H-B7-22's own committed pattern."""
    for r in metrics_data["results"]:
        if r["k"] <= 4:
            assert r["classification"] == "SCHEDULE_FRAGILE"
        else:
            assert r["classification"] == "SCHEDULE_ROBUST"


def test_branches_give_identical_savings_per_h_b7_27_28_isomorphism(metrics_data):
    """Regression lock: since branch_1/branch_2 are confirmed graph-isomorphic (H-B7-27/28),
    their early-exit statistics must match exactly at every k."""
    by_branch_k = {(r["branch"], r["k"]): r for r in metrics_data["results"]}
    for k in (1, 2, 3, 4, 5):
        r1 = by_branch_k[("branch_1", k)]
        r2 = by_branch_k[("branch_2", k)]
        assert r1["n_total_visited"] == r2["n_total_visited"]
        assert r1["n_visited_at_early_exit"] == r2["n_visited_at_early_exit"]


def test_total_states_match_h_b7_26s_own_committed_values(metrics_data):
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
        assert r["n_total_visited"] == h26_by_cond[key]["n_states_in_graph"]


def test_bfs_early_exit_detects_a_single_fate_case(run_module):
    """Sanity check: bfs_with_early_exit_tracking must actually be able to report only 1 fate
    found (not vacuously always finding 2) -- a minimal 2-state graph with only PROLIFERATION
    reachable, no Growth_arrest anywhere."""
    node_names = ["Proliferation", "Growth_arrest", "X"]
    prolif_idx = 0
    ga_idx = 1

    def compiled_rules_stub(state_dict):
        pass

    # monkeypatch async_successors behavior via a tiny closed system: start state has X=False,
    # its only successor flips X to True (Proliferation stays True forever, GA never appears)
    import networkx as nx  # noqa: F401 -- not used directly, just confirming import works

    start = (True, False, False)

    class FakeRules(dict):
        pass

    # directly exercise the function with a trivial deterministic rule set:
    # Proliferation: always True (never toggles, contributes no successor)
    # Growth_arrest: always False (never toggles, contributes no successor)
    # X: flips once from False to True, then True stays True (no successor after that)
    def evaluate_stub(rule, state):
        return rule(state)

    rules = {
        "Proliferation": lambda s: True,
        "Growth_arrest": lambda s: False,
        "X": lambda s: True,
    }

    # patch h1.evaluate_expression used inside async_successors via the loaded h22 module
    original_evaluate = run_module.h1.evaluate_expression
    run_module.h1.evaluate_expression = evaluate_stub
    try:
        result = run_module.bfs_with_early_exit_tracking(
            start, node_names, rules, 1000, prolif_idx, ga_idx
        )
    finally:
        run_module.h1.evaluate_expression = original_evaluate

    assert result["fates_seen"] == ["PROLIFERATION"]
    assert result["n_visited_at_early_exit"] is None
