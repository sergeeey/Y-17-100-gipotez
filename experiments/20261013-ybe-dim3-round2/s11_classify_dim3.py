import sys, numpy as np
R1 = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-ybe-dim3-beyond-acc"
sys.path.insert(0, R1)
from ybe import L_algebra, jac_F, braid_residual
sys.path.insert(0, '.')
from s09_sampler import spec_geom
d = np.load('s09_dim3_a.npz', allow_pickle=True); rng = np.random.default_rng(0)
print('n solutions', len(d['R']))
for i, R in enumerate(d['R']):
    Rn = R/np.abs(np.linalg.det(R))**(1/9)
    sg = spec_geom(Rn, 3)
    if sg != ((7, 7), (2, 2)): continue
    Ls, _ = L_algebra(Rn, 3, tol=1e-8)
    # eigenvalue pattern of generic element of L
    h = sum(rng.normal()*x for x in Ls) if len(Ls) > 1 else Ls[0]
    ev = np.linalg.eigvals(h)
    # normalise pattern: number of distinct eigenvalues
    nd = 1 + (abs(ev[0]-ev[1]) > 1e-6*max(1, abs(ev).max())) + (abs(ev[0]-ev[2]) > 1e-6*max(1, abs(ev).max()) and abs(ev[1]-ev[2]) > 1e-6*max(1, abs(ev).max()))
    J = jac_F(Rn, 3); s = np.linalg.svd(J, compute_uv=False); td = int((s < 1e-9*s[0]).sum())
    e = np.linalg.eigvals(Rn); lam = max(set(np.round(e, 5)), key=lambda z: (abs(e - z) < 1e-4).sum()); 
    print('sol', i, 'dimL', len(Ls), 'distinct eigenvalues of generic L element:', nd, ' tangent dim', td, ' res', np.linalg.norm(braid_residual(Rn, 3))/np.linalg.norm(Rn)**3)
