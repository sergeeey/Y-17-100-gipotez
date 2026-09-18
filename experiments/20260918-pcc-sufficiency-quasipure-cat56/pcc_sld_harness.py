"""H-CAT56-1 harness: PCC vs certified non-saturability for quasi-pure states.

DECISION RULE (corrected mid-experiment, see decision.md "Protocol correction"):
a counterexample is claimed ONLY from the exact, deterministic rank test -- Observation 2
of arXiv:2601.21801, `dim V_perp < d => the QCRB cannot be saturated`. No optimiser and
no constructive search is ever allowed to produce a negative verdict, because a failed
search cannot be distinguished from a non-existent measurement. This experiment's own
positive control measured that failure mode directly (`metrics/positive_control.json`).

A sample is a CANDIDATE counterexample iff all three hold:
  1. PCC holds WITH MARGIN (violation below 1e-2 x the pre-registered 1e-8 tolerance);
  2. `dim V_perp < d`;
  3. the rank deficiency is ROBUST -- identical rank across thresholds 1e-6..1e-12, the
     same rank from an independent Gram-eigenvalue route, and a singular-value gap > 1e4.
A candidate is CONFIRMED only after `reverify.py` rebuilds it along a second, independent
path. Zero candidates is reported as "no certified counterexample found under this
sampling distribution", NOT as evidence that PCC is sufficient -- the test is
one-directional.

Modes:
  --mode positive_control   Eq. (16) states ABOVE the Eq. (15) threshold, where Theorem 3
                            guarantees sufficiency. The harness must report PCC true and
                            NO certified counterexample. The constructive probe also runs
                            here, as the one place where its behaviour is informative.
  --mode negative_control   the PCC check fed independently drawn random Hermitian
                            matrices in place of real SLDs. Expect PCC false.
  --mode rank_detector      injected-error control: can the certified test fire at all?
  --mode main_search        the pre-registered N=200 search, up to two configurations.
  --mode extension          POST-REGISTRATION: same search over GENERIC quasi-pure states
                            (Yang arXiv:2405.00405 Eq. 12), the class the open question is
                            actually about.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pcc_core as pc
import pcc_sat as ps

METRICS = Path(__file__).parent / "metrics"

# Pre-registered (controls.md): N = 200 per configuration, at most 2 configurations,
# stop immediately on the first candidate counterexample.
N_PREREG = 200

# "PCC holds with margin": two decades inside the pre-registered 1e-8 tolerance.
PCC_MARGIN_TOL = pc.TOL_REL * 1e-2

# Configurations chosen by threshold_scan.py (metrics/threshold_scan.json), not by hand.
BIPARTITE_BELOW = [(2, 2, 2), (3, 2, 2)]  # (d_sys, rank, s) -> d = 4, then d = 6
BIPARTITE_ABOVE = (4, 2, 2)  # d = 8, n = 51 >= rhs 42 (margin 9)
GENERIC_BELOW = [(3, 2, 2), (4, 2, 2)]  # (d, rank, s)
# Re-run of the extension at configurations whose QFIM is NOT identically singular;
# see decision.md -- generic quasi-pure states with d - r = 1 have rank-1 QFIM under
# PCC, so the d=3 row of the first extension run is a degenerate configuration.
GENERIC_NONDEGENERATE = [(4, 2, 2), (5, 2, 3), (6, 2, 4)]


def _row(model: pc.Model, ana: pc.Analysis, sat: ps.SaturabilityResult) -> dict:
    pcc_margin = ana.pcc_violation < PCC_MARGIN_TOL
    certified = sat.outcome == "CERTIFIED_NON_SATURABLE_RANK"
    return {
        "label": model.label,
        "d": ana.d,
        "s": ana.s,
        "r": ana.rank,
        "sld_residual": ana.sld_residual,
        "pcc_violation": ana.pcc_violation,
        "pcc_holds": bool(ana.pcc_holds),
        "pcc_holds_with_margin": bool(pcc_margin),
        "trace_violation": ana.trace_violation,
        "dim_V": ana.dim_v,
        "dim_V_perp": ana.dim_v_perp,
        "dim_V_perp_minus_d": ana.dim_v_perp - ana.d,
        "r2_plus_1_bound": ana.rank**2 + 1,
        "rank_plateau": ana.rank_plateau,
        "gram_rank": ana.gram_rank,
        "rank_gap_ratio": ana.rank_gap_ratio,
        "rank_is_robust": bool(ana.rank_is_robust),
        "n": ana.n,
        "rhs_eq15": ana.rhs,
        "below_threshold": bool(ana.below_threshold),
        "qfim_min_eig": ana.qfim_min_eig,
        "qfim_rank": ana.qfim_rank,
        "qfim_full_rank": bool(ana.qfim_rank == ana.s),
        "verdict": sat.verdict,
        "outcome": sat.outcome,
        "test2_ran": sat.test2_ran,
        "test2_status": sat.test2_status,
        "test2_feasible": sat.test2_feasible,
        "test2_lp_slack": sat.test2_lp_slack,
        "test2_n_v_sampled": sat.test2_n_v_sampled,
        "test2_povm_size": sat.test2_povm_size,
        "test2_completeness_error": sat.test2_completeness_error,
        "test2_cfim_qfim_rel_gap": sat.test2_cfim_qfim_gap,
        "probe_ran": sat.probe_ran,
        "probe_constructed": sat.probe_constructed,
        "probe_lp_slack": sat.probe_lp_slack,
        "probe_povm_size": sat.probe_povm_size,
        "probe_completeness_error": sat.probe_completeness_error,
        "probe_cfim_qfim_rel_gap": sat.probe_cfim_qfim_gap,
        "candidate_counterexample": bool(pcc_margin and certified and ana.rank_is_robust),
        "detail": sat.detail,
    }


def _sample(kind: str, dims: tuple, rng: np.random.Generator, **kw) -> pc.Model | None:
    if kind == "bipartite":
        return pc.sample_bipartite_quasipure(*dims, rng, **kw)
    return pc.sample_generic_quasipure(*dims, rng, **kw)


def run_batch(
    kind: str,
    dims: tuple,
    n_samples: int,
    rng: np.random.Generator,
    run_probe: bool = False,
    run_test2: bool = False,
    probe_starts: int = 120,
    stop_on_candidate: bool = True,
    **sample_kw,
) -> dict:
    rows, t0, failed = [], time.time(), 0
    for _ in range(n_samples):
        model = _sample(kind, dims, rng, **sample_kw)
        if model is None:
            failed += 1
            continue
        ana = pc.analyse(model)
        sat = ps.saturability(
            ana, model, rng, run_probe=run_probe, run_test2=run_test2, n_starts=probe_starts
        )
        rows.append(_row(model, ana, sat))
        if stop_on_candidate and rows[-1]["candidate_counterexample"]:
            break
    return {
        "kind": kind,
        "dims": list(dims),
        "sample_kw": {k: bool(v) for k, v in sample_kw.items()},
        "requested": n_samples,
        "sampler_failures": failed,
        "completed": len(rows),
        "seconds": round(time.time() - t0, 2),
        "summary": summarise(rows),
        "rows": rows,
    }


def summarise(rows: list[dict]) -> dict:
    if not rows:
        return {"n": 0}
    verdicts: dict[str, int] = {}
    outcomes: dict[str, int] = {}
    for r in rows:
        verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
        outcomes[r["outcome"]] = outcomes.get(r["outcome"], 0) + 1
    probes = [r for r in rows if r["probe_ran"]]
    return {
        "n": len(rows),
        "pcc_true": sum(r["pcc_holds"] for r in rows),
        "pcc_true_with_margin": sum(r["pcc_holds_with_margin"] for r in rows),
        "below_threshold": sum(r["below_threshold"] for r in rows),
        "dim_V_values": sorted({r["dim_V"] for r in rows}),
        "dim_V_perp_values": sorted({r["dim_V_perp"] for r in rows}),
        "min_dim_V_perp_minus_d": min(r["dim_V_perp_minus_d"] for r in rows),
        "rank_robust_all": all(r["rank_is_robust"] for r in rows),
        "verdict_counts": verdicts,
        "outcome_counts": outcomes,
        "numerically_ambiguous": sum(
            r["verdict"] == "NUMERICALLY_AMBIGUOUS" for r in rows
        ),
        "test2_ran": sum(r["test2_ran"] for r in rows),
        "test2_feasible": sum(bool(r["test2_feasible"]) for r in rows),
        "test2_infeasible_on_sample": sum(
            r["test2_ran"] and r["test2_feasible"] is False for r in rows
        ),
        "test2_max_cfim_qfim_rel_gap": max(
            (r["test2_cfim_qfim_rel_gap"] for r in rows if r["test2_cfim_qfim_rel_gap"]),
            default=None,
        ),
        "candidate_counterexamples": sum(r["candidate_counterexample"] for r in rows),
        "max_sld_residual": max(r["sld_residual"] for r in rows),
        "max_pcc_violation": max(r["pcc_violation"] for r in rows),
        "max_trace_violation": max(r["trace_violation"] for r in rows),
        "min_qfim_eig": min(r["qfim_min_eig"] for r in rows),
        "qfim_full_rank_count": sum(r["qfim_full_rank"] for r in rows),
        "qfim_rank_values": sorted({r["qfim_rank"] for r in rows}),
        "probe_n": len(probes),
        "probe_constructed": sum(bool(r["probe_constructed"]) for r in probes),
        "probe_max_cfim_qfim_rel_gap": max(
            (r["probe_cfim_qfim_rel_gap"] for r in probes if r["probe_cfim_qfim_rel_gap"]),
            default=None,
        ),
    }


def mode_positive_control(rng: np.random.Generator, n: int) -> dict:
    batch = run_batch(
        "bipartite",
        BIPARTITE_ABOVE,
        n,
        rng,
        run_probe=True,
        run_test2=True,
        probe_starts=250,
        stop_on_candidate=False,
    )
    s = batch["summary"]
    batch["expected"] = (
        "Theorem 3 applies here, so: PCC true for every sample, none below threshold, "
        "and ZERO certified counterexamples. The constructive probe is informative only "
        "when it SUCCEEDS."
    )
    batch["pass"] = bool(
        s["n"] == n
        and s["pcc_true"] == n
        and s["below_threshold"] == 0
        and s["candidate_counterexamples"] == 0
        and s["verdict_counts"].get("NOT_EXCLUDED", 0) == n
    )
    batch["probe_false_negative_rate"] = (
        1.0 - s["probe_constructed"] / s["probe_n"] if s["probe_n"] else None
    )
    batch["probe_note"] = (
        "Every probe failure in this batch is a KNOWN false negative: Theorem 3 guarantees "
        "a saturating projective measurement exists here. This is the measured evidence "
        "that a search-based 'not saturable' verdict is unsound, and is why the main "
        "search uses the exact rank test instead."
    )
    return batch


def mode_negative_control(rng: np.random.Generator, n: int) -> dict:
    rows = []
    for _ in range(n):
        model = pc.sample_bipartite_quasipure(*BIPARTITE_BELOW[0], rng)
        if model is None:
            continue
        fake = [pc.random_hermitian(model.d, rng) for _ in range(model.s)]
        _, psis = pc.support_eigenvectors(model.rho, model.rank)
        scale = max(float(np.linalg.norm(lo, 2)) for lo in fake)
        worst = 0.0
        for i in range(model.s):
            for j in range(i + 1, model.s):
                comm = fake[i] @ fake[j] - fake[j] @ fake[i]
                worst = max(worst, float(np.max(np.abs(psis.conj().T @ comm @ psis))))
        v = worst / scale**2
        rows.append({"pcc_violation": v, "pcc_holds": v < pc.TOL_REL})
    frac = sum(r["pcc_holds"] for r in rows) / max(len(rows), 1)
    return {
        "mode": "negative_control",
        "n": len(rows),
        "pcc_true_fraction": frac,
        "min_pcc_violation": min(r["pcc_violation"] for r in rows),
        "median_pcc_violation": float(np.median([r["pcc_violation"] for r in rows])),
        "expected": "PCC false for essentially all unrelated random Hermitian matrices",
        "pass": bool(frac < 0.01),
    }


def mode_rank_detector(rng: np.random.Generator, n: int) -> dict:
    """Injected-error control: CAN the certified test fire at all?

    A test that cannot return YES on any input is not a test. One arm replaces `V` by a
    hand-built span of known dimension `d^2 - d + 1`, so `dim V_perp = d - 1 < d` by
    construction and Observation 2 MUST fire. The other builds `dim V = d^2 - d - 3`
    (`dim V_perp = d + 3 >= d`) and it must NOT fire.
    """
    rows = []
    for d in (3, 4, 5, 6):
        for target_dimv, should_fire in ((d * d - d + 1, True), (max(d * d - d - 3, 1), False)):
            for _ in range(n):
                basis = [pc.random_hermitian(d, rng) for _ in range(target_dimv)]
                vecs = np.array([pc.herm_to_real_vec(b) for b in basis])
                sv = np.linalg.svd(vecs, compute_uv=False)
                dim_v = int(np.sum(sv > sv[0] * pc.TOL_REL))
                fired = (d * d - dim_v) < d
                rows.append(
                    {
                        "d": d,
                        "target_dim_V": target_dimv,
                        "measured_dim_V": dim_v,
                        "dim_V_perp": d * d - dim_v,
                        "should_fire": should_fire,
                        "fired": bool(fired),
                        "ok": bool(fired == should_fire and dim_v == target_dimv),
                    }
                )
    return {
        "mode": "rank_detector",
        "n": len(rows),
        "all_ok": all(r["ok"] for r in rows),
        "fired_when_expected": sum(r["fired"] and r["should_fire"] for r in rows),
        "expected_fires": sum(r["should_fire"] for r in rows),
        "false_fires": sum(r["fired"] and not r["should_fire"] for r in rows),
        "pass": all(r["ok"] for r in rows),
        "rows": rows,
    }


def _search(
    kind: str,
    configs: list[tuple],
    rng: np.random.Generator,
    n: int,
    run_test2: bool = True,
) -> dict:
    batches = []
    for dims in configs:
        b = run_batch(kind, dims, n, rng, run_test2=run_test2)
        batches.append(b)
        if b["summary"]["candidate_counterexamples"]:
            break
    total = sum(b["summary"]["candidate_counterexamples"] for b in batches)
    return {
        "N": n,
        "configurations_run": len(batches),
        "candidate_counterexamples": total,
        "verdict": (
            "CANDIDATE_COUNTEREXAMPLE_FOUND" if total else "NO_CERTIFIED_COUNTEREXAMPLE_FOUND"
        ),
        "verdict_meaning": (
            "no counterexample was found via EITHER exact non-saturability test "
            "(Observation 2 rank test; End Matter completeness-feasibility) under this "
            "sampling distribution. Both are one-directional and the paper allows "
            "non-saturability for reasons outside them, so this is NOT evidence that "
            "PCC is sufficient and NOT a claim that these samples are saturable."
        ),
        "batches": batches,
    }


def mode_main_search(rng: np.random.Generator, n: int) -> dict:
    return {
        "mode": "main_search",
        "preregistered_N": N_PREREG,
        **_search("bipartite", BIPARTITE_BELOW, rng, n),
    }


def mode_extension(rng: np.random.Generator, n: int) -> dict:
    return {
        "mode": "extension_generic_quasipure",
        "note": "POST-REGISTRATION. claim.md pre-registered the Eq. (16) subclass, for "
        "which the paper's own End Matter already PROVES sufficiency via an LMCC "
        "construction. The open question is about GENERIC quasi-pure states "
        "(Yang arXiv:2405.00405 Eq. 12), which is what this mode samples.",
        **_search("generic", GENERIC_BELOW, rng, n),
    }


def mode_probe_check(rng: np.random.Generator, n: int) -> dict:
    """Measure the constructive probe's success rate where the answer is already known.

    For EVERY configuration here the paper proves a saturating measurement exists:
    `d = 4` and `d = 6` by the End Matter LMCC construction for Eq. (16) states, `d = 8`
    by that construction AND by Theorem 3 (it is above the Eq. (15) threshold). So every
    probe failure is a KNOWN false negative, and the measured rate is the evidence for
    this experiment's protocol correction: a search that cannot find a POVM is not
    evidence that none exists.
    """
    rows = []
    for dims in ((2, 2, 2), (3, 2, 2), (4, 2, 2)):
        b = run_batch(
            "bipartite", dims, n, rng, run_probe=True, probe_starts=300, stop_on_candidate=False
        )
        s = b["summary"]
        rows.append(
            {
                "dims": list(dims),
                "d": b["rows"][0]["d"],
                "dim_V_perp": s["dim_V_perp_values"],
                "above_eq15_threshold": all(not r["below_threshold"] for r in b["rows"]),
                "samples": s["n"],
                "probe_constructed": s["probe_constructed"],
                "probe_success_rate": s["probe_constructed"] / max(s["n"], 1),
                "max_cfim_qfim_rel_gap": s["probe_max_cfim_qfim_rel_gap"],
                "max_povm_completeness_error": max(
                    (r["probe_completeness_error"] for r in b["rows"] if r["probe_constructed"]),
                    default=None,
                ),
                "povm_sizes": sorted(
                    {r["probe_povm_size"] for r in b["rows"] if r["probe_constructed"]}
                ),
                "lp_slacks": [r["probe_lp_slack"] for r in b["rows"]],
                "seconds": b["seconds"],
            }
        )
    return {
        "mode": "probe_check",
        "rows": rows,
        "interpretation": (
            "Saturability is guaranteed by the paper at every configuration listed. Any "
            "row with probe_success_rate < 1 is a measured FALSE-NEGATIVE rate for the "
            "search-based route; the same code succeeds elsewhere, so it is a property "
            "of searching, not a bug."
        ),
        "probe_works_somewhere": any(r["probe_success_rate"] > 0.9 for r in rows),
        "probe_false_negative_somewhere": any(r["probe_success_rate"] < 0.1 for r in rows),
        "pass": (
            any(r["probe_success_rate"] > 0.9 for r in rows)
            and all(
                (r["max_cfim_qfim_rel_gap"] or 0.0) < 1e-6
                for r in rows
                if r["probe_constructed"]
            )
        ),
    }


def mode_extension_nondegenerate(rng: np.random.Generator, n: int) -> dict:
    return {
        "mode": "extension_generic_quasipure_nondegenerate",
        "note": "Re-run of the post-registration extension, skipping d - r = 1 where the "
        "QFIM is identically rank-deficient under PCC (a structural fact derived and "
        "verified in structure_check.py, not a sampling accident).",
        **_search("generic", GENERIC_NONDEGENERATE, rng, n),
    }


MODES = {
    "positive_control": (mode_positive_control, 20),
    "negative_control": (mode_negative_control, 500),
    "rank_detector": (mode_rank_detector, 10),
    "probe_check": (mode_probe_check, 10),
    "main_search": (mode_main_search, N_PREREG),
    "extension": (mode_extension, N_PREREG),
    "extension_nondegenerate": (mode_extension_nondegenerate, N_PREREG),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=sorted(MODES))
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--seed", type=int, default=56_20260918)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    fn, default_n = MODES[args.mode]
    rng = np.random.default_rng(args.seed)
    result = fn(rng, args.n if args.n is not None else default_n)
    result["seed"] = args.seed
    result["pcc_margin_tol"] = PCC_MARGIN_TOL

    METRICS.mkdir(exist_ok=True)
    out = METRICS / (args.out or f"{args.mode}.json")
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")

    slim = {k: v for k, v in result.items() if k not in ("batches", "rows")}
    if "batches" in result:
        slim["batch_summaries"] = [
            {"dims": b["dims"], "seconds": b["seconds"], **b["summary"]} for b in result["batches"]
        ]
    print(json.dumps(slim, indent=2, default=str))
    print("written:", out)


if __name__ == "__main__":
    main()
