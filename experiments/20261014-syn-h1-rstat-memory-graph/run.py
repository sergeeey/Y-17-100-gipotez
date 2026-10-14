# ruff: noqa: E501
"""Syn-H1 re-check driver.  Usage:  python run.py s2 | prep | s3 | s4
Protocol and decision rules are frozen in claim.md (commit 62660d1). Deviations -> decision.md.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import networkx as nx
import numpy as np
import rstat_lib as L
from scipy.stats import mannwhitneyu

HERE = Path(__file__).resolve().parent
METRICS = Path(os.environ.get("SYNH1_METRICS", HERE / "metrics"))  # A3: separate dir for the Qwen run
SEED = 20261014
N = 400
CORPUS_NAMES = ("C1", "C2", "C3")


def _dump(name: str, obj: dict) -> None:
    METRICS.mkdir(exist_ok=True)
    (METRICS / f"{name}.json").write_text(
        json.dumps(obj, indent=2, default=float), encoding="utf-8"
    )


# ---------------------------------------------------------------- generators ---
def er_graph(n: int, p: float, rng) -> np.ndarray:
    U = np.triu(rng.random((n, n)) < p, 1)
    return (U | U.T).astype(float)


def sbm_graph(n: int, m: int, pin: float, pout: float, rng) -> np.ndarray:
    blk = np.repeat(np.arange(m), n // m)
    P = np.where(blk[:, None] == blk[None, :], pin, pout)
    U = np.triu(rng.random((n, n)) < P, 1)
    return (U | U.T).astype(float)


def pasted_style_r(ev, cut: float = 0.05) -> float:
    """The pasted report's computation: drop tiny spacings from the SEQUENCE, then ratios."""
    ev = np.sort(ev)
    c = int(cut * len(ev))
    s = np.diff(ev[c : len(ev) - c])
    s = s[s > 1e-12]
    r = np.minimum(s[:-1], s[1:]) / np.maximum(s[:-1], s[1:])
    return float(r.mean())


def _mean_sd(vals) -> dict:
    v = np.asarray([x for x in vals if np.isfinite(x)], dtype=float)
    return {"mean": float(v.mean()), "sd": float(v.std(ddof=1)), "n": len(v)}


# -------------------------------------------------------------------- S2 -------
def s2() -> dict:
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    out: dict = {"seed": SEED, "N": N}

    # A. reference spectra (positive controls for the statistic itself)
    ref = {"poisson": [], "goe": [], "gue": []}
    for _ in range(100):
        a = rng.standard_normal((N, N))
        ref["goe"].append(L.level_ratio_stats(np.linalg.eigvalsh((a + a.T) / 2))[0].mean())
        b = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
        ref["gue"].append(L.level_ratio_stats(np.linalg.eigvalsh((b + b.conj().T) / 2))[0].mean())
        ref["poisson"].append(L.level_ratio_stats(np.sort(rng.random(N)))[0].mean())
    out["reference_spectra"] = {k: _mean_sd(v) for k, v in ref.items()}
    out["reference_constants"] = {
        "poisson": L.POISSON,
        "goe_large_n": L.GOE_LARGE_N,
        "gue_large_n": L.GUE_LARGE_N,
    }

    # B. ER graph -> GOE-like (pre-registered fit condition: within 0.02 of GOE large-N)
    er = [L.graph_stats(er_graph(N, 0.08, rng))["r_mean"] for _ in range(30)]
    out["er_p0.08"] = _mean_sd(er)
    out["er_fit_ok"] = bool(abs(out["er_p0.08"]["mean"] - L.GOE_LARGE_N) <= 0.02)

    # C. decoupled blocks -> Poisson-like (fit condition: within 0.03 of Poisson)
    blocks = [L.graph_stats(sbm_graph(N, 4, 0.32, 0.0, rng)) for _ in range(30)]
    out["blocks_m4_pout0"] = _mean_sd([b["r_mean"] for b in blocks])
    out["blocks_m4_pout0"]["n_components_mean"] = float(
        np.mean([b["n_components"] for b in blocks])
    )
    out["blocks_fit_ok"] = bool(abs(out["blocks_m4_pout0"]["mean"] - L.POISSON) <= 0.03)
    out["instrument_fit"] = bool(out["er_fit_ok"] and out["blocks_fit_ok"])

    # C2. weak coupling restores repulsion (the pasted SBM: p_in=0.15, p_out=0.001)
    weak = [L.graph_stats(sbm_graph(N, 4, 0.15, 0.001, rng)) for _ in range(30)]
    out["pasted_sbm_weak_coupling"] = _mean_sd([b["r_mean"] for b in weak])
    out["pasted_sbm_weak_coupling"]["n_components_mean"] = float(
        np.mean([b["n_components"] for b in weak])
    )

    # D. second Poisson control: regular structures (+ the pasted 'lattice 0.4006' claim)
    reg = {}
    for name, G in (
        ("grid20x20_open", nx.grid_2d_graph(20, 20)),
        ("torus20x20", nx.grid_2d_graph(20, 20, periodic=True)),
    ):
        A = nx.to_numpy_array(G)
        ev = L.spectrum(A)
        st = L.graph_stats(A)
        ev_s = np.sort(ev)
        c = int(0.05 * len(ev_s))
        sp = np.diff(ev_s[c : len(ev_s) - c])
        reg[name] = {
            **st,
            "frac_degenerate_tol1e-12": float((sp <= 1e-12).mean()),
            "frac_degenerate_tol1e-9": float((sp <= 1e-9).mean()),
            "r_pasted_style_filter": pasted_style_r(ev),
        }
    rr = [
        L.graph_stats(nx.to_numpy_array(nx.random_regular_graph(6, N, seed=int(s))))
        for s in range(30)
    ]
    reg["random_6_regular"] = _mean_sd([x["r_mean"] for x in rr])
    out["regular_structures"] = reg

    # E. unfolding / bulk-cut sensitivity
    sens = {}
    for cut in (0.0, 0.05, 0.10, 0.20):
        e = [
            L.level_ratio_stats(L.spectrum(er_graph(N, 0.08, rng)), cut=cut)[0].mean()
            for _ in range(15)
        ]
        bl = [
            L.level_ratio_stats(L.spectrum(sbm_graph(N, 4, 0.32, 0.0, rng)), cut=cut)[0].mean()
            for _ in range(15)
        ]
        sens[str(cut)] = {"er": float(np.mean(e)), "blocks_m4": float(np.mean(bl))}
    out["bulk_cut_sensitivity"] = sens

    # F. negative control: degree-preserving rewiring merges decoupled blocks
    rew = []
    for _ in range(20):
        A = sbm_graph(N, 4, 0.32, 0.0, rng)
        G = nx.from_numpy_array(A)
        nx.double_edge_swap(
            G, nswap=10 * G.number_of_edges(), max_tries=10**7, seed=int(rng.integers(1 << 30))
        )
        rew.append(L.graph_stats(nx.to_numpy_array(G)))
    out["rewired_blocks_negative_control"] = {
        **_mean_sd([x["r_mean"] for x in rew]),
        "n_components_mean": float(np.mean([x["n_components"] for x in rew])),
    }

    # G. pseudo-replication: MWU on r_i of ONE graph per arm vs graph-level permutation test
    pool_r = []
    pool_mean = []
    for _ in range(600):
        r, _fd = L.level_ratio_stats(L.spectrum(er_graph(N, 0.08, rng)))
        pool_r.append(r)
        pool_mean.append(r.mean())
    fp_mwu = np.mean(
        [mannwhitneyu(pool_r[2 * i], pool_r[2 * i + 1]).pvalue < 0.05 for i in range(300)]
    )
    lag1 = float(np.mean([np.corrcoef(r[:-1], r[1:])[0, 1] for r in pool_r[:100]]))
    fp_perm = []
    for rep in range(30):
        x = np.array(pool_mean[20 * rep : 20 * rep + 10])
        y = np.array(pool_mean[20 * rep + 10 : 20 * rep + 20])
        obs = abs(x.mean() - y.mean())
        z = np.concatenate([x, y])
        cnt = 0
        for _ in range(1000):
            rng.shuffle(z)
            cnt += abs(z[:10].mean() - z[10:].mean()) >= obs
        fp_perm.append((cnt + 1) / 1001 < 0.05)
    out["pseudo_replication"] = {
        "mwu_on_r_i_false_positive_rate_nominal_0.05": float(fp_mwu),
        "n_null_pairs_mwu": 300,
        "mean_lag1_autocorr_r_i": lag1,
        "graph_level_permutation_false_positive_rate_10v10": float(np.mean(fp_perm)),
        "n_null_pairs_perm": 30,
    }

    # H. Oracle adequacy (Step 2b): the evaluator = AUROC machinery, tested on known cases
    er_a = np.array([L.graph_stats(er_graph(N, 0.08, rng))["r_mean"] for _ in range(60)])
    er_b = np.array([L.graph_stats(er_graph(N, 0.08, rng))["r_mean"] for _ in range(60)])
    blk = np.array([L.graph_stats(sbm_graph(N, 4, 0.32, 0.0, rng))["r_mean"] for _ in range(60)])
    g = L.bootstrap_delta_auc(
        {"r": er_a, "b": er_a},
        {"r": blk, "b": blk},
        {"r": 1, "b": 1},
        "r",
        ["b"],
        n_boot=500,
        seed=1,
    )
    b = L.bootstrap_delta_auc(
        {"r": er_a, "b": er_a},
        {"r": er_b, "b": er_b},
        {"r": 1, "b": 1},
        "r",
        ["b"],
        n_boot=500,
        seed=2,
    )
    shuffled = rng.permutation(np.concatenate([er_a, blk]))
    flip = L.auroc(-er_a, -blk)
    shuf = L.auroc(shuffled[:60], shuffled[60:])
    g_ok = g["auc"]["r"] > 0.95
    b_ok = b["auc_ci"]["r"][0] <= 0.5 <= b["auc_ci"]["r"][1]
    flip_ok = abs(flip - (1.0 - g["auc"]["r"])) < 1e-9  # reversing the sign must mirror the AUROC
    shuf_ok = 0.35 <= shuf <= 0.65  # shuffled labels must sit near chance
    out["oracle_adequacy"] = {
        "G_positive_control_auc_ER_vs_blocks": g["auc"]["r"],
        "B_negative_control_auc_ER_vs_ER": b["auc"]["r"],
        "B_negative_control_ci": b["auc_ci"]["r"],
        "mutation_sign_flip_auc": flip,
        "mutation_label_shuffle_auc": shuf,
        "checks": {
            "G": bool(g_ok),
            "B": bool(b_ok),
            "sign_flip": bool(flip_ok),
            "shuffle": bool(shuf_ok),
        },
        "ok": bool(g_ok and b_ok and flip_ok and shuf_ok),
    }
    out["mde_check"] = {
        "hanley_mcneil_se_A0.75_n100": L.hanley_mcneil_se(0.75, 100, 100),
        "mde_single_auc_n100": L.mde_auc(0.75, 100),
        "mde_delta_auc_independent_n100": L.mde_delta_auc_independent(0.75, 100),
        "mde_single_auc_n30": L.mde_auc(0.75, 30),
        "note": "paired comparison of correlated detectors lies between single-AUC and independent values",
    }
    out["elapsed_s"] = time.time() - t0
    _dump("s2", out)
    return out


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "s2":
        res = s2()
        print(json.dumps(res, indent=2, default=float))
    elif cmd == "prep":  # needs SYNH1_CACHE (texts of the private vault stay outside the repo)
        import corpus as C

        _dump("prep", {c: C.prep(c) for c in CORPUS_NAMES})
    elif cmd == "s3":
        import detect as D

        per = {c: D.s3_corpus(c) for c in CORPUS_NAMES}
        verdict = D.s3_verdict(per)
        _dump("s3", {"per_corpus": per, "verdict": verdict})
        print(
            json.dumps(
                {c: {g: round(v["mean_r"], 4) for g, v in r.items()} for c, r in per.items()},
                indent=1,
            )
        )
        print(json.dumps(verdict, indent=1, default=float))
    elif cmd == "e1":
        import detect as D

        res = {c: D.e1_sparse_knn(c) for c in CORPUS_NAMES}
        _dump("e1_exploratory", res)
        print(json.dumps(res, indent=1, default=float))
    elif cmd == "pc":
        import detect as D

        res = {c: D.s3_positive_control(c) for c in CORPUS_NAMES}
        _dump("s3_positive_control", res)
        print(json.dumps(res, indent=1, default=float))
    elif cmd == "s4pc":
        import detect as D

        res = {c: D.s4_positive_control(c) for c in CORPUS_NAMES}
        _dump("s4_positive_control_posthoc", res)
        print(json.dumps(res, indent=1, default=float))
    elif cmd == "s3decide":
        import detect as D

        per = json.loads((METRICS / "s3.json").read_text(encoding="utf-8"))["per_corpus"]
        v = D.s3_verdict(per)
        _dump("s3_verdict_v2", v)
        print(json.dumps(v, indent=1, default=float))
    elif cmd == "s4decide":
        import detect as D

        per = json.loads((METRICS / "s4.json").read_text(encoding="utf-8"))["per_corpus"]
        prem = json.loads((METRICS / "s3_verdict_v2.json").read_text(encoding="utf-8"))[
            "PREMISE_HOLDS"
        ]
        d = D.s4_decide(per, prem)
        _dump("s4_decision_v2", d)
        print(
            json.dumps(
                {
                    "verdict_final": d["verdict_final"],
                    "models": {
                        m: {k: v for k, v in r.items() if k != "per_corpus"}
                        for m, r in d["models"].items()
                    },
                },
                indent=1,
            )
        )
    elif cmd == "s4":
        import detect as D

        premise = json.loads((METRICS / "s3.json").read_text(encoding="utf-8"))["verdict"][
            "PREMISE_HOLDS"
        ]
        per, raw = {}, {}
        for c in CORPUS_NAMES:
            r = D.s4_corpus(c)
            per[c], raw[c] = r["summary"], r["raw"]
        decision = D.s4_decide(per, premise)
        _dump("s4", {"per_corpus": per, "decision": decision})
        _dump("s4_raw", raw)
        print(json.dumps(decision, indent=1, default=float))
    else:
        raise SystemExit(f"unknown/unimplemented command: {cmd!r}")


if __name__ == "__main__":
    main()
