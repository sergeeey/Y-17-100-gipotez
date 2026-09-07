"""run.py — H-B2-1s: independent cross-implementation check of H-B2-1r's pseudospectral
abscissa claim, using the `pseudopy` package (named by the FL Step 8a skeptic pass on H-B2-1r
as the concrete way to close its remaining "no cross-implementation check" gap). User's own
Priority 1 instruction: verify at the primary large-N regime (N=40, N=50) before pursuing
anything further.

`pseudopy` is unmaintained (last compatible with pre-2.0 shapely) -- needs a one-line
compatibility shim before import. This is a pure rename (cascaded_union -> unary_union,
shapely's own deprecation, no behavior change), applied here at the call site, NOT by patching
the installed package.

Reuses H-B2-1m's build_matrix_with_seed_and_n UNCHANGED via dynamic import (Minimal Relaxation
Rule) -- M1 values are reused from H-B2-1r's own metrics/run.json, not recomputed.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import shapely.ops

if not hasattr(shapely.ops, "cascaded_union"):
    shapely.ops.cascaded_union = shapely.ops.unary_union

import numpy as np
import pseudopy
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1m_run", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_R_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
with open(_R_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1R_RESULT = json.load(f)

EPS = 1.0  # matches H-B2-1r exactly -- same quantity, same parameter
PRIMARY_N_DIM_VALUES = (40, 50)  # user's own "primary large-N regime"
ALPHA = 0.05

# Generous grid, wider than H-B2-1r's own default -- own values there topped out at 15.68 (N=50)
GRID_RE_MIN, GRID_RE_MAX = -2.0, 25.0
GRID_IM_MAX = 10.0
GRID_N = 150


def pseudopy_alpha_eps(a: np.ndarray, eps: float = EPS) -> float:
    """alpha_eps(A) via pseudopy.NonnormalMeshgrid -- an independently-written implementation
    of the SAME quantity (verified empirically against the exact symmetric-matrix formula
    before being trusted, see claim.md)."""
    pspec = pseudopy.NonnormalMeshgrid(
        a,
        real_min=GRID_RE_MIN,
        real_max=GRID_RE_MAX,
        real_n=GRID_N,
        imag_min=-GRID_IM_MAX,
        imag_max=GRID_IM_MAX,
        imag_n=GRID_N,
    )
    mask = pspec.Vals <= eps
    if not mask.any():
        return GRID_RE_MIN  # no hit found within the grid -- same fallback convention as H-B2-1r
    return float(pspec.Real[mask].max())


def cmd_run() -> dict:
    per_n_slice = {}

    for n_dim in PRIMARY_N_DIM_VALUES:
        mine_slice = H_B2_1R_RESULT["per_n_slice"][str(n_dim)]
        alpha_mine = []
        alpha_pseudopy = []
        m1s = []
        per_seed = {}
        for seed_str, seed_data in mine_slice["per_seed"].items():
            seed = int(seed_str)
            a = multin.build_matrix_with_seed_and_n(n_dim, seed)
            a_pseudopy = pseudopy_alpha_eps(a)
            alpha_mine.append(seed_data["alpha_eps"])
            alpha_pseudopy.append(a_pseudopy)
            m1s.append(seed_data["m1"])
            per_seed[seed_str] = {
                "alpha_eps_mine": seed_data["alpha_eps"],
                "alpha_eps_pseudopy": a_pseudopy,
                "abs_diff": abs(a_pseudopy - seed_data["alpha_eps"]),
                "rel_diff": abs(a_pseudopy - seed_data["alpha_eps"]) / seed_data["alpha_eps"],
                "m1": seed_data["m1"],
            }

        rho_impl, p_impl = spearmanr(alpha_mine, alpha_pseudopy)
        rho_pseudopy_m1, p_pseudopy_m1 = spearmanr(alpha_pseudopy, m1s)
        rel_diffs = [v["rel_diff"] for v in per_seed.values()]

        pseudopy_significant_positive = bool(p_pseudopy_m1 < ALPHA and rho_pseudopy_m1 > 0)
        mine_significant_positive = bool(
            mine_slice["spearman_p"] < ALPHA and mine_slice["spearman_rho"] > 0
        )

        per_n_slice[str(n_dim)] = {
            "n_dim": n_dim,
            "n_seeds": len(alpha_mine),
            "rho_between_implementations": float(rho_impl),
            "p_between_implementations": float(p_impl),
            "median_relative_diff": float(np.median(rel_diffs)),
            "max_relative_diff": float(np.max(rel_diffs)),
            "mine_vs_m1": {
                "rho": mine_slice["spearman_rho"],
                "p": mine_slice["spearman_p"],
                "significant_positive": mine_significant_positive,
            },
            "pseudopy_vs_m1": {
                "rho": float(rho_pseudopy_m1),
                "p": float(p_pseudopy_m1),
                "significant_positive": pseudopy_significant_positive,
            },
            "verdict_agrees": mine_significant_positive == pseudopy_significant_positive,
            "per_seed": per_seed,
        }

    both_slices_pseudopy_significant = all(
        v["pseudopy_vs_m1"]["significant_positive"] for v in per_n_slice.values()
    )
    all_median_diffs_under_15pct = all(
        v["median_relative_diff"] < 0.15 for v in per_n_slice.values()
    )
    any_slice_lost_significance = any(
        not v["pseudopy_vs_m1"]["significant_positive"] for v in per_n_slice.values()
    )

    if both_slices_pseudopy_significant and all_median_diffs_under_15pct:
        verdict = "CONFIRMED"
    elif any_slice_lost_significance:
        verdict = "KILLED_OR_WEAKENED"
    else:
        verdict = "WEAKENED"

    result = {
        "config": {
            "eps": EPS,
            "n_dim_values": list(PRIMARY_N_DIM_VALUES),
            "grid": {
                "re_min": GRID_RE_MIN,
                "re_max": GRID_RE_MAX,
                "im_max": GRID_IM_MAX,
                "n": GRID_N,
            },
            "package": "pseudopy==1.2.5",
            "population_note": (
                "Same matrices as H-B2-1r (build_matrix_with_seed_and_n, seeds 0-14, N=40,50). "
                "M1 reused from H-B2-1r's own metrics/run.json, not recomputed."
            ),
        },
        "per_n_slice": per_n_slice,
        "verdict": verdict,
        "verdict_note": (
            "CONFIRMED: both large-N slices individually significant under the independent "
            "implementation AND median relative value difference < 15% -- H-B2-1r's claim "
            "strengthens. KILLED_OR_WEAKENED: at least one slice loses significance under the "
            "independent implementation -- per the user's own kill criterion. WEAKENED: both "
            "significant but with notable systematic value disagreement."
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_n_slice"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
