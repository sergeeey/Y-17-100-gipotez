"""(b) continuation, SERIAL re-run of continuation2.py (which used Pool(8); its outputs are treated as UNVERIFIED).
Base: Lienard form, T_L=-2, D_L=5, T_R=0.5, D_R=1, a_L=a_R=0.5 (1 cycle).  beta = x'-jump parameter (zone R b=(beta,-a_R)).
1D sweeps in a_L, a_R, beta (121 pts each) + 2D (a_L,beta) 25x25 grid, wall-bounded."""

import sys, json, time, numpy as np
from pwl import *

BASE = dict(TL=-2.0, DL=5.0, TR=0.5, DR=1.0, aL=0.5, aR=0.5, beta=0.0)
budget = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0
t0 = time.time()


def build(p):
    zR = Zone([[p["TR"], -1.0], [p["DR"], 0.0]], [p["beta"], -p["aR"]])
    zL = Zone([[p["TL"], -1.0], [p["DL"], 0.0]], [0.0, -p["aL"]])
    return zR, zL


def cnt(p):
    zR, zL = build(p)
    r = count_cycles(zR, zL, n=3000, dmin=1e-5, dmax=400.0)
    good = [x for x in r["roots"] if abs(x["res"]) < 1e-8 * (1 + abs(x["y0"]))]
    return len(good), r["n_sign_changes"] - len(good), r["ambiguous_gaps"]


out = {}
for fam, lo, hi, key in (("aL", -6, 6, "aL"), ("aR", -6, 6, "aR"), ("beta", -4, 4, "beta")):
    rows = []
    for v in np.linspace(lo, hi, 121):
        if time.time() - t0 > budget:
            break
        n, spur, amb = cnt(dict(BASE, **{key: float(v)}))
        rows.append((float(v), n, spur, amb))
    out[fam] = rows
    ns = np.array([r[1] for r in rows])
    print(
        fam,
        "n_pts",
        len(rows),
        "hist",
        np.bincount(ns).tolist(),
        "spurious",
        sum(r[2] for r in rows),
        "ambig",
        sum(r[3] for r in rows),
        flush=True,
    )
    prev = None
    for v, n, sp, am in rows:
        if n != prev:
            print(f"   {fam}={v:+.3f} -> n={n}", flush=True)
            prev = n
rows = []
for aL in np.linspace(-6, 6, 25):
    for beta in np.linspace(-4, 4, 25):
        if time.time() - t0 > budget:
            break
        n, spur, amb = cnt(dict(BASE, aL=float(aL), beta=float(beta)))
        rows.append((float(aL), float(beta), n, spur, amb))
out["aL_beta"] = rows
ns = np.array([r[2] for r in rows])
print(
    "aL_beta n_pts",
    len(rows),
    "hist",
    np.bincount(ns).tolist(),
    "spurious",
    sum(r[3] for r in rows),
    flush=True,
)
print("2-cycle points:", [(r[0], r[1]) for r in rows if r[2] >= 2], flush=True)
json.dump(out, open("continuation3.json", "w"))
print("wall", time.time() - t0)
