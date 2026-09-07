"""peter_lake_variable_comparison.py -- H-B3-1h decision.md Addendum 3's own named next step:
replicate the Paul lake within-lake variable comparison (chl/pH/doSat) on Peter lake (the
positive-role lake), as an out-of-sample check of whether the same candidate mechanisms
(trend strength, lag-1 autocorrelation) behave the same way.

Verified crossing-rate context BEFORE running (from the already-committed cross-tabulation,
ac1_vs_crossing_rate_check.json): Peter_chl=6/7, Peter_pH=4/7, Peter_doSat=6/7 -- a MUCH
narrower spread than Paul lake's 3/7, 3/7, 7/7. This is itself a first, cheap, informative
observation before any new compute: whatever process makes Paul_doSat special (crossing under
literally every method) may be Paul-lake-specific (or role-specific), not a general
doSat-vs-chl/pH pattern -- Peter's own doSat and chl are actually TIED at the top, with pH lowest
(the opposite ranking from Paul, where chl and pH were tied at the BOTTOM).

Zero-Signal Gate:
  Entity: Peter lake's 3 raw daily-aggregated variables (chl, pH, doSat), already loaded by the
    peterlake experiment's own load_daily_series -- no new data, no new detection compute.
  Falsifiable predicate: does the SAME direction of effect found on Paul lake (trend inverted,
    weak negative AC1-crossing-rate association) replicate on Peter lake, or does the pattern
    differ because Peter's own crossing-rate spread is much narrower to begin with?
  Measurable outcome: per-variable Spearman trend (rho, p), lag-1..3 autocorrelation, n_seasons,
    reported side by side, compared directly against Paul lake's own already-committed results.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "paul_comparison", HERE / "paul_lake_variable_comparison.py"
)
paul_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(paul_mod)

# Reuse `analyze` unchanged -- it already takes (lake, var), Paul lake was just the first call site.
analyze = paul_mod.analyze


def main() -> dict:
    results = {var: analyze("Peter", var) for var in ("chl", "pH", "doSat")}
    out = {
        "per_variable": results,
        "tda_crossing_rate_context": {
            "chl": "6/7 (verified cross-tabulation, ac1_vs_crossing_rate_check.json)",
            "pH": "4/7 (lowest of the 3 -- opposite ranking from Paul lake)",
            "doSat": "6/7 (tied with chl -- NOT the outlier it was on Paul lake)",
        },
        "paul_lake_comparison_context": (
            "Paul lake (already committed, paul_lake_variable_comparison.json): "
            "chl=3/7, pH=3/7, doSat=7/7 -- doSat was the SOLE outlier there. "
            "Peter lake's spread (6/4/6) is narrower and ranks doSat/chl TIED at the top, "
            "pH lowest -- a qualitatively different pattern, not a replica."
        ),
    }
    out_path = HERE / "metrics" / "peter_lake_variable_comparison.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
