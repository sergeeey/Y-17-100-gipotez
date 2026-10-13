"""Independent enumeration of hyperbolic Coxeter pyramids over a product of p simplices (p=2: n=d+2, p=3: n=d+3)
via the combinatorial characterisation of McLeod 2013 (Lemma 3.2, generalising Tumarkin 2004 Lemma 4):
  S = union of p quasi-Lanner diagrams L_i glued at the common node v (the base), L_i \ v = A_i connected
  parabolic (affine), every other proper subdiagram of L_i elliptic, and for every choice v_i in A_i the diagram
  S \ {v_1..v_p} is elliptic or connected parabolic.   (This is a different code path from rooted2.py: it does
  NOT use the Schur-complement DFS prune; component options come from a PSD-pruned DFS on L_i alone.)
usage: pyr_mcleod.py p maxlabel   (labels 0,3..maxlabel,99)"""
import sys, itertools, json, time
import numpy as np
from cox import *
from cox2 import geom_validate
from rooted import block_diag_L

def comp_options(A, labels, tol=1e-9):
    """attachment vectors a (len m) of a new node v to affine component A such that L=A+v is a finite-volume noncompact simplex."""
    m = len(A); GA = gram_from_L(A); ent = {c: entry(c) for c in labels}
    res = []; vec = [0]*m
    def rec(j):
        if j == m:
            if not any(vec): return
            L = np.zeros((m+1, m+1), dtype=int); L[:m,:m] = A; L[:m, m] = vec; L[m, :m] = vec
            G = gram_from_L(L)
            r = vinberg_check(G)
            if r["finite"] and not r["compact"]:
                g = geom_validate(G, want_fvec=False)
                assert g["ok_polytope"] and not g["compact"], (L, g)
                res.append(tuple(vec))
            return
        for c in labels:
            vec[j] = c
            if j+1 < m:   # proper sub-collection v + first j+1 nodes lies in some L\{u}: must be PSD
                idx = list(range(j+1)); M = np.eye(j+2)
                M[:j+1,:j+1] = GA[:j+1,:j+1]
                for t in range(j+1): M[t, j+1] = M[j+1, t] = ent[vec[t]] if vec[t] else 0.0
                if np.linalg.eigvalsh(M)[0] < -tol: continue
            rec(j+1)
        vec[j] = 0
    rec(0)
    return res

def cond3(S, spans, tol=1e-9):
    n = len(S); G = gram_from_L(S)
    for pick in itertools.product(*spans):
        keep = [t for t in range(n) if t not in pick]
        Gs = G[np.ix_(keep, keep)]
        w = np.linalg.eigvalsh(Gs)
        if w[0] > tol: continue                       # elliptic
        comps = components(G, keep)
        if len(comps) == 1 and parabolic_comps(G, keep) == 1: continue   # connected parabolic
        return False
    return True

if __name__ == "__main__":
    p = int(sys.argv[1]); maxlab = int(sys.argv[2])
    labels = [0] + list(range(3, maxlab+1)) + [INF]
    t0 = time.time()
    aff = affine_connected(9)
    opts = []   # (name, A, vec)
    for name, A in aff:
        o = comp_options(A, labels)
        print("component", name, "n_options", len(o), flush=True)
        for v in o: opts.append((name, A, v))
    print("total options", len(opts), "secs", round(time.time()-t0,1), flush=True)
    found = {}   # d -> IsoSet
    stats = {}
    for combo in itertools.combinations_with_replacement(range(len(opts)), p):
        parts = [opts[i][1] for i in combo]; vecs = [opts[i][2] for i in combo]
        usize = sum(len(a) for a in parts); n = usize + 1; d = usize - p + 1
        U, spans = block_diag_L(parts)
        S = np.zeros((n, n), dtype=int); S[:usize,:usize] = U
        o = 0
        for a, v in zip(parts, vecs):
            for t, c in enumerate(v): S[o+t, usize] = S[usize, o+t] = c
            o += len(a)
        if not cond3(S, spans): continue
        G = gram_from_L(S); vr = vinberg_check(G); g = geom_validate(G)
        st = stats.setdefault(d, dict(cond3=0, vin=0, geo=0, both=0, euler_bad=0))
        st["cond3"] += 1; st["vin"] += int(vr["finite"]); st["geo"] += int(g["ok_polytope"])
        if vr["finite"] and g["ok_polytope"]:
            st["both"] += 1
            if not (g["euler_ok"] and g["facets_ok"]): st["euler_bad"] += 1
            found.setdefault(d, IsoSet()).add(S)
    out = dict(p=p, maxlab=maxlab, secs=round(time.time()-t0,1),
               per_d={d: dict(stats[d], iso_classes=len(found.get(d, IsoSet()).items)) for d in sorted(stats)})
    print(json.dumps(out), flush=True)
    for d in sorted(found):
        for M, _ in found[d].items:
            print("d=%d" % d, describe(M), flush=True)
