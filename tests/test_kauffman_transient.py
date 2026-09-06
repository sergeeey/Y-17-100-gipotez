"""Tests for H-B7-3's transient-perturbation ("clamp for k steps, then release") pipeline.
Verified on small hand-checkable synthetic networks BEFORE trusting the result on the real
10-node Fauré et al. 2006 network.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-kauffman-cellcycle-transient-h3"
)
_SPEC = importlib.util.spec_from_file_location("kauffman_h3_run", _HERE / "run.py")
h3 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(h3)


def test_run_until_attractor_finds_not_gate_period_2_cycle():
    compiled = h3.h1.compile_rules([("A", "!A")])
    cycle = h3.run_until_attractor({"A": False}, compiled, ["A"])
    assert len(cycle) == 2
    assert {tuple(s.values()) for s in cycle} == {(False,), (True,)}


def test_run_until_attractor_finds_identity_point_attractor_immediately():
    compiled = h3.h1.compile_rules([("A", "A")])
    cycle = h3.run_until_attractor({"A": True}, compiled, ["A"])
    assert cycle == [{"A": True}]


def test_run_until_attractor_raises_if_no_cycle_within_max_steps():
    """Sanity check on the guard itself: a max_steps too small for even a trivial 2-node
    system's cycle should raise, not silently return a wrong answer."""
    import pytest

    compiled = h3.h1.compile_rules([("A", "!A")])
    with pytest.raises(RuntimeError):
        h3.run_until_attractor({"A": False}, compiled, ["A"], max_steps=0)


def test_simulate_transient_clamp_hand_verified_case():
    """A'=!A (free oscillator), B'=A&B, clamp A=0 for k=3 steps from (A=0,B=0), then release.
    Hand trace: during the clamp, A stays 0 (forced) and B'=A&B=0 stays 0 -> state stays (0,0)
    for all 3 clamp steps. On release from (0,0) under the TRUE rules (A'=!A, B'=A&B):
    (0,0) -> (1,0) -> (0,0) -> ... a period-2 cycle {(0,0),(1,0)}, NOT the trivial single fixed
    point the clamp alone would suggest -- because releasing A lets it start oscillating again."""
    compiled = h3.h1.compile_rules([("A", "!A"), ("B", "A&B")])
    result = h3.simulate_transient_clamp(
        {"A": False, "B": False}, ["A", "B"], compiled, {"A": False}, k_steps=3
    )
    assert result["type"] == "complex"
    assert result["period"] == 2
    assert set(result["states"]) == {"00", "10"}


def test_simulate_transient_clamp_zero_duration_clamp_is_a_noop():
    """k_steps=0 should behave identically to never having clamped at all -- the clamped-state
    override still applies to the INITIAL state (per simulate_transient_clamp's own contract),
    but zero clamp iterations means the very next step already uses the true rule."""
    compiled = h3.h1.compile_rules([("A", "A")])  # identity: point attractor at whatever A is
    result = h3.simulate_transient_clamp({"A": True}, ["A"], compiled, {"A": False}, k_steps=0)
    # A is forced to False as the initial override, then immediately released; identity rule
    # keeps it at False forever -> point attractor "0"
    assert result["type"] == "point"
    assert result["states"] == ["0"]


def test_real_network_all_cases_run_without_crashing_and_report_the_expected_fields():
    """Smoke test against the real data file with the full test matrix -- confirms the pipeline
    executes end-to-end; the actual biological OUTCOME (does it return to quiescence) is
    interpreted in decision.md, not asserted blindly here."""
    result = h3.cmd_run()
    assert len(result["cases"]) == 6
    for case in result["cases"]:
        assert "returned_to_wild_type_quiescence" in case
        assert isinstance(case["returned_to_wild_type_quiescence"], bool)
    assert "all_cases_returned_to_quiescence" in result
