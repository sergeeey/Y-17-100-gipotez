"""Stage 3: condition the search on the paper's necessary condition.  Random walk INSIDE {k>=3, Delta_b>0} (k = number of
nonpositive roots of R, Thm 6: cycles <= k+2), growing a pool of such canonical systems, then count cycles on a spread
subsample; then a count-guided walk (accept child iff its count >= parent's count) started from the highest-count pool members.
Usage: search_stage3.py <seed> <k_min> <t_walk_s> <t_count_s> <t_guided_s>"""

import json
import sys
import time

import numpy as np

from lc2_core import canon_zones, count_cycles2
from lc2_theory import delta_b, k_negative_roots

seed, kmin, t_walk, t_count, t_guided = (
    int(sys.argv[1]),
    int(sys.argv[2]),
    float(sys.argv[3]),
    float(sys.argv[4]),
    float(sys.argv[5]),
)
rng = np.random.default_rng(seed)
t0 = time.time()


def valid(p):
    TL, DL, aL, TR, DR, aR, b = p
    return DL > 0 and DR > 0 and 4 * DL - TL**2 > 0 and 4 * DR - TR**2 > 0 and aL * aR * b != 0


def kd(p):
    k, info = k_negative_roots(tuple(p))
    if k is None or not isinstance(info, dict):
        return None, None, None
    return k, info["deg"], delta_b(*p)


def sample():
    DL = 1.0
    TL = rng.uniform(-2, 2) * 0.999
    DR = 10 ** rng.uniform(-2, 2)
    TR = rng.uniform(-2, 2) * np.sqrt(DR) * 0.999
    aL = rng.choice([-1.0, 1.0]) * 10 ** rng.uniform(-1.5, 1.5)
    aR = rng.choice([-1.0, 1.0]) * 10 ** rng.uniform(-2, 2)
    b = rng.choice([-1.0, 1.0]) * 10 ** rng.uniform(-1.5, 1.5)
    return np.array([TL, DL, aL, TR, DR, aR, b])


def perturb(p, s):
    q = p.copy()
    q[[0, 3]] = q[[0, 3]] + s * rng.normal(size=2) * (1 + np.abs(q[[0, 3]]))
    q[[2, 4, 5, 6]] = q[[2, 4, 5, 6]] * np.exp(s * rng.normal(size=4))
    return q


# ---- phase A: find seeds with k>=kmin, then diffuse inside the region
pool = []
ndraw = 0
while time.time() - t0 < t_walk * 0.4 and len(pool) < 40:
    p = sample()
    ndraw += 1
    k, deg, dl = kd(p)
    if k is not None and k >= kmin and dl > 0:
        pool.append((p, k, deg))
print("phase A: draws", ndraw, "seeds with k>=%d:" % kmin, len(pool), flush=True)
nstep = 0
while pool and time.time() - t0 < t_walk and len(pool) < 3000:
    p, k, deg = pool[rng.integers(len(pool))]
    q = perturb(p, float(rng.choice([0.02, 0.1, 0.3])))
    nstep += 1
    if not valid(q):
        continue
    k2, deg2, dl2 = kd(q)
    if k2 is not None and k2 >= kmin and dl2 > 0:
        pool.append((q, k2, deg2))
print(
    "phase B: steps",
    nstep,
    "pool",
    len(pool),
    "k-hist",
    {
        int(a): int(np.sum([1 for _, kk, _ in pool if kk == a]))
        for a in sorted(set(kk for _, kk, _ in pool))
    },
    flush=True,
)

# ---- phase C: count on a spread subsample
rows = []
idx = rng.permutation(len(pool))
tc = time.time()
for i in idx:
    if time.time() - tc > t_count:
        break
    p, k, deg = pool[i]
    zR, zL = canon_zones(*p)
    r = count_cycles2(zR, zL, n=2500, dmax=1e4, noise_rel=2.0e-14)
    if r["count"] is None:
        continue
    rows.append(
        dict(
            p=[float(v) for v in p],
            k=k,
            deg=deg,
            count=r["count"],
            hidden=len(r["hidden_pairs"]),
            nt=r["n_near_tangent"],
        )
    )
    if r["count"] >= 4 or (deg == 6 and r["count"] > k + 2):
        print("!!! CANDIDATE/VIOLATION", rows[-1], flush=True)
h = {}
for r in rows:
    h[(r["k"], r["count"])] = h.get((r["k"], r["count"]), 0) + 1
print(
    "phase C counted",
    len(rows),
    "hist (k,count):n",
    {str(a): b for a, b in sorted(h.items())},
    flush=True,
)

# ---- phase D: count-guided walk inside the high-k region (accept child iff count >= parent count and k>=kmin)
best_rows = sorted(rows, key=lambda r: -r["count"])[:20]
cur = [(np.array(r["p"]), r["count"]) for r in best_rows if r["count"] >= 1]
if not cur:
    cur = [(np.array(r["p"]), r["count"]) for r in rows[:10]]
td = time.time()
guided = []
maxc = max([c for _, c in cur], default=0)
n_eval = 0
while cur and time.time() - td < t_guided:
    j = rng.integers(len(cur))
    p, c = cur[j]
    q = perturb(p, float(rng.choice([0.003, 0.02, 0.1])))
    if not valid(q):
        continue
    k2, deg2, dl2 = kd(q)
    if k2 is None or k2 < kmin or dl2 <= 0:
        continue
    zR, zL = canon_zones(*q)
    r = count_cycles2(zR, zL, n=2500, dmax=1e4, noise_rel=2.0e-14)
    n_eval += 1
    if r["count"] is None:
        continue
    guided.append(dict(p=[float(v) for v in q], k=k2, deg=deg2, count=r["count"]))
    if r["count"] >= c:
        cur.append((q, r["count"]))
        if len(cur) > 60:
            cur.sort(key=lambda t: -t[1])
            cur = cur[:40]
    if r["count"] > maxc:
        maxc = r["count"]
        print("guided new max", maxc, "k", k2, flush=True)
    if r["count"] >= 4 or (deg2 == 6 and r["count"] > k2 + 2):
        print("!!! CANDIDATE/VIOLATION", guided[-1], flush=True)
hg = {}
for r in guided:
    hg[(r["k"], r["count"])] = hg.get((r["k"], r["count"]), 0) + 1
print(
    "phase D evals",
    n_eval,
    "hist (k,count):n",
    {str(a): b for a, b in sorted(hg.items())},
    flush=True,
)
json.dump(dict(rows=rows, guided=guided), open(f"search_stage3_seed{seed}.json", "w"))
print(
    "max count overall",
    max([r["count"] for r in rows + guided], default=None),
    "violations Thm6:",
    sum(1 for r in rows + guided if r["deg"] == 6 and r["count"] > r["k"] + 2),
    "done",
    round(time.time() - t0),
    flush=True,
)
