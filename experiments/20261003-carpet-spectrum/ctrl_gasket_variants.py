import numpy as np
from lib import *
def S(n, kind):
    A, v = gasket_graph(n)
    if kind == "4L2":
        return np.linalg.eigvalsh((4*laplacian(A, "L2")).toarray())
    if kind == "dirichlet":
        v = np.array(v); side = 2**n
        corner = [(0,0),(side,0),(0,side)]
        keep = [i for i,p in enumerate(map(tuple, v)) if p not in corner]
        M = (4*sp.identity(A.shape[0]) - A).tocsr()[keep][:, keep]
        return np.linalg.eigvalsh(M.toarray())
R = lambda z: z*(5-z)
for kind in ["4L2", "dirichlet"]:
    print(kind)
    for n in range(2, 6):
        a, ma = cluster(S(n, kind)); b, mb = cluster(S(n+1, kind))
        inc = 0; excl = []
        for mu in b:
            lam = R(mu)
            if np.min(np.abs(a-lam)) <= 1e-8: inc += 1
            else: excl.append(round(float(mu), 6))
        print(f" {n}->{n+1}: distinct {len(a)}->{len(b)} included {inc}  not-included {len(excl)} sample {excl[:6]}")
