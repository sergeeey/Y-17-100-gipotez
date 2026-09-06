"""Tests for H-B7-2's perturbation (do-operator) pipeline: clamp_rule and
find_attractors_with_membership. Verified on small hand-checkable synthetic networks BEFORE
trusting the result on the real 10-node Fauré et al. 2006 network with Rb/p27 clamped.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-kauffman-cellcycle-perturbation-h2"
)
_SPEC = importlib.util.spec_from_file_location("kauffman_h2_run", _HERE / "run.py")
h2 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(h2)


def test_clamp_rule_replaces_only_the_named_node():
    compiled = h2.h1.compile_rules([("A", "!A"), ("B", "A")])
    clamped = h2.clamp_rule(compiled, "A", False)
    # A's rule is now the constant FALSE
    assert h2.h1.evaluate_expression(clamped["A"], {"A": True, "B": True}) is False
    assert h2.h1.evaluate_expression(clamped["A"], {"A": False, "B": False}) is False
    # B's rule is untouched
    assert clamped["B"] is compiled["B"]


def test_clamp_rule_raises_on_unknown_node():
    compiled = h2.h1.compile_rules([("A", "!A")])
    with pytest.raises(KeyError):
        h2.clamp_rule(compiled, "NoSuchNode", True)


def test_find_attractors_with_membership_matches_h1_on_not_gate():
    """Same NOT-gate oscillator used in H-B7-1's own tests: A'=!A, one period-2 attractor
    covering both states."""
    compiled = h2.h1.compile_rules([("A", "!A")])
    result = h2.find_attractors_with_membership(["A"], compiled)
    assert result["n_attractors"] == 1
    (attr,) = result["attractors"]
    assert attr["type"] == "complex" and attr["period"] == 2
    # both states map to the same (only) attractor
    assert set(result["initial_state_to_attractor"].values()) == {0}
    assert set(result["initial_state_to_attractor"].keys()) == {"0", "1"}


def test_find_attractors_with_membership_matches_h1_on_merge_case():
    """A'=A, B'=A: (0,0) and (0,1) converge to fixed point (0,0); (1,0) and (1,1) converge to
    (1,1). Membership map must correctly attribute each of the 4 initial states."""
    compiled = h2.h1.compile_rules([("A", "A"), ("B", "A")])
    result = h2.find_attractors_with_membership(["A", "B"], compiled)
    assert result["n_attractors"] == 2
    membership = result["initial_state_to_attractor"]
    # states starting with A=0 (first char) must share one attractor index
    a0_targets = {idx for s, idx in membership.items() if s[0] == "0"}
    a1_targets = {idx for s, idx in membership.items() if s[0] == "1"}
    assert len(a0_targets) == 1
    assert len(a1_targets) == 1
    assert a0_targets != a1_targets


def test_clamping_changes_dynamics_on_a_hand_verifiable_synthetic_case():
    """A'=!A (free oscillator), B'=A&B. Unperturbed: A oscillates 0/1/0/1..., so B'=A&B is NOT
    a simple fixed rule -- but with do(A:=0), B'=A&B=0&B=False ALWAYS, so B converges to 0
    regardless of start, and the whole system has exactly ONE point attractor (0,0) with
    basin_size=4 (all 4 states funnel into it). This directly exercises the clamp end-to-end on
    a case simple enough to verify by hand."""
    compiled = h2.h1.compile_rules([("A", "!A"), ("B", "A&B")])
    clamped = h2.clamp_rule(compiled, "A", False)
    result = h2.find_attractors_with_membership(["A", "B"], clamped)
    assert result["n_attractors"] == 1
    (attr,) = result["attractors"]
    assert attr["type"] == "point"
    assert attr["states"] == ["00"]
    assert len(result["initial_state_to_attractor"]) == 4
    assert set(result["initial_state_to_attractor"].values()) == {0}


def test_real_network_rb_and_p27_clamp_runs_without_crashing():
    """Smoke test against the real data file with both interventions -- confirms the full
    cmd_run pipeline (parse -> clamp -> enumerate -> filter to CycD=0) executes and returns the
    expected key structure, without asserting the real biological OUTCOME here (that's the real
    run, checked and interpreted in decision.md)."""
    result = h2.cmd_run()
    assert set(result["interventions"].keys()) == {"do(Rb=0)", "do(p27=0)"}
    for intervention_result in result["interventions"].values():
        assert "cycd0_reaches_complex_attractor" in intervention_result
        assert isinstance(intervention_result["cycd0_reaches_complex_attractor"], bool)
