"""run.py — H-B3-1o: does Peter pH's 100-day-late total-persistence detection (H-B3-1g)
reflect a genuinely delayed raw topological signal, or an artifact of the tau-accumulation
/ self-calibrated-null detection method -- the last unexecuted item on H-B3-1g's own
Relaxation Map ("cheapest immediate follow-up if this branch is pursued").

Reuses UNCHANGED via dynamic import: peter.load_daily_series, obrien.WINDOW_FRAC,
obrien.EMBED_DIM, obrien.EMBED_DELAY, obrien.betti1_total_persistence_series. H-B3-1g's own
stored crossing dates (metrics/run.json) are reused unchanged, not recomputed.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_B_DIR = HERE.parent / "20260906-may1972-tda-ews-obrienlakes"
_SPEC_B = importlib.util.spec_from_file_location("chernoff_1o_obrien", _B_DIR / "run.py")
obrien = importlib.util.module_from_spec(_SPEC_B)
_SPEC_B.loader.exec_module(obrien)

_P_DIR = HERE.parent / "20260906-may1972-tda-ews-peterlake"
_SPEC_P = importlib.util.spec_from_file_location("chernoff_1o_peter", _P_DIR / "run.py")
peter = importlib.util.module_from_spec(_SPEC_P)
_SPEC_P.loader.exec_module(peter)

_G_DIR = HERE.parent / "20260906-lakes-tda-ews-total-persistence-v1g"
with open(_G_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B3_1G_RESULT = json.load(f)

POSITIVE_CONTROL_GATE_DAYS = 20.0  # doSat's half-rise date must be within this of its
# own tda_crossing (172) for the half-rise metric to be trusted at all -- see claim.md


def half_rise_date(series: np.ndarray, window_end_dates: np.ndarray) -> float | None:
    """First date at which `series` reaches >=50% of its own [min,max] range within the
    observed window -- a simple, scale-robust proxy for "when the raw signal structurally
    changes", independent of the tau-accumulation / surrogate-crossing machinery."""
    valid = ~np.isnan(series)
    if not np.any(valid):
        return None
    vals = series[valid]
    dates = window_end_dates[valid]
    lo, hi = float(np.min(vals)), float(np.max(vals))
    if hi <= lo:
        return None
    half = lo + 0.5 * (hi - lo)
    hit = np.where(vals >= half)[0]
    return float(dates[hit[0]]) if hit.size else None


def raw_total_persistence_for(var: str, lake: str) -> tuple[np.ndarray, float | None]:
    season_time, x, _transition_time = peter.load_daily_series(var, lake)
    n = len(x)
    window = round(obrien.WINDOW_FRAC * n)
    window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)
    series = obrien.betti1_total_persistence_series(x, window)
    window_end_dates = season_time[window - 1 :]
    hr = half_rise_date(series, window_end_dates)
    return series, hr


def cmd_run() -> dict:
    dosat_stored = H_B3_1G_RESULT["results"]["peterlake_Peter_doSat"]
    ph_stored = H_B3_1G_RESULT["results"]["peterlake_Peter_pH"]

    _, dosat_half_rise = raw_total_persistence_for("doSat", "Peter")
    _, ph_half_rise = raw_total_persistence_for("pH", "Peter")

    dosat_tda_crossing = dosat_stored["tda_betti_crossing"]
    dosat_gate_distance = (
        abs(dosat_half_rise - dosat_tda_crossing)
        if (dosat_half_rise is not None and dosat_tda_crossing is not None)
        else None
    )
    positive_control_gate_passes = (
        dosat_gate_distance is not None and dosat_gate_distance <= POSITIVE_CONTROL_GATE_DAYS
    )

    ph_classical_crossing = ph_stored["classical_earliest_crossing"]
    ph_tda_crossing = ph_stored["tda_betti_crossing"]

    dist_to_classical = (
        abs(ph_half_rise - ph_classical_crossing)
        if (ph_half_rise is not None and ph_classical_crossing is not None)
        else None
    )
    dist_to_tda_crossing = (
        abs(ph_half_rise - ph_tda_crossing)
        if (ph_half_rise is not None and ph_tda_crossing is not None)
        else None
    )

    if not positive_control_gate_passes:
        verdict = "METRIC_UNRELIABLE"
    elif dist_to_classical is None or dist_to_tda_crossing is None:
        verdict = "METRIC_UNRELIABLE"
    elif dist_to_classical < dist_to_tda_crossing:
        verdict = "ARTIFACT_HYPOTHESIS_SUPPORTED"
    else:
        verdict = "GENUINE_DELAY_HYPOTHESIS_SUPPORTED"

    result = {
        "positive_control": {
            "dosat_half_rise_date": dosat_half_rise,
            "dosat_tda_crossing": dosat_tda_crossing,
            "dosat_gate_distance_days": dosat_gate_distance,
            "gate_threshold_days": POSITIVE_CONTROL_GATE_DAYS,
            "gate_passes": positive_control_gate_passes,
        },
        "primary": {
            "ph_half_rise_date": ph_half_rise,
            "ph_classical_crossing": ph_classical_crossing,
            "ph_tda_crossing": ph_tda_crossing,
            "distance_to_classical_anchor": dist_to_classical,
            "distance_to_tda_crossing_anchor": dist_to_tda_crossing,
        },
        "verdict": verdict,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
