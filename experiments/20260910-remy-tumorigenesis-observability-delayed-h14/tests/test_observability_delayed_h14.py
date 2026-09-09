import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    GROWTH_ARREST_STATE_1,
    PYBOOLNET_NODE_ORDER,
    fate_label,
    h1,
    h13,
    simulate_transient_clamp_multi_with_delayed_observation,
)


def _load_network():
    text = (
        Path(__file__).resolve().parents[2]
        / "20260906-remy-tumorigenesis-transient-h4"
        / "data"
        / "remy_tumorigenesis.bnet"
    ).read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wild_type_rules = h1.compile_rules(rules)
    return node_names, wild_type_rules


def test_j0_reproduces_h_b7_13_release_state_exactly():
    """Regression/continuity check (Substrate Gate): j=0 (observe immediately at release, no
    delay) must produce the IDENTICAL observed_state as H-B7-13's own already-verified
    simulate_transient_clamp_multi_with_release_state, for the same (branch, k). If this fails,
    the new delayed-observation function has a bug -- not a finding about the network."""
    node_names, wild_type_rules = _load_network()
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))
    clamps = {"p21CIP": False, "RBL2": False}

    for k in (1, 4, 5, 6, 30):
        delayed_j0 = simulate_transient_clamp_multi_with_delayed_observation(
            start_state, node_names, wild_type_rules, clamps, k, 0
        )
        original = h13.simulate_transient_clamp_multi_with_release_state(
            start_state, node_names, wild_type_rules, clamps, k
        )
        assert delayed_j0["observed_state"] == original["release_state"]
        assert delayed_j0["final_state"] == original["final_state"]


def test_j0_fates_match_h_b7_10_ground_truth():
    """Same ground truth H-B7-13 itself was checked against: k=4 relapses (GROWTH_ARREST), k=5
    escapes (PROLIFERATION) on branch 1."""
    node_names, wild_type_rules = _load_network()
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))
    clamps = {"p21CIP": False, "RBL2": False}

    sim4 = simulate_transient_clamp_multi_with_delayed_observation(
        start_state, node_names, wild_type_rules, clamps, 4, 0
    )
    sim5 = simulate_transient_clamp_multi_with_delayed_observation(
        start_state, node_names, wild_type_rules, clamps, 5, 0
    )
    assert fate_label(sim4["final_state"]) == "GROWTH_ARREST"
    assert fate_label(sim5["final_state"]) == "PROLIFERATION"


def test_delayed_observation_state_changes_with_j():
    """Hand-verified structural check: for a fixed k, the observed_state at j=1 must generally
    differ from j=0 (continuing wild-type dynamics moves the state), UNLESS k is already large
    enough that the trajectory has already reached its final attractor by the time of release (a
    legitimate edge case, checked separately below) -- confirms j actually has an effect on what
    is captured, not a silent no-op."""
    node_names, wild_type_rules = _load_network()
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))
    clamps = {"p21CIP": False, "RBL2": False}

    sim_j0 = simulate_transient_clamp_multi_with_delayed_observation(
        start_state, node_names, wild_type_rules, clamps, 1, 0
    )
    sim_j1 = simulate_transient_clamp_multi_with_delayed_observation(
        start_state, node_names, wild_type_rules, clamps, 1, 1
    )
    assert sim_j0["observed_state"] != sim_j1["observed_state"]
    # both must still agree on the eventual fate -- j only changes WHEN we look, not the
    # deterministic trajectory or its endpoint
    assert fate_label(sim_j0["final_state"]) == fate_label(sim_j1["final_state"])


def test_large_j_observed_state_equals_final_state():
    """Hand-verified edge case: for j large enough that the trajectory has already converged
    (e.g. j=30 starting from k=1, well past H-B7-9/10's own max tested k=30), the observed state
    at that point must equal the eventual attractor state -- the delay cannot look PAST
    convergence to something else, by definition of an attractor."""
    node_names, wild_type_rules = _load_network()
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))
    clamps = {"p21CIP": False, "RBL2": False}

    sim = simulate_transient_clamp_multi_with_delayed_observation(
        start_state, node_names, wild_type_rules, clamps, 5, 30
    )
    assert sim["observed_state"] == sim["final_state"]
