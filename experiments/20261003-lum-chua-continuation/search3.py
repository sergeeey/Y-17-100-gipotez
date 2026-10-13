"""(d) structured search near the Huan-Yang / Llibre-Ponce 3-cycle mechanism -- SERIAL, wall-time bounded.
Replaces search.py / search2.py (which used multiprocessing.Pool, forbidden by the hardware rule).

usage:  lowprio.py search3.py phase1 <sigma> <N> <seed> <budget_s>
        lowprio.py search3.py es     <sigma0> <iters> <seed> <budget_s> [start=HY|best]
        lowprio.py search3.py rand   <N> <seed> <budget_s>
Every call appends one line to search3_runs.jsonl; any count>=4 is appended to found4.jsonl.
"""

import sys, json, time, numpy as np
from pwl import *
from search import P0, zones, evaluate, perturb

t0 = time.time()
mode = sys.argv[1]


def log(rec):
    rec["mode"] = mode
    rec["argv"] = sys.argv[2:]
    rec["wall_s"] = round(time.time() - t0, 1)
    with open("search3_runs.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)


def found(c, p, tag):
    with open("found4.jsonl", "a") as f:
        f.write(json.dumps(dict(count=int(c), params=[float(x) for x in p], tag=tag)) + "\n")
    print("FOUND>=4", c, tag, flush=True)


if mode == "phase1":
    sigma, N, seed, budget = (
        float(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
        float(sys.argv[5]),
    )
    rng = np.random.default_rng(seed)
    cs = []
    for i in range(N):
        if time.time() - t0 > budget:
            break
        q = perturb(rng, P0, sigma)
        c, _ = evaluate(q, with_score=False)
        cs.append(c)
        if c >= 4:
            found(c, q, f"phase1 sigma={sigma}")
    cs = np.array(cs)
    log(
        dict(
            sigma=sigma,
            n_done=len(cs),
            invalid=int((cs < 0).sum()),
            hist=np.bincount(cs[cs >= 0], minlength=6).tolist(),
            max=int(cs.max()),
        )
    )

elif mode == "es":
    sigma0, iters, seed, budget = (
        float(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
        float(sys.argv[5]),
    )
    r = np.random.default_rng(seed)
    cur = P0.copy()
    cc, cs_ = evaluate(cur)
    sig = sigma0
    it = 0
    best_seen = cc
    for it in range(iters):
        if time.time() - t0 > budget:
            break
        cand = [perturb(r, cur, sig) for _ in range(16)]
        res = [evaluate(c) for c in cand]
        for c, (k, _) in zip(cand, res):
            best_seen = max(best_seen, k)
            if k >= 4:
                found(k, c, f"es seed={seed}")
        bi = sorted(range(len(cand)), key=lambda i: (-res[i][0], res[i][1]))[0]
        if (res[bi][0], -res[bi][1]) > (cc, -cs_):
            cur, (cc, cs_) = cand[bi], res[bi]
            sig = min(sig * 1.2, 0.3)
        else:
            sig = max(sig * 0.85, 1e-4)
    log(
        dict(
            sigma0=sigma0,
            iters_done=it + 1,
            final_count=cc,
            final_score=cs_,
            best_seen=int(best_seen),
            final_sigma=sig,
            params=[float(x) for x in cur],
        )
    )

elif mode == "rand":
    N, seed, budget = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    rng = np.random.default_rng(seed)
    cs = []
    nv = 0
    while len(cs) < N and time.time() - t0 < budget:
        # general focus-focus system, line x=0, equilibria e_R,e_L anywhere in [-3,3]^2
        p = np.concatenate([rng.normal(size=8) * 1.5, rng.uniform(-3, 3, 4)])
        c, _ = evaluate(p, with_score=False)
        if c < 0:
            nv += 1
            continue
        cs.append(c)
        if c >= 4:
            found(c, p, "rand")
    cs = np.array(cs)
    log(
        dict(
            n_valid=len(cs),
            n_invalid_skipped=nv,
            hist=np.bincount(cs, minlength=6).tolist(),
            max=int(cs.max()),
        )
    )
