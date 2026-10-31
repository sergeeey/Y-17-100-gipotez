# WHY: compact, independent re-verification of the S+ moment certificate, WITHOUT materialising the
# multi-GB rational M*.  Two checks, both on the existing exact checkpoint y (logs/exact_povm_y_checkpoint.pkl):
#  (1) EXACT-MOD-P: the 484 equalities  A (m + delta) = b  hold modulo several 61-bit primes, with
#      A rebuilt here from the lift DEFINITION (not from exact_cert.py), delta = A_I^T y.
#      Zero residual mod p for every prime is strong evidence; the exact rational check is the earlier
#      exact_cert.py run (logs/exact_cert_result.json).  Mod-p is a fingerprint, not a proof on its own.
#  (2) HIGH-PRECISION POSITIVITY: M_j* = m_j + delta_j evaluated with Decimal (prec 200); LDL pivots per
#      block.  Rounding error is bounded by ~ 10^-180 * max|y| * max|A| * 175, far below the pivot margin.
# Output: logs/verify_cert_compact.json (compact, hashable).
import json
import os
import pickle
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
getcontext().prec = 200
# y entries have ~190k-digit numerators/denominators; lift the int<->str limit (only parse, no printing)
sys.set_int_max_str_digits(0)

D = pickle.load(open(os.path.join(STAGE, "logs", "exact_bases2.pkl"), "rb"))
S = pickle.load(open(os.path.join(STAGE, "logs", "exact_sdp2_M.pkl"), "rb"))
CK = pickle.load(open(os.path.join(STAGE, "logs", "exact_povm_y_checkpoint.pkl"), "rb"))
dirs, bases = D["dirs"], D["bases_exact"]
Mf = S["M"]
J = len(dirs)
dims = [len(bases[j]) for j in range(J)]
I = CK["I"]
ystr = CK["y"]
assert len(I) == 175 and len(ystr) == 175

UP = [(r, s) for r in range(20) for s in range(r, 20)]
SU = [(r, s) for r in range(20) for s in range(r + 1, 20)]
upos = {p: k for k, p in enumerate(UP)}
NR = 484
U = []
for j in range(J):
    m = dims[j]
    for a in range(m + 1):
        for b in range(a, m + 1):
            U.append((j, a, b))
N = len(U)
assert N == 6566, N


def frac_pair(p):
    # exact rational strings ("p/q" or "p") as Fraction
    return Fraction(str(p[0])), Fraction(str(p[1]))


# ---------- (1) exact arithmetic modulo primes ----------
def modp_build(p):
    def fm(f):
        return (f.numerator % p) * pow(f.denominator % p, -1, p) % p

    def cm(a, b):  # complex mult on pairs mod p
        return ((a[0] * b[0] - a[1] * b[1]) % p, (a[0] * b[1] + a[1] * b[0]) % p)

    def cc(a):
        return (a[0], (-a[1]) % p)

    X, B = [], []
    for j in range(J):
        (a0r, a0i), (a1r, a1i) = dirs[j]
        X.append(
            [
                (fm(Fraction(str(a0r))), fm(Fraction(str(a0i)))),
                (fm(Fraction(str(a1r))), fm(Fraction(str(a1i)))),
            ]
        )
        B.append(
            [
                [
                    (fm(Fraction(str(bases[j][v][r][0]))), fm(Fraction(str(bases[j][v][r][1]))))
                    for r in range(20)
                ]
                for v in range(dims[j])
            ]
        )

    cols = []
    for j, a, b in U:
        m = dims[j]
        V = [[(0, 0)] * 22 for _ in range(m + 1)]
        for c in range(m):
            for r in range(20):
                V[c][2 + r] = B[j][c][r]
        V[m][0], V[m][1] = X[j][0], X[j][1]
        if a == b:
            Sm = [[cm(V[a][i], cc(V[a][k])) for k in range(22)] for i in range(22)]
        else:
            P1 = [[cm(V[a][i], cc(V[b][k])) for k in range(22)] for i in range(22)]
            P2 = [[cm(V[b][i], cc(V[a][k])) for k in range(22)] for i in range(22)]
            Sm = [
                [
                    ((P1[i][k][0] + P2[i][k][0]) % p, (P1[i][k][1] + P2[i][k][1]) % p)
                    for k in range(22)
                ]
                for i in range(22)
            ]
        col = [0] * NR
        col[0] = Sm[0][0][0]
        col[1] = Sm[0][1][0]
        col[2] = Sm[1][1][0]
        col[3] = Sm[0][1][1]
        for al in range(2):
            for rho in range(20):
                col[4 + al * 20 + rho] = Sm[al][2 + rho][0]
                col[44 + al * 20 + rho] = Sm[al][2 + rho][1]
        for k, (r, s) in enumerate(UP):
            col[84 + k] = Sm[2 + r][2 + s][0]
        for k, (r, s) in enumerate(SU):
            col[294 + k] = Sm[2 + r][2 + s][1]
        cols.append(col)
    return cols, fm


def check_modp(p):
    cols, fm = modp_build(p)
    yv = [fm(Fraction(str(s))) for s in ystr]
    mvec = [fm(Fraction(float(Mf[j][a, b]))) for (j, a, b) in U]
    # delta_k = sum_i A[i][k] y_i   (i over independent rows I)
    delta = [0] * N
    for t, i in enumerate(I):
        yi = yv[t]
        for k in range(N):
            aik = cols[k][i]
            if aik:
                delta[k] = (delta[k] + aik * yi) % p
    Mstar = [(mvec[k] + delta[k]) % p for k in range(N)]
    bvec = [0] * NR
    bvec[0] = 1
    bvec[2] = 1
    for rho in range(20):
        bvec[84 + upos[(rho, rho)]] = 1
    bad = 0
    # residual over ALL 484 rows (uses all columns, not only I)
    res = [0] * NR
    for k in range(N):
        mk = Mstar[k]
        if mk:
            col = cols[k]
            for r in range(NR):
                if col[r]:
                    res[r] = (res[r] + col[r] * mk) % p
    for r in range(NR):
        if (res[r] - bvec[r]) % p:
            bad += 1
    return {"prime": p, "rows_nonzero_residual_mod_p": bad}


PRIMES = [
    2305843009213693951,
    4611686018427387847,
    9223372036854775783,
]  # 2^61-1, and two other large primes

out = {"instance": "verify_cert_compact", "rows": NR, "columns": N, "independent_rows": 175}
out["modp"] = []
for p in PRIMES:
    r = check_modp(p)
    out["modp"].append(r)
    print("mod p check:", r, flush=True)


# ---------- (2) high-precision positivity of the corrected blocks ----------
def dec_frac(f):
    return Decimal(f.numerator) / Decimal(f.denominator)


y_dec = [dec_frac(Fraction(str(s))) for s in ystr]
max_abs_y = max(abs(v) for v in y_dec)


def dec_build():
    def cd_mul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def cd_conj(a):
        return (a[0], -a[1])

    X, B = [], []
    for j in range(J):
        (a0r, a0i), (a1r, a1i) = dirs[j]
        X.append(
            [
                (dec_frac(Fraction(str(a0r))), dec_frac(Fraction(str(a0i)))),
                (dec_frac(Fraction(str(a1r))), dec_frac(Fraction(str(a1i)))),
            ]
        )
        B.append(
            [
                [
                    (
                        dec_frac(Fraction(str(bases[j][v][r][0]))),
                        dec_frac(Fraction(str(bases[j][v][r][1]))),
                    )
                    for r in range(20)
                ]
                for v in range(dims[j])
            ]
        )
    cols = []
    zero = (Decimal(0), Decimal(0))
    for j, a, b in U:
        m = dims[j]
        V = [[zero] * 22 for _ in range(m + 1)]
        for c in range(m):
            for r in range(20):
                V[c][2 + r] = B[j][c][r]
        V[m][0], V[m][1] = X[j][0], X[j][1]

        def S_entry(i, k):
            if a == b:
                return cd_mul(V[a][i], cd_conj(V[a][k]))
            t1 = cd_mul(V[a][i], cd_conj(V[b][k]))
            t2 = cd_mul(V[b][i], cd_conj(V[a][k]))
            return (t1[0] + t2[0], t1[1] + t2[1])

        col = [Decimal(0)] * NR
        col[0] = S_entry(0, 0)[0]
        col[1] = S_entry(0, 1)[0]
        col[2] = S_entry(1, 1)[0]
        col[3] = S_entry(0, 1)[1]
        for al in range(2):
            for rho in range(20):
                e = S_entry(al, 2 + rho)
                col[4 + al * 20 + rho] = e[0]
                col[44 + al * 20 + rho] = e[1]
        for k, (r, s) in enumerate(UP):
            col[84 + k] = S_entry(2 + r, 2 + s)[0]
        for k, (r, s) in enumerate(SU):
            col[294 + k] = S_entry(2 + r, 2 + s)[1]
        cols.append(col)
    return cols


cols_d = dec_build()
mvec_d = [Decimal(float(Mf[j][a, b])) for (j, a, b) in U]
delta_d = [Decimal(0)] * N
for t, i in enumerate(I):
    yi = y_dec[t]
    for k in range(N):
        aik = cols_d[k][i]
        if aik:
            delta_d[k] += aik * yi
Mstar_d = [mvec_d[k] + delta_d[k] for k in range(N)]

# block LDL in Decimal
pivots_min = None
blocks_pd = True
for j in range(J):
    m = dims[j]
    n = m + 1
    Mx = [[Decimal(0)] * n for _ in range(n)]
    for k, (jj, a, b) in enumerate(U):
        if jj == j:
            Mx[a][b] = Mstar_d[k]
            Mx[b][a] = Mstar_d[k]
    W = [row[:] for row in Mx]
    for p_ in range(n):
        piv = W[p_][p_]
        if piv <= 0:
            blocks_pd = False
            break
        pivots_min = piv if pivots_min is None or piv < pivots_min else pivots_min
        for q in range(p_ + 1, n):
            f = W[q][p_] / piv
            for c in range(p_, n):
                W[q][c] -= f * W[p_][c]
    if not blocks_pd:
        break

out["max_abs_y"] = str(max_abs_y)[:30]
out["min_pivot_decimal"] = str(pivots_min)[:30] if pivots_min is not None else None
out["all_blocks_positive_definite_decimal200"] = blocks_pd
out["blocks"] = J
out["note"] = (
    "mod-p residual = fingerprint; PD = high precision; exact rational check is exact_cert.py (earlier run)"
)
json.dump(out, open(os.path.join(STAGE, "logs", "verify_cert_compact.json"), "w"), indent=1)
print(json.dumps(out, indent=1), flush=True)
sys.exit(0 if blocks_pd and all(r["rows_nonzero_residual_mod_p"] == 0 for r in out["modp"]) else 1)
