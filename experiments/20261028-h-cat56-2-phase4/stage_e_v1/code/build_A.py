import numpy as np
# WHY: interval EXISTENCE certificate for the S+ POVM on exact directions.
# Unknowns: upper-triangular entries of M_j (moments of the rank-one elements at direction x_j).
# Linear constraints (exact rational coefficients from exact kernel bases B_j):
#   E1: sum_j t_j x_j x_j^dag = I_2          (4 real rows)
#   E2: sum_j x_j (B_j s_j)^dag = 0          (80 real rows)
#   E3: sum_j B_j Q_j B_j^dag = I_20         (400 real rows)
# Residual r = b - A m; if G = A A^T is invertible (interval check), then delta = A^T G^{-1} r gives an
# exact solution A(m+delta) = b with ||delta_j|| <= bound.  PSD margin: lambda_min(M_j) > ||delta_j||.
import pickle, sys, time
from fractions import Fraction
import flint
from flint import arb, arb_mat

t0 = time.time()
D = pickle.load(open("../logs/exact_bases2.pkl", "rb"))
S = pickle.load(open("../logs/exact_sdp2_M.pkl", "rb"))
Mf = S["M"]
J = len(Mf)
dims = [Mf[j].shape[0] - 1 for j in range(J)]


def fr(s):
    f = Fraction(s)
    return arb(f.numerator) / arb(f.denominator)


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cconj(a):
    return (a[0], -a[1])


X = []
B = []  # B[j][r][v]: component r of basis vector v (arb complex)
for j, (dr) in enumerate(D["dirs"]):
    (a0r, a0i), (a1r, a1i) = dr
    X.append([(fr(a0r), fr(a0i)), (fr(a1r), fr(a1i))])
    bj = D["bases_exact"][j]
    m = dims[j]
    B.append([[(fr(bj[v][r][0]), fr(bj[v][r][1])) for v in range(m)] for r in range(20)])

# unknown list: (j, a, b) with a <= b over 0..m_j
U = []
for j in range(J):
    m = dims[j]
    for a in range(m + 1):
        for b in range(a, m + 1):
            U.append((j, a, b))
N = len(U)
ui = {u: k for k, u in enumerate(U)}
NR = 484
A = [[arb(0) for _ in range(N)] for _ in range(NR)]
rhs = [arb(0) for _ in range(NR)]

# row maps
def e1_re(p, q): return {(0, 0): 0, (0, 1): 1, (1, 1): 2}[(p, q)]
def e1_im(p, q): return 3
def e2_re(al, rho): return 4 + al * 20 + rho
def e2_im(al, rho): return 4 + 40 + al * 20 + rho
UP = [(r, s) for r in range(20) for s in range(r, 20)]
SU = [(r, s) for r in range(20) for s in range(r + 1, 20)]
upos = {p: k for k, p in enumerate(UP)}
spos = {p: k for k, p in enumerate(SU)}
def e3_re(r, s): return 84 + upos[(r, s)]
def e3_im(r, s): return 84 + len(UP) + spos[(r, s)]

rhs[0] = arb(1); rhs[2] = arb(1)  # I_2 diagonal (0,0),(1,1) real parts

for k, (j, a, b) in enumerate(U):
    m = dims[j]
    xj = X[j]
    if (a, b) == (m, m):  # t_j
        for p in range(2):
            for q in range(p, 2):
                P = cmul(xj[p], cconj(xj[q]))
                A[e1_re(p, q)][k] = P[0]
                if p < q:
                    A[e1_im(p, q)][k] = P[1]
    elif b == m:  # s_a, a < m : contributes to E2 via x_al * conj(B[rho][a])
        for al in range(2):
            for rho in range(20):
                c = cmul(xj[al], cconj(B[j][rho][a]))
                A[e2_re(al, rho)][k] = c[0]
                A[e2_im(al, rho)][k] = c[1]
    else:  # Q_{a b}, a <= b < m
        for rho in range(20):
            for sig in range(rho, 20):
                if a == b:
                    c = cmul(B[j][rho][a], cconj(B[j][sig][a]))
                else:
                    c1 = cmul(B[j][rho][a], cconj(B[j][sig][b]))
                    c2 = cmul(B[j][rho][b], cconj(B[j][sig][a]))
                    c = (c1[0] + c2[0], c1[1] + c2[1])
                A[e3_re(rho, sig)][k] = c[0]
                if rho < sig:
                    A[e3_im(rho, sig)][k] = c[1]
for rho in range(20):
    rhs[e3_re(rho, rho)] = arb(1)
print("A built:", NR, "x", N, "in", round(time.time() - t0, 1), "s", flush=True)
Af = np.array([[float(A[i][k].mid()) for k in range(N)] for i in range(NR)])
np.save("../logs/A_float.npy", Af)
np.save("../logs/rhs_float.npy", np.array([float(rhs[i].mid()) for i in range(NR)]))
np.save("../logs/mvec_float.npy", np.array([float(arb(float(Mf[j][a, b])).mid()) for (j, a, b) in U]))
print("saved A", Af.shape, flush=True)
