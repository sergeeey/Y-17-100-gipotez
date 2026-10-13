"""AP test: for R, is there h in L(R) with 3 distinct eigenvalues in arithmetic progression (=> locally ACC)?
For dimL==2, L=span{1,h}; AP is affine-invariant so test eigenvalues of h directly. Applied after random local conjugation."""
import numpy as np
from ybe import *
def is_ap(ev, tol=1e-6):
    e = list(ev); sc = max(np.abs(e).max(), 1e-12)
    for i in range(3):
        a, b, c = e[i], e[(i+1)%3], e[(i+2)%3]
        if abs(a + c - 2*b) < tol*sc: return True
    return False
def ap_label(R, N=3):
    null, s = L_algebra(R, N)
    d = len(null)
    if d != 2: return ('dimL=%d' % d, None)
    # the non-scalar element: remove identity component
    h = [b for b in null if np.linalg.norm(b - np.trace(b)/N*np.eye(N)) > 1e-6]
    h = h[0] - np.trace(h[0])/N*np.eye(N) if h else None
    ev = np.linalg.eigvals(h)
    dist = min(abs(ev[i]-ev[j]) for i in range(3) for j in range(i+1,3))/np.abs(ev).max()
    return ('dimL=2', 'distinct' if dist>1e-4 else 'repeated', 'AP' if is_ap(ev) else 'nonAP')
rng = np.random.default_rng(5)
fam = table1_families(rng)
for nm, R in fam.items():
    g = rng.normal(size=(3,3)) + 1j*rng.normal(size=(3,3)); G = np.kron(g, g)
    Rc = G @ R @ np.linalg.inv(G)
    Rc = Rc/abs(np.linalg.det(Rc))**(1/9)
    print('%-26s conj-res %.1e  %s' % (nm, rel_res(Rc,3), ap_label(Rc)))
# negative control: a non-ACC solution (rank-3 Gaussian) must say not-AP/U1-free
w = np.exp(2j*np.pi/3); X = np.roll(np.eye(3),1,axis=0); Z = np.diag([w**j for j in range(3)])
PS = np.kron(X, Z); Gs = (np.eye(9) + w*(PS+PS@PS))/np.sqrt(3)
print('Gaussian res %.1e' % rel_res(Gs,3), ap_label(Gs))
