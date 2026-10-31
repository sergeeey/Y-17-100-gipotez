# WHY: independent EXACT rational re-verification over Q (python-flint fmpq_mat) of the S+ certificate,
# WITHOUT re-solving the linear system.  Uses the stored exact checkpoint y (logs/exact_povm_y_checkpoint.pkl)
# for the 175 independent rows I.  Checks, exactly:
#   (1) A (m + delta) = b for ALL 484 rows, delta = A_I^T y; A is rebuilt here from the lift DEFINITION
#       (own code, not exact_cert.py); m = exact dyadic value of the float start;
#   (2) each corrected block M_j* = m_j + delta_j is positive definite (LDL^T pivots > 0, over Q).
# Version 2: matrix products via fmpq_mat (v1 with python-level fmpq loops was too slow).
import json
import os
import pickle
import sys
import time
from fractions import Fraction

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
NI = len(I)
assert NI == 175
print("loaded", round(time.time() - t0, 1), "s", flush=True)


def fq_str(s):
    f = Fraction(str(s))
    return fmpq(f.numerator, f.denominator)


def fq_float(v):
    f = Fraction(float(v))
    return fmpq(f.numerator, f.denominator)


def cm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ca(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cc(a):
    return (a[0], -a[1])


X, B = [], []
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


def block_columns(j):
    """Sparse columns of the 484-row system for block j, from the lift definition; order (a,b), a<=b, a,b in 0..m."""
    m = dims[j]
    n = m + 1
    V = [[(ZERO, ZERO)] * 22 for _ in range(n)]
    for c in range(m):
        for r in range(20):
            V[c][2 + r] = B[j][c][r]
    V[m][0], V[m][1] = X[j][0], X[j][1]
    out = []
    for a in range(n):
        for b in range(a, n):

            def S_(i, k):
                if a == b:
                    return cm(V[a][i], cc(V[a][k]))
                return ca(cm(V[a][i], cc(V[b][k])), cm(V[b][i], cc(V[a][k])))

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
            out.append((a, b, col))
    return out


# ---- assemble global sparse data ----
NCOL = sum((dims[j] + 1) * (dims[j] + 2) // 2 for j in range(J))
assert NCOL == 6566, NCOL
col_meta = []  # (j, a, b)
col_entries = []  # dict row -> fmpq
for j in range(J):
    for a, b, col in block_columns(j):
        col_meta.append((j, a, b))
        col_entries.append(col)
print("columns built", len(col_entries), round(time.time() - t0, 1), "s", flush=True)

pos_in_I = {row: t for t, row in enumerate(I)}

A_full = fmpq_mat(NR, NCOL)
AIT = fmpq_mat(NCOL, NI)
for k, col in enumerate(col_entries):
    for row, val in col.items():
        A_full[row, k] = val
        if row in pos_in_I:
            AIT[k, pos_in_I[row]] = val
print("matrices filled", round(time.time() - t0, 1), "s", flush=True)

yv = fmpq_mat(NI, 1, [fq_str(s) for s in CK["y"]])
delta = AIT * yv
print("delta computed", round(time.time() - t0, 1), "s", flush=True)

mvec = [fq_float(Mf[j][a, b]) for (j, a, b) in col_meta]
Mstar = fmpq_mat(NCOL, 1, [mvec[k] + delta[k, 0] for k in range(NCOL)])
del delta

bvec = [ZERO] * NR
bvec[0] = fmpq(1)
bvec[2] = fmpq(1)
for rho in range(20):
    bvec[84 + upos[(rho, rho)]] = fmpq(1)
bcol = fmpq_mat(NR, 1, bvec)
res = A_full * Mstar - bcol
violated = [r for r in range(NR) if res[r, 0] != 0]
print("rows checked; violated =", len(violated), round(time.time() - t0, 1), "s", flush=True)

# ---- exact positive definiteness of each corrected block (LDL^T, pivots > 0) ----
k0 = 0
pd_ok = True
min_piv_float = None
for j in range(J):
    m = dims[j]
    n = m + 1
    Mx = [[ZERO] * n for _ in range(n)]
    for kk in range(k0, k0 + (n * (n + 1)) // 2):
        _, a, b = col_meta[kk]
        Mx[a][b] = Mstar[kk, 0]
        Mx[b][a] = Mstar[kk, 0]
    k0 += (n * (n + 1)) // 2
    W = [row[:] for row in Mx]
    for p in range(n):
        piv = W[p][p]
        if piv <= 0:
            pd_ok = False
            break
        fv = float(piv)
        min_piv_float = fv if min_piv_float is None or fv < min_piv_float else min_piv_float
        for q in range(p + 1, n):
            f = W[q][p] / piv
            for c in range(p, n):
                W[q][c] = W[q][c] - f * W[p][c]
    if not pd_ok:
        print("block", j, "NOT positive definite", flush=True)
        break
    if (j + 1) % 40 == 0:
        print("PD blocks", j + 1, round(time.time() - t0, 1), "s", flush=True)

out = {
    "method": "exact rational re-verification (flint fmpq_mat); y from checkpoint; A rebuilt from lift definition",
    "independent_rows": NI,
    "blocks": J,
    "columns": NCOL,
    "rows_checked": NR,
    "rows_violated_exactly": len(violated),
    "first_violated_rows": violated[:10],
    "all_blocks_positive_definite_exact": bool(pd_ok),
    "min_pivot_float": min_piv_float,
    "seconds": round(time.time() - t0, 1),
}
json.dump(out, open(os.path.join(STAGE, "logs", "verify_exact_rational_v2.json"), "w"), indent=1)
print(json.dumps(out, indent=1), flush=True)
