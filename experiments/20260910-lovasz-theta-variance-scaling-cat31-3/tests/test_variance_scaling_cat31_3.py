"""Tests for H-CAT31-3 -- variance scaling of log(theta(G)/sqrt(n))."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def run_module():
    return _load_module("h_cat31_3_run_under_test", EXPERIMENT_DIR / "run.py")


def test_substrate_gate_passes(run_module):
    """Positive control: theta_via_lp must still match the two closed-form checks
    H-CAT31-1 already established -- catches environment/dependency drift."""
    sub = run_module.substrate_gate_checks()
    assert sub["c5_check_passed"] is True
    assert sub["identity_check_passed"] is True
    assert sub["substrate_ready"] is True
    assert sub["theta_c5"] == pytest.approx(np.sqrt(5), abs=1e-6)
    assert sub["theta_g_times_gbar"] == pytest.approx(sub["n_check"], abs=1e-4)


def test_negative_control_zero_variance(run_module):
    """At p=0 every seed gives an identical degenerate graph -- Var(log(...)) must
    be exactly 0, confirming the estimator can register zero, not just report noise."""
    neg = run_module.negative_control_zero_variance()
    assert neg["all_identical"] is True
    assert neg["var_log_ratio"] == 0.0
    assert neg["control_passed"] is True


def test_bootstrap_var_ci_contains_point_estimate(run_module):
    rng = np.random.default_rng(42)
    x = rng.normal(0, 1, size=200)
    point_var = float(np.var(x, ddof=1))
    lo, hi = run_module.bootstrap_var_ci(x, n_boot=500, seed=1)
    assert lo < point_var < hi
    assert lo > 0  # variance is non-negative, CI should not cross zero for n=200 normal data


def test_bootstrap_var_ci_deterministic_given_seed(run_module):
    rng = np.random.default_rng(7)
    x = rng.normal(0, 1, size=50)
    ci_a = run_module.bootstrap_var_ci(x, n_boot=300, seed=5)
    ci_b = run_module.bootstrap_var_ci(x, n_boot=300, seed=5)
    assert ci_a == ci_b


def test_fit_exponent_recovers_known_exponent_on_synthetic_data(run_module):
    """Sanity check: if Var(n) is constructed EXACTLY as C*n^-1 (no noise), the fit
    must recover slope=-1 to high precision, and the CI-based checks must fire correctly."""
    ns = [32, 64, 128, 256, 512, 1024, 1536, 2048, 3000]
    rows = []
    for n in ns:
        var_exact = 5.0 / n  # exact -1 exponent by construction
        # Fake tiny bootstrap CI (near-zero width) so weights are huge and well-defined,
        # simulating the "very precise" regime -- tests the fit math, not real noise.
        rows.append(
            {
                "n": n,
                "n_reps": 1000,
                "var_log_ratio": var_exact,
                "var_log_ratio_bootstrap_ci95": [var_exact * 0.99, var_exact * 1.01],
            }
        )
    fit = run_module.fit_exponent(rows)
    assert fit["unweighted_ols"]["slope"] == pytest.approx(-1.0, abs=1e-6)
    assert fit["weighted_ols"]["slope"] == pytest.approx(-1.0, abs=1e-6)


def test_fit_exponent_rejects_wrong_exponent_on_synthetic_data(run_module):
    """Sanity check: if Var(n) is constructed as C*n^-2 (not -1), the fit's own CI must
    NOT contain -1 -- confirms the discrimination logic can actually say REJECTED,
    not just always default to CONFIRMED regardless of the underlying data."""
    ns = [32, 64, 128, 256, 512, 1024, 1536, 2048, 3000]
    rows = []
    for n in ns:
        var_exact = 5.0 / (n**2)
        rows.append(
            {
                "n": n,
                "n_reps": 1000,
                "var_log_ratio": var_exact,
                "var_log_ratio_bootstrap_ci95": [var_exact * 0.99, var_exact * 1.01],
            }
        )
    fit = run_module.fit_exponent(rows)
    assert fit["weighted_ols"]["slope"] == pytest.approx(-2.0, abs=1e-6)
    assert fit["ci_contains_minus_1"] is False


def test_fit_exponent_handles_noisy_realistic_case():
    """Uses the ACTUAL smoke-test-scale sweep (small reps) to confirm the fit pipeline
    runs end-to-end without crashing on genuinely noisy (not synthetic-exact) data."""
    module = _load_module("h_cat31_3_noisy_check", EXPERIMENT_DIR / "run.py")
    module.SWEEP_N_REPS = [(32, 15), (64, 15), (128, 15), (256, 15)]
    rows = module.run_sweep()
    fit = module.fit_exponent(rows)
    assert "weighted_ols" in fit
    assert np.isfinite(fit["weighted_ols"]["slope"])


def test_seed_base_does_not_collide_with_h_cat31_1_or_2(run_module):
    """H-CAT31-1 uses RNG_SEED_BASE=31000 with seeds up to ~31000+100000+2560*100+24
    (~356960 max). This experiment's own RNG_SEED_BASE=331000 with n*1000+i (n up to
    3000, i up to 300) reaches up to ~3331300 -- confirm no accidental overlap in the
    actual seed VALUES used, not just the base constants (a real, if unlikely, way two
    experiments could silently share randomness)."""
    import importlib.util as ilu

    h1_spec = ilu.spec_from_file_location(
        "h_cat31_1_seedcheck",
        EXPERIMENT_DIR.parent / "20260909-lovasz-theta-random-circulant-graphs" / "run.py",
    )
    h1 = ilu.module_from_spec(h1_spec)
    h1_spec.loader.exec_module(h1)

    h1_seeds = {
        h1.RNG_SEED_BASE + 100000 + n * 100 + i
        for n, reps in [
            (10, 25),
            (20, 25),
            (40, 25),
            (80, 25),
            (160, 25),
            (320, 25),
            (640, 15),
            (1280, 10),
            (2560, 6),
        ]
        for i in range(reps)
    }
    h3_seeds = {
        run_module.RNG_SEED_BASE + n * 1000 + i
        for n, reps in run_module.SWEEP_N_REPS
        for i in range(reps)
    }
    assert h1_seeds.isdisjoint(h3_seeds)
