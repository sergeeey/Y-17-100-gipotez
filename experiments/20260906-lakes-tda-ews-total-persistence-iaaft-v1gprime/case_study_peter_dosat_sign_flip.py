"""case_study_peter_dosat_sign_flip.py -- H-B3-1i Relaxation Map item 2: "Look at whether the
underlying persistence-diagram STRUCTURE (not just the crossing time) changes qualitatively
between AR1 and IAAFT surrogates for this one series."

Key structural fact (verified by reading run.py, not assumed): the REAL total-persistence tau
curve for Peter doSat depends ONLY on the real data + tda_stat_fn (total persistence) -- NOT on
surrogate_fn. `analyze_series` computes `tau = expanding_kendall_tau(stats["betti"])` once from
the real series, then compares it against a NULL CURVE built from `reps` surrogates. So the
crossing-time shift between V1g (AR(1) null, crossing=172d, lead=+13d) and H-B3-1i (IAAFT null,
crossing=259d, lead=-74d) can ONLY come from the null-threshold curve itself moving -- the real
tau curve is identical in both experiments by construction.

This script computes, ONCE, for Peter doSat only (not all 9 series -- far cheaper than a full
population run):
  1. the real total-persistence tau curve (shared by both experiments)
  2. the AR(1)-derived null curve (V1g's null)
  3. the IAAFT-derived null curve (H-B3-1i's null)
and reports where each null curve sits relative to the real tau curve near both crossing points,
to make the mechanism of the sign flip legible rather than just re-stating the crossing times.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

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

TDA_REPS = 20  # matches the rep count used in both parent experiments
SEED = 0


def main() -> dict:
    season_time, x, _transition_time = peter.load_daily_series("doSat", "Peter")
    n = len(x)
    window = round(obrien.WINDOW_FRAC * n)
    window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)

    real_stat = obrien.betti1_total_persistence_series(x, window)
    real_tau = obrien.expanding_kendall_tau(real_stat)
    window_end_axis = season_time[window - 1 :]

    ar1_null = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=TDA_REPS,
        seed=SEED,
        surrogate_fn=obrien.ar1_surrogate,
        tda_stat_fn=obrien.betti1_total_persistence_series,
    )
    iaaft_null = obrien.surrogate_null_curve(
        x,
        window,
        "betti",
        reps=TDA_REPS,
        seed=SEED,
        surrogate_fn=obrien.iaaft_surrogate,
        tda_stat_fn=obrien.betti1_total_persistence_series,
    )

    ar1_cross_idx = obrien.surrogate_crossing(real_tau, ar1_null)
    iaaft_cross_idx = obrien.surrogate_crossing(real_tau, iaaft_null)

    def describe_at(idx):
        if idx is None:
            return None
        return {
            "time": float(window_end_axis[idx]),
            "real_tau": float(real_tau[idx]),
            "ar1_null_threshold": float(ar1_null[idx]) if not np.isnan(ar1_null[idx]) else None,
            "iaaft_null_threshold": (
                float(iaaft_null[idx]) if not np.isnan(iaaft_null[idx]) else None
            ),
        }

    valid = ~np.isnan(real_tau) & ~np.isnan(ar1_null) & ~np.isnan(iaaft_null)
    mean_ar1 = float(np.mean(ar1_null[valid]))
    mean_iaaft = float(np.mean(iaaft_null[valid]))
    frac_iaaft_higher = float(np.mean(iaaft_null[valid] > ar1_null[valid]))

    out = {
        "series": "peterlake_Peter_doSat",
        "n_points": n,
        "window": window,
        "at_ar1_crossing_idx": describe_at(ar1_cross_idx),
        "at_iaaft_crossing_idx": describe_at(iaaft_cross_idx),
        "mean_ar1_null_over_valid_range": mean_ar1,
        "mean_iaaft_null_over_valid_range": mean_iaaft,
        "fraction_of_timepoints_iaaft_null_higher_than_ar1_null": frac_iaaft_higher,
        "interpretation": (
            "IAAFT null threshold sits HIGHER than AR(1) null on average -> real tau needs "
            "longer to clear it -> LATER crossing (explains the +13d -> -74d lead reversal) "
            if mean_iaaft > mean_ar1
            else "IAAFT null threshold sits LOWER than AR(1) null on average -> unexpected given "
            "the later observed crossing; mechanism is NOT simply 'IAAFT null is stricter on "
            "average' -- needs closer inspection of the crossing-region behavior specifically"
        ),
    }
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
