import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import boolean
from run import (
    CLAMPS,
    GROWTH_ARREST_STATE_1,
    PYBOOLNET_NODE_ORDER,
    fate_label,
    h1,
    simulate_transient_clamp_multi_with_delayed_observation,
    walk_clamped_trajectory_until_cycle,
)

ALGEBRA = boolean.BooleanAlgebra()


def test_walk_clamped_trajectory_synchronous_update_gives_immediate_fixed_point():
    """Hand-verified, CORRECTED after a first hand-trace error caught by the test itself failing:
    A := !B, B := !A LOOKS like it should alternate, but under SYNCHRONOUS update (both rules
    evaluated from the SAME old state simultaneously, not sequentially) it is actually an
    IMMEDIATE fixed point: A_new = !B_old = !False = True = A_old, B_new = !A_old = !True = False
    = B_old -- the state maps to itself in one step. This is exactly the kind of asynchronous-vs-
    synchronous confusion claim.md's own caveat #2 warns is a SEPARATE, untested question --
    caught here concretely, not just as an abstract caveat."""
    rules = {"A": ALGEBRA.parse("!B"), "B": ALGEBRA.parse("!A")}
    start = {"A": True, "B": False}
    result = walk_clamped_trajectory_until_cycle(start, ["A", "B"], rules)
    assert result["trajectory"] == [{"A": True, "B": False}]
    assert result["cycle_start_index"] == 0
    assert result["cycle_period"] == 1
    assert result["orbit_length"] == 1


def test_walk_clamped_trajectory_until_cycle_hand_verified_two_cycle():
    """Hand-verified: A := A (constant), B := A&!B. Starting A=True, B=False:
    step 1: A_new=A_old(T). B_new=A_old(T)&!B_old(T)=T&T=T -> state1=(T,T).
    step 2: A_new=A_old(T). B_new=A_old(T)&!B_old(T)=T&F=F -> state2=(T,F)=start!
    Genuine 2-cycle: trajectory=[(T,F),(T,T)], cycle_start_index=0, period=2."""
    rules = {"A": ALGEBRA.parse("A"), "B": ALGEBRA.parse("A&!B")}
    start = {"A": True, "B": False}
    result = walk_clamped_trajectory_until_cycle(start, ["A", "B"], rules)
    assert result["trajectory"] == [{"A": True, "B": False}, {"A": True, "B": True}]
    assert result["cycle_start_index"] == 0
    assert result["cycle_period"] == 2


def test_walk_clamped_trajectory_immediate_fixed_point():
    """Hand-verified: A := True (const), B := True (const) -- ANY start converges to (True,True)
    in exactly 1 step, then stays -- cycle_start_index=1, cycle_period=1, orbit_length=2
    (trajectory = [start, fixed_point])."""
    rules = {"A": ALGEBRA.parse("1"), "B": ALGEBRA.parse("1")}
    start = {"A": False, "B": False}
    result = walk_clamped_trajectory_until_cycle(start, ["A", "B"], rules)
    assert result["trajectory"] == [{"A": False, "B": False}, {"A": True, "B": True}]
    assert result["cycle_start_index"] == 1
    assert result["cycle_period"] == 1


def test_fate_independent_of_j_for_same_k():
    """Structural sanity check: the eventual fate must not depend on WHEN we peek (j), only on
    the underlying deterministic trajectory determined by k -- sim0 and sim1's final_state must
    agree for the same k."""
    text = (
        Path(__file__).resolve().parents[2]
        / "20260906-remy-tumorigenesis-transient-h4"
        / "data"
        / "remy_tumorigenesis.bnet"
    ).read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wild_type_rules = h1.compile_rules(rules)
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))

    for k in (3, 4, 5, 6):
        sim0 = simulate_transient_clamp_multi_with_delayed_observation(
            start_state, node_names, wild_type_rules, CLAMPS, k, 0
        )
        sim1 = simulate_transient_clamp_multi_with_delayed_observation(
            start_state, node_names, wild_type_rules, CLAMPS, k, 1
        )
        assert sim0["final_state"] == sim1["final_state"]
        assert fate_label(sim0["final_state"]) == fate_label(sim1["final_state"])


def test_real_network_clamped_orbit_is_finite_and_short():
    """Sanity/Substrate check on the REAL network: the clamped trajectory for branch 1 must
    actually terminate in a cycle well within the max_steps bound (a finite deterministic system
    MUST cycle -- this just confirms it happens at a plausible, small scale for this network, not
    that walk_clamped_trajectory_until_cycle's raise-on-timeout path is silently masking a bug)."""
    import importlib.util

    h2_spec = importlib.util.spec_from_file_location(
        "h_b7_15_test_h2",
        Path(__file__).resolve().parents[2]
        / "20260906-kauffman-cellcycle-perturbation-h2"
        / "run.py",
    )
    h2 = importlib.util.module_from_spec(h2_spec)
    h2_spec.loader.exec_module(h2)

    text = (
        Path(__file__).resolve().parents[2]
        / "20260906-remy-tumorigenesis-transient-h4"
        / "data"
        / "remy_tumorigenesis.bnet"
    ).read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wild_type_rules = h1.compile_rules(rules)
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))
    clamped_rules = dict(wild_type_rules)
    for node, value in CLAMPS.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)
    clamp_applied_start = dict(start_state)
    for node, value in CLAMPS.items():
        clamp_applied_start[node] = value

    result = walk_clamped_trajectory_until_cycle(clamp_applied_start, node_names, clamped_rules)
    assert result["cycle_period"] >= 1
    assert result["orbit_length"] >= 1
    assert result["orbit_length"] < 2000  # well within max_steps, not hitting the timeout path
