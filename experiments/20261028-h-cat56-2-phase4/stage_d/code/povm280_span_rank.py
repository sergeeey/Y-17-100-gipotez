# WHY: if I_22 is not in span{v_k v_k^H}, no weight correction (w -> w + dw) can make the sum exact,
# so the vectors themselves must move. Float SVD here is a HEURISTIC rank, not a certificate.
import numpy as np

P = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261027-h-cat56-2-discovery\metrics\s14_povm_prefix12.npz"
z = np.load(P)
V = z["vectors"]
w = z["weights"]
K, d = V.shape
cols = []
for k in range(K):
    M = np.outer(V[k], V[k].conj())
    cols.append(np.concatenate([M.real.ravel(), M.imag.ravel()]))
A = np.array(cols).T  # (2*d*d) x K
I = np.eye(d, dtype=complex)
b = np.concatenate([I.real.ravel(), I.imag.ravel()])
sA = np.linalg.svd(A, compute_uv=False)
sAb = np.linalg.svd(np.column_stack([A, b]), compute_uv=False)
print("rank-one span matrix A shape:", A.shape)
print("singular values A: max", sA[0], "min(last 5)", sA[-5:])
print("numerical rank A (tol 1e-10*max):", int(np.sum(sA > 1e-10 * sA[0])))
print("numerical rank [A|b] (tol 1e-10*max):", int(np.sum(sAb > 1e-10 * sAb[0])))
x, res, rk, _ = np.linalg.lstsq(A, b, rcond=1e-12)
print("lstsq residual ||A x - b||:", np.linalg.norm(A @ x - b))
print("max |x - w| (lstsq vs candidate weights):", np.max(np.abs(x - w)))
print("min(w + x - w) = min(x):", x.min(), " (positivity of corrected weights needs w + dx > 0)")
