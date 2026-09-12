"""Exam 2, stage C (interior layers): general E_3(q) at ANY layer, not just the q=3,N-3
boundary that check_l3_boundary_energy.py already solved for free.

Key idea, avoiding a from-scratch symbolic triple-centering derivation: verify_l2_projection_
rigorous.py already gives VERIFIED projection operators P_1[g], P_2[g] for an ARBITRARY target
function g (not just f) -- built once, reused here with g = E_abc(S) = e_a(S)e_b(S)e_c(S) (the
raw triple indicator) instead of g = f. Since E_abc is degree-3 in the 0/1 indicators, it lives
entirely in V_0 (+) V_1 (+) V_2 (+) V_3 -- no higher component exists. So

    z_abc(S) := E_abc(S) - P_1[E_abc](S) - P_2[E_abc](S)

is EXACTLY E_abc's pure-V_3 part (nothing left to remove above V_3). This sidesteps re-deriving
an inclusion-exclusion "triple-centering" formula symbolically (real risk of a sign/index error
in a 3-index generalization of the already-nontrivial r_ab formula) -- it reuses code already
verified to 0/94 violations.

Then mu_abc := Cov(f, z_abc) = Cov(h, z_abc)  (h=f_centered-P_1(f)-P_2(f), since z_abc _|_ V_0,
V_1,V_2 already) is the natural triple analogue of mu_ab. The remaining question is whether
E_3 = sum(mu_abc^2) / lambda_3 holds WITHOUT a further "r_abc"-style correction for the C(N,3)
triples' redundancy within dim(V_3) -- exactly the argument that already made E_2=sum(r_ab^2)/
lambda_2 work despite C(N,2) redundant y_ab's: IF the Gram/covariance structure of {z_abc} is a
SCALAR multiple of identity on its own achievable row space, then mu (being an actual Cov(f,.)
vector) automatically lies in that row space and ||mu||^2/lambda_3 = the true energy, no
pseudo-inverse needed. lambda_3 is HYPOTHESIZED (not assumed) by pattern-matching the already-
verified lambda_1, lambda_2 closed forms:

    lambda_l = [q]_l * [N-q]_l / [N]_{2l}   ([x]_l = falling factorial x(x-1)...(x-l+1))
    lambda_1 = q(N-q) / (N(N-1))                        <- matches e1_closed_form's scalar
    lambda_2 = q(q-1)(N-q)(N-q-1) / (N(N-1)(N-2)(N-3))  <- matches check_l2_analytic_projection
    lambda_3 = q(q-1)(q-2)(N-q)(N-q-1)(N-q-2)
               / (N(N-1)(N-2)(N-3)(N-4)(N-5))            <- HYPOTHESIS, verified below

Verification, in order of increasing trust requirement:
  1. At q=3,N-3 (where check_l3_boundary_energy.py already has an independently-verified exact
     E_3 via Var(h)): does sum(mu_abc^2)/lambda_3 match?
  2. At INTERIOR q for n=23,29,31 (where metrics/johnson_eigenspace_decomposition.json has exact
     diagonalization): does sum(mu_abc^2)/lambda_3 match the l=3 eigenspace energy?

Computational note: for a layer of size v=C(N,q), building the (v, C(N,3)) raw E_abc matrix
directly is only feasible for small-to-moderate N (matches check_johnson_eigenspace_decomposition.
py's own "small N only" scoping) -- this script targets n=23,29,31 (N<=14) where C(N,3)<=364,
matching the boundary of what's already tractable elsewhere in this experiment.
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
    "necklace_mod_l3interior", HERE / "check_necklace_orbit_reduction.py"
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


def interior_e3(n: int, max_triples_layer_size: int = 4000) -> list[dict]:
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
    rows = []
    for q in range(3, big_n - 2):
        subsets = list(combinations(ground, q))
        v = len(subsets)
        if v > max_triples_layer_size:
            print(f"  q={q}: skipped, layer size {v} too large for direct triple matrix")
            continue
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
        h = f_centered - p1_f - p2_f
        e1 = float(np.mean(p1_f**2))
        e2 = float(np.sum(r_f**2) / lam2)

        # build raw triple indicator matrix, then project each triple's E_abc onto V_{>=3}
        # via the SAME verified P1/P2 operators (applied to the triple's own column as target)
        big_e_triple = np.zeros((v, len(triples)))
        for i, (a, b, c) in enumerate(triples):
            big_e_triple[:, i] = big_e[:, a] * big_e[:, b] * big_e[:, c]

        # P1 applied to each triple column: coefficients = (mu_e for that column) * scale
        mu_e_triples = (
            big_e.T @ (big_e_triple - big_e_triple.mean(axis=0)) / v
        )  # (big_n, n_triples)
        c1_triples = mu_e_triples * big_n * (big_n - 1) / (q * (big_n - q))
        p1_triples = x_centered @ c1_triples  # (v, n_triples)

        eabc_centered = big_e_triple - big_e_triple.mean(axis=0)
        # Cov(E_ab, E_{triple k}) -- must correlate the PAIR indicator (both a AND b), not just
        # e_a alone (an earlier version of this line used a single-index e_a, undercounting the
        # V_1/V_2 content to remove and leaving the resulting z_abc nowhere near pure V_3 --
        # caught via the Gram-matrix diagnostic below, not assumed correct from the derivation).
        mu_pairs_triples = (big_e_pair.T @ eabc_centered) / v  # (n_pairs, n_triples)
        s_row_t = np.zeros((big_n, len(triples)))
        for idx, (a, b) in enumerate(pairs):
            s_row_t[a] += mu_pairs_triples[idx]
            s_row_t[b] += mu_pairs_triples[idx]
        big_s_t = mu_pairs_triples.sum(axis=0)
        r_triples = np.array(
            [
                mu_pairs_triples[idx]
                - (s_row_t[a] + s_row_t[b]) / (big_n - 2)
                + 2 * big_s_t / ((big_n - 1) * (big_n - 2))
                for idx, (a, b) in enumerate(pairs)
            ]
        )
        d_coef_triples = r_triples / lam2
        p2_triples = y_ab @ d_coef_triples  # (v, n_triples)

        # eabc_centered - p1_triples - p2_triples is E_abc's pure-V3 part (mean-zero): using
        # the already-centered eabc_centered here (not raw big_e_triple) keeps z_abc genuinely
        # V0-free, not just "V0 offset happens not to matter because f_centered sums to zero"
        # (reviewer-flagged 2026-09-12: the raw-big_e_triple version was numerically harmless
        # for mu_abc but would silently break any future reuse of z_abc that assumes mean-zero).
        z_abc = eabc_centered - p1_triples - p2_triples

        mu_abc = (z_abc * f_centered[:, None]).sum(axis=0) / v  # Cov(f, z_abc) per triple

        lam3 = lambda_l(q, big_n, 3)
        e3_formula = float(np.sum(mu_abc**2) / lam3) if lam3 != 0 else 0.0

        var_h = float(np.mean(h**2))
        rows.append(
            {
                "n": n,
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "E1": e1,
                "E2": e2,
                "E3_formula": e3_formula,
                "Var_h_minus_E3": var_h - e3_formula,  # should be >=0 (tail beyond l=3)
            }
        )
        print(
            f"n={n:3d} q={q:2d}/{big_n:2d}  C_q={c_q:.8f}  E1={e1:.8f}  E2={e2:.8f}  "
            f"E3_formula={e3_formula:.8f}  Var(h)-E3={var_h - e3_formula:.3e}",
            flush=True,
        )
    return rows


def cross_check(rows: list[dict], tol: float = 1e-6) -> list[dict]:
    """Compare E3_formula against the l=3 eigenspace energy from exact diagonalization, where
    available (metrics/johnson_eigenspace_decomposition.json)."""
    eig_data = json.load(open(METRICS / "johnson_eigenspace_decomposition.json", encoding="utf-8"))
    boundary_data = json.load(open(METRICS / "l3_boundary_energy.json", encoding="utf-8"))
    boundary_by_nq = {(r["n"], r["q"]): r["E3_via_var_h"] for r in boundary_data["e3_boundary"]}
    out = []
    for row in rows:
        n, q, big_n = row["n"], row["q"], row["N"]
        e3_diag = None
        n_str = str(n)
        if n_str in eig_data:
            layer = next((lyr for lyr in eig_data[n_str] if lyr["q"] == q), None)
            if layer is not None:
                d = q * (big_n - q)
                j = 3
                if q - j >= 0 and big_n - q - j >= 0:
                    lam_theory = ((q - j) * (big_n - q - j) - j) / d
                    for lvl in layer["levels"]:
                        if abs(lvl["lambda"] - lam_theory) < 1e-6:
                            e3_diag = lvl["energy"]
                            break
        e3_boundary = boundary_by_nq.get((n, q))
        match_diag = abs(e3_diag - row["E3_formula"]) < tol if e3_diag is not None else None
        match_boundary = (
            abs(e3_boundary - row["E3_formula"]) < tol if e3_boundary is not None else None
        )
        out.append(
            {
                "n": n,
                "q": q,
                "e3_formula": row["E3_formula"],
                "e3_diag": e3_diag,
                "match_diag": match_diag,
                "e3_boundary": e3_boundary,
                "match_boundary": match_boundary,
            }
        )
        print(
            f"  n={n:3d} q={q:2d}  formula={row['E3_formula']:.8f}  diag={e3_diag}  "
            f"match_diag={match_diag}  boundary={e3_boundary}  match_boundary={match_boundary}"
        )
    return out


if __name__ == "__main__":
    all_rows = []
    for n in [23, 29, 31]:
        print(f"\n--- n={n} ---")
        all_rows.extend(interior_e3(n))

    print("\n=== Cross-check against diagonalization / boundary ===")
    checks = cross_check(all_rows)

    violations = [c for c in checks if c["match_diag"] is False or c["match_boundary"] is False]
    print(f"\nTotal layers: {len(checks)}  violations: {len(violations)}")

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "l3_interior_energy.json", "w", encoding="utf-8") as f:
        json.dump({"rows": all_rows, "cross_check": checks, "violations": violations}, f, indent=2)
