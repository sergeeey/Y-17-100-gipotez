"""Tests for H-B7-5: combined permanent do(RAS=1, TP53=0) two-hit perturbation on the Remy et
al. 2015 bladder tumorigenesis network. Verified on a hand-checkable synthetic "genuine two-hit"
network BEFORE trusting the result on the real 35-node network.
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


def _genuine_two_hit_network():
    """A'=A|(B&C), B'=B, C'=C: A only flips to 1 if BOTH B and C are held at 1 -- a single
    clamp of either alone is provably insufficient. Hand-verified below before trusting the
    real 35-node network's combined clamp."""
    return h1.compile_rules([("A", "A|(B&C)"), ("B", "B"), ("C", "C")])


def test_single_hit_alone_is_insufficient_on_the_synthetic_two_hit_network():
    compiled = _genuine_two_hit_network()
    clamped_b_only = h2.clamp_rule(compiled, "B", True)
    cycle = h3.run_until_attractor(
        {"A": False, "B": False, "C": False}, clamped_b_only, ["A", "B", "C"]
    )
    assert cycle == [{"A": False, "B": True, "C": False}]  # A stays 0


def test_combined_two_hit_flips_the_synthetic_network():
    compiled = _genuine_two_hit_network()
    combined = h2.clamp_rule(compiled, "B", True)
    combined = h2.clamp_rule(combined, "C", True)
    cycle = h3.run_until_attractor({"A": False, "B": False, "C": False}, combined, ["A", "B", "C"])
    assert cycle == [{"A": True, "B": True, "C": True}]  # A flips to 1


def test_apply_combined_clamp_helper_matches_manual_double_clamp_rule():
    compiled = _genuine_two_hit_network()
    manual = h2.clamp_rule(h2.clamp_rule(compiled, "B", True), "C", True)
    via_helper = h5.apply_combined_clamp(compiled, {"B": True, "C": True})
    for node in ("A", "B", "C"):
        assert manual[node] == via_helper[node]


def test_remy_bnet_still_parses_and_ras_tp53_are_valid_targets():
    text = h5.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    names = {n for n, _ in rules}
    assert {"RAS", "TP53"} <= names


def test_real_network_combined_clamp_runs_without_crashing():
    """Smoke test against the real data file -- confirms the pipeline executes end-to-end and
    the branch-defining input nodes remain unchanged (checked explicitly, same discipline as
    H-B7-4, given a bug could let them drift under a combined clamp too)."""
    result = h5.cmd_run()
    assert "final_attractor_identity" in result
    assert result["branch_inputs_preserved"] is True
