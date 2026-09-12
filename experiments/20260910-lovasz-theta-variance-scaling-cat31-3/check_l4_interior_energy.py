"""Exam 3, stage 4: attempt a GENERAL recursive construction for E_l at arbitrary l, tested by
extending one level deeper than point 20 (l=3) to l=4 -- not a closed-form formula, but a
recursive algorithm, following the exact same discipline that made l=3 work (reuse already-
verified lower-level operators as generic projections, verify against boundary + diagonalization
before trusting).

Key simplification found while extending the l=3 construction: the "pure V_3 basis" z_abc(S)
built in check_l3_interior_energy.py (via z_abc = E_abc_centered - P_1[E_abc] - P_2[E_abc], using
each triple's OWN raw indicator as the projection target) is a FIXED basis, independent of which
function f is later correlated against it. This means P_3, as a REUSABLE operator for an
arbitrary target g, is simply:

    mu_abc(g) := Cov(g, z_abc)          (for each triple, using the ALREADY-BUILT z_abc basis)
    P_3[g](S) := sum_{a<b<c} (mu_abc(g)/lambda_3) * z_abc(S)

No new derivation needed -- z_abc only has to be built ONCE (reusing the l=3 code), then P_3[g]
for ANY g (including each of the C(N,4) raw quadruple indicators) is just a projection using the
same fixed basis. This is the GENERAL pattern: at each level k, build the "pure V_k basis" once
(from raw k-index indicators, purified by P_1..P_{k-1}), then P_k[g] for any target g reuses that
basis via a single covariance computation -- recursive, not requiring a fresh symbolic derivation
at each new level.

For l=4: E_abcd(S) = e_a*e_b*e_c*e_d (raw quadruple indicator, degree-4, content only in
V_0..V_4). w_abcd := E_abcd_centered - P_1[E_abcd] - P_2[E_abcd] - P_3[E_abcd] is its pure V_4
part. mu_abcd := Cov(f, w_abcd). lambda_4 is HYPOTHESIZED by extending the verified pattern
(lambda_l = [q]_l[N-q]_l/[N]_{2l}, falling factorials, confirmed for l=1,2,3) to l=4 -- stated as
a hypothesis, verified below, not assumed. E_4 := sum(mu_abcd^2)/lambda_4.

Verification (same two-pronged discipline as l=3, point 20): (1) q=4,N-4 boundary zero-residual
test (min(q,N-q)=4 means l=1..4 are the ONLY levels, so E_4=C_q-E1-E2-E3 exactly, no lambda_4
needed for this check); (2) cross-validation against exact diagonalization (metrics/johnson_
eigenspace_decomposition.json, l=4 eigenspace via the Eberlein formula) at interior layers for
n=23,29,31 where that data exists.

Computational note: requires the full (v, C(N,4)) raw-quadruple matrix (plus the (v,C(N,3)) z_abc
basis as an intermediate) -- feasible only at small N, matching check_l3_interior_energy.py's own
scope (n=23,29,31). Scaling to n=37-47 would need the same matmul-based efficiency trick as
check_l3_interior_energy_efficient.py, not attempted here.
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
    "necklace_mod_l4interior", HERE / "check_necklace_orbit_reduction.py"
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


def interior_e4(n: int, max_layer_size: int = 4000) -> list[dict]:
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
    triples = list(combinations(range(big_n), 3))
    quads = list(combinations(range(big_n), 4))

    rows = []
    for q in range(4, big_n - 3):
        subsets = list(combinations(ground, q))
        v = len(subsets)
        if v > max_layer_size:
            print(f"  q={q}: skipped, layer size {v} too large")
            continue
        masks = np.array([sum(1 << b for b in s) for s in subsets])
        f = delta[masks]
        c_q = float(np.var(f))
        f_centered = f - f.mean()

        big_e = np.zeros((v, big_n))
        for row_idx, s in enumerate(subsets):
            big_e[row_idx, [ground.index(g) for g in s]] = 1.0
        x_centered = big_e - q / big_n

        lam2 = lambda_l(q, big_n, 2)
        lam3 = lambda_l(q, big_n, 3)
        lam4 = lambda_l(q, big_n, 4)

        def p1_of(g_centered):
            mu_e = big_e.T @ g_centered / v
            c1 = mu_e * big_n * (big_n - 1) / (q * (big_n - q))
            return x_centered @ c1

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

        def r_pairs_of(g_centered):
            m_full = (big_e * g_centered[:, None]).T @ big_e / v
            mu_pairs = np.array([m_full[a, b] for a, b in pairs])
            s_row = np.zeros(big_n)
            for (a, b), mu in zip(pairs, mu_pairs):
                s_row[a] += mu
                s_row[b] += mu
            big_s = float(np.sum(mu_pairs))
            return np.array(
                [
                    mu_pairs[i]
                    - (s_row[a] + s_row[b]) / (big_n - 2)
                    + 2 * big_s / ((big_n - 1) * (big_n - 2))
                    for i, (a, b) in enumerate(pairs)
                ]
            )

        def p2_of(g_centered):
            return y_ab @ (r_pairs_of(g_centered) / lam2)

        p1_f = p1_of(f_centered)
        e1 = float(np.mean(p1_f**2))
        r_f_pairs = r_pairs_of(f_centered)
        e2 = float(np.sum(r_f_pairs**2) / lam2)

        big_e_triple = np.zeros((v, len(triples)))
        for i, (a, b, c) in enumerate(triples):
            big_e_triple[:, i] = big_e[:, a] * big_e[:, b] * big_e[:, c]
        eabc_centered = big_e_triple - big_e_triple.mean(axis=0)
        p1_triples = p1_of(eabc_centered)
        p2_triples = np.column_stack([p2_of(eabc_centered[:, k]) for k in range(len(triples))])
        z_abc = eabc_centered - p1_triples - p2_triples  # fixed pure-V3 basis, (v, n_triples)

        def mu_abc_of(g_centered):
            return (z_abc * g_centered[:, None]).sum(axis=0) / v

        mu_abc_f = mu_abc_of(f_centered)
        e3 = float(np.sum(mu_abc_f**2) / lam3)

        def p3_of(g_centered):
            return z_abc @ (mu_abc_of(g_centered) / lam3)

        big_e_quad = np.zeros((v, len(quads)))
        for i, (a, b, c, dd) in enumerate(quads):
            big_e_quad[:, i] = big_e[:, a] * big_e[:, b] * big_e[:, c] * big_e[:, dd]
        eabcd_centered = big_e_quad - big_e_quad.mean(axis=0)
        p1_quads = p1_of(eabcd_centered)
        p2_quads = np.column_stack([p2_of(eabcd_centered[:, k]) for k in range(len(quads))])
        p3_quads = np.column_stack([p3_of(eabcd_centered[:, k]) for k in range(len(quads))])
        w_abcd = eabcd_centered - p1_quads - p2_quads - p3_quads

        mu_abcd = (w_abcd * f_centered[:, None]).sum(axis=0) / v
        e4 = float(np.sum(mu_abcd**2) / lam4) if lam4 != 0 else 0.0

        rows.append(
            {
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "E1": e1,
                "E2": e2,
                "E3": e3,
                "E4": e4,
                "E4_via_subtraction": c_q - e1 - e2 - e3,
            }
        )
        print(
            f"n={n:3d} q={q:2d}/{big_n:2d}  C_q={c_q:.8f}  E1={e1:.8f}  E2={e2:.8f}  E3={e3:.8f}  "
            f"E4={e4:.8f}  E4(subtract)={c_q - e1 - e2 - e3:.8f}",
            flush=True,
        )
    return rows


def cross_check(rows, n, tol_boundary=1e-7, tol_diag=1e-6):
    eig_path = METRICS / "johnson_eigenspace_decomposition.json"
    eig_data = json.load(open(eig_path, encoding="utf-8")) if eig_path.exists() else {}
    out = []
    for row in rows:
        q, big_n = row["q"], row["N"]
        entry = {"n": n, "q": q}
        if min(q, big_n - q) == 4:
            resid = abs(row["E4"] - row["E4_via_subtraction"])
            entry["boundary_residual"] = resid
            entry["boundary_ok"] = resid < tol_boundary
        n_str = str(n)
        if n_str in eig_data:
            layer = next((lyr for lyr in eig_data[n_str] if lyr["q"] == q), None)
            if layer is not None:
                d = q * (big_n - q)
                j = 4
                if q - j >= 0 and big_n - q - j >= 0:
                    lam_theory = ((q - j) * (big_n - q - j) - j) / d
                    for lvl in layer["levels"]:
                        if abs(lvl["lambda"] - lam_theory) < 1e-6:
                            entry["e4_diag"] = lvl["energy"]
                            entry["diag_match"] = abs(lvl["energy"] - row["E4"]) < tol_diag
                            break
        out.append(entry)
    return out


if __name__ == "__main__":
    all_rows = {}
    all_checks = []
    for n in [23, 29, 31]:
        print(f"\n--- n={n} ---")
        rows = interior_e4(n)
        all_rows[n] = rows
        checks = cross_check(rows, n)
        all_checks.extend(checks)
        for c in checks:
            print("  check:", c)

    boundary_violations = [c for c in all_checks if c.get("boundary_ok") is False]
    diag_violations = [c for c in all_checks if c.get("diag_match") is False]
    print(f"\nBoundary violations: {len(boundary_violations)}")
    print(f"Diagonalization violations: {len(diag_violations)}")

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l4_interior_energy.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "rows": all_rows,
                "checks": all_checks,
                "boundary_violations": boundary_violations,
                "diag_violations": diag_violations,
            },
            f,
            indent=2,
        )
