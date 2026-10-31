# WHY: EXACT (rational) existence certificate for the S+ POVM moments on exact directions.
#  1. Build the exact rational constraint matrix A (484 x N) and RHS b from exact bases B_j and directions x_j.
#  2. Take 175 independent rows I (numerical pivoted QR; exactness of independence is tested below).
#  3. Exact rational y = G_I^{-1} r_I with G_I = A_I A_I^T, r = b - A m (m = float moments, exact dyadic).
#  4. delta = A_I^T y.  Check A delta == r for ALL 484 rows EXACTLY.  If yes, M* = m + delta solves all equations.
#  5. Exact positivity: LDL^T of each M_j* over Q (leading pivots > 0  <=>  M_j* positive definite).
import pickle, json, time
from fractions import Fraction
import numpy as np
import flint
from flint import fmpq, fmpq_mat

t0 = time.time()
D = pickle.load(open("../logs/exact_bases2.pkl", "rb"))
S = pickle.load(open("../logs/exact_sdp2_M.pkl", "rb"))
Mf = S["M"]
J = len(Mf)
dims = [Mf[j].shape[0] - 1 for j in range(J)]


def fq(s):
    f = Fraction(s)
    return fmpq(f.numerator, f.denominator)


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cconj(a):
    return (a[0], -a[1])


X, B = [], []
for j, dr in enumerate(D["dirs"]):
    (a0r, a0i), (a1r, a1i) = dr
    X.append([(fq(a0r), fq(a0i)), (fq(a1r), fq(a1i))])
    bj = D["bases_exact"][j]
    m = dims[j]
    B.append([[(fq(bj[v][r][0]), fq(bj[v][r][1])) for v in range(m)] for r in range(20)])
ZERO = fmpq(0)

UP = [(r, s) for r in range(20) for s in range(r, 20)]
SU = [(r, s) for r in range(20) for s in range(r + 1, 20)]
upos = {p: k for k, p in enumerate(UP)}
spos = {p: k for k, p in enumerate(SU)}
U = []
for j in range(J):
    m = dims[j]
    for a in range(m + 1):
        for b in range(a, m + 1):
            U.append((j, a, b))
N = len(U)
NR = 484
Arows = [dict() for _ in range(NR)]
b = [ZERO] * NR
b[0] = fmpq(1); b[2] = fmpq(1)
for rho in range(20):
    b[84 + upos[(rho, rho)]] = fmpq(1)


def put(i, k, v):
    if v != 0:
        Arows[i][k] = v


for k, (j, a, bb) in enumerate(U):
    m = dims[j]
    xj = X[j]
    if (a, bb) == (m, m):
        for p in range(2):
            for q in range(p, 2):
                P = cmul(xj[p], cconj(xj[q]))
                row_re = {(0, 0): 0, (0, 1): 1, (1, 1): 2}[(p, q)]
                put(row_re, k, P[0])
                if p < q:
                    put(3, k, P[1])
    elif bb == m:
        for al in range(2):
            for rho in range(20):
                c = cmul(xj[al], cconj(B[j][rho][a]))
                put(4 + al * 20 + rho, k, c[0])
                put(4 + 40 + al * 20 + rho, k, c[1])
    else:
        for rho in range(20):
            for sig in range(rho, 20):
                if a == bb:
                    c = cmul(B[j][rho][a], cconj(B[j][sig][a]))
                else:
                    c1 = cmul(B[j][rho][a], cconj(B[j][sig][bb]))
                    c2 = cmul(B[j][rho][bb], cconj(B[j][sig][a]))
                    c = (c1[0] + c2[0], c1[1] + c2[1])
                put(84 + upos[(rho, sig)], k, c[0])
                if rho < sig:
                    put(84 + len(UP) + spos[(rho, sig)], k, c[1])
print("A built (rows", NR, "cols", N, ") in", round(time.time() - t0, 1), "s", flush=True)

mvec = [fq(0)] * N
for k, (j, a, bb) in enumerate(U):
    mvec[k] = fq(float(Mf[j][a, bb]))
Afull = fmpq_mat(NR, N, [Arows[i].get(k, ZERO) for i in range(NR) for k in range(N)])
Mcol = fmpq_mat(N, 1, mvec)
bcol = fmpq_mat(NR, 1, b)
r = bcol - Afull * Mcol
print("residual r built; nonzero rows:", sum(1 for i in range(NR) if r[i, 0] != 0), flush=True)

I = [int(x) for x in np.load("../logs/indep_rows.npy")]
AI = fmpq_mat(len(I), N, [Arows[i].get(k, ZERO) for i in I for k in range(N)])
G = AI * AI.transpose()
rI = fmpq_mat(len(I), 1, [r[i, 0] for i in I])
try:
    y = G.solve(rI)
    solved = True
except Exception as e:
    solved = False
    print("G_I solve failed:", type(e).__name__, str(e)[:200], flush=True)
out = {"independent_rows": len(I), "G_I_invertible_exact": solved}
if solved:
    delta = AI.transpose() * y
    check = Afull * delta - r
    viol = [i for i in range(NR) if check[i, 0] != 0]
    out["rows_violated_exactly"] = len(viol)
    out["first_violated"] = viol[:10]
    if not viol:
        Ms = []
        for j in range(J):
            ks = [k for k, (jj, a, bb) in enumerate(U) if jj == j]
            m = dims[j]
            Mx = [[fmpq(0)] * (m + 1) for _ in range(m + 1)]
            for k in ks:
                _, a, bb = U[k]
                val = mvec[k] + delta[k, 0]
                Mx[a][bb] = val; Mx[bb][a] = val
            Ms.append(Mx)
        # exact LDL^T positivity: leading principal minors > 0 (Sylvester) for every M_j*
        pos_ok, min_piv = True, None
        for Mx in Ms:
            n = len(Mx)
            Mt = [row[:] for row in Mx]
            for p in range(n):
                piv = Mt[p][p]
                if piv <= 0:
                    pos_ok = False; break
                min_piv = piv if min_piv is None or piv < min_piv else min_piv
                for q in range(p + 1, n):
                    f = Mt[q][p] / piv
                    for c in range(p, n):
                        Mt[q][c] = Mt[q][c] - f * Mt[p][c]
            if not pos_ok:
                break
        out["all_M_positive_definite_exact"] = pos_ok
        out["min_pivot_float"] = float(min_piv) if min_piv is not None else None
out["seconds"] = round(time.time() - t0, 1)
json.dump(out, open("../logs/exact_cert_result.json", "w"), indent=1)
print(json.dumps(out, indent=1), flush=True)
