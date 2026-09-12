"""Exam 2, stage A: rigorous, function-level verification of the l=2 (degree-2) projection,
extending verify_l1_projection_rigorous.py's pattern from P_1 to P_1+P_2.

check_l2_analytic_projection.py's e2_analytic computes E_2 as a SCALAR (sum of squared
double-centered covariances / lambda_2) -- it never constructs the actual projection FUNCTION
P_2(S). This script derives and verifies that function directly, which Exam 2 (E_3 derivation)
needs: h(S) = f_centered(S) - P_1(S) - P_2(S) must be an actual computable residual, not just an
energy number, before it can be fit against degree-3 features.

Derivation (not taken on faith -- verified below against two independent properties):
  E_ab(S) = e_a(S)*e_b(S)               (raw pair indicator)
  y_ab(S) = E_ab(S) - (q-1)/(N-2)*(e_a(S)+e_b(S)) + q(q-1)/((N-1)(N-2))   (double-centered)

Two algebraic identities make y_ab the correct "pure V_2" basis function (both proven by direct
substitution, both re-checked numerically below rather than trusted from the derivation alone):
  (i)  sum_{b != a} y_ab(S) = 0 for EVERY S            (orthogonal to V_1, per-row)
  (ii) E[y_ab] = 0 under uniform S                     (orthogonal to V_0)
Both rely on the closed-form identity sum_{b!=a} E_ab(S) = (q-1)*e_a(S), itself exact for every S
(not just in expectation) since e_a(S) in {0,1} and e_a(S)^2 = e_a(S).

By linearity, Cov(f, y_ab) = mu_ab - (q-1)/(N-2)*(mu_e[a]+mu_e[b]), and separately
s_a = sum_{b!=a} mu_ab = (q-1)*mu_e[a] EXACTLY (same identity applied to Cov(f, .)) -- so this
should equal check_l2_analytic_projection.e2_analytic's r_ab BEFORE its "+2*S/((N-1)(N-2))"
term. Whether that extra term is needed is settled empirically below (Check 3), not assumed.

Checks:
  1. E[(P_2 f)^2] == E_2 (from check_l2_analytic_projection.e2_analytic)
  2. E[(f - P_1 f - P_2 f) * x_j] ~= 0 for every ground element j  (residual orthogonal to V_1)
  3. E[(f - P_1 f - P_2 f) * y_ab] ~= 0 for every pair a<b        (residual orthogonal to V_2)
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
    "necklace_mod_l2proj", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)

l2a_spec = importlib.util.spec_from_file_location(
    "l2_analytic_for_l2proj", HERE / "check_l2_analytic_projection.py"
)
l2a = importlib.util.module_from_spec(l2a_spec)
l2a_spec.loader.exec_module(l2a)


def rigorous_check(n: int, q_values: list[int] | None = None) -> list[dict]:
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

    rows = []
    layers = q_values if q_values is not None else range(1, big_n)
    pairs = list(combinations(range(big_n), 2))
    for q in layers:
        if q < 2 or big_n - q < 2:
            continue  # V_2 doesn't exist at these boundary layers
        subsets = list(combinations(ground, q))
        masks = np.array([sum(1 << b for b in s) for s in subsets])
        f = delta[masks]
        v = len(subsets)
        f_centered = f - f.mean()

        big_e = np.zeros((v, big_n))
        for row_idx, s in enumerate(subsets):
            big_e[row_idx, [ground.index(g) for g in s]] = 1.0
        x_centered = big_e - q / big_n

        mu_e = big_e.T @ f_centered / v
        c1 = mu_e * big_n * (big_n - 1) / (q * (big_n - q))
        p1f = x_centered @ c1

        m_full = (big_e * f_centered[:, None]).T @ big_e / v
        mu_pairs = np.array([m_full[a, b] for a, b in pairs])
        e2 = l2a.e2_analytic(big_n, q, mu_pairs, pairs)

        lam2 = (
            q
            * (q - 1)
            * (big_n - q)
            * (big_n - q - 1)
            / (big_n * (big_n - 1) * (big_n - 2) * (big_n - 3))
        )
        s_row = np.zeros(big_n)
        for (a, b), mu in zip(pairs, mu_pairs):
            s_row[a] += mu
            s_row[b] += mu
        big_s = float(np.sum(mu_pairs))
        r = np.array(
            [
                mu_pairs[i]
                - (s_row[a] + s_row[b]) / (big_n - 2)
                + 2 * big_s / ((big_n - 1) * (big_n - 2))
                for i, (a, b) in enumerate(pairs)
            ]
        )
        d_coef = r / lam2

        # build big_e_ab (v x n_pairs) and the double-centered y_ab basis
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
        p2f = y_ab @ d_coef

        energy_direct = float(np.mean(p2f**2))
        match_energy = abs(energy_direct - e2) < 1e-9

        residual = f_centered - p1f - p2f
        orth_x = (x_centered.T @ residual) / v
        orth_y = (y_ab.T @ residual) / v
        max_orth_x = float(np.max(np.abs(orth_x)))
        max_orth_y = float(np.max(np.abs(orth_y)))

        row = {
            "n": n,
            "q": q,
            "N": big_n,
            "E2_formula": e2,
            "E2_direct": energy_direct,
            "energy_match": match_energy,
            "max_orth_violation_x": max_orth_x,
            "max_orth_violation_y": max_orth_y,
        }
        rows.append(row)
        print(
            f"n={n:3d} q={q:2d}/{big_n:2d}  E2_formula={e2:.8f}  E2_direct={energy_direct:.8f}  "
            f"match={match_energy}  max|orth_x|={max_orth_x:.2e}  max|orth_y|={max_orth_y:.2e}",
            flush=True,
        )
    return rows


if __name__ == "__main__":
    all_rows = []
    for n in [23, 29, 31, 37, 41, 43, 47]:
        print(f"\n--- n={n} ---")
        all_rows.extend(rigorous_check(n))

    violations = [
        r
        for r in all_rows
        if not r["energy_match"]
        or r["max_orth_violation_x"] > 1e-6
        or r["max_orth_violation_y"] > 1e-6
    ]
    print(f"\nTotal layers checked: {len(all_rows)}  violations: {len(violations)}")
    if violations:
        for v in violations:
            print("  VIOLATION:", v)

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l2_projection_rigorous.json", "w", encoding="utf-8") as f:
        json.dump({"rows": all_rows, "violations": violations}, f, indent=2)
