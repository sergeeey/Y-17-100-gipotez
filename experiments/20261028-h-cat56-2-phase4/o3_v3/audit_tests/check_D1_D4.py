"""D1/D4 checks: diagonal imaginary parts, trace, s* values (no interval recomputation)."""
import sys
from fractions import Fraction
import numpy as np

RPATH = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261028-h-cat56-2-phase3\metrics\inputs\s14_R_4-5-6-7-8-9-10-11-12-13-14-15_nx250.npz"
R = np.load(RPATH)["R"]
print("dtype", R.dtype, "shape", R.shape)
print("max|R-R^H|", float(np.abs(R - R.conj().T).max()))
print("max|Im diag R|", float(np.abs(R.diagonal().imag).max()))
diag_re = [float(R[i, i].real) for i in range(20)]
# sequential binary64 as in code: trR_f = float(np.trace(0.5*(R+R^H)).real); s = 0.9*trR_f/20
H = 0.5 * (R + R.conj().T)
trH_f = float(np.trace(H).real)
s_seq = 0.9 * trH_f / 20.0
print("trH_f", repr(trH_f), float(s_seq).hex())
# exact rational of the stored binary64 real diagonal
tr_exact = sum(Fraction(d) for d in diag_re)
print("tr_exact", float(tr_exact), "as Fraction ok")
s_exact_real = Fraction(9, 10) * tr_exact / 20
s_round_once = float(s_exact_real)
print("s_round_once", repr(s_round_once), s_round_once.hex())
print("s_seq", repr(s_seq), s_seq.hex())
print("s_seq - s_round_once =", s_seq - s_round_once)
print("gamma_exact = tr - 20 s_seq =", float(tr_exact - 20 * Fraction(s_seq)))
print("max |trace(R) - trace(H)| =", abs(np.trace(R) - np.trace(H)))
