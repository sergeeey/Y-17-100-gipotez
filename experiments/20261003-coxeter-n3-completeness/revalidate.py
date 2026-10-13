import re, glob, sys, json
import numpy as np
from cox import *
from cox2 import geom_validate

def parse(line):
    m = re.match(r"(?:DISAGREE )?n=(\d+) \[([^\]]*)\]", line)
    if not m: return None
    n = int(m.group(1)); L = np.zeros((n,n),dtype=int)
    for tok in m.group(2).split():
        ij, lab = tok.split(":"); i,j = map(int, ij.split("-"))
        L[i,j]=L[j,i]= INF if lab=="inf" else int(lab)
    return L

res = {}
for f in sorted(glob.glob("results/c*k*_d*.txt")):
    tag = f.split("/")[-1][:-4]
    for line in open(f, encoding="utf8", errors="replace"):
        L = parse(line)
        if L is None: continue
        dis = line.startswith("DISAGREE")
        G = gram_from_L(L)
        v = vinberg_check(G)
        g = geom_validate(G)
        key = (tag.split("_")[0], "disagree-line" if dis else "found-line")
        r = res.setdefault(key, dict(n=0, vin_fin=0, geo_ok=0, both=0, euler_bad=0, reasons={}, d={}))
        r["n"] += 1
        r["vin_fin"] += int(v["finite"])
        r["geo_ok"] += int(g["ok_polytope"])
        r["both"] += int(v["finite"] and g["ok_polytope"])
        if g["ok_polytope"] and not (g.get("euler_ok") and g.get("facets_ok")): r["euler_bad"] += 1
        if not g["ok_polytope"]:
            k = re.sub(r"[\d\(\),\.\-=]+","#",g["reason"])[:40]
            r["reasons"][k] = r["reasons"].get(k,0)+1
        dd = tag.split("_d")[1]
        r["d"].setdefault(dd, [0,0]); r["d"][dd][0]+=1; r["d"][dd][1]+=int(v["finite"] and g["ok_polytope"])
for k,v in res.items(): print(k, json.dumps(v))
