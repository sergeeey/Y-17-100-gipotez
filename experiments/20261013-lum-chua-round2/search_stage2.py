"""Stage 2: structured search around the three published 3-cycle systems (HY, FPTT21, GRS) in the Lienard canonical form.
Random directions d in 7-D parameter space; p(t) = p0*(1+t*d), t log-spaced 1e-4..0.5 (both signs).  k(t) and Delta(t) of
the paper's criterion are computed everywhere (cheap); cycles are counted at every step with k>=2 (capped per direction)
and at every 20th step otherwise.  Usage: search_stage2.py <seed> <seeds:HY,FPTT,GRS> <n_dir> <budget_s>"""

import json
import sys
import time

import numpy as np

from controls_def import FPTT_CANON, GRS_CANON, HY_CANON
from lc2_core import canon_zones, count_cycles2
from lc2_theory import delta_b, k_negative_roots

seed, which, n_dir, budget = (
    int(sys.argv[1]),
    sys.argv[2].split(","),
    int(sys.argv[3]),
    float(sys.argv[4]),
)
rng = np.random.default_rng(seed)
SEEDS = {"HY": HY_CANON, "FPTT": FPTT_CANON, "GRS": GRS_CANON}
KEYS = ("TL", "DL", "aL", "TR", "DR", "aR", "b")
t0 = time.time()
rows = []
best = {}
khist = {}
nth = 0


def valid(p):
    TL, DL, aL, TR, DR, aR, b = p
    return DL > 0 and DR > 0 and 4 * DL - TL**2 > 0 and 4 * DR - TR**2 > 0 and aL * aR * b != 0


for di in range(n_dir):
    for name in which:
        if time.time() - t0 > budget:
            break
        p0 = np.array([float(SEEDS[name][k]) for k in KEYS])
        d = rng.normal(size=7)
        d[1] = 0.0 if rng.random() < 0.0 else d[1]
        ts = np.concatenate([10 ** np.linspace(-4, np.log10(0.5), 60)])
        n_k2_counted = 0
        for sgn in (+1, -1):
            for j, t in enumerate(ts):
                if time.time() - t0 > budget:
                    break
                p = p0 * (1 + sgn * t * d)
                if not valid(p):
                    continue
                k, info = k_negative_roots(tuple(p))
                if k is None or not isinstance(info, dict):
                    continue
                khist[k] = khist.get(k, 0) + 1
                dl = delta_b(*p)
                do_count = (k >= 2 and n_k2_counted < 12) or (j % 20 == 0)
                if not do_count:
                    continue
                if k >= 2:
                    n_k2_counted += 1
                zR, zL = canon_zones(*p)
                r = count_cycles2(zR, zL, n=2500, dmax=1e4, noise_rel=2.0e-14)
                if r["count"] is None:
                    continue
                nth += 1
                rec = dict(
                    seed=name,
                    dir=di,
                    sgn=sgn,
                    t=float(t),
                    k=k,
                    deg=info["deg"],
                    delta=float(dl),
                    count=r["count"],
                    hidden=len(r["hidden_pairs"]),
                    p=[float(v) for v in p],
                )
                rows.append(rec)
                key = (name, k)
                best[key] = max(best.get(key, 0), r["count"])
                if r["count"] >= 4 or (info["deg"] == 6 and r["count"] > k + 2):
                    print("!!! CANDIDATE/VIOLATION", rec, flush=True)
    if time.time() - t0 > budget:
        break
    if di % 5 == 0:
        print(
            "dir",
            di,
            "counted",
            nth,
            "elapsed",
            round(time.time() - t0),
            "best(seed,k)->count",
            {str(k): v for k, v in best.items()},
            flush=True,
        )
        json.dump(
            dict(rows=rows, best={str(k): v for k, v in best.items()}, khist=khist),
            open(f"search_stage2_seed{seed}.json", "w"),
        )
json.dump(
    dict(rows=rows, best={str(k): v for k, v in best.items()}, khist=khist),
    open(f"search_stage2_seed{seed}.json", "w"),
)
hist = {}
for r in rows:
    hist[(r["seed"], r["k"], r["count"])] = hist.get((r["seed"], r["k"], r["count"]), 0) + 1
print("hist (seed,k,count):n", {str(k): v for k, v in sorted(hist.items())}, flush=True)
print("k hist along all lines", khist, flush=True)
print(
    "max count",
    max((r["count"] for r in rows), default=None),
    "n counted",
    nth,
    "elapsed",
    round(time.time() - t0),
    flush=True,
)
print(
    "Thm6 violations:",
    sum(1 for r in rows if r["deg"] == 6 and r["count"] > r["k"] + 2),
    flush=True,
)
