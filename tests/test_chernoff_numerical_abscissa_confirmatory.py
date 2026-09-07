"""Tests for H-B2-1o: pre-registered confirmatory test of H-B2-1n's exploratory Fisher signal,
on fresh non-overlapping seeds 40-99.
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-numerical-abscissa-confirmatory"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1o_run", _HERE / "run.py")
confirmatory = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(confirmatory)

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
    """Minimal Relaxation Rule check: confirmatory.numerical_abscissa is a thin wrapper that
    delegates to H-B2-1n's implementation, byte-identical -- verify both the delegation (same
    numeric output) and that the delegate itself was imported unchanged (source-compared)."""
    assert inspect.getsource(abscissa_1n.numerical_abscissa) == inspect.getsource(
        confirmatory.abscissa_1n.numerical_abscissa
    )
    rng = np.random.default_rng(0)
    a = rng.normal(size=(4, 4))
    assert confirmatory.numerical_abscissa(a) == abscissa_1n.numerical_abscissa(a)
    assert inspect.getsource(confirmatory.multin.build_matrix_with_seed_and_n) == inspect.getsource(
        multin.build_matrix_with_seed_and_n
    )


def test_seed_range_has_zero_overlap_with_h_b2_1n_exploratory_seeds():
    """The whole point of a confirmatory experiment: independent data. H-B2-1n used seeds
    range(0, 40) -- this MUST start no earlier than 40."""
    h_b2_1n_seeds = set(range(0, 40))
    confirmatory_seeds = set(range(confirmatory.SEED_START, confirmatory.SEED_END))
    assert h_b2_1n_seeds.isdisjoint(confirmatory_seeds)
    assert confirmatory.SEED_START == 40


def test_n_dim_set_held_fixed_matching_h_b2_1n():
    """Minimal Relaxation Rule: only the seed range changes, not the N_DIM population."""
    assert confirmatory.LARGE_N_DIM_VALUES == abscissa_1n.LARGE_N_DIM_VALUES


def test_verdict_is_binary_confirmed_or_rejected_no_weakened_tier():
    """This experiment pre-registered a single binary primary criterion -- unlike H-B2-1n's
    three-tier verdict, there must be no WEAKENED here by design."""
    result = confirmatory.cmd_run()
    assert result["verdict"] in {"CONFIRMED", "REJECTED"}


def test_verdict_matches_primary_fisher_threshold_exactly():
    """The verdict must be a direct, mechanical function of the pre-registered primary
    criterion -- not influenced by the secondary descriptive stats."""
    result = confirmatory.cmd_run()
    fisher_p = result["primary_criterion"]["fisher_combined_p"]
    if fisher_p < confirmatory.PRIMARY_ALPHA:
        assert result["verdict"] == "CONFIRMED"
    else:
        assert result["verdict"] == "REJECTED"


def test_real_run_produces_5_slices_with_300_total_pairs():
    result = confirmatory.cmd_run()
    assert len(result["per_n_slice"]) == 5
    for slice_data in result["per_n_slice"].values():
        assert slice_data["n_seeds"] == 60
        assert slice_data["seed_range"] == [40, 100]
