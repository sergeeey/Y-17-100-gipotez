"""run.py — H-B2-1u: mechanistic verification of the Kreiss Matrix Theorem as the actual
explanation for pseudospectral abscissa's predictive power over kappa(V)/omega(A) (user's own
Priority 3, "pseudospectrum -> resolvent amplification -> transient growth -> M1").

Every prior experiment in this arc correlated alpha_eps(A) AT A SINGLE FIXED eps=1 with M1 --
real evidence, but indirect. This experiment computes what the theorem is actually ABOUT: a
genuine Kreiss constant estimate K(A) = max over several eps of (alpha_eps(A)-alpha(A))/eps, and
the raw (non-w-normalized) transient growth sup_t||exp(tA)||, then checks the proven inequality
K(A) <= sup_t||exp(tA)|| <= e*n*K(A) directly.

Reuses pseudospectral_abscissa (H-B2-1r), build_matrix_with_seed_and_n (H-B2-1m), and
dim_sweep's T_MAX/W/n_grid convention (H-B2-1k) UNCHANGED via dynamic import (Minimal
Relaxation Rule). Only the multi-eps Kreiss estimate and the raw (non-normalized) transient
growth measurement are new.
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm

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

_R_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
_SPEC_R = importlib.util.spec_from_file_location("chernoff_1r_run", _R_DIR / "run.py")
alpha_mod = importlib.util.module_from_spec(_SPEC_R)
_SPEC_R.loader.exec_module(alpha_mod)

N_DIM_VALUES = (40, 50)  # matches the arc's established "primary large-N regime"
SEED_START = 300  # reuses H-B2-1t's own fresh seed range -- same deterministic matrices,
SEED_COUNT = 10  # first 10 of 40 already used there (no new randomness introduced)

# BUG/FIX HISTORY (found by this experiment's own kill criterion, not by a later reviewer):
# first draft used EPS_VALUES=(0.5,1.0,1.5,2.0,3.0) reusing pseudospectral_abscissa's ARC-WIDE
# default grid (RE_MIN..RE_MAX=-5..60, N_RE=100 -> step 0.65). That produced 1/20 apparent
# violations of the PROVEN Kreiss upper bound (seed=301, N_DIM=50: growth=11025.75 > ceiling=
# 3104.06 computed from k_estimate=22.84). A violation of a proven theorem cannot be real --
# per claim.md's own Kill Criterion this meant "investigate before reporting a verdict," not
# "report CODE_BUG_SUSPECTED and stop." Diagnosis (script kept as
# ../../tooling-eval/diagnostics/h_b2_1u_seed301_n50_kreiss_eps_scan.py): this matrix family
# (build_matrix_with_seed_and_n = diagonal + strictly-upper-triangular random coupling, i.e.
# genuinely upper-triangular / near-nilpotent structure) has its TRUE Kreiss-constant supremum
# in the SMALL-eps regime, not the eps>=0.5 region originally sampled -- a locally-refined scan
# on the SAME matrix found ratio=259.78 at eps=0.02 vs. 22.84 at eps=0.5..3.0 (an 11x jump),
# giving a corrected ceiling of ~35313 that comfortably exceeds the observed growth. This was a
# SAMPLING gap in this experiment's own new code (EPS_VALUES missing the small-eps regime where
# this specific matrix family's Kreiss constant actually lives), not a bug in the already-twice-
# independently-verified pseudospectral_abscissa (H-B2-1r/H-B2-1s) and not evidence against the
# theorem. Fixed by widening EPS_VALUES down to 0.02 and switching to a dedicated, locally-
# refined grid (see KREISS_GRID_KWARGS below) instead of pseudospectral_abscissa's eps~1-tuned
# arc-wide default -- re-run confirmed the upper bound holds for all 20/20 matrices.
#
# CONVERGENCE CAVEAT (found by mandatory reviewer, P1, verified directly before accepting):
# k_estimate is pinned to the SMALLEST sampled eps (0.02) for 20/20 matrices with NO plateau --
# a targeted follow-up scan on the worst-case matrix (seed=301, N=50) down to eps=0.001 (finer,
# narrower grid: window +8, n_re=1200) found the ratio STILL climbing steeply (262.9 -> 437.7 ->
# 723.3 -> 1377.8 -> 2208.5 as eps: 0.02 -> 0.01 -> 0.005 -> 0.002 -> 0.001), not converging --
# and at these smaller eps the grid step itself becomes comparable to or larger than eps, so even
# THOSE numbers are not trustworthy as a converged K(A). This is a structural limitation of
# grid-search pseudospectral abscissa, not a fixable "just add more EPS_VALUES" bug: resolving
# eps requires grid step << eps, which needs grid resolution scaling with 1/eps -- unbounded as
# eps -> 0. k_estimate below is therefore a DEMONSTRATED LOWER BOUND on the true K(A), not a
# converged estimate. Consequences, both checked, not assumed:
# (1) MECHANISM_VERIFIED is UNAFFECTED in the safe direction -- an underestimated K(A) only makes
#     e*n*K(A) (the ceiling) SMALLER, i.e. the upper-bound check is STRICTER, not more lenient.
#     It still held 20/20 despite using an underestimated K -- the true (larger) ceiling holds
#     with even more margin.
# (2) The reported efficiency ratios (growth/ceiling) are UPPER bounds on the true efficiency --
#     true efficiency is likely LOWER (looser bound) than reported, strengthening rather than
#     undermining the "bound holds but is loose" qualitative finding in decision.md.
# (3) The N=50/seed=301 "efficiency max=0.31" outlier is likely an ARTIFACT of that specific
#     matrix happening to have a k_estimate that undershot proportionally more at eps=0.02 than
#     the other 19 -- at eps=0.001 its own efficiency would drop to ~0.037, in line with the
#     other matrices, not a genuine per-matrix difference. decision.md's "Convergence Caveat"
#     section states this explicitly rather than treating the outlier as a real finding.
# Not fixed further here (would need an adaptive/higher-resolution estimator, e.g. reusing
# pseudopy's own solver instead of a fixed grid, or an eigenvalue-perturbation-based small-eps
# expansion) -- named as a Pearl Registry follow-up, not chased with more compute in this cycle.
EPS_VALUES = (0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0)

# Dedicated grid for the Kreiss estimate: a LOCAL window around alpha(A) (not the arc-wide
# RE_MIN..RE_MAX=-5..60 grid, which is far too coarse -- step 0.65 -- to resolve eps as small
# as 0.02). Window width (+30 past spectral_abscissa) and n_re=150 were validated against the
# worst-case matrix found (seed=301, N=50, alpha_eps(eps=3.0)=20.28, comfortably inside +30).
# NOTE (reviewer P2, verified): pseudospectral_abscissa clamps its own re_min to
# max(re_min, spectral_abscissa) (H-B2-1r's bug fix) -- passing re_min < spectral_abscissa is
# always overridden. No re_min_offset key here (an earlier draft's -1.0 offset was silently
# discarded every call); the effective window is exactly [spectral_abscissa, spectral_abscissa +
# re_max_offset].
KREISS_GRID_KWARGS = {
    "re_max_offset": 30.0,
    "im_max": 10.0,
    "n_re": 150,
    "n_im": 80,
}

EULER_E = math.e


def raw_transient_growth(a: np.ndarray, t_max: float, n_grid: int = 1000) -> tuple[float, float]:
    """sup_t ||exp(tA)|| over t in (0, t_max] -- the RAW quantity the Kreiss theorem bounds,
    NOT measure_m1's w-normalized variant. Returns (max_norm, t_at_max) -- the second value
    diagnoses whether the peak was captured well before t_max (comfortable) or right at the
    boundary (T_MAX=1.0 may be truncating the true peak -- see claim.md's honest caveat)."""
    ts = np.linspace(t_max / n_grid, t_max, n_grid)
    norms = [np.linalg.norm(expm(t * a), ord=2) for t in ts]
    idx_max = int(np.argmax(norms))
    return float(norms[idx_max]), float(ts[idx_max])


def kreiss_constant_estimate(a: np.ndarray, eps_values: tuple[float, ...] = EPS_VALUES) -> dict:
    """K(A) = sup_{eps>0} (alpha_eps(A) - alpha(A)) / eps, estimated as the max over a FINITE
    sample of eps values -- a DEMONSTRATED LOWER BOUND on the true supremum, NOT shown to have
    converged (see the CONVERGENCE CAVEAT above EPS_VALUES -- the ratio was still climbing
    steeply at eps down to 0.001 on the worst-case matrix, with no plateau found). Uses a LOCAL,
    alpha(A)-centered grid (not pseudospectral_abscissa's arc-wide default) so small eps values
    are at least partially resolved -- see the EPS_VALUES/KREISS_GRID_KWARGS bug/fix note above.
    `re_min` is intentionally omitted: pseudospectral_abscissa clamps it to spectral_abscissa
    regardless (reviewer P2 finding), so passing an offset here would be dead code."""
    spectral_abscissa = float(np.max(np.linalg.eigvals(a).real))
    g = KREISS_GRID_KWARGS
    ratios = {}
    for eps in eps_values:
        alpha_eps = alpha_mod.pseudospectral_abscissa(
            a,
            eps=eps,
            re_max=spectral_abscissa + g["re_max_offset"],
            im_max=g["im_max"],
            n_re=g["n_re"],
            n_im=g["n_im"],
        )
        ratios[str(eps)] = (alpha_eps - spectral_abscissa) / eps
    k_estimate = max(ratios.values())
    return {
        "spectral_abscissa": spectral_abscissa,
        "ratios_by_eps": ratios,
        "k_estimate": float(k_estimate),
    }


def cmd_run() -> dict:
    per_n_slice = {}

    for n_dim in N_DIM_VALUES:
        per_seed = {}
        upper_bound_violations = 0
        lower_bound_violations = 0
        efficiencies = []

        for seed in range(SEED_START, SEED_START + SEED_COUNT):
            a = multin.build_matrix_with_seed_and_n(n_dim, seed)
            kreiss = kreiss_constant_estimate(a)
            k_est = kreiss["k_estimate"]
            growth, t_at_max = raw_transient_growth(a, dim_sweep.T_MAX)

            ceiling = EULER_E * n_dim * k_est
            upper_holds = bool(growth <= ceiling + 1e-9)
            lower_holds = bool(k_est <= growth + 1e-9)
            efficiency = growth / ceiling if ceiling > 0 else float("nan")

            if not upper_holds:
                upper_bound_violations += 1
            if not lower_holds:
                lower_bound_violations += 1
            efficiencies.append(efficiency)

            per_seed[str(seed)] = {
                "k_estimate": k_est,
                "raw_transient_growth": growth,
                "t_at_max": t_at_max,
                "t_at_max_near_boundary": bool(t_at_max > 0.95 * dim_sweep.T_MAX),
                "ceiling_e_n_k": ceiling,
                "upper_bound_holds": upper_holds,
                "lower_bound_holds": lower_holds,
                "efficiency": efficiency,
                "kreiss_detail": kreiss,
            }

        per_n_slice[str(n_dim)] = {
            "n_dim": n_dim,
            "n_seeds": SEED_COUNT,
            "seed_range": [SEED_START, SEED_START + SEED_COUNT],
            "upper_bound_violations": upper_bound_violations,
            "lower_bound_violations": lower_bound_violations,
            "efficiency_median": float(np.median(efficiencies)),
            "efficiency_min": float(np.min(efficiencies)),
            "efficiency_max": float(np.max(efficiencies)),
            "per_seed": per_seed,
        }

    total_upper_violations = sum(v["upper_bound_violations"] for v in per_n_slice.values())
    total_matrices = sum(v["n_seeds"] for v in per_n_slice.values())

    result = {
        "config": {
            "n_dim_values": list(N_DIM_VALUES),
            "seed_range": [SEED_START, SEED_START + SEED_COUNT],
            "eps_values": list(EPS_VALUES),
            "population_note": (
                "Reuses H-B2-1t's own fresh seeds 300-309 (first 10 of the 40 used there) -- "
                "same deterministic matrices, no new randomness."
            ),
        },
        "per_n_slice": per_n_slice,
        "upper_bound_check": {
            "total_matrices": total_matrices,
            "total_violations": total_upper_violations,
            "all_hold": total_upper_violations == 0,
        },
        "verdict": "MECHANISM_VERIFIED" if total_upper_violations == 0 else "CODE_BUG_SUSPECTED",
        "verdict_note": (
            "MECHANISM_VERIFIED: the proven Kreiss upper bound holds for every sampled matrix "
            "(mathematically required if this arc's own alpha_eps/transient-growth code is "
            "correct) -- the substantive finding is the efficiency ratio distribution, not this "
            "binary. CODE_BUG_SUSPECTED: the upper bound was violated somewhere -- this cannot "
            "happen if the theorem is applied correctly to correctly-computed inputs, so a "
            "violation indicates a real implementation bug requiring investigation, not a "
            "normal REJECT."
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_n_slice"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
