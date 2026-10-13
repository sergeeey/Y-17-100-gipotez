"""For every signature group that is NOT ACC/SCC-equivalent (cc != 'distinct'), report spectrum, rigidity (moduli), monomial test,
span{I,P,P^2} (Gaussian-type) test and one-step DS-move partners (does a DS move reach a charge-conserving solution?)."""
import os, sys, collections
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np
from multiprocessing import Pool
from ybe import *
from analyze import sig_of
from analyze3 import spec_ratios, is_monomial
from ds_check import ds_moves

def gaussian_span_dist(R):
    """distance of R (up to local conjugation it need not be in this form, but test the plain Pauli form) -- diagnostic only."""
    w3 = np.exp(2j*np.pi/3); Xm = np.roll(np.eye(3), 1, axis=0); Zm = np.diag([w3**j for j in range(3)])
    PS = np.kron(Xm, Zm)
    B = np.array([np.eye(9).ravel(), PS.ravel(), (PS @ PS).ravel()]).T
    c, *_ = np.linalg.lstsq(B, R.ravel(), rcond=None)
    return np.linalg.norm(B @ c - R.ravel()) / np.linalg.norm(R)

def work(R):
    Ts, out = ds_moves(R, 3, 30)
    return [(cc['dimL'], cc['label'], res) for T, RT, res, cc in out]

if __name__ == '__main__':
    files = sys.argv[1:]
    N = 3
    groups = collections.defaultdict(list)
    for f in files:
        d = np.load(f)
        for i, R in enumerate(d['R']):
            if rel_res(R, N) > 1e-10: continue
            sv = np.linalg.svd(R, compute_uv=False)
            if sv[0] / sv[-1] > 1e6 or np.abs(R).max() > 1e4: continue
            s, iv = sig_of(R, N)
            groups[s].append(R)
    sel = [(s, v) for s, v in groups.items() if s[2] != 'distinct']
    print('groups total %d; non-ACC-equivalent (U1-free or degenerate) groups: %d' % (len(groups), len(sel)))
    reps = []
    for s, v in sorted(sel, key=lambda t: -len(t[1])):
        for R in v[:2]:
            reps.append((s, R))
    with Pool(12) as p:
        res = p.map(work, [R for _, R in reps])
    seen = set()
    for (s, R), r in zip(reps, res):
        rat = [(m, np.round(x, 4)) for m, x in spec_ratios(R, N)]
        print('\nGROUP n=%d sig=%s' % (len(groups[s]), s))
        print('   spectrum (mult, ratio to most-degenerate eigenvalue): %s' % rat)
        print('   monomial: %s | dist to span{I,P,P^2}(Pauli): %.2e' % (is_monomial(R), gaussian_span_dist(R)))
        labs = collections.Counter((a, b) for a, b, _ in r)
        print('   one-step DS partners (non-scalar T): %d ; their (dimL, cc) = %s' % (len(r), dict(labs)))
