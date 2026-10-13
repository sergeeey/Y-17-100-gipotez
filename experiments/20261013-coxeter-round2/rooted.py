"""Rooted enumeration: fix an ideal vertex U (parabolic subdiagram of rank d-1 with c affine
components, |U| = d-1+c) and ONE extra node x (n = |U|+1) attached to U by labels in LAB.
Necessary: x must attach to every component (x does not pass through the ideal vertex).
Family: no dotted edges.  Each candidate is decided by vinberg_check AND geo_check."""

import sys, time, itertools, json
import numpy as np
from cox import *


def block_diag_L(parts):
    n = sum(len(p) for p in parts)
    M = np.zeros((n, n), dtype=int)
    o = 0
    spans = []
    for p in parts:
        k = len(p)
        M[o : o + k, o : o + k] = p
        spans.append(list(range(o, o + k)))
        o += k
    return M, spans


def component_multisets(total, c, aff):
    """multisets of c affine diagrams with total node count `total`."""
    res = []
    for combo in itertools.combinations_with_replacement(range(len(aff)), c):
        if sum(len(aff[i][1]) for i in combo) == total:
            res.append(combo)
    return res


def digits_chunk(start, stop, base, width):
    idx = np.arange(start, stop, dtype=np.int64)
    out = np.empty((len(idx), width), dtype=np.int8)
    for p in range(width):
        out[:, p] = idx % base
        idx = idx // base
    return out


def run_rooted(d, c, labels, extras=1, log=None, max_secs=1e9, chunk=400000):
    usize = d - 1 + c
    aff = affine_connected(usize)
    iso = IsoSet()
    found = []
    stats = dict(d=d, c=c, usize=usize, labels=labels, roots=0, candidates=0, attached=0, secs=0)
    t0 = time.time()
    labs = np.array(labels, dtype=np.int16)
    base = len(labels)
    for combo in component_multisets(usize, c, aff):
        parts = [aff[i][1] for i in combo]
        names = [aff[i][0] for i in combo]
        U, spans = block_diag_L(parts)
        stats["roots"] += 1
        n = usize + 1
        GU = gram_from_L(U)
        # root edges: U minus one node per component
        prio = []
        for pick in itertools.product(*spans):
            prio.append(tuple(v for v in range(usize) if v not in pick))
        total = base**usize
        for start in range(0, total, chunk):
            D = digits_chunk(start, min(total, start + chunk), base, usize)
            vals = labs[D]  # codes
            ok = np.ones(len(D), dtype=bool)
            for sp in spans:
                ok &= (vals[:, sp] != 0).any(axis=1)
            stats["candidates"] += len(D)
            sel = np.nonzero(ok)[0]
            stats["attached"] += len(sel)
            for r in sel:
                cvec = vals[r]
                M = np.zeros((n, n), dtype=int)
                M[:usize, :usize] = U
                M[:usize, usize] = cvec
                M[usize, :usize] = cvec
                G = gram_from_L(M)
                v = vinberg_check(G, priority=prio)
                if not v["finite"]:
                    continue
                g = geo_check(G)
                if not (g["finite"] and g["compact"] == v["compact"]):
                    print("DISAGREE", describe(M), v, g, flush=True)
                    found.append(dict(L=M.tolist(), disagree=True))
                    continue
                if iso.add(M):
                    found.append(
                        dict(
                            L=M.tolist(),
                            roots=names,
                            compact=v["compact"],
                            d=v["d"],
                            nonsimple=g["nonsimple_vertices"],
                            nverts=g["n_vertices"],
                        )
                    )
            if time.time() - t0 > max_secs:
                stats["truncated"] = True
                break
    stats["secs"] = round(time.time() - t0, 1)
    stats["found"] = len(found)
    return found, stats


if __name__ == "__main__":
    mode = sys.argv[1]
    d = int(sys.argv[2])
    labels = [int(x) for x in sys.argv[3].split(",")]
    c = int(sys.argv[4])
    found, stats = run_rooted(d, c, labels)
    print(json.dumps(stats), flush=True)
    for f in found:
        print(
            describe(np.array(f["L"])),
            f.get("roots"),
            "compact" if f.get("compact") else "noncompact",
            "nonsimple=%s" % f.get("nonsimple"),
            flush=True,
        )
