"""Rooted DFS enumeration with an exact necessary-condition prune.

Setting: ideal vertex U (parabolic subdiagram, c affine components, |U| = d-1+c) plus k extra nodes
(k=1: n = |U|+1 ; k=2: n = |U|+2).  No dotted edges.  Labels from `labels`.

Necessary condition (derived from Vinberg's criterion, proof in notes below):
  For each root edge S = U minus one node b_i from every component, S is elliptic (|S| = d-1) and needs
  a second extension (besides U). Every candidate extension is S+{v} elliptic or S+T parabolic with an
  extra node in T; in both cases S+{extra} is positive semidefinite, i.e. the Schur complement
  1 - a_S^T G_S^{-1} a_S >= 0 for that extra node.  For k=1 this must hold for EVERY root edge; for k=2
  for every root edge at least one of the two extra nodes must satisfy it.
  Since G_S^{-1} >= 0 entrywise (spherical Coxeter diagram), the quantity is monotone in |a|, so the DFS over
  attachment coordinates prunes exactly (no candidate satisfying the condition is lost).
"""

import sys, time, itertools, json
import numpy as np
from cox import *
from rooted import block_diag_L, component_multisets

TOL_Q = 1e-9


def run(d, c, labels, k=1, log_every=0, max_leaves=10**9, only_combo=None):
    usize = d - 1 + c
    n = usize + k
    aff = affine_connected(usize)
    iso = IsoSet()
    found = []
    st = dict(d=d, c=c, k=k, n=n, labels=labels, roots=0, leaves=0, vinberg_calls=0, nodes=0)
    t0 = time.time()
    codes = [x for x in labels]
    ent = {x: entry(x) for x in codes}
    combos = component_multisets(usize, c, aff)
    if only_combo is not None:
        combos = [combos[only_combo]]
    for combo in combos:
        parts = [aff[i][1] for i in combo]
        names = [aff[i][0] for i in combo]
        U, spans = block_diag_L(parts)
        GU = gram_from_L(U)
        st["roots"] += 1
        Ps = []
        prio = []
        for pick in itertools.product(*spans):
            keep = [v for v in range(usize) if v not in pick]
            P = np.zeros((usize, usize))
            P[np.ix_(keep, keep)] = np.linalg.inv(GU[np.ix_(keep, keep)])
            Ps.append(P)
            prio.append(tuple(keep))
        Pst = np.array(Ps)
        E = len(Ps)
        diagP = np.einsum("sjj->sj", Pst)  # (E,u)

        def leaf(vecs):
            st["leaves"] += 1
            for sp in spans:
                for v in vecs:
                    if not any(v[t] for t in sp):
                        return
            xy_opts = codes if k == 2 else [None]
            for xy in xy_opts:
                M = np.zeros((n, n), dtype=int)
                M[:usize, :usize] = U
                for e, v in enumerate(vecs):
                    M[:usize, usize + e] = v
                    M[usize + e, :usize] = v
                if k == 2:
                    M[usize, usize + 1] = M[usize + 1, usize] = xy
                G = gram_from_L(M)
                st["vinberg_calls"] += 1
                vr = vinberg_check(G, priority=prio)
                if not vr["finite"]:
                    continue
                g = geo_check(G)
                if not (g["finite"] and g["compact"] == vr["compact"]):
                    print("DISAGREE", describe(M), vr, g, flush=True)
                    found.append(dict(L=M.tolist(), disagree=True))
                    continue
                if iso.add(M):
                    found.append(
                        dict(
                            L=M.tolist(),
                            roots=names,
                            compact=vr["compact"],
                            d=vr["d"],
                            nonsimple=g["nonsimple_vertices"],
                            nverts=g["n_vertices"],
                        )
                    )

        if k == 1:
            vec = [0] * usize
            q0 = np.zeros(E)
            R0 = np.zeros((E, usize))

            def rec1(j, q, R):
                st["nodes"] += 1
                if st["leaves"] > max_leaves:
                    return
                if j == usize:
                    leaf([list(vec)])
                    return
                vec[j] = 0
                rec1(j + 1, q, R)
                for code in codes:
                    if code == 0:
                        continue
                    v = ent[code]
                    qn = q + 2 * v * R[:, j] + v * v * diagP[:, j]
                    if qn.max() > 1 + TOL_Q:
                        continue
                    vec[j] = code
                    rec1(j + 1, qn, R + v * Pst[:, :, j])
                vec[j] = 0

            rec1(0, q0, R0)
        else:
            vx = [0] * usize
            vy = [0] * usize

            def rec2(j, qx, Rx, qy, Ry):
                st["nodes"] += 1
                if st["leaves"] > max_leaves:
                    return
                if j == usize:
                    leaf([list(vx), list(vy)])
                    return
                for cx in codes:
                    if cx == 0:
                        qx2, Rx2 = qx, Rx
                    else:
                        v = ent[cx]
                        qx2 = qx + 2 * v * Rx[:, j] + v * v * diagP[:, j]
                        Rx2 = Rx + v * Pst[:, :, j]
                    vx[j] = cx
                    if ((qx2 > 1 + TOL_Q) & (qy > 1 + TOL_Q)).any():
                        continue
                    for cy in codes:
                        if cy == 0:
                            qy2, Ry2 = qy, Ry
                        else:
                            v = ent[cy]
                            qy2 = qy + 2 * v * Ry[:, j] + v * v * diagP[:, j]
                            Ry2 = Ry + v * Pst[:, :, j]
                        if ((qx2 > 1 + TOL_Q) & (qy2 > 1 + TOL_Q)).any():
                            continue
                        vy[j] = cy
                        rec2(j + 1, qx2, Rx2, qy2, Ry2)
                    vy[j] = 0
                vx[j] = 0

            rec2(0, np.zeros(E), np.zeros((E, usize)), np.zeros(E), np.zeros((E, usize)))
    st["secs"] = round(time.time() - t0, 1)
    st["found"] = len(found)
    return found, st


if __name__ == "__main__":
    d = int(sys.argv[1])
    c = int(sys.argv[2])
    labels = [int(x) for x in sys.argv[3].split(",")]
    k = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    found, st = run(d, c, labels, k)
    print(json.dumps(st), flush=True)
    for f in found:
        print(
            describe(np.array(f["L"])),
            f.get("roots"),
            "compact" if f.get("compact") else "noncompact",
            "nonsimple=%s" % f.get("nonsimple"),
            flush=True,
        )
