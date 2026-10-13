"""cox2.py -- stricter, independent polytope validator (v2, written after the interrupted attempt).

Why: Vinberg's finite-volume criterion (vinberg_check in cox.py) presupposes that the Gram matrix G
is the Gram matrix of an actual acute-angled polytope with n NON-REDUNDANT facets. For an arbitrary
candidate matrix of signature (d,1) that need not hold (the first attempt logged 900+ cases where
vinberg_check said 'finite' while the geometric cone had no timelike ray at all).

geom_validate(G) builds the cone K = {x : <e_i,x> <= 0} in R^{d,1} from scratch (no diagram
combinatorics) and returns a dict with:
  ok_polytope   : cone nonempty, every extreme ray time- or lightlike with a common orientation
                  (=> P = K ∩ H^d has finite volume), every facet is a genuine (d-1)-face
                  (non-redundant), and the ridge structure agrees with G:
                    facets i,j meet in a (d-2)-face  <=>  G_ij > -1 (angle pi/m or pi/2),
                  so the diagram of P is exactly the diagram that was fed in.
  compact       : no lightlike ray
  fvec          : f-vector from the face lattice (rays counted as vertices, ideal included)
  euler_ok      : sum (-1)^i f_i == 1 (including the d-face)
"""

import itertools
import numpy as np

TOLV = 1e-7


def _cone_rays(G, tol=TOLV):
    n = G.shape[0]
    w, Q = np.linalg.eigh(G)
    pos = [i for i in range(n) if w[i] > 1e-9]
    neg = [i for i in range(n) if w[i] < -1e-9]
    if len(neg) != 1:
        return None
    d = len(pos)
    idx = pos + neg
    V = Q[:, idx] * np.sqrt(np.abs(w[idx]))
    J = np.diag([1.0] * d + [-1.0])
    A = V @ J  # row i = J e_i  so that (A x)_i = <e_i, x>_J
    rays = {}
    for S in itertools.combinations(range(n), d):
        M = A[list(S)]
        u, s, vt = np.linalg.svd(M)
        if s[-1] < 1e-9:
            continue
        x = vt[-1]
        v = A @ x
        if np.all(v <= tol):
            y = x
        elif np.all(v >= -tol):
            y = -x
        else:
            continue
        y = y / np.linalg.norm(y)
        key = tuple((np.round(y, 6) + 0.0).tolist())
        rays[key] = y
    return d, A, J, list(rays.values())


def geom_validate(G, tol=TOLV, want_fvec=True):
    n = G.shape[0]
    out = dict(ok_polytope=False, compact=False, reason="")
    cr = _cone_rays(G, tol)
    if cr is None:
        out["reason"] = "signature"
        return out
    d, A, J, R = cr
    out["d"] = d
    if not R:
        out["reason"] = "empty cone"
        return out
    R = np.array(R)
    q = np.einsum("ij,jk,ik->i", R, J, R)
    if (q > tol).any():
        out["reason"] = "spacelike ray (%d of %d)" % (int((q > tol).sum()), len(R))
        return out
    orient = set((R[:, -1] > 0).tolist())
    if len(orient) != 1:
        out["reason"] = "mixed orientation"
        return out
    out["n_rays"] = len(R)
    out["n_ideal"] = int((np.abs(q) <= tol).sum())
    out["compact"] = out["n_ideal"] == 0
    tight = np.abs(R @ A.T) < 1e-6  # (rays, facets)
    # facet non-redundancy: rays on facet span rank d
    for i in range(n):
        Ri = R[tight[:, i]]
        if len(Ri) < d or np.linalg.matrix_rank(Ri, tol=1e-6) < d:
            out["reason"] = "redundant/degenerate facet %d" % i
            return out
    # ridge structure vs Gram
    for i in range(n):
        for j in range(i + 1, n):
            Rij = R[tight[:, i] & tight[:, j]]
            ridge = (
                len(Rij) >= d - 1 and np.linalg.matrix_rank(Rij, tol=1e-6) >= d - 1
                if len(Rij)
                else False
            )
            if d - 1 == 0:
                ridge = True
            adj = G[i, j] > -1 + 1e-9
            # WHY: in d=2 a ridge is a point, and two parallel sides meet at an ideal vertex = ridge.
            if d == 2 and abs(G[i, j] + 1) <= 1e-9:
                adj = True
            if ridge != adj:
                out["reason"] = "ridge mismatch facets (%d,%d): ridge=%s G=%.4f" % (
                    i,
                    j,
                    ridge,
                    G[i, j],
                )
                return out
    out["ok_polytope"] = True
    out["reason"] = "ok"
    if want_fvec:
        masks = []
        for i in range(n):
            m = 0
            for r in np.nonzero(tight[:, i])[0]:
                m |= 1 << int(r)
            masks.append(m)
        full = (1 << len(R)) - 1
        seen = {full: d}
        frontier = [full]
        while frontier:
            nxt = []
            for f in frontier:
                for m in masks:
                    g = f & m
                    if g and g not in seen:
                        pts = [r for r in range(len(R)) if g >> r & 1]
                        dim = np.linalg.matrix_rank(R[pts], tol=1e-6) - 1
                        seen[g] = dim
                        nxt.append(g)
            frontier = nxt
        fv = [0] * (d + 1)
        for g, dim in seen.items():
            if 0 <= dim <= d:
                fv[dim] += 1
        out["fvec"] = fv
        out["euler_ok"] = sum((-1) ** i * fv[i] for i in range(d + 1)) == 1
        out["facets_ok"] = fv[d - 1] == n
    return out
