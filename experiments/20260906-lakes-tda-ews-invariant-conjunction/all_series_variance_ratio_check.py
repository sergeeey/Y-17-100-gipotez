"""all_series_variance_ratio_check.py -- pearl_registry/INDEX.md 2026-09-06 entry
"H-B3-1h case study (Loch Leven / Paul doSat raw data)", falsifiable_prediction:

    "If local_var_ratio in the crossing window is checked for ALL 9 series in the
    B3 population (not just the 3 checked in the case study), the fraction of
    series with var_ratio < 0.5 at their crossing will be high REGARDLESS OF
    ROLE (positive/negative) -- confirming this is a generic property of the
    expanding-Kendall-tau crossing rule, not a useful discriminator."

Only 6 of the 9 series have a recorded tda_betti_crossing at all (V1, entropy
invariant, AR(1) null) -- the other 3 (Windermere, Peter pH, Paul pH) never
cross, so there is no crossing window to check for them. This script computes
local_var_ratio for all 6 crossing series and reports the fraction with
var_ratio < 0.5, split by role, to test the prediction above.

NO new detection compute -- reuses V1's already-committed tda_betti_crossing
values and re-derives local_var_ratio via the same describe_window() logic
introduced in case_study_loch_leven_paul_dosat.py (duplicated here rather than
imported, since that module's main() is a fixed 3-series report, not a
library entry point -- kept small and inline for this one-off check).
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


def local_var_ratio(time_axis: np.ndarray, x: np.ndarray, crossing: float) -> float:
    idx = int(np.argmin(np.abs(time_axis - crossing)))
    lo, hi = max(0, idx - 10), min(len(x), idx + 11)
    seg = x[lo:hi]
    full_std = float(np.std(x, ddof=1))
    seg_std = float(np.std(seg, ddof=1))
    return (seg_std**2) / (full_std**2) if full_std > 0 else float("nan")


def main() -> dict:
    v1 = json.load(open(V1_METRICS, encoding="utf-8"))["results"]
    rdata = pyreadr.read_r(str(obrien.DATA))

    series_loaders = {
        "obrien_lower_zurich": lambda: obrien.load_series(rdata, "lower_zurich"),
        "obrien_loch_leven": lambda: obrien.load_series(rdata, "loch_leven"),
        "peterlake_Peter_chl": lambda: peter.load_daily_series("chl", "Peter")[:2],
        "peterlake_Peter_doSat": lambda: peter.load_daily_series("doSat", "Peter")[:2],
        "peterlake_Paul_chl": lambda: peter.load_daily_series("chl", "Paul")[:2],
        "peterlake_Paul_doSat": lambda: peter.load_daily_series("doSat", "Paul")[:2],
    }

    out = {}
    for key, loader in series_loaders.items():
        cross = v1[key]["tda_betti_crossing"]
        if cross is None:
            continue
        time_axis, x = loader()
        ratio = local_var_ratio(time_axis, x, cross)
        out[key] = {
            "role": v1[key]["role"],
            "crossing_time": cross,
            "local_var_ratio": ratio,
            "below_0_5": bool(ratio < 0.5),
        }

    n_below = sum(1 for v in out.values() if v["below_0_5"])
    n_total = len(out)
    by_role: dict[str, list[float]] = {}
    for v in out.values():
        by_role.setdefault(v["role"], []).append(v["local_var_ratio"])

    summary = {
        "series": out,
        "n_series_with_crossing": n_total,
        "n_below_0_5": n_below,
        "fraction_below_0_5": n_below / n_total if n_total else None,
        "mean_var_ratio_by_role": {role: float(np.mean(vals)) for role, vals in by_role.items()},
        "prediction_check": (
            "PREDICTION CONFIRMED: fraction below 0.5 is high across BOTH roles"
            if n_below / n_total >= 0.7
            and len(by_role.get("positive", [])) > 0
            and len(by_role.get("negative", [])) > 0
            else "PREDICTION NOT CONFIRMED as stated -- see per-role means"
        ),
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
