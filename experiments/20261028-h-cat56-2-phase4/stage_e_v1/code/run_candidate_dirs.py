# WHY: fix the 280 candidate directions x_k (from the float POVM) and ask whether EXACT weights and
# y_k in Y_S+(x_k) can satisfy sum_k w_k v_k v_k^dag = I_22.  This is the joint "correction of
# weights and vectors" test restricted to the candidate's own directions (no grid assumption).
import json, time
import numpy as np
from ys_space import load_A, y_basis, S_PLUS
from sdp_feas import solve

NPZ = (r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
       r"\20261027-h-cat56-2-discovery\metrics\s14_povm_prefix12.npz")
d = np.load(NPZ)
V = d["vectors"]
x_list = [V[k, :2] for k in range(V.shape[0])]
A = load_A(S_PLUS)
t0 = time.time()
Bs, ranks = [], []
for x in x_list:
    B, s, rank = y_basis(x, A, S_PLUS)
    Bs.append(B); ranks.append(rank)
X = np.array(x_list)
print("grid points:", len(Bs), " kernel dims:", sorted(set(B.shape[1] for B in Bs)))
TI2 = np.eye(2, dtype=complex); TI20 = np.eye(20, dtype=complex); TX = np.zeros((2, 20), complex)
st, Ms, prob = solve(X, Bs, TI2, TI20, TX, eps_abs=1e-9, eps_rel=1e-9, max_iters=200000)
out = {"directions": "candidate x_k (280)", "status": st, "seconds": round(time.time() - t0, 1)}
if st in ("optimal", "optimal_inaccurate"):
    tw = np.array([float(M.value[-1, -1]) for M in Ms])
    out.update({"t_min": float(tw.min()), "n_t_positive": int((tw > 1e-10).sum()), "sum_t": float(tw.sum())})
print(json.dumps(out, indent=1))
