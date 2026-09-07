"""run.py — H-B2-1n: does the numerical abscissa omega(A) = lambda_max((A+A^T)/2) explain M1
where kappa(V) (eigenvector conditioning) failed -- at large N_DIM (16,24,32,40,50), per H-B2-1m's
own decision.md Relaxation Map ("targeted test of a specific alternative descriptor... not
another broad N-sweep").

Reuses H-B2-1m's build_matrix_with_seed_and_n (identical population: same N_DIM values, same 40
seeds/slice, same SeedSequence-based independence) and H-B2-1k's dim_sweep.measure_m1 UNCHANGED
via dynamic import (Minimal Relaxation Rule) -- only the numerical-abscissa computation and the
per-slice correlation analysis (matching H-B2-1m's own per-slice, never-pooled discipline) are new.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.stats import combine_pvalues, spearmanr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_K_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-dimension-sweep"
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1k_run", _K_DIR / "run.py")
dim_sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(dim_sweep)

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1m_run", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

LARGE_N_DIM_VALUES = (16, 24, 32, 40, 50)  # matches H-B2-1m's power follow-up population exactly
N_SEEDS = 40  # matches H-B2-1m's power follow-up seed count exactly -- same population


def numerical_abscissa(a: np.ndarray) -> float:
    """omega(A) = lambda_max((A + A^T)/2), the numerical abscissa. Bendixson/Lumer-Phillips:
    d/dt||x||^2 = x^T(A+A^T)x <= 2*omega(A)*||x||^2, giving ||exp(tA)|| <= exp(t*omega(A)) for
    the initial growth rate -- a proven bound, not an assumed behavior (no FL Step 0a trigger,
    same status as the Trefethen-Embree inequality underlying kappa(V))."""
    symmetric_part = (a + a.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(symmetric_part)  # symmetric -> real eigenvalues, stable
    return float(np.max(eigenvalues))


def cmd_run() -> dict:
    per_n_slice = {}

    for n_dim in LARGE_N_DIM_VALUES:
        omegas = []
        m1s = []
        per_seed = {}
        for seed in range(N_SEEDS):
            a = multin.build_matrix_with_seed_and_n(n_dim, seed)
            omega = numerical_abscissa(a)
            m1 = dim_sweep.measure_m1(a, dim_sweep.T_MAX, dim_sweep.W)
            omegas.append(omega)
            m1s.append(m1)
            per_seed[str(seed)] = {"omega": omega, "m1": m1}

        rho, p = spearmanr(omegas, m1s)
        per_n_slice[str(n_dim)] = {
            "n_dim": n_dim,
            "n_seeds": N_SEEDS,
            "spearman_rho": float(rho),
            "spearman_p": float(p),
            "omega_range": [float(min(omegas)), float(max(omegas))],
            "omega_std": float(np.std(omegas)),
            "per_seed": per_seed,
        }

    slice_rhos = [v["spearman_rho"] for v in per_n_slice.values()]
    slice_ps = [v["spearman_p"] for v in per_n_slice.values()]
    n_slices = len(slice_rhos)
    majority = n_slices // 2 + 1

    n_significant = sum(1 for p in slice_ps if p < 0.05)
    n_positive = sum(1 for r in slice_rhos if r > 0)
    n_negative = sum(1 for r in slice_rhos if r < 0)
    consistent_sign = n_positive >= majority or n_negative >= majority

    # omega(A) variance check (claim.md's Step 0a note): if omega barely varies across seeds,
    # any correlation test is uninformative by construction -- report this explicitly rather
    # than let a near-constant descriptor silently produce a meaningless p-value.
    near_degenerate_slices = [
        n_dim
        for n_dim, v in per_n_slice.items()
        if v["omega_std"] < 1e-6 * max(abs(v["omega_range"][0]), abs(v["omega_range"][1]), 1e-12)
    ]

    if n_significant >= majority and consistent_sign:
        verdict = "CONFIRMED"
    elif n_significant > 0:
        verdict = "WEAKENED"
    else:
        verdict = "REJECTED"

    # EXPLORATORY, POST-HOC -- NOT part of the pre-registered kill criterion (claim.md) and does
    # NOT change the verdict above. Reported because all 5 slices show consistent positive sign
    # and similar magnitude (rho 0.21-0.35), unlike kappa(V)'s mixed-sign large-N pattern -- this
    # combines the 5 INDEPENDENT slice p-values via Fisher's method, which is legitimate (unlike
    # pooling raw data across N_DIM, the Step 0a confound this project already found) because
    # each slice is a genuinely independent test on a disjoint (N_DIM, seed) population. Adding
    # this AFTER seeing individually-non-significant slices risks exactly the post-hoc-relaxation
    # pattern the Anti-Overfitting Gate warns against, so it is explicitly walled off from the
    # pre-registered verdict, not used to upgrade WEAKENED to CONFIRMED.
    fisher_stat, fisher_p_combined = combine_pvalues(slice_ps, method="fisher")

    result = {
        "config": {
            "n_dim_values": list(LARGE_N_DIM_VALUES),
            "n_seeds": N_SEEDS,
            "population_note": "identical (N_DIM, seed) population to H-B2-1m's power follow-up",
        },
        "per_n_slice": per_n_slice,
        "slice_summary": {
            "n_slices": n_slices,
            "n_slices_significant_alpha05": n_significant,
            "n_slices_positive": n_positive,
            "n_slices_negative": n_negative,
            "majority_needed": majority,
            "consistent_sign": consistent_sign,
            "near_degenerate_omega_slices": near_degenerate_slices,
        },
        "exploratory_post_hoc_NOT_part_of_kill_criterion": {
            "fisher_combined_statistic": float(fisher_stat),
            "fisher_combined_p": float(fisher_p_combined),
            "warning": (
                "computed AFTER seeing individually-non-significant slices -- legitimate "
                "combination of 5 independent slice p-values (not the pooled-raw-data confound "
                "Step 0a already found), but explicitly NOT used to change the pre-registered "
                "verdict above, per the Anti-Overfitting Gate's own discipline against post-hoc "
                "criterion relaxation"
            ),
        },
        "verdict": verdict,
        "verdict_note": (
            "CONFIRMED: majority of large-N slices individually significant, consistent sign -- "
            "omega(A) explains transient growth where kappa(V) did not. WEAKENED: some but not "
            "majority significant. REJECTED: no slice significant -- leaves the large-N gap "
            "unexplained by either candidate descriptor, informative about THESE TWO options, "
            "not proof no descriptor could work (pseudospectral abscissa remains untested)."
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_n_slice"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
