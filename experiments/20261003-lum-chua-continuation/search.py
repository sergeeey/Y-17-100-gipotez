"""(d) structured search near the Huan-Yang / Llibre-Ponce 3-cycle mechanism.
Parameters p (12): A_R (4), A_L (4), e_R (2), e_L (2) in coordinates where the line is x=0.
HY base: A_R=HY_AP, A_L=HY_AM, e_R=e_L=(-1,0).  z' = A (z - e) in each zone.
Phase 1: random multiplicative perturbations at several scales -> count histogram.
Phase 2: (1+1)-ES maximizing count, tie-break by near-birth score (small = close to a new root)."""
import sys, json, time, numpy as np
from multiprocessing import Pool
from pwl import *

P0 = np.concatenate([HY_AP.ravel(), HY_AM.ravel(), [-1.0, 0.0], [-1.0, 0.0]])

def zones(p):
    AR = p[0:4].reshape(2, 2); AL = p[4:8].reshape(2, 2)
    return Zone(AR, -AR @ p[8:10]), Zone(AL, -AL @ p[10:12])

def profile_score(yg, g, win=12):
    """small = some event (extremum not crossing zero / root entering through a domain end) is
    close, measured against the LOCAL |g| scale (max over +-win grid points)."""
    fin = np.isfinite(g)
    best = 1.0
    i = 0; n = len(g)
    while i < n:
        if not fin[i]: i += 1; continue
        j = i
        while j + 1 < n and fin[j + 1]: j += 1
        if j - i >= 4:
            seg = g[i : j + 1]
            m = len(seg)
            def loc(k):
                return np.max(np.abs(seg[max(0, k - win) : min(m, k + win + 1)])) + 1e-300
            if i > 0: best = min(best, abs(seg[0]) / loc(0))
            if j < n - 1: best = min(best, abs(seg[-1]) / loc(m - 1))
            d = np.diff(seg)
            for k in range(1, m - 1):
                if d[k - 1] > 0 and d[k] <= 0 and seg[k] < 0: best = min(best, abs(seg[k]) / loc(k))
                if d[k - 1] < 0 and d[k] >= 0 and seg[k] > 0: best = min(best, abs(seg[k]) / loc(k))
        i = j + 1
    return best

def evaluate(p, n=2500, dmax=200.0, with_score=True):
    try:
        zR, zL = zones(p)
    except Exception:
        return -1, 1.0
    if abs(zR.a12) < 1e-3: return -1, 1.0
    yg = y_grid(zR, n, 1e-5, dmax)
    g = G(zR, zL, yg)
    fin = np.isfinite(g)
    cnt = 0; last = None
    for i in range(n):
        if not fin[i]: continue
        if last is not None and i == last + 1 and g[last] * g[i] < 0: cnt += 1
        last = i
    sc = profile_score(yg, g) if with_score else 1.0
    return cnt, sc

def job(args):
    p = np.array(args)
    return evaluate(p)

def perturb(rng, p, sigma):
    q = p.copy()
    q[:8] = p[:8] * (1 + sigma * rng.standard_normal(8)) + sigma * 0.02 * rng.standard_normal(8)
    q[8:] = p[8:] + sigma * rng.standard_normal(4) * 0.5
    return q

if __name__ == "__main__":
    rng = np.random.default_rng(20261003)
    t0 = time.time()
    c0 = evaluate(P0); print("base HY:", c0, flush=True)
    results = {}
    best_overall = (c0[0], P0.copy())
    with Pool(8) as pool:
        for sigma in (0.01, 0.03, 0.1, 0.3, 1.0):
            ps = [perturb(rng, P0, sigma) for _ in range(1200)]
            res = pool.map(job, [list(q) for q in ps], chunksize=10)
            cs = np.array([r[0] for r in res])
            hist = np.bincount(cs[cs >= 0], minlength=8)
            print(f"sigma={sigma}: invalid={int((cs<0).sum())} hist(0..)={hist.tolist()} max={cs.max()}  ({time.time()-t0:.0f}s)", flush=True)
            results[str(sigma)] = hist.tolist()
            k = int(np.argmax(cs))
            if cs[k] > best_overall[0]: best_overall = (int(cs[k]), ps[k].copy())
            if cs.max() >= 4:
                for q, c in zip(ps, cs):
                    if c >= 4: print("  FOUND>=4:", c, list(q), flush=True)
        # Phase 2: ES from several starts (HY + best 3-cycle random samples)
        def es(start, iters, sigma0, seed):
            r = np.random.default_rng(seed)
            cur = start.copy(); cc, cs_ = evaluate(cur)
            sig = sigma0
            hist = []
            for it in range(iters):
                cand = [perturb(r, cur, sig) for _ in range(24)]
                res = [evaluate(c) for c in cand]
                # lexicographic: count desc, score asc ; must keep count >= current count - 0
                order = sorted(range(len(cand)), key=lambda i: (-res[i][0], res[i][1]))
                bi = order[0]
                if (res[bi][0], -res[bi][1]) > (cc, -cs_):
                    cur, (cc, cs_) = cand[bi], res[bi]
                    sig = min(sig * 1.2, 0.3)
                else:
                    sig = max(sig * 0.85, 1e-4)
                hist.append((cc, cs_))
                if cc >= 4: break
            return cc, cs_, cur, hist
        # parallel ES runs via pool.apply_async with different seeds
        jobs = [pool.apply_async(es, (P0, 40, s0, 100 + i)) for i, s0 in enumerate([0.02, 0.05, 0.1, 0.2] * 2)]
        for i, jb in enumerate(jobs):
            cc, cs_, cur, hist = jb.get()
            print(f"ES run {i}: final count={cc} score={cs_:.3e}  params={[round(float(x),6) for x in cur]}", flush=True)
            if cc > best_overall[0]: best_overall = (cc, cur.copy())
    print("BEST overall count:", best_overall[0], "params:", list(best_overall[1]))
    json.dump(dict(hist=results, best=best_overall[0], best_params=list(best_overall[1])), open("search.json", "w"))
    print("time", time.time() - t0)
