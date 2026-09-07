"""trend_magnitude_vs_crossing_rate_combined.py -- pools Paul lake's and Peter lake's own
within-lake variable comparisons (both already committed) to test, with n=6 (twice the power of
either single-lake comparison), whether |trend| correlates NEGATIVELY with TDA-crossing rate --
the direction found (informally) on both lakes individually: pH has the strongest trend and the
lowest crossing rate in BOTH Paul lake and Peter lake, independently.

Zero-Signal Gate:
  Entity: all 6 peterlake-experiment daily variables (Peter/Paul x chl/pH/doSat), already
    analyzed by paul_lake_variable_comparison.py and peter_lake_variable_comparison.py.
  Falsifiable predicate: |Spearman trend rho| correlates negatively with crossing_rate_out_of_7
    across these 6 variables (n=6, pooling both lakes).
  Measurable outcome: Spearman correlation between |trend rho| and crossing rate, p-value.
"""

from __future__ import annotations

import json
from pathlib import Path

from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent

paul = json.loads((HERE / "metrics" / "paul_lake_variable_comparison.json").read_text())
peter = json.loads((HERE / "metrics" / "peter_lake_variable_comparison.json").read_text())

# Crossing rates verified directly in ac1_vs_crossing_rate_check.json (already committed).
CROSSING_RATE = {
    "Paul_chl": 3,
    "Paul_pH": 3,
    "Paul_doSat": 7,
    "Peter_chl": 6,
    "Peter_pH": 4,
    "Peter_doSat": 6,
}


def main() -> dict:
    per_series = {}
    for lake_key, data in [("Paul", paul), ("Peter", peter)]:
        for var, stats in data["per_variable"].items():
            key = f"{lake_key}_{var}"
            per_series[key] = {
                "abs_trend_rho": abs(stats["spearman_trend_rho"]),
                "ac1_lag1": stats["acf_lag1_3"][0],
                "crossing_rate": CROSSING_RATE[key],
            }

    keys = list(per_series.keys())
    trend_vec = [per_series[k]["abs_trend_rho"] for k in keys]
    rate_vec = [per_series[k]["crossing_rate"] for k in keys]
    ac1_vec = [per_series[k]["ac1_lag1"] for k in keys]

    rho_trend, p_trend = spearmanr(trend_vec, rate_vec)
    rho_ac1, p_ac1 = spearmanr(ac1_vec, rate_vec)

    out = {
        "per_series": per_series,
        "trend_vs_crossing_rate": {
            "spearman_rho": float(rho_trend),
            "p_value": float(p_trend),
            "predicted_direction": "negative (stronger trend -> fewer crossings)",
            "confirmed_at_0.05": bool(rho_trend < 0 and p_trend < 0.05),
        },
        "ac1_vs_crossing_rate_pooled_6": {
            "spearman_rho": float(rho_ac1),
            "p_value": float(p_ac1),
            "predicted_direction": "negative (lower AC1 -> more crossings)",
            "confirmed_at_0.05": bool(rho_ac1 < 0 and p_ac1 < 0.05),
        },
    }
    out_path = HERE / "metrics" / "trend_magnitude_vs_crossing_rate_combined.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
