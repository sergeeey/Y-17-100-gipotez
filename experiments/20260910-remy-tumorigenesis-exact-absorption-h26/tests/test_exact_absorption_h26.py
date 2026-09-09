"""Tests for H-B7-26 -- exact absorbing Markov chain escape probability."""

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
    return _load_module("h_b7_26_run_under_test", EXPERIMENT_DIR / "run.py")


@pytest.fixture(scope="module")
def metrics_data():
    path = EXPERIMENT_DIR / "metrics" / "run.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_branch1_k1_matches_known_exact_value(metrics_data):
    """Regression lock on the Compute-First Check's own verified value."""
    r = next(x for x in metrics_data["results"] if x["branch"] == "branch_1" and x["k"] == 1)
    assert r["status"] == "OK"
    assert r["exact_escape_probability"] == pytest.approx(0.068866, abs=1e-5)


def test_k5_gives_exactly_one_both_branches(metrics_data):
    """k=5 is the positive control (H-B7-22's own SCHEDULE_ROBUST condition):
    exact escape probability must equal exactly 1.0. Expected steps to
    absorption is NOT required to be 0 -- the release state need not itself
    be the fixed point, only guaranteed (probability 1) to reach it."""
    for branch in ("branch_1", "branch_2"):
        r = next(x for x in metrics_data["results"] if x["branch"] == branch and x["k"] == 5)
        assert r["status"] == "OK"
        assert r["exact_escape_probability"] == 1.0
        assert r["expected_steps_to_absorption"] >= 0.0


def test_oracle_gate_passes_for_all_ten_conditions(metrics_data):
    assert metrics_data["n_conditions_tested"] == 10
    assert metrics_data["n_ok"] == 10
    assert metrics_data["oracle_gate_all_passed"] is True
    assert metrics_data["n_oracle_passed"] == metrics_data["n_oracle_checked"] == 10
    for r in metrics_data["results"]:
        assert r.get("oracle_gate_passed", True) is True


def test_verdict_is_confirmed(metrics_data):
    assert metrics_data["verdict"] == "CONFIRMED"
    assert metrics_data["k5_positive_control_all_exactly_one"] is True


def test_branch_release_states_are_not_identical(run_module):
    """Locks in the user's own correction: branch_1 and branch_2 are correlated
    but genuinely distinct computations, not literal duplicates, at every fragile k."""
    h13 = run_module.h13
    h1 = run_module.h1

    text = h13.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    for k in (1, 2, 3, 4):
        start_1 = dict(
            zip(
                run_module.PYBOOLNET_NODE_ORDER,
                (c == "1" for c in run_module.GROWTH_ARREST_STATE_1),
            )
        )
        start_2 = dict(
            zip(
                run_module.PYBOOLNET_NODE_ORDER,
                (c == "1" for c in run_module.GROWTH_ARREST_STATE_2),
            )
        )
        sim1 = h13.simulate_transient_clamp_multi_with_release_state(
            start_1, node_names, wild_type_rules, run_module.CLAMPS, k
        )
        sim2 = h13.simulate_transient_clamp_multi_with_release_state(
            start_2, node_names, wild_type_rules, run_module.CLAMPS, k
        )
        assert sim1["release_state"] != sim2["release_state"], (
            f"k={k}: branch_1 and branch_2 release states must NOT be identical"
        )


def test_transition_matrix_rows_are_well_formed():
    """Sanity check on solve_absorption's own transition-matrix construction:
    every transient state's outgoing probability mass to (absorbing-prolif +
    transient successors) sums to 1, via a small synthetic 3-state chain."""
    import networkx as nx

    run_module_local = _load_module("h_b7_26_sanity", EXPERIMENT_DIR / "run.py")

    graph = nx.DiGraph()
    node_names = ["Proliferation", "Growth_arrest", "X"]
    # states as tuples of bools over node_names
    prolif_state = (True, False, False)
    ga_state = (False, True, False)
    transient_state = (False, False, True)

    graph.add_edge(transient_state, prolif_state)
    graph.add_edge(transient_state, ga_state)

    result = run_module_local.solve_absorption(graph, transient_state, node_names)
    assert result["status"] == "OK"
    assert result["n_transient"] == 1
    assert result["n_absorbing_prolif"] == 1
    assert result["n_absorbing_ga"] == 1
    # 1 of 2 outgoing edges leads to PROLIFERATION -> exact probability 0.5
    assert result["exact_escape_probability"] == pytest.approx(0.5)
    assert result["expected_steps_to_absorption"] == pytest.approx(1.0)


def test_classify_absorbing_state():
    run_module_local = _load_module("h_b7_26_classify", EXPERIMENT_DIR / "run.py")
    node_names = ["Proliferation", "Growth_arrest"]
    assert run_module_local.classify_absorbing_state((True, False), node_names) == "PROLIFERATION"
    assert run_module_local.classify_absorbing_state((False, True), node_names) == "GROWTH_ARREST"
    assert run_module_local.classify_absorbing_state((True, True), node_names) == "GROWTH_ARREST"
    assert run_module_local.classify_absorbing_state((False, False), node_names) == "AMBIGUOUS"
