"""run.py — H-B2-1v: independent cross-implementation check of H-B2-1u's small-eps Kreiss
constant growth, using pseudopy.NonnormalAuto -- a genuinely DIFFERENT algorithm from both
H-B2-1u's own grid-search AND H-B2-1s's pseudopy.NonnormalMeshgrid: adaptive circles of points
placed around each eigenvalue (resolution scales with eps directly), not a fixed 2D box grid.

Reuses build_matrix_with_seed_and_n (H-B2-1m) and pseudospectral_abscissa (H-B2-1r) UNCHANGED
via dynamic import. Needs THREE compatibility shims for the unmaintained `pseudopy` package:
- shapely.ops.cascaded_union -> unary_union (same shim as H-B2-1s, shapely's own rename)
- numpy.Inf -> numpy.inf (numpy>=2.0 removed the alias; pseudopy/nonnormal.py:275 still uses it)
- matplotlib.tricontour called DIRECTLY (see EXTRACTION BUG note below), not via pseudopy's own
  contour_paths() wrapper, which crashes on modern matplotlib (TriContourSet.collections was
  removed).
All applied at the call site here, not by patching the installed package.

EXTRACTION BUG, found and fixed BEFORE trusting any comparison (Gate 3 / Positive-Control
Digitization discipline -- caught by the positive-control test itself, not discovered after):
the first draft extracted alpha_eps via `pspec.points`/`pspec.vals` with a boolean mask
(`vals <= eps`, same pattern H-B2-1s used for `NonnormalMeshgrid`). On a KNOWN-exact symmetric
positive control (ratio should be EXACTLY 1.0 for every eps), this gave a systematic ~16%
UNDERSHOOT (ratio~0.84, not converging toward 1.0 as eps shrank) -- `vals` here are not
independently-evaluated resolvent norms at arbitrary points, they are labels tied to pseudopy's
own discrete sampling circles, and naive masking does not properly interpolate the true eps-level
contour. Root cause understood by reading pseudopy's own `contour_paths()` source
(`nonnormal.py:150-160`): it calls `matplotlib.pyplot.tricontour(self.triang, self.vals,
levels=[eps])`, which does proper Delaunay-triangulated linear interpolation to find the true
eps-level contour -- NOT the raw threshold mask. Replicating that exact call directly (bypassing
pseudopy's own broken `.collections` access) and taking the max real part across ALL contour
segments gives ratio=0.9998-1.0000 on the same positive control -- essentially exact.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

import shapely.ops

if not hasattr(shapely.ops, "cascaded_union"):
    shapely.ops.cascaded_union = shapely.ops.unary_union

import matplotlib

matplotlib.use("Agg")  # headless -- this experiment only needs contour math, never a display
import matplotlib.pyplot as plt
import numpy as np

if not hasattr(np, "Inf"):
    np.Inf = np.inf

import pseudopy

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1v_multin", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_U_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-kreiss-mechanism"
with open(_U_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1U_RESULT = json.load(f)

# (n_dim, seed) -> the exact grid-search ratios_by_eps already computed in H-B2-1u, reused
# unchanged as the comparison baseline (not recomputed).
MATRICES = (
    (50, 301),  # worst-case: highest k_estimate in H-B2-1u (261.74 at eps=0.02)
    (40, 307),  # lowest k_estimate in H-B2-1u (30.20 at eps=0.02)
    (50, 304),  # mid-range k_estimate in H-B2-1u (161.07 at eps=0.02)
)

EPS_VALUES = (0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0001)

# n_circles/n_points give resolution scaling with eps directly (unlike a box grid) -- validated
# on the primary matrix (seed=301,N=50) during claim.md's disclosed exploratory pilot, WITH the
# fixed tricontour extraction (see EXTRACTION BUG note at module top): agreed with grid-search
# within <1.5% at every matching eps from 0.02 down to 0.0001, ~1.5min construction + ~1s per
# eps for the corrected extraction.
AUTO_KWARGS = {"eps_min": 0.00005, "eps_max": 0.05, "n_circles": 40, "n_points": 150}


def _alpha_eps_via_tricontour(pspec, eps: float) -> float | None:
    """Extract alpha_eps(A) = max real part of the eps-level pseudospectrum contour, via
    matplotlib's own tricontour (linear interpolation over pseudopy's Delaunay triangulation) --
    replicates pseudopy's own contour_paths() logic exactly (nonnormal.py:150-160) but bypasses
    its broken `.collections` access. Returns None if the contour is empty at this eps (honest
    gap, not silently 0)."""
    fig = plt.figure()
    try:
        cs = plt.tricontour(pspec.triang, pspec.vals, levels=[eps])
        max_re = None
        for level_segs in cs.allsegs:
            for seg in level_segs:
                seg = np.asarray(seg)
                if len(seg):
                    seg_max = float(seg[:, 0].max())
                    max_re = seg_max if max_re is None else max(max_re, seg_max)
        return max_re
    finally:
        plt.close(fig)


def pseudopy_auto_ratios(a: np.ndarray, eps_values: tuple[float, ...] = EPS_VALUES) -> dict:
    """ratio(eps) = (alpha_eps(A) - alpha(A)) / eps, computed via pseudopy.NonnormalAuto +
    direct tricontour extraction (see EXTRACTION BUG note at module top -- the naive
    points/vals mask this originally used was verified WRONG on a positive control, systematic
    ~16% undershoot; this is the fixed, positive-control-verified version)."""
    spectral_abscissa = float(np.max(np.linalg.eigvals(a).real))
    pspec = pseudopy.NonnormalAuto(a, **AUTO_KWARGS)
    ratios = {}
    for eps in eps_values:
        alpha_eps = _alpha_eps_via_tricontour(pspec, eps)
        if alpha_eps is None:
            ratios[str(eps)] = None  # empty contour at this eps -- honest gap
            continue
        ratios[str(eps)] = (alpha_eps - spectral_abscissa) / eps
    return {"spectral_abscissa": spectral_abscissa, "ratios_by_eps": ratios}


def _plateau_check(ratios: dict) -> dict:
    """Qualitative plateau call: consecutive-octave growth factor (ratio at smaller eps / ratio
    at next-larger eps) -- MCID says growth factor stabilizing below 1.3x signals a plateau; the
    raw data so far showed ~1.6-2x per halving, i.e. no plateau."""
    eps_sorted = sorted((float(e) for e in ratios if ratios[e] is not None), reverse=True)
    factors = []
    for prev_eps, cur_eps in itertools.pairwise(eps_sorted):
        prev_r = ratios[str(prev_eps)]
        cur_r = ratios[str(cur_eps)]
        if prev_r and prev_r > 0:
            factors.append(cur_r / prev_r)
    plateau = bool(factors) and all(f < 1.3 for f in factors[-2:])
    return {"growth_factors": factors, "plateau_detected": plateau}


def cmd_run() -> dict:
    per_matrix = {}
    for n_dim, seed in MATRICES:
        a = multin.build_matrix_with_seed_and_n(n_dim, seed)
        grid_search_detail = H_B2_1U_RESULT["per_n_slice"][str(n_dim)]["per_seed"][str(seed)][
            "kreiss_detail"
        ]
        grid_ratios = grid_search_detail["ratios_by_eps"]

        auto_result = pseudopy_auto_ratios(a)
        auto_ratios = auto_result["ratios_by_eps"]

        comparison = {}
        for eps in EPS_VALUES:
            eps_key = str(eps)
            grid_r = grid_ratios.get(eps_key)
            auto_r = auto_ratios.get(eps_key)
            if grid_r is None or auto_r is None:
                comparison[eps_key] = {"grid": grid_r, "pseudopy_auto": auto_r, "rel_diff": None}
                continue
            rel_diff = abs(grid_r - auto_r) / max(abs(grid_r), 1e-12)
            comparison[eps_key] = {
                "grid": grid_r,
                "pseudopy_auto": auto_r,
                "rel_diff": rel_diff,
                "agrees_within_20pct": bool(rel_diff <= 0.20),
            }

        per_matrix[f"n{n_dim}_seed{seed}"] = {
            "n_dim": n_dim,
            "seed": seed,
            "spectral_abscissa": auto_result["spectral_abscissa"],
            "comparison": comparison,
            "pseudopy_plateau_check": _plateau_check(auto_ratios),
        }

    all_agree = all(
        v["agrees_within_20pct"]
        for m in per_matrix.values()
        for v in m["comparison"].values()
        if v.get("rel_diff") is not None
    )
    any_plateau = any(m["pseudopy_plateau_check"]["plateau_detected"] for m in per_matrix.values())

    if all_agree and not any_plateau:
        verdict = "CONFIRMED_GENUINE_MATRIX_PROPERTY"
    elif any_plateau:
        verdict = "GRID_SEARCH_ARTIFACT_SUSPECTED"
    else:
        verdict = "METHODS_DISAGREE"

    result = {
        "config": {
            "matrices": [{"n_dim": n, "seed": s} for n, s in MATRICES],
            "eps_values": list(EPS_VALUES),
            "auto_kwargs": AUTO_KWARGS,
        },
        "per_matrix": per_matrix,
        "all_agree_within_20pct": all_agree,
        "any_plateau_detected": any_plateau,
        "verdict": verdict,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_matrix"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
