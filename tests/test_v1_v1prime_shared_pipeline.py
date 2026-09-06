"""Regression tests for the V1 run.py refactor that added a `surrogate_fn` parameter (needed so
V1' can reuse V1's analyze_series/run_* functions instead of duplicating them).

Uses tiny synthetic series (not the real datasets) -- fast, and isolates the API contract from
the real-data compute cost already covered by the V1/V1' experiment runs themselves.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_SPEC = importlib.util.spec_from_file_location(
    "v1_run",
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-lakes-tda-ews-surrogate-null-v1"
    / "run.py",
)
v1 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(v1)


def _series():
    rng = np.random.default_rng(7)
    x = np.cumsum(rng.normal(0, 1, 40))
    time_axis = np.arange(len(x), dtype=float)
    window = 20
    return x, window, time_axis


def test_analyze_series_defaults_to_ar1_when_surrogate_fn_omitted():
    x, window, t = _series()
    result = v1.analyze_series(x, window, t)  # no surrogate_fn -- must not error, must default
    assert set(result) == {
        "classical_ac1_crossing",
        "classical_var_crossing",
        "classical_earliest_crossing",
        "tda_betti_crossing",
        "tda_lead",
    }


def test_analyze_series_accepts_iaaft_surrogate_fn():
    x, window, t = _series()
    result = v1.analyze_series(x, window, t, surrogate_fn=v1.obrien.iaaft_surrogate)
    assert set(result) == {
        "classical_ac1_crossing",
        "classical_var_crossing",
        "classical_earliest_crossing",
        "tda_betti_crossing",
        "tda_lead",
    }


def test_cmd_run_signature_accepts_surrogate_fn_and_label():
    import inspect

    sig = inspect.signature(v1.cmd_run)
    assert "surrogate_fn" in sig.parameters
    assert "detection_rule_label" in sig.parameters
    assert sig.parameters["surrogate_fn"].default is None
    assert sig.parameters["detection_rule_label"].default == "AR(1)-surrogate"
