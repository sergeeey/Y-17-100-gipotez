import numpy as np, scipy.sparse.linalg as sla
from lib import *
A, xy = carpet_graph(5)
L = laplacian(A, "L1").tocsc()
ev = np.sort(np.load("../carpet_spectra_L1_n5.npz")["n5"])
hi = np.sort(sla.eigsh(L, k=6, which="LA", tol=1e-12, ncv=80, return_eigenvectors=False))
print("ARPACK tight top6", hi); print("stored top6     ", ev[-6:]); print("maxdiff", np.abs(hi-ev[-6:]).max())
