# WHY: exact rational re-verification of the S+ certificate by CLEARING DENOMINATORS, i.e. integer arithmetic
# (flint fmpz_mat).  v2 (fmpq_mat residual) did not finish in 27 min: every addition of huge fractions triggers a gcd.
# Here all data are scaled to integers, so no gcd is needed in the big products.
#
# Checks, exactly over Z (hence over Q):
#   (1) A_full * M = b for all 484 rows, where M = m + A_I^T y, A rebuilt here from the lift DEFINITION;
#   (2) every corrected block M_j is positive definite: all leading principal minors > 0 (Sylvester), computed
#       on the integer matrix W-block (a positive rescaling does not change the signs of minors).
#
# Scaling:  A_full = Aint / DA,  y = Yint / Dn,  m = mint / Dm  (all integers).
#           W := DA*Dn*mint + Dm*(Aint_I^T Yint)  satisfies  M = W / (DA*Dn*Dm).
#           Hence  A_full M = b  <=>  Aint * W = DA^2 * Dn * Dm * b   (integers).
import json
import os
import pickle
import sys
import time
from fractions import Fraction

from flint import fmpq, fmpz, fmpz_mat

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


col_meta, col_entries = [], []
for j in range(J):
    for a, b, col in block_columns(j):
        col_meta.append((j, a, b))
        col_entries.append(col)
NCOL = len(col_entries)
assert NCOL == 6566
print("columns", NCOL, round(time.time() - t0, 1), "s", flush=True)

# ---- common denominators ----
DA = fmpz(1)
for col in col_entries:
    for val in col.values():
        DA = DA.lcm(val.q)
print("DA digits", len(str(DA)), round(time.time() - t0, 1), "s", flush=True)

yq = [fq_str(s) for s in CK["y"]]
Dn = fmpz(1)
for v in yq:
    Dn = Dn.lcm(v.q)
Yint = [int(v * Dn) for v in yq]  # exact integers
print("Dn digits", len(str(Dn)), round(time.time() - t0, 1), "s", flush=True)

mq = [fq_float(Mf[j][a, b]) for (j, a, b) in col_meta]
Dm = fmpz(1)
for v in mq:
    Dm = Dm.lcm(v.q)
mint = [int(v * Dm) for v in mq]
print("Dm bits", Dm.bit_length(), round(time.time() - t0, 1), "s", flush=True)

# ---- integer matrices ----
pos_in_I = {row: t for t, row in enumerate(I)}
Aint = fmpz_mat(NR, NCOL)
AIT = fmpz_mat(NCOL, NI)
for k, col in enumerate(col_entries):
    for row, val in col.items():
        iv = int(val * DA)  # exact integer (DA is a common multiple of all denominators)
        Aint[row, k] = iv
        if row in pos_in_I:
            AIT[k, pos_in_I[row]] = iv
print("integer A filled", round(time.time() - t0, 1), "s", flush=True)

Yvec = fmpz_mat(NI, 1, Yint)
T = AIT * Yvec  # 6566 x 1 integers: Aint_I^T * Yint
print("T computed", round(time.time() - t0, 1), "s", flush=True)
mvec = fmpz_mat(NCOL, 1, mint)
Wvec = (DA * Dn) * mvec + Dm * T  # integers, M = W / (DA*Dn*Dm)
print("W computed", round(time.time() - t0, 1), "s", flush=True)

# ---- residual check: Aint * W == DA^2 * Dn * Dm * b ----
bvec = [0] * NR
bvec[0] = 1
bvec[2] = 1
for rho in range(20):
    bvec[84 + upos[(rho, rho)]] = 1
scale_b = DA * DA * Dn * Dm
lhs = Aint * Wvec
violated = [r for r in range(NR) if lhs[r, 0] != scale_b * bvec[r]]
print("rows checked; violated =", len(violated), round(time.time() - t0, 1), "s", flush=True)

# ---- positive definiteness: leading principal minors of each block (Sylvester) ----
k0 = 0
pd_ok = True
blocks_checked = 0
for j in range(J):
    m = dims[j]
    n = m + 1
    cnt = n * (n + 1) // 2
    Mx = [[0] * n for _ in range(n)]
    for kk in range(k0, k0 + cnt):
        _, a, b = col_meta[kk]
        Mx[a][b] = int(Wvec[kk, 0])
        Mx[b][a] = int(Wvec[kk, 0])
    k0 += cnt
    # leading principal minors (exact integer determinants)
    for p in range(1, n + 1):
        sub = fmpz_mat(p, p, [Mx[a][b] for a in range(p) for b in range(p)])
        if sub.det() <= 0:
            pd_ok = False
            break
    blocks_checked += 1
    if not pd_ok:
        print("block", j, "NOT positive definite", flush=True)
        break
    if (j + 1) % 40 == 0:
        print("PD blocks", j + 1, round(time.time() - t0, 1), "s", flush=True)

out = {
    "method": "exact integer re-verification (common denominators; flint fmpz_mat); y from checkpoint; A rebuilt from lift definition",
    "independent_rows": NI,
    "blocks": J,
    "columns": NCOL,
    "rows_checked": NR,
    "rows_violated_exactly": len(violated),
    "first_violated_rows": violated[:10],
    "blocks_checked_PD": blocks_checked,
    "all_blocks_positive_definite_exact": bool(pd_ok and blocks_checked == J),
    "seconds": round(time.time() - t0, 1),
}
json.dump(out, open(os.path.join(STAGE, "logs", "verify_exact_integer_v3.json"), "w"), indent=1)
print(json.dumps(out, indent=1), flush=True)
