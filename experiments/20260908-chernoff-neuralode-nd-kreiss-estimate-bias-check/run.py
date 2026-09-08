"""run.py — H-B2-1y: does the shallow K(A) estimate's underestimation bias grow with the
matrix's own apparent K(A) -- and if so, does a deeper measurement pull the fitted M1~K(A)
exponent back toward 1 (linear, classical) from the ~2.35 found in H-B2-1x?

Reuses UNCHANGED via dynamic import: build_matrix_with_seed_and_n (H-B2-1m). SHALLOW K(A) is not
recomputed -- pulled directly from H-B2-1x's own stored metrics/run.json (train_data), Minimal
Relaxation Rule. DEEP K(A) reuses H-B2-1v's own validated technique (pseudopy.NonnormalAuto +
direct matplotlib.tricontour extraction, positive-control-verified there), with eps range
extended roughly an order of magnitude deeper than H-B2-1v's own convergence check.

Needs the same 3 pseudopy/matplotlib compat shims as H-B2-1v (shapely rename, np.Inf removal,
direct tricontour call bypassing pseudopy's own broken .collections access).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import shapely.ops

if not hasattr(shapely.ops, "cascaded_union"):
    shapely.ops.cascaded_union = shapely.ops.unary_union

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

if not hasattr(np, "Inf"):
    np.Inf = np.inf

import pseudopy

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1y_multin", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

# NOTE: shallow_k is NOT recomputed here -- pulled directly from H-B2-1x's own stored
# metrics/run.json (train_data), Minimal Relaxation Rule. kreiss_constant_estimate (H-B2-1u) is
# therefore not imported; only build_matrix_with_seed_and_n is reused for the deep re-measurement.
_X_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-tighter-predictor-robustness"
with open(_X_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1X_RESULT = json.load(f)

# 16 matrices, stratified across H-B2-1x's own TRAIN population's K(A) range (30.2-221.5) --
# EXACT (n_dim, seed) pairs already studied, no new matrices.
SAMPLE_MATRICES = (
    (40, 307),
    (40, 326),
    (40, 334),
    (40, 337),
    (40, 332),
    (40, 321),
    (50, 309),
    (40, 318),
    (40, 339),
    (40, 325),
    (40, 306),
    (50, 336),
    (50, 306),
    (40, 322),
    (50, 304),
    (50, 329),
)

# Extended an order of magnitude deeper than H-B2-1v's own check (which used eps_min=0.00005).
# VERIFIED after running (not assumed): all 16/16 matrices hit their max ratio at the SMALLEST
# tested eps (0.00001), still climbing steeply with no inflection -- "deep_k" here is a LESS
# shallow lower bound, not a converged value (same pattern H-B2-1u/1v found for the arc's own
# shallow estimate). This means the bias factors and the corrected exponent in decision.md are
# themselves conservative -- the true correction is likely larger, not smaller. See decision.md
# Honest Caveat #2 for the full account.
DEEP_AUTO_KWARGS = {"eps_min": 0.000005, "eps_max": 0.05, "n_circles": 50, "n_points": 150}
DEEP_EPS_VALUES = (0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0001, 0.00005, 0.00001)


def _alpha_eps_via_tricontour(pspec, eps: float) -> float | None:
    """Identical technique to H-B2-1v's own validated helper (positive-control ratio
    0.9998-1.0000) -- max real part across all eps-level contour segments."""
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


def deep_kreiss_estimate(a: np.ndarray) -> dict:
    spectral_abscissa = float(np.max(np.linalg.eigvals(a).real))
    pspec = pseudopy.NonnormalAuto(a, **DEEP_AUTO_KWARGS)
    ratios = {}
    for eps in DEEP_EPS_VALUES:
        alpha_eps = _alpha_eps_via_tricontour(pspec, eps)
        if alpha_eps is None:
            ratios[str(eps)] = None
            continue
        ratios[str(eps)] = (alpha_eps - spectral_abscissa) / eps
    valid = [v for v in ratios.values() if v is not None]
    k_deep = max(valid) if valid else None
    return {"spectral_abscissa": spectral_abscissa, "ratios_by_eps": ratios, "k_deep": k_deep}


def _fit_ols(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    coeffs, *_ = np.linalg.lstsq(x, y, rcond=None)
    return coeffs


def cmd_run() -> dict:
    per_matrix = {}
    for n_dim, seed in SAMPLE_MATRICES:
        train_row = next(
            r for r in H_B2_1X_RESULT["train_data"] if r["n_dim"] == n_dim and r["seed"] == seed
        )
        shallow_k = train_row["k_estimate"]
        m1 = train_row["m1"]

        a = multin.build_matrix_with_seed_and_n(n_dim, seed)
        deep_result = deep_kreiss_estimate(a)
        deep_k = deep_result["k_deep"]

        bias_factor = (deep_k / shallow_k) if (deep_k is not None and shallow_k > 0) else None

        per_matrix[f"n{n_dim}_seed{seed}"] = {
            "n_dim": n_dim,
            "seed": seed,
            "shallow_k": shallow_k,
            "deep_k": deep_k,
            "bias_factor": bias_factor,
            "m1": m1,
            "deep_ratios_by_eps": deep_result["ratios_by_eps"],
        }

    valid_rows = [r for r in per_matrix.values() if r["bias_factor"] is not None]
    log_shallow_k = np.log(np.array([r["shallow_k"] for r in valid_rows]))
    log_bias = np.log(np.array([r["bias_factor"] for r in valid_rows]))
    log_deep_k = np.log(np.array([r["deep_k"] for r in valid_rows]))
    log_m1 = np.log(np.array([r["m1"] for r in valid_rows]))

    # Does bias grow with shallow_K?
    x_bias = np.column_stack([np.ones_like(log_shallow_k), log_shallow_k])
    bias_coeffs = _fit_ols(x_bias, log_bias)
    bias_slope = float(bias_coeffs[1])
    resid_bias = log_bias - x_bias @ bias_coeffs
    ss_res = float(np.sum(resid_bias**2))
    ss_tot = float(np.sum((log_bias - log_bias.mean()) ** 2))
    bias_r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    # Matched exponent comparison on the SAME subset: shallow-K-only vs deep-K-only (single
    # feature, no N_DIM term -- H-B2-1x already showed N_DIM is not well-constrained anyway).
    x_shallow = np.column_stack([np.ones_like(log_shallow_k), log_shallow_k])
    shallow_coeffs = _fit_ols(x_shallow, log_m1)
    shallow_exponent = float(shallow_coeffs[1])

    x_deep = np.column_stack([np.ones_like(log_deep_k), log_deep_k])
    deep_coeffs = _fit_ols(x_deep, log_m1)
    deep_exponent = float(deep_coeffs[1])

    exponent_moved_toward_linear = bool(abs(deep_exponent - 1.0) < abs(shallow_exponent - 1.0))
    bias_grows_with_k = bool(bias_slope > 0.1)  # a real, non-negligible positive trend

    if bias_grows_with_k and exponent_moved_toward_linear:
        verdict = "ARTIFACT_HYPOTHESIS_SUPPORTED"
    elif not bias_grows_with_k and not exponent_moved_toward_linear:
        verdict = "GENUINE_SUPERLINEAR_PATTERN_SURVIVES"
    else:
        verdict = "MIXED_INCONCLUSIVE"

    result = {
        "config": {
            "n_matrices": len(SAMPLE_MATRICES),
            "n_valid": len(valid_rows),
            "deep_auto_kwargs": DEEP_AUTO_KWARGS,
        },
        "per_matrix": per_matrix,
        "bias_vs_shallow_k": {
            "slope": bias_slope,
            "r2": bias_r2,
            "intercept": float(bias_coeffs[0]),
        },
        "shallow_k_exponent_on_subset": shallow_exponent,
        "deep_k_exponent_on_subset": deep_exponent,
        "exponent_moved_toward_linear": exponent_moved_toward_linear,
        "bias_grows_with_k": bias_grows_with_k,
        "verdict": verdict,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_matrix"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
