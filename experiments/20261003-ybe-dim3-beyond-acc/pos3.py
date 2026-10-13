"""Positive control (dim 3, new det-normalised solver lm_det): start from noisy copies of every Table-1 family of 2310.03816
(+ identity, flip) and require convergence to a solution with the same L-class / dimL / spectrum multiplicities / tangent dim.
Serial, throttled-friendly."""
import numpy as np, collections
from ybe import *
from solver_mask import lm_det, flip
from classify3 import analyse, clean

def sig(R):
    a = analyse(R)
    td, _ = tangent_dim(clean(R), 3)
    return (a["label"], a["dimL"], a["mults"], a["geom"], td)

import sys
noise = float(sys.argv[1]); ntr = int(sys.argv[2])
fam = table1_families(np.random.default_rng(99))
fam["Id"] = np.eye(9, dtype=complex)
fam["flip"] = flip(3).astype(complex)
idx = np.arange(81)
tot = collections.Counter()
for nm, R in fam.items():
    Rn = clean(R)
    s0 = sig(Rn)
    res = []
    for t in range(ntr):
        rng = np.random.default_rng(1000 + t)
        R0 = Rn + noise * (rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9))) / np.sqrt(2)
        R0 = R0 * np.linalg.det(R0) ** (-1 / 9)
        Rf, f, it, why = lm_det(R0, idx, maxit=200, abort=False)
        if why != "ok":
            res.append("nc(%s)" % why); continue
        s1 = sig(Rf)
        res.append("same" if s1[:4] == s0[:4] else ("sameL" if s1[:2] == s0[:2] else "other"))
    c = collections.Counter(res)
    tot.update(c)
    print("%-26s %s | %s" % (nm, dict(c), s0), flush=True)
print("TOTAL", dict(tot))
