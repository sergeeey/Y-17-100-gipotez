# ruff: noqa
"""Skeptic tests T3/T4/T6 on the embedding cache (npz only; the *_texts.json files are NOT opened).

Run (PowerShell):
  $env:SYNH1_CACHE = "<cache dir>"
  python skeptic_synh1_emb.py "<D>"
"""

import sys
from pathlib import Path

import numpy as np
from scipy.sparse.csgraph import connected_components

D = Path(sys.argv[1])
sys.path.insert(0, str(D))
import corpus as C  # noqa: E402  (reads SYNH1_CACHE)
import detect as DT  # noqa: E402
import rstat_lib as L  # noqa: E402

REPS = 30


def r_raw(A):
    """r~ on non-degenerate adjacent triples, NO exclusion rule (diagnostic only)."""
    r, fd = L.level_ratio_stats(L.spectrum(A))
    return (float(r.mean()) if len(r) else float("nan")), fd


def giant(A):
    _, lab = connected_components(A > 0, directed=False)
    g = np.bincount(lab).argmax()
    ix = np.where(lab == g)[0]
    return A[np.ix_(ix, ix)]


def mutual_knn(X, k):
    A = L.knn_graph(X, k)  # union
    S = L.cosine_sim(X)
    idx = np.argpartition(-S, k, axis=1)[:, :k]
    B = np.zeros_like(A)
    B[np.repeat(np.arange(len(X)), k), idx.ravel()] = 1.0
    return B * B.T  # intersection


for name in ("C1", "C2", "C3"):
    Dd = C.load(name)
    rows = {
        k: []
        for k in (
            "eps_raw",
            "eps_fd",
            "eps_iso",
            "eps_giant_n",
            "eps_giant_r",
            "knn10_centered",
            "mutual10_raw",
            "mutual10_ncomp",
            "gauss_knn10",
            "colshuf_knn10",
        )
    }
    rng = np.random.default_rng(123)
    for s in range(REPS):
        X = DT.make_sample(Dd, s)
        A = L.eps_graph(X, 10.0)
        r, fd = r_raw(A)
        rows["eps_raw"].append(r)
        rows["eps_fd"].append(fd)
        rows["eps_iso"].append(float((A.sum(1) == 0).mean()))
        G = giant(A)
        rows["eps_giant_n"].append(len(G))
        rows["eps_giant_r"].append(L.spectrum_stats(L.spectrum(G))["r_mean"])
        Xc = X - X.mean(0)
        rows["knn10_centered"].append(L.graph_stats(L.knn_graph(Xc, 10))["r_mean"])
        M = mutual_knn(X, 10)
        rm, _ = r_raw(M)
        rows["mutual10_raw"].append(rm)
        rows["mutual10_ncomp"].append(connected_components(M > 0, directed=False)[0])
        Z = rng.standard_normal(X.shape)
        rows["gauss_knn10"].append(L.graph_stats(L.knn_graph(Z, 10))["r_mean"])
        Xs = np.column_stack([rng.permutation(X[:, j]) for j in range(X.shape[1])])
        rows["colshuf_knn10"].append(L.graph_stats(L.knn_graph(Xs, 10))["r_mean"])
    print(name, {k: round(float(np.nanmean(v)), 4) for k, v in rows.items()})

# T6: are P_bridge[i] and B_bridge[i] the same three source chunks (item-level match)?
for name in ("C1", "C2", "C3"):
    Dd = C.load(name)
    P = Dd["E_P_bridge"] / np.linalg.norm(Dd["E_P_bridge"], axis=1, keepdims=True)
    B = Dd["E_B_bridge"] / np.linalg.norm(Dd["E_B_bridge"], axis=1, keepdims=True)
    same = float(np.mean(np.sum(P * B, axis=1)))
    shifted = float(np.mean(np.sum(P * np.roll(B, 1, axis=0), axis=1)))
    print(
        name,
        "cos(P_bridge[i],B_bridge[i]) =",
        round(same, 4),
        "vs cos(P_bridge[i],B_bridge[i-1]) =",
        round(shifted, 4),
        "(equal => NOT item-matched)",
    )
