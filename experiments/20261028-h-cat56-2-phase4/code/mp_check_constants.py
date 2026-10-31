"""mpmath (40 digits) re-verification of float constants used by the S- cell certificate.
Independent of numpy: Phi rows rebuilt from the integer data of the instance; R float values taken as exact binary rationals and Hermitized exactly.
Checks: L_Phi, ||M||, and sigma_36 / lambda_K at sample cell centres vs float values.
"""

import json
import math
import sys

import numpy as np
from mpmath import mp, mpf, mpc, matrix, eigsy, sqrt, cos, sin, exp, pi

mp.dps = 40
BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
RPATH = (
    BASE
    + r"\20261028-h-cat56-2-phase3\metrics\inputs\s14_R_4-5-6-7-8-9-10-11-12-13-14-15_nx250.npz"
)
S = list(range(4, 16))

rec = json.loads(open(INST, encoding="utf-8").readline())
A = []  # A[i][r][a] mpc, A = -2i (re + i im)
for flat in rec["blocks"]:
    blk = [[None, None] for _ in range(20)]
    for r in range(20):
        for a in range(2):
            re_, im_ = mpf(flat[2 * r + a]), mpf(flat[40 + 2 * r + a])
            blk[r][a] = mpc(2 * im_, -2 * re_)
    A.append(blk)


def phi_rows(x):
    rows = []
    for i in S:
        a0 = [A[i][r][0].conjugate() for r in range(20)]
        a1 = [A[i][r][1].conjugate() for r in range(20)]
        g1 = [x[0] * a1[r] - x[1] * a0[r] for r in range(20)]
        g3 = [x[0].conjugate() * a0[r] + x[1].conjugate() * a1[r] for r in range(20)]
        rows.append([g.real for g in g1] + [-g.imag for g in g1])
        rows.append([g.imag for g in g1] + [g.real for g in g1])
        rows.append([g.imag for g in g3] + [g.real for g in g3])
    return matrix(rows)


def specnorm(P):
    G = P * P.T
    E = eigsy(G, eigvals_only=True)
    return sqrt(max(E))


BX = [(mpc(1), mpc(0)), (mpc(0, 1), mpc(0)), (mpc(0), mpc(1)), (mpc(0), mpc(0, 1))]
PHI = [phi_rows(x) for x in BX]
norms = [specnorm(P) for P in PHI]
L = sqrt(sum(n**2 for n in norms))
print("mp L_Phi =", mp.nstr(L, 15), " per-basis norms", [mp.nstr(n, 10) for n in norms])

R0 = np.load(RPATH)["R"]
Rr = [[mpf(float(R0[i, j].real)) for j in range(20)] for i in range(20)]
Ri = [[mpf(float(R0[i, j].imag)) for j in range(20)] for i in range(20)]
Rre = matrix(20, 20)
Rim = matrix(20, 20)
for i in range(20):
    for j in range(20):
        Rre[i, j] = (Rr[i][j] + Rr[j][i]) / 2
        Rim[i, j] = (Ri[i][j] - Ri[j][i]) / 2
M = matrix(40, 40)
for i in range(20):
    for j in range(20):
        M[i, j] = Rre[i, j]
        M[i, 20 + j] = -Rim[i, j]
        M[20 + i, j] = Rim[i, j]
        M[20 + i, 20 + j] = Rre[i, j]
Em = eigsy(M, eigvals_only=True)
print(
    "mp ||M|| =",
    mp.nstr(max(abs(e) for e in Em), 15),
    " lambda_max(M) =",
    mp.nstr(max(Em), 15),
    " trR =",
    mp.nstr(sum(Rre[i, i] for i in range(20)), 15),
)

rng = np.random.default_rng(7)
out = []
for _ in range(6):
    th = math.acos(rng.uniform(-1, 1))
    ph = rng.uniform(0, 2 * math.pi)
    t, p = mpf(th), mpf(ph)
    u = [cos(t / 2), mpf(0), sin(t / 2) * cos(p), sin(t / 2) * sin(p)]
    Phi = sum((u[j] * PHI[j] for j in range(4)), matrix(36, 40))
    E, Q = eigsy(Phi.T * Phi)  # ascending
    sig36 = sqrt(E[4])  # 5th smallest eigenvalue = 36th singular value (4 zeros)
    zeros = [mp.nstr(E[k], 3) for k in range(4)]
    Z = Q[:, 0:4]
    G = Z.T * M * Z
    lamK = max(eigsy(G, eigvals_only=True))
    # float counterpart
    sys.path.insert(0, BASE + r"\20261027-h-cat56-2-discovery\code")
    import s8_admissible_span as sa

    As = sa.load_A(INST)
    xf = np.array([math.cos(th / 2), math.sin(th / 2) * np.exp(1j * ph)])
    Pf = sa.phi_rows(As, S, xf)
    sf = np.linalg.svd(Pf, compute_uv=False)[35]
    out.append((th, ph, float(sig36), float(sf), float(lamK)))
    print(
        f"th={th:.4f} ph={ph:.4f}  mp sigma36={mp.nstr(sig36, 12)} float={sf:.12f} rel.diff={abs(float(sig36) - sf) / float(sig36):.2e}  mp lambda_K={mp.nstr(lamK, 10)}  4 smallest eig(Phi'Phi)={zeros}"
    )
