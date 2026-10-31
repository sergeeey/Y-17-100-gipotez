"""Exact (integer) check: is A_a^dag A_b Hermitian for all pairs? and 12x12 QFIM on S+/S- invertibility.
A = -2i (re + i im) with integer re, im, so A_a^dag A_b = 4 (re_a - i im_a)^T-like products: use Python ints via numpy object arrays.
"""

import json

import numpy as np

INST = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
rec = json.loads(open(INST, encoding="utf-8").readline())
G = []  # G = re + i im as (re_int, im_int) matrices 20x2
for flat in rec["blocks"]:
    re = np.array([[int(flat[2 * r + a]) for a in range(2)] for r in range(20)], dtype=object)
    im = np.array([[int(flat[40 + 2 * r + a]) for a in range(2)] for r in range(20)], dtype=object)
    assert all(float(flat[k]) == int(flat[k]) for k in range(80))
    G.append((re, im))

# A = -2i G, A_a^dag A_b = (2i G_a^dag)(-2i G_b) = 4 G_a^dag G_b.  G_a^dag G_b = (re_a^T - i im_a^T)(re_b + i im_b)
bad = 0
maxasym = 0
for a in range(16):
    for b in range(16):
        ra, ia = G[a]
        rb, ib = G[b]
        real = ra.T.dot(rb) + ia.T.dot(ib)
        imag = ra.T.dot(ib) - ia.T.dot(rb)
        # Hermitian: real symmetric, imag antisymmetric
        asym = max(
            max(abs(int(real[0, 1] - real[1, 0])), 0),
            abs(int(imag[0, 0])),
            abs(int(imag[1, 1])),
            abs(int(imag[0, 1] + imag[1, 0])),
        )
        maxasym = max(maxasym, asym)
        if asym != 0:
            bad += 1
print(
    "pairs (ordered, 256) with A_a^dag A_b NOT Hermitian:", bad, " max integer asymmetry:", maxasym
)

# QFIM_ij = Re tr(P A_i^dag A_j), P = diag(1/3, 2/3)
As = []
for re, im in G:
    As.append(-2j * (np.array(re, float) + 1j * np.array(im, float)))
P = np.diag([1 / 3, 2 / 3])
for name, S in (("S+", range(0, 12)), ("S-", range(4, 16)), ("all16", range(16))):
    S = list(S)
    F = np.array([[np.trace(P @ As[i].conj().T @ As[j]).real for j in S] for i in S])
    w = np.linalg.eigvalsh(0.5 * (F + F.T))
    print(name, "QFIM min/max eig", w[0], w[-1], "cond", w[-1] / w[0])
