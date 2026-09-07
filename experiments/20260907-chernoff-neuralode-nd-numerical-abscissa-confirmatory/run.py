"""run.py — H-B2-1o: pre-registered confirmatory test of the Fisher-combination signal H-B2-1n
found exploratory (p=0.013, walled off from that experiment's own WEAKENED verdict per the
Anti-Overfitting Gate). Fresh seeds 40-99 (ZERO overlap with H-B2-1n's seeds 0-39), same N_DIM
set held fixed, Fisher combination is now the PRIMARY pre-registered criterion, not a post-hoc
add-on.

Reuses H-B2-1m's build_matrix_with_seed_and_n, H-B2-1k's dim_sweep.measure_m1, and H-B2-1n's
numerical_abscissa UNCHANGED via dynamic import (Minimal Relaxation Rule) -- only the seed range
and the pre-registration of Fisher-as-primary are new.
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

_N_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-numerical-abscissa"
_SPEC_N = importlib.util.spec_from_file_location("chernoff_1n_run", _N_DIR / "run.py")
abscissa_1n = importlib.util.module_from_spec(_SPEC_N)
_SPEC_N.loader.exec_module(abscissa_1n)

LARGE_N_DIM_VALUES = (16, 24, 32, 40, 50)  # held fixed -- Minimal Relaxation Rule
SEED_START = 40  # fresh seeds -- ZERO overlap with H-B2-1n's seeds 0-39
SEED_END = 100  # exclusive -- 60 fresh seeds per slice, 300 total pairs
PRIMARY_ALPHA = 0.05


def numerical_abscissa(a: np.ndarray) -> float:
    """Reused unchanged from H-B2-1n -- same proven Bendixson/Lumer-Phillips bound."""
    return abscissa_1n.numerical_abscissa(a)


def cmd_run() -> dict:
    per_n_slice = {}

    for n_dim in LARGE_N_DIM_VALUES:
        omegas = []
        m1s = []
        per_seed = {}
        for seed in range(SEED_START, SEED_END):
            a = multin.build_matrix_with_seed_and_n(n_dim, seed)
            omega = numerical_abscissa(a)
            m1 = dim_sweep.measure_m1(a, dim_sweep.T_MAX, dim_sweep.W)
            omegas.append(omega)
            m1s.append(m1)
            per_seed[str(seed)] = {"omega": omega, "m1": m1}

        rho, p = spearmanr(omegas, m1s)
        per_n_slice[str(n_dim)] = {
            "n_dim": n_dim,
            "n_seeds": SEED_END - SEED_START,
            "seed_range": [SEED_START, SEED_END],
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

    n_significant = sum(1 for p in slice_ps if p < PRIMARY_ALPHA)
    n_positive = sum(1 for r in slice_rhos if r > 0)
    n_negative = sum(1 for r in slice_rhos if r < 0)
    consistent_sign = n_positive >= majority or n_negative >= majority

    # PRIMARY, PRE-REGISTERED CRITERION -- pre-registered in claim.md BEFORE this code ran.
    # Legitimate combination of 5 independent slice p-values (disjoint N_DIM x fresh-seed
    # populations), not the pooled-raw-data confound Step 0a caught in H-B2-1l.
    fisher_stat, fisher_p_combined = combine_pvalues(slice_ps, method="fisher")

    if fisher_p_combined < PRIMARY_ALPHA:
        verdict = "CONFIRMED"
    else:
        verdict = "REJECTED"

    result = {
        "config": {
            "n_dim_values": list(LARGE_N_DIM_VALUES),
            "seed_range": [SEED_START, SEED_END],
            "n_seeds_per_slice": SEED_END - SEED_START,
            "population_note": (
                "FRESH seeds 40-99 -- ZERO overlap with H-B2-1n's exploratory-discovery seeds "
                "0-39. Same N_DIM set held fixed per Minimal Relaxation Rule."
            ),
        },
        "per_n_slice": per_n_slice,
        "primary_criterion": {
            "statistic": "fisher_combined_p",
            "pre_registered_threshold": PRIMARY_ALPHA,
            "fisher_combined_statistic": float(fisher_stat),
            "fisher_combined_p": float(fisher_p_combined),
            "note": (
                "PRE-REGISTERED PRIMARY criterion (claim.md, written before this run) -- unlike "
                "H-B2-1n where the Fisher combination was exploratory/post-hoc and explicitly "
                "walled off from the verdict, here it IS the verdict."
            ),
        },
        "secondary_descriptive": {
            "n_slices": n_slices,
            "n_slices_significant_alpha05": n_significant,
            "n_slices_positive": n_positive,
            "n_slices_negative": n_negative,
            "majority_needed": majority,
            "consistent_sign": consistent_sign,
            "note": "reported for transparency/comparability with H-B2-1n; NOT verdict-determining",
        },
        "verdict": verdict,
        "verdict_note": (
            "CONFIRMED: Fisher-combined p < 0.05 on fresh, non-overlapping seeds -- the "
            "exploratory signal H-B2-1n reported replicates on independent data. REJECTED: "
            "Fisher-combined p >= 0.05 -- the exploratory signal does not replicate; omega(A), "
            "like kappa(V) before it, does not clear a pre-registered bar at large N_DIM via "
            "simple monotone correlation with M1."
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_n_slice"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
