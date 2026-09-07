"""H-B3-1l: peak-tau (argmax) reporting instead of first-crossing -- H-B3-1b's own Relaxation
Map Row 3 ("cheapest -- no new statistical machinery, just report peaks instead of first-
crossings"), the one item left untested after Row 1 (surrogate null, tested via H-B3-1c/d/e,
REJECTED) and before Row 2 (change-point co-requirement, still untested).

Reuses H-B3-1/H-B3-1b's own pipeline (load_series, rolling_stat, betti1_entropy_series,
expanding_kendall_tau, LAKES, WINDOW_FRAC, EMBED_DIM, EMBED_DELAY, DATA) UNCHANGED via dynamic
import -- Minimal Relaxation Rule: only the REPORTING step (first_crossing -> peak_index) and the
resulting verdict logic change.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pyreadr

HERE = Path(__file__).resolve().parent

_B_DIR = HERE.parent / "20260906-may1972-tda-ews-obrienlakes"
_SPEC_B = importlib.util.spec_from_file_location("lakes_tda_ews_obrienlakes_run", _B_DIR / "run.py")
obrien = importlib.util.module_from_spec(_SPEC_B)
_SPEC_B.loader.exec_module(obrien)

METRICS = HERE / "metrics"


def peak_index(tau_series: np.ndarray) -> int | None:
    """argmax of `tau_series`, ignoring NaN. None if the whole series is NaN."""
    valid = ~np.isnan(tau_series)
    if not np.any(valid):
        return None
    idx = np.where(valid)[0]
    return int(idx[np.argmax(tau_series[idx])])


def cmd_run() -> dict:
    rdata = pyreadr.read_r(str(obrien.DATA))
    results = {}

    for lake_key, cfg in obrien.LAKES.items():
        dates, pca1 = obrien.load_series(rdata, lake_key)
        n = len(pca1)
        window = round(obrien.WINDOW_FRAC * n)
        window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)

        ac1 = obrien.rolling_stat(pca1, window, "ac1")
        var = obrien.rolling_stat(pca1, window, "var")
        betti = obrien.betti1_entropy_series(pca1, window)

        tau_ac1 = obrien.expanding_kendall_tau(ac1)
        tau_var = obrien.expanding_kendall_tau(var)
        tau_betti = obrien.expanding_kendall_tau(betti)

        window_end_dates = dates[window - 1 :]

        def peak_date(tau_series: np.ndarray) -> float | None:
            idx = peak_index(tau_series)
            return float(window_end_dates[idx]) if idx is not None else None

        peak_ac1 = peak_date(tau_ac1)
        peak_var = peak_date(tau_var)
        peak_betti = peak_date(tau_betti)

        transition = cfg["transition"]
        classical_candidates = [c for c in (peak_ac1, peak_var) if c is not None]
        if transition is not None and classical_candidates:
            # Classical's own best case: whichever of AC1/var peaks CLOSEST to the true
            # transition -- the fair analogue of the original code's "earliest crossing wins"
            # convention, adapted to a proximity (not speed) comparison.
            classical_peak = min(classical_candidates, key=lambda d: abs(d - transition))
        elif classical_candidates:
            classical_peak = min(classical_candidates)  # descriptive fallback, no transition
        else:
            classical_peak = None

        lead_months = None
        if peak_betti is not None and classical_peak is not None:
            lead_months = (classical_peak - peak_betti) * 12.0

        entry = {
            "role": cfg["role"],
            "n_points": n,
            "window": window,
            "documented_transition": transition,
            "tda_betti_peak_date": peak_betti,
            "classical_ac1_peak_date": peak_ac1,
            "classical_var_peak_date": peak_var,
            "classical_peak_date_used": classical_peak,
            "peak_lead_months_tda_minus_classical": lead_months,
        }
        if transition is not None:
            entry["tda_distance_to_transition_years"] = (
                abs(peak_betti - transition) if peak_betti is not None else None
            )
            entry["classical_distance_to_transition_years"] = (
                abs(classical_peak - transition) if classical_peak is not None else None
            )
        results[lake_key] = entry

    lz = results["lower_zurich"]
    tda_dist = lz.get("tda_distance_to_transition_years")
    classical_dist = lz.get("classical_distance_to_transition_years")
    tda_peak = lz["tda_betti_peak_date"]
    classical_peak = lz["classical_peak_date_used"]

    if None in (tda_dist, classical_dist, tda_peak, classical_peak):
        verdict = "AMBIGUOUS"
    elif tda_dist < classical_dist and tda_peak <= classical_peak:
        verdict = "CONFIRMED"
    else:
        verdict = "REJECTED"

    negative_control_leads = {
        lake: results[lake]["peak_lead_months_tda_minus_classical"]
        for lake in ("windermere", "loch_leven")
    }
    lz_lead = lz["peak_lead_months_tda_minus_classical"]
    same_direction_as_positive = {
        lake: (lead is not None and lz_lead is not None and (lead > 0) == (lz_lead > 0))
        for lake, lead in negative_control_leads.items()
    }

    out = {
        "config": {
            "window_frac": obrien.WINDOW_FRAC,
            "embed_dim": obrien.EMBED_DIM,
            "embed_delay": obrien.EMBED_DELAY,
            "detection_rule": "peak (argmax) of expanding Kendall tau, no threshold",
        },
        "results": results,
        "verdict": verdict,
        "negative_control_leads_months": negative_control_leads,
        "negative_control_same_direction_as_lower_zurich": same_direction_as_positive,
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
