"""Partial commutativity of the SLDs at theta=0 for subsets S+ = 0..11, S- = 4..15 and all 16 blocks.

Model at theta=0: rho0 = Q (+) 0 on C^2 (+) C^20, Q = diag(1/3, 2/3);
SLD (verified in checks/fu_normalization_and_Y_2026-10-31.py):  L_a = [[0, A_a^H], [A_a, L_kk]].
Support block of the product: (L_a L_b)_ss = A_a^H A_b.
Single-copy necessary condition (partial commutativity): P [L_a, L_b] P = 0
   <=> A_a^H A_b - A_b^H A_a = 0  (2x2).
Weak commutativity (asymptotic classicality): tr(rho [L_a, L_b]) = tr(Q (A_a^H A_b - A_b^H A_a)) = 0.
"""
import itertools
import sys

import numpy as np

BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
sys.path.insert(0, BASE + r"\20261027-h-cat56-2-discovery\code")
import s8_admissible_span as sa  # noqa: E402

INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
As = sa.load_A(INST)
Q = np.diag([1 / 3, 2 / 3])


def stats(S, name):
    worst_pc = 0.0
    worst_w = 0.0
    nviol = 0
    pairs = list(itertools.combinations(S, 2))
    for a, b in pairs:
        M = As[a].conj().T @ As[b]
        C = M - M.conj().T
        pc = float(np.abs(C).max())
        w = float(abs(np.trace(Q @ C)))
        worst_pc = max(worst_pc, pc)
        worst_w = max(worst_w, w)
        if pc > 1e-9:
            nviol += 1
    print(f"{name}: pairs={len(pairs)}  max|P[L_a,L_b]P|={worst_pc:.3e}  violating pairs (>1e-9)={nviol}  max|tr(rho[L_a,L_b])|={worst_w:.3e}")
    return worst_pc


print("block shape", As[0].shape, "entries are", As[0].dtype)
stats(list(range(0, 12)), "S+ = {0..11}")
stats(list(range(4, 16)), "S- = {4..15}")
stats(list(range(0, 16)), "all 16")
# a few raw pairs
for a, b in [(0, 1), (4, 5), (14, 15), (0, 15)]:
    M = As[a].conj().T @ As[b]
    print((a, b), "A_a^H A_b =", np.round(M, 3).tolist())
