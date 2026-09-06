"""run.py — H-B3-1 (Peter Lake, unblocked 2026-09-06 by a user-provided CSV): TDA vs classical
EWS lead time on Carpenter et al. 2011's whole-ecosystem manipulation experiment.

Reuses the SAME pipeline functions as the sibling experiment `20260906-may1972-tda-ews-obrienlakes`
(Takens embedding, rolling AC1/variance, TDA persistence entropy, expanding-Kendall-tau crossing
rule, AR(1) floor check) via direct import -- not reimplemented, so the two experiments are
methodologically comparable and the lesson learned there (ALWAYS compute the floor before a
verdict) is applied here from the start, not bolted on after a hook complaint.

Ground truth [VERIFIED, read directly from the primary-source PDF, Carpenter et al. 2011 Science
preprint, pp.1-3]:
  - Bass additions: day 193/2008, day 169/2009, day 203/2009 (destabilizing manipulation)
  - "Planktivore numbers ... were similar to the reference lake by about day 230 of 2010" --
    the food-web transition is described as COMPLETE at day 230, 2010 (~2010.630 decimal year)
  - Abstract: classical EWS were "evident ... more than a year before the food web transition was
    complete" -- i.e. sometime in 2009
  - The paper's OWN early-warning analysis used DAILY chlorophyll concentrations (p.3: "Early
    warning indicators calculated for daily chlorophyll concentrations") -- daily aggregation here
    matches their methodology, not an arbitrary downsampling choice.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "squealSondesMet_08to11_forOPUS.csv"
METRICS = HERE / "metrics"

_SIBLING = HERE.parent / "20260906-may1972-tda-ews-obrienlakes" / "run.py"
_spec = importlib.util.spec_from_file_location("obrien_lakes_run", _SIBLING)
shared = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(shared)

TRANSITION_DOY_2010 = 230  # day 230 of 2010, Carpenter et al. 2011 p.3
TRANSITION_DECIMAL_YEAR = 2010 + (TRANSITION_DOY_2010 - 1) / 365.0

VARIABLES = ["chl", "pH", "doSat"]
LAKES = {"Peter": "positive", "Paul": "negative"}


SEASON_GAP_DAYS = 30  # WHY: winter ice-cover is not sampled by design (Carpenter et al. 2011 p.2:
# "monitored daily ... for three years of summer stratification") -- a >30-day gap marks a season
# boundary to SKIP, not missing data to exclude the surrounding record for (see decision.md
# Escape Point: an earlier version applied the sibling experiment's "keep only the longest
# contiguous run" ICE rule unmodified and silently analyzed only the 2009 season out of four).
INCLUDED_SEASONS = (2008, 2009, 2010)  # 2011 excluded: paper states the food web had already
# re-converged with the reference lake by day 230/2010 -- 2011 is post-transition, not lead-up.


def load_daily_series(var: str, lake: str) -> tuple[np.ndarray, np.ndarray, float]:
    """Daily mean of `var` for one lake, concatenated across the 2008-2010 field seasons on a
    SEASON-TIME axis (winter gaps compressed out, not bridged and not silently dropped) plus the
    transition point mapped onto that same axis. Returns (season_time, values, transition_time)."""
    df = pd.read_csv(DATA, usecols=["lake", "datetime", var])
    df = df[df["lake"] == lake].copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.dropna(subset=[var])
    daily = df.set_index("datetime")[var].resample("D").mean().dropna()
    dates = daily.index
    decimal_year = (dates.year + (dates.dayofyear - 1) / 365.0).to_numpy(dtype=float)
    values = daily.to_numpy(dtype=float)
    years = dates.year.to_numpy()

    keep = np.isin(years, INCLUDED_SEASONS)
    decimal_year, values = decimal_year[keep], values[keep]

    # detect season boundaries on the (already year-filtered) series
    spacing = np.diff(decimal_year)
    med = np.median(spacing)
    gap_idx = np.where(spacing > SEASON_GAP_DAYS * med)[0]
    bounds = [0, *[i + 1 for i in gap_idx], len(decimal_year)]

    season_time = np.empty_like(decimal_year)
    offset = 0.0
    transition_time = None
    for i in range(len(bounds) - 1):
        s, e = bounds[i], bounds[i + 1]
        local = (decimal_year[s:e] - decimal_year[s]) * 365.0  # days since this season's start
        season_time[s:e] = offset + local
        if decimal_year[s] <= TRANSITION_DECIMAL_YEAR <= decimal_year[e - 1]:
            transition_time = offset + (TRANSITION_DECIMAL_YEAR - decimal_year[s]) * 365.0
        offset = season_time[e - 1] + median_gap_bridge_days(spacing, med)
    return season_time, values, transition_time


def median_gap_bridge_days(spacing: np.ndarray, med: float) -> float:
    """1 unit past the last real sample -- season-time advances by exactly one nominal step
    across a compressed winter gap, so windows never span a literal multi-month jump."""
    return med if med > 0 else 1.0


def analyze_one(var: str, lake: str, role: str) -> dict:
    season_time, x, transition_time = load_daily_series(var, lake)
    n = len(x)
    window = round(shared.WINDOW_FRAC * n)
    window = max(window, shared.EMBED_DIM * shared.EMBED_DELAY + 8)

    ac1 = shared.rolling_stat(x, window, "ac1")
    var_stat = shared.rolling_stat(x, window, "var")
    betti = shared.betti1_entropy_series(x, window)

    tau_ac1 = shared.expanding_kendall_tau(ac1)
    tau_var = shared.expanding_kendall_tau(var_stat)
    tau_betti = shared.expanding_kendall_tau(betti)

    window_end_times = season_time[window - 1 :]

    def crossing_time(tau_series: np.ndarray) -> float | None:
        idx = shared.first_crossing(tau_series)
        return float(window_end_times[idx]) if idx is not None else None

    cross_ac1 = crossing_time(tau_ac1)
    cross_var = crossing_time(tau_var)
    cross_betti = crossing_time(tau_betti)
    classical_cross = min([c for c in (cross_ac1, cross_var) if c is not None], default=None)

    lead_days = None
    if cross_betti is not None and classical_cross is not None:
        lead_days = classical_cross - cross_betti

    lead_before_transition_days = {
        "classical": (transition_time - classical_cross)
        if classical_cross is not None and transition_time is not None
        else None,
        "tda": (transition_time - cross_betti)
        if cross_betti is not None and transition_time is not None
        else None,
    }

    floor_fp_rate = shared.floor_false_positive_rate(x, window, reps=20, seed=0)

    return {
        "lake": lake,
        "variable": var,
        "role": role,
        "n_points": n,
        "season_time_range_days": [float(season_time[0]), float(season_time[-1])],
        "transition_time_days": transition_time,
        "window": window,
        "classical_ac1_crossing_day": cross_ac1,
        "classical_var_crossing_day": cross_var,
        "classical_earliest_crossing_day": classical_cross,
        "tda_betti_crossing_day": cross_betti,
        "lead_days_tda_minus_classical": lead_days,
        "lead_before_transition_days": lead_before_transition_days,
        "false_positive": role == "negative"
        and (cross_ac1 is not None or cross_var is not None or cross_betti is not None),
        "floor_ar1_false_positive_rate": floor_fp_rate,
    }


def cmd_run() -> dict:
    results = {}
    for lake, role in LAKES.items():
        for var in VARIABLES:
            results[f"{lake}_{var}"] = analyze_one(var, lake, role)

    peter_hits = [
        r
        for k, r in results.items()
        if k.startswith("Peter_")
        and r["lead_days_tda_minus_classical"] is not None
        and r["lead_days_tda_minus_classical"] > 0
        and (r["lead_before_transition_days"]["tda"] or -1)
        > 0  # crossing must precede the transition to count as "early"
    ]
    paul_false_positives = [
        r for k, r in results.items() if k.startswith("Paul_") and r["false_positive"]
    ]
    floor_rates = [r["floor_ar1_false_positive_rate"] for r in results.values()]

    if max(floor_rates) > 0.3:
        verdict = "CRITERION_INVALID"
    elif len(peter_hits) >= 1 and not paul_false_positives:
        verdict = "PASS"
    else:
        verdict = "KILLED"

    out = {
        "ground_truth": {
            "transition_doy_2010": TRANSITION_DOY_2010,
            "transition_decimal_year": TRANSITION_DECIMAL_YEAR,
            "source": "Carpenter et al. 2011 Science preprint p.3, read directly from PDF",
        },
        "config": {
            "window_frac": shared.WINDOW_FRAC,
            "embed_dim": shared.EMBED_DIM,
            "embed_delay": shared.EMBED_DELAY,
            "tau_threshold": shared.TAU_THRESHOLD,
            "aggregation": "daily mean (matches Carpenter et al. 2011's own EWS methodology)",
        },
        "results": results,
        "max_floor_false_positive_rate": max(floor_rates),
        "verdict": verdict,
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
