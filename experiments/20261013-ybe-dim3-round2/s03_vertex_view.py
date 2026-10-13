import sys, numpy as np
R1 = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-ybe-dim3-beyond-acc"
sys.path.insert(0, R1)
from ybe import braid_residual, flip
np.set_printoptions(precision=5, suppress=True, linewidth=220)
d = np.load(R1 + '/d3_w001.npz', allow_pickle=True)
P = flip(3)
W = [0, 1, 3, 4]; S1 = [2, 5, 6, 7]
def L2(B):
    cols = []
    for k in range(4):
        h = np.zeros((2, 2)); h[k//2, k%2] = 1
        D = np.kron(h, np.eye(2)) + np.kron(np.eye(2), h)
        cols.append((B@D - D@B).reshape(-1))
    u, s, vh = np.linalg.svd(np.array(cols).T)
    return [vh[i].conj().reshape(2, 2) for i in range(4) if s[i] < 1e-9]
for idx in (101, 88):
    R = d['R'][idx].copy(); R[abs(R) < 1e-13] = 0
    if idx == 101:
        Ls = L2(R[np.ix_(W, W)]); h = max([h - np.trace(h)/2*np.eye(2) for h in Ls], key=np.linalg.norm)
        ev, V = np.linalg.eig(h); g2 = V
    else:
        g2 = np.eye(2)
    g = np.eye(3, dtype=complex); g[:2, :2] = g2; G = np.kron(g, g)
    Rn = np.linalg.inv(G) @ R @ G
    Rv = P @ Rn
    print('=== idx', idx, ' vertex-form blocks')
    print(' V0xV0 block of Rv\n', Rv[np.ix_(W, W)])
    print(' charge-1 block of Rv (|02>,|12>,|20>,|21>)\n', Rv[np.ix_(S1, S1)])
    print(' Rv[8,8]', Rv[8, 8])
    print(' nonzeros in charge-1 vertex block:', int((np.abs(Rv[np.ix_(S1, S1)]) > 1e-9).sum()))
