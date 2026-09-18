"""
Independently re-verify the skeptic's core claim BEFORE accepting it:
(1) f(x) = sum_i g_i <a_i,x>^3 depends on x only through u=Ax in R^n, so the
    optimizer's found x* should increasingly lie in span{a_i} as d grows
    (project x* onto span{a_i}, check the orthogonal-component norm).
(2) as d->infty with n fixed, G=AA^T -> I, and the true sup should converge
    to E[max_i|g_i|] for n iid standard normals -- verify this closed-form
    value both by direct high-N Monte Carlo AND by numerical integration,
    then compare to the actually observed plateau (2.1565) from the pilot.
"""

import numpy as np
from scipy import integrate, stats
from tensor_injective_norm import estimate_injective_norm

# --- Part 1: verify E[max_i |g_i|] for n=20 iid N(0,1) ---
n = 20
rng = np.random.default_rng(2026)

# (a) direct massive Monte Carlo
N = 4_000_000
Z = rng.standard_normal((N, n))
maxabs = np.max(np.abs(Z), axis=1)
mc_mean = maxabs.mean()
mc_se = maxabs.std(ddof=1) / np.sqrt(N)
print(f"(a) Monte Carlo E[max_i|Z_i|], n={n}, N={N}: {mc_mean:.5f} +/- {mc_se:.5f}")


# (b) numerical integration of E[X] = int_0^inf P(X>t) dt = int_0^inf (1-F(t)) dt
#     where F(t) = P(max|Z_i|<=t) = (2*Phi(t)-1)^n
def survival(t):
    return 1.0 - (2 * stats.norm.cdf(t) - 1) ** n


val, err = integrate.quad(survival, 0, 50)
print(f"(b) Numerical integration E[max_i|Z_i|]: {val:.5f} (quad err est {err:.2e})")

# --- Part 2: does the optimizer's x* increasingly concentrate in span{a_i} as d grows? ---
print()
for d in (5, 20, 40, 80, 160, 400):
    A = rng.standard_normal((n, d))
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    g = rng.standard_normal(n)
    val, x_star = estimate_injective_norm(A, g, n_restarts=60, n_iter=80, rng=rng)

    # orthogonal projection residual of x* onto span(rows of A)
    # (rows of A are the a_i; project x* onto their span via QR)
    Q, _ = np.linalg.qr(A.T)  # Q: d x min(n,d) orthonormal basis for span{a_i}
    proj = Q @ (Q.T @ x_star)
    resid_norm = np.linalg.norm(x_star - proj)
    print(
        f"d={d:4d}: injective-norm estimate={val:.4f}  "
        f"||x* - proj_span(x*)||={resid_norm:.2e}  ||x*||={np.linalg.norm(x_star):.4f}"
    )

# --- Part 3: does the estimate converge to E[max_i|g_i|] as d/n -> infty? ---
print()
print(f"Predicted asymptotic plateau (E[max_i|g_i|], n={n}): {mc_mean:.4f}")
print("Pilot's own reported plateau (weighted const, d=40,80,160): 2.1565")
print(f"Relative gap: {abs(mc_mean - 2.1565) / mc_mean:.4%}")
