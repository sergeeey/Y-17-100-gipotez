raise SystemExit("DISABLED (hardware rule 7a): uses multiprocessing.Pool. Use run_serial.py or pos3.py instead.")
"""Parallel random-start search. usage: python run_search.py N nstarts seed0 maxit out.npz [modes]"""
import os, sys, time
os.environ.setdefault('OMP_NUM_THREADS', '1'); os.environ.setdefault('MKL_NUM_THREADS', '1'); os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import numpy as np
from multiprocessing import Pool
from solver import one_start

if __name__ == '__main__':
    N = int(sys.argv[1]); ns = int(sys.argv[2]); seed0 = int(sys.argv[3]); maxit = int(sys.argv[4]); out = sys.argv[5]
    modes = sys.argv[6].split(',') if len(sys.argv) > 6 else ['gauss', 'near_id', 'near_flip', 'real']
    jobs = [(N, seed0 + s, modes[s % len(modes)], maxit) for s in range(ns)]
    t = time.time()
    res = []
    with Pool(20) as p:
        for i, o in enumerate(p.imap_unordered(one_start, jobs, chunksize=2)):
            res.append(o)
            if (i + 1) % 50 == 0:
                print('done', i + 1, 'ok', sum(r['ok'] for r in res), 'elapsed %.0fs' % (time.time() - t), flush=True)
    ok = [r for r in res if r['ok']]
    print('N=%d starts=%d converged=%d time=%.0fs' % (N, ns, len(ok), time.time() - t), flush=True)
    for m in modes:
        sub = [r for r in res if r['mode'] == m]
        print('  mode %-9s starts %d ok %d' % (m, len(sub), sum(r['ok'] for r in sub)), flush=True)
    np.savez(out, R=np.array([r['R'] for r in ok]), seed=np.array([r['seed'] for r in ok]), mode=np.array([r['mode'] for r in ok]),
             f=np.array([r['f'] for r in ok]), sminR=np.array([r['sminR'] for r in ok]))
