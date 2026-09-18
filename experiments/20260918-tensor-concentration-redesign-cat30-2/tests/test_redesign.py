import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from redesign_analysis import weighted_power_law_fit_on_R
from run import matricization_upper_bound, run_one_point, summarize_point
from tensor_injective_norm import estimate_injective_norm


def test_matricization_upper_bound_dominates_power_iteration_lower_bound():
    """Regression lock: sigma_max(M) >= ||S||_{I_2} must hold on every draw
    (verify_matricization_upper_bound.py's own claim) -- a violation here
    would mean the certified-upper-bound argument in claim.md is wrong."""
    rng = np.random.default_rng(11)
    for d, n in [(5, 8), (10, 15), (20, 25)]:
        A = rng.standard_normal((n, d))
        A = A / np.linalg.norm(A, axis=1, keepdims=True)
        g = rng.standard_normal(n)
        lower, _ = estimate_injective_norm(A, g, n_restarts=60, n_iter=70, rng=rng)
        upper = matricization_upper_bound(A, g, d)
        assert upper >= lower - 1e-9


def test_matricization_upper_bound_exact_on_rank1_tensor():
    """For a single rank-1 tensor T=a^{otimes3} with unit a, the sandwich
    should be nearly tight: sigma_max(M) should be close to the known exact
    injective norm (1.0), not wildly loose."""
    rng = np.random.default_rng(4)
    d = 20
    a = rng.standard_normal(d)
    a = a / np.linalg.norm(a)
    A = a.reshape(1, d)
    g = np.array([1.0])
    upper = matricization_upper_bound(A, g, d)
    assert abs(upper - 1.0) < 1e-6


def test_summarize_point_recovers_known_mean_and_scales_by_sqrt_n():
    """summarize_point's R = grand_mean/sqrt(n_d) must divide by sqrt(n_d)
    exactly, and between_family_se must be the standard error of the mean
    of family_means (not e.g. the raw std)."""
    family_means = [2.0, 2.0, 2.0, 2.0]  # zero variance -> se must be exactly 0
    summary = summarize_point(family_means, n_d=4)
    assert abs(summary["grand_mean"] - 2.0) < 1e-12
    assert summary["between_family_se"] == 0.0
    assert abs(summary["R"] - 1.0) < 1e-12  # 2.0 / sqrt(4) = 1.0

    varying = [1.0, 2.0, 3.0, 4.0]
    summary2 = summarize_point(varying, n_d=1)
    expected_se = np.std(varying, ddof=1) / np.sqrt(4)
    assert abs(summary2["between_family_se"] - expected_se) < 1e-12
    assert abs(summary2["R"] - np.mean(varying)) < 1e-12  # n_d=1, sqrt(1)=1


def test_span_full_rank_once_n_at_least_d():
    """Regression lock for the redesign's core structural claim: once n>=d,
    rank(A) should be d (full rank) with overwhelming probability for random
    Gaussian rows -- the specific mechanism that removes H-CAT30-1's
    span-confinement degeneracy."""
    rng = np.random.default_rng(2027)
    for d, n in [(10, 10), (20, 89), (30, 164)]:
        A = rng.standard_normal((n, d))
        A = A / np.linalg.norm(A, axis=1, keepdims=True)
        assert np.linalg.matrix_rank(A) == d


def test_weighted_power_law_fit_on_R_recovers_known_slope():
    """redesign_analysis.py's weighted_power_law_fit_on_R is the arithmetic
    claim.md's own LEAD/INFORMATIVE-NEGATIVE criterion is decided on (P1
    finding from code review) -- must recover a known synthetic slope
    (noiseless, so beta must match to high precision)."""
    true_alpha, true_beta = 0.9, -0.42
    d_values = [10, 20, 40, 80]
    points = [(d, float(np.exp(true_alpha + true_beta * np.log(d))), 1e-6) for d in d_values]
    fit = weighted_power_law_fit_on_R(points)
    assert abs(fit["beta"] - true_beta) < 1e-4
    assert abs(fit["alpha"] - true_alpha) < 1e-4

    # exact points -> near-zero residuals -> chi2 close to 0
    assert fit["chi2"] < 1e-4


def test_run_one_point_smoke_and_seed_independence_across_d():
    """Smoke test for run_one_point's orchestration (family/draw loop,
    accumulation) -- not exercised by any other test (P2 finding from code
    review). Also checks that two different seeds (as run_scale offsets per
    d-point) produce genuinely different family_means, ruling out an
    accidental shared-seed bug."""
    means_a, ratios_a = run_one_point(
        d=3, n=3, n_families=2, n_gaussian_draws=2, n_upper_check=1, seed=1
    )
    means_b, _ratios_b = run_one_point(
        d=3, n=3, n_families=2, n_gaussian_draws=2, n_upper_check=1, seed=2
    )
    assert len(means_a) == 2
    assert all(m > 0 for m in means_a)
    assert len(ratios_a) == 2  # n_upper_check=1 * n_families=2
    assert means_a != means_b  # different seeds -> different draws
