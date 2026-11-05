"""m1_scan.py - independent numeric falsification scan of the final inequality  y^H H' y >= 0  on the fibre Y_S.
Own code; reads only the blob and H_rational.json from the (untrusted) package.  usage: python -I m1_scan.py PKGDIR
Fibre(x) = { y in C^20 : exists real lam (12): A_i^H y = lam_i x }.  Real model: [Areal | -L(x)] (y,lam) = 0.
For each x on CP^1 (two charts, |z|<=1) take the y-projection of the null space, build min eigenvalue of H~ restricted to unit y."""

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

pkg = Path(sys.argv[1])
blob = json.loads((pkg / "canonical" / "blob_09f545d8.json").read_text())
S = list(range(4, 16))
A = []
for b in blob["blocks"]:
    b = np.array(b, dtype=float)
    A.append(b[:40].reshape(20, 2) + 1j * b[40:].reshape(20, 2))
assert all(
    np.all(np.abs(a.real - np.round(a.real)) == 0)
    and np.all(np.abs(a.imag - np.round(a.imag)) == 0)
    for a in A
)
Adag = np.vstack([A[i].conj().T for i in S])  # 24 x 20
Ar = np.block([[Adag.real, -Adag.imag], [Adag.imag, Adag.real]])  # 48 x 40
print(
    "Areal shape",
    Ar.shape,
    "rank",
    np.linalg.matrix_rank(Ar),
    "sv min/max",
    np.linalg.svd(Ar, compute_uv=False)[[-1, 0]],
)

h = json.loads((pkg / "branch_A" / "a2" / "H_rational.json").read_text())
Hr = np.array([[float(Fr(s)) for s in r] for r in h["Hr"]])
Hi = np.array([[float(Fr(s)) for s in r] for r in h["Hi"]])
H = Hr + 1j * Hi
print(
    "H herm err", np.abs(H - H.conj().T).max(), "trace", np.trace(H).real, "exact", h["trace_exact"]
)
Ht = np.block([[Hr, -Hi], [Hi, Hr]])


def Lx(x):
    xr, xi = np.real(x), np.imag(x)
    L = np.zeros((48, 12))
    for i in range(12):
        for k in range(2):
            L[2 * i + k, i] = xr[k]
            L[24 + 2 * i + k, i] = xi[k]
    return L


def point(x):
    """return (min eig of Ht on fibre(x) unit y, fibre dim, 8th sing value of B)"""
    M = np.hstack([Ar, -Lx(x)])  # 48 x 52
    u, s, vt = np.linalg.svd(M)
    tol = 1e-9 * s[0]
    r = int((s > tol).sum())
    K = vt[r:].T  # null space (52 x d)
    Y = K[:40]
    q, rr = np.linalg.qr(Y)
    rk = int((np.abs(np.diag(rr)) > 1e-12).sum())
    Q = q[:, :rk]
    w = np.linalg.eigvalsh(Q.T @ Ht @ Q)
    return w[0], rk, s[r - 1]


def xz(ch, a, b):
    z = a + 1j * b
    return np.array([1, z]) if ch == 1 else np.array([z, 1])


res = {}
for ch in (1, 2):
    best = (1e9, None)
    dims = {}
    sig = 1e9
    rs = np.concatenate([np.linspace(0, 1, 121)])
    for r in rs:
        for th in np.linspace(0, 2 * np.pi, 181 if r > 0 else 2, endpoint=False):
            lam, d, sg = point(xz(ch, r * np.cos(th), r * np.sin(th)))
            dims[d] = dims.get(d, 0) + 1
            sig = min(sig, sg)
            if lam < best[0]:
                best = (lam, (r, th))
    print(
        f"chart {ch}: grid min lam_min = {best[0]:.6g} at r,th = {best[1]}; fibre dims {dims}; min smallest-nonzero sv of [A|-L] = {sig:.3g}"
    )
    # local refinement
    f = lambda p: point(xz(ch, p[0], p[1]))[0] + 1e3 * max(0.0, np.hypot(p[0], p[1]) - 1) ** 2
    r0, t0 = best[1]
    p0 = np.array([r0 * np.cos(t0), r0 * np.sin(t0)])
    o = minimize(
        f, p0, method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-16, "maxiter": 2000}
    )
    print(
        f"   Nelder-Mead from best grid point: f = {o.fun:.8g} at z = {o.x}, |z| = {np.hypot(*o.x):.9f}"
    )
    res[ch] = (best[0], float(o.fun))
print("SUMMARY", res)
