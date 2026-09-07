"""paul_lake_variable_comparison.py -- corrected, sharper follow-up to H-B3-1h's own open question
(see CORRECTION ADDENDUM in decision.md). The honest cross-tabulation of tda_betti_crossing across
all 7 method variants tried in this arc shows crossing rate does NOT track true/false-positive
role at all (Windermere crosses at the same 6/7 rate as 3 of 4 positive-role series). The genuine
outliers are Paul_doSat (7/7, crosses under literally every method) vs. its own siblings Paul_chl
and Paul_pH (3/7 each, tied for the lowest rate of all 9 series).

This is a much cleaner natural experiment than any cross-lake comparison: three variables, SAME
lake, SAME period, SAME (absence of) manipulation -- basin morphology, sampling protocol,
instrumentation, and observer are held constant by construction. Whatever differs between doSat's
raw dynamics and chl/pH's is the candidate explanation for the crossing-rate gap.

Zero-Signal Gate:
  Entity: Paul lake's 3 raw daily-aggregated variables (chl, pH, doSat), already loaded by the
    peterlake experiment's own load_daily_series -- no new data, no new detection compute.
  Falsifiable predicate: Paul_doSat's raw series shows a distinguishing statistical property
    (stronger monotonic trend, and/or different short-lag autocorrelation structure) relative to
    Paul_chl/Paul_pH that plausibly explains its much higher TDA-crossing rate.
  Measurable outcome: per-variable Spearman trend (rho, p), lag-1..3 autocorrelation, basic
    descriptive stats (mean, std, n_points, season count), reported side by side.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
PETER_DIR = HERE.parent / "20260906-may1972-tda-ews-peterlake"

_spec_peter = importlib.util.spec_from_file_location("peter_run", PETER_DIR / "run.py")
peter = importlib.util.module_from_spec(_spec_peter)
_spec_peter.loader.exec_module(peter)


def acf(x: np.ndarray, max_lag: int) -> list[float]:
    x = x - np.mean(x)
    denom = np.sum(x**2)
    return [float(np.sum(x[: len(x) - lag] * x[lag:]) / denom) for lag in range(1, max_lag + 1)]


def count_seasons(var: str, lake: str) -> int:
    """Independently re-derive the number of field seasons (gap-separated contiguous runs) from
    the raw dates -- NOT from `season_time`, whose own gap-bridging logic (peterlake/run.py's
    `median_gap_bridge_days`) deliberately compresses each season boundary to a single nominal
    step, indistinguishable from a normal daily increment (per that function's own docstring:
    "so windows never span a literal multi-month jump"). A diff-based heuristic on `season_time`
    can therefore never see season boundaries at all -- confirmed by review before trusting it;
    the original version of this function always returned 1, silently, for every series. Mirrors
    `load_daily_series`'s own gap-detection logic exactly (same constants, same threshold), on
    the raw decimal-year axis where the gap IS still visible."""
    df = pd.read_csv(peter.DATA, usecols=["lake", "datetime", var])
    df = df[df["lake"] == lake].copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.dropna(subset=[var])
    daily = df.set_index("datetime")[var].resample("D").mean().dropna()
    dates = daily.index
    decimal_year = (dates.year + (dates.dayofyear - 1) / 365.0).to_numpy(dtype=float)
    years = dates.year.to_numpy()
    keep = np.isin(years, peter.INCLUDED_SEASONS)
    decimal_year = decimal_year[keep]
    spacing = np.diff(decimal_year)
    med = np.median(spacing)
    gap_idx = np.where(spacing > peter.SEASON_GAP_DAYS * med)[0]
    return len(gap_idx) + 1


def analyze(lake: str, var: str) -> dict:
    _, values, _ = peter.load_daily_series(var, lake)
    t = np.arange(len(values))
    rho, p = spearmanr(t, values)
    return {
        "lake": lake,
        "variable": var,
        "n_points": len(values),
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
        "cv": float(np.std(values) / np.mean(values)) if np.mean(values) != 0 else None,
        "spearman_trend_rho": float(rho),
        "spearman_trend_p": float(p),
        "acf_lag1_3": acf(values, 3),
        "n_seasons": count_seasons(var, lake),
    }


def main() -> dict:
    results = {var: analyze("Paul", var) for var in ("chl", "pH", "doSat")}
    out = {
        "per_variable": results,
        "tda_crossing_rate_context": {
            "chl": "3/7 (verified cross-tabulation, H-B3-1h decision.md correction addendum)",
            "pH": "3/7",
            "doSat": "7/7 (crosses under literally every method tested)",
        },
    }
    out_path = HERE / "metrics" / "paul_lake_variable_comparison.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
