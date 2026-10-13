import sys, numpy as np
R1 = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-ybe-dim3-beyond-acc"
sys.path.insert(0, R1)
from ybe import ybe_residual_R, flip
d = np.load(R1 + '/d3_w001.npz', allow_pickle=True); P = flip(3)
for idx in (88, 101):
    R = d['R'][idx]; Rv = P @ R
    print(idx, 'vertex residual of P*R_braid (R12R13R23=R23R13R12):', np.linalg.norm(ybe_residual_R(Rv, 3))/np.linalg.norm(Rv)**3)
# colex-triangularity test (Hietarinta 1993 definition): R^{kl}_{ij}=0 if j>l or (j=l and i>k). R_v|ij> = sum R^{kl}_{ij}|kl>, index 3i+j
def triangular_defect(Rv, perm):
    # perm: relabeling of the 3 states (basis ordering); returns max |entry| violating the pattern
    Q = np.zeros((3, 3)); 
    for a, b in enumerate(perm): Q[b, a] = 1
    G = np.kron(Q, Q); M = np.linalg.inv(G) @ Rv @ G
    bad = 0.0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if j > l or (j == l and i > k): bad = max(bad, abs(M[3*k+l, 3*i+j]))
    return bad
import itertools
# gauge from s04/s06: g2 (+) 1 ; evaluate in the product basis (0,1,e) with all orderings, for Rv, Rv^T, P Rv P
def gauge101():
    W = [0, 1, 3, 4]
    R = d['R'][101].copy(); B0 = R[np.ix_(W, W)]
    cols = []
    for k in range(4):
        h = np.zeros((2, 2)); h[k//2, k%2] = 1
        D = np.kron(h, np.eye(2)) + np.kron(np.eye(2), h)
        cols.append((B0@D - D@B0).reshape(-1))
    u, s, vh = np.linalg.svd(np.array(cols).T)
    Ls = [vh[i].conj().reshape(2, 2) for i in range(4) if s[i] < 1e-9]
    h = max([x - np.trace(x)/2*np.eye(2) for x in Ls], key=np.linalg.norm)
    ev, V = np.linalg.eig(h)
    g = np.eye(3, dtype=complex); g[:2, :2] = V; G = np.kron(g, g)
    return np.linalg.inv(G) @ R @ G
Rn = gauge101(); Rv = P @ Rn
best = min((triangular_defect(M, perm), name, perm) for M, name in ((Rv, 'Rv'), (Rv.T, 'Rv^T'), (P @ Rv @ P, 'PRvP'), (P @ Rv.T @ P, 'P Rv^T P')) for perm in itertools.permutations(range(3)))
print('101 in gauge (g2+1): smallest colex-triangularity defect over 6 orderings x 4 symmetries =', best, ' (scale of entries ~1)')
