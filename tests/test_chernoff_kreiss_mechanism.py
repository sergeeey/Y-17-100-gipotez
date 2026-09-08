"""Tests for H-B2-1u: direct verification of the Kreiss Matrix Theorem inequality
K(A) <= sup_t||exp(tA)|| <= e*n*K(A) on this arc's own matrices (user's Priority 3,
mechanistic analysis)."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260908-chernoff-neuralode-nd-kreiss-mechanism"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1u_run", _HERE / "run.py")
kreiss = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(kreiss)

_R_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
)
_SPEC_R = importlib.util.spec_from_file_location("chernoff_1r_run_direct", _R_DIR / "run.py")
alpha_mod = importlib.util.module_from_spec(_SPEC_R)
_SPEC_R.loader.exec_module(alpha_mod)

_CACHED_RESULT = None


def _cached_run():
    """cmd_run() is expensive (20 matrices x 5-eps Kreiss estimate + 1000-point expm sweep
    each) -- cache across tests in this module instead of tripling the cost (same fix as
    H-B2-1s's _cached_run helper)."""
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = kreiss.cmd_run()
    return _CACHED_RESULT


def test_reuses_pseudospectral_abscissa_unchanged():
    import inspect

    assert inspect.getsource(kreiss.alpha_mod.pseudospectral_abscissa) == inspect.getsource(
        alpha_mod.pseudospectral_abscissa
    )


def test_kreiss_constant_is_zero_for_symmetric_normal_matrix():
    """A symmetric matrix is normal -- pseudospectra are disks of radius eps around each
    eigenvalue, so alpha_eps(A) = alpha(A) + eps exactly for every eps, giving K(A) = 1
    (the minimum possible value: K(A) >= 1 always, per Trefethen-Embree).

    pseudospectral_abscissa is a FINITE GRID SEARCH -- kreiss_constant_estimate uses the
    LOCAL, alpha(A)-centered KREISS_GRID_KWARGS window (not the arc-wide default), so it can
    only ever UNDERSHOOT the true alpha_eps by up to that grid's own step -- same discipline
    as H-B2-1r's regression test. The tightest bound comes from whichever sampled eps
    minimizes grid_step/eps -- here the largest EPS_VALUES entry -- so that sets the
    tolerance, not an arbitrary constant."""
    rng = np.random.default_rng(0)
    m = rng.standard_normal((5, 5))
    a = (m + m.T) / 2 - 3 * np.eye(5)  # symmetric, shifted to stable (Re < 0)
    g = kreiss.KREISS_GRID_KWARGS
    grid_step = (g["re_max_offset"] - g["re_min_offset"]) / g["n_re"]
    max_eps = max(kreiss.EPS_VALUES)
    tolerance = grid_step / max_eps
    kr = kreiss.kreiss_constant_estimate(a)
    assert abs(kr["k_estimate"] - 1.0) < tolerance + 1e-9
    assert kr["k_estimate"] <= 1.0 + 1e-9  # must not OVERSHOOT the proven exact value


def test_raw_transient_growth_never_below_one_at_t_near_zero():
    """||exp(tA)|| -> ||I|| = 1 as t -> 0+, and growth (if any) only increases the sup;
    for any real matrix the raw transient growth measured over (0, t_max] must be >= a
    value close to 1 (exact equality only in the t->0 limit, which the grid doesn't hit)."""
    rng = np.random.default_rng(1)
    m = rng.standard_normal((6, 6)) * 2 - 2 * np.eye(6)
    growth, t_at_max = kreiss.raw_transient_growth(m, t_max=1.0)
    assert growth >= 0.9  # comfortably below the exact ||I||=1 floor, grid-spacing tolerant
    assert 0.0 < t_at_max <= 1.0


def test_upper_bound_holds_on_a_known_nonnormal_example():
    """Direct check of the proven inequality sup_t||exp(tA)|| <= e*n*K(A) on a hand-built
    non-normal Jordan-like matrix with real, stable eigenvalues -- this is the exact
    mathematical claim the experiment is built to verify at scale."""
    n = 8
    a = -1.0 * np.eye(n) + np.diag(np.ones(n - 1) * 5.0, k=1)  # strongly non-normal, stable
    kr = kreiss.kreiss_constant_estimate(a)
    growth, _ = kreiss.raw_transient_growth(a, t_max=1.0)
    ceiling = kreiss.EULER_E * n * kr["k_estimate"]
    assert growth <= ceiling + 1e-9


def test_regression_seed301_n50_that_previously_hit_the_eps_sampling_gap_bug():
    """seed=301, N_DIM=50 was the exact matrix where EPS_VALUES=(0.5..3.0) with the arc-wide
    grid produced an apparent (false) violation of the proven Kreiss upper bound: k_estimate
    was 22.84 (undersampled small-eps regime), giving ceiling=3104.06 < observed growth=
    11025.75. Locks in the fix: with the widened EPS_VALUES + local grid, the bound must hold
    for this specific matrix, with k_estimate meaningfully above the old undersampled value."""
    a = kreiss.multin.build_matrix_with_seed_and_n(50, 301)
    kr = kreiss.kreiss_constant_estimate(a)
    growth, _ = kreiss.raw_transient_growth(a, kreiss.dim_sweep.T_MAX)
    ceiling = kreiss.EULER_E * 50 * kr["k_estimate"]
    assert kr["k_estimate"] > 22.84 * 2  # must have found the small-eps regime, not just noise
    assert growth <= ceiling + 1e-9


def test_cmd_run_produces_two_slices_of_ten_seeds_matching_h_b2_1t_range():
    result = _cached_run()
    assert result["config"]["n_dim_values"] == [40, 50]
    assert result["config"]["seed_range"] == [300, 310]
    assert len(result["per_n_slice"]) == 2
    for slice_data in result["per_n_slice"].values():
        assert slice_data["n_seeds"] == 10
        assert slice_data["seed_range"] == [300, 310]


def test_upper_bound_verdict_is_the_only_valid_kill_signal_per_claim_md():
    """Per claim.md's Kill Criterion: a clean run reports MECHANISM_VERIFIED (all upper
    bounds hold); any violation must report CODE_BUG_SUSPECTED, never a normal REJECT."""
    result = _cached_run()
    if result["upper_bound_check"]["all_hold"]:
        assert result["verdict"] == "MECHANISM_VERIFIED"
    else:
        assert result["verdict"] == "CODE_BUG_SUSPECTED"


def test_efficiency_ratio_is_bounded_between_zero_and_one_when_bound_holds():
    result = _cached_run()
    for slice_data in result["per_n_slice"].values():
        for seed_data in slice_data["per_seed"].values():
            if seed_data["upper_bound_holds"]:
                assert 0.0 <= seed_data["efficiency"] <= 1.0 + 1e-9


def test_euler_e_constant_matches_math_e():
    assert kreiss.EULER_E == math.e
