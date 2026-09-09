"""run.py -- H-B3-2: PH_0 chirality-excess (Baryshnikov 2022) vs simple trend and
classical time-reversal-asymmetry, on the O'Brien et al. lake series H-B3-1 used.

Reuses UNCHANGED, via distinct-name import (avoids the run.py-collision bug
caught in H-CAT37-2): load_series, expanding_kendall_tau, first_crossing,
ar1_surrogate, floor_false_positive_rate, WINDOW_FRAC, LAKES, TAU_THRESHOLD.
"""

from __future__ import annotations

import importlib.util
import json
import warnings
from pathlib import Path

import numpy as np
import pyreadr
from scipy.stats import linregress

HERE = Path(__file__).resolve().parent
B3_1_DIR = HERE.parent / "20260906-may1972-tda-ews-obrienlakes"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


b3_1 = _load_module("h_b3_2_base", B3_1_DIR / "run.py")

DATA = B3_1_DIR / "data" / "wrangled_genus_plank_data_public.Rdata"
LAKES = b3_1.LAKES
WINDOW_FRAC = b3_1.WINDOW_FRAC
TAU_THRESHOLD = b3_1.TAU_THRESHOLD


# ───────────────────────── PH_0 chirality (Baryshnikov Def 2.5/2.6) ─────────────────────────
def _extrema_indices(w: np.ndarray) -> list[int]:
    """Endpoints (always "half-extrema" relative to their one interior
    neighbor, per the paper's own interval convention, Section 2.4.1) +
    interior local min/max via strict sign-change detection."""
    n = len(w)
    idx = [0]
    for i in range(1, n - 1):
        left, right = w[i] - w[i - 1], w[i + 1] - w[i]
        if left == 0 or right == 0:
            continue  # plateau point, generic real data essentially never hits this exactly
        if (left > 0) != (right > 0):
            idx.append(i)
    idx.append(n - 1)
    return idx


def merge_tree_bars(w: np.ndarray) -> list[tuple[int, int, float, float]]:
    """0-dim persistence bars of a 1D sequence via recursive stem-pruning,
    implemented DIRECTLY per Baryshnikov 2022 Section 2.2.1: find the GLOBAL
    min and GLOBAL max among the current point set, record that pair as a
    bar (the "stem"), remove both points, and recurse SEPARATELY on each
    maximal contiguous run of the remaining points (the "forest" left after
    pruning the stem).

    Caught and fixed this session (reviewer pass): an earlier version used a
    different, non-equivalent heuristic (repeatedly pairing the two INDEX-
    ADJACENT points with smallest value-difference, working inward) that
    silently DROPPED the window's global minimum whenever the total extrema
    count was odd (~55% of real windows in the actual dataset tested) --
    caught by an independent reviewer via a hand-constructed 7-point counter-
    example, not found by the original test suite (whose count-invariant
    check used floor division, which silently absorbs a dropped point).

    This global-min/max-first recursive version has the SAME odd-count
    boundary case (a real, structural property of 0-dim persistence on an
    interval whose two endpoints are the same extremum "type" -- the paper's
    own Section 2.4 acknowledges this needs a "stitching" transformation for
    conventions other than "global min at left, global max at right").
    Rather than silently dropping the point OR inventing a fabricated data
    point to force parity, the leftover point (if any) is returned as its
    own explicit entry in `unmatched_indices` on the wrapper -- see
    `merge_tree_bars_full`. `merge_tree_bars` itself returns bars only, for
    callers (chirality_excess) that intentionally exclude the unmatched
    point rather than inventing a pairing for it.
    """
    return merge_tree_bars_full(w)[0]


def merge_tree_bars_full(
    w: np.ndarray,
) -> tuple[list[tuple[int, int, float, float]], list[int]]:
    """Returns (bars, unmatched_indices). unmatched_indices has at most 1
    entry per recursive branch that hits the odd-count boundary case."""
    idx = _extrema_indices(w)
    return _recursive_pairing(w, idx)


def _recursive_pairing(
    w: np.ndarray, indices: list[int]
) -> tuple[list[tuple[int, int, float, float]], list[int]]:
    if len(indices) == 0:
        return [], []
    if len(indices) == 1:
        return [], [indices[0]]
    vals = [w[i] for i in indices]
    min_pos_in_list = int(np.argmin(vals))
    max_pos_in_list = int(np.argmax(vals))
    min_idx, max_idx = indices[min_pos_in_list], indices[max_pos_in_list]
    b_idx, d_idx = (min_idx, max_idx)  # min_idx IS the lower value by construction
    bars = [(b_idx, d_idx, float(w[b_idx]), float(w[d_idx]))]
    remove_positions = {min_pos_in_list, max_pos_in_list}
    unmatched: list[int] = []
    # split remaining indices into maximal contiguous runs (by ORIGINAL LIST
    # position, not by index value), matching "the forest left after pruning
    # the stem" -- each run recurses independently.
    run: list[int] = []
    for pos, i in enumerate(indices):
        if pos in remove_positions:
            if run:
                sub_bars, sub_unmatched = _recursive_pairing(w, run)
                bars.extend(sub_bars)
                unmatched.extend(sub_unmatched)
                run = []
            continue
        run.append(i)
    if run:
        sub_bars, sub_unmatched = _recursive_pairing(w, run)
        bars.extend(sub_bars)
        unmatched.extend(sub_unmatched)
    return bars, unmatched


def chirality_excess(w: np.ndarray) -> float:
    """(n_N - n_L) / (n_N + n_L). L: min precedes max in time (s<t, min_idx<max_idx).
    N: max precedes min (s>t). Definition 2.6, Baryshnikov 2022."""
    bars = merge_tree_bars(w)
    if not bars:
        return 0.0
    n_l = sum(1 for b_idx, d_idx, _, _ in bars if b_idx < d_idx)
    n_n = sum(1 for b_idx, d_idx, _, _ in bars if b_idx > d_idx)
    total = n_l + n_n
    return float((n_n - n_l) / total) if total else 0.0


def chirality_excess_series(x: np.ndarray, window: int) -> np.ndarray:
    out = np.full(len(x) - window + 1, np.nan)
    for i in range(len(out)):
        out[i] = chirality_excess(x[i : i + window])
    return out


# ───────────────────────── Baselines ─────────────────────────
def trend_slope_series(x: np.ndarray, window: int) -> np.ndarray:
    out = np.full(len(x) - window + 1, np.nan)
    t = np.arange(window)
    for i in range(len(out)):
        out[i] = linregress(t, x[i : i + window]).slope
    return out


def time_reversal_asymmetry_series(x: np.ndarray, window: int, tau: int = 1) -> np.ndarray:
    """TR(tau) = mean((x_{t+tau} - x_t)^3), classical nonlinear-TSA irreversibility
    statistic (Diks et al. 1995 and standard practice)."""
    out = np.full(len(x) - window + 1, np.nan)
    for i in range(len(out)):
        w = x[i : i + window]
        diffs = w[tau:] - w[:-tau]
        out[i] = float(np.mean(diffs**3))
    return out


# ───────────── V1 per-series calibrated crossing (generic stat_fn) ─────────────
# The base module's own `surrogate_null_curve` is hardcoded to kind in {"ac1","var","betti"} --
# not reusable as-is for an arbitrary new stat_fn without editing that module (avoided, per
# Minimal Relaxation Rule -- the closed arc's own code stays unchanged). This mirrors its EXACT
# logic (per-timepoint (1-alpha) percentile of the surrogate-null expanding-tau curve), just
# generalized to accept any `stat_fn(x, window) -> series`.
def surrogate_null_curve_generic(
    x: np.ndarray, window: int, stat_fn, reps: int, seed: int, alpha: float = 0.05
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n_out = len(x) - window + 1
    curves = np.full((reps, n_out), np.nan)
    for r in range(reps):
        surrogate = b3_1.ar1_surrogate(x, rng)
        curves[r] = b3_1.expanding_kendall_tau(stat_fn(surrogate, window))
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="All-NaN slice encountered")
        return np.nanpercentile(curves, 100 * (1 - alpha), axis=0)


def surrogate_crossing_generic(real_tau: np.ndarray, null_curve: np.ndarray) -> int | None:
    valid = ~np.isnan(real_tau) & ~np.isnan(null_curve)
    hit = np.where(valid & (real_tau > null_curve))[0]
    return int(hit[0]) if hit.size else None


def cmd_run() -> dict:
    rdata = pyreadr.read_r(str(DATA))
    results = {"claim": "H-B3-2 PH_0 chirality-excess vs trend/TR-asymmetry baselines"}

    for lake_key, cfg in LAKES.items():
        _dates, pca1 = b3_1.load_series(rdata, lake_key)
        window = max(8, round(WINDOW_FRAC * len(pca1)))

        chir = chirality_excess_series(pca1, window)
        trend = trend_slope_series(pca1, window)
        tr_asym = time_reversal_asymmetry_series(pca1, window)

        tau_chir = b3_1.expanding_kendall_tau(chir)
        tau_trend = b3_1.expanding_kendall_tau(trend)
        tau_asym = b3_1.expanding_kendall_tau(tr_asym)

        cross_chir = b3_1.first_crossing(tau_chir, TAU_THRESHOLD)
        cross_trend = b3_1.first_crossing(tau_trend, TAU_THRESHOLD)
        cross_asym = b3_1.first_crossing(tau_asym, TAU_THRESHOLD)

        floor_chir = _floor_rate(pca1, window, chirality_excess_series, reps=30, seed=42)
        floor_trend = _floor_rate(pca1, window, trend_slope_series, reps=30, seed=43)
        floor_asym = _floor_rate(
            pca1, window, lambda x, w: time_reversal_asymmetry_series(x, w), reps=30, seed=44
        )

        # V1-style per-series calibrated crossing (see module docstring section) --
        # the arc's own established fix for the fixed-threshold floor problem,
        # generalized to these three statistics instead of the base module's
        # hardcoded ac1/var/betti kinds.
        null_chir = surrogate_null_curve_generic(pca1, window, chirality_excess_series, 30, 52)
        null_trend = surrogate_null_curve_generic(pca1, window, trend_slope_series, 30, 53)
        null_asym = surrogate_null_curve_generic(
            pca1, window, time_reversal_asymmetry_series, 30, 54
        )
        v1_cross_chir = surrogate_crossing_generic(tau_chir, null_chir)
        v1_cross_trend = surrogate_crossing_generic(tau_trend, null_trend)
        v1_cross_asym = surrogate_crossing_generic(tau_asym, null_asym)

        results[lake_key] = {
            "role": cfg["role"],
            "n_points": len(pca1),
            "window": window,
            "first_crossing_index": {
                "chirality_excess": cross_chir,
                "trend_slope": cross_trend,
                "time_reversal_asymmetry": cross_asym,
            },
            "v1_per_series_calibrated_crossing_index": {
                "chirality_excess": v1_cross_chir,
                "trend_slope": v1_cross_trend,
                "time_reversal_asymmetry": v1_cross_asym,
            },
            "floor_false_positive_rate": {
                "chirality_excess": floor_chir,
                "trend_slope": floor_trend,
                "time_reversal_asymmetry": floor_asym,
            },
        }

    Path(HERE / "metrics").mkdir(exist_ok=True)
    with open(HERE / "metrics" / "run.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(json.dumps(results, indent=2, default=str))
    return results


def _floor_rate(x: np.ndarray, window: int, stat_fn, reps: int, seed: int) -> float:
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(reps):
        surrogate = b3_1.ar1_surrogate(x, rng)
        stat = stat_fn(surrogate, window)
        tau = b3_1.expanding_kendall_tau(stat)
        if b3_1.first_crossing(tau, TAU_THRESHOLD) is not None:
            hits += 1
    return hits / reps


if __name__ == "__main__":
    cmd_run()
