"""
Skeptical robustness check BEFORE writing anything to decision.md: does the
apparent flat/decreasing trend in tensor_conj16_pilot.py survive a much
larger restart budget at the largest d values, or is it a curse-of-
dimensionality search artifact (fixed 50 restarts underestimating the true
sup as d grows, since the search space of unit directions grows with d)?
"""

import numpy as np
from tensor_injective_norm import estimate_injective_norm

n = 20
seed = 0
rng = np.random.default_rng(seed)

# Reproduce EXACT same tensor families as the pilot (same seed, same draw order)
d_values = (5, 10, 20, 40, 80, 160)
n_gaussian_draws = 60

families = {}
gaussian_draws_by_d = {}
for d in d_values:
    A = rng.standard_normal((n, d))
    A = A / np.linalg.norm(A, axis=1, keepdims=True)
    families[d] = A
    draws_g = []
    for _ in range(n_gaussian_draws):
        g = rng.standard_normal(n)
        draws_g.append(g)
        _ = estimate_injective_norm(
            A, g, n_restarts=50, n_iter=70, rng=rng
        )  # consume rng identically
    gaussian_draws_by_d[d] = draws_g

# Now re-estimate at d=80 and d=160 with a MUCH larger restart budget on the
# SAME (A, g) pairs used by the pilot, and compare.
for d in (80, 160):
    A = families[d]
    gs = gaussian_draws_by_d[d]
    rng2 = np.random.default_rng(12345 + d)
    vals_small = []
    vals_large = []
    for g in gs[:20]:  # subset for speed
        v_small, _ = estimate_injective_norm(A, g, n_restarts=50, n_iter=70, rng=rng2)
        v_large, _ = estimate_injective_norm(A, g, n_restarts=400, n_iter=150, rng=rng2)
        vals_small.append(v_small)
        vals_large.append(v_large)
    vals_small = np.array(vals_small)
    vals_large = np.array(vals_large)
    print(
        f"d={d}: mean(50 restarts)={vals_small.mean():.4f}  "
        f"mean(400 restarts)={vals_large.mean():.4f}  "
        f"relative increase={(vals_large.mean() - vals_small.mean()) / vals_small.mean():.4%}  "
        f"max single-draw increase={(vals_large - vals_small).max():.4f}"
    )
