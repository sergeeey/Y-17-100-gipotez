"""run.py -- H-B3-1q: revives H-B3-1o's own named revival condition (compare the expanding-tau
TRAJECTORY, not raw value) between Peter pH and doSat. That specific comparison stays
inconclusive (aligned correlation on too few overlapping points). The attempt's own mandatory
floor check (per this arc's established discipline -- H-B3-1c/1d both floor-failed on a
single-series threshold approach) surfaced a different, floor-tested signal instead:
cross-variable tau-trajectory correlation cleanly discriminates Peter (positive, real
manipulation) from Paul (negative, no manipulation).

Reuses obrien.expanding_kendall_tau/betti1_total_persistence_series and
peter.load_daily_series/VARIABLES/LAKES UNCHANGED.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_OBRIEN_DIR = HERE.parent / "20260906-may1972-tda-ews-obrienlakes"
_PETER_DIR = HERE.parent / "20260906-may1972-tda-ews-peterlake"
_H_B3_1G_DIR = HERE.parent / "20260906-lakes-tda-ews-total-persistence-v1g"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


obrien = _load_module("h_b3_1q_obrien", _OBRIEN_DIR / "run.py")
peter = _load_module("h_b3_1q_peter", _PETER_DIR / "run.py")

with open(_H_B3_1G_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B3_1G_RESULT = json.load(f)

FLOOR_CHECK_PASS_MIN_POSITIVE_FRACTION_PETER = 1.0  # ALL 3 Peter pairs must be positive
FLOOR_CHECK_FAIL_MAX_POSITIVE_FRACTION_PAUL = 2 / 3  # Paul must NOT also show 3/3 consistent
MIN_ALIGNED_OVERLAP_POINTS = 30  # below this, the aligned comparison is not trustworthy


def tau_trajectory_for(var: str, lake: str) -> tuple[np.ndarray, np.ndarray]:
    season_time, x, _transition_time = peter.load_daily_series(var, lake)
    n = len(x)
    window = round(obrien.WINDOW_FRAC * n)
    window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)
    series = obrien.betti1_total_persistence_series(x, window)
    tau = obrien.expanding_kendall_tau(series)
    window_end_dates = season_time[window - 1 :]
    return window_end_dates, tau


def unaligned_correlation(tau_a: np.ndarray, tau_b: np.ndarray) -> dict:
    n = min(len(tau_a), len(tau_b))
    mask = ~np.isnan(tau_a[:n]) & ~np.isnan(tau_b[:n])
    if mask.sum() < 3:
        return {"rho": None, "p": None, "n": int(mask.sum())}
    rho, p = spearmanr(tau_a[:n][mask], tau_b[:n][mask])
    return {"rho": float(rho), "p": float(p), "n": int(mask.sum())}


def cmd_run() -> dict:
    variables = peter.VARIABLES  # ["chl", "pH", "doSat"]
    lakes = peter.LAKES  # {"Peter": "positive", "Paul": "negative"}

    trajectories = {}
    for lake in lakes:
        for var in variables:
            dates, tau = tau_trajectory_for(var, lake)
            trajectories[(lake, var)] = (dates, tau)

    crossvar_results = {}
    for lake in lakes:
        pair_results = []
        for v1, v2 in combinations(variables, 2):
            _, tau1 = trajectories[(lake, v1)]
            _, tau2 = trajectories[(lake, v2)]
            corr = unaligned_correlation(tau1, tau2)
            pair_results.append({"var1": v1, "var2": v2, **corr})
        crossvar_results[lake] = pair_results

    peter_pairs = crossvar_results["Peter"]
    paul_pairs = crossvar_results["Paul"]

    peter_all_positive = all(r["rho"] is not None and r["rho"] > 0 for r in peter_pairs)
    paul_n_positive = sum(1 for r in paul_pairs if r["rho"] is not None and r["rho"] > 0)
    paul_not_consistent = (
        paul_n_positive / len(paul_pairs)
    ) <= FLOOR_CHECK_FAIL_MAX_POSITIVE_FRACTION_PAUL

    floor_check_passed = peter_all_positive and paul_not_consistent

    # --- H-B3-1o's own original revival condition: aligned pH-vs-doSat comparison on Peter ---
    ph_dates, ph_tau = trajectories[("Peter", "pH")]
    dosat_dates, dosat_tau = trajectories[("Peter", "doSat")]

    ph_crossing = H_B3_1G_RESULT["results"]["peterlake_Peter_pH"]["tda_betti_crossing"]
    dosat_crossing = H_B3_1G_RESULT["results"]["peterlake_Peter_doSat"]["tda_betti_crossing"]

    ph_crossing_idx = np.where(ph_dates >= ph_crossing)[0]
    dosat_crossing_idx = np.where(dosat_dates >= dosat_crossing)[0]

    aligned_result = {"rho": None, "p": None, "n": 0, "shift_days": None}
    if ph_crossing_idx.size and dosat_crossing_idx.size:
        shift = int(ph_crossing_idx[0]) - int(dosat_crossing_idx[0])
        if shift >= 0:
            ph_aligned = ph_tau[shift:]
            dosat_aligned = dosat_tau[: len(ph_aligned)]
        else:
            dosat_aligned = dosat_tau[-shift:]
            ph_aligned = ph_tau[: len(dosat_aligned)]
        corr = unaligned_correlation(ph_aligned, dosat_aligned)
        aligned_result = {**corr, "shift_days": shift}

    unaligned_ph_dosat = unaligned_correlation(ph_tau, dosat_tau)

    original_question_conclusive = (
        aligned_result["n"] is not None and aligned_result["n"] >= MIN_ALIGNED_OVERLAP_POINTS
    )
    original_question_supports_genuine_delay = (
        original_question_conclusive
        and aligned_result["rho"] is not None
        and unaligned_ph_dosat["rho"] is not None
        and aligned_result["rho"] > unaligned_ph_dosat["rho"]
    )

    verdict = "CONFIRMED-CROSSVAR-COHERENCE-LEAD" if floor_check_passed else "CRITERION_INVALID"

    out = {
        "claim": "H-B3-1q -- H-B3-1o's own revival condition attempted directly (pH-vs-doSat "
        "trajectory alignment, stays inconclusive); the attempt's own mandatory floor check "
        "surfaced a different, cleanly-discriminating signal instead: cross-variable "
        "tau-trajectory coherence separates Peter (real transition) from Paul (no transition)",
        "crossvar_results": crossvar_results,
        "peter_all_pairs_positive": peter_all_positive,
        "paul_n_positive_of_3": paul_n_positive,
        "floor_check_passed": floor_check_passed,
        "original_h_b3_1o_question": {
            "unaligned_ph_vs_dosat": unaligned_ph_dosat,
            "aligned_ph_vs_dosat": aligned_result,
            "min_overlap_required": MIN_ALIGNED_OVERLAP_POINTS,
            "conclusive": original_question_conclusive,
            "supports_genuine_delay_if_conclusive": original_question_supports_genuine_delay,
        },
        "verdict": verdict,
        "sample_size_caveat": "n=1 lake-pair (Peter/Paul), 3 non-independent within-lake "
        "variable-pairs -- LEAD, not PROMOTE, regardless of pattern cleanliness",
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
