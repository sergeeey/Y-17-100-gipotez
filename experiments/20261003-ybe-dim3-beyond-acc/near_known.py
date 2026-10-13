raise SystemExit("DISABLED (hardware rule 7a): uses multiprocessing.Pool. Use run_serial.py or pos3.py instead.")
"""Positive control for the SOLVER: start from noisy copies of known solutions; it must converge to a solution with the same
conjugation-invariant signature (dim 2: Hietarinta families; dim 3: Table-1 families of 2310.03816)."""
import os, sys
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from multiprocessing import Pool
from ybe import *
from solver import lm_solve
from analyze import sig_of

def job(a):
    N, name, _, seed, noise = a
    rng = np.random.default_rng(seed)
    R = (hiet_families if N == 2 else table1_families)(np.random.default_rng(seed + 777))[name]
    K2 = N*N
    R = R / abs(np.linalg.det(R))**(1.0/K2)
    sig0, _ = sig_of(R, N)
    R0 = R + noise*(rng.normal(size=R.shape)+1j*rng.normal(size=R.shape))/np.sqrt(2)
    w = rng.normal(size=R.shape)+1j*rng.normal(size=R.shape)
    R0 = R0/np.sum(w*R0)
    Rf, f, it = lm_solve(R0, N, w, maxit=300)
    if Rf is None or f > 1e-10:
        return (name, seed, sig0, None, f)
    s1, _ = sig_of(Rf, N)
    return (name, seed, sig0, s1, f)

if __name__ == '__main__':
    N = int(sys.argv[1]); ntr = int(sys.argv[2]); noise = float(sys.argv[3])
    rng = np.random.default_rng(99)
    fam = hiet_families(rng) if N == 2 else table1_families(rng)
    jobs = [(N, nm, R, 1000*i+t, noise) for i,(nm,R) in enumerate(fam.items()) for t in range(ntr)]
    with Pool(6) as p: out = p.map(job, jobs)
    import collections
    agg = collections.defaultdict(lambda: [0,0,0])
    for nm, seed, s0, s1, f in out:
        a = agg[nm]; a[0]+=1
        if s1 is None: a[2]+=1
        elif s1 == s0: a[1]+=1
    print('N=%d noise=%.2f trials/family=%d' % (N, noise, ntr))
    for nm,(n,same,fail) in agg.items():
        print('  %-26s n=%d same-signature=%d no-convergence=%d other=%d' % (nm, n, same, fail, n-same-fail))
