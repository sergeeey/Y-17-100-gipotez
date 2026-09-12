"""Final, definitive three-term ladder bound: uses the analytic (pinv-free) E_2 from
check_l2_analytic_projection.py, resolving decision.md point 18's numerical discrepancy.
Single shared theta_full per n (as in check_l3_ladder_bound_unified.py), all quantities derived
from one source, E_2 now via the verified closed-form projection instead of a Gram-matrix pinv.

    C_q  <=  E_1 + E_2 + (T_q/2 - gamma_1*E_1 - gamma_2*E_2) / gamma_3
"""

from __future__ import annotations

import importlib.util
import json
from itertools import combinations
from math import comb
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def _load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


nm = _load_module("nm_l3analytic", "check_necklace_orbit_reduction.py")
l2a = _load_module("l2a_l3analytic", "check_l2_analytic_projection.py")


def gamma(level: int, big_n: int, q: int) -> float:
    return level * (big_n - level + 1) / (q * (big_n - q))


def analytic_ladder_for_n(n: int) -> list[dict]:
    m = (n - 1) // 2
    ground = list(range(1, m))
    big_n = len(ground)

    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x_arr = np.log(theta_full / np.sqrt(n))
    n_subsets = 1 << m
    delta = np.empty(n_subsets)
    for mask in range(n_subsets):
        if mask & 1:
            continue
        delta[mask] = x_arr[mask] - x_arr[mask | 1]

    pairs = list(combinations(range(big_n), 2))

    rows = []
    for q in range(1, big_n):
        subsets = list(combinations(ground, q))
        masks = np.array([sum(1 << b for b in s) for s in subsets])
        f = delta[masks]
        c_q = float(np.var(f))
        v = len(subsets)
        f_centered = f - f.mean()

        big_e = np.zeros((v, big_n))
        for row_idx, s in enumerate(subsets):
            big_e[row_idx, [ground.index(g) for g in s]] = 1.0

        # T_q: swap-Dirichlet-energy
        sq_diffs = []
        for mask, combo in zip(masks, subsets):
            in_set = set(combo)
            out_set = [b for b in ground if b not in in_set]
            d_s = delta[mask]
            for a in combo:
                base = mask & ~(1 << a)
                for b in out_set:
                    mask_swapped = base | (1 << b)
                    sq_diffs.append((d_s - delta[mask_swapped]) ** 2)
        t_q = float(np.mean(sq_diffs)) if sq_diffs else float("nan")

        mu_e = big_e.T @ f_centered / v
        e1 = l2a.e1_closed_form(big_n, q, mu_e)

        m_full = (big_e * f_centered[:, None]).T @ big_e / v
        mu_pairs = np.array([m_full[a, b] for a, b in pairs])
        e2 = l2a.e2_analytic(big_n, q, mu_pairs, pairs)

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
                "T_q": t_q,
                "E1": e1,
                "E2": e2,
                "naive_bound": naive_bound,
                "two_term_bound": two_term_bound,
                "three_term_bound": three_term_bound,
                "three_holds": c_q <= three_term_bound + 1e-9,
                "three_le_two": three_term_bound <= two_term_bound + 1e-9,
                "two_holds": c_q <= two_term_bound + 1e-9,
            }
        )
        print(
            f"  q={q:2d}/{big_n:2d}  C_q={c_q:.9f}  two={two_term_bound:.9f}  "
            f"three={three_term_bound:.9f}  three_holds={c_q <= three_term_bound + 1e-9}  "
            f"three<=two={three_term_bound <= two_term_bound + 1e-9}",
            flush=True,
        )
    return rows


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
        "naive_tightness": total_c / total_naive,
        "two_term_tightness": total_c / total_two,
        "three_term_tightness": total_c / total_three,
    }


if __name__ == "__main__":
    out = {}
    agg_summary = []
    all_violations = []
    for n in [23, 29, 31, 37, 41, 43, 47]:
        print(f"\n--- n={n} (analytic, no pinv) ---")
        rows = analytic_ladder_for_n(n)
        out[n] = rows
        for r in rows:
            if not r["three_holds"] or not r["three_le_two"] or not r["two_holds"]:
                all_violations.append({"n": n, **r})
        agg = aggregate(n, rows)
        agg_summary.append(agg)
        print(
            f"  AGGREGATE n={n}: naive_tight={agg['naive_tightness']:.4f}  "
            f"two_tight={agg['two_term_tightness']:.4f}  "
            f"three_tight={agg['three_term_tightness']:.4f}"
        )

    print("\n=== SUMMARY (analytic E_2, no pinv) ===")
    for agg in agg_summary:
        print(
            f"n={agg['n']:3d}  n2*obs={agg['n2_observed']:7.4f}  "
            f"naive_tight={agg['naive_tightness']:.4f}  "
            f"two_tight={agg['two_term_tightness']:.4f}  "
            f"three_tight={agg['three_term_tightness']:.4f}"
        )

    print(f"\n=== VIOLATIONS: {len(all_violations)} ===")
    for v in all_violations:
        print(f"  n={v['n']} q={v['q']}: C_q={v['C_q']} three={v['three_term_bound']}")

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l3_ladder_bound_analytic.json", "w", encoding="utf-8") as f:
        json.dump(
            {"per_layer": out, "aggregate": agg_summary, "violations": all_violations},
            f,
            indent=2,
        )
