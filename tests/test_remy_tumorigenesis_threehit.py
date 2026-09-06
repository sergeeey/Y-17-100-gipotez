"""Tests for H-B7-6: combined permanent do(RAS=1, TP53=0, p21CIP=0) three-hit perturbation on the
Remy et al. 2015 bladder tumorigenesis network. Verified on a hand-checkable synthetic "genuine
three-hit" network BEFORE trusting the result on the real 35-node network.
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

_H2_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-kauffman-cellcycle-perturbation-h2"
)
_SPEC_H2 = importlib.util.spec_from_file_location("kauffman_h2_run", _H2_DIR / "run.py")
h2 = importlib.util.module_from_spec(_SPEC_H2)
_SPEC_H2.loader.exec_module(h2)

_H3_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-kauffman-cellcycle-transient-h3"
)
_SPEC_H3 = importlib.util.spec_from_file_location("kauffman_h3_run", _H3_DIR / "run.py")
h3 = importlib.util.module_from_spec(_SPEC_H3)
_SPEC_H3.loader.exec_module(h3)

_H5_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-remy-tumorigenesis-twohit-h5"
)
_SPEC_H5 = importlib.util.spec_from_file_location("remy_h5_run", _H5_DIR / "run.py")
h5 = importlib.util.module_from_spec(_SPEC_H5)
_SPEC_H5.loader.exec_module(h5)

_H6_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-remy-tumorigenesis-threehit-h6"
)
_SPEC_H6 = importlib.util.spec_from_file_location("remy_h6_run", _H6_DIR / "run.py")
h6 = importlib.util.module_from_spec(_SPEC_H6)
_SPEC_H6.loader.exec_module(h6)


def _genuine_three_hit_network():
    """A'=A|(B&C&!D), B'=B, C'=C, D'=D: A flips to 1 only if B AND C are held at 1 AND D is held
    at 0 -- a redundant blocker D means clamping B+C alone (the "two-hit" case) is provably
    insufficient while D=1, mirroring H-B7-5's p21CIP-as-redundant-blocker finding. Hand-verified
    below before trusting the real 35-node network's triple clamp."""
    return h1.compile_rules([("A", "A|(B&C&!D)"), ("B", "B"), ("C", "C"), ("D", "D")])


def test_two_hit_alone_is_insufficient_while_the_redundant_blocker_is_active():
    compiled = _genuine_three_hit_network()
    two_hit = h5.apply_combined_clamp(compiled, {"B": True, "C": True})
    cycle = h3.run_until_attractor(
        {"A": False, "B": False, "C": False, "D": True}, two_hit, ["A", "B", "C", "D"]
    )
    assert cycle == [{"A": False, "B": True, "C": True, "D": True}]  # A stays 0, D still blocks


def test_three_hit_removes_the_blocker_and_flips_the_synthetic_network():
    compiled = _genuine_three_hit_network()
    three_hit = h5.apply_combined_clamp(compiled, {"B": True, "C": True, "D": False})
    cycle = h3.run_until_attractor(
        {"A": False, "B": False, "C": False, "D": True}, three_hit, ["A", "B", "C", "D"]
    )
    assert cycle == [{"A": True, "B": True, "C": True, "D": False}]  # A flips to 1


def test_apply_combined_clamp_helper_handles_three_simultaneous_clamps():
    compiled = _genuine_three_hit_network()
    manual = h2.clamp_rule(h2.clamp_rule(h2.clamp_rule(compiled, "B", True), "C", True), "D", False)
    via_helper = h5.apply_combined_clamp(compiled, {"B": True, "C": True, "D": False})
    for node in ("A", "B", "C", "D"):
        assert manual[node] == via_helper[node]


def test_remy_bnet_still_parses_and_p21cip_is_a_valid_target():
    text = h5.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    names = {n for n, _ in rules}
    assert {"RAS", "TP53", "p21CIP"} <= names


def test_real_network_triple_clamp_runs_without_crashing():
    """Smoke test against the real data file -- confirms the pipeline executes end-to-end and
    the branch-defining input nodes remain unchanged, same discipline as H-B7-4/H-B7-5."""
    result = h6.cmd_run()
    assert "final_attractor_identity" in result
    assert result["branch_inputs_preserved"] is True
