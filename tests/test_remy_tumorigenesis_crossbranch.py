"""Tests for H-B7-11: cross-branch generalization test of the permanent do(p21CIP=0, RBL2=0)
clamp on the SECOND phenotype-divergent branch of the Remy et al. 2015 network. The underlying
clamp mechanism (apply_combined_clamp) is already validated in H-B7-5's own test suite and reused
UNCHANGED here -- these tests confirm (a) the branch scoping data is internally consistent and
(b) the real cross-branch run executes end-to-end.
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

_H11_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-remy-tumorigenesis-crossbranch-h11"
)
_SPEC_H11 = importlib.util.spec_from_file_location("remy_h11_run", _H11_DIR / "run.py")
h11 = importlib.util.module_from_spec(_SPEC_H11)
_SPEC_H11.loader.exec_module(h11)


def test_second_branch_states_differ_from_first_branch_by_exactly_one_bit():
    """The two branches differ only in EGFR_stimulus -- their GA/PR state strings should differ
    at exactly one position (verified independently during scoping; re-checked here as a
    regression guard)."""
    from_h4 = h11.h4

    def diff_positions(a, b):
        return [i for i, (x, y) in enumerate(zip(a, b)) if x != y]

    ga_diffs = diff_positions(from_h4.GROWTH_ARREST_STATE, h11.GROWTH_ARREST_STATE_2)
    pr_diffs = diff_positions(from_h4.PROLIFERATION_STATE, h11.PROLIFERATION_STATE_2)
    assert len(ga_diffs) == 1
    assert len(pr_diffs) == 1
    assert ga_diffs == pr_diffs  # same node (EGFR_stimulus) differs in both


def test_second_branch_growth_arrest_state_is_a_genuine_fixed_point():
    """Sanity check: running the WT rules from GROWTH_ARREST_STATE_2 (this branch's own inputs)
    should stay at GROWTH_ARREST_STATE_2 -- confirms it is a real fixed point, not a typo'd
    string, before trusting the perturbation result."""
    text = h11.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wt = h1.compile_rules(rules)
    start = dict(zip(h11.PYBOOLNET_NODE_ORDER, (c == "1" for c in h11.GROWTH_ARREST_STATE_2)))
    cycle = h11.h3.run_until_attractor(start, wt, node_names)
    final_str = "".join("1" if cycle[0][n] else "0" for n in h11.PYBOOLNET_NODE_ORDER)
    assert final_str == h11.GROWTH_ARREST_STATE_2


def test_real_crossbranch_run_runs_without_crashing():
    """Smoke test against the real data file -- confirms the pipeline executes end-to-end on the
    second branch and the branch-defining input nodes remain unchanged."""
    result = h11.cmd_run()
    assert "final_attractor_identity" in result
    assert result["branch_inputs_preserved"] is True
