"""Regression tests for the Syn-H1 re-check instrument.

Experiment: experiments/20261014-syn-h1-rstat-memory-graph.

Fast (seconds). They pin: reference constants of the ratio statistic, degeneracy handling (the
pasted report silently filtered degenerate spacings and paired non-adjacent levels), AUROC maths,
graph builders, and the Hanley-McNeil MDE quoted in claim.md. Numerical regression only.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

EXP = Path(__file__).resolve().parents[1] / "experiments" / "20261014-syn-h1-rstat-memory-graph"
sys.path.insert(0, str(EXP))

import rstat_lib as L  # noqa: E402


def test_equally_spaced_levels_give_r_one():
    r, frac = L.level_ratio_stats(np.arange(200, dtype=float))
    assert frac == 0.0
    assert np.allclose(r, 1.0)


def test_poisson_and_goe_reference_values():
    rng = np.random.default_rng(0)
    pois = np.mean([L.level_ratio_stats(np.sort(rng.random(400)))[0].mean() for _ in range(40)])
    goe = []
    for _ in range(40):
        a = rng.standard_normal((300, 300))
        goe.append(L.level_ratio_stats(np.linalg.eigvalsh((a + a.T) / 2))[0].mean())
    assert abs(pois - L.POISSON) < 0.01
    assert abs(np.mean(goe) - L.GOE_LARGE_N) < 0.012


def test_degenerate_spacings_are_not_paired_across_gaps():
    # levels 0,1,1,2,3,4,...: a tie must not create a ratio between non-adjacent levels
    ev = np.array([0.0, 1.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    r, frac = L.level_ratio_stats(ev, cut=0.0)
    assert frac > 0.0
    # only triples with both spacings > tol count: spacings = [1,0,1,1,1,1,1,1,1] -> 6 valid pairs
    assert len(r) == 6
    assert np.allclose(r, 1.0)


def test_lattice_is_flagged_degenerate_and_excluded():
    import networkx as nx

    A = nx.to_numpy_array(nx.grid_2d_graph(20, 20))
    st = L.graph_stats(A)
    assert st["frac_degenerate"] > 0.3
    assert st["excluded"] is True
    assert np.isnan(st["r_mean"])


def test_auroc_perfect_chance_and_ties():
    assert L.auroc([3, 4, 5], [0, 1, 2]) == 1.0
    assert L.auroc([0, 1, 2], [3, 4, 5]) == 0.0
    assert L.auroc([1, 1], [1, 1]) == pytest.approx(0.5)
    rng = np.random.default_rng(1)
    x, y = rng.standard_normal(2000), rng.standard_normal(2000)
    assert abs(L.auroc(x, y) - 0.5) < 0.03


def test_auroc_known_gaussian_shift():
    rng = np.random.default_rng(2)
    pos, neg = rng.standard_normal(4000) + 1.0, rng.standard_normal(4000)
    assert abs(L.auroc(pos, neg) - 0.7602) < 0.02  # Phi(1/sqrt(2))


def test_bootstrap_ci_covers_true_delta_and_uses_signs():
    rng = np.random.default_rng(3)
    n = 120
    pos = {"r": rng.standard_normal(n) + 1.0, "b": rng.standard_normal(n)}
    neg = {"r": rng.standard_normal(n), "b": rng.standard_normal(n)}
    res = L.bootstrap_delta_auc(pos, neg, {"r": 1, "b": 1}, "r", ["b"], n_boot=300, seed=0)
    lo, hi = res["delta_auc_vs_max_ci"]
    assert lo < res["delta_auc"] < hi
    assert res["delta_auc"] > 0.15
    flipped = L.bootstrap_delta_auc(pos, neg, {"r": -1, "b": 1}, "r", ["b"], n_boot=100, seed=0)
    assert flipped["auc"]["r"] == pytest.approx(1 - res["auc"]["r"])


def test_knn_graph_symmetric_zero_diag_min_degree():
    rng = np.random.default_rng(4)
    X = rng.standard_normal((120, 16))
    A = L.knn_graph(X, 5)
    assert np.array_equal(A, A.T)
    assert np.all(np.diag(A) == 0)
    assert A.sum(axis=1).min() >= 5


def test_eps_graph_mean_degree_close_to_target():
    rng = np.random.default_rng(5)
    X = rng.standard_normal((200, 16))
    A = L.eps_graph(X, 10.0)
    assert abs(A.sum(axis=1).mean() - 10.0) < 1.0


def test_normalized_laplacian_spectrum_in_0_2_and_zero_mode():
    rng = np.random.default_rng(6)
    U = np.triu(rng.random((60, 60)) < 0.3, 1)
    A = (U | U.T).astype(float)
    ev = L.spectrum(A)
    assert ev.min() > -1e-10 and ev.max() < 2 + 1e-10
    assert abs(ev.min()) < 1e-10  # connected or not, lowest eigenvalue is 0


def test_mde_matches_claim_md():
    assert L.hanley_mcneil_se(0.75, 100, 100) == pytest.approx(0.0344, abs=0.0005)
    assert L.mde_auc(0.75, 100) == pytest.approx(
        0.0965, abs=0.002
    )  # claim.md says ~0.10 (MDE > MCID 0.05)
    assert L.mde_auc(0.75, 100) > 0.05


def test_degeneracy_rule_alone_excludes_and_nans_r_mean():
    # review 2026-10-14: this input trips ONLY the >5 % degeneracy rule (plenty of ratios remain)
    rng = np.random.default_rng(7)
    ev = np.sort(rng.random(400))
    ev[100:140] = ev[100]  # ~10 % tied spacings
    st = L.spectrum_stats(ev)
    assert st["n_ratios"] >= L.MIN_RATIOS
    assert st["frac_degenerate"] > L.DEGEN_LIMIT
    assert st["excluded"] is True
    assert np.isnan(st["r_mean"])


def test_clean_spectrum_is_not_excluded():
    rng = np.random.default_rng(8)
    st = L.spectrum_stats(np.sort(rng.random(400)))
    assert st["excluded"] is False
    assert np.isfinite(st["r_mean"])


def test_mde_independent_is_sqrt2_times_single_auc_mde():
    assert L.mde_delta_auc_independent(0.75, 100) == pytest.approx(
        np.sqrt(2) * L.mde_auc(0.75, 100)
    )
    assert L.mde_delta_auc_independent(0.75, 100) == pytest.approx(0.136, abs=0.003)


def test_bootstrap_returns_fixed_baseline_ci_that_is_not_below_max_ci():
    rng = np.random.default_rng(9)
    n = 100
    pos = {
        "r": rng.standard_normal(n) + 0.5,
        "b1": rng.standard_normal(n) + 0.5,
        "b2": rng.standard_normal(n) + 0.5,
    }
    neg = {k: rng.standard_normal(n) for k in pos}
    sg = {k: 1 for k in pos}
    res = L.bootstrap_delta_auc(pos, neg, sg, "r", ["b1", "b2"], n_boot=400, seed=0)
    # max over resampled baselines is biased upward => its CI sits lower than the fixed-baseline CI
    assert res["delta_auc_vs_max_ci"][1] <= res["delta_auc_vs_best_point_ci"][1] + 1e-12


# ---- detect.py (skeptic finding 10: decision code had no tests) ---------------------------
import detect as DT  # noqa: E402


def _fake_D(n_base=150, n_held=50, d=16, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n_base + n_held, d))
    return {
        "X": X,
        "base": np.arange(n_base),
        "held": np.arange(n_base, n_base + n_held),
        "E_P_targeted": rng.standard_normal((DT.C.POISON_POOL, d)) + 5.0,
        "E_P_bridge": rng.standard_normal((DT.C.POISON_POOL, d)) + 6.0,
        "E_B_bridge": rng.standard_normal((DT.C.POISON_POOL, d)) + 7.0,
    }


def test_make_sample_matched_design_same_positions_and_base_across_arms(monkeypatch):
    monkeypatch.setattr(DT, "N", 100)
    D = _fake_D()
    clean = DT.make_sample(D, 5)
    a = DT.make_sample(D, 5, "P_bridge", 7)
    b = DT.make_sample(D, 5, "B_growth", 7)
    changed_a = np.where(~np.all(a == clean, axis=1))[0]
    changed_b = np.where(~np.all(b == clean, axis=1))[0]
    assert len(changed_a) == 7 and len(changed_b) == 7
    assert np.array_equal(changed_a, changed_b)  # same positions replaced in every arm
    other = np.setdiff1d(np.arange(100), changed_a)
    assert np.array_equal(a[other], clean[other])  # untouched rows are the same base sample


def test_make_sample_different_seed_gives_different_base(monkeypatch):
    monkeypatch.setattr(DT, "N", 100)
    D = _fake_D()
    assert not np.array_equal(DT.make_sample(D, 1), DT.make_sample(D, 2))


def test_s3_verdict_marks_all_excluded_construction_not_evaluable():
    def corpus(r):
        return {g: {"mean_r": r.get(g, float("nan"))} for g in [*DT.CONSTRUCTIONS, "dense"]}

    near_goe = {"knn5": 0.53, "knn10": 0.53, "knn20": 0.53}  # eps10 -> NaN (all excluded)
    v = DT.s3_verdict({"C1": corpus(near_goe), "C2": corpus(near_goe), "C3": corpus(near_goe)})
    assert v["verdict"] == "PREMISE_KILLED"
    assert v["per_corpus"]["C1"]["constructions_not_evaluable"] == ["eps10"]
    assert v["per_corpus"]["C1"]["P1_some_construction_near_poisson"] is False


def test_s3_verdict_holds_only_when_poisson_like_and_stable_on_two_corpora():
    pois = {"knn5": 0.39, "knn10": 0.39, "knn20": 0.40, "eps10": 0.39}
    goe = {"knn5": 0.53, "knn10": 0.53, "knn20": 0.53, "eps10": 0.53}

    def corpus(r):
        return {g: {"mean_r": r[g]} for g in r} | {"dense": {"mean_r": 0.53}}

    assert DT.s3_verdict({"C1": corpus(pois), "C2": corpus(pois), "C3": corpus(goe)})[
        "PREMISE_HOLDS"
    ]
    assert not DT.s3_verdict({"C1": corpus(pois), "C2": corpus(goe), "C3": corpus(goe)})[
        "PREMISE_HOLDS"
    ]


def _arm(delta, lo_max, hi_fixed, tpr, auc_vs_benign=0.5):
    return {
        "delta_auc": delta,
        "delta_auc_vs_max_ci": [lo_max, hi_fixed],
        "delta_auc_vs_best_point_ci": [lo_max, hi_fixed],
        "tpr_or_fpr_at_clean_p95": tpr,
        "auc_vs_matched_benign": {"auc": auc_vs_benign},
    }


def test_s4_decide_c4_uses_b_growth_and_confirms_only_with_premise():
    arms = {}
    for model in DT.POISON_MODELS:
        for rate in DT.RATES:
            arms[f"{model}@{rate}"] = _arm(0.12, 0.03, 0.2, 0.8, auc_vs_benign=0.7)
    for rate in DT.RATES:
        arms[f"B_growth@{rate}"] = _arm(0, -0.1, 0.1, 0.05)
        arms[f"B_bridge@{rate}"] = _arm(0, -0.1, 0.1, 0.9)  # must be IGNORED by C4
    per = {c: {"arms": arms} for c in ("C1", "C2", "C3")}
    ok = DT.s4_decide(per, premise_holds=True)
    assert ok["verdict_final"] == "CONFIRMED"
    killed_premise = DT.s4_decide(per, premise_holds=False)
    assert killed_premise["verdict_final"] == "KILLED"  # C1 failed: formulation killed
    assert killed_premise["exploratory_s4_outcome_capped"] == "LEAD"  # S4 alone never above LEAD
    for rate in DT.RATES:  # now make benign GROWTH noisy: C4 must fail
        arms[f"B_growth@{rate}"] = _arm(0, -0.1, 0.1, 0.9)
    bad = DT.s4_decide(per, premise_holds=True)
    assert not bad["models"]["P_bridge"]["passes_C2_C3_C4_on_ge2_corpora"]


def test_s4_decide_kill_when_signal_only_at_20pct():
    arms = {}
    for model in DT.POISON_MODELS:
        for rate in DT.RATES:
            top = rate == 0.20
            arms[f"{model}@{rate}"] = _arm(0.2 if top else 0.0, 0.1 if top else -0.1, 0.3, 0.9)
    for rate in DT.RATES:
        arms[f"B_growth@{rate}"] = _arm(0, -0.1, 0.1, 0.05)
        arms[f"B_bridge@{rate}"] = _arm(0, -0.1, 0.1, 0.05)
    per = {c: {"arms": arms} for c in ("C1", "C2", "C3")}
    assert DT.s4_decide(per, premise_holds=True)["verdict_final"] == "KILLED"
