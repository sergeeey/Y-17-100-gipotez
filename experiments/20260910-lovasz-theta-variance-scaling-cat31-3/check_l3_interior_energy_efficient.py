"""Exam 2, stage D: scale the verified interior-layer E_3(q) formula (check_l3_interior_energy.py,
22/22 violations at n=23,29,31) to n=37,41,43,47, where the direct (v, C(N,3)) matrix
construction is infeasible (n=47: v up to 705432, C(22,3)=1540 -> ~8.7GB just for one matrix).

Per the user's explicit direction (2026-09-12): extending E_3 to all 7 n and computing the full
four-term sharpened Poincare ladder is a "kill-or-promote" test for the whole Johnson-ladder
mechanism -- does the excess-growth-halving pattern (91.3pp -> 69.3pp -> 32.8pp, naive/two-term/
three-term) continue at a fourth rung, or does it plateau? This is a cheaper, more decisive
question than jumping straight to a general law for arbitrary l (deferred Exam 3).

Key algebraic reduction (avoiding (v, C(N,3)) entirely): from check_l3_interior_energy.py,

    mu_abc = Cov(f, z_abc)  where z_abc = E_abc_centered - P_1[E_abc] - P_2[E_abc]
           = Cov(f, E_abc) - Cov(P_1(f), E_abc) - Cov(P_2(f), E_abc)   (self-adjointness of the
                                                                          projection operators)

For ANY weight vector w (f_centered, P_1(f), or P_2(f) in turn), Cov(w, E_abc) for ALL triples
(a,b,c) can be computed via ONE matmul against the ALREADY-BUILT (v, C(N,2)) pair-indicator
matrix `big_e_pair` -- no (v, C(N,3)) structure is ever materialized:

    weighted = big_e_pair * w[:, None]            (v, C(N,2))
    M_w[ab_idx, c] = (weighted.T @ big_e)[ab_idx, c] / v = Cov(w, E_{a,b,c})   (C(N,2), N)

(valid only for c not in {a,b} -- those entries are masked out when extracting triples). Running
this three times (w = f_centered, P_1(f), P_2(f)) and subtracting gives mu_abc directly, reusing
structures already built for the P_1/P_2 machinery (big_e_pair is already needed for y_ab). Peak
memory is O(v * C(N,2)), the SAME class already handled successfully at n=47 by
check_l2_analytic_projection.py -- not a new scaling regime.

Verification order: (1) re-derive n=23,29,31 with this method and confirm EXACT agreement with
check_l3_interior_energy.py's already-verified brute-force result (sanity check the reduction
itself, not just trust the algebra); (2) only then run n=37,41,43,47.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_mod = importlib.util.spec_from_file_location(
    "necklace_mod_l3eff", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)


def lambda_l(q: int, big_n: int, level: int) -> float:
    num = 1.0
    for i in range(level):
        num *= (q - i) * (big_n - q - i)
    den = 1.0
    for i in range(2 * level):
        den *= big_n - i
    return num / den


def e3_efficient(n: int, q_values: list[int] | None = None) -> list[dict]:
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
    layers = q_values if q_values is not None else range(3, big_n - 2)
    for q in layers:
        if q < 3 or big_n - q < 3:
            continue
        subsets = list(combinations(ground, q))
        v = len(subsets)
        masks = np.array([sum(1 << b for b in s) for s in subsets])
        f = delta[masks]
        c_q = float(np.var(f))
        f_centered = f - f.mean()

        big_e = np.zeros((v, big_n))
        for row_idx, s in enumerate(subsets):
            big_e[row_idx, [ground.index(g) for g in s]] = 1.0
        x_centered = big_e - q / big_n

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

        mu_e_f = big_e.T @ f_centered / v
        c1_f = mu_e_f * big_n * (big_n - 1) / (q * (big_n - q))
        p1_f = x_centered @ c1_f
        e1 = float(np.mean(p1_f**2))

        m_full_f = (big_e * f_centered[:, None]).T @ big_e / v
        mu_pairs_f = np.array([m_full_f[a, b] for a, b in pairs])
        lam2 = lambda_l(q, big_n, 2)
        s_row = np.zeros(big_n)
        for (a, b), mu in zip(pairs, mu_pairs_f):
            s_row[a] += mu
            s_row[b] += mu
        big_s = float(np.sum(mu_pairs_f))
        r_f = np.array(
            [
                mu_pairs_f[i]
                - (s_row[a] + s_row[b]) / (big_n - 2)
                + 2 * big_s / ((big_n - 1) * (big_n - 2))
                for i, (a, b) in enumerate(pairs)
            ]
        )
        d_coef_f = r_f / lam2
        p2_f = y_ab @ d_coef_f
        e2 = float(np.sum(r_f**2) / lam2)

        # -- efficient triple-covariance step: one (C(N,2), N)-shaped matmul per weight vector,
        # no (v, C(N,3)) structure ever built.
        def cov_with_all_triples(w: np.ndarray) -> np.ndarray:
            weighted = big_e_pair * w[:, None]  # (v, n_pairs)
            return (weighted.T @ big_e) / v  # (n_pairs, big_n): [ab_idx, c] = Cov(w, E_abc)

        m_f = cov_with_all_triples(f_centered)
        m_p1 = cov_with_all_triples(p1_f)
        m_p2 = cov_with_all_triples(p2_f)
        m_net = m_f - m_p1 - m_p2  # [ab_idx, c] = mu_abc for triple {a,b,c}, a<b, c arbitrary

        triples = list(combinations(range(big_n), 3))
        mu_abc = np.empty(len(triples))
        for i, (a, b, c) in enumerate(triples):
            # extract via the pair (a,b) column at row c -- any of the 3 pair choices agree by
            # symmetry of Cov(f, E_abc); using the smallest-index pair consistently.
            mu_abc[i] = m_net[pair_index[(a, b)], c]

        lam3 = lambda_l(q, big_n, 3)
        e3 = float(np.sum(mu_abc**2) / lam3) if lam3 != 0 else 0.0

        rows.append(
            {
                "n": n,
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "E1": e1,
                "E2": e2,
                "E3": e3,
                "E3_frac_of_Cq": e3 / c_q if c_q > 0 else float("nan"),
            }
        )
        print(
            f"n={n:3d} q={q:2d}/{big_n:2d}  C_q={c_q:.8f}  E1={e1:.8f}  E2={e2:.8f}  E3={e3:.8f}  "
            f"E1+E2+E3={e1 + e2 + e3:.8f}  E3/C_q={e3 / c_q:.4f}",
            flush=True,
        )
    return rows


def cross_check_against_bruteforce(rows: list[dict], tol: float = 1e-9) -> list[dict]:
    """Sanity check: at n=23,29,31, this efficient method should EXACTLY match the already-
    verified brute-force result from check_l3_interior_energy.py's metrics file."""
    bf = json.load(open(METRICS / "l3_interior_energy.json", encoding="utf-8"))
    bf_by_nq = {(r["n"], r["q"]): r["E3_formula"] for r in bf["rows"]}
    out = []
    for row in rows:
        key = (row["n"], row["q"])
        bf_e3 = bf_by_nq.get(key)
        match = abs(bf_e3 - row["E3"]) < tol if bf_e3 is not None else None
        out.append(
            {
                "n": row["n"],
                "q": row["q"],
                "efficient_E3": row["E3"],
                "bruteforce_E3": bf_e3,
                "match": match,
            }
        )
        if bf_e3 is not None:
            eff = row["E3"]
            print(
                f"  n={row['n']:3d} q={row['q']:2d}  eff={eff:.10f}  bf={bf_e3:.10f}  match={match}"
            )
    return out


if __name__ == "__main__":
    print("=== Sanity check: n=23,29,31 must match brute-force exactly ===")
    sanity_rows = []
    for n in [23, 29, 31]:
        print(f"\n--- n={n} ---")
        sanity_rows.extend(e3_efficient(n))
    print("\n=== Cross-check against check_l3_interior_energy.py's verified brute-force result ===")
    checks = cross_check_against_bruteforce(sanity_rows)
    sanity_violations = [c for c in checks if c["match"] is False]
    print(f"\nSanity violations: {len(sanity_violations)}/{len(checks)}")
    if sanity_violations:
        print("SANITY CHECK FAILED -- stopping before running larger n.")
        raise SystemExit(1)

    print("\n=== Extending to n=37,41,43,47 ===")
    big_rows = []
    for n in [37, 41, 43, 47]:
        print(f"\n--- n={n} ---")
        big_rows.extend(e3_efficient(n))

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l3_interior_energy_efficient.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "sanity_n23_29_31": sanity_rows,
                "sanity_cross_check": checks,
                "n37_to_47": big_rows,
            },
            f,
            indent=2,
        )
    print(f"\nTotal n=37-47 layers computed: {len(big_rows)}")
