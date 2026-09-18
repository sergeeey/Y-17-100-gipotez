"""
Verify BEFORE using it as a certified upper bound: for a symmetric order-3
tensor S = sum_i g_i a_i^{otimes 3}, does sigma_max(M) >= ||S||_{I_2}, where
M is the mode-1 matricization (d x d^2)?

Argument: injective norm max_{||x||=1} |S(x,x,x)| is a maximum over the
RESTRICTED set {(x, x centerdot x) : ||x||=1} subset {(u,W): ||u||=1,
||W||_F=1}. The matricization operator norm maximizes over the LARGER set
(independent u, W) -- so sigma_max(M) >= ||S||_{I_2} always. Verify this
numerically on several random small cases where the power-iteration LOWER
bound is already independently cross-checked against scipy.
"""

import numpy as np
from tensor_injective_norm import estimate_injective_norm


def matricization_upper_bound(A, g, d):
    """M[k,(l,m)] = S_{klm} = sum_i g_i a_i[k] a_i[l] a_i[m].
    Build M as (d, d*d) and return its top singular value."""
    n = A.shape[0]
    M = np.zeros((d, d * d))
    for i in range(n):
        a = A[i]
        outer = np.outer(a, a).reshape(-1)  # a_l * a_m, length d*d
        M += g[i] * np.outer(a, outer)  # a_k * (a_l*a_m)
    sv = np.linalg.svd(M, compute_uv=False)
    return sv[0]


def main():
    rng = np.random.default_rng(3)
    for d, n in [(5, 8), (10, 15), (20, 25), (40, 50)]:
        A = rng.standard_normal((n, d))
        A = A / np.linalg.norm(A, axis=1, keepdims=True)
        g = rng.standard_normal(n)
        lower, _ = estimate_injective_norm(A, g, n_restarts=80, n_iter=80, rng=rng)
        upper = matricization_upper_bound(A, g, d)
        ok = "OK" if upper >= lower - 1e-9 else "VIOLATED"
        print(
            f"d={d:3d} n={n:3d}: lower(power-iter)={lower:.4f}  "
            f"upper(matricization SVD)={upper:.4f}  ratio={upper / lower:.3f}  [{ok}]"
        )


if __name__ == "__main__":
    main()
