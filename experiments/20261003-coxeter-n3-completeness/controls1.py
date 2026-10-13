import sys, time, itertools, json
import numpy as np
from cox import *

out = {}
# ---- 1. library sanity (transcription check of spherical / affine diagrams)
bad = []
for name, L in spherical_connected(12):
    G = gram_from_L(L)
    if not is_elliptic(G, range(len(L))):
        bad.append(name)
for name, L in affine_connected(12):
    G = gram_from_L(L)
    if parabolic_comps(G, range(len(L))) != 1:
        bad.append(name)
print("library transcription failures:", bad, flush=True)
out["library_bad"] = bad

# ---- 2. simplices via PSD-hereditary DFS
LABELS = [0, 3, 4, 5, 6, INF]


def extensions(L, n_total):
    """All new-node attachment vectors c (len k) such that every partial induced matrix is PSD,
    except the final full matrix which is returned unfiltered (caller decides)."""
    k = len(L)
    G0 = gram_from_L(L)
    res = []
    c = [0] * k

    def rec(j):
        if j == k:
            if any(c):
                res.append(tuple(c))
            return
        for lab in LABELS:
            c[j] = lab
            idx = list(range(j + 1))
            M = np.eye(j + 2)
            M[: j + 1, : j + 1] = G0[: j + 1, : j + 1]
            for t in range(j + 1):
                M[t, j + 1] = M[j + 1, t] = entry(c[t])
            last = j == k - 1
            if last or np.linalg.eigvalsh(M)[0] > -1e-9:
                rec(j + 1)
        c[j] = 0

    rec(0)
    return res


def enum_simplices(d):
    n = d + 1
    base = []
    for name, L in spherical_connected(n - 1) + affine_connected(n - 1):
        if len(L) == n - 1:
            base.append((name, L))
    iso = IsoSet()
    found = []
    for name, L in base:
        for c in extensions(L, n):
            M = np.zeros((n, n), dtype=int)
            M[: n - 1, : n - 1] = L
            M[: n - 1, n - 1] = c
            M[n - 1, : n - 1] = c
            G = gram_from_L(M)
            sg = signature(G)
            if sg != (d, 1, 0):
                continue
            # proper subdiagrams must be PSD: guaranteed except those containing the last node and all
            # old nodes minus one -> check explicitly (final-level pruning was skipped)
            ok = True
            for u in range(n):
                keep = [t for t in range(n) if t != u]
                if np.linalg.eigvalsh(G[np.ix_(keep, keep)])[0] < -1e-9:
                    ok = False
                    break
            if not ok:
                continue
            if iso.add(M):
                found.append(M)
    return found


summary = {}
for d in range(3, 10):
    t0 = time.time()
    simp = enum_simplices(d)
    nc = nnc = 0
    disagree = 0
    eul_bad = 0
    for M in simp:
        G = gram_from_L(M)
        v = vinberg_check(G)
        g = geo_check(G)
        if v["finite"] != g["finite"] or v["compact"] != g["compact"]:
            disagree += 1
        if v["finite"]:
            f, nid, types, eul = vinberg_fvector(G)
            if eul != 1:
                eul_bad += 1
            # cross-check vertex count
            if g["n_vertices"] != f[0]:
                disagree += 1
            if v["compact"]:
                nc += 1
            else:
                nnc += 1
    summary[d] = dict(
        candidates=len(simp),
        compact=nc,
        noncompact=nnc,
        disagree=disagree,
        euler_bad=eul_bad,
        secs=round(time.time() - t0, 1),
    )
    print(
        "d=%d simplex-candidates=%d finite-compact=%d finite-noncompact=%d disagree=%d euler_bad=%d (%.1fs)"
        % (d, len(simp), nc, nnc, disagree, eul_bad, time.time() - t0),
        flush=True,
    )
out["simplices"] = summary

# ---- 3. hand controls
hc = {}


def run(name, L):
    G = gram_from_L(L)
    v = vinberg_check(G)
    g = geo_check(G)
    hc[name] = dict(
        vinberg=(v["finite"], v["compact"], v["reason"]),
        geo=(g["finite"], g["compact"], g["reason"]),
    )
    print("%-28s vinberg=%s geo=%s" % (name, hc[name]["vinberg"], hc[name]["geo"]), flush=True)


run("Lanner [3,5,3] (pos)", chain([3, 5, 3]))
run("Lanner [5,3,5] (pos)", chain([5, 3, 5]))
run("Lanner [5,3,3,5] dim4 (pos)", chain([5, 3, 3, 5]))
run("E10=T(2,3,7) dim9 (pos nc)", star((1, 2, 6)))
run("neg: chain [3,5,4]", chain([3, 5, 4]))
run("neg: E11 sig(10,2)", star((1, 2, 7)))
run("neg: chain [5,3,3,3,5]", chain([5, 3, 3, 3, 5]))
run("neg: Lanner [3,5,3] label 5->6", chain([3, 6, 3]))
out["hand"] = {k: str(v) for k, v in hc.items()}
json.dump(out, open("controls1_result.json", "w"), indent=1, default=str)
