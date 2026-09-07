"""run.py — H-B2-1p: discriminating test at N_DIM in {64, 80} -- does the omega(A)-M1 signal
that vanished at N_DIM in {40, 50} (H-B2-1o) reappear ("unlucky pair") or stay null ("genuine
ceiling")? Skeptic's own suggested next test, recorded verbatim in H-B2-1o's Pearl Registry.

Reuses H-B2-1m's build_matrix_with_seed_and_n, H-B2-1k's dim_sweep.measure_m1, and H-B2-1n's
numerical_abscissa UNCHANGED via dynamic import (Minimal Relaxation Rule) -- only the N_DIM
values are new (never tested in this arc before).
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

BOUNDARY_N_DIM_VALUES = (64, 80)  # never tested before in this arc -- genuinely new dimensions
N_SEEDS = 60  # matches H-B2-1o for direct comparability; seed reuse across N_DIM is fine --
# SeedSequence([n_dim, seed]) makes each (N_DIM, seed) pair unique regardless of N_DIM novelty
ALPHA = 0.05


def numerical_abscissa(a: np.ndarray) -> float:
    """Reused unchanged from H-B2-1n."""
    return abscissa_1n.numerical_abscissa(a)


def cmd_run() -> dict:
    per_n_slice = {}

    for n_dim in BOUNDARY_N_DIM_VALUES:
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
            "m1_range": [float(min(m1s)), float(max(m1s))],
            "per_seed": per_seed,
        }

    slice_ps = [v["spearman_p"] for v in per_n_slice.values()]
    slice_rhos = [v["spearman_rho"] for v in per_n_slice.values()]
    n_positive_significant = sum(1 for r, p in zip(slice_rhos, slice_ps) if r > 0 and p < ALPHA)

    if n_positive_significant == 2:
        verdict = "REAPPEARS"
    elif n_positive_significant == 0:
        verdict = "CEILING_CONFIRMED"
    else:
        verdict = "MIXED"

    # Fisher combination reported for context, NOT the primary criterion (see claim.md -- with
    # only 2 slices it has even less power to discriminate heterogeneity than the 5-slice case).
    fisher_stat, fisher_p_combined = combine_pvalues(slice_ps, method="fisher")

    result = {
        "config": {
            "n_dim_values": list(BOUNDARY_N_DIM_VALUES),
            "n_seeds": N_SEEDS,
            "population_note": (
                "N_DIM in {64,80} -- never tested before in the H-B2-1* arc. Direct comparison "
                "point: H-B2-1o found rho=0.007 (p=0.96) at BOTH N=40 and N=50."
            ),
        },
        "per_n_slice": per_n_slice,
        "fisher_context_only": {
            "fisher_combined_statistic": float(fisher_stat),
            "fisher_combined_p": float(fisher_p_combined),
            "note": "reported for context; NOT the primary criterion (only 2 slices, low power)",
        },
        "verdict": verdict,
        "verdict_note": (
            "REAPPEARS: both N=64,80 individually significant, positive sign -- supports "
            "N=40,50 being an unlucky patch, not a real boundary. CEILING_CONFIRMED: neither "
            "significant -- extends the null pattern, strengthens a genuine ceiling around "
            "N~35-40. MIXED: exactly one significant -- genuinely ambiguous, reported as such."
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_n_slice"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
