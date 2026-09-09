import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    PROLIFERATION_STATE,
    PROLIFERATION_STATE_2,
    PYBOOLNET_NODE_ORDER,
    dict_to_state_str,
    state_str_to_dict,
)


def test_state_str_round_trip():
    """Hand-verified: converting a state string to a dict and back must be lossless."""
    d = state_str_to_dict(PROLIFERATION_STATE)
    assert dict_to_state_str(d) == PROLIFERATION_STATE


def test_proliferation_state_has_CyclinD1_false_CyclinE1_true():
    """Hand-derivation from claim.md, computationally verified: at PROLIFERATION_STATE,
    index 9 (CyclinD1) must be '0' and index 10 (CyclinE1) must be '1'."""
    assert PYBOOLNET_NODE_ORDER[9] == "CyclinD1"
    assert PYBOOLNET_NODE_ORDER[10] == "CyclinE1"
    d = state_str_to_dict(PROLIFERATION_STATE)
    assert d["CyclinD1"] is False
    assert d["CyclinE1"] is True


def test_proliferation_state_2_differs_from_state_1_at_exactly_one_bit():
    """H-B7-11's own established finding: PROLIFERATION_STATE and PROLIFERATION_STATE_2 differ
    at exactly one bit (EGFR_stimulus, index 17) -- computationally re-verified here as a
    Substrate Gate sanity check before trusting either constant."""
    assert PYBOOLNET_NODE_ORDER[17] == "EGFR_stimulus"
    diffs = [
        i
        for i in range(len(PROLIFERATION_STATE))
        if PROLIFERATION_STATE[i] != PROLIFERATION_STATE_2[i]
    ]
    assert diffs == [17]


def test_proliferation_state_has_RBL2_false():
    """Ground truth: RBL2 must be False at PROLIFERATION_STATE (Proliferation = CyclinE1 |
    CyclinA, both of which require !RBL2 in their own rules) -- hand-verified against the
    known state string directly."""
    d = state_str_to_dict(PROLIFERATION_STATE)
    assert d["RBL2"] is False
