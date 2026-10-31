# WHY: numerical rank of the constraint operator A (484 x 6566) and independent row subset.
import numpy as np, scipy.linalg as sl
Af = np.load("../logs/A_float.npy")
s = np.linalg.svd(Af, compute_uv=False)
print("sing. values: top", s[:3], " 470th..", s[465:475], " last", s[-3:])
for thr in [1e-6, 1e-8, 1e-10]:
    print("numerical rank at thr", thr, ":", int((s > thr * s[0]).sum()))
# independent rows via QR with column pivoting on A^T
Q, R, P = sl.qr(Af.T, pivoting=True, mode="economic")
d = np.abs(np.diag(R))
rk = int((d > 1e-9 * d[0]).sum())
print("row-rank via pivoted QR (1e-9):", rk, " pivot diag tail:", d[rk-3:rk+3])
np.save("../logs/indep_rows.npy", np.sort(P[:rk]))
