"""Pilot of the twin-exclusion protocol on the commuting prime (P12).

Exact arithmetic over Q (python-flint). For m random points of the linear
subspace L4 = span{S^a (x) S^b} (the commuting component, tangent directions),
computes rank of the Jacobian of the 170 Qbar forms and the dimension of
L4 + gauge tangents. Self-tests on toy ideals are run first.

Inputs are read-only: ../20261004-c3-obstruction-cas/C3_STAGE1_INPUT/.
"""

import json
import random
import sys
from fractions import Fraction
from pathlib import Path

from flint import fmpq, fmpq_mat

PKG = Path(__file__).resolve().parents[1] / "20261004-c3-obstruction-cas" / "C3_STAGE1_INPUT"
SEED, N, M = 20261014, 10**6, 4
EXPECTED_RANK = 33 - 15  # codim of the 15-dim commuting component in the 33-dim kernel


def fq(value) -> fmpq:
    f = Fraction(str(value))
    return fmpq(f.numerator, f.denominator)


def jac_rank(forms, point):
    """forms: list of [(a, b, coeff)], a <= b, 0-based. Literal polynomial sum c*x_a*x_b."""
    n = len(point)
    rows = []
    for form in forms:
        row = [fmpq(0)] * n
        for a, b, c in form:
            if a == b:
                row[a] += 2 * c * point[a]
            else:
                row[a] += c * point[b]
                row[b] += c * point[a]
        rows.append(row)
    return fmpq_mat(len(rows), n, [x for r in rows for x in r]).rank()


def self_test():
    # control A: (x) in Q[x,y] along x=0 -> rank 1 = codim, reduced
    ok_a = jac_rank([[(0, 0, fmpq(0))]], [fmpq(0), fmpq(5)]) == 0  # zero form: rank 0
    # control B (the tangent-tangent twin): x^2 = 0 along x=0 -> rank 0 < codim 1, must be flagged
    flagged = jac_rank([[(0, 0, fmpq(1))]], [fmpq(0), fmpq(5)]) < 1
    # control C: xy along the x-axis (y=0), generic x != 0 -> rank 1 = codim, reduced
    reduced = jac_rank([[(0, 1, fmpq(1))]], [fmpq(7), fmpq(0)]) == 1
    assert ok_a and flagged and reduced, "toy controls failed"
    print("SELF_TEST=PASS (non-reduced toy flagged, reduced toy not flagged)")


def main():
    self_test()
    kb = json.load(open(PKG / "basis_K.json"))
    qb = json.load(open(PKG / "qbar_170.json"))
    forms = [[(a, b, fq(c)) for a, b, c in f] for f in qb["forms"]]
    assert len(kb) == 33 and len(forms) == 170

    def flat(entries):
        v = [fmpq(0)] * 81
        for e in entries:
            v[e["row"] * 9 + e["col"]] = fq(e["value"])
        return v

    K = [flat(v) for v in kb]  # 33 vectors of length 81

    def shift(power):
        s = [[0] * 3 for _ in range(3)]
        for i in range(3):
            s[(i + power) % 3][i] = 1
        return s

    def kron(a, b):
        out = [fmpq(0)] * 81
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        out[(3 * i + k) * 9 + (3 * j + l)] = fmpq(a[i][j] * b[k][l])
        return out

    L4 = [kron(shift(a), shift(b)) for a in range(3) for b in range(3)]

    # express each L4 vector in the K basis: solve sum c_i K_i = target (81 x 33 system)
    aug = fmpq_mat(81, 33 + 9)
    for i, vec in enumerate(K):
        for r in range(81):
            aug[r, i] = vec[r]
    for t, vec in enumerate(L4):
        for r in range(81):
            aug[r, 33 + t] = vec[r]
    rref, rk = aug.rref()
    pivots = [next(c for c in range(42) if rref[r, c] != 0) for r in range(rk)]
    assert rk == 33 and all(p < 33 for p in pivots), "L4 is not inside span(K) or K dependent"
    coords = [[rref[i, 33 + t] for i in range(33)] for t in range(9)]  # K-coordinates of L4 basis

    # gauge tangents [X (x) I + I (x) X, R0], X = E_ij; R0 = kron(S, S^2)
    R0 = kron(shift(1), shift(2))

    def mat(v):
        return [[v[r * 9 + c] for c in range(9)] for r in range(9)]

    def mul(a, b):
        return [
            [sum((a[i][k] * b[k][j] for k in range(9)), fmpq(0)) for j in range(9)]
            for i in range(9)
        ]

    gauge = []
    for i in range(3):
        for j in range(3):
            E = [[0] * 3 for _ in range(3)]
            E[i][j] = 1
            I3 = [[1 if a == b else 0 for b in range(3)] for a in range(3)]
            G = [
                [fmpq(a_ + b_) for a_, b_ in zip(r1, r2)]
                for r1, r2 in zip(
                    [[x for x in row] for row in mat(kron(E, I3))],
                    [[x for x in row] for row in mat(kron(I3, E))],
                )
            ]
            A, B = mul(G, mat(R0)), mul(mat(R0), G)
            gauge.append([A[r][c] - B[r][c] for r in range(9) for c in range(9)])
    span = fmpq_mat(9 + 9, 81, [x for v in L4 + gauge for x in v])
    dim_span = span.rank()
    print(f"dim span(L4 + gauge tangents) = {dim_span}   (expected 15)")

    rng = random.Random(SEED)
    ranks = []
    for _ in range(M):
        c = [fmpq(rng.randrange(N)) for _ in range(9)]
        x = [sum((c[t] * coords[t][i] for t in range(9)), fmpq(0)) for i in range(33)]
        ranks.append(jac_rank(forms, x))
    print(f"seed={SEED} N={N} m={M} ranks of J2 at random points of L4: {ranks}")
    print(
        f"expected for generically reduced: {EXPECTED_RANK}; tangent dim = {[33 - r for r in ranks]}"
    )
    verdict = (
        "CLASS_A_P12"
        if max(ranks) == EXPECTED_RANK and dim_span == 15
        else "NOT_CLASS_A_OR_UNRESOLVED"
    )
    print("VERDICT=" + verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
