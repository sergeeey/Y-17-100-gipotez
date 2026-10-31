"""Diagnostics for c3b: size of each term of the cell bound at random Bloch points (S-), to see which term forces tiny cells."""

import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(
    0, os.path.normpath(os.path.join(HERE, "..", "..", "20261027-h-cat56-2-discovery", "code"))
)
import s8_admissible_span as sa  # noqa: E402

inst, rpath = sys.argv[1], sys.argv[2]
S = list(range(4, 16))
n = 12
As = sa.load_A(inst)
B = np.hstack([As[i] for i in S])
_, sv, Vh = np.linalg.svd(B)
N = Vh[20:].conj().T
Wm = np.linalg.solve(B @ B.conj().T, B)
R = np.load(rpath)["R"]
R = 0.5 * (R + R.conj().T)
M = np.block([[R.real, -R.imag], [R.imag, R.real]])
s = 0.9 * np.trace(R).real / 20
T = s * np.eye(40) - M
BX = [np.array(v, complex) for v in ([1, 0], [1j, 0], [0, 1], [0, 1j])]


def psi_b(xv):
    return np.array(
        [
            np.concatenate(
                [
                    (N[2 * i : 2 * i + 2].conj().T @ xv).real,
                    (N[2 * i : 2 * i + 2].conj().T @ xv).imag,
                ]
            )
            for i in range(n)
        ]
    ).T


def w_b(xv):
    return np.array(
        [
            np.concatenate(
                [(Wm[:, 2 * i : 2 * i + 2] @ xv).real, (Wm[:, 2 * i : 2 * i + 2] @ xv).imag]
            )
            for i in range(n)
        ]
    ).T


PSI = np.array([psi_b(x) for x in BX])
WB = np.array([w_b(x) for x in BX])
rng = np.random.default_rng(1)
print("theta phi | sigma8 |W0| smin(W0Z) smax(W0Z) mu(H0|K) | ratio g=maxeig(Z'W'MWZ)/(Z'W'WZ)")
for _ in range(12):
    th = math.acos(rng.uniform(-1, 1))
    ph = rng.uniform(0, 2 * math.pi)
    u = np.array(
        [math.cos(th / 2), 0, math.sin(th / 2) * math.cos(ph), math.sin(th / 2) * math.sin(ph)]
    )
    Psi = np.tensordot(u, PSI, axes=1)
    W = np.tensordot(u, WB, axes=1)
    _, sg, Vt = np.linalg.svd(Psi)
    Z = Vt[8:].T
    WZ = W @ Z
    sw = np.linalg.svd(WZ, compute_uv=False)
    H = Z.T @ W.T @ T @ W @ Z
    mu = np.linalg.eigvalsh(0.5 * (H + H.T))[0]
    E = WZ.T @ WZ
    Pm = WZ.T @ M @ WZ
    g = np.linalg.eigvals(np.linalg.solve(E, Pm)).real.max()
    print(
        f"{th:.2f} {ph:.2f} | {sg[7]:.4f} {np.linalg.norm(W, 2):.2f} {sw[-1]:.4f} {sw[0]:.3f} {mu:.4f} | {g:.5f}"
    )
