"""Family B (post-hoc robustness, NOT the pre-registered family): polynomial R of degree d<=3 with FREE constant term,
arbitrary (non-monotone) assignment of d+1 nodes (from lowest fine values incl. 0) to targets (lowest Q coarse values incl. 0).
Controls: gasket 4L2 with coarse spectrum shifted (R(0)=1) and flipped (R decreasing at 0)."""

import itertools
import json
import time

import numpy as np

from lib import cluster
from search import _nearest_dist

TOL = 1e-8


def polyval(a, x):  # a (...,d+1) increasing powers
    out = np.zeros(a.shape[:-1] + (x.shape[0],))
    xp = np.ones_like(x)
    for k in range(a.shape[-1]):
        out += a[..., k : k + 1] * xp
        xp = xp * x
    return out


def extend(a, f, c):
    d1 = len(a)
    for t in (1e-5, 1e-6, 1e-7, 1e-8, 1e-8):
        pred = polyval(a[None, :], f)[0]
        dist, _ = _nearest_dist(pred, c)
        M = dist <= t
        if M.sum() < d1 + 1:
            break
        _, idx = _nearest_dist(pred[M], c)
        V = np.vander(f[M], d1, increasing=True)
        a, *_ = np.linalg.lstsq(V, c[idx], rcond=None)
    pred = polyval(a[None, :], f)[0]
    dist, idx = _nearest_dist(pred, c)
    return a, dist <= TOL, idx


def search_relaxed(fine, coarse, d, P=None, Q=12, W=40, min_hits=5, top=40):
    f, c = fine, coarse  # include 0 deliberately
    P = min(P or d + 4, len(f))
    Q = min(Q, len(c))
    fw = f[: min(W, len(f))]
    nodes = f[:P]
    targ = np.concatenate([c[: Q // 2], c[-(Q - Q // 2) :]])  # both ends (R may be decreasing at 0)
    tt = np.array(list(itertools.product(range(Q), repeat=d + 1)))
    Tm = targ[tt]
    cands = []
    for ns in itertools.combinations(range(P), d + 1):
        x = nodes[list(ns)]
        V = np.vander(x, d + 1, increasing=True)
        Vinv = np.linalg.inv(V)
        a = Tm @ Vinv.T
        for s in range(0, len(a), 20000):
            ac = a[s : s + 20000]
            pred = polyval(ac, fw)
            dist, _ = _nearest_dist(pred.ravel(), c)
            hits = (dist.reshape(pred.shape) <= 1e-6).sum(axis=1)
            for i in np.nonzero(hits >= d + 1 + min_hits)[0]:
                a_i = ac[i]
                if np.ptp(polyval(a_i[None, :], fw)[0]) < 1e-3:  # constant-ish R: trivial
                    continue
                cands.append((int(hits[i]), a_i.copy()))
    cands.sort(key=lambda t: -t[0])
    best = None
    for h, a in cands[:top]:
        a2, M, idx = extend(a, f, c)
        # non-triviality: image must not collapse
        if len(set(idx[M].tolist())) < 0.5 * len(c) and M.sum() > 0.5 * len(f):
            continue
        if best is None or M.sum() > best[0]:
            best = (int(M.sum()), a2, len(set(idx[M].tolist())))
    if best is None:
        return {
            "d": d,
            "matched": 0,
            "frac": 0.0,
            "a": None,
            "n_fine": len(f),
            "n_cands": len(cands),
        }
    return {
        "d": d,
        "matched": best[0],
        "frac": best[0] / len(f),
        "coverage": best[2] / len(c),
        "a": [float(x) for x in best[1]],
        "n_fine": len(f),
        "n_cands": len(cands),
    }


def run(name, fev, cev, ds=(2, 3)):
    fv = cluster(fev, 1e-9)[0]
    cv = cluster(cev, 1e-9)[0]
    t = time.time()
    res = [search_relaxed(fv, cv, d) for d in ds]
    OUT[name] = res
    print(f"== {name} fine {len(fv)} coarse {len(cv)} {time.time() - t:.0f}s", flush=True)
    for r in res:
        a = None if r["a"] is None else [float(f"{x:.5g}") for x in r["a"]]
        print(
            f"   d={r['d']} matched={r['matched']}/{r['n_fine']} frac={r['frac']:.3f} cov={r.get('coverage', 0):.3f} cands={r['n_cands']} a(c0,c1,..)={a}",
            flush=True,
        )


OUT = {}
if __name__ == "__main__":
    G = np.load("gasket_4L2_spectra.npz")
    g5, g6 = G["L5"], G["L6"]
    run("CTRL_B1_gasket_shifted(R(0)=1)", g6, g5 + 1.0)
    run("CTRL_B2_gasket_flipped(R decreasing)", g6, 7.0 - g5)
    rng = np.random.default_rng(7)
    run("NEG_B_jittered_gasket", g6 * (1 + 1e-4 * rng.standard_normal(len(g6))), g5)
    for kind in ("L1", "L2"):
        S = np.load(f"carpet_spectra_{kind}.npz")
        for n in (2, 3):
            run(f"carpet_{kind}_{n}to{n + 1}", S[f"n{n + 1}"], S[f"n{n}"])
    json.dump(OUT, open("relaxed_result.json", "w"), indent=1, default=float)
