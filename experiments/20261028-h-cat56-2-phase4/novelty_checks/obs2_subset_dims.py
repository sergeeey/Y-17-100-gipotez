"""Dimension criterion of Yang-Imai-Pezze (arXiv:2601.21801, Observation 2) applied to S+, S- and all 16 blocks.

V = M (+) W as in TECHNICAL_NOTE_A0_EN_v1.2 section 5.4 (P-conv: L_{++} = 0, L_{+0} = A^H, L_{0+} = A, A = -2i B):
  M-family: sigma B_i^H  (2 x 20, off-diagonal blocks),   i in S, sigma in {I, X, Y, Z}
  W-family: i (B_l sigma B_m^H - B_m sigma B_l^H) (20 x 20 Hermitian, kernel block),  l < m in S
dim V = rank M + rank W,  dim V_perp = 484 - dim V;  Observation 2: dim V_perp < 22 excludes saturation.
Ranks: numerical (SVD) and exact modulo two primes (integer data), a lower bound on the rational rank for each prime.
"""

import itertools
import sys

import numpy as np

BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
sys.path.insert(0, BASE + r"\20261027-h-cat56-2-discovery\code")
import s8_admissible_span as sa  # noqa: E402

INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
As = sa.load_A(INST)
Bs = [1j * A / 2.0 for A in As]  # A = -2i B  =>  B = i A / 2
for B in Bs:
    assert np.allclose(B.real, np.round(B.real)) and np.allclose(B.imag, np.round(B.imag))
SIG = [np.eye(2), np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.diag([1, -1])]


def rank_mod(rows, p):
    """Rank of an integer matrix modulo the prime p (Gaussian elimination on Python ints)."""
    m = [[int(x) % p for x in r] for r in rows]
    rank, ncol = 0, len(m[0])
    for c in range(ncol):
        piv = next((i for i in range(rank, len(m)) if m[i][c]), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        inv = pow(m[rank][c], -1, p)
        m[rank] = [(x * inv) % p for x in m[rank]]
        for i in range(len(m)):
            if i != rank and m[i][c]:
                f = m[i][c]
                m[i] = [(a - f * b) % p for a, b in zip(m[i], m[rank])]
        rank += 1
    return rank


def to_row(Mx):
    return np.concatenate([np.round(Mx.real).ravel(), np.round(Mx.imag).ravel()]).astype(np.int64)


def dims(S):
    mrows, wrows = [], []
    for i in S:
        for s in SIG:
            mrows.append(to_row(s @ Bs[i].conj().T))
    for l, m in itertools.combinations(S, 2):
        for s in SIG:
            X = 1j * (Bs[l] @ s @ Bs[m].conj().T - Bs[m] @ s @ Bs[l].conj().T)
            assert np.allclose(X, X.conj().T)
            wrows.append(to_row(X))
    out = {}
    for name, rows in (("M", mrows), ("W", wrows)):
        arr = np.array(rows, dtype=float)
        sv = np.linalg.svd(arr, compute_uv=False)
        num = int((sv > 1e-9 * sv[0]).sum())
        gap = (sv[num - 1] / sv[num]) if num < len(sv) else float("inf")
        r1 = rank_mod(rows, (1 << 61) - 1)
        r2 = rank_mod(rows, 2147483629)
        out[name] = (len(rows), num, r1, r2, gap)
    return out


for name, S in (
    ("all 16", list(range(16))),
    ("S+ = 0..11", list(range(12))),
    ("S- = 4..15", list(range(4, 16))),
):
    d = dims(S)
    rm, rw = d["M"][1], d["W"][1]
    print(
        f"{name}: M rows {d['M'][0]} rank num/p1/p2 = {d['M'][1]}/{d['M'][2]}/{d['M'][3]};  "
        f"W rows {d['W'][0]} rank num/p1/p2 = {d['W'][1]}/{d['W'][2]}/{d['W'][3]} (sv gap {d['W'][4]:.2e})"
    )
    dimV = rm + rw
    print(
        f"   dim V = {dimV}, dim V_perp = {484 - dimV}, Observation 2 excludes saturation: {484 - dimV < 22}"
    )
