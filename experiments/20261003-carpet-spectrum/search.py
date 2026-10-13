"""Blind polynomial-decimation search (pre-registered family in claim.md).

Find R(z)=sum_{k=1..d} a_k z^k such that most distinct eigenvalues of the FINE level map (to 1e-8) onto
distinct eigenvalues of the COARSE level. Nodes: d values among the lowest P nonzero fine values; targets:
increasing d-subsets of the lowest Q nonzero coarse values; then iterative least-squares extension.
The search never uses the known answer for any control.
"""

import itertools
import numpy as np

TOL = 1e-8


def _nearest_dist(x, coarse):
    """distance from each x to nearest element of sorted array coarse, plus index."""
    j = np.searchsorted(coarse, x)
    j0 = np.clip(j - 1, 0, len(coarse) - 1)
    j1 = np.clip(j, 0, len(coarse) - 1)
    d0 = np.abs(x - coarse[j0])
    d1 = np.abs(x - coarse[j1])
    use1 = d1 < d0
    return np.where(use1, d1, d0), np.where(use1, j1, j0)


def _polyval0(a, x):
    """sum_{k=1..d} a[k-1] x^k, a shape (...,d), x shape (m,) -> (..., m)"""
    d = a.shape[-1]
    out = np.zeros(a.shape[:-1] + (x.shape[0],))
    xp = np.ones_like(x)
    for k in range(d):
        xp = xp * x
        out += a[..., k : k + 1] * xp
    return out


def _extend(a, fine, coarse, tols=(1e-5, 1e-6, 1e-7, 1e-8, 1e-8)):
    d = len(a)
    for t in tols:
        pred = _polyval0(a[None, :], fine)[0]
        dist, _ = _nearest_dist(pred, coarse)
        M = dist <= t
        if M.sum() < d + 1:
            break
        _, idx = _nearest_dist(pred[M], coarse)
        V = np.vander(fine[M], d + 1, increasing=True)[:, 1:]
        # weighted LS in relative scale
        sol, *_ = np.linalg.lstsq(V, coarse[idx], rcond=None)
        a = sol
    pred = _polyval0(a[None, :], fine)[0]
    dist, idx = _nearest_dist(pred, coarse)
    M = dist <= TOL
    return a, M, idx


def search(fine, coarse, d, P=None, Q=16, W=40, min_hits=5, top=40, verbose=False, exclude_identity=False):
    """fine, coarse: sorted DISTINCT eigenvalues (include 0). Returns dict with best candidate for degree d."""
    f = fine[fine > 1e-9]
    c = coarse[coarse > 1e-9]
    P = P or d + 3
    P = min(P, len(f))
    Q = min(Q, len(c))
    nodes_pool = f[:P]
    targ_pool = c[:Q]
    W = min(W, len(f))
    fw = f[:W]
    cands = []  # (hits, a)
    tcomb = np.array(list(itertools.combinations(range(Q), d)))
    Tm = targ_pool[tcomb]  # (nt, d)
    for ns in itertools.combinations(range(P), d):
        x = nodes_pool[list(ns)]
        V = np.vander(x, d + 1, increasing=True)[:, 1:]
        try:
            Vinv = np.linalg.inv(V)
        except np.linalg.LinAlgError:
            continue
        a = Tm @ Vinv.T  # (nt, d)
        if d >= 2:  # R must be increasing at the low end: a_1 > 0
            keep = a[:, 0] > 0
            a = a[keep]
        if exclude_identity:
            ident = (np.abs(a[:, 0] - 1) < 1e-6) & (np.abs(a[:, 1:]).max(axis=1) < 1e-6)
            a = a[~ident]
        # chunk evaluation
        for s in range(0, len(a), 20000):
            ac = a[s : s + 20000]
            pred = _polyval0(ac, fw)  # (nc, W)
            dist, _ = _nearest_dist(pred.ravel(), c)
            hits = (dist.reshape(pred.shape) <= 1e-6).sum(axis=1)
            sel = np.nonzero(hits >= d + min_hits)[0]
            for i in sel:
                cands.append((int(hits[i]), ac[i].copy()))
    cands.sort(key=lambda t: -t[0])
    best = None
    seen = 0
    for hits, a in cands[:top]:
        a2, M, idx = _extend(a, f, c)
        nm = int(M.sum())
        if best is None or nm > best["matched"]:
            best = {"matched": nm, "a": a2.tolist(), "stage1_hits": hits, "M": M, "idx": idx}
        seen += 1
    n_f = len(f)
    if best is None:
        return {
            "d": d,
            "n_candidates_stage1": len(cands),
            "matched": 0,
            "frac": 0.0,
            "coverage": 0.0,
            "a": None,
            "n_fine": n_f,
            "n_coarse": len(c),
        }
    unmatched = n_f - best["matched"]
    frac = best["matched"] / (n_f - min(5, unmatched))
    cov = len(set(best["idx"][best["M"]].tolist())) / len(c)
    return {
        "d": d,
        "n_candidates_stage1": len(cands),
        "matched": best["matched"],
        "frac": float(frac),
        "coverage": float(cov),
        "a": best["a"],
        "n_fine": n_f,
        "n_coarse": len(c),
        "stage1_hits": best["stage1_hits"],
    }


def search_all(fine, coarse, dmax=6, **kw):
    out = []
    for d in range(2, dmax + 1):
        out.append(search(fine, coarse, d, **kw))
    return out
