import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    BRANCH_INPUTS_1,
    GROWTH_ARREST_STATE_1,
    PYBOOLNET_NODE_ORDER,
    fate_label,
    find_collisions,
    marker_projection,
    simulate_transient_clamp_multi_with_release_state,
)


def test_marker_projection_is_order_independent_and_complete():
    """Hand-verified: projection is a sorted tuple of (node, value) pairs -- two states that
    agree on the markers' values must produce an IDENTICAL projection regardless of dict order."""
    s1 = {"A": True, "B": False, "C": True}
    s2 = {"C": True, "A": True, "B": False}
    assert marker_projection(s1, {"A", "C"}) == marker_projection(s2, {"A", "C"})
    assert marker_projection(s1, {"A", "C"}) == (("A", True), ("C", True))


def test_fate_label_hand_cases():
    assert fate_label({"Growth_arrest": True, "Proliferation": False}) == "GROWTH_ARREST"
    assert fate_label({"Growth_arrest": False, "Proliferation": True}) == "PROLIFERATION"
    assert fate_label({"Growth_arrest": True, "Proliferation": True}) == "GROWTH_ARREST"
    assert fate_label({"Growth_arrest": False, "Proliferation": False}) == "AMBIGUOUS"


def test_find_collisions_synthetic_positive_case():
    """Hand-constructed: two entries share the SAME markers projection but have DIFFERENT fates
    -- must be reported as exactly one collision group with both members."""
    domain = [
        {"branch": "b1", "k": 1, "release_state": {"X": True, "Y": False}, "fate": "GROWTH_ARREST"},
        {"branch": "b1", "k": 2, "release_state": {"X": True, "Y": True}, "fate": "PROLIFERATION"},
    ]
    collisions = find_collisions(domain, {"X"})  # only X observed -- Y (which differs) is hidden
    assert len(collisions) == 1
    fates_in_collision = {m["fate"] for m in collisions[0]["members"]}
    assert fates_in_collision == {"GROWTH_ARREST", "PROLIFERATION"}


def test_find_collisions_synthetic_negative_case_full_observation():
    """Hand-constructed: observing BOTH X and Y (the full state here) makes every projection
    unique by construction -- zero collisions possible, tautologically."""
    domain = [
        {"branch": "b1", "k": 1, "release_state": {"X": True, "Y": False}, "fate": "GROWTH_ARREST"},
        {"branch": "b1", "k": 2, "release_state": {"X": True, "Y": True}, "fate": "PROLIFERATION"},
    ]
    collisions = find_collisions(domain, {"X", "Y"})
    assert collisions == []


def test_find_collisions_no_false_positive_when_fates_agree():
    """Hand-constructed: same markers projection, but SAME fate too -- not a collision (the
    marker set correctly, if coincidentally, agrees with the true outcome here)."""
    domain = [
        {"branch": "b1", "k": 1, "release_state": {"X": True, "Y": False}, "fate": "GROWTH_ARREST"},
        {"branch": "b1", "k": 2, "release_state": {"X": True, "Y": True}, "fate": "GROWTH_ARREST"},
    ]
    collisions = find_collisions(domain, {"X"})
    assert collisions == []


def test_release_state_captured_before_release_not_after():
    """Ground truth from H-B7-10 (metrics/run.json, already committed): branch 1, k=4 relapses to
    GROWTH_ARREST, k=5 escapes to PROLIFERATION -- clean threshold. The RELEASE-moment state
    (this function's new contribution) must differ from H-B7-9/10's FINAL state for small k (the
    trajectory is still mid-flight at release, not yet at its eventual attractor) -- confirms
    release_state != final_state in general, i.e. the new field carries real information."""
    import importlib.util

    h1_spec = importlib.util.spec_from_file_location(
        "h_b7_13_test_h1",
        Path(__file__).resolve().parents[2]
        / "20260906-kauffman-cellcycle-attractors-h1"
        / "run.py",
    )
    h1 = importlib.util.module_from_spec(h1_spec)
    h1_spec.loader.exec_module(h1)

    data_path = (
        Path(__file__).resolve().parents[2]
        / "20260906-remy-tumorigenesis-transient-h4"
        / "data"
        / "remy_tumorigenesis.bnet"
    )
    rules = h1.parse_bnet(data_path.read_text(encoding="utf-8"))
    node_names = [n for n, _ in rules]
    wild_type_rules = h1.compile_rules(rules)
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))

    sim_k1 = simulate_transient_clamp_multi_with_release_state(
        start_state, node_names, wild_type_rules, {"p21CIP": False, "RBL2": False}, 1
    )
    assert sim_k1["release_state"] != sim_k1["final_state"]

    sim_k4 = simulate_transient_clamp_multi_with_release_state(
        start_state, node_names, wild_type_rules, {"p21CIP": False, "RBL2": False}, 4
    )
    sim_k5 = simulate_transient_clamp_multi_with_release_state(
        start_state, node_names, wild_type_rules, {"p21CIP": False, "RBL2": False}, 5
    )
    assert fate_label(sim_k4["final_state"]) == "GROWTH_ARREST"  # matches H-B7-10 ground truth
    assert fate_label(sim_k5["final_state"]) == "PROLIFERATION"  # matches H-B7-10 ground truth
    # both k=4 and k=5 share the SAME (constant) DNA_damage value at release -- confirms the
    # floor negative-control marker set is a genuine (not vacuous) test case
    assert sim_k4["release_state"]["DNA_damage"] == sim_k5["release_state"]["DNA_damage"]
    assert BRANCH_INPUTS_1["DNA_damage"] == sim_k4["release_state"]["DNA_damage"]
