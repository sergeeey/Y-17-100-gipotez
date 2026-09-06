"""run.py — H-B3-1f (V3): descriptive-only join of all 4 already-run detection methods on the
same 9 series. NO new statistics are computed here -- this reads the 4 parent experiments' own
already-committed metrics/run.json files and joins them into one comparison table.

Methods joined:
    raw   -- fixed tau>=0.5 threshold (H-B3-1 + H-B3-1b, two separate files, different key/unit
              conventions: O'Brien lakes in decimal years/months, Peter/Paul in season-time days)
    v1    -- per-series AR(1)-surrogate-null (H-B3-1c)
    v1p   -- per-series IAAFT-surrogate-null (H-B3-1d)
    v2p   -- per-series detrend+IAAFT-surrogate-null (H-B3-1e)
"""

from __future__ import annotations

import json
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

RAW_OBRIEN = EXPERIMENTS / "20260906-may1972-tda-ews-obrienlakes" / "metrics" / "run.json"
RAW_PETER = EXPERIMENTS / "20260906-may1972-tda-ews-peterlake" / "metrics" / "run.json"
V1 = EXPERIMENTS / "20260906-lakes-tda-ews-surrogate-null-v1" / "metrics" / "run.json"
V1P = EXPERIMENTS / "20260906-lakes-tda-ews-iaaft-null-v1prime" / "metrics" / "run.json"
V2P = EXPERIMENTS / "20260906-lakes-tda-ews-detrend-surrogate-v2prime" / "metrics" / "run.json"

# Maps the surrogate-family key (obrien_lower_zurich, peterlake_Peter_chl, ...) to
# (series_id, role, raw-file, raw-key) -- the raw files use different naming per dataset.
SERIES = {
    "obrien_lower_zurich": ("Lower Zurich", "positive", RAW_OBRIEN, "lower_zurich"),
    "obrien_windermere": ("Windermere", "negative", RAW_OBRIEN, "windermere"),
    "obrien_loch_leven": ("Loch Leven", "negative", RAW_OBRIEN, "loch_leven"),
    "peterlake_Peter_chl": ("Peter chl", "positive", RAW_PETER, "Peter_chl"),
    "peterlake_Peter_pH": ("Peter pH", "positive", RAW_PETER, "Peter_pH"),
    "peterlake_Peter_doSat": ("Peter doSat", "positive", RAW_PETER, "Peter_doSat"),
    "peterlake_Paul_chl": ("Paul chl", "negative", RAW_PETER, "Paul_chl"),
    "peterlake_Paul_pH": ("Paul pH", "negative", RAW_PETER, "Paul_pH"),
    "peterlake_Paul_doSat": ("Paul doSat", "negative", RAW_PETER, "Paul_doSat"),
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _raw_entry(raw_data: dict, raw_key: str, is_obrien: bool) -> dict:
    r = raw_data["results"][raw_key]
    if is_obrien:
        return {
            "tda_crossing": r["tda_betti_crossing"],
            "classical_crossing": r["classical_earliest_crossing"],
            "lead": r["lead_months_tda_minus_classical"],
            "lead_unit": "months",
            "floor_fp_rate": r["floor_ar1_false_positive_rate"],
        }
    return {
        "tda_crossing": r["tda_betti_crossing_day"],
        "classical_crossing": r["classical_earliest_crossing_day"],
        "lead": r["lead_days_tda_minus_classical"],
        "lead_unit": "days",
        "floor_fp_rate": r["floor_ar1_false_positive_rate"],
    }


def _surrogate_entry(data: dict, key: str) -> dict:
    r = data["results"][key]
    return {
        "tda_crossing": r["tda_betti_crossing"],
        "classical_crossing": r["classical_earliest_crossing"],
        "lead": r["tda_lead"],
        "lead_unit": "native (years for O'Brien, days for Peter/Paul)",
    }


def cmd_run() -> dict:
    raw_obrien = _load(RAW_OBRIEN)
    raw_peter = _load(RAW_PETER)
    v1_data = _load(V1)
    v1p_data = _load(V1P)
    v2p_data = _load(V2P)

    table = {}
    for surrogate_key, (label, role, raw_file, raw_key) in SERIES.items():
        is_obrien = raw_file == RAW_OBRIEN
        raw_data = raw_obrien if is_obrien else raw_peter
        table[surrogate_key] = {
            "label": label,
            "role": role,
            "raw_fixed_threshold": _raw_entry(raw_data, raw_key, is_obrien),
            "v1_ar1_null": _surrogate_entry(v1_data, surrogate_key),
            "v1prime_iaaft_null": _surrogate_entry(v1p_data, surrogate_key),
            "v2prime_detrend_iaaft_null": _surrogate_entry(v2p_data, surrogate_key),
        }

    # Descriptive-only counts (NOT a pass/fail verdict): how many methods gave a NONNULL TDA
    # crossing for each series, and how many negative-control series had >=1 method with a
    # POSITIVE (TDA leads classical, i.e. TDA earlier) lead.
    summary = {}
    for key, row in table.items():
        methods = [
            "raw_fixed_threshold",
            "v1_ar1_null",
            "v1prime_iaaft_null",
            "v2prime_detrend_iaaft_null",
        ]
        n_tda_crossings = sum(1 for m in methods if row[m]["tda_crossing"] is not None)
        positive_leads = [
            row[m]["lead"] for m in methods if row[m]["lead"] is not None and row[m]["lead"] > 0
        ]
        summary[key] = {
            "label": row["label"],
            "role": row["role"],
            "n_methods_with_tda_crossing": n_tda_crossings,
            "n_methods_with_positive_lead": len(positive_leads),
        }

    out = {
        "note": (
            "DESCRIPTIVE ONLY -- no binary verdict, no kill_criterion. Re-joins already-committed "
            "results from H-B3-1/1b (raw), H-B3-1c (V1), H-B3-1d (V1'), H-B3-1e (V2'). No new "
            "compute performed."
        ),
        "table": table,
        "summary": summary,
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
