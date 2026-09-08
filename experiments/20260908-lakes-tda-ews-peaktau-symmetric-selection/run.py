"""run.py — H-B3-1p: does H-B3-1l's CONFIRMED peak-tau verdict on Lower Zurich survive when
the classical-statistic-selection rule is made SYMMETRIC (the same 'earliest of the two'
rule already used for negative controls), instead of the oracle-informed 'closest to the
known transition' rule currently used only for the positive case?

Reuses UNCHANGED via dynamic import: H-B3-1l's own peak_index() and the obrienlakes
pipeline (load_series, rolling_stat, betti1_entropy_series, expanding_kendall_tau) via
H-B3-1l's own run.py. The ONE assumption changed (Minimal Relaxation Rule): the
classical-peak selection rule -- earliest-of-two for ALL lakes, not just negative controls.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pyreadr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_L_DIR = HERE.parent / "20260907-lakes-tda-ews-peaktau-v3"
_SPEC_L = importlib.util.spec_from_file_location("chernoff_1p_peaktau", _L_DIR / "run.py")
peaktau = importlib.util.module_from_spec(_SPEC_L)
_SPEC_L.loader.exec_module(peaktau)

obrien = peaktau.obrien  # H-B3-1l's own dynamic import of the obrienlakes pipeline

with open(_L_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B3_1L_RESULT = json.load(f)


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
            idx = peaktau.peak_index(tau_series)
            return float(window_end_dates[idx]) if idx is not None else None

        peak_ac1 = peak_date(tau_ac1)
        peak_var = peak_date(tau_var)
        peak_betti = peak_date(tau_betti)

        # THE ONE CHANGED ASSUMPTION: symmetric "earliest of the two" for ALL lakes, no
        # transition-based oracle selection, even for the positive case.
        classical_candidates = [c for c in (peak_ac1, peak_var) if c is not None]
        classical_peak = min(classical_candidates) if classical_candidates else None

        lead_months = (
            (classical_peak - peak_betti) * 12.0
            if (peak_betti is not None and classical_peak is not None)
            else None
        )

        transition = cfg["transition"]
        entry = {
            "role": cfg["role"],
            "documented_transition": transition,
            "tda_betti_peak_date": peak_betti,
            "classical_ac1_peak_date": peak_ac1,
            "classical_var_peak_date": peak_var,
            "classical_peak_date_used_symmetric": classical_peak,
            "peak_lead_months_tda_minus_classical_symmetric": lead_months,
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
    tda_peak = lz["tda_betti_peak_date"]
    classical_peak = lz["classical_peak_date_used_symmetric"]
    tda_dist = lz.get("tda_distance_to_transition_years")
    classical_dist = lz.get("classical_distance_to_transition_years")

    if None in (tda_dist, classical_dist, tda_peak, classical_peak):
        verdict_symmetric = "AMBIGUOUS"
    elif tda_dist < classical_dist and tda_peak <= classical_peak:
        verdict_symmetric = "CONFIRMED"
    else:
        verdict_symmetric = "REJECTED"

    # consistency check: negative controls should be UNCHANGED (they already used the
    # symmetric rule in H-B3-1l -- this is a re-derivation, not a genuine new computation
    # for them, so it should match the stored H-B3-1l values exactly).
    negative_controls_match_original = {}
    for lake in ("windermere", "loch_leven"):
        stored = H_B3_1L_RESULT["results"][lake]["classical_peak_date_used"]
        recomputed = results[lake]["classical_peak_date_used_symmetric"]
        match = stored is not None and recomputed is not None and abs(stored - recomputed) < 1e-6
        negative_controls_match_original[lake] = {
            "stored": stored,
            "recomputed": recomputed,
            "match": match,
        }

    pearl_prediction_confirmed = (
        classical_peak is not None
        and abs(classical_peak - 1999.25) < 1e-6
        and tda_peak is not None
        and tda_peak > classical_peak
        and verdict_symmetric == "REJECTED"
    )

    out = {
        "results": results,
        "original_verdict_h_b3_1l": H_B3_1L_RESULT["verdict"],
        "verdict_under_symmetric_rule": verdict_symmetric,
        "verdict_inverted": (
            H_B3_1L_RESULT["verdict"] == "CONFIRMED" and verdict_symmetric == "REJECTED"
        ),
        "pearl_prediction_confirmed": pearl_prediction_confirmed,
        "negative_controls_consistency_check": negative_controls_match_original,
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
