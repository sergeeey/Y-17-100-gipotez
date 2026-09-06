"""Harness sanity for experiments/20260906-riemann-rstat-gue/run.py (Substrate Gate check).

NOT the scientific controls (those live in metrics/controls.json). These check assumption A5:
the r-statistic pairing has no off-by-one, on inputs with hand-computed answers.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import numpy as np
import pytest

_SPEC = importlib.util.spec_from_file_location(
    "riemann_run",
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-riemann-rstat-gue"
    / "run.py",
)
run = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(run)


def test_pairing_hand_computed() -> None:
    # levels 0,1,3,7 → spacings 1,2,4 → r = (1/2, 2/4) → mean 0.5
    assert run.mean_r(np.array([0.0, 1.0, 3.0, 7.0])) == pytest.approx(0.5)
    # levels 0,2,3,9 → spacings 2,1,6 → r = (1/2, 1/6) → mean 1/3
    assert run.mean_r(np.array([0.0, 2.0, 3.0, 9.0])) == pytest.approx(1 / 3)


def test_pure_python_matches_numpy() -> None:
    rng = np.random.default_rng(1)
    lv = np.cumsum(rng.exponential(1.0, 2000))
    assert run.mean_r_pure_python(lv) == pytest.approx(run.mean_r(lv), abs=1e-12)


def test_scale_invariance_exact() -> None:
    lv = np.array([0.0, 1.0, 3.0, 7.0, 8.0])
    assert run.mean_r(lv * 1e-3) == pytest.approx(run.mean_r(lv), abs=1e-15)
    assert run.mean_r(lv * 1e3) == pytest.approx(run.mean_r(lv), abs=1e-15)


def test_duplicate_level_aborts() -> None:
    with pytest.raises(ValueError, match="non-positive spacing"):
        run.mean_r(np.array([0.0, 1.0, 1.0, 3.0]))


def test_constants_match_surmise_formulas() -> None:
    # Literature quotes 5-6 sig. digits (Atas et al. 2013); exact 2*sqrt(3)/pi - 1/2 = 0.6026578.
    # WHY abs=5e-6: first run used 1e-6 and FAILED on 0.60266 vs 0.602658 — a rounding artefact
    # in the *documents*, not in the constant. Substrate Gate fix log, attempt 1.
    assert run.R_POISSON == pytest.approx(0.386294, abs=5e-6)
    assert run.R_GOE == pytest.approx(0.535898, abs=5e-6)
    assert run.R_GUE == pytest.approx(0.602658, abs=5e-6)
    assert run.R_GUE - run.R_POISSON > 20 * run.TOL  # headroom sanity
    assert math.isclose(run.R_GUE, 2 * math.sqrt(3) / math.pi - 0.5)
