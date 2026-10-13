"""Classify converged dim-3 solutions (chunks d3*_chunk*.npz).
Per solution: rel. residual, conditioning, spectrum multiplicities (alg,geom), L(R) dimension and class
(U1-free / degenerate / distinct), monomial test, Hecke test (#distinct eigenvalues), 'charge' type of L.
Class 'distinct' => locally conjugate to a strict/additive charge-conserving solution (enzuigiri, arXiv:2609.38290 Thm 3.1):
  an element of L with 3 distinct eigenvalues has either AP spectrum (ACC) or generic spectrum (=> L = full torus => SCC).
'Beyond ACC' = class U1-free or degenerate.
usage: python classify3.py out.json chunk1.npz chunk2.npz ...
"""

import sys, json, collections, glob
import numpy as np
from ybe import *


def clean(R, N=3):
    R = R / abs(np.linalg.det(R)) ** (1.0 / (N * N))
    return R


def is_monomial(R, tol=1e-8):
    A = np.abs(R) > tol * np.abs(R).max()
    return bool(A.sum(0).max() == 1 and A.sum(1).max() == 1)


def analyse(R, N=3):
    Rn = clean(R, N)
    sv = np.linalg.svd(Rn, compute_uv=False)
    cond = sv[0] / sv[-1]
    ev = np.linalg.eigvals(Rn)
    groups = cluster_eigs(ev, 1e-4)
    mults = tuple(sorted((len(g) for g in groups), reverse=True))
    sig = spectral_signature(Rn, N, tol=1e-4)
    geom = tuple(sorted((a, g) for a, g, _ in sig))
    cc = cc_class(Rn, N)
    null, s = L_algebra(Rn, N)
    # type of L: eigen-structure of generic element
    rng = np.random.default_rng(0)
    d = len(null)
    ltype = None
    if d >= 2:
        c = rng.normal(size=d) + 1j * rng.normal(size=d)
        h = sum(ci * b for ci, b in zip(c, null))
        hev = np.linalg.eigvals(h)
        hg = cluster_eigs(hev, 1e-5)
        ltype = tuple(sorted((len(g) for g in hg), reverse=True))
        # diagonalizable? (compare rank of h - lam I)
        diag = True
        for g in hg:
            lam = np.mean(g)
            r = np.linalg.matrix_rank(h - lam * np.eye(N), tol=1e-6 * max(1, abs(lam)))
            if N - r != len(g):
                diag = False
        ltype = (ltype, "diag" if diag else "jordan")
    return dict(
        res=float(rel_res(Rn, N)),
        cond=float(cond),
        mults=mults,
        geom=geom,
        dimL=cc["dimL"],
        label=cc["label"],
        ltype=ltype,
        monomial=is_monomial(Rn),
        nspec=len(groups),
        rank=int(np.linalg.matrix_rank(Rn, tol=1e-8)),
    )


if __name__ == "__main__":
    out = sys.argv[1]
    files = []
    for a in sys.argv[2:]:
        files += sorted(glob.glob(a))
    rows = []
    Rs = []
    for f in files:
        d = np.load(f)
        for i, R in enumerate(d["R"]):
            Rs.append(R)
            a = analyse(R)
            a["file"] = f
            a["idx"] = i
            a["mode"] = str(d["mode"][i])
            a["seed"] = int(d["seed"][i])
            rows.append(a)
    print("total converged", len(rows))
    good = [r for r in rows if r["res"] < 1e-10 and r["cond"] < 1e6]
    print("residual<1e-10 and cond<1e6:", len(good))
    cnt = collections.Counter(r["label"] for r in good)
    print("by L-class:", dict(cnt))
    grp = collections.defaultdict(list)
    for r in good:
        grp[
            (r["label"], r["dimL"], r["ltype"], r["mults"], r["geom"], r["monomial"], r["rank"])
        ].append(r)
    for k, v in sorted(grp.items(), key=lambda t: (t[0][0] == "distinct", -len(t[1]))):
        print(len(v), k)
    json.dump(rows, open(out, "w"), default=str)
