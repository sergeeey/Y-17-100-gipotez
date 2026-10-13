"""pyr2.py -- independent (McLeod/Tumarkin Lemma-11 style) enumeration of hyperbolic Coxeter pyramids over
a product of p simplices (p=2: n=d+2 ; p=3: n=d+3), SERIAL, with a pairwise elliptic prune.
Path differs from rooted2.py: component options come from L_i alone (quasi-Lanner simplices with a marked
parabolic L_i\\v), glued at the common node v; Lemma conditions (1)-(3) checked directly; every survivor is
then decided by BOTH vinberg_check and the strict geometric validator geom_validate (cox2).
usage: pyr2.py p maxlabel      (alphabet 0,3..maxlabel,inf)"""

import sys, itertools, json, time
import numpy as np
from cox import *
from cox2 import geom_validate
from rooted import block_diag_L


def comp_options(A, labels, tol=1e-9):
    m = len(A)
    GA = gram_from_L(A)
    ent = {c: entry(c) for c in labels}
    res = []
    vec = [0] * m

    def rec(j):
        if j == m:
            if not any(vec):
                return
            L = np.zeros((m + 1, m + 1), dtype=int)
            L[:m, :m] = A
            L[:m, m] = vec
            L[m, :m] = vec
            G = gram_from_L(L)
            # Lemma cond (2): every proper subdiagram of L other than A=L\v is elliptic
            for u in range(m):
                keep = [t for t in range(m + 1) if t != u]
                if np.linalg.eigvalsh(G[np.ix_(keep, keep)])[0] <= tol:
                    return
            r = vinberg_check(G)
            if r["finite"] and not r["compact"]:
                g = geom_validate(G, want_fvec=False)
                assert g["ok_polytope"] and not g["compact"], (L, g)
                res.append(tuple(vec))
            return
        for c in labels:
            vec[j] = c
            if j + 1 < m:
                M = np.eye(j + 2)
                M[: j + 1, : j + 1] = GA[: j + 1, : j + 1]
                for t in range(j + 1):
                    M[t, j + 1] = M[j + 1, t] = ent[vec[t]] if vec[t] else 0.0
                if np.linalg.eigvalsh(M)[0] < -tol:
                    continue
            rec(j + 1)
        vec[j] = 0

    rec(0)
    return res


def option_block(A, vec):
    m = len(A)
    L = np.zeros((m + 1, m + 1), dtype=int)
    L[:m, :m] = A
    L[:m, m] = vec
    L[m, :m] = vec
    return gram_from_L(L)


def pair_ok(Gi, Gj, mi, mj, tol=1e-9):
    """(A_i\\u) + (A_j\\w) + v must be elliptic for all u,w (a sub-diagram of S\\{v1..vp}, which is
    elliptic or connected parabolic; it cannot be the whole thing because the third part / extra nodes remain,
    and a proper subdiagram of a connected parabolic diagram is elliptic)."""
    for u in range(mi):
        ki = [t for t in range(mi) if t != u]
        for w in range(mj):
            kj = [t for t in range(mj) if t != w]
            idx = len(ki) + len(kj) + 1
            M = np.eye(idx)
            M[: len(ki), : len(ki)] = Gi[np.ix_(ki, ki)]
            o = len(ki)
            M[o : o + len(kj), o : o + len(kj)] = Gj[np.ix_(kj, kj)]
            M[: len(ki), -1] = M[-1, : len(ki)] = Gi[ki, mi]
            M[o : o + len(kj), -1] = M[-1, o : o + len(kj)] = Gj[kj, mj]
            if np.linalg.eigvalsh(M)[0] <= tol:
                return False
    return True


def cond3(S, spans, tol=1e-9):
    n = len(S)
    G = gram_from_L(S)
    for pick in itertools.product(*spans):
        keep = [t for t in range(n) if t not in pick]
        w = np.linalg.eigvalsh(G[np.ix_(keep, keep)])
        if w[0] > tol:
            continue
        comps = components(G, keep)
        if len(comps) == 1 and parabolic_comps(G, keep) == 1:
            continue
        return False
    return True


if __name__ == "__main__":
    p = int(sys.argv[1])
    maxlab = int(sys.argv[2])
    labels = [0] + list(range(3, maxlab + 1)) + [INF]
    t0 = time.time()
    opts = []
    for name, A in affine_connected(9):
        o = comp_options(A, labels)
        for v in o:
            opts.append((name, A, v))
    print("options", len(opts), "secs", round(time.time() - t0, 1), flush=True)
    blocks = [option_block(A, v) for _, A, v in opts]
    sizes = [len(A) for _, A, _ in opts]
    N = len(opts)
    ok = np.zeros((N, N), dtype=bool)
    if p == 2:
        # WHY: for p=2 the pair diagram IS the whole S\{v1,v2} (may be connected parabolic), so the pair-elliptic
        # prune is INVALID here (it wrongly dropped dims 9,12,13,17 in the first p=2 run). Valid only for p>=3.
        ok[:, :] = True
    else:
        for i in range(N):
            for j in range(i, N):
                ok[i, j] = ok[j, i] = pair_ok(blocks[i], blocks[j], sizes[i], sizes[j])
    print(
        "pair table done",
        int(ok.sum()),
        "of",
        N * N,
        "secs",
        round(time.time() - t0, 1),
        flush=True,
    )
    combos = []
    if p == 2:
        combos = [(i, j) for i in range(N) for j in range(i, N) if ok[i, j]]
    else:
        for i in range(N):
            for j in range(i, N):
                if not ok[i, j]:
                    continue
                for k in range(j, N):
                    if ok[i, k] and ok[j, k]:
                        combos.append((i, j, k))
    print(
        "candidate combos after pair prune",
        len(combos),
        "secs",
        round(time.time() - t0, 1),
        flush=True,
    )
    found = {}
    stats = {}
    for combo in combos:
        parts = [opts[i][1] for i in combo]
        vecs = [opts[i][2] for i in combo]
        usize = sum(len(a) for a in parts)
        n = usize + 1
        d = usize - p + 1
        U, spans = block_diag_L(parts)
        S = np.zeros((n, n), dtype=int)
        S[:usize, :usize] = U
        o = 0
        for a, v in zip(parts, vecs):
            for t, c in enumerate(v):
                S[o + t, usize] = S[usize, o + t] = c
            o += len(a)
        if not cond3(S, spans):
            continue
        G = gram_from_L(S)
        vr = vinberg_check(G)
        g = geom_validate(G)
        st = stats.setdefault(d, dict(cond3=0, vin=0, geo=0, both=0, euler_bad=0))
        st["cond3"] += 1
        st["vin"] += int(vr["finite"])
        st["geo"] += int(g["ok_polytope"])
        if vr["finite"] and g["ok_polytope"]:
            st["both"] += 1
            if not (g["euler_ok"] and g["facets_ok"]):
                st["euler_bad"] += 1
            found.setdefault(d, IsoSet()).add(S, [opts[i][0] for i in combo])
    out = dict(
        p=p,
        maxlab=maxlab,
        n_options=N,
        n_combos=len(combos),
        secs=round(time.time() - t0, 1),
        per_d={
            d: dict(stats[d], iso_classes=len(found.get(d, IsoSet()).items)) for d in sorted(stats)
        },
    )
    print(json.dumps(out), flush=True)
    for d in sorted(found):
        for M, pay in found[d].items:
            print("d=%d" % d, pay, describe(M), flush=True)
