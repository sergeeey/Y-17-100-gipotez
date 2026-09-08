"""Tests for H-B2-1t: fresh-seed confirmatory replication (user's Priority 2), kappa(V)/omega(A)
as pre-registered comparators.
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260908-chernoff-neuralode-nd-pseudospectral-fresh-confirmatory"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1t_run", _HERE / "run.py")
fresh = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(fresh)

_L_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-eigenvector-conditioning"
)
_SPEC_L = importlib.util.spec_from_file_location("chernoff_1l_run", _L_DIR / "run.py")
eig_cond = importlib.util.module_from_spec(_SPEC_L)
_SPEC_L.loader.exec_module(eig_cond)

_N_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-numerical-abscissa"
)
_SPEC_N = importlib.util.spec_from_file_location("chernoff_1n_run", _N_DIR / "run.py")
omega_mod = importlib.util.module_from_spec(_SPEC_N)
_SPEC_N.loader.exec_module(omega_mod)

_R_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
)
_SPEC_R = importlib.util.spec_from_file_location("chernoff_1r_run", _R_DIR / "run.py")
alpha_mod = importlib.util.module_from_spec(_SPEC_R)
_SPEC_R.loader.exec_module(alpha_mod)


def test_reuses_all_three_descriptor_implementations_unchanged():
    assert inspect.getsource(fresh.eig_cond.eigenvector_condition_number) == inspect.getsource(
        eig_cond.eigenvector_condition_number
    )
    assert inspect.getsource(fresh.omega_mod.numerical_abscissa) == inspect.getsource(
        omega_mod.numerical_abscissa
    )
    assert inspect.getsource(fresh.alpha_mod.pseudospectral_abscissa) == inspect.getsource(
        alpha_mod.pseudospectral_abscissa
    )


def test_seed_range_has_zero_overlap_with_every_prior_range_in_the_arc():
    """0-39 (H-B2-1m/1n original), 40-99 (H-B2-1o large-N), 0-59 (H-B2-1p at N=64,80),
    100-159 (H-B2-1q fixed-grid) -- this experiment's seeds must be disjoint from ALL of them."""
    prior_ranges = [set(range(0, 40)), set(range(40, 100)), set(range(0, 60)), set(range(100, 160))]
    this_range = set(range(fresh.SEED_START, fresh.SEED_END))
    for prior in prior_ranges:
        assert this_range.isdisjoint(prior)
    assert fresh.SEED_START == 300


def test_n_dim_matches_users_primary_large_n_regime():
    assert fresh.N_DIM_VALUES == (40, 50)


def test_verdict_determined_solely_by_pseudospectral_abscissa_not_comparators():
    """kappa(V)/omega(A) are comparators, not part of the kill criterion -- the verdict must
    depend only on alpha_eps_vs_m1 significance, never on the comparators' results."""
    result = fresh.cmd_run()
    primary_met = all(
        v["alpha_eps_vs_m1"]["significant_positive"] for v in result["per_n_slice"].values()
    )
    if primary_met:
        assert result["verdict"] == "CONFIRMED"
    else:
        assert result["verdict"] == "REJECTED"


def test_real_run_produces_2_slices_of_40_fresh_seeds_with_all_three_descriptors():
    result = fresh.cmd_run()
    assert len(result["per_n_slice"]) == 2
    for slice_data in result["per_n_slice"].values():
        assert slice_data["n_seeds"] == 40
        assert slice_data["seed_range"] == [300, 340]
        for key in ("kappa_v_vs_m1", "omega_a_vs_m1", "alpha_eps_vs_m1"):
            assert key in slice_data
            assert "rho" in slice_data[key] and "p" in slice_data[key]
