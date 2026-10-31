# WHY: exact-target SDP for S+ = {0..11} on a Fibonacci grid of J directions (identity targets).
# Saves status, weights per grid point, and residual of the equality system for the first pass.
import sys, json, time
import numpy as np
from ys_space import S_PLUS
from sdp_feas import build_grid, solve

J = int(sys.argv[1]) if len(sys.argv) > 1 else 200
t0 = time.time()
X, Bs = build_grid(S_PLUS, J)
TI2 = np.eye(2, dtype=complex); TI20 = np.eye(20, dtype=complex); TX = np.zeros((2, 20), complex)
st, Ms, prob = solve(X, Bs, TI2, TI20, TX, eps_abs=1e-9, eps_rel=1e-9, max_iters=200000)
out = {"J": J, "status": st, "seconds": round(time.time() - t0, 1)}
if st in ("optimal", "optimal_inaccurate"):
    tw = np.array([float(M.value[-1, -1]) for M in Ms])
    out.update({"sum_t": float(tw.sum()), "t_min": float(tw.min()), "t_max": float(tw.max()),
                "n_t_positive_1e-10": int((tw > 1e-10).sum())})
    # residual of identity on the x-block and y-block from the solution
    m = Bs[0].shape[1]
    R20 = np.zeros((20, 20), complex); R2 = np.zeros((2, 2), complex); RX = np.zeros((2, 20), complex)
    for j in range(J):
        Mj = Ms[j].value; t = Mj[m, m]; s = Mj[:m, m]; Q = Mj[:m, :m]
        R2 += t * np.outer(X[j], X[j].conj())
        RX += np.outer(X[j], (Bs[j] @ s).conj())
        R20 += Bs[j] @ Q @ Bs[j].conj().T
    out.update({"res_I2": float(np.abs(R2 - TI2).max()), "res_cross": float(np.abs(RX).max()),
                "res_I20": float(np.abs(R20 - TI20).max())})
print(json.dumps(out, indent=1))
np.savez(f"../logs/splus_grid_J{J}.npz", X=X, status=st)
