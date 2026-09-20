# ruff: noqa: E501
"""Regression tests for the H-CAT56-2 verification gates (experiments/20260920-h-cat56-2-verification-gates).

Fast (seconds). They pin: the published-example positive control, the threshold arithmetic
d*(r) = 22, 23, 31, 41 for r = 2..5, the d=21 non-firing control, and the d=22 float count
dim V = 463 (dim V-perp = 21 < 22). Not a proof of anything: numerical regression only.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1] / "experiments"
GATES = ROOT / "20260920-h-cat56-2-verification-gates"
CORE = ROOT / "20260919-pcc-generic-quasipure-cat56-2"


def _load(path: Path, name: str):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def g4():
    return _load(GATES / "gate4_source_example.py", "gate4_source_example")


@pytest.fixture(scope="module")
def g13():
    return _load(GATES / "gate13_threshold_formula.py", "gate13_threshold_formula")


@pytest.fixture(scope="module")
def oc():
    return _load(CORE / "orchestrator_independent_check.py", "orchestrator_independent_check")


def test_source_example_qfim_matches_published_formula(g4):
    for q, th in [(0.3, 0.7), (0.5, 1.1), (0.8, 0.4)]:
        res = g4.example(q, th, 0.4, 0.9)
        assert res["qfim_matches_paper_formula"]
        assert res["pcc_residual"] < 1e-10
        assert res["quasi_pure_residual"] < 1e-10
        # derived, not published: dim V = 12 of 64, so dim V-perp = 52 >= d = 8 (saturation not excluded)
        assert res["dimV_tol1e-08"] == 12
        assert res["dimVperp"] == 52


def test_first_firing_sizes(g13):
    assert [g13.first_d(r)[0] for r in (2, 3, 4, 5)] == [22, 23, 31, 41]


def test_bound_never_fires_below_22_for_r2(g13):
    for k in range(2, 20):  # d = k + 2 <= 21
        d = k + 2
        assert min(g13.lb(k, 2, s) for s in range(1, 2 * k * 2 + 1)) >= d


@pytest.mark.parametrize(
    ("k", "s", "expected_vperp", "fires"),
    [(20, 16, 21, True), (19, 16, 21, False)],
)
def test_float_counterexample_and_control(oc, k, s, expected_vperp, fires):
    res = oc.analyse(k, 2, s, 4242, False)
    assert res["qfim_full_rank"]
    assert res["pcc_residual_full_commutator"] < 1e-9
    assert res["dimVperp"] == expected_vperp
    assert res["fires_dimVperp_lt_d"] is fires
    assert np.isfinite(res["gap_ratio"]) or res["gap_ratio"] == float("inf")
