"""ac1_vs_crossing_rate_check.py -- direct follow-up to the Paul lake within-lake finding
(decision.md Addendum 3): does lag-1 autocorrelation correlate with TDA-crossing rate across the
FULL 9-series population, not just Paul lake's 3 variables?

Zero-Signal Gate:
  Entity: all 9 raw B3 population series (already loaded, no new detection compute).
  Falsifiable predicate: series' raw lag-1 autocorrelation correlates NEGATIVELY with their
    verified crossing rate (out of 7 method variants, per decision.md's cross-tabulation).
  Measurable outcome: Spearman correlation between per-series ACF(lag=1) and crossing_rate/7.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pyreadr
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
OBRIEN_DIR = HERE.parent / "20260906-may1972-tda-ews-obrienlakes"
PETER_DIR = HERE.parent / "20260906-may1972-tda-ews-peterlake"

_spec_obrien = importlib.util.spec_from_file_location("obrien_run", OBRIEN_DIR / "run.py")
obrien = importlib.util.module_from_spec(_spec_obrien)
_spec_obrien.loader.exec_module(obrien)

_spec_peter = importlib.util.spec_from_file_location("peter_run", PETER_DIR / "run.py")
peter = importlib.util.module_from_spec(_spec_peter)
_spec_peter.loader.exec_module(peter)


def acf_lag1(x: np.ndarray) -> float:
    x = x - np.mean(x)
    return float(np.sum(x[:-1] * x[1:]) / np.sum(x**2))


# Verified cross-tabulation from decision.md's CORRECTION ADDENDUM (2026-09-07), read directly
# from each experiment's own committed metrics/run.json -- not re-derived from memory here.
CROSSING_RATE_OUT_OF_7 = {
    "obrien_lower_zurich": 6,
    "obrien_windermere": 6,
    "obrien_loch_leven": 6,
    "peterlake_Peter_chl": 6,
    "peterlake_Peter_pH": 4,
    "peterlake_Peter_doSat": 6,
    "peterlake_Paul_chl": 3,
    "peterlake_Paul_pH": 3,
    "peterlake_Paul_doSat": 7,
}


def main() -> dict:
    ac1_by_series: dict[str, float] = {}

    rdata = pyreadr.read_r(str(obrien.DATA))
    for lake_key, out_key in [
        ("lower_zurich", "obrien_lower_zurich"),
        ("windermere", "obrien_windermere"),
        ("loch_leven", "obrien_loch_leven"),
    ]:
        _, pca1 = obrien.load_series(rdata, lake_key)
        ac1_by_series[out_key] = acf_lag1(pca1)

    for lake, var, out_key in [
        ("Peter", "chl", "peterlake_Peter_chl"),
        ("Peter", "pH", "peterlake_Peter_pH"),
        ("Peter", "doSat", "peterlake_Peter_doSat"),
        ("Paul", "chl", "peterlake_Paul_chl"),
        ("Paul", "pH", "peterlake_Paul_pH"),
        ("Paul", "doSat", "peterlake_Paul_doSat"),
    ]:
        _, values, _ = peter.load_daily_series(var, lake)
        ac1_by_series[out_key] = acf_lag1(values)

    series = list(CROSSING_RATE_OUT_OF_7.keys())
    ac1_vec = [ac1_by_series[s] for s in series]
    rate_vec = [CROSSING_RATE_OUT_OF_7[s] for s in series]
    rho, p = spearmanr(ac1_vec, rate_vec)

    out = {
        "per_series": {
            s: {"ac1_lag1": ac1_by_series[s], "crossing_rate_out_of_7": CROSSING_RATE_OUT_OF_7[s]}
            for s in series
        },
        "spearman_rho_ac1_vs_crossing_rate": float(rho),
        "spearman_p": float(p),
        "predicted_direction": "negative (lower AC1 -> higher crossing rate)",
        "prediction_confirmed": bool(rho < 0 and p < 0.05),
    }

    out_path = HERE / "metrics" / "ac1_vs_crossing_rate_check.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
