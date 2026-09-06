"""Tests for H-B7-1's Boolean-network pipeline (parsing, evaluation, synchronous update,
brute-force attractor search), verified on small hand-checkable synthetic networks BEFORE
trusting the result on the real 10-node Fauré et al. 2006 network.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-kauffman-cellcycle-attractors-h1"
)
_SPEC = importlib.util.spec_from_file_location("kauffman_run", _HERE / "run.py")
kc = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(kc)


def test_parse_bnet_skips_header_and_comments():
    text = """targets, factors

# a comment line
A,    B&!C
B,    A|C
"""
    rules = kc.parse_bnet(text)
    assert rules == [("A", "B&!C"), ("B", "A|C")]


def test_evaluate_expression_matches_truth_table():
    compiled = kc.compile_rules([("X", "A&!B | C")])
    expr = compiled["X"]
    assert kc.evaluate_expression(expr, {"A": True, "B": False, "C": False}) is True
    assert kc.evaluate_expression(expr, {"A": True, "B": True, "C": False}) is False
    assert kc.evaluate_expression(expr, {"A": False, "B": False, "C": True}) is True
    assert kc.evaluate_expression(expr, {"A": False, "B": False, "C": False}) is False


def test_synchronous_step_updates_all_nodes_simultaneously():
    compiled = kc.compile_rules([("A", "B"), ("B", "!A")])
    # A=0,B=1 -> A'=B=1, B'=!A=1 (uses OLD A, not the just-computed new A)
    nxt = kc.synchronous_step({"A": False, "B": True}, compiled)
    assert nxt == {"A": True, "B": True}


def test_find_attractors_not_gate_gives_one_period_2_cycle():
    """Classic single-node oscillator: A' = !A. No point attractor -- both states 0 and 1
    belong to the same period-2 cycle. Basin size = 2 (the whole state space)."""
    compiled = kc.compile_rules([("A", "!A")])
    result = kc.find_attractors(["A"], compiled)
    assert result["n_states_total"] == 2
    assert result["n_attractors"] == 1
    (attr,) = result["attractors"]
    assert attr["type"] == "complex"
    assert attr["period"] == 2
    assert attr["basin_size"] == 2


def test_find_attractors_identity_gives_two_point_attractors():
    """A' = A: every state is already a fixed point. Two point attractors, basin_size=1 each."""
    compiled = kc.compile_rules([("A", "A")])
    result = kc.find_attractors(["A"], compiled)
    assert result["n_attractors"] == 2
    assert all(a["type"] == "point" and a["basin_size"] == 1 for a in result["attractors"])


def test_find_attractors_merges_multiple_initial_states_into_same_point_attractor():
    """A'=A (input), B'=A: (0,0) and (0,1) both converge to fixed point (0,0); (1,0) and (1,1)
    both converge to fixed point (1,1). Tests the 'trajectory feeds into an already-known
    attractor' merge path, not just the 'discover a brand-new cycle' path."""
    compiled = kc.compile_rules([("A", "A"), ("B", "A")])
    result = kc.find_attractors(["A", "B"], compiled)
    assert result["n_states_total"] == 4
    assert result["n_attractors"] == 2
    basins = sorted(a["basin_size"] for a in result["attractors"])
    assert basins == [2, 2]
    assert all(a["type"] == "point" for a in result["attractors"])


def test_real_bnet_file_parses_to_ten_named_nodes():
    """Smoke test against the real data file -- confirms it parses without touching the
    Fauré-specific attractor CLAIM (that's the real run, checked separately in decision.md)."""
    text = kc.DATA.read_text(encoding="utf-8")
    rules = kc.parse_bnet(text)
    names = [name for name, _ in rules]
    assert len(names) == 10
    assert set(names) == {
        "CycD",
        "Cdc20",
        "CycA",
        "CycB",
        "CycE",
        "E2F",
        "Rb",
        "UbcH10",
        "cdh1",
        "p27",
    }
