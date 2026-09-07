"""Tests for H-B2-1r: does pseudospectral abscissa alpha_eps(A) explain M1 at N_DIM in {40,50}
where kappa(V) and omega(A) are both confirmed null?

The two correctness tests (test_matches_exact_formula_for_symmetric_matrix and
test_shows_real_sensitivity_to_non_normality) are FL Step 0a positive controls -- they must pass
BEFORE the real (expensive) population run is trusted, since the grid-based pseudospectral
abscissa computation is a genuinely new, approximate numerical routine (unlike kappa(V)/omega(A),
which were simple closed-form quantities).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

_HERE = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
)
_SPEC = importlib.util.spec_from_file_location("chernoff_1r_run", _HERE / "run.py")
pseudo = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(pseudo)

_M_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260907-chernoff-neuralode-nd-multiseed-multin"
)
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1m_run", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)


def test_reuses_h_b2_1m_build_matrix_unchanged():
    import inspect

    assert inspect.getsource(pseudo.multin.build_matrix_with_seed_and_n) == inspect.getsource(
        multin.build_matrix_with_seed_and_n
    )


def test_matches_exact_formula_for_symmetric_matrix():
    """FL Step 0a positive control #1: for a normal (symmetric) matrix, alpha_eps(A) EXACTLY
    equals the spectral abscissa plus eps (pseudospectrum is a union of eps-disks around each
    eigenvalue). Uses a fine, tight grid specific to this test for a meaningful tolerance."""
    rng = np.random.default_rng(0)
    b = rng.normal(size=(5, 5))
    a_sym = (b + b.T) / 2.0
    spectral_abscissa = float(np.max(np.linalg.eigvalsh(a_sym)))
    eps = 1.0
    expected = spectral_abscissa + eps

    computed = pseudo.pseudospectral_abscissa(
        a_sym,
        eps=eps,
        re_min=spectral_abscissa - 2.0,
        re_max=spectral_abscissa + eps + 2.0,
        im_max=1.0,
        n_re=400,
        n_im=50,
    )
    assert abs(computed - expected) < 0.05  # a couple grid spacings at this resolution


def test_shows_real_sensitivity_to_non_normality():
    """FL Step 0a positive control #2: a strongly non-normal upper-triangular matrix (matching
    this project's own matrix family -- diagonal + large strictly-upper-triangular coupling)
    must show alpha_eps(A) SUBSTANTIALLY LARGER than spectral_abscissa + eps, demonstrating the
    implementation actually captures non-normality rather than silently returning the trivial
    normal-matrix answer."""
    eigenvalues = np.array([-5.0, -4.0, -3.0, -2.0, -1.0])
    rng = np.random.default_rng(1)
    a = np.diag(eigenvalues) + np.triu(rng.uniform(-15.0, 15.0, size=(5, 5)), k=1)
    spectral_abscissa = float(np.max(eigenvalues))  # triangular matrix -> eigenvalues = diagonal
    eps = 1.0
    trivial_normal_answer = spectral_abscissa + eps

    computed = pseudo.pseudospectral_abscissa(
        a, eps=eps, re_min=-10.0, re_max=30.0, im_max=20.0, n_re=80, n_im=80
    )
    assert computed > trivial_normal_answer + 1.0  # meaningfully above the trivial answer


def test_pseudospectral_abscissa_never_below_the_universal_lower_bound():
    """CORRECT universal bound (rank-1 perturbation argument, holds for ANY matrix, normal or
    not): alpha_eps(A) >= alpha(A) + eps, not just >= alpha(A). An earlier version of this test
    only checked the weaker >= alpha(A) bound -- that weaker check passed even with the real bug
    (see test_regression_seeds_that_previously_hit_the_grid_boundary_bug below) because most
    seeds happened not to trigger it. This is the test that should have caught it."""
    eigenvalues = np.array([-5.0, -4.0, -3.0, -2.0, -1.0])
    rng = np.random.default_rng(2)
    a = np.diag(eigenvalues) + np.triu(rng.uniform(-15.0, 15.0, size=(5, 5)), k=1)
    spectral_abscissa = float(np.max(eigenvalues))
    eps = 1.0
    computed = pseudo.pseudospectral_abscissa(
        a, eps=eps, re_min=-10.0, re_max=30.0, im_max=20.0, n_re=80, n_im=80
    )
    assert computed >= spectral_abscissa + eps - 1e-9


def test_regression_seeds_that_previously_hit_the_grid_boundary_bug():
    """Direct regression test on the exact real-population matrices (N_DIM=3, seeds 7/8/14)
    that returned the impossible value 0.0 before the fix (RE_MIN=-5.0 let the search land on
    the SECOND-largest eigenvalue's own eps-disk, at re=-1+eps=0.0, instead of the dominant
    eigenvalue's disk at re>=0.5+eps=1.5). Uses PRODUCTION default grid parameters, not a
    hand-tuned test-only grid, so this specifically guards the real run's own settings.

    Tolerance is ONE grid step below the true universal lower bound, not zero: this grid-search
    estimator is inherently a LOWER-BOUND approximation of the continuous alpha_eps(A) -- the
    true rightmost point of an eps-disk (re=alpha+eps exactly, at im=0) generally does not sit
    exactly on a grid point, so the search returns the highest re ON THE GRID with any hit,
    which can undershoot the true value by up to about one grid spacing. That is expected,
    bounded discretization error -- a fundamentally different (and far smaller) failure mode
    than the original bug, which returned a value from an entirely WRONG eigenvalue's region,
    unbounded in magnitude. This test distinguishes the two: it still fails hard if the result
    is drastically below the bound (the original bug's signature), but accepts one grid step of
    honest approximation slack."""
    for seed in (7, 8, 14):
        a = multin.build_matrix_with_seed_and_n(3, seed)
        spectral_abscissa = float(np.max(np.diag(a)))  # triangular -> eigenvalues = diagonal
        effective_re_min = max(pseudo.RE_MIN, spectral_abscissa)
        grid_spacing = (pseudo.RE_MAX - effective_re_min) / (pseudo.N_RE - 1)
        lower_bound = spectral_abscissa + pseudo.EPS
        computed = pseudo.pseudospectral_abscissa(a)  # production defaults
        assert computed >= lower_bound - grid_spacing - 1e-9, (
            f"seed={seed}: got {computed}, more than one grid step ({grid_spacing:.3f}) below "
            f"the universal lower bound {lower_bound} -- the grid-boundary bug has regressed"
        )


def test_real_run_produces_6_slices_with_verdict():
    result = pseudo.cmd_run()
    assert len(result["per_n_slice"]) == 6
    assert result["verdict"] in {"CONFIRMED", "REJECTED"}
    assert result["large_n_criterion"]["n_dim_tested"] == [40, 50]
    for n_dim_str, slice_data in result["per_n_slice"].items():
        assert slice_data["n_seeds"] == 15
        assert slice_data["alpha_eps_range"][1] >= slice_data["alpha_eps_range"][0]
