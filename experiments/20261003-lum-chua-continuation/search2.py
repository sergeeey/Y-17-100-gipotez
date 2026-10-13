"""(d) structured search near the HY 3-cycle mechanism, v2 (restart-safe, per-stage json, flush logs).
Uses search.evaluate (count of simple sign changes of G, n=2500 grid, y range from fold) +
near-event score.  Any candidate with count>=4 is dumped to found4.json for independent verification."""
import json, time, sys, numpy as np
from multiprocessing import Pool
from search import P0, evaluate, perturb

def job(p): return evaluate(np.array(p))

def es(args):
    start, iters, sigma0, seed = args
    r = np.random.default_rng(seed)
    cur = np.array(start); cc, cs_ = evaluate(cur)
    sig = sigma0; best4 = None
    for it in range(iters):
        cand = [perturb(r, cur, sig) for _ in range(20)]
        res = [evaluate(c) for c in cand]
        order = sorted(range(len(cand)), key=lambda i: (-res[i][0], res[i][1]))
        bi = order[0]
        if (res[bi][0], -res[bi][1]) > (cc, -cs_):
            cur, (cc, cs_) = cand[bi], res[bi]; sig = min(sig * 1.2, 0.3)
        else:
            sig = max(sig * 0.85, 1e-4)
        if cc >= 4: best4 = cur.tolist(); break
    return cc, cs_, cur.tolist(), best4

if __name__ == "__main__":
    t0 = time.time(); rng = np.random.default_rng(20261004)
    out = dict(phase1={}, es=[], found4=[])
    with Pool(10) as pool:
        for sigma in (0.003, 0.01, 0.03, 0.1, 0.3):
            ps = [perturb(rng, P0, sigma) for _ in range(800)]
            res = pool.map(job, [list(q) for q in ps], chunksize=8)
            cs = np.array([x[0] for x in res])
            hist = np.bincount(cs[cs >= 0], minlength=8).tolist()
            out["phase1"][str(sigma)] = hist
            print(f"sigma={sigma}: hist={hist} max={cs.max()} ({time.time()-t0:.0f}s)", flush=True)
            for q, c in zip(ps, cs):
                if c >= 4: out["found4"].append((int(c), list(map(float, q)))); print("FOUND>=4", c, flush=True)
            json.dump(out, open("search2.json", "w"))
        jobs = [(P0.tolist(), 40, s0, 500 + i) for i, s0 in enumerate([0.01, 0.03, 0.1, 0.2] * 4)]
        for i, (cc, sc, cur, b4) in enumerate(pool.imap_unordered(es, jobs)):
            print(f"ES run: final count={cc} score={sc:.3e} ({time.time()-t0:.0f}s)", flush=True)
            out["es"].append(dict(count=cc, score=sc, params=cur))
            if b4: out["found4"].append((cc, b4)); print("FOUND>=4 in ES", flush=True)
            json.dump(out, open("search2.json", "w"))
    print("DONE", time.time() - t0, flush=True)
