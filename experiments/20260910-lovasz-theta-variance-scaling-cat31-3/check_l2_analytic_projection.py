"""Definitive, pinv-free E_2 computation -- replaces check_l2_pairwise_energy.py's numerically
fragile approach (raw {e_j, e_j*e_k} features are linearly dependent, forcing a pseudo-inverse
that introduced ~1e-6 to 5e-5 noise at low-min(q,N-q) layers, see decision.md point 18's two
in-session corrections).

Closed-form V_2 projection, proposed in a pasted external analysis and independently verified
against BOTH exact diagonalization (n=23,29,31, ALL OK to ~1e-9) and the q=2,N-2 zero-residual
unit test (E_1+E_2=C_q exactly, since min(q,N-q)=2 means l=1,2 are the ONLY existing levels
there) -- verified exact at all 7 tested n, not just some. This verification is NOT ad hoc: see
verify_l2_analytic_against_diagonalization.py + metrics/l2_analytic_verification.json for the
persisted, independently-re-runnable check (0/34 diagonalization violations, 0/14 zero-residual
violations) -- added after a reviewer agent (2026-09-12) correctly flagged that an earlier
revision of this docstring claimed this verification without a repo artifact backing it
(audit-verification-gate.md: a claim's own [VERIFIED] is the next reader's [INFERRED] unless the
check is actually in the repo to re-run).

    mu_ab = Cov(f, e_a*e_b)                      (pairwise marginal effect)
    s_a   = sum_{b!=a} mu_ab
    S     = sum_{a<b} mu_ab
    r_ab  = mu_ab - (s_a+s_b)/(N-2) + 2S/((N-1)(N-2))     (orthogonal projection onto pure V_2)
    lambda_2 = q(q-1)(N-q)(N-q-1) / (N(N-1)(N-2)(N-3))    (V_2's scalar covariance eigenvalue)
    E_2 = sum_{a<b} r_ab^2 / lambda_2

No Gram matrix, no pinv, no redundant raw features -- r_ab lives exactly in V_2 by construction
(the double-centering removes the V_0,V_1 leakage that made the raw {e_j*e_k} features
redundant with {e_j}), so lambda_2 acts as a genuine scalar, not an approximation.
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
    "necklace_mod_l2analytic", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)


def e1_closed_form(big_n: int, q: int, mu_e: np.ndarray) -> float:
    return float(np.sum(mu_e**2) * big_n * (big_n - 1) / (q * (big_n - q)))


def e2_analytic(big_n: int, q: int, mu_pairs: np.ndarray, pairs: list[tuple[int, int]]) -> float:
    if big_n <= 3:
        return 0.0
    lam2 = (
        q
        * (q - 1)
        * (big_n - q)
        * (big_n - q - 1)
        / (big_n * (big_n - 1) * (big_n - 2) * (big_n - 3))
    )
    if lam2 == 0:
        return 0.0
    s = np.zeros(big_n)
    for (a, b), mu in zip(pairs, mu_pairs):
        s[a] += mu
        s[b] += mu
    big_s = float(np.sum(mu_pairs))
    r = np.array(
        [
            mu_pairs[i] - (s[a] + s[b]) / (big_n - 2) + 2 * big_s / ((big_n - 1) * (big_n - 2))
            for i, (a, b) in enumerate(pairs)
        ]
    )
    return float(np.sum(r**2) / lam2)


def l2_energy_per_layer(n: int) -> list[dict]:
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

        mu_e = big_e.T @ f_centered / v
        m_full = (big_e * f_centered[:, None]).T @ big_e / v
        mu_pairs = np.array([m_full[a, b] for a, b in pairs])

        e1 = e1_closed_form(big_n, q, mu_e)
        e2 = e2_analytic(big_n, q, mu_pairs, pairs)

        rows.append(
            {
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "E1": e1,
                "E2": e2,
                "E2_frac_of_Cq": e2 / c_q if c_q > 0 else float("nan"),
            }
        )
        print(
            f"  q={q:2d}/{big_n:2d}  C_q={c_q:.8f}  E1={e1:.8f}  E2={e2:.8f}  E1+E2={e1 + e2:.8f}",
            flush=True,
        )
    return rows


if __name__ == "__main__":
    out = {}
    for n in [23, 29, 31, 37, 41, 43, 47]:
        print(f"\n--- n={n} (analytic E_2, no pinv) ---")
        out[n] = l2_energy_per_layer(n)

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l2_analytic_projection.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
