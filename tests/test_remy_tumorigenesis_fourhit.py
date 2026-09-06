"""Tests for H-B7-7: combined permanent do(RAS=1, TP53=0, p21CIP=0, RBL2=0) four-hit perturbation
on the Remy et al. 2015 bladder tumorigenesis network. Verified on a hand-checkable synthetic
"genuine four-hit" network BEFORE trusting the result on the real 35-node network.
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

_H7_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-remy-tumorigenesis-fourhit-h7"
)
_SPEC_H7 = importlib.util.spec_from_file_location("remy_h7_run", _H7_DIR / "run.py")
h7 = importlib.util.module_from_spec(_SPEC_H7)
_SPEC_H7.loader.exec_module(h7)


def _genuine_four_hit_network():
    """A'=A|(B&C&!D&!E), B'=B, C'=C, D'=D, E'=E: A flips to 1 only if B AND C are held at 1 AND
    BOTH D and E are held at 0 -- two independent redundant blockers (D, E) mirror H-B7-6's
    Growth_arrest = p21CIP|RBL2|RB1 three-way OR (here reduced to two active blockers, since the
    third -- RB1's analogue -- is not directly targeted, matching this experiment's own scope).
    Hand-verified below before trusting the real 35-node network's quadruple clamp."""
    return h1.compile_rules(
        [("A", "A|(B&C&!D&!E)"), ("B", "B"), ("C", "C"), ("D", "D"), ("E", "E")]
    )


def test_three_hit_alone_is_insufficient_while_one_blocker_remains():
    compiled = _genuine_four_hit_network()
    three_hit = h5.apply_combined_clamp(compiled, {"B": True, "C": True, "D": False})
    cycle = h3.run_until_attractor(
        {"A": False, "B": False, "C": False, "D": True, "E": True},
        three_hit,
        ["A", "B", "C", "D", "E"],
    )
    assert cycle == [{"A": False, "B": True, "C": True, "D": False, "E": True}]  # A stays 0


def test_four_hit_removes_both_blockers_and_flips_the_synthetic_network():
    compiled = _genuine_four_hit_network()
    four_hit = h5.apply_combined_clamp(compiled, {"B": True, "C": True, "D": False, "E": False})
    cycle = h3.run_until_attractor(
        {"A": False, "B": False, "C": False, "D": True, "E": True},
        four_hit,
        ["A", "B", "C", "D", "E"],
    )
    assert cycle == [{"A": True, "B": True, "C": True, "D": False, "E": False}]  # A flips to 1


def test_apply_combined_clamp_helper_handles_four_simultaneous_clamps():
    compiled = _genuine_four_hit_network()
    manual = h2.clamp_rule(
        h2.clamp_rule(h2.clamp_rule(h2.clamp_rule(compiled, "B", True), "C", True), "D", False),
        "E",
        False,
    )
    via_helper = h5.apply_combined_clamp(compiled, {"B": True, "C": True, "D": False, "E": False})
    for node in ("A", "B", "C", "D", "E"):
        assert manual[node] == via_helper[node]


def test_remy_bnet_still_parses_and_rbl2_is_a_valid_target():
    text = h5.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    names = {n for n, _ in rules}
    assert {"RAS", "TP53", "p21CIP", "RBL2"} <= names


def test_real_network_four_hit_clamp_runs_without_crashing():
    """Smoke test against the real data file -- confirms the pipeline executes end-to-end and
    the branch-defining input nodes remain unchanged, same discipline as H-B7-4/5/6."""
    result = h7.cmd_run()
    assert "final_attractor_identity" in result
    assert result["branch_inputs_preserved"] is True
