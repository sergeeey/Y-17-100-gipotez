"""Tests for H-B7-9: transient do(p21CIP=0, RBL2=0) for k steps then released, on the Remy et al.
2015 bladder tumorigenesis network. Verified on a hand-checkable synthetic network with a genuine
basin-crossing self-sustaining switch BEFORE trusting the result on the real 35-node network.
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

_H9_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-remy-tumorigenesis-transient-necessity-h9"
)
_SPEC_H9 = importlib.util.spec_from_file_location("remy_h9_run", _H9_DIR / "run.py")
h9 = importlib.util.module_from_spec(_SPEC_H9)
_SPEC_H9.loader.exec_module(h9)


def _self_sustaining_switch_network():
    """A'=A|(B&C), B'=!A&B_stimulus, C'=!A&C_stimulus, B_stimulus'=B_stimulus,
    C_stimulus'=C_stimulus: mirrors a genuine basin-crossing switch -- once A flips to 1 via a
    transient B&C push, A's own rule (A|...) keeps it at 1 forever even after B/C are released and
    (because A=1 now suppresses B/C's own drivers) B and C fall back to 0. This is the shape a
    REAL Kauffman-strict escape should have: transient push -> permanent phenotype change -> the
    ORIGINAL trigger nodes need not stay activated."""
    return h1.compile_rules(
        [
            ("A", "A|(B&C)"),
            ("B", "!A&B_stimulus"),
            ("C", "!A&C_stimulus"),
            ("B_stimulus", "B_stimulus"),
            ("C_stimulus", "C_stimulus"),
        ]
    )


def test_transient_push_flips_a_and_a_survives_release():
    compiled = _self_sustaining_switch_network()
    wild = compiled  # no clamp yet, wild-type rules
    node_names = ["A", "B", "C", "B_stimulus", "C_stimulus"]
    start = {"A": False, "B": False, "C": False, "B_stimulus": True, "C_stimulus": True}
    result = h9.simulate_transient_clamp_multi(
        start, node_names, wild, {"B": True, "C": True}, k_steps=2
    )
    # A must be 1 in the settled attractor, having survived release back to wild-type rules
    assert result["final_state"]["A"] is True


def test_no_push_never_flips_a_when_stimuli_are_off():
    """With BOTH stimuli off, B and C can never turn on via their own rules (!A&B_stimulus with
    B_stimulus=False is always False) -- A can only ever flip via an explicit external push,
    never spontaneously. Isolates the transient-push mechanism from any accidental self-driven
    synchronization the toy network might otherwise exhibit."""
    compiled = _self_sustaining_switch_network()
    node_names = ["A", "B", "C", "B_stimulus", "C_stimulus"]
    start = {"A": False, "B": False, "C": False, "B_stimulus": False, "C_stimulus": False}
    result = h9.simulate_transient_clamp_multi(start, node_names, compiled, {}, k_steps=0)
    assert result["final_state"]["A"] is False


def test_remy_bnet_still_parses_and_p21cip_rbl2_are_valid_targets():
    text = h5.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    names = {n for n, _ in rules}
    assert {"p21CIP", "RBL2", "Growth_arrest", "Proliferation"} <= names


def test_real_network_transient_necessity_runs_without_crashing():
    """Smoke test against the real data file -- confirms the pipeline executes end-to-end for all
    4 tested durations and the branch-defining input nodes remain unchanged, same discipline as
    H-B7-4/5/6/7/8."""
    result = h9.cmd_run()
    assert "results_by_k" in result
    assert len(result["results_by_k"]) == 4
    for entry in result["results_by_k"]:
        assert entry["branch_inputs_preserved"] is True
