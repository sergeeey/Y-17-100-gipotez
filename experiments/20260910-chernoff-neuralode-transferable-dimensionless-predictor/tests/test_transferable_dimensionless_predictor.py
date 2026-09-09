import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    build_matrix_with_seed_and_n,
    build_rotation_block_matrix,
    dimensionless_matrix,
    fit_power_law,
    measure_m_t_w,
    predict,
)


def test_dimensionless_reduction_identity_holds_numerically():
    """Mechanism Claim Gate (Step 0a) check: M_T,W(B) must equal M_1,0(C) where
    C = T*(B - W*I), for several (T, W, B) combinations -- not just asserted
    algebraically in claim.md, verified against the actual implementation."""
    a = build_matrix_with_seed_and_n(10, seed=1)
    for T in (0.3, 1.0, 2.5):
        for w in (0.0, 0.5, 1.2):
            lhs = measure_m_t_w(a, T, w)
            c = dimensionless_matrix(a, w, T)
            rhs = measure_m_t_w(c, 1.0, 0.0)
            assert abs(lhs - rhs) / max(lhs, 1e-12) < 1e-6, f"T={T} w={w}: {lhs} vs {rhs}"


def test_measure_m_t_w_on_pure_decay_matrix_equals_one():
    """Positive control: for A = -I (pure decay, no non-normality), the transient
    growth factor relative to its own decay rate must be exactly 1 -- ||exp(-tI)||
    = exp(-t), so the ratio to exp(w*t) with w=-1 is exactly 1 for all t."""
    a = -np.eye(5)
    m = measure_m_t_w(a, t_max=2.0, w=-1.0, n_grid=200)
    assert abs(m - 1.0) < 1e-6


def test_build_rotation_block_matrix_has_complex_eigenvalues():
    """The new transfer-test family must genuinely differ in structure from the
    original (always-real-eigenvalue, strictly-upper-triangular) family --
    otherwise Transfer B/C would not be testing anything new."""
    a = build_rotation_block_matrix(10, seed=42)
    eigvals = np.linalg.eigvals(a)
    assert np.any(np.abs(eigvals.imag) > 1e-6), "expected genuinely complex eigenvalues"


def test_build_rotation_block_matrix_preserves_the_growth_rate_w():
    """The one designated growing mode must have real part matching W=0.5,
    otherwise the shared normalization used in both families would not be
    comparable."""
    a = build_rotation_block_matrix(10, seed=7)
    eigvals = np.linalg.eigvals(a)
    assert np.any(np.abs(eigvals.real - 0.5) < 1e-6)


def test_fit_power_law_and_predict_round_trip_on_synthetic_exact_data():
    """Sanity/positive control: if M = 3*K^1.5 exactly (no noise), the OLS fit
    must recover intercept=log(3), exponent=1.5, and `predict` must reproduce M
    exactly for the same K."""
    k = np.array([1.0, 2.0, 5.0, 10.0, 20.0])
    m = 3.0 * k**1.5
    fit = fit_power_law(k, m)
    assert abs(fit["exponent"] - 1.5) < 1e-8
    assert abs(np.exp(fit["intercept"]) - 3.0) < 1e-6
    pred = predict(k, fit)
    assert np.allclose(pred, m, rtol=1e-6)
