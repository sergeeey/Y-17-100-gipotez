# WHY: independent EXACT rational re-verification (over Q, python-flint fmpq) of the S+ certificate, WITHOUT
# re-solving the linear system.  Given the stored exact checkpoint y (logs/exact_povm_y_checkpoint.pkl) for the
# 175 independent rows I, it checks, exactly over Q:
#   (1) A (m + delta) = b for ALL 484 rows, delta = A_I^T y, with A rebuilt here from the lift DEFINITION;
#   (2) every corrected block M_j* = m_j + delta_j is positive definite (LDL^T pivots > 0, over Q).
# It does NOT check positivity of the float start m, and does NOT re-derive y (y is taken as given; its
# validity is exactly what check (1) tests).  Output: logs/verify_exact_rational_v1.json (small, hashable).
import json
import os
import pickle
import sys
import time
from fractions import Fraction

import flint
from flint import fmpq, fmpq_mat

sys.set_int_max_str_digits(0)
t0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)

D = pickle.load(open(os.path.join(STAGE, "logs", "exact_bases2.pkl"), "rb"))
S = pickle.load(open(os.path.join(STAGE, "logs", "exact_sdp2_M.pkl"), "rb"))
CK = pickle.load(open(os.path.join(STAGE, "logs", "exact_povm_y_checkpoint.pkl"), "rb"))
dirs, bases = D["dirs"], D["bases_exact"]
Mf = S["M"]
J = len(dirs)
dims = [len(bases[j]) for j in range(J)]
I = [int(v) for v in CK["I"]]
assert len(I) == 175
print("loaded", round(time.time() - t0, 1), "s", flush=True)


def fq_str(s):
    f = Fraction(str(s))
    return fmpq(f.numerator, f.denominator)


def fq_float(v):
    f = Fraction(float(v))  # exact binary value of the float
    return fmpq(f.numerator, f.denominator)


def cm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ca(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cc(a):
    return (a[0], -a[1])


X = []
B = []
for j in range(J):
    (a0r, a0i), (a1r, a1i) = dirs[j]
    X.append([(fq_str(a0r), fq_str(a0i)), (fq_str(a1r), fq_str(a1i))])
    B.append(
        [
            [(fq_str(bases[j][v][r][0]), fq_str(bases[j][v][r][1])) for r in range(20)]
            for v in range(dims[j])
        ]
    )

UP = [(r, s) for r in range(20) for s in range(r, 20)]
SU = [(r, s) for r in range(20) for s in range(r + 1, 20)]
upos = {p: k for k, p in enumerate(UP)}
NR = 484
ZERO = fmpq(0)


# ----- exact sparse columns of A, block by block, from the lift definition -----
def block_columns(j):
    m = dims[j]
    n = m + 1
    V = [[(ZERO, ZERO)] * 22 for _ in range(n)]
    for c in range(m):
        for r in range(20):
            V[c][2 + r] = B[j][c][r]
    V[m][0], V[m][1] = X[j][0], X[j][1]
    cols = []
    for a in range(n):
        for b in range(a, n):

            def S_(i, k):
                if a == b:
                    return cm(V[a][i], cc(V[a][k]))
                t1 = cm(V[a][i], cc(V[b][k]))
                t2 = cm(V[b][i], cc(V[a][k]))
                return ca(t1, t2)

            col = {}

            def put(row, val):
                if val != 0:
                    col[row] = val

            e = S_(0, 0)
            put(0, e[0])
            e = S_(0, 1)
            put(1, e[0])
            put(3, e[1])
            e = S_(1, 1)
            put(2, e[0])
            for al in range(2):
                for rho in range(20):
                    e = S_(al, 2 + rho)
                    put(4 + al * 20 + rho, e[0])
                    put(44 + al * 20 + rho, e[1])
            for k, (r, s) in enumerate(UP):
                put(84 + k, S_(2 + r, 2 + s)[0])
            for k, (r, s) in enumerate(SU):
                put(294 + k, S_(2 + r, 2 + s)[1])
            cols.append((a, b, col))
    return cols


# y as exact rationals (one per independent row)
yv = [fq_str(s) for s in CK["y"]]
pos_in_I = {row: t for t, row in enumerate(I)}

resid = [ZERO] * NR  # running sum of A[r,k] * Mstar_k over all columns
pd_ok = True
min_piv = None
blocks_done = 0
col_index = 0
for j in range(J):
    m = dims[j]
    n = m + 1
    cols = block_columns(j)
    mstar = {}  # (a,b) -> exact M*_j[a,b]
    # delta for this block's columns: delta_k = sum_{row in I} A[row,k] * y_row
    for a, b, col in cols:
        delta = ZERO
        for row, val in col.items():
            if row in pos_in_I:
                delta += val * yv[pos_in_I[row]]
        mv = fq_float(Mf[j][a, b])
        mstar[(a, b)] = mv + delta
        # residual contribution (all rows of this column), exact
        for row, val in col.items():
            resid[row] += val * mstar[(a, b)]
        col_index += 1
    # block PD check: LDL^T over Q on the symmetric (n x n) M*_j
    Mx = [[mstar[(min(a, b), max(a, b))] for b in range(n)] for a in range(n)]
    W = [row[:] for row in Mx]
    for p in range(n):
        piv = W[p][p]
        if piv <= 0:
            pd_ok = False
            break
        fv = float(piv)
        min_piv = fv if min_piv is None or fv < min_piv else min_piv
        for q in range(p + 1, n):
            f = W[q][p] / piv
            for c in range(p, n):
                W[q][c] = W[q][c] - f * W[p][c]
    blocks_done += 1
    if blocks_done % 40 == 0:
        print("block", blocks_done, "done", round(time.time() - t0, 1), "s", flush=True)
    if not pd_ok:
        break

# right-hand side b (exact)
bvec = [ZERO] * NR
bvec[0] = fmpq(1)
bvec[2] = fmpq(1)
for rho in range(20):
    bvec[84 + upos[(rho, rho)]] = fmpq(1)
violated = [r for r in range(NR) if resid[r] != bvec[r]]

out = {
    "method": "exact rational re-verification (fmpq); y taken from checkpoint; A rebuilt from lift definition",
    "independent_rows": len(I),
    "blocks": J,
    "columns_processed": col_index,
    "rows_violated_exactly": len(violated),
    "first_violated_rows": violated[:10],
    "all_blocks_positive_definite_exact": pd_ok and blocks_done == J,
    "min_pivot_float": min_piv,
    "seconds": round(time.time() - t0, 1),
}
json.dump(out, open(os.path.join(STAGE, "logs", "verify_exact_rational_v1.json"), "w"), indent=1)
print(json.dumps(out, indent=1), flush=True)
