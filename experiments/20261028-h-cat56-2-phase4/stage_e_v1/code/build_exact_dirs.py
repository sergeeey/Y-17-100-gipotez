# WHY: build EXACT dyadic directions from the candidate (phase fixed by the LARGER component, real-snap for
# structural real points), then exact kernels.  Output: exact kernel dims and float bases for the SDP.
import json, pickle
from fractions import Fraction
import numpy as np
from exact_kernel import exact_kernel
NPZ = (r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
       r"\20261027-h-cat56-2-discovery\metrics\s14_povm_prefix12.npz")
V = np.load(NPZ)["vectors"]
SC = 2 ** 40
def dy(v): return Fraction(round(float(v) * SC), SC)
dirs, labels, dims, bases = [], [], [], []
for k in range(V.shape[0]):
    x = V[k, :2].astype(complex)
    big = 0 if abs(x[0]) >= abs(x[1]) else 1
    ph = x[big] / abs(x[big])
    x = x * np.conj(ph)           # larger component now real positive
    rel_imag_small = abs(x[1 - big].imag) < 1e-7 * np.linalg.norm(x)
    if big == 0:
        x0 = (dy(x[0].real), Fraction(0))
        x1 = (dy(x[1].real), Fraction(0)) if rel_imag_small else (dy(x[1].real), dy(x[1].imag))
    else:
        x1 = (dy(x[1].real), Fraction(0))
        x0 = (dy(x[0].real), Fraction(0)) if rel_imag_small else (dy(x[0].real), dy(x[0].imag))
    rank, basis = exact_kernel((x0, x1))
    dirs.append(((str(x0[0]), str(x0[1])), (str(x1[0]), str(x1[1]))))
    labels.append("real" if rel_imag_small else "generic")
    dims.append(len(basis))
    # complex basis: y = p + i q, p = v[:20], q = v[20:]
    bases.append([[complex(float(v[r]), float(v[20 + r])) for r in range(20)] for v in basis])
vals, cnt = np.unique(dims, return_counts=True)
print("exact kernel dims:", dict(zip(vals.tolist(), cnt.tolist())))
print("labels:", {l: labels.count(l) for l in set(labels)})
print("dims by label:", {l: {d: sum(1 for a, b in zip(labels, dims) if a == l and b == d) for d in set(dims)} for l in set(labels)})
pickle.dump({"dirs": dirs, "labels": labels, "dims": dims, "bases": bases}, open("../logs/exact_dirs.pkl", "wb"))
json.dump({"dirs": dirs, "labels": labels, "dims": dims}, open("../logs/exact_dirs.json", "w"))
