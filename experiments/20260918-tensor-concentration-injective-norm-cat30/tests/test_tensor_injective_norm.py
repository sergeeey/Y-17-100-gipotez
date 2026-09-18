import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tensor_injective_norm import estimate_injective_norm, f_and_grad, scipy_cross_check


def test_single_rank1_tensor_injective_norm_is_exactly_one():
    """T = a^{otimes 3} with ||a||_2=1 must have ||T||_{I_2} = ||a||_2^3 = 1
    exactly (Hoelder duality, p=2 self-dual) -- the exact normalization the
    whole experiment's RHS relies on."""
    rng = np.random.default_rng(7)
    for d in (5, 40, 160):
        a = rng.standard_normal(d)
        a = a / np.linalg.norm(a)
        A = a.reshape(1, d)
        g = np.array([1.0])
        val, _ = estimate_injective_norm(A, g, n_restarts=80, n_iter=80, rng=rng)
        assert abs(val - 1.0) < 1e-8


def test_power_iteration_agrees_with_independent_scipy_search():
    """Regression lock: power-iteration estimate must match an independently
    implemented scipy.optimize search to within a small numerical tolerance."""
    rng = np.random.default_rng(42)
    d, n = 10, 15
    A = rng.standard_normal((n, d))
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    g = rng.standard_normal(n)
    val_pi, x_best = estimate_injective_norm(A, g, n_restarts=80, n_iter=80, rng=rng)
    val_sp = scipy_cross_check(A, g, x_best, seed=1)
    assert abs(val_pi - val_sp) / max(val_pi, val_sp, 1e-12) < 1e-4


def test_gradient_matches_finite_difference():
    """f_and_grad's analytic gradient must match a numerical finite-difference
    gradient -- catches a sign/factor error in the cubic-form derivative."""
    rng = np.random.default_rng(1)
    d, n = 6, 5
    A = rng.standard_normal((n, d))
    g = rng.standard_normal(n)
    x = rng.standard_normal(d)
    x = x / np.linalg.norm(x)
    _, grad_analytic = f_and_grad(x, A, g)
    eps = 1e-6
    grad_fd = np.zeros(d)
    for k in range(d):
        xp = x.copy()
        xp[k] += eps
        xm = x.copy()
        xm[k] -= eps
        fp, _ = f_and_grad(xp, A, g)
        fm, _ = f_and_grad(xm, A, g)
        grad_fd[k] = (fp - fm) / (2 * eps)
    assert np.allclose(grad_analytic, grad_fd, atol=1e-4)


def test_optimizer_is_confined_to_span_of_fixed_tensor_family():
    """Regression lock for the H-CAT30-1 REJECT finding (decision.md): the
    found x* must lie EXACTLY in span{a_i} regardless of d, since f(x)
    depends on x only through u=Ax -- this is the structural degeneracy
    that made the original pilot's d-scan uninformative. Confirms the
    optimizer cannot search outside this subspace even when d>>n."""
    rng = np.random.default_rng(2026)
    n, d = 20, 200
    A = rng.standard_normal((n, d))
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    g = rng.standard_normal(n)
    _, x_star = estimate_injective_norm(A, g, n_restarts=40, n_iter=60, rng=rng)
    Q, _ = np.linalg.qr(A.T)
    proj = Q @ (Q.T @ x_star)
    resid_norm = np.linalg.norm(x_star - proj)
    assert resid_norm < 1e-10


def test_more_restarts_does_not_change_estimate_on_a_fixed_instance():
    """Regression lock for the restart-count robustness check that ruled out
    a curse-of-dimensionality search bias: 50 restarts must already find the
    same optimum as 400 restarts on a representative d=80 instance."""
    rng = np.random.default_rng(99)
    d, n = 80, 20
    A = rng.standard_normal((n, d))
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    g = rng.standard_normal(n)
    val_small, _ = estimate_injective_norm(
        A, g, n_restarts=50, n_iter=70, rng=np.random.default_rng(1)
    )
    val_large, _ = estimate_injective_norm(
        A, g, n_restarts=400, n_iter=150, rng=np.random.default_rng(1)
    )
    assert abs(val_large - val_small) / max(val_small, 1e-12) < 1e-6
