"""Brute-force (no prune) cross-check of the pruned DFS in rooted2.py.
usage: bf_check.py d c k labels   -> compares iso-sets from DFS and from exhaustive attachment enumeration."""

import sys, itertools, json, time
import numpy as np
from cox import *
from rooted import block_diag_L, component_multisets
import rooted2


def bf_root(args):
    d, c, k, labels, ci = args
    usize = d - 1 + c
    n = usize + k
    aff = affine_connected(usize)
    combo = component_multisets(usize, c, aff)[ci]
    U, spans = block_diag_L([aff[i][1] for i in combo])
    prio = [tuple(v for v in range(usize) if v not in pick) for pick in itertools.product(*spans)]
    out = []
    vecs = [
        v
        for v in itertools.product(labels, repeat=usize)
        if all(any(v[t] for t in sp) for sp in spans)
    ]
    pairs = itertools.product(vecs, repeat=k)
    for tup in pairs:
        xy_opts = labels if k == 2 else [None]
        for xy in xy_opts:
            M = np.zeros((n, n), dtype=int)
            M[:usize, :usize] = U
            for e, v in enumerate(tup):
                M[:usize, usize + e] = v
                M[usize + e, :usize] = v
            if k == 2:
                M[usize, usize + 1] = M[usize + 1, usize] = xy
            G = gram_from_L(M)
            r = vinberg_check(G, priority=prio)
            if r["finite"]:
                out.append(M.tolist())
    return out


def dfs_root(args):
    d, c, k, labels, ci = args
    found, st = rooted2.run(d, c, labels, k, only_combo=ci)
    return [f["L"] for f in found]


if __name__ == "__main__":
    d, c, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    labels = [int(x) for x in sys.argv[4].split(",")]
    usize = d - 1 + c
    nroots = len(component_multisets(usize, c, affine_connected(usize)))
    t0 = time.time()
    # SERIAL (hardware rule 7a: ProcessPoolExecutor(22) removed after the 2026-10-03 overheating)
    bf = [m for i in range(nroots) for m in bf_root((d, c, k, labels, i))]
    dfs = [m for i in range(nroots) for m in dfs_root((d, c, k, labels, i))]
    A, B = IsoSet(), IsoSet()
    for m in bf:
        A.add(np.array(m))
    for m in dfs:
        B.add(np.array(m))
    onlyA = sum(1 for m, _ in A.items if B.add(m) is not False and False) if False else None
    # symmetric difference via fresh sets
    sA, sB = IsoSet(), IsoSet()
    for m, _ in A.items:
        sA.add(m)
    for m, _ in B.items:
        sB.add(m)
    miss_in_dfs = sum(1 for m, _ in A.items if sB.add(m))  # new => not present in DFS
    miss_in_bf = sum(1 for m, _ in B.items if sA.add(m))
    print(
        json.dumps(
            dict(
                d=d,
                c=c,
                k=k,
                labels=labels,
                roots=nroots,
                bf_iso=len(A.items),
                dfs_iso=len(B.items),
                in_bf_not_dfs=miss_in_dfs,
                in_dfs_not_bf=miss_in_bf,
                secs=round(time.time() - t0, 1),
            )
        ),
        flush=True,
    )
