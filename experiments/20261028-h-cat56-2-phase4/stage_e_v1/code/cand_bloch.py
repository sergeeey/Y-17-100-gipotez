# WHY: where on the Bloch sphere are the dim-6 candidate directions? (structure check, not a proof)
import numpy as np
from ys_space import load_A, y_basis, S_PLUS
NPZ = (r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
       r"\20261027-h-cat56-2-discovery\metrics\s14_povm_prefix12.npz")
V = np.load(NPZ)["vectors"]
A = load_A(S_PLUS)
rows = []
for k in range(V.shape[0]):
    x = V[k, :2]
    B, s, rank = y_basis(x, A, S_PLUS)
    nrm = np.linalg.norm(x) ** 2
    n = np.array([2 * (x[0].conjugate() * x[1]).real, 2 * (x[0].conjugate() * x[1]).imag, abs(x[0]) ** 2 - abs(x[1]) ** 2]) / nrm
    rows.append((k, B.shape[1], *np.round(n, 4), round(float(abs(x[0]) ** 2 / nrm), 4)))
rows = np.array(rows, dtype=float)
for dim in (4, 5, 6):
    sel = rows[rows[:, 1] == dim]
    if len(sel):
        print(f"dim {dim}: n={len(sel)}  nz range [{sel[:,4].min():.4f},{sel[:,4].max():.4f}]  |n_x| range [{np.abs(sel[:,2]).min():.4f},{np.abs(sel[:,2]).max():.4f}]  |n_y| range [{np.abs(sel[:,3]).min():.4f},{np.abs(sel[:,3]).max():.4f}]")
np.save("../logs/cand_bloch.npy", rows)
