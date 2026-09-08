"""run.py — H-B3-1n: does H-B3-1l's +50.0-month TDA-vs-classical peak-lead on Lower Zurich
arise at comparable magnitude from mechanism-free AR(1) surrogates of the same series?

Reuses UNCHANGED via dynamic import: obrien.ar1_surrogate, obrien.rolling_stat,
obrien.betti1_entropy_series, obrien.expanding_kendall_tau, obrien.load_series
(H-B3-1/obrienlakes) and H-B3-1l's own peak_index() (same-file reuse, not reimplemented).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pyreadr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_B_DIR = HERE.parent / "20260906-may1972-tda-ews-obrienlakes"
_SPEC_B = importlib.util.spec_from_file_location("chernoff_1n_obrien", _B_DIR / "run.py")
obrien = importlib.util.module_from_spec(_SPEC_B)
_SPEC_B.loader.exec_module(obrien)

_L_DIR = HERE.parent / "20260907-lakes-tda-ews-peaktau-v3"
_SPEC_L = importlib.util.spec_from_file_location("chernoff_1n_peaktau", _L_DIR / "run.py")
peaktau = importlib.util.module_from_spec(_SPEC_L)
_SPEC_L.loader.exec_module(peaktau)

N_REPS = 500
SEED = 20260908
TRANSITION = 2002.0  # documented transition date, held FIXED across all surrogates -- see
# claim.md: this is a design parameter of the peak-selection algorithm, not derived from
# the series being tested, so keeping it fixed while randomizing the series isolates
# "does the algorithm produce large leads on structureless input" from "is there a real
# transition."


def _peak_date_from_series(tau_series: np.ndarray, window_end_dates: np.ndarray) -> float | None:
    idx = peaktau.peak_index(tau_series)
    return float(window_end_dates[idx]) if idx is not None else None


def one_surrogate_lead(pca1: np.ndarray, window: int, window_end_dates: np.ndarray, rng) -> dict:
    surrogate = obrien.ar1_surrogate(pca1, rng)

    ac1 = obrien.rolling_stat(surrogate, window, "ac1")
    var = obrien.rolling_stat(surrogate, window, "var")
    betti = obrien.betti1_entropy_series(surrogate, window)

    tau_ac1 = obrien.expanding_kendall_tau(ac1)
    tau_var = obrien.expanding_kendall_tau(var)
    tau_betti = obrien.expanding_kendall_tau(betti)

    peak_ac1 = _peak_date_from_series(tau_ac1, window_end_dates)
    peak_var = _peak_date_from_series(tau_var, window_end_dates)
    peak_tda = _peak_date_from_series(tau_betti, window_end_dates)

    classical_candidates = [c for c in (peak_ac1, peak_var) if c is not None]
    classical_peak = (
        min(classical_candidates, key=lambda d: abs(d - TRANSITION))
        if classical_candidates
        else None
    )

    lead_months = (
        (classical_peak - peak_tda) * 12.0
        if (classical_peak is not None and peak_tda is not None)
        else None
    )
    ac1_lead_months = (
        (peak_ac1 - peak_tda) * 12.0 if (peak_ac1 is not None and peak_tda is not None) else None
    )

    return {
        "peak_ac1": peak_ac1,
        "peak_var": peak_var,
        "peak_tda": peak_tda,
        "classical_peak_used": classical_peak,
        "lead_months": lead_months,
        "ac1_lead_months": ac1_lead_months,
    }


def cmd_run() -> dict:
    rdata = pyreadr.read_r(str(obrien.DATA))
    dates, pca1 = obrien.load_series(rdata, "lower_zurich")
    n = len(pca1)
    window = round(obrien.WINDOW_FRAC * n)
    window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)
    window_end_dates = dates[window - 1 :]

    rng = np.random.default_rng(SEED)
    reps = []
    for _ in range(N_REPS):
        reps.append(one_surrogate_lead(pca1, window, window_end_dates, rng))

    leads = np.array([r["lead_months"] for r in reps if r["lead_months"] is not None])
    ac1_leads = np.array([r["ac1_lead_months"] for r in reps if r["ac1_lead_months"] is not None])

    real_lead = 50.00000000000091  # H-B3-1l's own stored value, metrics/run.json
    # same convention as ac1_lead_months in one_surrogate_lead(): (peak_ac1 - peak_tda)*12.
    # real peak_ac1=1999.25, peak_tda=2000.5 -> -15.0 (negative = AC1 peaks BEFORE TDA).
    real_ac1_lead = (1999.25 - 2000.5) * 12.0

    n_valid = len(leads)
    pct_surrogates_matching_or_exceeding = float(np.mean(leads >= real_lead)) if n_valid else None
    percentile_of_real_lead = (
        float(np.mean(leads < real_lead) * 100) if n_valid else None
    )  # what fraction of surrogates the real lead exceeds

    if percentile_of_real_lead is None:
        verdict = "INCONCLUSIVE_NO_VALID_SURROGATES"
    elif percentile_of_real_lead <= 80.0:
        verdict = "CRITERION_INVALID_FLOOR_ARTIFACT"
    elif percentile_of_real_lead > 95.0:
        verdict = "LEAD_SURVIVES_AS_INFORMATIVE"
    else:
        verdict = "INCONCLUSIVE_AT_THIS_SAMPLE_SIZE"

    result = {
        "config": {
            "n_reps": N_REPS,
            "seed": SEED,
            "transition_fixed": TRANSITION,
            "window": window,
            "n_valid_surrogate_leads": n_valid,
        },
        "real_lead_months": real_lead,
        "real_ac1_lead_months": real_ac1_lead,
        "surrogate_lead_summary": {
            "median": float(np.median(leads)) if n_valid else None,
            "mean": float(np.mean(leads)) if n_valid else None,
            "std": float(np.std(leads)) if n_valid else None,
            "p05": float(np.percentile(leads, 5)) if n_valid else None,
            "p50": float(np.percentile(leads, 50)) if n_valid else None,
            "p80": float(np.percentile(leads, 80)) if n_valid else None,
            "p95": float(np.percentile(leads, 95)) if n_valid else None,
            "max": float(np.max(leads)) if n_valid else None,
        },
        "percentile_of_real_lead_within_null": percentile_of_real_lead,
        "fraction_surrogates_matching_or_exceeding_real_lead": pct_surrogates_matching_or_exceeding,
        "ac1_lead_surrogate_summary": {
            "median": float(np.median(ac1_leads)) if len(ac1_leads) else None,
            "p05": float(np.percentile(ac1_leads, 5)) if len(ac1_leads) else None,
            "p95": float(np.percentile(ac1_leads, 95)) if len(ac1_leads) else None,
            "n_valid": len(ac1_leads),
        },
        "verdict": verdict,
        "reps": reps,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "reps"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
