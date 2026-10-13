"""(b) continuation from the known 1-cycle continuous Lienard example.
Base: T_L=-2, D_L=5, T_R=0.5, D_R=1, a_L=a_R=0.5 (1 cycle at L-entry y=2.8877).
Family 1 (x'-continuous, Round-1 class):   a_L varies, a_R fixed (and a_R varies, a_L fixed).
Family 2 (general discontinuous): add x'-jump  beta:  zone R has b=(beta,-a_R), zone L b=(0,-a_L).
Counts #simple sign changes of G (crossing cycles), n=3000 grid, y-range log from fold."""
import sys, json, time, numpy as np
from multiprocessing import Pool
from pwl import *

BASE = dict(TL=-2.0, DL=5.0, TR=0.5, DR=1.0, aL=0.5, aR=0.5, beta=0.0)

def build(p):
    zR = Zone([[p["TR"], -1.0], [p["DR"], 0.0]], [p["beta"], -p["aR"]])
    zL = Zone([[p["TL"], -1.0], [p["DL"], 0.0]], [0.0, -p["aL"]])
    return zR, zL

def cnt(p):
    zR, zL = build(p)
    r = count_cycles(zR, zL, n=3000, dmin=1e-5, dmax=400.0)
    good = [x for x in r["roots"] if abs(x["res"]) < 1e-8 * (1 + abs(x["y0"]))]
    return len(good), r["ambiguous_gaps"] + (r["n_sign_changes"] - len(good)) * 1000, [x["y1"] for x in good]

def job(args):
    key, p = args
    return key, cnt(p)

if __name__ == "__main__":
    jobs = []
    # 1D sweeps
    for aL in np.linspace(-6, 6, 121):
        jobs.append((("aL", float(aL)), dict(BASE, aL=float(aL))))
    for aR in np.linspace(-6, 6, 121):
        jobs.append((("aR", float(aR)), dict(BASE, aR=float(aR))))
    for beta in np.linspace(-4, 4, 121):
        jobs.append((("beta", float(beta)), dict(BASE, beta=float(beta))))
    # 2D: (aL, beta) at aR=0.5 and (aL,aR)
    for aL in np.linspace(-6, 6, 33):
        for beta in np.linspace(-4, 4, 33):
            jobs.append((("aL_beta", float(aL), float(beta)), dict(BASE, aL=float(aL), beta=float(beta))))
    for aL in np.linspace(-6, 6, 33):
        for aR in np.linspace(-6, 6, 33):
            jobs.append((("aL_aR", float(aL), float(aR)), dict(BASE, aL=float(aL), aR=float(aR))))
    t = time.time()
    with Pool(8) as pool:
        res = pool.map(job, jobs, chunksize=8)
    print("time", time.time() - t, "jobs", len(jobs), flush=True)
    out = {}
    for key, (n, amb, ys) in res:
        out.setdefault(key[0], []).append((list(key[1:]), n, amb, ys))
    json.dump(out, open("continuation2.json", "w"))
    for fam, rows in out.items():
        ns = np.array([r[1] for r in rows])
        print(fam, "count histogram", np.bincount(ns), "max", ns.max(), "ambig", sum(r[2] for r in rows), flush=True)
    # 1D tracks: print transitions
    for fam in ("aL", "aR", "beta"):
        rows = out[fam]
        prev = None
        print("--", fam, "transitions in sign-change count:")
        for key, n, amb, ys in rows:
            if n != prev:
                print(f"   {fam}={key[0]:+.3f} -> n={n}  y1={['%.4f'%y for y in ys]}")
                prev = n
