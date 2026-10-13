import json, numpy as np
from ybe import *
from analyze import sig_of
from classify3 import clean
rows = json.load(open('cls_w001.json')); d = np.load('d3_w001.npz', allow_pickle=True)
fam = hiet_families(np.random.default_rng(5)); fam['P'] = flip(2).astype(complex); fam['Id'] = np.eye(4, dtype=complex)
fsig = {nm: sig_of(R, 2)[0] for nm, R in fam.items()}
W = [0, 1, 3, 4]
def show(r):
    R = clean(d['R'][r['idx']])
    B0 = R[np.ix_(W, W)]
    print('--- candidate idx', r['idx'], 'seed', r['seed'], 'mode', r['mode'], 'res3=%.1e' % rel_res(R, 3), 'tangent', r['tangent'], 'dimL', r['dimL'])
    # block-diagonality in the charge-sum grading (0,0,1)
    mask = np.zeros((9, 9), bool)
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for e in range(3):
                    if (a == 2) + (b == 2) == (c == 2) + (e == 2): mask[a*3+b, c*3+e] = True
    print('  offblock max |R| = %.1e' % np.abs(R * ~mask).max())
    print('  B0 (W(x)W block) dim-2 YBE residual = %.2e, det=%.3e' % (rel_res(B0, 2), abs(np.linalg.det(B0))))
    s, iv = sig_of(B0 / abs(np.linalg.det(B0)) ** 0.25, 2)
    print('  B0 dim-2 signature', s)
    print('  matches Hietarinta families:', [nm for nm, f in fsig.items() if f == s])
    S1 = [2, 5, 6, 7]
    print('  eig(B1 charge-1 block)', np.round(np.linalg.eigvals(R[np.ix_(S1, S1)]), 4), ' R[8,8]=', np.round(R[8, 8], 4))
    print('  eig(B0)', np.round(np.linalg.eigvals(B0), 4))
for r in rows:
    if r['verdict'] == 'BEYOND-ACC-candidate': show(r)
# statistics over ALL w001 solutions: dim-2 signature of B0
import collections
c = collections.Counter()
for r in rows:
    R = clean(d['R'][r['idx']]); B0 = R[np.ix_(W, W)]
    s, _ = sig_of(B0 / abs(np.linalg.det(B0)) ** 0.25, 2)
    c[tuple(nm for nm, f in fsig.items() if f == s) or ('unmatched' + str(s),)] += 1
print('B0 -> Hietarinta-family match over all', len(rows), 'w001 solutions:'); [print(' ', v, k) for k, v in c.most_common()]
