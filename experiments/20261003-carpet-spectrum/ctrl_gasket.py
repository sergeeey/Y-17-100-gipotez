import numpy as np, json, time
from lib import *
res = {}
specs = {}
for n in range(0, 8):
    t = time.time()
    A, v = gasket_graph(n)
    N = A.shape[0]
    assert N == (3**(n+1)+3)//2, (n, N)
    ev = spectrum(laplacian(A, "L1"))
    specs[n] = ev
    print("gasket level", n, "N", N, "t=%.1fs" % (time.time()-t), flush=True)
np.savez("gasket_spectra.npz", **{f"L{n}": specs[n] for n in specs})
R = lambda z: z*(5-z)
tol = 1e-8
EXC = [2.0, 5.0, 6.0]
for n in range(0, 7):
    vals0, m0 = cluster(specs[n]); vals1, m1 = cluster(specs[n+1])
    bad = []; ok = 0; exc = []
    for mu, m in zip(vals1, m1):
        if any(abs(mu-e) < 1e-8 for e in EXC):
            exc.append((round(mu, 10), int(m))); continue
        lam = R(mu)
        j = np.argmin(np.abs(vals0-lam))
        if abs(vals0[j]-lam) <= tol:
            ok += 1
            # multiplicity check
            if m != m0[j]: bad.append(("mult", mu, int(m), int(m0[j])))
        else:
            bad.append(("noinc", float(mu), int(m), float(lam)))
    # reverse: every level-n eigenvalue (non-exceptional) has both preimages in level n+1?
    miss = 0
    for lam in vals0:
        disc = 25-4*lam
        if disc < -1e-12: miss += 1; continue
        for s in (+1, -1):
            mu = (5 + s*np.sqrt(max(disc, 0)))/2
            if np.min(np.abs(vals1-mu)) > 1e-7: miss += 1
    print(f"n={n}->{n+1}: distinct {len(vals0)}->{len(vals1)} included={ok} exceptional={exc} bad={len(bad)} missing_preimages={miss}")
    if bad[:3]: print("  bad sample", bad[:3])
