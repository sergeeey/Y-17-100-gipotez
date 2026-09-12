"""Exam 3, stage 5: extend the general recursive E_l construction (point 25, l=4) one more level
to l=5, following the exact same pattern -- reuse each level's "pure V_k basis" (built once,
independent of correlation target) as a generic operator P_k[g] for the next level up.

New at this stage: the pure-V4 basis `w_abcd` (already built while computing E_4 in point 25) is
extracted here as a reusable operator P_4[g] the same way z_abc (pure-V3) became P_3[g] in point
25 -- no new derivation needed, just one more level of the same pattern:

    mu_abcd(g) := Cov(g, w_abcd)
    P_4[g](S)  := sum_{quadruples} (mu_abcd(g)/lambda_4) * w_abcd(S)

For l=5: E_abcde(S) = e_a*e_b*e_c*e_d*e_e (raw quintuple indicator, degree-5, content only in
V_0..V_5). v_abcde := E_abcde_centered - P_1[E_abcde] - P_2[E_abcde] - P_3[E_abcde] -
P_4[E_abcde] is its pure V_5 part. mu_abcde := Cov(f, v_abcde). lambda_5 hypothesized by
extending the verified falling-factorial pattern (lambda_l=[q]_l[N-q]_l/[N]_{2l}, confirmed
l=1,2,3,4) to l=5. E_5 := sum(mu_abcde^2)/lambda_5.

Verification: same two-pronged discipline as l=3,4 -- (1) q=5,N-5 boundary zero-residual test
(min(q,N-q)=5 means l=1..5 are the ONLY levels, so E_5=C_q-E1-E2-E3-E4 exactly); (2) cross-check
against exact diagonalization (metrics/johnson_eigenspace_decomposition.json, l=5 eigenspace)
at interior layers for n=29,31 (n=23 has N=10, where q=5 is itself the only layer with
min(q,N-q)>=5, so it only exercises the boundary case, not an interior cross-check).

Computational note: needs the full (v, C(N,5)) raw-quintuple matrix plus (v,C(N,4)),(v,C(N,3)),
(v,C(N,2)) intermediates -- same small-N-only scope as l=3,4 (n=23,29,31).
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
    "necklace_mod_l5interior", HERE / "check_necklace_orbit_reduction.py"
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


def interior_e5(n: int, max_layer_size: int = 4000) -> list[dict]:
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
    quints = list(combinations(range(big_n), 5))

    rows = []
    for q in range(5, big_n - 4):
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
        lam5 = lambda_l(q, big_n, 5)

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
        z_abc = eabc_centered - p1_triples - p2_triples  # fixed pure-V3 basis

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
        w_abcd = eabcd_centered - p1_quads - p2_quads - p3_quads  # fixed pure-V4 basis

        def mu_abcd_of(g_centered):
            return (w_abcd * g_centered[:, None]).sum(axis=0) / v

        mu_abcd_f = mu_abcd_of(f_centered)
        assert lam4 > 0, f"lam4 must be positive: q={q}, N={big_n}"
        e4 = float(np.sum(mu_abcd_f**2) / lam4)

        def p4_of(g_centered):
            return w_abcd @ (mu_abcd_of(g_centered) / lam4)

        big_e_quint = np.zeros((v, len(quints)))
        for i, (a, b, c, dd, ee) in enumerate(quints):
            big_e_quint[:, i] = (
                big_e[:, a] * big_e[:, b] * big_e[:, c] * big_e[:, dd] * big_e[:, ee]
            )
        eabcde_centered = big_e_quint - big_e_quint.mean(axis=0)
        p1_quints = p1_of(eabcde_centered)
        p2_quints = np.column_stack([p2_of(eabcde_centered[:, k]) for k in range(len(quints))])
        p3_quints = np.column_stack([p3_of(eabcde_centered[:, k]) for k in range(len(quints))])
        p4_quints = np.column_stack([p4_of(eabcde_centered[:, k]) for k in range(len(quints))])
        v_abcde = eabcde_centered - p1_quints - p2_quints - p3_quints - p4_quints

        mu_abcde = (v_abcde * f_centered[:, None]).sum(axis=0) / v
        assert lam5 > 0, f"lam5 must be positive: q={q}, N={big_n}"
        e5 = float(np.sum(mu_abcde**2) / lam5)

        rows.append(
            {
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "E1": e1,
                "E2": e2,
                "E3": e3,
                "E4": e4,
                "E5": e5,
                "E5_via_subtraction": c_q - e1 - e2 - e3 - e4,
            }
        )
        print(
            f"n={n:3d} q={q:2d}/{big_n:2d}  C_q={c_q:.8f}  E1={e1:.8f}  E2={e2:.8f}  E3={e3:.8f}  "
            f"E4={e4:.8f}  E5={e5:.8f}  E5(subtract)={c_q - e1 - e2 - e3 - e4:.8f}",
            flush=True,
        )
    return rows


def cross_check(rows, n, tol_boundary=1e-6, tol_diag=1e-6):
    eig_path = METRICS / "johnson_eigenspace_decomposition.json"
    eig_data = json.load(open(eig_path, encoding="utf-8")) if eig_path.exists() else {}
    out = []
    for row in rows:
        q, big_n = row["q"], row["N"]
        entry = {"n": n, "q": q}
        if min(q, big_n - q) == 5:
            resid = abs(row["E5"] - row["E5_via_subtraction"])
            entry["boundary_residual"] = resid
            entry["boundary_ok"] = resid < tol_boundary
        n_str = str(n)
        if n_str in eig_data:
            layer = next((lyr for lyr in eig_data[n_str] if lyr["q"] == q), None)
            if layer is not None:
                d = q * (big_n - q)
                j = 5
                if q - j >= 0 and big_n - q - j >= 0:
                    lam_theory = ((q - j) * (big_n - q - j) - j) / d
                    closest = min(layer["levels"], key=lambda lvl: abs(lvl["lambda"] - lam_theory))
                    if abs(closest["lambda"] - lam_theory) < 1e-6:
                        entry["e5_diag"] = closest["energy"]
                        entry["diag_match"] = abs(closest["energy"] - row["E5"]) < tol_diag
        out.append(entry)
    return out


if __name__ == "__main__":
    all_rows = {}
    all_checks = []
    for n in [23, 29, 31]:
        print(f"\n--- n={n} ---")
        rows = interior_e5(n)
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
    with open(METRICS / "l5_interior_energy.json", "w", encoding="utf-8") as f:
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
