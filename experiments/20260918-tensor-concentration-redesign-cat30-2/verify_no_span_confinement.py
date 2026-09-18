"""Confirm the redesign's n>=d scaling actually removes the span-confinement
degeneracy: with n=d (or n=d^1.5), span{a_i} should generically equal R^d
(full rank), so the 'x* confined to an at-most-n-dim proper subspace' issue
from H-CAT30-1 cannot recur in the same form. Directly check rank(A) and the
projection residual as before."""

import numpy as np
from tensor_injective_norm import estimate_injective_norm

rng = np.random.default_rng(555)
for d, n in [(10, 10), (40, 40), (20, 89)]:
    A = rng.standard_normal((n, d))
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    rank = np.linalg.matrix_rank(A)
    g = rng.standard_normal(n)
    _, x_star = estimate_injective_norm(A, g, n_restarts=40, n_iter=60, rng=rng)
    print(
        f"d={d:3d} n={n:3d}: rank(A)={rank} (full d-rank? {rank == d}), "
        f"||x*||={np.linalg.norm(x_star):.4f}"
    )
