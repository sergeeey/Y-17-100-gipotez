"""Independent integrity check of stored level-5 spectra (UNVERIFIED, from the interrupted run): trace identities + eigsh lowest."""
import numpy as np, scipy.sparse.linalg as sla
from lib import *
A, xy = carpet_graph(5)
N = A.shape[0]; d = np.asarray(A.sum(1)).ravel()
print("V", N, "E", int(d.sum()//2))
for kind in ("L1", "L2"):
    ev = np.load(f"../carpet_spectra_{kind}_n5.npz")["n5"]
    L = laplacian(A, kind)
    tr = L.diagonal().sum(); tr2 = (L.multiply(L)).sum()
    print(kind, "len", len(ev), "min", ev.min(), "sum", ev.sum(), "trace", tr, "| sum sq", (ev**2).sum(), "trace(L^2)", tr2)
    lo = np.sort(sla.eigsh(L.tocsc(), k=12, sigma=-1e-3, which="LM", return_eigenvectors=False))
    print("   eigsh lowest 8 :", np.round(lo[:8], 10))
    print("   stored lowest 8:", np.round(np.sort(ev)[:8], 10), " maxdiff(12)", np.abs(lo - np.sort(ev)[:12]).max())
    hi = np.sort(sla.eigsh(L.tocsc(), k=6, which="LA", return_eigenvectors=False))
    print("   top diff", np.abs(hi - np.sort(ev)[-6:]).max())
