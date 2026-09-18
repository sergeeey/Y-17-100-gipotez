"""
Independently verify the skeptic's central claim: when a_i are orthonormal
(G=A A^T = I_n, achieved here with a_i = standard basis vectors e_i, d=n),
||S||_{I_2} = max_i|g_i| EXACTLY, and that the existing power-iteration
estimator recovers this to high precision (the "orthonormal canary" the
skeptic proposed as the decisive cheap test).

Also independently checks whether power iteration UNDER-estimates as n grows
at FIXED restart budget (n_restarts=40) -- the skeptic's concern #1/#3.
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tensor_injective_norm import estimate_injective_norm


def brute_force_max_abs_f(g, n_restarts=200):
    """Independent brute-force check via many random restarts + Nelder-Mead
    on the raw (unnormalized) vector, scale-invariant objective -- NOT using
    the power-iteration code at all, a genuinely separate implementation."""
    n = len(g)

    def neg_f2(y):
        nrm = np.linalg.norm(y)
        if nrm < 1e-12:
            return 0.0
        x = y / nrm
        f = np.sum(g * x**3)
        return -(f**2)

    best = 0.0
    rng = np.random.default_rng(0)
    for _ in range(n_restarts):
        y0 = rng.standard_normal(n)
        res = minimize(
            neg_f2,
            y0,
            method="Nelder-Mead",
            options={"maxiter": 3000, "xatol": 1e-10, "fatol": 1e-14},
        )
        val = np.sqrt(max(0.0, -res.fun))
        if val > best:
            best = val
    return best


print("=== Part 1: exact closed form check, small n (orthonormal a_i = e_i) ===")
rng = np.random.default_rng(42)
for n in [5, 10, 20]:
    g = rng.standard_normal(n)
    exact = np.max(np.abs(g))
    A = np.eye(n)  # a_i = e_i, orthonormal, G=I exactly
    power_iter_val, _ = estimate_injective_norm(A, g, n_restarts=80, n_iter=80, rng=rng)
    brute_val = brute_force_max_abs_f(g, n_restarts=100)
    print(
        f"n={n:3d}: exact max|g_i|={exact:.6f}  power_iter={power_iter_val:.6f}  "
        f"brute_force={brute_val:.6f}"
    )

print("\n=== Part 2: budget-sensitivity canary at LARGE n (skeptic's n=80,d=200 test) ===")
n, d = 80, 200
g = rng.standard_normal(n)
A = np.zeros((n, d))
A[:, :n] = np.eye(n)  # orthonormal a_i embedded in R^d, d>n so extra dims are unused
exact = np.max(np.abs(g))
val_40restarts, _ = estimate_injective_norm(A, g, n_restarts=40, n_iter=60, rng=rng)
val_200restarts, _ = estimate_injective_norm(A, g, n_restarts=200, n_iter=100, rng=rng)
print(f"n={n} d={d}: exact max|g_i|={exact:.6f}")
print(
    f"  power_iter(40 restarts, as used in H-CAT30-2)  ={val_40restarts:.6f}  "
    f"deficit={exact - val_40restarts:.6f} ({(exact - val_40restarts) / exact:.4%})"
)
print(
    f"  power_iter(200 restarts, generous)               ={val_200restarts:.6f}  "
    f"deficit={exact - val_200restarts:.6f} ({(exact - val_200restarts) / exact:.4%})"
)

print("\n=== Part 3: certified lower bound via G^3 (skeptic's free check) ===")
G = A @ A.T
lb = np.abs((G**3) @ g).max()
print(f"lb = max_i |f(a_i)| = {lb:.6f} vs exact {exact:.6f} (should equal for orthonormal case)")
