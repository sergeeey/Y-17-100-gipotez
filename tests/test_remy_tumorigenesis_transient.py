"""Tests for H-B7-4: transient RAS perturbation on the Remy et al. 2015 bladder tumorigenesis
network's bistable (Growth_arrest / Proliferation) branch. Verified on a hand-checkable
synthetic bistable toggle switch BEFORE trusting the result on the real 35-node network.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_H1_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-kauffman-cellcycle-attractors-h1"
)
_SPEC_H1 = importlib.util.spec_from_file_location("kauffman_h1_run", _H1_DIR / "run.py")
h1 = importlib.util.module_from_spec(_SPEC_H1)
_SPEC_H1.loader.exec_module(h1)

_H3_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-kauffman-cellcycle-transient-h3"
)
_SPEC_H3 = importlib.util.spec_from_file_location("kauffman_h3_run", _H3_DIR / "run.py")
h3 = importlib.util.module_from_spec(_SPEC_H3)
_SPEC_H3.loader.exec_module(h3)

_H4_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-remy-tumorigenesis-transient-h4"
)
_SPEC_H4 = importlib.util.spec_from_file_location("remy_h4_run", _H4_DIR / "run.py")
h4 = importlib.util.module_from_spec(_SPEC_H4)
_SPEC_H4.loader.exec_module(h4)


def test_toggle_switch_has_exactly_two_fixed_points():
    """A'=A|B, B'=A|B: a classic bistable toggle. (0,0) and (1,1) are fixed points; (1,0) and
    (0,1) both flow to (1,1). Hand-verified before trusting the real network."""
    compiled = h1.compile_rules([("A", "A|B"), ("B", "A|B")])
    cycle_00 = h3.run_until_attractor({"A": False, "B": False}, compiled, ["A", "B"])
    cycle_10 = h3.run_until_attractor({"A": True, "B": False}, compiled, ["A", "B"])
    cycle_11 = h3.run_until_attractor({"A": True, "B": True}, compiled, ["A", "B"])
    assert cycle_00 == [{"A": False, "B": False}]
    assert cycle_10 == [{"A": True, "B": True}]
    assert cycle_11 == [{"A": True, "B": True}]


def test_transient_clamp_flips_the_toggle_switch_to_the_other_attractor():
    """From the (0,0) fixed point, a 1-step transient clamp of A=1 then release moves the
    system to the OTHER attractor (1,1) -- exactly the mechanism this experiment tests on the
    real network, verified here on a network simple enough to trace by hand:
    clamp step: A=1 (forced), B'=A|B=0|0=0 -> (1,0).
    release from (1,0): A'=A|B=1|0=1, B'=A|B=1|0=1 -> (1,1), a fixed point."""
    compiled = h1.compile_rules([("A", "A|B"), ("B", "A|B")])
    result = h3.simulate_transient_clamp(
        {"A": False, "B": False}, ["A", "B"], compiled, {"A": True}, k_steps=1
    )
    assert result["type"] == "point"
    assert result["states"] == ["11"]


def test_remy_bnet_parses_to_35_named_nodes():
    text = h4.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    names = {n for n, _ in rules}
    assert len(names) == 35
    assert {"RAS", "TP53", "RB1", "Growth_arrest", "Proliferation"} <= names


def test_growth_arrest_and_proliferation_states_are_both_fixed_points_under_own_pipeline():
    """Independent cross-check (Gate 3 spirit): both attractor states pyboolnet reported for
    this branch must ALSO be fixed points under this project's own from-scratch
    synchronous_step -- verified BEFORE trusting the transient-perturbation result built on
    top of them."""
    text = h4.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    compiled = h1.compile_rules(rules)
    for state_str in (h4.GROWTH_ARREST_STATE, h4.PROLIFERATION_STATE):
        state = dict(zip(h4.PYBOOLNET_NODE_ORDER, (c == "1" for c in state_str)))
        nxt = h1.synchronous_step(state, compiled)
        assert nxt == state, f"{state_str} is not a fixed point"


def test_real_network_transient_ras_clamp_runs_without_crashing():
    """Smoke test against the real data file -- confirms the pipeline executes end-to-end and
    the branch-defining input nodes remain unchanged throughout (a bug could let them drift,
    which would silently invalidate the whole experiment)."""
    result = h4.cmd_run()
    assert len(result["cases"]) >= 1
    for case in result["cases"]:
        assert "final_attractor_type" in case
        assert case["branch_inputs_preserved"] is True
