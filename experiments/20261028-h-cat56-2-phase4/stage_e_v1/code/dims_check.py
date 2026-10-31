# WHY: check real dimension of Y_S+(x) over random directions, and the singular-value gap (rank jumps).
import numpy as np
from ys_space import load_A, y_basis, bloch_x, S_PLUS

A = load_A(S_PLUS)
rng = np.random.default_rng(0)
dims, gaps = [], []
for _ in range(200):
    th, ph = np.arccos(rng.uniform(-1, 1)), rng.uniform(0, 2 * np.pi)
    B, s, rank = y_basis(bloch_x(th, ph), A)
    dims.append(B.shape[1])
    gaps.append((s[rank - 1] if rank > 0 else 0, s[rank] if rank < len(s) else 0))
dims = np.array(dims)
print("kernel dims over 200 random directions:", dict(zip(*np.unique(dims, return_counts=True))))
print("min sing. value kept (rank side):", min(g[0] for g in gaps), " max sing. value dropped:", max(g[1] for g in gaps))
