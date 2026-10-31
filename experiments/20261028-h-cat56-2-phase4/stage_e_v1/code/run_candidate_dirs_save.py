# WHY: re-solve the 280-direction exact-target SDP (candidate directions) and SAVE the moments M_j,
# then verify residuals of (a),(b),(c) and the minimal eigenvalue of each M_j (interior => Newton-polish possible).
# Looser tolerance than the first run (eps 1e-7) to fit the time budget; residuals are measured, not assumed.
import json, time
import numpy as np
from ys_space import load_A, y_basis, S_PLUS
from sdp_feas import solve

NPZ = (r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
       r"\20261027-h-cat56-2-discovery\metrics\s14_povm_prefix12.npz")
V = np.load(NPZ)["vectors"]
X = V[:, :2].copy()
A = load_A(S_PLUS)
Bs = [y_basis(X[k], A, S_PLUS)[0] for k in range(len(X))]
TI2 = np.eye(2, dtype=complex); TI20 = np.eye(20, dtype=complex); TX = np.zeros((2, 20), complex)
t0 = time.time()
st, Ms, prob = solve(X, Bs, TI2, TI20, TX, eps_abs=1e-7, eps_rel=1e-7, max_iters=100000)
out = {"status": st, "seconds": round(time.time() - t0, 1)}
if st in ("optimal", "optimal_inaccurate"):
    vals = [M.value for M in Ms]
    R2 = np.zeros((2, 2), complex); RX = np.zeros((2, 20), complex); R20 = np.zeros((20, 20), complex)
    mineig = []
    for j, Mv in enumerate(vals):
        mj = Bs[j].shape[1]; t = Mv[mj, mj]; s = Mv[:mj, mj]; Q = Mv[:mj, :mj]
        R2 += t * np.outer(X[j], X[j].conj())
        RX += np.outer(X[j], (Bs[j] @ s).conj())
        R20 += Bs[j] @ Q @ Bs[j].conj().T
        mineig.append(np.linalg.eigvalsh(Mv).min())
    mineig = np.array(mineig)
    out.update({"res_I2": float(np.abs(R2 - TI2).max()), "res_cross": float(np.abs(RX).max()),
                "res_I20": float(np.abs(R20 - TI20).max()),
                "min_eig_M": float(mineig.min()), "n_M_with_min_eig_gt_1e-8": int((mineig > 1e-8).sum())})
    np.savez("../logs/candidate_dirs_M.npz", *vals)
print(json.dumps(out, indent=1))
