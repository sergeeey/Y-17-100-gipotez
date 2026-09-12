"""Aggregates check_l2_pairwise_energy.py's per-layer E1/E2/C_q values (w_q-weighted, same
convention as point 14/15b) across n=23..47, to see the E1, E2, and E1+E2 coverage trend.
Recomputes n=23,29,31 (cheap, seconds) since check_l2_pairwise_energy.py's cross-validation
step only used them transiently; reads n=37,41,43,47 from the persisted extension file.
"""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

spec = importlib.util.spec_from_file_location("l2mod_agg", HERE / "check_l2_pairwise_energy.py")
l2mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(l2mod)


def run() -> list[dict]:
    with open(METRICS / "l2_pairwise_energy.json", encoding="utf-8") as f:
        saved = json.load(f)

    all_rows = {}
    for n in [23, 29, 31]:
        all_rows[str(n)] = l2mod.l2_energy_per_layer(n)
    for n_str, rows in saved.items():
        all_rows[n_str] = rows

    summary = []
    for n_str in ["23", "29", "31", "37", "41", "43", "47"]:
        rows = all_rows[n_str]
        total_c = total_e1 = total_e2 = 0.0
        for r in rows:
            big_n = r["N"]
            q = r["q"]
            w_q = comb(big_n, q) / (2**big_n)
            total_c += w_q * r["C_q"]
            total_e1 += w_q * r["E1"]
            total_e2 += w_q * r["E2"]
        row = {
            "n": int(n_str),
            "agg_C": total_c,
            "agg_E1": total_e1,
            "agg_E2": total_e2,
            "E1_frac": total_e1 / total_c,
            "E2_frac": total_e2 / total_c,
            "E1_plus_E2_frac": (total_e1 + total_e2) / total_c,
        }
        summary.append(row)
        print(
            f"n={n_str:>3}  E1_frac={100 * row['E1_frac']:.3f}%  "
            f"E2_frac={100 * row['E2_frac']:.3f}%  "
            f"E1+E2_covers={100 * row['E1_plus_E2_frac']:.3f}%"
        )
    return summary


if __name__ == "__main__":
    out = run()
    with open(METRICS / "l2_energy_aggregate.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
