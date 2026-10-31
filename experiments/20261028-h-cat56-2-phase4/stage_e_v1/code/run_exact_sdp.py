# WHY: SDP on the EXACT directions (dyadic x_k, exact kernels).  Saves moments M_j for the certificate step.
import pickle, json, time
import numpy as np
from fractions import Fraction
from sdp_feas import solve
D = pickle.load(open("../logs/exact_dirs.pkl", "rb"))
X = np.array([np.array([complex(float(Fraction(a)), float(Fraction(b))) for a, b in d]) for d in D["dirs"]])
Bs = [np.array(b).T for b in D["bases"]]          # 20 x m complex
TI2 = np.eye(2, dtype=complex); TI20 = np.eye(20, dtype=complex); TX = np.zeros((2, 20), complex)
t0 = time.time()
st, Ms, prob = solve(X, Bs, TI2, TI20, TX, eps_abs=1e-8, eps_rel=1e-8, max_iters=100000)
out = {"status": st, "seconds": round(time.time() - t0, 1)}
if st in ("optimal", "optimal_inaccurate"):
    vals = [M.value for M in Ms]
    R2 = np.zeros((2, 2), complex); RX = np.zeros((2, 20), complex); R20 = np.zeros((20, 20), complex)
    mineig = []
    for j, Mv in enumerate(vals):
        mj = Bs[j].shape[1]; t = Mv[mj, mj]; s = Mv[:mj, mj]; Q = Mv[:mj, :mj]
        R2 += t * np.outer(X[j], X[j].conj()); RX += np.outer(X[j], (Bs[j] @ s).conj())
        R20 += Bs[j] @ Q @ Bs[j].conj().T; mineig.append(np.linalg.eigvalsh(Mv).min())
    out.update({"res_I2": float(np.abs(R2 - TI2).max()), "res_cross": float(np.abs(RX).max()),
                "res_I20": float(np.abs(R20 - TI20).max()), "min_eig_M": float(min(mineig))})
    pickle.dump({"M": vals, "dirs": D["dirs"], "dims": D["dims"]}, open("../logs/exact_sdp_M.pkl", "wb"))
print(json.dumps(out, indent=1))
