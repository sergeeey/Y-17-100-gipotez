raise SystemExit("DISABLED (hardware rule 7a): uses multiprocessing.Pool. Use run_serial.py or pos3.py instead.")
"""Chunked parallel random-start search (resume-safe): python run_search2.py N nstarts seed0 maxit outprefix modes nproc
Saves outprefix_chunkK.npz after every chunk of 200 starts (the first attempt lost everything to a pool crash)."""

import os, sys, time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from multiprocessing import Pool
from solver import one_start

if __name__ == "__main__":
    N = int(sys.argv[1])
    ns = int(sys.argv[2])
    seed0 = int(sys.argv[3])
    maxit = int(sys.argv[4])
    pref = sys.argv[5]
    modes = sys.argv[6].split(",")
    nproc = int(sys.argv[7])
    jobs = [(N, seed0 + s, modes[s % len(modes)], maxit) for s in range(ns)]
    CH = 200
    t = time.time()
    for c in range(0, ns, CH):
        fn = "%s_chunk%d.npz" % (pref, c // CH)
        if os.path.exists(fn):
            continue
        with Pool(nproc) as p:
            res = p.map(one_start, jobs[c : c + CH], chunksize=1)
        ok = [r for r in res if r["ok"]]
        np.savez(
            fn,
            R=np.array([r["R"] for r in ok]),
            seed=np.array([r["seed"] for r in ok]),
            mode=np.array([r["mode"] for r in ok]),
            f=np.array([r["f"] for r in ok]),
            sminR=np.array([r["sminR"] for r in ok]),
            allmode=np.array([r["mode"] for r in res]),
            allok=np.array([r["ok"] for r in res]),
        )
        print(
            "chunk",
            c // CH,
            "starts",
            len(res),
            "ok",
            len(ok),
            "elapsed %.0fs" % (time.time() - t),
            flush=True,
        )
    print("DONE", flush=True)
