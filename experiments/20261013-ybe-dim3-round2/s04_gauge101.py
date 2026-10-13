import sys, numpy as np
R1 = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-ybe-dim3-beyond-acc"
sys.path.insert(0, R1)
from ybe import braid_residual, flip
np.set_printoptions(precision=6, suppress=True, linewidth=220)
d = np.load(R1 + '/d3_w001.npz', allow_pickle=True)
W = [0, 1, 3, 4]; S1 = [2, 5, 6, 7]
R = d['R'][101].copy(); R[abs(R) < 1e-13] = 0
B0 = R[np.ix_(W, W)]
cols = []
for k in range(4):
    h = np.zeros((2, 2)); h[k//2, k%2] = 1
    D = np.kron(h, np.eye(2)) + np.kron(np.eye(2), h)
    cols.append((B0@D - D@B0).reshape(-1))
u, s, vh = np.linalg.svd(np.array(cols).T)
Ls = [vh[i].conj().reshape(2, 2) for i in range(4) if s[i] < 1e-9]
h = max([x - np.trace(x)/2*np.eye(2) for x in Ls], key=np.linalg.norm)
ev, V = np.linalg.eig(h)
lam = R[0, 0] if False else None
def build(V, sc):
    g = np.eye(3, dtype=complex); g[:2, :2] = V @ np.diag(sc); G = np.kron(g, g)
    return np.linalg.inv(G) @ R @ G
# find which eigenvector ordering gives Rn[|01>,|10>] pattern with lambda on |00>: use order giving B0[1,2]!=0 as (01<-10)
for order in ([0, 1], [1, 0]):
    Vo = V[:, order]
    Rn = build(Vo, np.ones(2))
    B = Rn[np.ix_(W, W)]
    print('order', order, 'B0[1,2]=', B[1, 2], 'B0[2,1]=', B[2, 1], 'B0[1,1]', B[1,1], 'B0[2,2]', B[2,2])
# choose order where B0 = [[lam,0,0,0],[0,0,a,0],[0,b,e,0],[0,0,0,lam]] (round-1 first print: B0[1,2]=a, B0[2,1]=lam')
Vo = V[:, [0, 1]]
Rn0 = build(Vo, np.ones(2)); B = Rn0[np.ix_(W, W)]
lam = B[0, 0]; a = B[1, 2]; b = B[2, 1]; e = B[2, 2]
print('lam', lam, 'a', a, 'b', b, 'e', e, ' eigenvalue mu_b = e - lam? ->', e - lam, ' check -mu: ', -a*b/lam)
# rescale so that a = b (symmetric gauge): conj with diag(s,t): a -> a*(t/s)^2 ? determine numerically
# try sc=(1,x): find x with new a == new b
for x in np.linspace(0.2, 5, 7):
    pass
# analytic: conj by g=diag(1,x): |01> weight x, |10> weight x -> equal; but Rn entries: B[1,2] maps |10>(idx2)->|01>(idx1)? both have weight x. so no change. try generic V columns scaling instead:
# the true residual gauge is the scaling of the basis vectors of V0 in the eigenbasis of h: sc=(s0,s1) acts on |01>,|10> equally => a,b unchanged. So a,b are gauge-invariant here:
print('a*b/lam^2=', a*b/lam**2, ' a/lam=', a/lam, ' b/lam=', b/lam)
# charge-1 block in this gauge, divided by lam
Rn = Rn0
print('B1/lam:\n', Rn[np.ix_(S1, S1)]/lam)
print('R88/lam', Rn[8, 8]/lam)
# invariants for scaling of e: conj diag(1,1,u): affects entries of B1? compute the effect numerically
for u in (2.0, 3.0):
    g = np.diag([1, 1, u]).astype(complex); G = np.kron(g, g)
    Rm = np.linalg.inv(G) @ Rn @ G
    print('u', u, 'max change in B1', np.abs(Rm[np.ix_(S1, S1)] - Rn[np.ix_(S1, S1)]).max())
