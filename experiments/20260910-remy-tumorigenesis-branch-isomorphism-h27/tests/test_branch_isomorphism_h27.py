"""Tests for H-B7-27 -- graph automorphism explanation of branch_1/branch_2 escape-prob equality."""

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
    return _load_module("h_b7_27_run_under_test", EXPERIMENT_DIR / "run.py")


@pytest.fixture(scope="module")
def metrics_data():
    path = EXPERIMENT_DIR / "metrics" / "run.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_verdict_is_confirmed(metrics_data):
    assert metrics_data["verdict"] == "CONFIRMED"
    assert metrics_data["n_conditions_tested"] == 5


def test_all_isomorphisms_confirmed_for_every_k(metrics_data):
    for r in metrics_data["results"]:
        assert r["isomorphism"]["node_set_bijection"] is True
        assert r["isomorphism"]["edges_g1_to_g2_preserved"] is True
        assert r["isomorphism"]["edges_g2_to_g1_preserved"] is True
        assert r["isomorphism"]["isomorphism_confirmed"] is True


def test_phi_maps_release_1_to_release_2_for_every_k(metrics_data):
    for r in metrics_data["results"]:
        assert r["phi_release_1_equals_release_2"] is True


def test_fgfr3_grb2_egfr_invariant_zero_exceptions(metrics_data):
    """The actual mechanism: FGFR3=True, GRB2=False, EGFR=False with ZERO exceptions
    across every reachable state, both branches, every k."""
    for r in metrics_data["results"]:
        for branch_key in ("invariant_branch_1", "invariant_branch_2"):
            inv = r[branch_key]
            assert inv["n_fgfr3_false"] == 0, f"k={r['k']} {branch_key}: FGFR3 was False somewhere"
            assert inv["n_grb2_true"] == 0, f"k={r['k']} {branch_key}: GRB2 was True somewhere"
            assert inv["n_egfr_true"] == 0, f"k={r['k']} {branch_key}: EGFR was True somewhere"
            assert inv["invariant_holds"] is True
            assert inv["n_states"] > 0


def test_corollary_escape_probabilities_match_h26_and_each_other(metrics_data):
    for r in metrics_data["results"]:
        assert r["corollary_escape_probability_matches"] is True
        assert r["exact_escape_probability_branch_1"] == pytest.approx(
            r["exact_escape_probability_branch_2"], abs=1e-9
        )


def test_k5_gives_exactly_one_both_branches(metrics_data):
    r = next(x for x in metrics_data["results"] if x["k"] == 5)
    assert r["exact_escape_probability_branch_1"] == 1.0
    assert r["exact_escape_probability_branch_2"] == 1.0


def test_build_phi_flips_only_the_named_node(run_module):
    node_names = ["A", "B", "EGFR_stimulus", "C"]
    phi = run_module.build_phi(node_names, "EGFR_stimulus")
    state = (True, False, True, False)
    flipped = phi(state)
    assert flipped == (True, False, False, False)
    # applying twice returns to the original (phi is an involution)
    assert phi(flipped) == state


def test_check_invariant_detects_a_violation():
    """Sanity check: check_invariant must actually be able to fail, not vacuously pass."""
    import networkx as nx

    run_module_local = _load_module("h_b7_27_sanity", EXPERIMENT_DIR / "run.py")

    node_names = ["FGFR3", "GRB2", "EGFR"]
    graph = nx.DiGraph()
    # one state where FGFR3=False -- should be caught as a violation
    violating_state = (False, False, False)
    graph.add_node(violating_state)

    result = run_module_local.check_invariant(graph, node_names)
    assert result["n_fgfr3_false"] == 1
    assert result["invariant_holds"] is False


def test_check_isomorphism_detects_a_non_isomorphism():
    """Sanity check: check_isomorphism must actually be able to fail, not vacuously pass."""
    import networkx as nx

    run_module_local = _load_module("h_b7_27_sanity2", EXPERIMENT_DIR / "run.py")

    node_names = ["X", "Y"]
    phi = run_module_local.build_phi(node_names, "X")

    g1 = nx.DiGraph()
    g1.add_edge((False, False), (True, False))

    g2 = nx.DiGraph()
    # phi maps (False,False)->(True,False) and (True,False)->(False,False);
    # g2 deliberately does NOT contain the required edge (False,False)->(True,False)
    g2.add_node((True, False))
    g2.add_node((False, False))

    result = run_module_local.check_isomorphism(g1, g2, phi)
    assert result["isomorphism_confirmed"] is False
