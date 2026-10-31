# WHY: kernel dimension of Y_S+(x_k) at the 280 candidate directions and smallest kept singular values.
import numpy as np
from ys_space import load_A, y_basis, S_PLUS
NPZ = (r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
       r"\20261027-h-cat56-2-discovery\metrics\s14_povm_prefix12.npz")
V = np.load(NPZ)["vectors"]
A = load_A(S_PLUS)
dims, gap = [], []
for k in range(V.shape[0]):
    B, s, rank = y_basis(V[k, :2], A, S_PLUS)
    dims.append(B.shape[1]); gap.append((s[rank - 1], s[rank] if rank < len(s) else 0.0))
dims = np.array(dims)
vals, cnt = np.unique(dims, return_counts=True)
print("kernel dim counts over 280 candidate directions:", dict(zip(vals.tolist(), cnt.tolist())))
g = np.array(gap)
print("min kept sing. value:", g[:, 0].min(), " max dropped sing. value:", g[:, 1].max())
ylocal = [k for k in range(len(dims)) if dims[k] != 4]
print("indices with dim != 4 (first 20):", ylocal[:20])
