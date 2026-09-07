"""run.py — H-B2-1m: genuinely independent multi-seed x multi-N_DIM test of the kappa(V)->M1
mechanism (H-B2-1l), replacing the discredited N-sweep leg (SEED=0 hard-coded across N -- one
deterministic curve, not 9 independent draws) with fresh independent seeds at EVERY (N_DIM, seed)
combination.

Reuses H-B2-1k's dim_sweep.measure_m1 / SPECTRAL_RANGE / POSITIVE_EIGENVALUE / W /
COUPLING_MAGNITUDE / T_MAX / N_DIM_VALUES and H-B2-1l's eigenvector_condition_number UNCHANGED
via dynamic import (Minimal Relaxation Rule) -- only build_matrix is new (parameterized by seed,
not hard-coded), and only the per-slice + Fisher-combined analysis is new.

FL Step 0a (Mechanism Claim Gate) already ran before this file was written -- see claim.md: a
naive pooled Spearman across N_DIM is CONFOUNDED (verified: synthetic no-real-link data gives
rho=0.948, p=2.1e-45 pooled). Primary analysis here is therefore per-N_DIM-slice, never pooled.
"""

from __future__ import annotations

import importlib.util
import json
from math import factorial
from pathlib import Path

import numpy as np
from scipy.stats import combine_pvalues, spearmanr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_K_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-dimension-sweep"
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1k_run", _K_DIR / "run.py")
dim_sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(dim_sweep)

_L_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-eigenvector-conditioning"
_SPEC_L = importlib.util.spec_from_file_location("chernoff_1l_run", _L_DIR / "run.py")
eig_cond = importlib.util.module_from_spec(_SPEC_L)
_SPEC_L.loader.exec_module(eig_cond)

N_SEEDS_PER_N = 15  # fresh independent seeds at EVERY (N_DIM, seed) pair -- the actual fix
CONFIRM_THRESHOLD = 0.2  # matches H-B2-1l's own pre-registered |rho| threshold

# FOLLOW-UP (2026-09-07, user's own request after reading decision.md's Relaxation Map): the
# original run left an open question -- is the large-N_DIM null (N_DIM in {16,24,32,40,50}, none
# individually significant at n=15/slice) a genuine breakdown of the kappa(V) mechanism, or just
# inadequate power? N_DIM=50's p=0.056 at n=15 was close enough to alpha=0.05 to be suspicious.
# LARGE_N_THRESHOLD=16 matches the ACTUAL boundary found in this experiment's own data: N_DIM=12
# was individually significant (p=9.4e-8), N_DIM=16 was the first slice that was not -- the
# threshold is drawn where the real data broke, not chosen a priori.
LARGE_N_THRESHOLD = 16
N_SEEDS_LARGE_N = 40  # detects rho~=0.43 at 80% power, alpha=0.05 -- comparable to this
# experiment's own original point estimates at N_DIM=24 (0.446) and N_DIM=50 (0.504), so a real
# effect of that size should become individually significant; SeedSequence-based seeding means
# seeds 0..14 are byte-identical to the original run, this only ADDS seeds 15..39, not a fresh
# randomization of the already-collected small-N results.


def seeds_for(n_dim: int) -> int:
    return N_SEEDS_LARGE_N if n_dim >= LARGE_N_THRESHOLD else N_SEEDS_PER_N


def build_matrix_with_seed_and_n(n_dim: int, seed: int) -> np.ndarray:
    """Same construction as H-B2-1k's dim_sweep.build_matrix (fixed SPECTRAL_RANGE, not scaled
    with n_dim -- avoids H-B2-1j's own confound). RNG seeded on the (n_dim, seed) PAIR via
    SeedSequence, not on seed alone -- FL Step 8a skeptic pass (2026-09-07) found and I
    independently verified that seeding on `seed` alone shares the SAME raw uniform stream
    across every n_dim for a matching seed index (default_rng(0).uniform(size=(3,3)).ravel()
    == default_rng(0).uniform(size=(4,4)).ravel()[:9], confirmed by direct computation) --
    this made the 9 N_DIM slices statistically dependent, not the "9 independent slice tests"
    claim.md's Zero-Signal Gate asserted. SeedSequence([n_dim, seed]) gives each (N_DIM, seed)
    combination its own independent stream, matching what was actually claimed."""
    eigenvalues = np.concatenate(
        [
            [dim_sweep.POSITIVE_EIGENVALUE],
            np.linspace(dim_sweep.SPECTRAL_RANGE[0], dim_sweep.SPECTRAL_RANGE[1], n_dim - 1),
        ]
    )
    rng = np.random.default_rng(np.random.SeedSequence([n_dim, seed]))
    a = np.diag(eigenvalues)
    coupling = rng.uniform(
        -dim_sweep.COUPLING_MAGNITUDE, dim_sweep.COUPLING_MAGNITUDE, size=(n_dim, n_dim)
    )
    return a + np.triu(coupling, k=1)


def n3_low_dof_structural_check(n_seeds: int = N_SEEDS_PER_N) -> dict:
    """FL Step 8a skeptic finding: at N_DIM=3 there are only 3 random coupling entries (the
    upper-triangular k=1 positions of a 3x3 matrix), and the eigenvalues are FIXED across seeds
    (upper-triangular -> eigenvalues = diagonal, unaffected by coupling). Both kappa(V) and M1
    are then smooth monotone functions of the SAME 3-parameter input -- rho=1.000 exactly across
    15 seeds could be a low-degrees-of-freedom construction artifact, not evidence of a physical
    mechanism. Test: do two ARBITRARY monotone functions of the same 3 coupling values ALSO
    correlate near-perfectly with kappa(V) and M1? If yes, N=3 cannot distinguish "kappa(V)
    specifically matters" from "anything smooth-and-monotone of these 3 numbers correlates with
    anything else smooth-and-monotone of them" -- the slice would carry no mechanistic content."""
    kappas, m1s, f1s, f2s = [], [], [], []
    for seed in range(n_seeds):
        a = build_matrix_with_seed_and_n(3, seed)
        kappa = eig_cond.eigenvector_condition_number(a)
        m1 = dim_sweep.measure_m1(a, dim_sweep.T_MAX, dim_sweep.W)
        c = np.triu(a, k=1)
        c01, c02, c12 = c[0, 1], c[0, 2], c[1, 2]
        f1 = abs(c01) + abs(c02) + abs(c12)  # arbitrary monotone function #1
        f2 = max(abs(c01), abs(c02), abs(c12))  # arbitrary monotone function #2
        kappas.append(kappa)
        m1s.append(m1)
        f1s.append(f1)
        f2s.append(f2)

    def _r(x, y):
        rho, p = spearmanr(x, y)
        return {"rho": float(rho), "p": float(p)}

    return {
        "f1_vs_kappa": _r(f1s, kappas),
        "f1_vs_m1": _r(f1s, m1s),
        "f2_vs_kappa": _r(f2s, kappas),
        "f2_vs_m1": _r(f2s, m1s),
        "interpretation": (
            "if these are ALSO near rho=1.0, N=3's perfect correlation reflects the "
            "low-degrees-of-freedom construction (any two monotone functions of 3 numbers "
            "correlate near-perfectly with each other), not a kappa(V)-specific mechanism"
        ),
    }


def cmd_run() -> dict:
    per_n_slice = {}
    kappa_all: list[float] = []
    m1_all: list[float] = []
    n_all: list[int] = []

    for n_dim in dim_sweep.N_DIM_VALUES:
        n_seeds_here = seeds_for(n_dim)
        kappas = []
        m1s = []
        per_seed = {}
        for seed in range(n_seeds_here):
            a = build_matrix_with_seed_and_n(n_dim, seed)
            kappa = eig_cond.eigenvector_condition_number(a)
            m1 = dim_sweep.measure_m1(a, dim_sweep.T_MAX, dim_sweep.W)
            kappas.append(kappa)
            m1s.append(m1)
            per_seed[str(seed)] = {"kappa_v": kappa, "m1": m1}
            kappa_all.append(kappa)
            m1_all.append(m1)
            n_all.append(n_dim)

        rho, p = spearmanr(kappas, m1s)
        per_n_slice[str(n_dim)] = {
            "n_dim": n_dim,
            "n_seeds": n_seeds_here,
            "spearman_rho": float(rho),
            "spearman_p": float(p),
            "per_seed": per_seed,
        }

    slice_rhos = [v["spearman_rho"] for v in per_n_slice.values()]
    slice_ps = [v["spearman_p"] for v in per_n_slice.values()]
    n_positive = sum(1 for r in slice_rhos if r > 0)
    n_confirmed_threshold = sum(1 for r in slice_rhos if r >= CONFIRM_THRESHOLD)
    n_slices = len(slice_rhos)
    majority = n_slices // 2 + 1

    # Floor before combining: a perfect (rho=+-1.0) slice makes scipy's asymptotic t-approximation
    # return an exact 0.0 (1-rho^2=0 -> t=inf -> survival function is exactly 0). FL Step 8a
    # skeptic pass (2026-09-07) found np.finfo(float).tiny (~2.2e-308) as a floor launders this
    # into an astronomically-inflated Fisher statistic dominated by one slice. The PRINCIPLED
    # floor for this specific artifact is the exact-permutation minimum p-value achievable at
    # THAT SLICE's own sample size (slices now differ in size after the large-N power follow-up):
    # with n independent ranks, the smallest possible two-sided exact Spearman p-value is 2/n!
    # (only 2 of n! permutations give a perfect rank match, in either direction).
    slice_p_floors = [2.0 / factorial(v["n_seeds"]) for v in per_n_slice.values()]
    slice_ps_floored = [max(p, floor) for p, floor in zip(slice_ps, slice_p_floors)]
    any_floored = any(p < floor for p, floor in zip(slice_ps, slice_p_floors))
    fisher_stat, fisher_p = combine_pvalues(slice_ps_floored, method="fisher")

    # Honest trend report (skeptic finding #3): does correlation strength itself trend with
    # N_DIM? A per-N_DIM Fisher-combined "CONFIRMED" can be true while masking a monotonic
    # decay to non-significance at the large-N end -- report the trend directly, not just the
    # combined significance test, so a decay pattern is visible rather than hidden.
    trend_rho, trend_p = spearmanr(list(dim_sweep.N_DIM_VALUES), slice_rhos)

    n_slices_significant_individually = sum(1 for p in slice_ps if p < 0.05)
    n_large_n_significant = sum(
        1 for n_dim, p in zip(dim_sweep.N_DIM_VALUES, slice_ps) if n_dim >= 24 and p < 0.05
    )

    # WEAKENED branch bug fix (skeptic finding, LOW severity but real): claim.md's own text
    # restricts the fallback condition to slices that are BOTH positive AND >= threshold, not
    # "any slice >= threshold regardless of sign" (irrelevant given every slice here is
    # positive, but the prior code did not actually implement the pre-registered text).
    n_positive_and_at_threshold = sum(1 for r in slice_rhos if r > 0 and r >= CONFIRM_THRESHOLD)

    if n_positive >= majority and fisher_p < 0.05 and n_large_n_significant > 0:
        verdict = "CONFIRMED"
    elif n_positive >= majority and fisher_p < 0.05:
        # Combined significance driven by small-N slices only -- large-N end not individually
        # significant. Per FL Step 8a Recomposition Gate: "generalizes across dimension" does
        # NOT follow from "combined p is tiny" when the tail of the range shows no effect.
        verdict = "WEAKENED"
    elif n_positive >= majority or n_positive_and_at_threshold > 0:
        verdict = "WEAKENED"
    else:
        verdict = "REJECTED"

    # Naive pooled Spearman -- reported ONLY as a labeled, confounded reference (FL Step 0a).
    pooled_rho, pooled_p = spearmanr(kappa_all, m1_all)

    n3_check = n3_low_dof_structural_check()

    result = {
        "config": {
            "n_dim_values": list(dim_sweep.N_DIM_VALUES),
            "seeds_per_n_small": N_SEEDS_PER_N,
            "seeds_per_n_large": N_SEEDS_LARGE_N,
            "large_n_threshold": LARGE_N_THRESHOLD,
            "confirm_threshold": CONFIRM_THRESHOLD,
        },
        "per_n_slice": per_n_slice,
        "slice_summary": {
            "n_slices": n_slices,
            "n_slices_positive": n_positive,
            "n_slices_at_or_above_threshold": n_confirmed_threshold,
            "majority_needed": majority,
            "fisher_combined_statistic": float(fisher_stat),
            "fisher_combined_p": float(fisher_p),
            "note_p_value_floored": any_floored,
            "note": (
                "one or more slice p-values underflowed below the exact-permutation floor "
                "2/N! (perfect rho=+-1.0 slice) and were floored to that value before "
                "Fisher combination"
                if any_floored
                else None
            ),
            "n_slices_significant_individually_alpha05": n_slices_significant_individually,
            "n_large_n_slices_significant": n_large_n_significant,
            "decay_trend_rho_vs_n_dim": float(trend_rho),
            "decay_trend_p": float(trend_p),
            "decay_trend_note": (
                "Spearman(N_DIM, per-slice rho) across the 9 slices -- a strong NEGATIVE "
                "value here means correlation strength itself decays with dimension, which "
                "a combined Fisher p can hide"
            ),
        },
        "pooled_CONFOUNDED_reference_only": {
            "spearman_rho": float(pooled_rho),
            "spearman_p": float(pooled_p),
            "warning": (
                "FL Step 0a check (claim.md) confirmed pooling across N_DIM is confounded "
                "-- NOT the claim under test, reference only"
            ),
        },
        "n3_low_dof_structural_check": n3_check,
        "verdict": verdict,
        "verdict_note": (
            "CONFIRMED means: majority of slices positive, Fisher-combined p<0.05, AND at least "
            "one large-N (>=24) slice individually significant -- i.e. the effect is present at "
            "the large-N end too, not just driving the combined stat via small N. WEAKENED means "
            "the combined significance is real but concentrated at small N, OR partial support "
            "only. See FL Step 8a skeptic pass (2026-09-07) that found the original criterion "
            "did not check this and would have called a small-N-only effect 'generalizes across "
            "dimension'."
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_n_slice"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
