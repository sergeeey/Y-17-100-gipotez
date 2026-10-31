# WHY: SDP restricted to the real circle x = (cos a, sin a), where Y_S+(x) has exact real dim 6.
# Tests whether directions on the circle alone can give exact I_22 (no complex directions needed).
import sys, json, time
import numpy as np
from ys_space import load_A, y_basis, S_PLUS
from sdp_feas import solve

J = int(sys.argv[1]) if len(sys.argv) > 1 else 48
A = load_A(S_PLUS)
t0 = time.time()
a_grid = np.pi * np.arange(J) / J  # real directions up to sign; sign does not change Y(x)
X = np.array([np.array([np.cos(a), np.sin(a)], dtype=complex) for a in a_grid])
Bs = []
for x in X:
    B, s, rank = y_basis(x, A, S_PLUS, tol=1e-12)
    Bs.append(B)
dims = sorted(set(B.shape[1] for B in Bs))
TI2 = np.eye(2, dtype=complex); TI20 = np.eye(20, dtype=complex); TX = np.zeros((2, 20), complex)
st, Ms, prob = solve(X, Bs, TI2, TI20, TX, eps_abs=1e-9, eps_rel=1e-9, max_iters=200000)
out = {"J": J, "dims": dims, "status": st, "seconds": round(time.time() - t0, 1)}
if st in ("optimal", "optimal_inaccurate"):
    tw = np.array([float(M.value[-1, -1]) for M in Ms])
    out.update({"t_min": float(tw.min()), "t_max": float(tw.max()), "n_t_positive_1e-10": int((tw > 1e-10).sum())})
print(json.dumps(out, indent=1))
