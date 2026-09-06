"""Regression test for H-B3-1f (V3): the descriptive join must reproduce the PARENT experiments'
own already-committed numbers verbatim, not recompute or approximate them.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_HERE = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-lakes-tda-ews-descriptive-v3"
)
_SPEC = importlib.util.spec_from_file_location("v3_run", _HERE / "run.py")
v3 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(v3)


def test_join_reproduces_known_v1prime_peter_dosat_lead_verbatim():
    out = v3.cmd_run()
    row = out["table"]["peterlake_Peter_doSat"]
    # H-B3-1d's own committed metrics/run.json: tda_lead ~= +13.0 days for Peter doSat under IAAFT.
    assert abs(row["v1prime_iaaft_null"]["lead"] - 12.999999999976808) < 1e-6


def test_join_reproduces_known_raw_lower_zurich_lead_verbatim():
    out = v3.cmd_run()
    row = out["table"]["obrien_lower_zurich"]
    # H-B3-1b's own committed metrics/run.json: 24.0 months, positive, correct direction.
    assert row["raw_fixed_threshold"]["lead"] == 24.0
    assert row["raw_fixed_threshold"]["floor_fp_rate"] == 0.8333333333333334


def test_all_9_series_present_and_labeled():
    out = v3.cmd_run()
    assert len(out["table"]) == 9
    labels = {row["label"] for row in out["table"].values()}
    assert "Lower Zurich" in labels
    assert "Paul doSat" in labels


def test_no_verdict_field_present_descriptive_only():
    """This experiment must not smuggle in a binary pass/fail verdict -- it is descriptive-only
    per claim.md's explicit L0 reclassification."""
    out = v3.cmd_run()
    assert "verdict" not in out
