"""Exam 3, stage 9 (point 29): independent numeric check (exact Fraction arithmetic, no
floating point) of a classical fact cited by the user -- the inclusion-product matrix
M^(k) with M^(k)_{S,T} = C(|S cap T|, k) has eigenvalue C(N-2k, q-k) on the level-k Johnson
eigenspace V_k (the eigenvalue of A^(i) on V_j at i=j=k, from inclusion-matrix spectral
theory tracing to Wilson's inclusion-matrix rank/diagonalization results). Per this project's
audit-verification-gate.md ("agent's [VERIFIED] = my [INFERRED]"), a cited external formula is
verified here directly rather than accepted on the strength of the citation alone.

Method: for k=1,2,3, build a Z_A-type vector using code already reviewed/verified in this
project (x_j for k=1, y_ab for k=2, z_abc for k=3 -- points 25-28), apply M^(k) directly by
brute-force summation over all q-subsets T, and check M^(k) @ Z_A == C(N-2k,q-k) * Z_A exactly
(as Fractions) -- exact vector equality, not just an eigenvalue-ratio spot check.

Why this matters: binomial(N-2k,q-k)/binomial(N,q) is algebraically identical to
(q)_k(N-q)_k/(N)_{2k}, the falling-factorial lambda_k this project independently derived via a
completely different recursive self-adjoint-projection method (derive_lambda_k_from_first_
principles.py, points 27-28). Combined with the algebraic identity (verified by hand, pure
factorial cancellation) and Filmus (2016, EJC 23(1) P1.23, Theorem 4.1 -- verified against the
paper's own LaTeX source, not an AI summary), this confirms lambda_k's closed form is a
CLASSICAL result (Johnson-scheme / inclusion-matrix spectral theory), not new mathematics --
see decision.md point 29 for the full reclassification.
"""

from fractions import Fraction as Fr
from itertools import combinations


def comb(n, r):
    if r < 0 or r > n:
        return 0
    num = 1
    for i in range(r):
        num *= n - i
    den = 1
    for i in range(1, r + 1):
        den *= i
    return num // den


def build_and_check(N, q, k):
    ground = list(range(N))
    subsets = list(combinations(ground, q))
    v = len(subsets)

    def e(j, s):
        return Fr(1) if j in s else Fr(0)

    big_e = [[e(j, s) for j in ground] for s in subsets]

    def prod_cols(idxs):
        return [Fr(1) if all(idx in subsets[i] for idx in idxs) else Fr(0) for i in range(v)]

    def dot(colf, colg):
        return sum(colf[i] * colg[i] for i in range(v)) / v

    # M^(k)_{S,T} = C(|S cap T|, k); apply directly to a vector via brute-force sum over T
    def apply_M_k(vec):
        out = [Fr(0)] * v
        for i, S in enumerate(subsets):
            acc = Fr(0)
            for j, T in enumerate(subsets):
                overlap = len(set(S) & set(T))
                acc += comb(overlap, k) * vec[j]
            out[i] = acc
        return out

    # build Z_A for the given k, reusing already-reviewed constructions
    if k == 1:
        a = 0
        Z = [big_e[i][a] - Fr(q, N) for i in range(v)]
    elif k == 2:
        a, b = 0, 1
        eab = prod_cols((a, b))
        Z = [
            eab[i]
            - Fr(q - 1, N - 2) * (big_e[i][a] + big_e[i][b])
            + Fr(q * (q - 1), (N - 1) * (N - 2))
            for i in range(v)
        ]
    elif k == 3:
        a, b, c = 0, 1, 2

        def mean_center(vec):
            m = sum(vec) / v
            return [x - m for x in vec]

        def p1_of(g_centered):
            mu = [dot([big_e[i][j] for i in range(v)], g_centered) for j in ground]
            scale = Fr(N * (N - 1), q * (N - q))
            c_ = [mu[j] * scale for j in ground]
            out = [Fr(0)] * v
            for i in range(v):
                out[i] = sum(c_[j] * (big_e[i][j] - Fr(q, N)) for j in ground)
            return out

        pairs = list(combinations(ground, 2))
        y_ab = {}
        for x, y in pairs:
            exy = prod_cols((x, y))
            y_ab[(x, y)] = [
                exy[i]
                - Fr(q - 1, N - 2) * (big_e[i][x] + big_e[i][y])
                + Fr(q * (q - 1), (N - 1) * (N - 2))
                for i in range(v)
            ]
        lam2 = Fr(q * (q - 1) * (N - q) * (N - q - 1), N * (N - 1) * (N - 2) * (N - 3))

        def r_pairs_of(g_centered):
            m_full = {}
            for x, y in pairs:
                m_full[(x, y)] = dot(prod_cols((x, y)), g_centered)
            s_row = [Fr(0)] * N
            for (x, y), mu in m_full.items():
                s_row[x] += mu
                s_row[y] += mu
            big_s = sum(m_full.values())
            r = {}
            for x, y in pairs:
                r[(x, y)] = (
                    m_full[(x, y)]
                    - (s_row[x] + s_row[y]) / (N - 2)
                    + 2 * big_s / ((N - 1) * (N - 2))
                )
            return r

        def p2_of(g_centered):
            r = r_pairs_of(g_centered)
            out = [Fr(0)] * v
            for (x, y), rv in r.items():
                d = rv / lam2
                yab = y_ab[(x, y)]
                for i in range(v):
                    out[i] += d * yab[i]
            return out

        eabc = prod_cols((a, b, c))
        eabc_c = mean_center(eabc)
        p1v = p1_of(eabc_c)
        p2v = p2_of(eabc_c)
        Z = [eabc_c[i] - p1v[i] - p2v[i] for i in range(v)]
    else:
        raise ValueError("only k=1,2,3 wired for this quick check")

    claimed_eigenvalue = comb(N - 2 * k, q - k)
    MZ = apply_M_k(Z)

    # check MZ == claimed_eigenvalue * Z exactly
    ratios = set()
    for i in range(v):
        if Z[i] != 0:
            ratios.add(MZ[i] / Z[i])
    # direct vector equality check (covers Z[i]==0 entries too, not just the nonzero ratios)
    exact_match = all(MZ[i] == claimed_eigenvalue * Z[i] for i in range(v))

    print(
        f"N={N} q={q} k={k}: claimed eigenvalue C(N-2k,q-k)="
        f"C({N - 2 * k},{q - k})={claimed_eigenvalue}"
    )
    print(f"  distinct MZ[i]/Z[i] ratios (nonzero Z only): {ratios}")
    print(f"  exact vector match M@Z == eigenvalue*Z: {exact_match}")
    return exact_match


if __name__ == "__main__":
    cases = [(8, 4, 1), (8, 4, 2), (8, 4, 3), (9, 5, 1), (9, 5, 2), (9, 5, 3), (10, 4, 2)]
    results = [build_and_check(N, q, k) for N, q, k in cases]
    all_pass = all(results)
    print()
    print("ALL PASS:", all_pass)

    import json
    from pathlib import Path

    metrics_dir = Path(__file__).resolve().parent / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    with open(metrics_dir / "inclusion_matrix_eigenvalue_check.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "cases": [{"N": N, "q": q, "k": k} for N, q, k in cases],
                "results": results,
                "all_pass": all_pass,
            },
            f,
            indent=2,
        )
