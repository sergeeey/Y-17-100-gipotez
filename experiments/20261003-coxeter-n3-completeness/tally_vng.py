import re, glob, json
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
tally = dict(total=0, V_not_Gv=0, no_timelike_ray=0, has_timelike_and_space=0, other=0, sig_d_vs_filename_mismatch=0)
ex = []
for f in sorted(glob.glob("results/c2k2_d*.txt")):
    dfile = int(re.search(r"_d(\d+)", f).group(1))
    for line in open(f, encoding="utf8", errors="replace"):
        L = parse(line)
        if L is None: continue
        G = gram_from_L(L); sg = signature(G)
        if sg[1] != 1: continue
        tally["total"] += 1
        v = vinberg_check(G); g = geom_validate(G, want_fvec=False)
        if sg[0] != dfile: tally["sig_d_vs_filename_mismatch"] += 1
        if v["finite"] and not g["ok_polytope"]:
            tally["V_not_Gv"] += 1
            d, A, J, R = _cone_rays(G); R = np.array(R)
            q = np.einsum("ij,jk,ik->i", R, J, R) if len(R) else np.array([])
            nt = int((q < -1e-7).sum()); ns = int((q > 1e-7).sum())
            if nt == 0: tally["no_timelike_ray"] += 1
            elif ns > 0: tally["has_timelike_and_space"] += 1
            else: tally["other"] += 1; ex.append(describe(L))
print(json.dumps(tally)); print(ex[:3])
