"""m2_subsets.py - consistency cross-check: H' (separator for S_minus) must NOT be nonnegative on Y_{S'} for the 12 eleven-subsets S' of S_minus,
because the package claims every proper subset is attainable (then A1 would be contradicted if H' were nonneg on Y_{S'}).  Own code, float64 scan.
usage: python -I m2_subsets.py PKGDIR"""

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

pkg = Path(sys.argv[1])
blob = json.loads((pkg / "canonical" / "blob_09f545d8.json").read_text())
A = []
for b in blob["blocks"]:
    b = np.array(b, dtype=float)
    A.append(b[:40].reshape(20, 2) + 1j * b[40:].reshape(20, 2))
h = json.loads((pkg / "branch_A" / "a2" / "H_rational.json").read_text())
Hr = np.array([[float(Fr(s)) for s in r] for r in h["Hr"]])
Hi = np.array([[float(Fr(s)) for s in r] for r in h["Hi"]])
Ht = np.block([[Hr, -Hi], [Hi, Hr]])
SM = list(range(4, 16))


def build(S):
    Adag = np.vstack([A[i].conj().T for i in S])
    m = Adag.shape[0]
    Ar = np.block([[Adag.real, -Adag.imag], [Adag.imag, Adag.real]])
    return Ar, m


def Lx(x, ns, m):
    L = np.zeros((2 * m, ns))
    for i in range(ns):
        for k in range(2):
            L[2 * i + k, i] = x[k].real
            L[m + 2 * i + k, i] = x[k].imag
    return L


def point(Ar, m, ns, x):
    M = np.hstack([Ar, -Lx(x, ns, m)])
    u, s, vt = np.linalg.svd(M)
    r = int((s > 1e-9 * s[0]).sum())
    K = vt[r:].T[:40]
    q, rr = np.linalg.qr(K)
    rk = int((np.abs(np.diag(rr)) > 1e-12).sum())
    Q = q[:, :rk]
    return np.linalg.eigvalsh(Q.T @ Ht @ Q)[0], rk


rng = np.random.default_rng(1)
print("subset removed | min over scan of lam_min(H' on fibre_S'(x)) | fibre dim range")
for j in SM:
    S = [i for i in SM if i != j]
    Ar, m = build(S)
    mn = 1e9
    dims = set()
    for ch in (1, 2):
        for r in np.linspace(0, 1, 41):
            for th in np.linspace(0, 2 * np.pi, 60, endpoint=False):
                z = r * np.exp(1j * th)
                x = np.array([1, z]) if ch == 1 else np.array([z, 1])
                lam, d = point(Ar, m, len(S), x)
                dims.add(d)
                mn = min(mn, lam)
    print(f"  {j:2d} | {mn:+.6f} | {sorted(dims)}")
