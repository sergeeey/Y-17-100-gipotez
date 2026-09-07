"""Tests for H-B2-1q: pre-registered FIXED-grid replication of H-B2-1p's disputed N=64 finding."""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-numerical-abscissa-fixedgrid"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1q_run", _HERE / "run.py")
fixedgrid = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(fixedgrid)

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
    assert fixedgrid.numerical_abscissa(a) == abscissa_1n.numerical_abscissa(a)
    assert inspect.getsource(fixedgrid.multin.build_matrix_with_seed_and_n) == inspect.getsource(
        multin.build_matrix_with_seed_and_n
    )


def test_grid_matches_exactly_what_h_b2_1p_pre_registered():
    """The grid must be {56,64,72} -- not adjusted after the fact to whatever looked promising."""
    assert fixedgrid.FIXED_GRID_N_DIM_VALUES == (56, 64, 72)
    assert fixedgrid.PRIMARY_N_DIM == 64


def test_seed_range_has_zero_overlap_with_every_prior_range_in_the_arc():
    """H-B2-1m/1n/1o used 0-39 or 40-99; H-B2-1p used 0-59 at N=64,80. This experiment's seeds
    must be disjoint from ALL of them, not just the most recent one."""
    prior_ranges = [set(range(0, 40)), set(range(40, 100)), set(range(0, 60))]
    this_range = set(range(fixedgrid.SEED_START, fixedgrid.SEED_END))
    for prior in prior_ranges:
        assert this_range.isdisjoint(prior)
    assert fixedgrid.SEED_START == 100


def test_verdict_is_binary_and_determined_solely_by_n64():
    result = fixedgrid.cmd_run()
    assert result["verdict"] in {"REPLICATED", "NOT_REPLICATED"}
    n64 = result["per_n_slice"]["64"]
    is_sig_positive = n64["spearman_p"] < fixedgrid.ALPHA and n64["spearman_rho"] > 0
    if is_sig_positive:
        assert result["verdict"] == "REPLICATED"
    else:
        assert result["verdict"] == "NOT_REPLICATED"


def test_real_run_produces_3_slices_with_60_fresh_seeds_each():
    result = fixedgrid.cmd_run()
    assert len(result["per_n_slice"]) == 3
    for slice_data in result["per_n_slice"].values():
        assert slice_data["n_seeds"] == 60
        assert slice_data["seed_range"] == [100, 160]
