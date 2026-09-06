"""case_study_loch_leven_paul_dosat.py -- H-B3-1h Relaxation Map, cheapest item:
"A focused single-series case study on just these two [Loch Leven, Paul doSat]
(what does their raw data actually look like around the false-crossing date?)"

NO new detection compute, no new surrogate runs. Pure descriptive inspection of
already-collected raw series around each series' own recorded tda_betti_crossing
time (from H-B3-1c/V1's committed metrics/run.json). Read-only diagnostic script,
not a new claim/experiment -- output feeds the Kill Analysis note in decision.md.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pyreadr

HERE = Path(__file__).resolve().parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


obrien = _load_module(
    "obrien_lakes_run", HERE.parent / "20260906-may1972-tda-ews-obrienlakes" / "run.py"
)
peter = _load_module("peterlake_run", HERE.parent / "20260906-may1972-tda-ews-peterlake" / "run.py")

V1_METRICS = HERE.parent / "20260906-lakes-tda-ews-surrogate-null-v1" / "metrics" / "run.json"


def describe_window(time_axis: np.ndarray, x: np.ndarray, crossing: float, label: str) -> dict:
    idx = int(np.argmin(np.abs(time_axis - crossing)))
    lo, hi = max(0, idx - 10), min(len(x), idx + 11)
    seg = x[lo:hi]
    full_mean, full_std = float(np.mean(x)), float(np.std(x, ddof=1))
    seg_mean, seg_std = float(np.mean(seg)), float(np.std(seg, ddof=1))
    # crude local "event-ness": does the +-10-point window around the crossing look unusual
    # relative to the whole series (z-scored mean shift, local variance ratio)?
    z_shift = (seg_mean - full_mean) / full_std if full_std > 0 else float("nan")
    var_ratio = (seg_std**2) / (full_std**2) if full_std > 0 else float("nan")
    return {
        "label": label,
        "n_total": len(x),
        "crossing_time": float(crossing),
        "window_idx": [lo, hi],
        "window_time_range": [float(time_axis[lo]), float(time_axis[hi - 1])],
        "full_series_mean": full_mean,
        "full_series_std": full_std,
        "local_window_mean": seg_mean,
        "local_window_std": seg_std,
        "local_mean_zshift": z_shift,
        "local_var_ratio": var_ratio,
        "local_values_head": [round(float(v), 4) for v in seg[:5]],
        "local_values_tail": [round(float(v), 4) for v in seg[-5:]],
        "series_min": float(np.min(x)),
        "series_max": float(np.max(x)),
        "n_unique_values": len(np.unique(x)),
    }


def main() -> dict:
    v1 = json.load(open(V1_METRICS, encoding="utf-8"))["results"]

    # Loch Leven (O'Brien dataset, decimal-year time axis)
    rdata = pyreadr.read_r(str(obrien.DATA))
    dates_ll, pca1_ll = obrien.load_series(rdata, "loch_leven")
    cross_ll = v1["obrien_loch_leven"]["tda_betti_crossing"]
    report_ll = describe_window(dates_ll, pca1_ll, cross_ll, "Loch Leven (pca1)")

    # Paul doSat (Peter-Paul dataset, season-time day axis)
    season_time, x_paul, _transition_time = peter.load_daily_series("doSat", "Paul")
    cross_paul = v1["peterlake_Paul_doSat"]["tda_betti_crossing"]
    report_paul = describe_window(season_time, x_paul, cross_paul, "Paul doSat")
    report_paul["note"] = (
        "Paul is the reference (no-manipulation) lake in the Peter-Paul whole-lake experiment "
        "-- role=negative by design, so ANY crossing here is by definition a false positive."
    )

    # Contrast case: Peter doSat is the ONE positive-role series whose TDA crossing has a
    # real paired classical crossing (interpretable +13d lead) and survives every variant
    # tried so far -- if false positives are a local-variance-minimum artifact, a genuine
    # signal should NOT show the same pattern (expect flat or rising local variance instead).
    season_time_p, x_peter, _transition_time_p = peter.load_daily_series("doSat", "Peter")
    cross_peter = v1["peterlake_Peter_doSat"]["tda_betti_crossing"]
    report_peter = describe_window(season_time_p, x_peter, cross_peter, "Peter doSat (contrast)")
    report_peter["note"] = (
        "Positive control: Peter doSat is role=positive with an interpretable +13d TDA lead "
        "that survives every variant tried (V1/V1'/V2'/V1g/conjunction). Contrast target: "
        "does its crossing ALSO sit in a local-variance minimum, or is that pattern specific "
        "to the two unexplained false positives?"
    )

    out = {"loch_leven": report_ll, "paul_dosat": report_paul, "peter_dosat_contrast": report_peter}
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
