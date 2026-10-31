# WHY: diagnose solver failure on the positive control (scale, solver choice).
import numpy as np, cvxpy as cp
from ys_space import S_PLUS
from sdp_feas import build_grid, solve

rng = np.random.default_rng(1)
J = 120
Xp, Bp = build_grid(S_PLUS, J)
m = Bp[0].shape[1]
TI2 = np.zeros((2, 2), complex); TX = np.zeros((2, 20), complex); TI20 = np.zeros((20, 20), complex)
for j in range(J):
    G = rng.normal(size=(m + 1, m + 1)); M = G @ G.T
    t, s, Q = M[m, m], M[:m, m], M[:m, :m]
    TI2 += t * np.outer(Xp[j], Xp[j].conj())
    TX += np.outer(Xp[j], (Bp[j] @ s).conj())
    TI20 += Bp[j] @ Q @ Bp[j].conj().T
print("target norms:", np.abs(TI2).max(), np.abs(TX).max(), np.abs(TI20).max())
for sol in ["SCS", "CLARABEL"]:
    try:
        st, _, _ = solve(Xp, Bp, TI2, TI20, TX, solver=sol)
        print(sol, "->", st)
    except Exception as e:
        print(sol, "EXC", type(e).__name__, str(e)[:120])
