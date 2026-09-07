"""Tests for H-B3-1l: peak-tau (argmax) reporting instead of first-crossing.

H-B3-1b's own Relaxation Map Row 3, the one item left untested. Confirms (a) peak_index behaves
correctly on hand-checkable arrays, (b) the real run executes end-to-end and produces a coherent
result shape, reusing H-B3-1/H-B3-1b's own pipeline UNCHANGED.
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np

_B_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260906-may1972-tda-ews-obrienlakes"
)
_SPEC_B = importlib.util.spec_from_file_location("lakes_tda_ews_obrienlakes_run", _B_DIR / "run.py")
obrien = importlib.util.module_from_spec(_SPEC_B)
_SPEC_B.loader.exec_module(obrien)

_L_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "20260907-lakes-tda-ews-peaktau-v3"
)
_SPEC_L = importlib.util.spec_from_file_location("lakes_tda_ews_peaktau_v3_run", _L_DIR / "run.py")
peaktau = importlib.util.module_from_spec(_SPEC_L)
_SPEC_L.loader.exec_module(peaktau)


def test_peak_index_on_hand_checkable_array():
    tau = np.array([0.1, 0.4, np.nan, 0.9, 0.3, np.nan])
    assert peaktau.peak_index(tau) == 3


def test_peak_index_returns_none_for_all_nan():
    tau = np.array([np.nan, np.nan, np.nan])
    assert peaktau.peak_index(tau) is None


def test_peak_index_matches_argmax_on_series_without_nan():
    rng = np.random.default_rng(0)
    tau = rng.uniform(-1, 1, size=50)
    assert peaktau.peak_index(tau) == int(np.argmax(tau))


def test_reuses_obrienlakes_pipeline_functions_unchanged():
    """Minimal Relaxation Rule check: only the reporting step (peak vs first-crossing) and
    verdict logic are new -- the data/statistic pipeline itself must be byte-identical source,
    not a diverged copy. `peaktau.py` and this test file each do their OWN dynamic import of
    the same run.py (importlib.util.spec_from_file_location + exec_module), so the two module
    objects are DISTINCT instances -- an `is` check between them would fail even for correct,
    byte-identical, unchanged code, which is not the drift this test is meant to catch.
    Comparing source text instead is the check that actually matters."""
    assert inspect.getsource(peaktau.obrien.load_series) == inspect.getsource(obrien.load_series)
    assert inspect.getsource(peaktau.obrien.rolling_stat) == inspect.getsource(obrien.rolling_stat)
    assert inspect.getsource(peaktau.obrien.betti1_entropy_series) == inspect.getsource(
        obrien.betti1_entropy_series
    )
    assert inspect.getsource(peaktau.obrien.expanding_kendall_tau) == inspect.getsource(
        obrien.expanding_kendall_tau
    )
    assert peaktau.obrien.LAKES == obrien.LAKES


def test_real_run_executes_and_reports_coherent_shape():
    """Smoke test against the real 3-lake data: verdict is one of the three pre-registered
    categories, and Lower Zurich (the only lake with a documented transition) carries distance
    fields that the negative controls do not."""
    result = peaktau.cmd_run()
    assert result["verdict"] in {"CONFIRMED", "REJECTED", "AMBIGUOUS"}
    lz = result["results"]["lower_zurich"]
    assert "tda_distance_to_transition_years" in lz
    assert "classical_distance_to_transition_years" in lz
    for lake in ("windermere", "loch_leven"):
        assert "tda_distance_to_transition_years" not in result["results"][lake]
    assert set(result["negative_control_leads_months"].keys()) == {"windermere", "loch_leven"}
