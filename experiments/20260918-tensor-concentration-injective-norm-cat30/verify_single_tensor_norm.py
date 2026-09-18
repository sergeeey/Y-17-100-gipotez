import numpy as np
from tensor_injective_norm import estimate_injective_norm

rng = np.random.default_rng(7)
for d in [5, 40, 160]:
    a = rng.standard_normal(d)
    a = a / np.linalg.norm(a)
    A = a.reshape(1, d)  # single tensor T = a^{otimes 3}
    g = np.array([1.0])
    val, x = estimate_injective_norm(A, g, n_restarts=80, n_iter=80, rng=rng)
    print(f"d={d}: numerically estimated ||T||_I2 = {val:.10f}  (exact claim: 1.0)")
