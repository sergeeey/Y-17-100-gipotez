# WHY: EXACT real kernel of the 36x40 constraint system for dyadic-rational directions, via python-flint fmpq_mat.
# Constraints for one i (u = G y, G = A_i^dag, c = x^dag G, d = (-x1, x0) G):  Im(c y)=0, Re(d y)=0, Im(d y)=0.
# Real rows on [p, q] (y = p + i q): Re(c y) -> [Re c, -Im c], Im(c y) -> [Im c, Re c].
import json
from fractions import Fraction
import numpy as np
import flint
from ys_space import load_A, S_PLUS

# exact integer data: A = 2*im - 2i*re  ->  G = A^dag has entries 2*im + 2i*re (integers)
DATA = (r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
        r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl")
rec = json.loads(open(DATA, encoding="utf-8").readline())
RE = {i: [[int(rec["blocks"][i][2 * r + a]) for a in range(2)] for r in range(20)] for i in S_PLUS}
IM = {i: [[int(rec["blocks"][i][40 + 2 * r + a]) for a in range(2)] for r in range(20)] for i in S_PLUS}


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def constraint_rows(x):
    """x = ((x0r,x0i),(x1r,x1i)) Fractions. Returns list of 36 rows (40 Fractions each)."""
    x0, x1 = x
    conj = lambda z: (z[0], -z[1])
    dvec = ((-x1[0], -x1[1]), x0)  # d = (-x1, x0)
    rows = []
    for i in S_PLUS:
        # G[a][r] = conj(A[r][a]) = 2*im + 2i*re
        G = [[(Fraction(2 * IM[i][r][a]), Fraction(2 * RE[i][r][a])) for r in range(20)] for a in range(2)]
        c = []
        d = []
        for r in range(20):
            cr = (Fraction(0), Fraction(0)); dr = (Fraction(0), Fraction(0))
            for a in range(2):
                t = cmul(conj((x0, x1)[a]), G[a][r]); cr = (cr[0] + t[0], cr[1] + t[1])
                t2 = cmul(dvec[a], G[a][r]); dr = (dr[0] + t2[0], dr[1] + t2[1])
            c.append(cr); d.append(dr)
        for (zs, which) in ((c, "Im"), (d, "Re"), (d, "Im")):
            if which == "Im" and zs is c:
                row = [z[1] for z in zs] + [z[0] for z in zs]  # Im(c y) = Im c . p + Re c . q  -> [Im c, Re c]
            elif which == "Re":
                row = [z[0] for z in zs] + [-z[1] for z in zs]  # Re(d y) = Re d . p - Im d . q
            else:
                row = [z[1] for z in zs] + [z[0] for z in zs]   # Im(d y) = Im d . p + Re d . q
            rows.append(row)
    return rows


def exact_kernel(x):
    rows = constraint_rows(x)
    M = flint.fmpq_mat(len(rows), 40, [flint.fmpq(q.numerator, q.denominator) for row in rows for q in row])
    R, rank = M.rref()
    piv = []
    r = 0
    for col in range(40):
        if r < rank and R[r, col] != 0:
            piv.append(col); r += 1
    free = [c for c in range(40) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * 40
        v[f] = Fraction(1)
        for ri, pc in enumerate(piv):
            val = R[ri, f]
            v[pc] = -Fraction(int(val.p), int(val.q))
        basis.append(v)
    return rank, basis


if __name__ == "__main__":
    # sanity: a real direction must have kernel dim 6 exactly, a generic one 4
    for x in [((Fraction(3, 5), Fraction(0)), (Fraction(4, 5), Fraction(0))),
              ((Fraction(1, 3), Fraction(1, 7)), (Fraction(2, 5), Fraction(-3, 11)))]:
        rank, b = exact_kernel(x)
        print("rank", rank, "kernel dim", len(b))
