"""S3 (premise on clean graphs) and S4 (detection, benign controls, decision rules C1-C4).

Frozen protocol: claim.md (commit 62660d1) + its Addendum. No thresholds are chosen here from data.
"""

from __future__ import annotations

import time

import corpus as C
import numpy as np
import rstat_lib as L

SEED = 20261014
N = 400
REPS = 100
CONSTRUCTIONS = ["knn5", "knn10", "knn20", "eps10"]
KNN = ["knn5", "knn10", "knn20"]
RATES = [0.005, 0.01, 0.05, 0.20]
ZONE = [0.005, 0.01, 0.05]  # working zone: poison share <= 5 %
POISON_MODELS = {
    "P_targeted": "B_growth",
    "P_bridge": "B_bridge",
}  # model -> matched benign control
ARMS = ["P_targeted", "P_bridge", "B_bridge", "B_growth"]
SIGNS = {"r": +1, "n_components": -1, "lambda2": +1, "modularity": -1, "centroid_cos": +1}
BASELINES = ["n_components", "lambda2", "modularity", "centroid_cos"]
CLEAN_SEEDS = range(0, REPS)
ARM_SEEDS = range(REPS, 2 * REPS)  # same base samples for every non-clean arm (matched design)


def build(X: np.ndarray, constr: str) -> np.ndarray:
    if constr.startswith("knn"):
        return L.knn_graph(X, int(constr[3:]))
    if constr == "eps10":
        return L.eps_graph(X, 10.0)
    if constr == "dense":
        return L.dense_cosine_graph(X)
    raise ValueError(constr)


def make_sample(D: dict, seed: int, kind: str | None = None, m: int = 0) -> np.ndarray:
    """N base chunks; if m>0, m random positions are REPLACED by poison/benign/held-out vectors.

    The rng stream is identical across arms for the same seed, so base sample and positions are
    matched between arms (the draw order below must not change).
    """
    rng = np.random.default_rng(SEED * 1000 + seed)
    idx = rng.choice(D["base"], size=N, replace=False)
    Xs = D["X"][idx].copy()
    if m:
        pos = rng.choice(N, size=m, replace=False)
        if kind == "B_growth":
            src = D["X"][rng.choice(D["held"], size=m, replace=False)]
        else:
            src = D[f"E_{kind}"][rng.choice(C.POISON_POOL, size=m, replace=False)]
        Xs[pos] = src
    return Xs


def record(Xs: np.ndarray, constr: str, baselines: bool = False) -> dict:
    A = build(Xs, constr)
    st = L.graph_stats(A)
    st["r"] = st.pop("r_mean")
    if baselines:
        st["modularity"] = L.modularity_louvain(A, seed=0)
        st["centroid_cos"] = L.centroid_cosine(Xs)
    return st


# ----------------------------------------------------------------------- S3 ----
def s3_corpus(name: str) -> dict:
    D = C.load(name)
    out = {}
    for g in [*CONSTRUCTIONS, "dense"]:
        recs = [record(make_sample(D, s), g) for s in CLEAN_SEEDS]
        ok = [x for x in recs if not x["excluded"]]
        r = np.array([x["r"] for x in ok])
        ncomp = np.array([x["n_components"] for x in recs])
        out[g] = {
            "mean_r": float(r.mean()) if len(r) else float("nan"),
            "sd_r": float(r.std(ddof=1)) if len(r) > 1 else float("nan"),
            "n_graphs": len(recs),
            "n_excluded_degenerate": len(recs) - len(ok),
            "mean_n_components": float(ncomp.mean()),
            "share_graphs_ge2_components": float((ncomp >= 2).mean()),
            "mean_lambda2": float(np.mean([x["lambda2"] for x in recs])),
            "corr_r_vs_n_components": (
                float(np.corrcoef(r, [x["n_components"] for x in ok])[0, 1])
                if len(r) > 2 and np.ptp([x["n_components"] for x in ok]) > 0
                else None
            ),
        }
    return out


def s3_verdict(per_corpus: dict) -> dict:
    flags = {}
    for c, res in per_corpus.items():
        m = {g: res[g]["mean_r"] for g in CONSTRUCTIONS}
        # a construction whose graphs were ALL excluded (mean_r = NaN) is "not evaluable", never
        # silently "not near Poisson" (skeptic finding 2026-10-14); it cannot satisfy P1.
        evaluable = {g: bool(np.isfinite(m[g])) for g in CONSTRUCTIONS}
        p1 = any(evaluable[g] and abs(m[g] - L.POISSON) <= 0.05 for g in CONSTRUCTIONS)
        knn_vals = [m[g] for g in KNN]
        spread = float(max(knn_vals) - min(knn_vals))
        flags[c] = {
            "P1_some_construction_near_poisson": bool(p1),
            "constructions_not_evaluable": [g for g in CONSTRUCTIONS if not evaluable[g]],
            "knn_spread": spread,
            "P2_spread_le_0.05": bool(spread <= 0.05),
        }
        flags[c]["both"] = bool(p1 and flags[c]["P2_spread_le_0.05"])
    holds = sum(f["both"] for f in flags.values()) >= 2
    return {
        "per_corpus": flags,
        "PREMISE_HOLDS": bool(holds),
        "verdict": "PREMISE_HOLDS" if holds else "PREMISE_KILLED",
    }


# ----------------------------------------------------------------------- S4 ----
def auroc_ci(pos, neg, n_boot: int = 2000, seed: int = 0) -> list[float]:
    rng = np.random.default_rng(seed)
    pos, neg = np.asarray(pos), np.asarray(neg)
    vals = [
        L.auroc(pos[rng.integers(0, len(pos), len(pos))], neg[rng.integers(0, len(neg), len(neg))])
        for _ in range(n_boot)
    ]
    return [float(x) for x in np.percentile(vals, [2.5, 97.5])]


def _arrays(recs: list[dict]) -> dict:
    return {k: np.array([x[k] for x in recs], dtype=float) for k in SIGNS}


def s4_corpus(name: str, constr: str = "knn10") -> dict:
    D = C.load(name)
    t0 = time.time()
    clean = [record(make_sample(D, s), constr, baselines=True) for s in CLEAN_SEEDS]
    arms: dict = {}
    for kind in ARMS:
        for rate in RATES:
            m = round(rate * N)
            arms[(kind, rate)] = [
                record(make_sample(D, s, kind, m), constr, baselines=True) for s in ARM_SEEDS
            ]
        print(f"  [{name}] {kind} done ({time.time() - t0:.0f}s)", flush=True)

    def keep(recs):  # graph-level exclusion (degenerate), applied to every detector alike
        return [x for x in recs if not x["excluded"]]

    cl = keep(clean)
    cl_a = _arrays(cl)
    thr = float(np.percentile(cl_a["r"], 95))  # alarm threshold: FPR = 5 % on clean graphs
    out = {
        "construction": constr,
        "n_clean_used": len(cl),
        "n_clean_excluded": len(clean) - len(cl),
        "alarm_threshold_r_p95_clean": thr,
        "clean_r_mean": float(cl_a["r"].mean()),
        "clean_n_components_mean": float(cl_a["n_components"].mean()),
        "arms": {},
    }
    raw = {"clean": {k: v.tolist() for k, v in cl_a.items()}}
    for (kind, rate), recs in arms.items():
        ok = keep(recs)
        a = _arrays(ok)
        key = f"{kind}@{rate}"
        raw[key] = {k: v.tolist() for k, v in a.items()}
        res = L.bootstrap_delta_auc(a, cl_a, SIGNS, "r", BASELINES, n_boot=2000, seed=11)
        res.update(
            {
                "n_used": len(ok),
                "n_excluded": len(recs) - len(ok),
                "mean_r": float(a["r"].mean()),
                "mean_n_components": float(a["n_components"].mean()),
                "tpr_or_fpr_at_clean_p95": float((a["r"] > thr).mean()),
            }
        )
        out["arms"][key] = res
    # C3: poison vs MATCHED BENIGN insertion (same positions, same rate)
    for model, benign in POISON_MODELS.items():
        for rate in RATES:
            p = np.array([x["r"] for x in keep(arms[(model, rate)])])
            b = np.array([x["r"] for x in keep(arms[(benign, rate)])])
            out["arms"][f"{model}@{rate}"]["auc_vs_matched_benign"] = {
                "benign": benign,
                "auc": L.auroc(p, b),
                "ci": auroc_ci(p, b),
            }
    out["elapsed_s"] = time.time() - t0
    return {"summary": out, "raw": raw}


def s4_decide(per_corpus: dict, premise_holds: bool) -> dict:
    """Apply claim.md decision rules C1-C4 (lenient reading of 'm <= 5 %': ANY rate in the zone)."""
    rep: dict = {"C1_premise": premise_holds, "models": {}}
    for model in POISON_MODELS:
        per_c = {}
        for c, res in per_corpus.items():
            rows = {}
            for rate in ZONE:
                a = res["arms"][f"{model}@{rate}"]
                lo, hi_max = a[
                    "delta_auc_vs_max_ci"
                ]  # conservative side: used for superiority (C2)
                hi = a["delta_auc_vs_best_point_ci"][
                    1
                ]  # fixed baseline: used for 'CI excludes MCID'
                c2 = bool(a["delta_auc"] >= 0.05 and lo > 0)
                c3 = bool(a["auc_vs_matched_benign"]["auc"] - 0.5 >= 0.10)
                # claim.md C4: FPR of the alarm on B-growth (benign memory growth), for BOTH models;
                # (an earlier version of this line used the matched-structure control by mistake)
                ben = res["arms"][f"B_growth@{rate}"]
                c4 = bool(
                    a["tpr_or_fpr_at_clean_p95"] >= 0.5 and ben["tpr_or_fpr_at_clean_p95"] <= 0.15
                )
                rows[str(rate)] = {
                    "delta_auc": a["delta_auc"],
                    "ci_vs_max_baseline": [lo, hi_max],
                    "ci_vs_fixed_best_baseline": a["delta_auc_vs_best_point_ci"],
                    "C2": c2,
                    "C3": c3,
                    "C4": c4,
                    "all": bool(c2 and c3 and c4),
                    "ci_excludes_mcid": bool(hi < 0.05),
                }
            top = res["arms"][f"{model}@0.2"]
            per_c[c] = {
                "zone": rows,
                "any_all": any(r["all"] for r in rows.values()),
                "strict_all": all(r["all"] for r in rows.values()),  # A1.4 strict reading (report)
                "any_C2": any(r["C2"] for r in rows.values()),
                "only_at_20pct": bool(
                    not any(r["C2"] for r in rows.values())
                    and top["delta_auc"] >= 0.05
                    and top["delta_auc_vs_max_ci"][0] > 0
                ),
                "ci_excludes_mcid_all_zone": all(r["ci_excludes_mcid"] for r in rows.values()),
            }
        rep["models"][model] = {
            "per_corpus": per_c,
            "passes_C2_C3_C4_on_ge2_corpora": bool(sum(v["any_all"] for v in per_c.values()) >= 2),
            "passes_strict_on_ge2_corpora": bool(sum(v["strict_all"] for v in per_c.values()) >= 2),
            "only_at_20pct_on_ge2": bool(sum(v["only_at_20pct"] for v in per_c.values()) >= 2),
            "ci_excludes_mcid_on_ge2": bool(
                sum(v["ci_excludes_mcid_all_zone"] for v in per_c.values()) >= 2
            ),
        }
    ms = rep["models"]
    # S4 judged on its own, as if the premise held (C1 is a separate, earlier gate).
    confirmed_alone = any(m["passes_C2_C3_C4_on_ge2_corpora"] for m in ms.values())
    killed_alone = any(m["only_at_20pct_on_ge2"] for m in ms.values()) or all(
        m["ci_excludes_mcid_on_ge2"] for m in ms.values()
    )
    if confirmed_alone:
        s4_alone = "CONFIRMED"
    elif killed_alone:
        s4_alone = "KILLED"
    else:
        s4_alone = "LEAD"  # default bucket of the frozen rule = inconclusive, NOT positive evidence
    rep["verdict_s4_alone"] = s4_alone
    if premise_holds:
        rep["verdict_final"] = s4_alone
        rep["exploratory_cap"] = None
    else:
        # C1 failed: the Syn-H1 formulation is KILLED (claim.md). S4 then only answers an
        # exploratory sub-question and can never exceed LEAD.
        rep["verdict_final"] = "KILLED"
        rep["exploratory_s4_outcome_capped"] = "LEAD" if s4_alone == "CONFIRMED" else s4_alone
        rep["exploratory_cap"] = "premise killed -> S4 is EXPLORATORY; maximum verdict LEAD"
    rep["verdict_raw"] = rep["verdict_final"]  # kept for backward compatibility of s4.json readers
    return rep


# ------------------------------------------------- E1 (EXPLORATORY, post-S3) -----
def e1_sparse_knn(name: str, ks: tuple = (2, 3)) -> dict:
    """Exploratory robustness of the S3 kill: are even sparser kNN graphs Poisson-like?
    Not part of the pre-registered rule; cannot rescue or change the S3 verdict."""
    D = C.load(name)
    out = {}
    for k in ks:
        recs = [record(make_sample(D, s), f"knn{k}") for s in CLEAN_SEEDS]
        ok = [x for x in recs if not x["excluded"]]
        r = np.array([x["r"] for x in ok])
        out[f"knn{k}"] = {
            "mean_r": float(r.mean()) if len(r) else float("nan"),
            "n_excluded_degenerate": len(recs) - len(ok),
            "mean_n_components": float(np.mean([x["n_components"] for x in recs])),
            "mean_frac_degenerate": float(np.mean([x["frac_degenerate"] for x in recs])),
        }
    return out


# --------------------------------------- PC: positive control for the S3 pipeline ---
def s3_positive_control(name: str, reps: int = 30, groups: int = 4, k: int = 10) -> dict:
    """Real embeddings, artificially separated into `groups` blocks (extra orthogonal coordinate).

    Known-good input for the S3 pipeline: the graph must split into ~`groups` components and the
    statistic must move to the Poisson-like value. If it did not, 'all clean graphs are GOE' could
    be a graph-construction bug rather than a property of real memory graphs.
    """
    D = C.load(name)
    mean_norm = float(np.linalg.norm(D["X"], axis=1).mean())
    vals, comps = [], []
    per = N // groups
    for s in range(reps):
        rng = np.random.default_rng(SEED * 7 + s)
        idx = rng.choice(D["base"], size=N, replace=False)
        X = D["X"][idx]
        extra = np.zeros((N, groups))
        for g in range(groups):
            extra[g * per : (g + 1) * per, g] = 2.0 * mean_norm
        st = L.graph_stats(L.knn_graph(np.hstack([X, extra]), k))
        if not st["excluded"]:
            vals.append(st["r_mean"])
        comps.append(st["n_components"])
    return {
        "mean_r": float(np.mean(vals)),
        "sd_r": float(np.std(vals, ddof=1)),
        "n_used": len(vals),
        "mean_n_components": float(np.mean(comps)),
        "near_poisson_pm_0.05": bool(abs(np.mean(vals) - L.POISSON) <= 0.05),
    }


# ------------------------------- S4-PC: positive control for <r~> inside S4 (post-hoc) ---
def s4_positive_control(name: str, rates=(0.01, 0.05, 0.20), constr: str = "knn10") -> dict:
    """Inserted vectors forced into their OWN component (extra orthogonal coordinate): the one
    known mechanism that moves <r~> (S2/PC). Calibrates how much structural change <r~> needs before
    it responds at all. Direction chosen post hoc (disconnection LOWERS r), so AUROCs are reported
    with sign -1 for r and lambda2, +1 for #components. Exploratory; not part of the verdict."""
    D = C.load(name)
    off = 2.0 * float(np.linalg.norm(D["X"], axis=1).mean())

    def aug(Xs, mask):
        col = np.zeros((len(Xs), 1))
        col[mask, 0] = off
        return np.hstack([Xs, col])

    def rec(Xs, mask):
        st = L.graph_stats(build(aug(Xs, mask), constr))
        return st

    clean = [rec(make_sample(D, s), np.zeros(N, bool)) for s in CLEAN_SEEDS]
    cl = [x for x in clean if not x["excluded"]]
    out = {"clean_mean_r": float(np.mean([x["r_mean"] for x in cl])), "arms": {}}
    sg = {"r_mean": -1, "lambda2": -1, "n_components": +1}
    for rate in rates:
        m = round(rate * N)
        recs = []
        for s in ARM_SEEDS:
            rng = np.random.default_rng(SEED * 1000 + s)
            idx = rng.choice(D["base"], size=N, replace=False)
            Xs = D["X"][idx].copy()
            pos = rng.choice(N, size=m, replace=False)
            Xs[pos] = D["X"][rng.choice(D["held"], size=m, replace=False)]
            mask = np.zeros(N, bool)
            mask[pos] = True
            recs.append(rec(Xs, mask))
        ok = [x for x in recs if not x["excluded"]]
        out["arms"][f"DISC@{rate}"] = {
            "m": m,
            "n_used": len(ok),
            "n_excluded": len(recs) - len(ok),
            "mean_r": float(np.mean([x["r_mean"] for x in ok])),
            "mean_n_components": float(np.mean([x["n_components"] for x in ok])),
            "auc": {
                k: L.auroc(
                    sg[k] * np.array([x[k] for x in ok], float),
                    sg[k] * np.array([x[k] for x in cl], float),
                )
                for k in sg
            },
        }
    return out
