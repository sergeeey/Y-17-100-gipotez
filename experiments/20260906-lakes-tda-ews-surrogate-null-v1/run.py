"""run.py — H-B3-1c (V1): per-series surrogate-null detection rule, re-run on BOTH prior datasets.

Reuses tested code from both parent experiments via import -- no pipeline logic reimplemented:
  - `20260906-may1972-tda-ews-obrienlakes/run.py`: rolling_stat, betti1_entropy_series,
    expanding_kendall_tau, ar1_surrogate, surrogate_null_curve, surrogate_crossing (the V1
    machinery itself), load_series (O'Brien lakes loader), LAKES config
  - `20260906-may1972-tda-ews-peterlake/run.py`: load_daily_series (Peter/Paul season-time
    loader), VARIABLES, LAKES config, TRANSITION_DECIMAL_YEAR

Only the DETECTION RULE differs from both parents (Minimal Relaxation Rule: one assumption
changed) -- window fraction, embedding, and statistics are identical to H-B3-1 / H-B3-1b.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pyreadr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


obrien = _load_module(
    "obrien_lakes_run", HERE.parent / "20260906-may1972-tda-ews-obrienlakes" / "run.py"
)
peter = _load_module("peterlake_run", HERE.parent / "20260906-may1972-tda-ews-peterlake" / "run.py")

CLASSICAL_REPS = 100
TDA_REPS = 20  # matches the rep count already spent on the floor check in both parents
SEED = 0


def analyze_series(x: np.ndarray, window: int, time_axis: np.ndarray, surrogate_fn=None) -> dict:
    """Run classical (AC1, variance) and TDA (Betti-1) statistics through the surrogate-null
    detection rule. `time_axis` is decimal year (O'Brien lakes) or season-time days (Peter Lake).
    `surrogate_fn` defaults to `obrien.ar1_surrogate` (V1); pass `obrien.iaaft_surrogate` for V1'
    -- the ONLY thing that changes between the two experiments (Minimal Relaxation Rule)."""
    surrogate_fn = surrogate_fn or obrien.ar1_surrogate
    stats = {
        "ac1": obrien.rolling_stat(x, window, "ac1"),
        "var": obrien.rolling_stat(x, window, "var"),
        "betti": obrien.betti1_entropy_series(x, window),
    }
    reps = {"ac1": CLASSICAL_REPS, "var": CLASSICAL_REPS, "betti": TDA_REPS}

    crossings: dict[str, float | None] = {}
    for kind, series in stats.items():
        tau = obrien.expanding_kendall_tau(series)
        null_curve = obrien.surrogate_null_curve(
            x, window, kind, reps[kind], SEED, surrogate_fn=surrogate_fn
        )
        idx = obrien.surrogate_crossing(tau, null_curve)
        window_end_axis = time_axis[window - 1 :]
        crossings[kind] = float(window_end_axis[idx]) if idx is not None else None

    classical_cross = min(
        [c for c in (crossings["ac1"], crossings["var"]) if c is not None], default=None
    )
    tda_cross = crossings["betti"]
    lead = (
        (classical_cross - tda_cross)
        if (classical_cross is not None and tda_cross is not None)
        else None
    )

    return {
        "classical_ac1_crossing": crossings["ac1"],
        "classical_var_crossing": crossings["var"],
        "classical_earliest_crossing": classical_cross,
        "tda_betti_crossing": tda_cross,
        "tda_lead": lead,
    }


def run_obrien_lakes(surrogate_fn=None) -> dict:
    rdata = pyreadr.read_r(str(obrien.DATA))
    out = {}
    for lake_key, cfg in obrien.LAKES.items():
        dates, pca1 = obrien.load_series(rdata, lake_key)
        n = len(pca1)
        window = round(obrien.WINDOW_FRAC * n)
        window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)
        result = analyze_series(pca1, window, dates, surrogate_fn=surrogate_fn)
        result["role"] = cfg["role"]
        result["n_points"] = n
        result["false_positive"] = cfg["role"] == "negative" and (
            result["classical_ac1_crossing"] is not None
            or result["classical_var_crossing"] is not None
            or result["tda_betti_crossing"] is not None
        )
        out[f"obrien_{lake_key}"] = result
    return out


def run_peter_paul_lake(surrogate_fn=None) -> dict:
    out = {}
    for lake, role in peter.LAKES.items():
        for var in peter.VARIABLES:
            season_time, x, _transition_time = peter.load_daily_series(var, lake)
            n = len(x)
            window = round(obrien.WINDOW_FRAC * n)
            window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)
            result = analyze_series(x, window, season_time, surrogate_fn=surrogate_fn)
            result["role"] = role
            result["n_points"] = n
            result["false_positive"] = role == "negative" and (
                result["classical_ac1_crossing"] is not None
                or result["classical_var_crossing"] is not None
                or result["tda_betti_crossing"] is not None
            )
            out[f"peterlake_{lake}_{var}"] = result
    return out


def cmd_run(
    surrogate_fn=None, detection_rule_label: str = "AR(1)-surrogate", write_output: bool = True
) -> dict:
    """`write_output=False` lets a sibling experiment (V1') reuse this function's compute logic
    without overwriting THIS experiment's own metrics/run.json -- V1's historical REJECT result
    must not be silently replaced by a re-run under a different surrogate model."""
    results = {
        **run_obrien_lakes(surrogate_fn=surrogate_fn),
        **run_peter_paul_lake(surrogate_fn=surrogate_fn),
    }

    negatives = [r for r in results.values() if r["role"] == "negative"]
    positives = [r for r in results.values() if r["role"] == "positive"]
    n_false_positives = sum(1 for r in negatives if r["false_positive"])
    positive_leads = [
        r["tda_lead"] for r in positives if r["tda_lead"] is not None and r["tda_lead"] > 0
    ]

    if n_false_positives == 0 and len(positive_leads) >= 1:
        verdict = "PASS"
    elif n_false_positives < len(negatives):
        verdict = "IMPROVED_NOT_PASS"  # fewer FPs than the fixed-threshold rule, but not clean
    else:
        verdict = "NO_IMPROVEMENT"

    out = {
        "config": {
            "detection_rule": f"per-series per-timepoint {detection_rule_label} 95th percentile",
            "alpha": obrien.SURROGATE_ALPHA,
            "classical_reps": CLASSICAL_REPS,
            "tda_reps": TDA_REPS,
            "window_frac": obrien.WINDOW_FRAC,
            "embed_dim": obrien.EMBED_DIM,
            "embed_delay": obrien.EMBED_DELAY,
        },
        "results": results,
        "n_negative_controls": len(negatives),
        "n_false_positives": n_false_positives,
        "n_positive_cases_with_tda_lead": len(positive_leads),
        "verdict": verdict,
    }
    if write_output:
        METRICS.mkdir(exist_ok=True)
        (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
