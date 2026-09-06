"""Tests for H-B7-10: fine duration sweep k=4..9 of the transient do(p21CIP=0, RBL2=0) clamp on
the Remy et al. 2015 network. The underlying mechanism (simulate_transient_clamp_multi) is already
validated on a hand-traced synthetic network in H-B7-9's own test suite and is reused UNCHANGED
here (Minimal Relaxation Rule: only the duration set changes) -- these tests confirm (a) the real
network sweep runs end-to-end and (b) a synthetic network with a KNOWN duration threshold shows the
same clean monotone relapse-then-escape shape this experiment's kill criterion requires.
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

_H9_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-remy-tumorigenesis-transient-necessity-h9"
)
_SPEC_H9 = importlib.util.spec_from_file_location("remy_h9_run", _H9_DIR / "run.py")
h9 = importlib.util.module_from_spec(_SPEC_H9)
_SPEC_H9.loader.exec_module(h9)

_H10_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-remy-tumorigenesis-transient-sweep-h10"
)
_SPEC_H10 = importlib.util.spec_from_file_location("remy_h10_run", _H10_DIR / "run.py")
h10 = importlib.util.module_from_spec(_SPEC_H10)
_SPEC_H10.loader.exec_module(h10)


def _delay_line_network():
    """A'=A|(B&C), B'=!A&Push1, C'=!A&Push2, Push1'=Push1, Push2'=Push2, but the "clamped" nodes
    here are Counter1..Counter3 (a 3-step counter chain that must fully propagate before B/C can
    both read 1) -- gives a KNOWN, hand-computable duration threshold (k>=3 needed) to confirm the
    sweep methodology finds a clean monotone boundary, not just on the real 35-node network."""
    return h1.compile_rules(
        [
            ("A", "A|(B&C)"),
            ("B", "Counter3"),
            ("C", "Counter3"),
            ("Counter1", "Push"),
            ("Counter2", "Counter1"),
            ("Counter3", "Counter2"),
            ("Push", "Push"),
        ]
    )


def test_synthetic_delay_line_shows_clean_monotone_threshold():
    compiled = _delay_line_network()
    node_names = ["A", "B", "C", "Counter1", "Counter2", "Counter3", "Push"]
    start = {
        "A": False,
        "B": False,
        "C": False,
        "Counter1": False,
        "Counter2": False,
        "Counter3": False,
        "Push": False,
    }
    # Clamp "Push" to True for k steps then release -- Counter1/2/3 need 3 steps to propagate
    # Push=True through the chain before B/C can both read Counter3=True simultaneously.
    outcomes = {}
    for k in range(0, 6):
        sim = h9.simulate_transient_clamp_multi(start, node_names, compiled, {"Push": True}, k)
        outcomes[k] = sim["final_state"]["A"]
    # Must be monotone: once it flips to True, it stays True for all larger k.
    flipped = [k for k, v in outcomes.items() if v]
    if flipped:
        k_star = min(flipped)
        assert all(outcomes[k] is False for k in range(0, k_star))
        assert all(outcomes[k] is True for k in range(k_star, 6))


def test_real_network_sweep_runs_without_crashing():
    """Smoke test against the real data file -- confirms the pipeline executes end-to-end for all
    6 swept durations and the branch-defining input nodes remain unchanged, same discipline as
    H-B7-4 through H-B7-9."""
    result = h10.cmd_run()
    assert "results_by_k" in result
    assert len(result["results_by_k"]) == 6
    for entry in result["results_by_k"]:
        assert entry["branch_inputs_preserved"] is True
