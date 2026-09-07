"""Tests for H-B2-1p: discriminating test at N_DIM in {64,80} -- does omega(A)-M1 signal
reappear ("unlucky pair") or stay null ("genuine ceiling") beyond H-B2-1o's N=40,50 null?
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-numerical-abscissa-boundary"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1p_run", _HERE / "run.py")
boundary = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(boundary)

_N_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-numerical-abscissa"
)
_SPEC_N = importlib.util.spec_from_file_location("chernoff_1n_run", _N_DIR / "run.py")
abscissa_1n = importlib.util.module_from_spec(_SPEC_N)
_SPEC_N.loader.exec_module(abscissa_1n)

_M_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-multiseed-multin"
)
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1m_run", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)


def test_reuses_h_b2_1n_numerical_abscissa_and_h_b2_1m_build_matrix_unchanged():
    rng = np.random.default_rng(0)
    a = rng.normal(size=(4, 4))
    assert boundary.numerical_abscissa(a) == abscissa_1n.numerical_abscissa(a)
    assert inspect.getsource(boundary.multin.build_matrix_with_seed_and_n) == inspect.getsource(
        multin.build_matrix_with_seed_and_n
    )


def test_n_dim_values_are_genuinely_new_never_tested_before():
    """These specific N_DIM values must not overlap with H-B2-1m/1n/1o's tested range."""
    prior_n_dim_values = {3, 4, 8, 12, 16, 24, 32, 40, 50}
    assert set(boundary.BOUNDARY_N_DIM_VALUES).isdisjoint(prior_n_dim_values)
    assert boundary.BOUNDARY_N_DIM_VALUES == (64, 80)


def test_verdict_is_one_of_three_discriminating_outcomes():
    result = boundary.cmd_run()
    assert result["verdict"] in {"REAPPEARS", "CEILING_CONFIRMED", "MIXED"}


def test_verdict_matches_significant_positive_slice_count():
    result = boundary.cmd_run()
    n_pos_sig = sum(
        1
        for v in result["per_n_slice"].values()
        if v["spearman_rho"] > 0 and v["spearman_p"] < boundary.ALPHA
    )
    if n_pos_sig == 2:
        assert result["verdict"] == "REAPPEARS"
    elif n_pos_sig == 0:
        assert result["verdict"] == "CEILING_CONFIRMED"
    else:
        assert result["verdict"] == "MIXED"


def test_real_run_produces_2_slices_with_60_seeds_each():
    result = boundary.cmd_run()
    assert len(result["per_n_slice"]) == 2
    for slice_data in result["per_n_slice"].values():
        assert slice_data["n_seeds"] == 60
