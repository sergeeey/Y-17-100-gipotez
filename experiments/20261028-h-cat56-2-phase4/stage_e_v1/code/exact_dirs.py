# WHY: exact directions for the S+ POVM.  Candidate x_k are phase-normalised (x0 real >= 0); components whose
# imaginary part is at the 1e-7 noise level are set to real exactly (structural real-circle points).
# Each direction is rounded to dyadic rationals (2^-40), so the real 36x40 constraint matrix is EXACT (rational)
# and its kernel dimension is determined exactly (no tolerance).
import numpy as np, json
from fractions import Fraction
import flint
from ys_space import load_A, S_PLUS

NPZ = (r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
       r"\20261027-h-cat56-2-discovery\metrics\s14_povm_prefix12.npz")
V = np.load(NPZ)["vectors"]
SCALE = 2 ** 40
DATA = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
rec = json.loads(open(DATA, encoding="utf-8").readline())

def dy(v):  # dyadic rational from float
    return Fraction(round(float(v) * SCALE), SCALE)

X_exact, labels = [], []
for k in range(V.shape[0]):
    x = V[k, :2].astype(complex)
    ph = x[0] / abs(x[0]) if abs(x[0]) > 0 else 1
    x = x * np.conj(ph)               # x0 real positive
    if abs(x[1].imag) < 1e-7:         # structural real-circle point
        x = np.array([x[0].real, x[1].real + 0j])
        labels.append("real")
    else:
        labels.append("generic")
    X_exact.append((dy(x[0].real), dy(x[0].imag), dy(x[1].real), dy(x[1].imag)))
json.dump({"labels": labels, "x_exact": [[str(q) for q in t] for t in X_exact]},
          open("../logs/exact_dirs.json", "w"))
print("labels:", {l: labels.count(l) for l in set(labels)})
