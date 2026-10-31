"""Composite generators i(A_i s A_j^H - A_j s A_i^H), i<j in S, s in {1, X, Y, Z}: rows vs numerical rank.
Target dimension: traceless Hermitian 20x20 = 399 (the 'rank 399' of the ledger)."""
import sys
import numpy as np
BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
sys.path.insert(0, BASE + r"\20261027-h-cat56-2-discovery\code")
import s8_admissible_span as sa
As = sa.load_A(BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl")
print("traceless Hermitian 20x20 dim =", 20 * 20 - 1, " Hermitian 20x20 dim =", 20 * 20)
for name, S in [("S+ {0..11}", range(0, 12)), ("S- {4..15}", range(4, 16)), ("all 16", range(0, 16))]:
    r, n = sa.kk_rank(As, list(S))
    print(f"{name}: rows={n} (= pairs*4), numerical rank={r}")
# trace of the generators (is the identity direction present?)
import itertools
sig = [np.eye(2, dtype=complex), np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]], dtype=complex), np.array([[1, 0], [0, -1]], dtype=complex)]
tr = []
for i, j in itertools.combinations(range(16), 2):
    for s in sig:
        W = 1j * (As[i] @ s @ As[j].conj().T - As[j] @ s @ As[i].conj().T)
        tr.append(abs(np.trace(W)))
print("max |trace| of any generator =", max(tr))
