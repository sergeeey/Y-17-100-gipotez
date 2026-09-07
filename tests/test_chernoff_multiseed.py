"""Tests for H-B2-1i: seed-ensemble test of M1 at fixed coupling_magnitude=15.

Confirms (a) build_matrix_with_seed(0) exactly reproduces H-B2-1g's own module-level A (same
provenance-check discipline as H-B2-1h), (b) the real ensemble run executes end-to-end and
produces a coherent distribution summary.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_G_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-chernoff-neuralode-nd-strong-coupling"
)
_SPEC_G = importlib.util.spec_from_file_location("chernoff_1g_run", _G_DIR / "run.py")
h2_1g = importlib.util.module_from_spec(_SPEC_G)
_SPEC_G.loader.exec_module(h2_1g)

_I_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-chernoff-neuralode-nd-multiseed"
)
_SPEC_I = importlib.util.spec_from_file_location("chernoff_1i_run", _I_DIR / "run.py")
multiseed = importlib.util.module_from_spec(_SPEC_I)
_SPEC_I.loader.exec_module(multiseed)


def test_build_matrix_with_seed_0_reproduces_h_b2_1g_module_level_matrix_exactly():
    """Regression guard: build_matrix_with_seed(0) at coupling=15 must reproduce H-B2-1g's own
    module-level A byte-for-byte -- same provenance discipline as H-B2-1h's own equivalent test."""
    a = multiseed.build_matrix_with_seed(0)
    assert np.allclose(a, h2_1g.A)


def test_reference_m1_matches_h_b2_1g_own_committed_value():
    """The reference seed's M1, measured via the ensemble's own machinery, must reproduce
    H-B2-1g's own committed M1=158.93 (regression guard against drift in reused formulas)."""
    a = multiseed.build_matrix_with_seed(multiseed.REFERENCE_SEED)
    m1 = multiseed.h2_1h.measure_m1(a, multiseed.T_MAX, multiseed.W)
    assert abs(m1 - multiseed.REFERENCE_M1) < 1.0


def test_quartiles_on_hand_checkable_array():
    """Sanity check on the quartile/Tukey-fence helper against a known array."""
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
    stats = multiseed._quartiles(values)
    assert abs(stats["median"] - 5.0) < 1e-9
    assert stats["q1"] < stats["median"] < stats["q3"]
    assert stats["tukey_lower_fence"] < stats["q1"]
    assert stats["tukey_upper_fence"] > stats["q3"]


def test_real_ensemble_runs_and_reports_coherent_distribution():
    """Smoke test against the real construction: 30 seeds run end-to-end, provenance check
    passes, and the reported verdict is one of the three pre-registered categories."""
    result = multiseed.cmd_run()
    assert result["provenance_check_ok"] is True
    assert result["verdict"] in {"TYPICAL", "MODERATE", "OUTLIER"}
    stats = result["distribution_stats"]
    assert stats["n_seeds"] == 30
    assert stats["min"] <= stats["median"] <= stats["max"]
    assert stats["q1"] <= stats["median"] <= stats["q3"]
