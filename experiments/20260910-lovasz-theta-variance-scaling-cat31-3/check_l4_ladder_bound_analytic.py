"""Exam 2, stage E (the "kill-or-promote" test): four-term sharpened Poincare ladder bound,
extending check_l3_ladder_bound_analytic.py's three-term bound with the now-verified E_3 (points
19-20, cross-validated 22/22 against exact diagonalization at n=23,29,31, and the efficient
(v,C(N,2))-based computation, sanity-checked to match brute-force exactly before trusting
n=37-47, decision.md point 21).

    C_q  <=  E_1 + E_2 + E_3 + (T_q/2 - gamma_1*E_1 - gamma_2*E_2 - gamma_3*E_3) / gamma_4

E_3 = 0 at q in {1,2,N-2,N-1} (l=3 doesn't exist there -- min(q,N-q)<3), matching the same
boundary convention already used for E_2 at q in {1,N-1}.

Question this settles (per the user's explicit priority, 2026-09-12): does the excess-growth-
halving pattern of naive->two-term->three-term (91.3pp->69.3pp->32.8pp, decision.md point 18)
continue at a fourth rung, or does it plateau? A strong fourth-rung improvement is a real signal
for a general law (Exam 3); a weak one means the ladder mechanism itself may be near its limit.
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


nm = _load_module("nm_l4analytic", "check_necklace_orbit_reduction.py")
l2a = _load_module("l2a_l4analytic", "check_l2_analytic_projection.py")


def gamma(level: int, big_n: int, q: int) -> float:
    return level * (big_n - level + 1) / (q * (big_n - q))


def four_term_ladder_for_n(n: int) -> list[dict]:
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
    pair_index = {(a, b): i for i, (a, b) in enumerate(pairs)}

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
        x_centered = big_e - q / big_n

        # T_q: swap-Dirichlet-energy (unchanged from check_l3_ladder_bound_analytic.py)
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
        c1_f = mu_e * big_n * (big_n - 1) / (q * (big_n - q))
        p1_f = x_centered @ c1_f

        m_full = (big_e * f_centered[:, None]).T @ big_e / v
        mu_pairs = np.array([m_full[a, b] for a, b in pairs])
        e2 = l2a.e2_analytic(big_n, q, mu_pairs, pairs)

        e3 = 0.0
        if q >= 3 and big_n - q >= 3:
            big_e_pair = np.zeros((v, len(pairs)))
            for i, (a, b) in enumerate(pairs):
                big_e_pair[:, i] = big_e[:, a] * big_e[:, b]
            y_ab = (
                big_e_pair
                - (q - 1)
                / (big_n - 2)
                * (big_e[:, [a for a, b in pairs]] + big_e[:, [b for a, b in pairs]])
                + q * (q - 1) / ((big_n - 1) * (big_n - 2))
            )
            lam2 = gamma_scalar(2, q, big_n)
            s_row = np.zeros(big_n)
            for (a, b), mu in zip(pairs, mu_pairs):
                s_row[a] += mu
                s_row[b] += mu
            big_s = float(np.sum(mu_pairs))
            r_f = np.array(
                [
                    mu_pairs[i]
                    - (s_row[a] + s_row[b]) / (big_n - 2)
                    + 2 * big_s / ((big_n - 1) * (big_n - 2))
                    for i, (a, b) in enumerate(pairs)
                ]
            )
            d_coef_f = r_f / lam2
            p2_f = y_ab @ d_coef_f

            def cov_with_all_triples(w: np.ndarray) -> np.ndarray:
                weighted = big_e_pair * w[:, None]
                return (weighted.T @ big_e) / v

            m_f = cov_with_all_triples(f_centered)
            m_p1 = cov_with_all_triples(p1_f)
            m_p2 = cov_with_all_triples(p2_f)
            m_net = m_f - m_p1 - m_p2

            triples = list(combinations(range(big_n), 3))
            mu_abc = np.empty(len(triples))
            for i, (a, b, c) in enumerate(triples):
                mu_abc[i] = m_net[pair_index[(a, b)], c]
            lam3 = gamma_scalar(3, q, big_n)
            e3 = float(np.sum(mu_abc**2) / lam3) if lam3 != 0 else 0.0

        g1 = gamma(1, big_n, q)
        g2 = gamma(2, big_n, q)
        g3 = gamma(3, big_n, q)
        g4 = gamma(4, big_n, q)
        naive_bound = t_q / (2 * g1)
        two_term_bound = e1 + (t_q / 2 - g1 * e1) / g2
        three_term_bound = e1 + e2 + (t_q / 2 - g1 * e1 - g2 * e2) / g3
        four_term_bound = e1 + e2 + e3 + (t_q / 2 - g1 * e1 - g2 * e2 - g3 * e3) / g4

        rows.append(
            {
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "T_q": t_q,
                "E1": e1,
                "E2": e2,
                "E3": e3,
                "naive_bound": naive_bound,
                "two_term_bound": two_term_bound,
                "three_term_bound": three_term_bound,
                "four_term_bound": four_term_bound,
                "four_holds": c_q <= four_term_bound + 1e-9,
                "four_le_three": four_term_bound <= three_term_bound + 1e-9,
                "three_holds": c_q <= three_term_bound + 1e-9,
                "three_le_two": three_term_bound <= two_term_bound + 1e-9,
                "two_holds": c_q <= two_term_bound + 1e-9,
            }
        )
        print(
            f"  q={q:2d}/{big_n:2d}  C_q={c_q:.9f}  three={three_term_bound:.9f}  "
            f"four={four_term_bound:.9f}  four_holds={c_q <= four_term_bound + 1e-9}  "
            f"four<=three={four_term_bound <= three_term_bound + 1e-9}",
            flush=True,
        )
    return rows


def gamma_scalar(level: int, q: int, big_n: int) -> float:
    """The e2_analytic/e3-formula scalar lambda_l = [q]_l[N-q]_l/[N]_{2l} -- DIFFERENT from the
    swap-walk gamma() above (same greek letter used for two distinct quantities in this
    codebase's prior art; kept as a separate name here to avoid silently confusing the two)."""
    num = 1.0
    for i in range(level):
        num *= (q - i) * (big_n - q - i)
    den = 1.0
    for i in range(2 * level):
        den *= big_n - i
    return num / den


def aggregate(n: int, rows: list[dict]) -> dict:
    total_c = total_naive = total_two = total_three = total_four = 0.0
    for r in rows:
        big_n = r["N"]
        q = r["q"]
        w_q = comb(big_n, q) / (2**big_n)
        total_c += w_q * r["C_q"]
        total_naive += w_q * r["naive_bound"]
        total_two += w_q * r["two_term_bound"]
        total_three += w_q * r["three_term_bound"]
        total_four += w_q * r["four_term_bound"]
    return {
        "n": n,
        "n2_observed": n**2 * total_c,
        "naive_tightness": total_c / total_naive,
        "two_term_tightness": total_c / total_two,
        "three_term_tightness": total_c / total_three,
        "four_term_tightness": total_c / total_four,
    }


if __name__ == "__main__":
    out = {}
    agg_summary = []
    all_violations = []
    for n in [23, 29, 31, 37, 41, 43, 47]:
        print(f"\n--- n={n} (four-term, efficient E_3) ---")
        rows = four_term_ladder_for_n(n)
        out[n] = rows
        for r in rows:
            if not r["four_holds"] or not r["four_le_three"]:
                all_violations.append({"n": n, **r})
        agg = aggregate(n, rows)
        agg_summary.append(agg)
        print(
            f"  AGGREGATE n={n}: naive={agg['naive_tightness']:.4f}  "
            f"two={agg['two_term_tightness']:.4f}  three={agg['three_term_tightness']:.4f}  "
            f"four={agg['four_term_tightness']:.4f}"
        )

    print("\n=== SUMMARY ===")
    for agg in agg_summary:
        print(
            f"n={agg['n']:3d}  n2*obs={agg['n2_observed']:7.4f}  "
            f"naive={agg['naive_tightness']:.4f}  two={agg['two_term_tightness']:.4f}  "
            f"three={agg['three_term_tightness']:.4f}  four={agg['four_term_tightness']:.4f}"
        )

    print(f"\n=== VIOLATIONS: {len(all_violations)} ===")
    for v in all_violations:
        print(f"  n={v['n']} q={v['q']}: C_q={v['C_q']} four={v['four_term_bound']}")

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l4_ladder_bound_analytic.json", "w", encoding="utf-8") as f:
        json.dump(
            {"per_layer": out, "aggregate": agg_summary, "violations": all_violations},
            f,
            indent=2,
        )
