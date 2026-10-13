"""Serial random-start search (NO multiprocessing). usage (via scripts/lowprio.py):
  run_serial.py <tag> <mask-name> <nstarts> <seed0> <maxit> <modes comma> <time_limit_s>
mask-name in: full | w001 (charge q=(0,0,1) in Z) | z3 (q=(0,1,2) mod 3) | acc (q=(0,1,2) in Z) | z2 (q=(0,0,1) mod 2) | scc (q=(0,1,3) in Z)
Saves <tag>.npz at the end and every 40 starts."""
import sys, os, time, collections
import numpy as np
from solver_mask import *

MASKS = {
    "full": lambda: np.ones((9, 9), bool),
    "w001": lambda: grading_mask((0, 0, 1)),
    "z3": lambda: grading_mask((0, 1, 2), 3),
    "acc": lambda: grading_mask((0, 1, 2)),
    "z2": lambda: grading_mask((0, 0, 1), 2),
    "scc": lambda: grading_mask((0, 1, 3)),
}

if __name__ == "__main__":
    tag, mname, ns, seed0, maxit, modes, tl = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6].split(","), float(sys.argv[7])
    mask = MASKS[mname]()
    idx = np.flatnonzero(mask.reshape(-1))
    print("mask", mname, "free entries", len(idx), flush=True)
    t0 = time.time()
    Rs, seeds, mds = [], [], []
    reasons = collections.Counter()
    done = 0
    for s in range(ns):
        if time.time() - t0 > tl:
            print("time limit reached", flush=True)
            break
        mode = modes[s % len(modes)]
        rng = np.random.default_rng(seed0 + s)
        R0 = random_det_start(mask, rng, mode)
        R, f, it, why = lm_det(R0, idx, maxit=maxit, abort=not os.environ.get("NOABORT"))
        done += 1
        reasons[(mode, why)] += 1
        if why == "ok":
            Rs.append(R); seeds.append(seed0 + s); mds.append(mode)
        if (s + 1) % 20 == 0:
            print("starts", s + 1, "ok", len(Rs), "elapsed %.0fs" % (time.time() - t0), flush=True)
            np.savez(tag + ".npz", R=np.array(Rs), seed=np.array(seeds), mode=np.array(mds), mask=mname)
    np.savez(tag + ".npz", R=np.array(Rs), seed=np.array(seeds), mode=np.array(mds), mask=mname)
    print("DONE starts", done, "ok", len(Rs), "elapsed %.0fs" % (time.time() - t0))
    for k, v in sorted(reasons.items()):
        print("  ", k, v)
