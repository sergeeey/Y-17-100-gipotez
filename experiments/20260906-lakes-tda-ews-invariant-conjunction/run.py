"""run.py — H-B3-1h: conjunction rule (entropy AND total persistence must BOTH cross) -- pure
re-join of V1's and V1g's already-committed metrics/run.json, NO new compute. Explicitly named in
H-B3-1g's own Relaxation Map.
"""

from __future__ import annotations

import json
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

V1_ENTROPY = EXPERIMENTS / "20260906-lakes-tda-ews-surrogate-null-v1" / "metrics" / "run.json"
V1G_TOTAL_PERSISTENCE = (
    EXPERIMENTS / "20260906-lakes-tda-ews-total-persistence-v1g" / "metrics" / "run.json"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_run() -> dict:
    v1 = _load(V1_ENTROPY)["results"]
    v1g = _load(V1G_TOTAL_PERSISTENCE)["results"]

    table = {}
    for key in v1:
        entropy_crosses = v1[key]["tda_betti_crossing"] is not None
        total_persistence_crosses = v1g[key]["tda_betti_crossing"] is not None
        both_cross = entropy_crosses and total_persistence_crosses
        role = v1[key]["role"]
        table[key] = {
            "role": role,
            "entropy_tda_crosses": entropy_crosses,
            "entropy_tda_lead": v1[key]["tda_lead"],
            "total_persistence_tda_crosses": total_persistence_crosses,
            "total_persistence_tda_lead": v1g[key]["tda_lead"],
            "conjunction_both_cross": both_cross,
            "conjunction_false_positive": role == "negative" and both_cross,
            "conjunction_positive_signal": role == "positive" and both_cross,
        }

    negatives = [r for r in table.values() if r["role"] == "negative"]
    positives = [r for r in table.values() if r["role"] == "positive"]
    n_false_positives_conjunction = sum(1 for r in negatives if r["conjunction_false_positive"])
    n_positive_signals_conjunction = sum(1 for r in positives if r["conjunction_positive_signal"])

    out = {
        "note": (
            "DESCRIPTIVE re-join, NO new compute -- pure conjunction of V1 (entropy) and V1g "
            "(total persistence), both already-committed AR(1)-null results."
        ),
        "table": table,
        "n_negative_controls": len(negatives),
        "n_false_positives_conjunction": n_false_positives_conjunction,
        "n_false_positives_entropy_alone": sum(1 for r in negatives if r["entropy_tda_crosses"]),
        "n_false_positives_total_persistence_alone": sum(
            1 for r in negatives if r["total_persistence_tda_crosses"]
        ),
        "n_positive_signals_conjunction": n_positive_signals_conjunction,
        "peter_dosat_survives_conjunction": table["peterlake_Peter_doSat"][
            "conjunction_both_cross"
        ],
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
