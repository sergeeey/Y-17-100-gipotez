"""Tests for H-B7-12: transient do(p21CIP=0, RBL2=0) sweep on the SECOND branch (H-B7-11), to
check whether H-B7-10's exact threshold k*=5 generalizes. Reuses H-B7-9's already-validated
simulate_transient_clamp_multi UNCHANGED -- these tests confirm the second-branch smoke run
executes end-to-end and the branch-defining inputs are preserved.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_H12_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-remy-tumorigenesis-crossbranch-transient-h12"
)
_SPEC_H12 = importlib.util.spec_from_file_location("remy_h12_run", _H12_DIR / "run.py")
h12 = importlib.util.module_from_spec(_SPEC_H12)
_SPEC_H12.loader.exec_module(h12)


def test_second_branch_growth_arrest_state_is_a_genuine_fixed_point_under_wt_rules():
    """Sanity check: running WT rules from GROWTH_ARREST_STATE_2 (this branch's own inputs)
    should stay put -- confirms it's a real fixed point before trusting the sweep result."""
    text = h12.DATA.read_text(encoding="utf-8")
    rules = h12.h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wt = h12.h1.compile_rules(rules)
    start = dict(zip(h12.PYBOOLNET_NODE_ORDER, (c == "1" for c in h12.GROWTH_ARREST_STATE_2)))
    cycle = h12.h3.run_until_attractor(start, wt, node_names)
    final_str = "".join("1" if cycle[0][n] else "0" for n in h12.PYBOOLNET_NODE_ORDER)
    assert final_str == h12.GROWTH_ARREST_STATE_2


def test_real_crossbranch_transient_sweep_runs_without_crashing():
    """Smoke test against the real data file -- confirms the pipeline executes end-to-end for all
    swept durations on the second branch and the branch-defining input nodes remain unchanged."""
    result = h12.cmd_run()
    assert "results_by_k" in result
    assert len(result["results_by_k"]) == len(h12.TESTED_DURATIONS)
    for entry in result["results_by_k"]:
        assert entry["branch_inputs_preserved"] is True
