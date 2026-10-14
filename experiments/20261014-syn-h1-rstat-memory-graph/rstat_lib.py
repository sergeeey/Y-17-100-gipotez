"""Instrument for the Syn-H1 re-check: level-spacing-ratio statistic of graph Laplacians.

Pipeline contract (see claim.md, "Pre-registered protocol"):
  adjacency -> normalized Laplacian -> sorted spectrum -> bulk (central 90 %) -> r~ values
  degenerate spacings (<= TOL) are NOT silently filtered out of the sequence (the pasted code
  did that, which pairs non-adjacent levels): r~ is computed only on adjacent non-degenerate
  triples, and the degenerate fraction is reported; a graph with > DEGEN_LIMIT is excluded.
"""

from __future__ import annotations

import numpy as np
from scipy.sparse.csgraph import connected_components
from scipy.stats import norm, rankdata

POISSON = 2.0 * np.log(2.0) - 1.0  # 0.38629 exact
GOE_LARGE_N = 0.5307  # numerical large-N (Atas et al.); surmise 4-2*sqrt(3)=0.5359
GUE_LARGE_N = 0.5996  # numerical large-N; surmise 2*sqrt(3)/pi-1/2=0.6027

TOL = 1e-9
DEGEN_LIMIT = 0.05
MIN_RATIOS = 30


# ---------------------------------------------------------------- spectrum -----
def normalized_laplacian(A: np.ndarray) -> np.ndarray:
    """L = I - D^-1/2 A D^-1/2 (isolated vertices keep L_ii = 1, as in networkx)."""
    A = np.asarray(A, dtype=float)
    d = A.sum(axis=1)
    inv = np.zeros_like(d)
    nz = d > 0
    inv[nz] = d[nz] ** -0.5
    return np.eye(len(A)) - (inv[:, None] * A) * inv[None, :]


def spectrum(A: np.ndarray) -> np.ndarray:
    return np.linalg.eigvalsh(normalized_laplacian(A))


def level_ratio_stats(ev, cut: float = 0.05, tol: float = TOL):
    """Return (r_tilde array, degenerate fraction) on the central (1-2*cut) of the spectrum."""
    ev = np.sort(np.asarray(ev, dtype=float))
    n = len(ev)
    c = int(cut * n)
    bulk = ev[c : n - c] if c > 0 else ev
    s = np.diff(bulk)
    if len(s) < 3:
        return np.array([]), 1.0
    frac_deg = float((s <= tol).mean())
    a, b = s[:-1], s[1:]
    ok = (a > tol) & (b > tol)
    r = np.minimum(a[ok], b[ok]) / np.maximum(a[ok], b[ok])
    return r, frac_deg


def spectrum_stats(ev, cut: float = 0.05, tol: float = TOL) -> dict:
    """r~ record of one spectrum. An excluded spectrum (too degenerate OR too few ratios) has
    r_mean = NaN, so no consumer can average it in by accident (review finding, 2026-10-14)."""
    r, frac_deg = level_ratio_stats(ev, cut=cut, tol=tol)
    excluded = bool(frac_deg > DEGEN_LIMIT or len(r) < MIN_RATIOS)
    return {
        "r_mean": float("nan") if excluded else float(r.mean()),
        "n_ratios": len(r),
        "frac_degenerate": frac_deg,
        "excluded": excluded,
    }


def graph_stats(A: np.ndarray, cut: float = 0.05, tol: float = TOL) -> dict:
    """Per-graph record: r~ mean, degenerate fraction, components, lambda2 (+ exclusion flag)."""
    ev = spectrum(A)
    st = spectrum_stats(ev, cut=cut, tol=tol)
    st["n_components"] = int(connected_components(np.asarray(A) > 0, directed=False)[0])
    st["lambda2"] = float(np.sort(ev)[1])
    return st


# ------------------------------------------------------------ graph builders ---
def cosine_sim(X: np.ndarray) -> np.ndarray:
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    S = Xn @ Xn.T
    np.fill_diagonal(S, -np.inf)
    return S


def knn_graph(X: np.ndarray, k: int) -> np.ndarray:
    """Unweighted kNN graph, symmetrised by union."""
    S = cosine_sim(X)
    n = len(S)
    idx = np.argpartition(-S, k, axis=1)[:, :k]
    A = np.zeros((n, n))
    A[np.repeat(np.arange(n), k), idx.ravel()] = 1.0
    A = np.maximum(A, A.T)
    np.fill_diagonal(A, 0.0)
    return A


def eps_graph(X: np.ndarray, mean_degree: float = 10.0) -> np.ndarray:
    """Epsilon-threshold graph with threshold chosen per sample so the mean degree ~ mean_degree."""
    S = cosine_sim(X)
    n = len(S)
    iu = np.triu_indices(n, 1)
    vals = S[iu]
    m = round(n * mean_degree / 2.0)
    thr = np.partition(vals, -m)[-m]
    A = (S >= thr).astype(float)
    np.fill_diagonal(A, 0.0)
    return np.maximum(A, A.T)


def dense_cosine_graph(X: np.ndarray) -> np.ndarray:
    S = cosine_sim(X)
    W = np.clip(S, 0.0, None)
    np.fill_diagonal(W, 0.0)
    return W


# ------------------------------------------------------------------ baselines --
def modularity_louvain(A: np.ndarray, seed: int = 0) -> float:
    import networkx as nx

    G = nx.from_numpy_array((np.asarray(A) > 0).astype(float))
    comms = nx.community.louvain_communities(G, seed=seed)
    return float(nx.community.modularity(G, comms))


def centroid_cosine(X: np.ndarray) -> float:
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    c = Xn.mean(axis=0)
    c = c / np.linalg.norm(c)
    return float((Xn @ c).mean())


# ----------------------------------------------------------------- statistics --
def auroc(pos, neg) -> float:
    """P(pos > neg) + 0.5 P(pos == neg) via ranks."""
    pos = np.asarray(pos, dtype=float)
    neg = np.asarray(neg, dtype=float)
    n1, n2 = len(pos), len(neg)
    ranks = rankdata(np.concatenate([pos, neg]))
    return float((ranks[:n1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n2))


def bootstrap_delta_auc(
    pos: dict,
    neg: dict,
    signs: dict,
    primary: str,
    baselines: list,
    n_boot: int = 2000,
    seed: int = 0,
) -> dict:
    """AUROC per detector and paired bootstrap CIs of the primary detector's advantage.

    pos/neg: {detector: array over graphs}; signs: {detector: +1/-1} fixed in advance
    (+1 = larger value means poisoned). Resampling is over GRAPHS (never over r_i).

    Two CIs (review 2026-10-14): `delta_auc_vs_max_ci` uses max over RESAMPLED baselines. That max
    is biased upward, so the CI is shifted down: conservative for "primary beats baselines" (C2),
    ANTI-conservative for "CI excludes MCID". `delta_auc_vs_best_point_ci` holds the baseline
    chosen on the point estimate FIXED across resamples; it is the one used for the exclusion rule.
    """
    rng = np.random.default_rng(seed)
    n1 = len(next(iter(pos.values())))
    n2 = len(next(iter(neg.values())))
    names = [primary, *list(baselines)]

    def aucs(ip, ineg):
        return {nm: auroc(signs[nm] * pos[nm][ip], signs[nm] * neg[nm][ineg]) for nm in names}

    point = aucs(np.arange(n1), np.arange(n2))
    best_base = max(baselines, key=lambda b: point[b])
    deltas, deltas_fixed, per = [], [], {nm: [] for nm in names}
    for _ in range(n_boot):
        a = aucs(rng.integers(0, n1, n1), rng.integers(0, n2, n2))
        for nm in names:
            per[nm].append(a[nm])
        deltas.append(a[primary] - max(a[b] for b in baselines))
        deltas_fixed.append(a[primary] - a[best_base])
    lo, hi = np.percentile(deltas, [2.5, 97.5])
    lo_f, hi_f = np.percentile(deltas_fixed, [2.5, 97.5])
    return {
        "auc": point,
        "best_baseline": best_base,
        "delta_auc": point[primary] - point[best_base],
        "delta_auc_vs_max_ci": [float(lo), float(hi)],
        "delta_auc_vs_best_point_ci": [float(lo_f), float(hi_f)],
        "auc_ci": {nm: [float(x) for x in np.percentile(per[nm], [2.5, 97.5])] for nm in names},
        "n_pos": n1,
        "n_neg": n2,
    }


def hanley_mcneil_se(A: float, n1: int, n2: int) -> float:
    q1 = A / (2.0 - A)
    q2 = 2.0 * A * A / (1.0 + A)
    var = (A * (1 - A) + (n1 - 1) * (q1 - A * A) + (n2 - 1) * (q2 - A * A)) / (n1 * n2)
    return float(np.sqrt(var))


def mde_auc(A: float, n: int, alpha: float = 0.05, power: float = 0.8) -> float:
    """MDE for ONE AUROC (SE of a single AUC, Hanley-McNeil), per arm size n.

    This is the lower-bound proxy for a PAIRED comparison of two correlated detectors on the same
    graphs (the design actually used). For two INDEPENDENT AUCs use `mde_delta_auc_independent`."""
    return float((norm.ppf(1 - alpha / 2) + norm.ppf(power)) * hanley_mcneil_se(A, n, n))


def mde_delta_auc_independent(A: float, n: int, alpha: float = 0.05, power: float = 0.8) -> float:
    """MDE of a difference of two INDEPENDENT AUCs: SE_diff = sqrt(2) * SE (upper-bound proxy)."""
    return float(np.sqrt(2.0) * mde_auc(A, n, alpha, power))
