import sys, numpy as np
R1 = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-ybe-dim3-beyond-acc"
sys.path.insert(0, R1)
from ybe import braid_residual, flip
np.set_printoptions(precision=5, suppress=True, linewidth=200)
d = np.load(R1 + '/d3_w001.npz', allow_pickle=True)
W = [0, 1, 3, 4]; S1 = [2, 5, 6, 7]
def L2(B):
    cols = []
    for k in range(4):
        h = np.zeros((2, 2)); h[k//2, k%2] = 1
        D = np.kron(h, np.eye(2)) + np.kron(np.eye(2), h)
        cols.append((B@D - D@B).reshape(-1))
    u, s, vh = np.linalg.svd(np.array(cols).T)
    return [vh[i].conj().reshape(2, 2) for i in range(4) if s[i] < 1e-9], s
for idx in (101, 88):
    R = d['R'][idx].copy(); R[abs(R) < 1e-13] = 0
    B0 = R[np.ix_(W, W)]
    Ls, s = L2(B0)
    print('=== idx', idx, 'dim L2(B0)=', len(Ls), 'sv', s)
    # nonscalar h in L2: remove identity component
    hs = [h - np.trace(h)/2*np.eye(2) for h in Ls]
    h = max(hs, key=lambda m: np.linalg.norm(m))
    ev, V = np.linalg.eig(h); print(' eig h', ev)
    g2 = V
    for order in (g2, g2[:, ::-1]):
        g = np.zeros((3, 3), complex); g[:2, :2] = order; g[2, 2] = 1
        G = np.kron(g, g); Rn = np.linalg.inv(G) @ R @ G
        print(' B0 in new basis:\n', Rn[np.ix_(W, W)])
        print(' B1 (|02>,|12>,|20>,|21>):\n', Rn[np.ix_(S1, S1)])
        print(' R88=', Rn[8, 8], ' offblock max', np.abs(Rn[np.ix_(W, S1)]).max(), np.abs(Rn[np.ix_(W, [8])]).max(), np.abs(Rn[np.ix_(S1, [8])]).max())
