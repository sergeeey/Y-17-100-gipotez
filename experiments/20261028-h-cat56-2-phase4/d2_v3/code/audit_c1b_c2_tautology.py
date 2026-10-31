"""Audit of d2_v3_checks.py C1b / C2 (skeptic, 2026-10-30). NOT executed by the auditor (no shell).

Claim under audit: log line "C1b ... min eig 0.00e+00" is a measured machine zero.
Suspicion: worst_psd is initialised to 0.0 and updated with min(); R = Rr = 0.05 * X X^H is
full rank by construction, so the true minimum eigenvalue is strictly positive and the printed 0
is the initial value. Also: C2 does not use A at all and T1 = T2 = mu^2 tr(QP) identically.

Run: python -I audit_c1b_c2_tautology.py
Expected if the suspicion holds: true_min_eig_R > 0 (order 1e-3..1e-1); C2 diff == 0 for any P, mu.
"""

import numpy as np
from scipy.linalg import sqrtm

rng = np.random.default_rng(20261030)
Q = np.diag([1 / 3, 2 / 3]).astype(complex)


def herm_psd(n, rank=None):
    r = n if rank is None else rank
    X = rng.normal(size=(n, r)) + 1j * rng.normal(size=(n, r))
    return X @ X.conj().T


true_min = np.inf
for kind in ["P_full", "P_rank1"]:
    for _ in range(60):
        P = herm_psd(2) + 0.2 * np.eye(2) if kind == "P_full" else herm_psd(2, rank=1)
        Ph = sqrtm(P)
        Pi = P @ np.linalg.pinv(P)
        Z = Pi @ (rng.normal(size=(2, 20)) + 1j * rng.normal(size=(2, 20)))
        B = Ph @ Z
        D = Z.conj().T @ Z + 0.05 * herm_psd(20)
        R = D - B.conj().T @ np.linalg.pinv(P) @ B
        true_min = min(true_min, np.min(np.linalg.eigvalsh((R + R.conj().T) / 2)))
print(f"C1b true min eig(R) without the 0.0 initialisation: {true_min:.3e}")

# C2 tautology: T1 - T2 = mu^2 tr(QP) - mu^2 tr(QP) for ANY P > 0, ANY real mu, no A involved.
worst = 0.0
for _ in range(1000):
    P = herm_psd(2) + 0.01 * np.eye(2)
    mu = rng.normal() * 10
    c = mu * P @ Q
    T1 = np.real(np.trace(np.linalg.inv(P) @ c @ np.linalg.inv(Q) @ c.conj().T))
    T2 = np.real(np.trace(c)) ** 2 / np.real(np.trace(Q @ P))
    worst = max(worst, abs(T1 - T2) / max(1.0, T1))
print(f"C2 bracket over 1000 random (P, mu), A unused: max rel {worst:.2e} (identity, not a test)")

# Necessity direction (what Lemma 2 actually uses): near-equality must force c ~ mu P Q.
# Perturb c = mu P Q + eps * G; bracket should grow like eps^2 unless G is itself of the form
# real * P Q. Prints bracket / eps^2 for a random complex G (should be bounded away from 0).
P = herm_psd(2) + 0.2 * np.eye(2)
G = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
for eps in [1e-1, 1e-2, 1e-3]:
    c = 0.7 * P @ Q + eps * G
    T1 = np.real(np.trace(np.linalg.inv(P) @ c @ np.linalg.inv(Q) @ c.conj().T))
    T2 = np.real(np.trace(c)) ** 2 / np.real(np.trace(Q @ P))
    print(f"necessity probe eps={eps:.0e}: bracket/eps^2 = {(T1 - T2) / eps**2:.4f}")
