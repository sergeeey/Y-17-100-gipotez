# WHY: exact rational kernel K (40 x m, real) is ill-conditioned (cond up to 2.5e10).  Any rational T gives
# another exact basis K*T of the SAME kernel.  Choose T = round(R^{-1}, 2^-40) from a QR of K, so K*T is
# (exactly) a well-conditioned basis.  Output: exact basis strings for the certificate + float basis for SDP.
import pickle
import numpy as np
from fractions import Fraction
from exact_kernel import exact_kernel
D = pickle.load(open("../logs/exact_dirs.pkl", "rb"))
SC = 2 ** 40
out, conds = [], []
for d in D["dirs"]:
    (a0r, a0i), (a1r, a1i) = d
    x = ((Fraction(a0r), Fraction(a0i)), (Fraction(a1r), Fraction(a1i)))
    rank, basis = exact_kernel(x)       # list of m real 40-vectors (Fractions)
    m = len(basis)
    K = np.array([[float(v[i]) for v in basis] for i in range(40)])   # 40 x m float (for T only)
    _, R = np.linalg.qr(K)
    T = np.linalg.inv(R)
    Tr = [[Fraction(round(T[i, j] * SC), SC) for j in range(m)] for i in range(m)]
    Bn = [[sum((basis[k][i] * Tr[k][j] for k in range(m)), Fraction(0)) for j in range(m)] for i in range(40)]
    Bn_f = np.array([[float(Bn[i][j]) for j in range(m)] for i in range(40)])
    conds.append(np.linalg.cond(Bn_f))
    # complex basis column j: p = rows 0..19, q = rows 20..39
    out.append([[(str(Bn[r][j]), str(Bn[20 + r][j])) for r in range(20)] for j in range(m)])
print("cond(new basis) min/median/max:", min(conds), float(np.median(conds)), max(conds))
pickle.dump({"dirs": D["dirs"], "dims": D["dims"], "bases_exact": out}, open("../logs/exact_bases2.pkl", "wb"))
print("stored", len(out), "points")
