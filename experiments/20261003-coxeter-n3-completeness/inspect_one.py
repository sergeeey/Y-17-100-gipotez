import re, glob, json, itertools
import numpy as np
from cox import *
from cox2 import geom_validate, _cone_rays

def parse(line):
    m = re.match(r"(?:DISAGREE )?n=(\d+) \[([^\]]*)\]", line)
    if not m: return None
    n = int(m.group(1)); L = np.zeros((n,n),dtype=int)
    for tok in m.group(2).split():
        ij, lab = tok.split(":"); i,j = map(int, ij.split("-"))
        L[i,j]=L[j,i]= INF if lab=="inf" else int(lab)
    return L
if __name__ != "__main__": raise SystemExit
shown = 0
for f in sorted(glob.glob("results/c2k2_d4.txt")) + sorted(glob.glob("results/c2k2_d3.txt")):
    for k, line in enumerate(open(f, encoding="utf8", errors="replace")):
        L = parse(line)
        if L is None: continue
        G = gram_from_L(L)
        v = vinberg_check(G); g = geom_validate(G)
        if v["finite"] and not g["ok_polytope"]:
            f_, nid, _, eu = vinberg_fvector(G)
            if eu != 1: continue
            d, A, J, R = _cone_rays(G)
            R = np.array(R); q = np.einsum("ij,jk,ik->i", R, J, R)
            print(f, k, describe(L)); print(" d=",d,"n=",len(L)," vinberg fvec", f_, "ideal", nid, "euler", eu)
            print(" geom reason:", g["reason"], "| rays:", len(R), "time", int((q<-1e-7).sum()), "null", int((abs(q)<=1e-7).sum()), "space", int((q>1e-7).sum()), "space q values", np.round(q[q>1e-7],4)[:5])
            shown += 1
            if shown >= 3: raise SystemExit
