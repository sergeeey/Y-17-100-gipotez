# WHY: positive control (known feasible target built from random moments) and
# negative control (S- = {4..15}: stage C Theorem C says I_20 not in cone -> must be infeasible).
import numpy as np
from ys_space import load_A, S_PLUS
from sdp_feas import build_grid, solve

rng = np.random.default_rng(1)
J = 120
Xp, Bp = build_grid(S_PLUS, J)
m = Bp[0].shape[1]

# positive control: random PSD moments -> targets they produce -> must be feasible
TI2 = np.zeros((2, 2), complex); TX = np.zeros((2, 20), complex); TI20 = np.zeros((20, 20), complex)
for j in range(J):
    G = rng.normal(size=(m + 1, m + 1)); M = G @ G.T
    t, s, Q = M[m, m], M[:m, m], M[:m, :m]
    TI2 += t * np.outer(Xp[j], Xp[j].conj())
    TX += np.outer(Xp[j], (Bp[j] @ s).conj())
    TI20 += Bp[j] @ Q @ Bp[j].conj().T
st, _, pr = solve(Xp, Bp, TI2, TI20, TX, eps_abs=1e-9, eps_rel=1e-9, max_iters=200000)
print("positive control (must be feasible):", st)

# negative control: S- with identity target
Xm, Bm = build_grid(list(range(4, 16)), J)
TI2 = np.eye(2, dtype=complex); TI20 = np.eye(20, dtype=complex); TX = np.zeros((2, 20), complex)
st, _, pm = solve(Xm, Bm, TI2, TI20, TX, eps_abs=1e-9, eps_rel=1e-9, max_iters=200000)
print("negative control S- (expected infeasible per stage C):", st)
