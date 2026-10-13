import sys, collections
import numpy as np
from ybe import *

def sig_of(R, N):
    iv = invariants(R, N)
    return (tuple(iv['spec']), iv['dimL'], iv['cc'], iv['tangent'], iv['moduli'], iv['rank']), iv

if __name__ == '__main__':
    N = int(sys.argv[1]); f = sys.argv[2]
    d = np.load(f)
    groups = collections.defaultdict(list)
    nfilt = 0
    for i, R in enumerate(d['R']):
        if rel_res(R, N) > 1e-10: continue
        sv = np.linalg.svd(R, compute_uv=False)
        if sv[0] / sv[-1] > 1e6 or np.abs(R).max() > 1e4:
            nfilt += 1; continue
        s, iv = sig_of(R, N)
        groups[s].append((i, iv))
    print('filtered ill-conditioned (cond>1e6 or |R|>1e4):', nfilt)
    print('converged solutions:', len(d['R']), ' distinct signatures:', len(groups))
    print('signature = (spec[(alg,geom)...], dimL, cc-class, tangent, moduli, rank)')
    for s, v in sorted(groups.items(), key=lambda t: -len(t[1])):
        print(len(v), s)
