# WHY: exact POVM for S+ (stage E). Same exact certificate as exact_cert.py (identical A, b, r, G_I),
# plus what exact_cert.py did not keep:
#  (1) checkpoint of the rational solve y (resumes if the checkpoint exists),
#  (2) exact corrected moments M_j* saved,
#  (3) exact LDL^T of each M_j* into rank-one pieces c c^T with positive weights d (positive pivots),
#      lifted to POVM elements u = (c_m * x_j ; sum_a c_a * B_j[:, a]) with weight d,
#  (4) exact check of sum_k d_k u_k u_k^H = I_22 over Q(i).
# The lift is linear: sum_k d_k Phi(u_k) = sum_j sum_ab M_j*[a,b] Phi_ab, so (4) tests the same
# equations as the certificate, now on the actual vectors. (4) is an independent re-check, not a formality.
import json
import os
import pickle
import time
from fractions import Fraction

import numpy as np
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
b[0] = fmpq(1)
b[2] = fmpq(1)
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

# (1) checkpoint: reuse the rational solve if it exists for the same independent-row set
CK = "../logs/exact_povm_y_checkpoint.pkl"
if os.path.exists(CK):
    ck = pickle.load(open(CK, "rb"))
    assert ck["I"] == I, "checkpoint row set differs"
    y = fmpq_mat(len(I), 1, [fq(s) for s in ck["y"]])
    print("y loaded from checkpoint", flush=True)
else:
    G = AI * AI.transpose()
    rI = fmpq_mat(len(I), 1, [r[i, 0] for i in I])
    y = G.solve(rI)
    pickle.dump({"I": I, "y": [str(y[i, 0]) for i in range(len(I))]}, open(CK, "wb"))
    print("y solved and checkpointed at", round(time.time() - t0, 1), "s", flush=True)

delta = AI.transpose() * y
check = Afull * delta - r
viol = [i for i in range(NR) if check[i, 0] != 0]
print("rows violated exactly:", len(viol), flush=True)
if viol:
    raise SystemExit("exact certificate FAILED; stop")

# (2) exact corrected moments M_j* = m + delta
Ms = [[[fmpq(0)] * (dims[j] + 1) for _ in range(dims[j] + 1)] for j in range(J)]
for k, (j, a, bb) in enumerate(U):
    val = mvec[k] + delta[k, 0]
    Ms[j][a][bb] = val
    Ms[j][bb][a] = val
json.dump(
    [[[str(v) for v in row] for row in Mx] for Mx in Ms],
    open("../logs/exact_povm_Mstar.json", "w"),
)
print("M* saved", round(time.time() - t0, 1), "s", flush=True)


# (3) exact LDL^T over Q: M = sum_p d_p c_p c_p^T, c_p unit-lower column, d_p > 0
def ldl(Mx):
    n = len(Mx)
    W = [row[:] for row in Mx]
    cols, weights = [], []
    for p in range(n):
        piv = W[p][p]
        if piv <= 0:
            raise ValueError("non-positive pivot %s at %d" % (piv, p))
        col = [fmpq(0)] * n
        col[p] = fmpq(1)
        for q in range(p + 1, n):
            col[q] = W[q][p] / piv
        for q in range(p + 1, n):
            for c in range(p + 1, n):
                W[q][c] = W[q][c] - W[q][p] * W[p][c] / piv
        cols.append(col)
        weights.append(piv)
    return cols, weights


Ele = []  # (block j, weight w, vector u in C^22 as pairs)
recon_ok = True
for j in range(J):
    m = dims[j]
    cols, wts = ldl(Ms[j])
    # reconstruction check: sum_p d_p c_p c_p^T == M_j* exactly
    n = m + 1
    for a in range(n):
        for bb in range(n):
            s_ = fmpq(0)
            for col, w in zip(cols, wts):
                s_ += w * col[a] * col[bb]
            if s_ != Ms[j][a][bb]:
                recon_ok = False
    for col, w in zip(cols, wts):
        u = []
        for al in range(2):
            u.append((col[m] * X[j][al][0], col[m] * X[j][al][1]))
        for rho in range(20):
            re_ = fmpq(0)
            im_ = fmpq(0)
            for a in range(m):
                re_ += col[a] * B[j][rho][a][0]
                im_ += col[a] * B[j][rho][a][1]
            u.append((re_, im_))
        Ele.append((j, w, u))
print("elements:", len(Ele), "LDL reconstruction exact:", recon_ok, flush=True)

# (4) exact sum_k w_k u_k u_k^H over Q(i)
Smat = [[(fmpq(0), fmpq(0)) for _ in range(22)] for _ in range(22)]
for j, w, u in Ele:
    for r1 in range(22):
        for s1 in range(22):
            p_ = cmul(u[r1], cconj(u[s1]))
            Smat[r1][s1] = (Smat[r1][s1][0] + w * p_[0], Smat[r1][s1][1] + w * p_[1])
sum_ok = True
max_dev = None
for r1 in range(22):
    for s1 in range(22):
        tgt = 1 if r1 == s1 else 0
        if Smat[r1][s1][0] != tgt or Smat[r1][s1][1] != 0:
            sum_ok = False
print("sum_k w_k u_k u_k^H == I22 exactly:", sum_ok, round(time.time() - t0, 1), "s", flush=True)

weights_f = [float(w) for (_, w, _) in Ele]
out = {
    "independent_rows": len(I),
    "rows_violated_exactly": len(viol),
    "M_positive_pivots_exact": True,
    "LDL_reconstruction_exact": recon_ok,
    "n_elements": len(Ele),
    "sum_equals_I22_exactly": sum_ok,
    "min_weight_float": min(weights_f),
    "max_weight_float": max(weights_f),
    "seconds": round(time.time() - t0, 1),
}
json.dump(out, open("../logs/exact_povm_result.json", "w"), indent=1)
elements = [
    {
        "block": j,
        "x": [[str(X[j][al][0]), str(X[j][al][1])] for al in range(2)],
        "w": str(w),
        "u": [[str(re_), str(im_)] for (re_, im_) in u],
    }
    for (j, w, u) in Ele
]
json.dump(elements, open("../logs/exact_povm_elements.json", "w"))
print(json.dumps(out, indent=1), flush=True)
