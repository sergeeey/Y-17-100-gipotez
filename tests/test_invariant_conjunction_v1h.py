"""Regression test for H-B3-1h: the conjunction join must reproduce V1's and V1g's own
already-committed numbers verbatim, not recompute or approximate them.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-lakes-tda-ews-invariant-conjunction"
)
_SPEC = importlib.util.spec_from_file_location("v1h_run", _HERE / "run.py")
v1h = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(v1h)


def test_all_9_series_present():
    out = v1h.cmd_run()
    assert len(out["table"]) == 9


def test_peter_dosat_crosses_both_invariants():
    out = v1h.cmd_run()
    row = out["table"]["peterlake_Peter_doSat"]
    assert row["entropy_tda_crosses"] is True
    assert row["total_persistence_tda_crosses"] is True
    assert row["conjunction_both_cross"] is True
    assert out["peter_dosat_survives_conjunction"] is True


def test_paul_chl_conjunction_reflects_source_data():
    out = v1h.cmd_run()
    row = out["table"]["peterlake_Paul_chl"]
    # V1 (entropy): Paul chl WAS a false positive (crossed). V1g (total persistence): did NOT cross.
    assert row["entropy_tda_crosses"] is True
    assert row["total_persistence_tda_crosses"] is False
    assert row["conjunction_both_cross"] is False  # conjunction requires BOTH


def test_entropy_alone_tda_only_crossing_count():
    """NOTE: this counts ONLY tda_betti_crossing != None, not V1's own combined
    classical-OR-TDA false_positive field (which was 5/5) -- a deliberately narrower,
    TDA-vs-TDA comparison for this conjunction experiment. Verified against the source data:
    3 of 5 negative controls had a TDA (entropy) crossing specifically."""
    out = v1h.cmd_run()
    assert out["n_false_positives_entropy_alone"] == 3


def test_total_persistence_alone_tda_only_crossing_count():
    out = v1h.cmd_run()
    assert out["n_false_positives_total_persistence_alone"] == 4
