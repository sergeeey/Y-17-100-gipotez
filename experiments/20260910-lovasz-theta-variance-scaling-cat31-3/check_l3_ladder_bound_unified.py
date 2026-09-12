"""Common-source re-verification of point 18's three-term ladder bound, per direct user
concern: the earlier check_l3_ladder_bound.py computed T_q, E_1, E_2 via THREE independent
calls to solve_orbit_reduced (one per reused module), and a handful of layers showed ~1e-6
violations of C_q<=bound / three<=two -- plausibly from catastrophic cancellation amplifying
tiny cross-recomputation differences, but not proven until isolated.

This script computes theta_full ONCE per n and derives C_q, T_q, E_1, E_2, and the ladder
bounds ALL from that single source, eliminating the cross-recomputation as a possible cause.
All formulas (swap-energy, marginal-effect E_1 closed form, pairwise E_2 via the verified
hypergeometric Gram matrix) are reused UNCHANGED from check_johnson_swap_energy.py,
verify_marginal_effect_l1_predictor.py, and check_l2_pairwise_energy.py -- only the theta/delta
SOURCE is now shared, not the math.
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


nm = _load_module("nm_unified", "check_necklace_orbit_reduction.py")
l2_mod = _load_module("l2_mod_unified", "check_l2_pairwise_energy.py")


def gamma(level: int, big_n: int, q: int) -> float:
    return level * (big_n - level + 1) / (q * (big_n - q))


def unified_ladder_for_n(n: int) -> list[dict]:
    m = (n - 1) // 2
    ground = list(range(1, m))
    big_n = len(ground)

    # ONE shared theta computation for this n
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

        # T_q: swap-Dirichlet-energy (SAME delta/masks as everything else here)
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

        # E_1: marginal-effect closed form (SAME f_centered/big_e)
        mu_e = big_e.T @ f_centered / v
        e1 = float(np.sum(mu_e**2) * big_n * (big_n - 1) / (q * (big_n - q)))

        # E_2: pairwise, via l2_mod's verified Gram-matrix machinery (SAME f_centered/big_e)
        m_full = (big_e * f_centered[:, None]).T @ big_e / v
        mu_pairs = np.array([m_full[a, b] for a, b in pairs])
        mu_vec = np.concatenate([mu_e, mu_pairs])
        gram = l2_mod.build_gram_matrix(big_n, q, pairs)
        gram_pinv = np.linalg.pinv(gram)
        e_le2 = float(mu_vec @ gram_pinv @ mu_vec)
        e2 = e_le2 - e1

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
            f"  q={q:2d}/{big_n:2d}  C_q={c_q:.8f}  two={two_term_bound:.8f}  "
            f"three={three_term_bound:.8f}  three_holds={c_q <= three_term_bound + 1e-9}  "
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
    all_violations = []
    for n in [23, 29, 31, 37, 41, 43, 47]:
        print(f"\n--- n={n} (unified single-source) ---")
        rows = unified_ladder_for_n(n)
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

    print("\n=== SUMMARY (unified single-source) ===")
    for agg in agg_summary:
        print(
            f"n={agg['n']:3d}  n2*obs={agg['n2_observed']:7.4f}  "
            f"naive_tight={agg['naive_tightness']:.4f}  "
            f"two_tight={agg['two_term_tightness']:.4f}  "
            f"three_tight={agg['three_term_tightness']:.4f}"
        )

    print(
        f"\n=== VIOLATIONS (should be empty if unification fixed the noise): "
        f"{len(all_violations)} ==="
    )
    for v in all_violations:
        print(f"  n={v['n']} q={v['q']}: {v}")

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l3_ladder_bound_unified.json", "w", encoding="utf-8") as f:
        json.dump(
            {"per_layer": out, "aggregate": agg_summary, "violations": all_violations},
            f,
            indent=2,
        )
