"""Implements and tests the two-term sharpened Poincare bound proposed in a pasted external
analysis (independently re-derived and verified by hand before implementing -- both algebraic
claims checked: the peeling inequality itself, and gap_2=2*(N-1)/(q*(N-q)) matching the already-
verified general Eberlein spectrum lambda_j=(q-j)*(N-q-j)-j at j=2).

Exact energy identity (already established this session):
    T_q/2 = sum_l gap_l * E_l        (l=1,...,min(q,N-q))
    C_q   = sum_l E_l

Naive point-15 bound (uses only the worst gap, gap_1):
    C_q <= T_q / (2*gap_1)

Sharpened bound (peels off the now-exactly-known E_1, bounds the REST by the next-best gap,
gap_2 -- NOT circular: E_1 and T_q are both computable independently of C_q, gap_1/gap_2 are
pure graph-theoretic constants):
    T_q/2 - gap_1*E_1 = sum_{l>=2} gap_l*E_l >= gap_2 * sum_{l>=2} E_l = gap_2*(C_q - E_1)
    =>  C_q <= E_1 + (T_q/2 - gap_1*E_1) / gap_2

Both T_q (check_johnson_swap_energy.py's swap_energy_per_layer) and E_1
(verify_marginal_effect_l1_predictor.py's marginal_l1_energy_per_layer) are reused UNCHANGED --
no new derivation risk, only a new combination of two already-validated quantities.
"""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def _load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


swap_mod = _load_module("swap_mod_improved", "check_johnson_swap_energy.py")
marginal_mod = _load_module("marginal_mod_improved", "verify_marginal_effect_l1_predictor.py")


def gap1(big_n: int, q: int) -> float:
    return big_n / (q * (big_n - q))


def gap2(big_n: int, q: int) -> float:
    return 2 * (big_n - 1) / (q * (big_n - q))


def improved_bound_for_n(n: int) -> dict:
    t_rows = {r["q"]: r for r in swap_mod.swap_energy_per_layer(n)}
    e_rows = {r["q"]: r for r in marginal_mod.marginal_l1_energy_per_layer(n)}

    rows = []
    # marginal_l1_energy_per_layer already excludes the trivial boundary layers (q=0, q=N,
    # where C_q=0 and T_q is undefined) -- iterate over its domain, not swap_energy_per_layer's
    # wider one, to keep the two dicts' keys aligned.
    for q, t_row in ((q, t_rows[q]) for q in e_rows if q in t_rows):
        big_n = t_row["N"]
        t_q = t_row["T_q"]
        c_q = t_row["C_q"]
        e1 = e_rows[q]["predicted_l1_energy"]
        g1 = gap1(big_n, q)
        g2 = gap2(big_n, q)

        naive_bound = t_q / (2 * g1)
        improved_bound = e1 + (t_q / 2 - g1 * e1) / g2

        rows.append(
            {
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "T_q": t_q,
                "E1": e1,
                "naive_bound": naive_bound,
                "improved_bound": improved_bound,
                "naive_holds": c_q <= naive_bound + 1e-9,
                "improved_holds": c_q <= improved_bound + 1e-9,
                "improved_le_naive": improved_bound <= naive_bound + 1e-9,
            }
        )
        print(
            f"  q={q:2d}/{big_n:2d}  C_q={c_q:.6f}  naive_bound={naive_bound:.6f}  "
            f"improved_bound={improved_bound:.6f}  "
            f"naive_holds={c_q <= naive_bound + 1e-9}  "
            f"improved_holds={c_q <= improved_bound + 1e-9}  "
            f"improved<=naive={improved_bound <= naive_bound + 1e-9}",
            flush=True,
        )
    return {"n": n, "rows": rows}


def aggregate(n: int, rows: list[dict]) -> dict:
    total_c = 0.0
    total_naive = 0.0
    total_improved = 0.0
    for r in rows:
        big_n = r["N"]
        q = r["q"]
        w_q = comb(big_n, q) / (2**big_n)
        total_c += w_q * r["C_q"]
        total_naive += w_q * r["naive_bound"]
        total_improved += w_q * r["improved_bound"]
    return {
        "n": n,
        "n2_observed": n**2 * total_c,
        "n2_naive_bound": n**2 * total_naive,
        "n2_improved_bound": n**2 * total_improved,
        "naive_tightness": total_c / total_naive if total_naive > 0 else float("nan"),
        "improved_tightness": total_c / total_improved if total_improved > 0 else float("nan"),
    }


if __name__ == "__main__":
    out = {}
    agg_summary = []
    for n in [23, 29, 31, 37, 41, 43, 47]:
        print(f"\n--- n={n} ---")
        result = improved_bound_for_n(n)
        out[n] = result["rows"]
        agg = aggregate(n, result["rows"])
        agg_summary.append(agg)
        print(
            f"  AGGREGATE n={n}: n2*observed={agg['n2_observed']:.4f}  "
            f"n2*naive={agg['n2_naive_bound']:.4f}  n2*improved={agg['n2_improved_bound']:.4f}  "
            f"naive_tightness={agg['naive_tightness']:.4f}  "
            f"improved_tightness={agg['improved_tightness']:.4f}"
        )

    print("\n=== SUMMARY ===")
    for agg in agg_summary:
        print(
            f"n={agg['n']:3d}  n2*obs={agg['n2_observed']:7.4f}  "
            f"n2*naive={agg['n2_naive_bound']:7.4f}  n2*improved={agg['n2_improved_bound']:7.4f}  "
            f"naive_tight={agg['naive_tightness']:.4f}  "
            f"improved_tight={agg['improved_tightness']:.4f}"
        )

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "improved_poincare_bound.json", "w", encoding="utf-8") as f:
        json.dump({"per_layer": out, "aggregate": agg_summary}, f, indent=2)
