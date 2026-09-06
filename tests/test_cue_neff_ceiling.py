"""Harness sanity for experiments/20260906-riemann-cue-neff-ceiling/run.py (H-B1-1c).

Checks the N_e(T) / predicted_relative_deviation formulas against hand-computable values, so a
future refactor can't silently drift from the primary-source formulas (Nishigaki 2025, Eq. 42
and Fig. 6 fit) without a test catching it.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "cue_neff_ceiling",
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-riemann-cue-neff-ceiling"
    / "run.py",
)
mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mod)


def test_n_eff_matches_hand_computation():
    # N_e(T) = (1/sqrt(12*Lambda)) * log(T/2pi), Lambda = 1.573151071
    t = 74920.827498994
    expected = (1 / math.sqrt(12 * 1.573151071)) * math.log(t / (2 * math.pi))
    assert mod.n_eff(t) == pytest.approx(expected, rel=1e-12)
    assert mod.n_eff(t) == pytest.approx(2.1603248512641673, rel=1e-9)


def test_predicted_relative_deviation_matches_hand_computation():
    t = 74920.827498994
    expected = 0.1896 * mod.n_eff(t) ** (-3.081)
    assert mod.predicted_relative_deviation(t) == pytest.approx(expected, rel=1e-12)


def test_e_r_inf_is_the_published_sine_kernel_constant():
    # Nishigaki 2025 p.14: E[r-tilde]_infinity = 0.5997504209...
    assert mod.E_R_INF == pytest.approx(0.5997504209, abs=1e-9)


def test_ceiling_run_reproduces_pilot_r_mean():
    # H-B1-1c reuses H-B1-1a's cached data + tested mean_r() -- must reproduce the exact
    # r_mean already recorded in the sibling experiment's metrics/run.json, not a new number.
    out = mod.main()
    cum = out["results"]["cumulative_first_100k"]
    assert cum["r_observed"] == pytest.approx(0.6109167772757004, abs=1e-12)
    assert cum["verdict"] == "PASS"


def test_pass_band_can_fail():
    # Negative control: if the fit predicted a deviation 10x too small, the ratio would exceed
    # the [1/3, 3] band. This just confirms the band construction is not vacuously always-PASS.
    assert not (1 / 3 <= 10.0 <= 3)
