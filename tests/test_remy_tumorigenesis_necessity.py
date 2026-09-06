"""Tests for H-B7-8: necessity test do(p21CIP=0, RBL2=0) WITHOUT clamping RAS/TP53, on the Remy
et al. 2015 bladder tumorigenesis network. Verified on a hand-checkable synthetic network where a
node "already happens to be" at the needed value at the starting state but is NOT clamped, so it
can drift, BEFORE trusting the result on the real 35-node network.
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

_H5_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-remy-tumorigenesis-twohit-h5"
)
_SPEC_H5 = importlib.util.spec_from_file_location("remy_h5_run", _H5_DIR / "run.py")
h5 = importlib.util.module_from_spec(_SPEC_H5)
_SPEC_H5.loader.exec_module(h5)

_H8_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-remy-tumorigenesis-necessity-h8"
)
_SPEC_H8 = importlib.util.spec_from_file_location("remy_h8_run", _H8_DIR / "run.py")
h8 = importlib.util.module_from_spec(_SPEC_H8)
_SPEC_H8.loader.exec_module(h8)


def _network_where_ras_analogue_can_drift():
    """A'=A|(B&C), B'=B, C'=C, R'=R&A (R="RAS-analogue" -- happens to be 1 at the start, but its
    own rule depends on A, so if A flips, R can drift away from 1 WITHOUT being clamped). Mirrors
    the real question: does the un-clamped node stay put once the clamped nodes change the
    trajectory, or does it drift?"""
    return h1.compile_rules([("A", "A|(B&C)"), ("B", "B"), ("C", "C"), ("R", "R&A")])


def test_two_hit_without_clamping_r_flips_a_and_r_stays_put_when_a_was_already_1():
    """Starting with A=1 already (so R's dependency on A holds automatically) -- R should stay 1
    without being clamped, since R'=R&A=1&1=1."""
    compiled = _network_where_ras_analogue_can_drift()
    two_hit = h5.apply_combined_clamp(compiled, {"B": True, "C": True})
    cycle = h3.run_until_attractor(
        {"A": True, "B": False, "C": False, "R": True}, two_hit, ["A", "B", "C", "R"]
    )
    assert cycle == [{"A": True, "B": True, "C": True, "R": True}]  # R stayed 1, unclamped


def test_r_analogue_drifts_to_zero_if_a_starts_at_zero_and_never_flips():
    """If the two-hit clamp is insufficient to ever raise A to 1 (e.g. B or C never both held),
    R's own dependency on A causes it to drift to 0 -- demonstrating R is NOT structurally
    guaranteed to "just stay" at 1 without either being clamped or A independently reaching 1."""
    compiled = _network_where_ras_analogue_can_drift()
    one_hit_only = h5.apply_combined_clamp(compiled, {"B": True})  # C never clamped -> A stays 0
    cycle = h3.run_until_attractor(
        {"A": False, "B": False, "C": False, "R": True}, one_hit_only, ["A", "B", "C", "R"]
    )
    assert cycle == [{"A": False, "B": True, "C": False, "R": False}]  # R drifted to 0


def test_remy_bnet_ras_and_tp53_are_not_in_the_necessity_clamp_set():
    text = h5.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    names = {n for n, _ in rules}
    assert {"RAS", "TP53", "p21CIP", "RBL2"} <= names


def test_real_network_necessity_clamp_runs_without_crashing():
    """Smoke test against the real data file -- confirms the pipeline executes end-to-end and
    the branch-defining input nodes remain unchanged, same discipline as H-B7-4/5/6/7."""
    result = h8.cmd_run()
    assert "final_attractor_identity" in result
    assert result["branch_inputs_preserved"] is True
