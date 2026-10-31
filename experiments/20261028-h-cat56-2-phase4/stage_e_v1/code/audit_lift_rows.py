# WHY: independent check of the 484-row moment system A (the linearisation used by exact_cert.py).
# Builds the coefficient of each moment entry M_j[a,b] (a<=b, column U=(j,a,b)) DIRECTLY from the lift
# definition  u = sum_a c_a v_a,  v_a = (x_j * [a==m] ; B_j[:,a]),  so  sum_p d_p u_p u_p^H = sum_ab M_ab v_a v_b^H,
# then reads off the 484 real coordinates (E1: 2x2 block, E2: 2x20 block, E3: 20x20 block) and compares
# to logs/A_float.npy (float build from build_A.py). Also checks the target b against I_22 directly.
# Floats only (the exact-integer identity is already checked by exact_cert.py); tolerance 1e-9 relative.
import os
import pickle
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
D = pickle.load(open(os.path.join(STAGE, "logs", "exact_bases2.pkl"), "rb"))
dirs, bases = D["dirs"], D["bases_exact"]
dims = [len(bases[j]) for j in range(len(dirs))]  # m_j basis vectors per direction
J = len(dirs)


def cf(p):
    # pickled values are exact rational strings such as "117932410739/549755813888"
    return complex(float(Fraction(str(p[0]))), float(Fraction(str(p[1]))))


UP = [(r, s) for r in range(20) for s in range(r, 20)]
SU = [(r, s) for r in range(20) for s in range(r + 1, 20)]
NR = 4 + 80 + 400  # 484 real rows: E1 (4), E2 (80), E3 (400)
assert NR == 484 and len(UP) == 210 and len(SU) == 190

cols = []  # direct columns, in order U=(j,a,b), a<=b, a,b in 0..m_j
for j in range(J):
    (a0r, a0i), (a1r, a1i) = dirs[j]
    x = np.array([cf((a0r, a0i)), cf((a1r, a1i))])
    m = dims[j]
    V = np.zeros((m + 1, 22), dtype=complex)  # v_a rows (length 22)
    for a in range(m):
        V[a, 2:] = [cf(bases[j][a][r]) for r in range(20)]
    V[m, :2] = x
    for a in range(m + 1):
        for b in range(a, m + 1):
            if a == b:
                S = np.outer(V[a], V[a].conj())
            else:
                S = np.outer(V[a], V[b].conj()) + np.outer(V[b], V[a].conj())
            col = np.zeros(NR)
            col[0] = S[0, 0].real
            col[1] = S[0, 1].real
            col[2] = S[1, 1].real
            col[3] = S[0, 1].imag
            for al in range(2):
                for rho in range(20):
                    col[4 + al * 20 + rho] = S[al, 2 + rho].real
                    col[44 + al * 20 + rho] = S[al, 2 + rho].imag
            for k, (r, s) in enumerate(UP):
                col[84 + k] = S[2 + r, 2 + s].real
            for k, (r, s) in enumerate(SU):
                col[294 + k] = S[2 + r, 2 + s].imag
            cols.append(col)

Adirect = np.array(cols).T  # 484 x N
Afloat = np.load(os.path.join(STAGE, "logs", "A_float.npy"))
print("direct A shape", Adirect.shape, "stored A shape", Afloat.shape, flush=True)
if Adirect.shape != Afloat.shape:
    raise SystemExit("shape mismatch")
scale = max(1.0, np.abs(Afloat).max())
err = np.abs(Adirect - Afloat).max()
print("max |A_direct - A_float| =", err, "relative to max|A| =", err / scale, flush=True)

# target b: I_22 in the same coordinates (only diagonal of E1 (0,0),(1,1) and E3 diagonal; E2, offdiag zero)
b = np.zeros(NR)
b[0] = 1.0
b[2] = 1.0
for rho in range(20):
    b[84 + UP.index((rho, rho))] = 1.0
bf = np.load(os.path.join(STAGE, "logs", "rhs_float.npy"))
print("max |b_direct - rhs_float| =", np.abs(b - bf).max(), flush=True)
ok = err <= 1e-9 * scale and np.abs(b - bf).max() == 0.0
print("LIFT_ROWS_AGREE" if ok else "LIFT_ROWS_DISAGREE", flush=True)
