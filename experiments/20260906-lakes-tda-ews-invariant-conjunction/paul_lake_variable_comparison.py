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


def analyze(lake: str, var: str) -> dict:
    season_time, values, _ = peter.load_daily_series(var, lake)
    t = np.arange(len(values))
    rho, p = spearmanr(t, values)
    # n_seasons: count contiguous runs via the same gap logic load_daily_series uses internally
    # (re-derive cheaply from season_time resets, since load_daily_series doesn't return bounds).
    diffs = np.diff(season_time)
    n_season_boundaries = int(np.sum(diffs < 0))  # season_time resets near 0 at each new season
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
        "approx_n_seasons": n_season_boundaries + 1,
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
