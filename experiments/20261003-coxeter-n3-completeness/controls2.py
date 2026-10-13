"""controls2.py -- differential test of the two criterion implementations (Vinberg vs strict geometric cone
validator geom_validate in cox2.py) on mutants of known-good diagrams, plus diagnosis of the stored
'Vinberg says finite, geometry says no' candidates from the first (interrupted) c2k2 run.

Definitions per Gram matrix G (sig (d,1)):
  V   = vinberg_check(G)["finite"]           (combinatorial: elliptic/parabolic subdiagram extensions)
  Gv  = geom_validate(G)["ok_polytope"]      (cone built from scratch; finite volume AND the facets/ridges of
                                              the cone reproduce exactly the diagram that was fed in)
Soundness direction (must hold, else toolkit BLOCKED, kill K1):  Gv  =>  V.
Converse direction can fail legitimately when G is NOT the Gram matrix of any polytope (Vinberg's theorem
presupposes that it is).  For every V and not Gv case we compute the Euler characteristic of the face counts
that Vinberg's subdiagram combinatorics would assert; a genuine finite-volume polytope has Euler sum == 1.
"""

import sys, re, glob, json, time, random
import numpy as np
from cox import *
from cox2 import geom_validate

random.seed(20261003)
T0 = time.time()
LAB = [0, 3, 4, 5, 6, INF]


def parse(line):
    m = re.match(r"(?:DISAGREE )?n=(\d+) \[([^\]]*)\]", line)
    if not m:
        return None
    n = int(m.group(1))
    L = np.zeros((n, n), dtype=int)
    for tok in m.group(2).split():
        ij, lab = tok.split(":")
        i, j = map(int, ij.split("-"))
        L[i, j] = L[j, i] = INF if lab == "inf" else int(lab)
    return L


def classify(L):
    G = gram_from_L(L)
    sg = signature(G)
    # WHY: n > d+1 facets => the Gram matrix has nullity n-d-1 > 0. The first version of this script demanded
    # nullity 0 and therefore silently tested only the simplex case (the bug that made 'stored c2k2' empty).
    if sg[1] != 1:
        return None
    v = vinberg_check(G)
    g = geom_validate(G)
    return G, v, g


def euler_of_vinberg(G):
    try:
        f, nid, _, eu = vinberg_fvector(G)
        return eu
    except Exception as e:
        return None


# ---------------- seeds: known positives (verified earlier lines + hand controls)
seeds = []
for f in sorted(glob.glob("results/c3k1_d*.txt")) + sorted(glob.glob("results/c2k1_d*.txt")):
    for line in open(f, encoding="utf8", errors="replace"):
        L = parse(line)
        if L is not None and len(L) <= 9:
            seeds.append(L)
for labs in ([3, 5, 3], [5, 3, 5], [5, 3, 3, 5], [3, 3, 6], [4, 3, 6], [3, 4, 3, 4]):
    seeds.append(chain(labs))
print("seeds", len(seeds), flush=True)
pos = dict(n=0, V=0, Gv=0, both=0, euler_bad=0, nullity_hist={})
for L in seeds:
    r = classify(L)
    if r is None: continue
    G, v, g = r
    pos["n"] += 1; pos["V"] += int(v["finite"]); pos["Gv"] += int(g["ok_polytope"])
    pos["both"] += int(v["finite"] and g["ok_polytope"])
    if g["ok_polytope"] and not (g.get("euler_ok") and g.get("facets_ok")): pos["euler_bad"] += 1
    nz = signature(G)[2]; pos["nullity_hist"][nz] = pos["nullity_hist"].get(nz, 0) + 1
print("unmutated verified positives (seeds):", json.dumps(pos), flush=True)

conf = dict(n_mut=0, sig_ok=0, V_and_Gv=0, V_not_Gv=0, notV_and_Gv=0, neither=0)
v_not_gv_reasons = {}
v_not_gv_euler = {"1": 0, "not1": 0, "err": 0}
sound_violations = []
MAXMUT = 900
tries = 0
while conf["n_mut"] < MAXMUT and tries < 20000 and time.time() - T0 < 420:
    tries += 1
    L = random.choice(seeds).copy()
    n = len(L)
    for _ in range(random.choice([1, 1, 2])):
        i, j = random.sample(range(n), 2)
        L[i, j] = L[j, i] = random.choice(LAB)
    conf["n_mut"] += 0
    r = classify(L)
    if r is None:
        continue
    G, v, g = r
    conf["n_mut"] += 1
    conf["sig_ok"] += 1
    V, Gv = v["finite"], g["ok_polytope"]
    if V and Gv:
        conf["V_and_Gv"] += 1
    elif V and not Gv:
        conf["V_not_Gv"] += 1
        k = re.sub(r"[\d\(\),\.\-=]+", "#", g["reason"])[:40]
        v_not_gv_reasons[k] = v_not_gv_reasons.get(k, 0) + 1
        eu = euler_of_vinberg(G)
        if eu is None:
            v_not_gv_euler["err"] += 1
        elif eu == 1:
            v_not_gv_euler["1"] += 1
        else:
            v_not_gv_euler["not1"] += 1
    elif Gv and not V:
        conf["notV_and_Gv"] += 1
        sound_violations.append(describe(L))
    else:
        conf["neither"] += 1
print("mutation differential:", json.dumps(conf), flush=True)
print("V_not_Gv reasons:", json.dumps(v_not_gv_reasons), flush=True)
print("V_not_Gv Vinberg-fvector Euler sum:", json.dumps(v_not_gv_euler), flush=True)
print(
    "SOUNDNESS VIOLATIONS (Gv and not V):", sound_violations[:5], len(sound_violations), flush=True
)

# ---------------- diagnose stored first-run candidates (c2k2 d=3..5)
diag = dict(n=0, V=0, Gv=0, V_not_Gv=0, euler1=0, euler_not1=0, euler_err=0)
cnt = 0
for f in sorted(glob.glob("results/c2k2_d*.txt")):
    for line in open(f, encoding="utf8", errors="replace"):
        L = parse(line)
        if L is None:
            continue
        if time.time() - T0 > 560:
            break
        r = classify(L)
        if r is None:
            continue
        G, v, g = r
        diag["n"] += 1
        diag["V"] += int(v["finite"])
        diag["Gv"] += int(g["ok_polytope"])
        if v["finite"] and not g["ok_polytope"]:
            diag["V_not_Gv"] += 1
            cnt += 1
            if cnt % 6 == 0:  # Euler on a 1/6 subsample (cost)
                eu = euler_of_vinberg(G)
                if eu is None:
                    diag["euler_err"] += 1
                elif eu == 1:
                    diag["euler1"] += 1
                else:
                    diag["euler_not1"] += 1
print("stored c2k2 candidates:", json.dumps(diag), flush=True)
print("secs", round(time.time() - T0, 1), flush=True)
