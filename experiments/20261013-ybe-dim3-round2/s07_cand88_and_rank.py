import sys, numpy as np, sympy as sp, json
R1 = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-ybe-dim3-beyond-acc"
sys.path.insert(0, R1)
from ybe import braid_residual, jac_F
np.set_printoptions(precision=6, suppress=True, linewidth=200)
# ---------- symbolic: diagonal dressing of H1,4 (braid form), parameters p,q,k,a,b,c
p, q, k, a, b, c = sp.symbols('p q k a b c')
def fam88(p, q, k, a, b, c, mod=sp):
    R = mod.zeros(9, 9)
    # V0 = {0,1}: pair index 3*i+j ; |00>=0 |01>=1 |10>=3 |11>=4
    R[0, 4] = p; R[1, 1] = k; R[3, 3] = k; R[4, 0] = q       # H1,4 = [[0,0,0,p],[0,k,0,0],[0,0,k,0],[q,0,0,0]]
    # braid-form dressing: Ř(x (x) e) = b e (x) x ; Ř(e (x) x) = a x (x) e ; Ř(ee) = c ee
    R[6, 2] = b; R[7, 5] = b      # |02>(2) -> |20>(6), |12>(5) -> |21>(7)
    R[2, 6] = a; R[5, 7] = a
    R[8, 8] = c
    return R
Rs = fam88(p, q, k, a, b, c)
I3 = sp.eye(3)
A = sp.kronecker_product(Rs, I3); B = sp.kronecker_product(I3, Rs)
F = (A*B*A - B*A*B).applyfunc(sp.expand)
print('cand88 family: symbolic braid residual nonzero entries =', sum(1 for x in F if x != 0), flush=True)
# ---------- numeric match
d = np.load(R1 + '/d3_w001.npz', allow_pickle=True)
W = [0, 1, 3, 4]; S1 = [2, 5, 6, 7]
R = d['R'][88].copy(); R[abs(R) < 1e-13] = 0
B0 = R[np.ix_(W, W)]
ev, V = np.linalg.eig(B0)
# eigenvalue with multiplicity 2 (k)
ks = [(i, j) for i in range(4) for j in range(i+1, 4) if abs(ev[i]-ev[j]) < 1e-6]
kk = ev[ks[0][0]]; print('k =', kk)
Nsp = np.linalg.svd(B0 - kk*np.eye(4))[2][-2:].conj().T   # 4x2 nullspace
M1 = Nsp[:, 0].reshape(2, 2); M2 = Nsp[:, 1].reshape(2, 2)
# rank-1 elements: det(x M1 + y M2) = 0
polys = np.polynomial.polynomial
def det2(x, y): m = x*M1 + y*M2; return np.linalg.det(m)
c0, c1, c2 = det2(0, 1), (det2(1, 1) - det2(1, -1))/2, (det2(1, 1) + det2(1, -1))/2 - det2(0, 1)
roots = np.roots([c2, c1, c0])   # x/y
mats = [r_*M1 + M2 for r_ in roots]
# each is rank-1 : a b^T
def split(M):
    u_, s_, vh_ = np.linalg.svd(M); return u_[:, 0]*s_[0], vh_[0]
(aa, bb), (bb2, aa2) = split(mats[0]), split(mats[1])
g2 = np.array([aa, split(mats[1])[0]]).T
g = np.eye(3, dtype=complex); g[:2, :2] = g2
G = np.kron(g, g); Rn = np.linalg.inv(G) @ R @ G
print('B0 in new gauge:\n', Rn[np.ix_(W, W)])
print('offpattern max', np.abs(Rn[np.ix_(W, W)] * (1 - np.array([[0,0,0,1],[0,1,0,0],[0,0,1,0],[1,0,0,0]]))).max())
B0n = Rn[np.ix_(W, W)]
pc, qc, kc = B0n[0, 3], B0n[3, 0], B0n[1, 1]
print('p,q,k', pc, qc, kc, ' H11-H22 =', B0n[1, 1] - B0n[2, 2])
bc = Rn[6, 2]; ac = Rn[2, 6]; cc = Rn[8, 8]
Rf = np.array(fam88(sp.Float(0), 0, 0, 0, 0, 0).tolist(), dtype=complex)
Rf = np.array(fam88(pc, qc, kc, ac, bc, cc, mod=None) if False else 0)  # placeholder
def num88(pc, qc, kc, ac, bc, cc):
    Rm = np.zeros((9, 9), complex)
    Rm[0, 4] = pc; Rm[1, 1] = kc; Rm[3, 3] = kc; Rm[4, 0] = qc
    Rm[6, 2] = bc; Rm[7, 5] = bc; Rm[2, 6] = ac; Rm[5, 7] = ac; Rm[8, 8] = cc
    return Rm
Rf = num88(pc, qc, kc, ac, bc, cc)
print('a,b,c', ac, bc, cc)
print('max |gauged candidate - family| =', np.abs(Rn - Rf).max(), ' family braid res', np.linalg.norm(braid_residual(Rf, 3))/np.linalg.norm(Rf)**3)
# ---------- tangent / orbit rank test for both candidates
def tangent_dim(R):
    J = jac_F(R, 3)
    s = np.linalg.svd(J, compute_uv=False)
    return int((s < 1e-9*s[0]).sum()) + (J.shape[1] - len(s)), s
def orbit_vecs(R):
    I3 = np.eye(3); out = []
    for kx in range(9):
        h = np.zeros((3, 3)); h[kx//3, kx % 3] = 1
        D = np.kron(h, I3) + np.kron(I3, h)
        out.append((D @ R - R @ D).reshape(-1))
    return out
def rank(vs, tol=1e-9):
    s = np.linalg.svd(np.array(vs).T, compute_uv=False); return int((s > tol*s[0]).sum())
res = {}
# 88: family derivatives
vec = lambda M: M.reshape(-1)
Rn88 = Rn
dp = np.zeros((9, 9), complex); dp[0, 4] = 1
dq = np.zeros((9, 9), complex); dq[4, 0] = 1
dk = np.zeros((9, 9), complex); dk[1, 1] = dk[3, 3] = 1
da = np.zeros((9, 9), complex); da[2, 6] = da[5, 7] = 1
db = np.zeros((9, 9), complex); db[6, 2] = db[7, 5] = 1
dc = np.zeros((9, 9), complex); dc[8, 8] = 1
fam_d = [vec(x) for x in (dp, dq, dk, da, db, dc)]
ob = orbit_vecs(Rn88)
td, _ = tangent_dim(Rn88)
print('cand88: tangent dim (nullity of dF) =', td, '| rank orbit =', rank(ob), '| rank orbit+family(6 params, incl scale as sum) =', rank(ob + fam_d), '| rank orbit+R+family', rank(ob + [vec(Rn88)] + fam_d))
res['88'] = [td, rank(ob), rank(ob + fam_d)]
# 101: use the gauged family F(e,u,v) with lam=1 (read from s06_out.json)
o = json.load(open('s06_out.json'))
ec = complex(*o['e']); uc = complex(*o['u']); vc = complex(*o['v'])
def num101(e, u, v):
    Rm = np.zeros((9, 9), complex)
    Rm[0, 0] = Rm[4, 4] = Rm[8, 8] = 1
    Rm[1, 3] = 1 - e; Rm[3, 1] = 1; Rm[3, 3] = e
    Rm[2, 2] = 1; Rm[6, 6] = 1
    Rm[5, 2] = 1; Rm[5, 5] = e; Rm[5, 6] = (e-1)*v/u; Rm[5, 7] = -(e-1)/u
    Rm[7, 2] = u/(e-1); Rm[7, 5] = u; Rm[7, 6] = v
    return Rm
R101 = num101(ec, uc, vc); h_ = 1e-6
fd = [(num101(ec + h_, uc, vc) - num101(ec - h_, uc, vc))/(2*h_), (num101(ec, uc + h_, vc) - num101(ec, uc - h_, vc))/(2*h_), (num101(ec, uc, vc + h_) - num101(ec, uc, vc - h_))/(2*h_)]
ob = orbit_vecs(R101); td, _ = tangent_dim(R101)
print('cand101: tangent dim =', td, '| rank orbit =', rank(ob), '| rank orbit+R =', rank(ob + [vec(R101)]), '| rank orbit+R+dE,dU,dV =', rank(ob + [vec(R101)] + [vec(x) for x in fd], tol=1e-7))
res['101'] = [td, rank(ob), rank(ob + [vec(R101)] + [vec(x) for x in fd], tol=1e-7)]
json.dump({'rank_tests': res, 'cand88': {'p': [pc.real, pc.imag], 'q': [qc.real, qc.imag], 'k': [kc.real, kc.imag], 'a': [ac.real, ac.imag], 'b': [bc.real, bc.imag], 'c': [cc.real, cc.imag]}}, open('s07_out.json', 'w'), indent=1)
