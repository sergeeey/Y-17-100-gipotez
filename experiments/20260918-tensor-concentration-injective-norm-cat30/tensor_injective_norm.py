"""
Core routine: estimate the symmetric injective ell_2 norm of an order-3 tensor
S = sum_i g_i * a_i^{otimes 3}, i.e.
    ||S||_{I_2} = max_{||x||_2=1} | sum_i g_i * <a_i,x>^3 |
via multi-restart symmetric tensor power iteration, plus an independent
scipy.optimize cross-check for small d.

For T_i = a_i^{otimes 3} with ||a_i||_2=1, the exact injective l2 norm of T_i
alone is ||a_i||_2^3 = 1 (self-dual p=2 Holder argument), used as the RHS
normalization in Conjecture 16 (Bandeira et al., arXiv:2603.29571, Entry 8).
"""

import numpy as np


def f_and_grad(x, A, g):
    """f(x) = sum_i g_i <a_i,x>^3 ; grad f(x) = 3 * A^T (g * (A x)^2)."""
    Ax = A @ x
    f = np.sum(g * Ax**3)
    grad = 3.0 * (A.T @ (g * Ax**2))
    return f, grad


def power_iteration_restart(A, g, x0, n_iter=60):
    x = x0 / np.linalg.norm(x0)
    for _ in range(n_iter):
        Ax = A @ x
        grad = A.T @ (g * Ax**2)  # unnormalized power-method direction
        nrm = np.linalg.norm(grad)
        if nrm < 1e-14:
            break
        x = grad / nrm
    f, _ = f_and_grad(x, A, g)
    return x, f


def estimate_injective_norm(A, g, n_restarts=60, n_iter=60, rng=None):
    """Multi-restart symmetric-tensor power iteration; returns max |f(x)| found."""
    if rng is None:
        rng = np.random.default_rng()
    d = A.shape[1]
    best_abs = 0.0
    best_x = None
    for _ in range(n_restarts):
        x0 = rng.standard_normal(d)
        x, f = power_iteration_restart(A, g, x0, n_iter=n_iter)
        if abs(f) > best_abs:
            best_abs = abs(f)
            best_x = x.copy()
    return best_abs, best_x


def scipy_cross_check(A, g, x_init, seed=0):
    """Independent re-implementation via scipy.optimize, UNCONSTRAINED over a raw
    d-vector y with x=y/||y|| folded into the objective (scale-invariant, avoids
    equality-constraint line-search blowup) -- maximizes f(x)^2 (sign-agnostic)."""
    from scipy.optimize import minimize

    d = A.shape[1]

    def neg_f2(y):
        nrm = np.linalg.norm(y)
        if nrm < 1e-12:
            return 0.0
        x = y / nrm
        Ax = A @ x
        f = np.sum(g * Ax**3)
        return -(f**2)

    best = 0.0
    rng = np.random.default_rng(seed)
    starts = [x_init] + [rng.standard_normal(d) for _ in range(5)]
    for s in starts:
        s = s / np.linalg.norm(s)
        res = minimize(
            neg_f2,
            s,
            method="Nelder-Mead",
            options={"maxiter": 4000, "xatol": 1e-10, "fatol": 1e-14},
        )
        val = np.sqrt(max(0.0, -res.fun))
        if val > best:
            best = val
    return best


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    d, n = 10, 15
    A = rng.standard_normal((n, d))
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    g = rng.standard_normal(n)

    val_pi, x_best = estimate_injective_norm(A, g, n_restarts=80, n_iter=80, rng=rng)
    val_sp = scipy_cross_check(A, g, x_best, seed=1)
    print(f"power-iteration estimate: {val_pi:.6f}")
    print(f"scipy cross-check       : {val_sp:.6f}")
    print(f"relative gap            : {abs(val_pi - val_sp) / max(val_pi, val_sp, 1e-12):.4%}")
