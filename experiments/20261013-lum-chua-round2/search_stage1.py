"""Stage 1: how often does the paper's necessary condition for >=4 (k>=2 nonpositive roots of R and Delta_b>0) hold in the
Lienard canonical family, and what do cycle counts look like there?  Also the consistency check count <= k+2 (Thm 6)
and the sign check sign(delta')=sign(F) on found roots.
Usage: search_stage1.py <seed> <n_screen> <n_count_k2> <n_count_k01> <time_budget_s>"""

import json
import sys
import time

import numpy as np

from lc2_core import canon_zones, count_cycles2
from lc2_theory import FG_tilde, delta_b, k_negative_roots

seed, n_screen, n_k2, n_k01, budget = (
    int(sys.argv[1]),
    int(sys.argv[2]),
    int(sys.argv[3]),
    int(sys.argv[4]),
    float(sys.argv[5]),
)
rng = np.random.default_rng(seed)
t_start = time.time()


def sample():
    DL = 1.0  # time scaling fixes D_L = 1
    TL = rng.uniform(-2, 2) * 0.999
    DR = 10 ** rng.uniform(-2, 2)
    TR = rng.uniform(-2, 2) * np.sqrt(DR) * 0.999
    aL = rng.choice([-1.0, 1.0]) * 10 ** rng.uniform(
        -1.5, 1.5
    )  # space scaling is kept free: sample a_L magnitude
    aR = rng.choice([-1.0, 1.0]) * 10 ** rng.uniform(-2, 2)
    b = rng.choice([-1.0, 1.0]) * 10 ** rng.uniform(-1.5, 1.5)
    return (TL, DL, aL, TR, DR, aR, b)


screen = []
n_valid = 0
kh = {}
n_notP = 0
k2 = []
k01 = []
for _ in range(n_screen):
    p = sample()
    k, info = k_negative_roots(p)
    if k is None or not isinstance(info, dict):
        continue
    n_valid += 1
    kh[k] = kh.get(k, 0) + 1
    dlt = delta_b(*p)
    if dlt > 0:
        n_notP += 1
    full = info["deg"] == 6
    rec = dict(p=p, k=k, delta=float(dlt), deg=info["deg"])
    if k >= 2 and dlt > 0 and len(k2) < 4000:
        k2.append(rec)
    elif k <= 1 and len(k01) < 4000:
        k01.append(rec)
print(
    "screened",
    n_valid,
    "k-hist",
    kh,
    "notP share",
    n_notP / max(1, n_valid),
    "k>=2&notP kept",
    len(k2),
    flush=True,
)

results = dict(screen=dict(n=n_valid, khist=kh, n_notP=n_notP, n_k2_kept=len(k2)), counted=[])


def run(recs, nmax, label):
    cnt = 0
    for rec in recs[:nmax]:
        if time.time() - t_start > budget:
            print("budget hit", flush=True)
            return False
        p = rec["p"]
        zR, zL = canon_zones(*p)
        r = count_cycles2(zR, zL, n=2500, dmax=1e4, noise_rel=2.0e-14)
        if r["count"] is None:
            continue
        # sign check: sign(F at (paper y0=my y1, paper y1=my y0)) vs sign(multiplier-1)
        sgn_ok = []
        for q in r["roots"]:
            if not q["crossing"]:
                continue
            Y0 = q["y1"] + q["y0"]
            Y1 = q["y1"] * q["y0"]
            F, _ = FG_tilde(Y0, Y1, p)
            sgn_ok.append(float(np.sign(F) * np.sign(q["multiplier"] - 1.0)))
        out = dict(
            label=label,
            p=[float(v) for v in p],
            k=rec["k"],
            delta=rec["delta"],
            deg=rec["deg"],
            count=r["count"],
            hidden_pairs=len(r["hidden_pairs"]),
            n_near_tangent=r["n_near_tangent"],
            rejected=r["rejected_float_sign_changes"],
            kappa=r["kappa"],
            signF_vs_mult=sgn_ok,
            ambiguous=r["ambiguous_gaps"],
        )
        results["counted"].append(out)
        cnt += 1
        if r["count"] >= 3 or r["count"] > rec["k"] + 2 and rec["deg"] == 6:
            print("NOTE", out, flush=True)
        if cnt % 25 == 0:
            print(label, cnt, "elapsed", round(time.time() - t_start), flush=True)
            json.dump(results, open(f"search_stage1_seed{seed}.json", "w"), default=float)
    return True


run(k2, n_k2, "k>=2")
run(k01, n_k01, "k<=1")
json.dump(results, open(f"search_stage1_seed{seed}.json", "w"), default=float)
ch = {}
for o in results["counted"]:
    key = (o["label"], o["count"])
    ch[str(key)] = ch.get(str(key), 0) + 1
print("count hist", ch, flush=True)
viol = [o for o in results["counted"] if o["deg"] == 6 and o["count"] > o["k"] + 2]
print("Thm6 violations (count>k+2, deg 6):", len(viol), flush=True)
sg = [s for o in results["counted"] for s in o["signF_vs_mult"]]
print(
    "signF*sign(mult-1): +1:",
    sum(1 for s in sg if s > 0),
    " -1:",
    sum(1 for s in sg if s < 0),
    flush=True,
)
print("done", round(time.time() - t_start), flush=True)
