"""Q-C for cand101: exact 3-parameter family (e,u,v), symbolic braid check + numeric match to the candidate."""
import sys, numpy as np, sympy as sp, json
R1 = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-ybe-dim3-beyond-acc"
sys.path.insert(0, R1)
from ybe import braid_residual
e, u, v = sp.symbols('e u v')
def fam(e, u, v, lam=1):
    R = sp.zeros(9, 9)
    R[0, 0] = R[4, 4] = R[8, 8] = 1
    R[1, 3] = 1 - e; R[3, 1] = 1; R[3, 3] = e
    R[2, 2] = 1; R[6, 6] = 1
    R[5, 2] = 1; R[5, 5] = e; R[5, 6] = (e-1)*v/u; R[5, 7] = -(e-1)/u
    R[7, 2] = u/(e-1); R[7, 5] = u; R[7, 6] = v
    return lam*R
Rs = fam(e, u, v)
I3 = sp.eye(3)
A = sp.kronecker_product(Rs, I3); B = sp.kronecker_product(I3, Rs)
F = (A*B*A - B*A*B).applyfunc(sp.simplify)
nz = [q for q in F if q != 0]
print('SYMBOLIC braid residual nonzero entries over Q(e,u,v):', len(nz), flush=True)
print('charpoly of Rs:', sp.factor(Rs.charpoly(sp.symbols('x')).as_expr()))
# numeric match
d = np.load(R1 + '/d3_w001.npz', allow_pickle=True)
W = [0, 1, 3, 4]; S1 = [2, 5, 6, 7]
R = d['R'][101].copy(); R[abs(R) < 1e-13] = 0
B0 = R[np.ix_(W, W)]
cols = []
for k in range(4):
    h = np.zeros((2, 2)); h[k//2, k%2] = 1
    D = np.kron(h, np.eye(2)) + np.kron(np.eye(2), h)
    cols.append((B0@D - D@B0).reshape(-1))
uu, s, vh = np.linalg.svd(np.array(cols).T)
Ls = [vh[i].conj().reshape(2, 2) for i in range(4) if s[i] < 1e-9]
h = max([x - np.trace(x)/2*np.eye(2) for x in Ls], key=np.linalg.norm)
ev, V = np.linalg.eig(h)
g = np.eye(3, dtype=complex); g[:2, :2] = V; G = np.kron(g, g)
Rn = np.linalg.inv(G) @ R @ G
lam = Rn[0, 0]; Rn = Rn / lam
ec = Rn[3, 3]
print('e_c =', ec, ' B0[1,2] (should be 1-e):', Rn[1, 3], 1 - ec, ' B0[3,1] (should be 1):', Rn[3, 1])
# gauge s0/s1 : entry R[5,2] -> multiply by r ; entries (out idx, in idx) with V0-index o,i scale by s_i/s_o.
idx0 = {2: 0, 5: 1, 6: 0, 7: 1}   # V0 index of the state in B1
def gauge(M, r):  # conj by diag(1,r,1): entry out<-in scales by w_in/w_out with w(index)= (1,r)[idx]
    Mg = M.copy()
    for o in S1:
        for i in S1:
            Mg[o, i] = M[o, i] * ((1, r)[idx0[i]]) / ((1, r)[idx0[o]])
    return Mg
r = 1 / Rn[5, 2] * 1.0
# entry 5<-2 : out idx1 (weight r), in idx 0 (weight 1) -> factor 1/r ; want 1 => r = Rn[5,2]
r = Rn[5, 2]
Rg = gauge(Rn, r)
print('after gauge x1 =', Rg[5, 2])
uc = Rg[7, 5]; vc = Rg[7, 6]
print('u_c =', uc, 'v_c =', vc)
Rfam = np.array(fam(sp.nsimplify(0), 1, 1).tolist(), dtype=complex)  # placeholder to get shape
def famnum(e, u, v):
    R = np.zeros((9, 9), complex)
    R[0, 0] = R[4, 4] = R[8, 8] = 1
    R[1, 3] = 1 - e; R[3, 1] = 1; R[3, 3] = e
    R[2, 2] = 1; R[6, 6] = 1
    R[5, 2] = 1; R[5, 5] = e; R[5, 6] = (e-1)*v/u; R[5, 7] = -(e-1)/u
    R[7, 2] = u/(e-1); R[7, 5] = u; R[7, 6] = v
    return R
Rf = famnum(ec, uc, vc)
print('max |candidate_gauged/lam - family(e_c,u_c,v_c)| =', np.abs(Rg - Rf).max())
print('family braid residual numeric', np.linalg.norm(braid_residual(Rf, 3))/np.linalg.norm(Rf)**3)
# negative control: perturb u by 1% in only one entry
Rp = Rf.copy(); Rp[5, 6] *= 1.01
print('N: perturbed entry residual', np.linalg.norm(braid_residual(Rp, 3))/np.linalg.norm(Rp)**3)
json.dump({'symbolic_nonzero_residual_entries': len(nz), 'e': [ec.real, ec.imag], 'u': [uc.real, uc.imag], 'v': [vc.real, vc.imag], 'lam': [lam.real, lam.imag]}, open('s06_out.json', 'w'))
