import sys, collections
import numpy as np
from ybe import *
from analyze import sig_of

def spec_ratios(R, N):
    Rn = R / abs(np.linalg.det(R)) ** (1.0 / (N * N))
    ev = np.linalg.eigvals(Rn)
    groups = cluster_eigs(ev, 1e-5)
    groups.sort(key=lambda g: -len(g))
    lam0 = np.mean(groups[0])
    # eigenvalue ratios relative to the most degenerate eigenvalue, as (mult, ratio) pairs ordered by mult then |phase|
    return [(len(g), np.mean(g) / lam0) for g in groups]

def is_monomial(R, tol=1e-8):
    # generalized permutation matrix: one nonzero per row & column
    A = np.abs(R) > tol * np.abs(R).max()
    return A.sum(0).max() == 1 and A.sum(1).max() == 1

if __name__ == '__main__':
    N = 3
    files = sys.argv[1:]
    groups = collections.defaultdict(list)
    nfilt = 0; ntot = 0
    for f in files:
        d = np.load(f)
        for i, R in enumerate(d['R']):
            ntot += 1
            if rel_res(R, N) > 1e-10: continue
            sv = np.linalg.svd(R, compute_uv=False)
            if sv[0] / sv[-1] > 1e6 or np.abs(R).max() > 1e4:
                nfilt += 1; continue
            s, iv = sig_of(R, N)
            groups[s].append((f, i, R))
    print('total converged', ntot, 'filtered ill-conditioned', nfilt, 'signatures', len(groups))
    print('signature = (spec[(alg,geom)], dimL, cc-class, tangent, moduli, rank)')
    for s, v in sorted(groups.items(), key=lambda t: -len(t[1])):
        rat = [spec_ratios(R, N) for _, _, R in v]
        mono = sum(is_monomial(R) for _, _, R in v)
        # spectrum ratios: report first element's, and spread of the 2nd-eigenvalue ratio across group
        first = [(m, np.round(r, 4)) for m, r in rat[0]]
        spread = None
        if len(rat[0]) > 1 and all(len(r) == len(rat[0]) for r in rat):
            spread = float(np.max([abs(r[1][1] - rat[0][1][1]) for r in rat]))
        print('%4d  %s\n       first spectrum (mult, ratio): %s | monomial: %d | 2nd-ratio spread: %s' % (len(v), s, first, mono, spread))
