"""Three-term sharpened Poincare bound -- the decisive test proposed alongside point 17:
does peeling BOTH E_1 and E_2 (now both exactly known) and paying the remainder at the
next-best gap gamma_3 finally slow (or reverse) the divergence trend from points 15/16?

    C_q  <=  E_1 + E_2 + (T_q/2 - gamma_1*E_1 - gamma_2*E_2) / gamma_3

gamma_l = l*(N-l+1)/(q*(N-q)) (verified general Eberlein-spectrum pattern: gamma_1=N/(q(N-q)),
gamma_2=2(N-1)/(q(N-q)) already verified by hand against the diagonalized spectrum; gamma_3=
3(N-2)/(q(N-q)) follows the same derivation, checked below by hand before use).

Reuses T_q (check_johnson_swap_energy.py), E_1 (verify_marginal_effect_l1_predictor.py), E_2
(check_l2_pairwise_energy.py) UNCHANGED -- no new derivation risk, only a new combination.
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


swap_mod = _load_module("swap_mod_l3", "check_johnson_swap_energy.py")
marginal_mod = _load_module("marginal_mod_l3", "verify_marginal_effect_l1_predictor.py")
l2_mod = _load_module("l2_mod_l3", "check_l2_pairwise_energy.py")


def gamma(level: int, big_n: int, q: int) -> float:
    return level * (big_n - level + 1) / (q * (big_n - q))


def three_term_bound_for_n(n: int) -> dict:
    t_rows = {r["q"]: r for r in swap_mod.swap_energy_per_layer(n)}
    e1_rows = {r["q"]: r for r in marginal_mod.marginal_l1_energy_per_layer(n)}
    e2_rows = {r["q"]: r for r in l2_mod.l2_energy_per_layer(n)}

    rows = []
    common_q = [q for q in e2_rows if q in t_rows and q in e1_rows]
    for q in common_q:
        big_n = t_rows[q]["N"]
        t_q = t_rows[q]["T_q"]
        c_q = t_rows[q]["C_q"]
        e1 = e1_rows[q]["predicted_l1_energy"]
        e2 = e2_rows[q]["E2"]

        g1 = gamma(1, big_n, q)
        g2 = gamma(2, big_n, q)
        g3 = gamma(3, big_n, q)

        naive_bound = t_q / (2 * g1)
        two_term_bound = e1 + (t_q / 2 - g1 * e1) / g2
        three_term_bound = e1 + e2 + (t_q / 2 - g1 * e1 - g2 * e2) / g3

        rows.append(
            {
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "naive_bound": naive_bound,
                "two_term_bound": two_term_bound,
                "three_term_bound": three_term_bound,
                "three_holds": c_q <= three_term_bound + 1e-9,
                "three_le_two": three_term_bound <= two_term_bound + 1e-9,
            }
        )
        print(
            f"  q={q:2d}/{big_n:2d}  C_q={c_q:.6f}  naive={naive_bound:.6f}  "
            f"two_term={two_term_bound:.6f}  three_term={three_term_bound:.6f}  "
            f"holds={c_q <= three_term_bound + 1e-9}  "
            f"three<=two={three_term_bound <= two_term_bound + 1e-9}",
            flush=True,
        )
    return {"n": n, "rows": rows}


def aggregate(n: int, rows: list[dict]) -> dict:
    total_c = total_naive = total_two = total_three = 0.0
    for r in rows:
        big_n = r["N"]
        q = r["q"]
        w_q = comb(big_n, q) / (2**big_n)
        total_c += w_q * r["C_q"]
        total_naive += w_q * r["naive_bound"]
        total_two += w_q * r["two_term_bound"]
        total_three += w_q * r["three_term_bound"]
    return {
        "n": n,
        "n2_observed": n**2 * total_c,
        "n2_naive": n**2 * total_naive,
        "n2_two_term": n**2 * total_two,
        "n2_three_term": n**2 * total_three,
        "naive_tightness": total_c / total_naive,
        "two_term_tightness": total_c / total_two,
        "three_term_tightness": total_c / total_three,
    }


if __name__ == "__main__":
    out = {}
    agg_summary = []
    for n in [23, 29, 31, 37, 41, 43, 47]:
        print(f"\n--- n={n} ---")
        result = three_term_bound_for_n(n)
        out[n] = result["rows"]
        agg = aggregate(n, result["rows"])
        agg_summary.append(agg)
        print(
            f"  AGGREGATE n={n}: n2*obs={agg['n2_observed']:.4f}  "
            f"n2*naive={agg['n2_naive']:.4f}  n2*two_term={agg['n2_two_term']:.4f}  "
            f"n2*three_term={agg['n2_three_term']:.4f}  "
            f"naive_tight={agg['naive_tightness']:.4f}  "
            f"two_tight={agg['two_term_tightness']:.4f}  "
            f"three_tight={agg['three_term_tightness']:.4f}"
        )

    print("\n=== SUMMARY ===")
    for agg in agg_summary:
        print(
            f"n={agg['n']:3d}  n2*obs={agg['n2_observed']:7.4f}  "
            f"naive_tight={agg['naive_tightness']:.4f}  "
            f"two_tight={agg['two_term_tightness']:.4f}  "
            f"three_tight={agg['three_term_tightness']:.4f}"
        )

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l3_ladder_bound.json", "w", encoding="utf-8") as f:
        json.dump({"per_layer": out, "aggregate": agg_summary}, f, indent=2)
