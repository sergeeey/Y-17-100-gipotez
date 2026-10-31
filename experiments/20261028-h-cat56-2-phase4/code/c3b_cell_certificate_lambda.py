"""Stage C, route 2b: cell-wise bound in WELL-CONDITIONED (lambda, x) variables.

Y_S(x) = { y : A_i^dag y = lambda_i x, lambda real }.  With B = [A_i]_{i in S} (20 x 2n, rank 20) and q = lambda (x) x:
    y = (B B^dag)^{-1} B q  =: W_x lambda   (real-linear in lambda, real-linear in u=(Re x0, Im x0, Re x1, Im x1)),
    admissibility  q in Ran B^dag  <=>  N^dag q = 0  (N spans ker B, 2n x (2n-20))  <=>  Psi(u) lambda = 0  (8 x 12 real for n=12).
y^dag R y <= s |y|^2 for all y in Y_S(x)  <=>  H(u) = W(u)^T T W(u) is PSD on K(u) = ker Psi(u),   T = s I - M,  M = real form of R.

Cell with centre u0 (|Delta u| <= du):  omega = |W(Delta)| <= L_W du,  delta = |Psi(Delta)| <= L_Psi du,  sigma = sigma_8(Psi(u0)),
eps = delta/sigma (<1).  For unit lambda in K(u):  |Q lambda| <= eps (Q onto row space of Psi(u0)), a^2 = 1 - b^2, b <= eps and
    lambda^T H(u) lambda >= mu (1-eps^2) - 2 h1 eps - h0 eps^2 - eta,
    mu = lambda_min(Z^T H0 Z), h1 = |H0 Z|, h0 = |H0|, eta = |T| (2 |W0| omega + omega^2)  (>= |H(u)-H0|).
Cell certified if the right side is > 0.  Floating-point error: explicit relative margins MARGIN (label VERIFIED-float-with-margin).

Usage: python -I c3b_cell_certificate_lambda.py <instance.jsonl> <R.npz> <s_target_frac> <n_theta0> <n_phi0> <max_depth> <out.json> [S-|S+|csv]
"""

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(
    0, os.path.normpath(os.path.join(HERE, "..", "..", "20261027-h-cat56-2-discovery", "code"))
)
import s8_admissible_span as sa  # noqa: E402

MARGIN = 1e-7
BASIS_X = [
    np.array([1, 0], complex),
    np.array([1j, 0], complex),
    np.array([0, 1], complex),
    np.array([0, 1j], complex),
]
path, r_path, frac, n_th0, n_ph0, max_depth, out_path = (
    sys.argv[1],
    sys.argv[2],
    float(sys.argv[3]),
    int(sys.argv[4]),
    int(sys.argv[5]),
    int(sys.argv[6]),
    sys.argv[7],
)
which = sys.argv[8] if len(sys.argv) > 8 else "S-"
S = (
    list(range(12))
    if which == "S+"
    else list(range(4, 16))
    if which == "S-"
    else [int(t) for t in which.split(",")]
)
n = len(S)
As = sa.load_A(path)
B = np.hstack([As[i] for i in S])  # 20 x 2n
R = np.load(r_path)["R"]
R = 0.5 * (R + R.conj().T)
M = np.block([[R.real, -R.imag], [R.imag, R.real]])
M = 0.5 * (M + M.T)
tr_R = float(np.trace(R).real)
s = frac * tr_R / 20.0
T = s * np.eye(40) - M
T_norm = float(np.linalg.norm(T, 2)) * (1 + MARGIN)

# null space of B and generalized inverse map
_, sv, Vh = np.linalg.svd(B)
N = Vh[20:].conj().T  # 2n x (2n-20)
nul_res = float(np.abs(B @ N).max())
BBd = B @ B.conj().T
Wm = np.linalg.solve(BBd, B)  # 20 x 2n complex
print(
    f"{which}: n={n} sv(B)=[{sv[0]:.3f},{sv[19]:.3f}] cond(BBd)={np.linalg.cond(BBd):.3e} |B N|={nul_res:.2e}",
    flush=True,
)


def psi_basis(xv):
    """Psi_j: 8 x n real matrix. Column i = [Re;Im] of N_i^dag x, N_i = rows (2i, 2i+1) of N."""
    cols = []
    for i in range(n):
        Ni = N[2 * i : 2 * i + 2, :]  # 2 x k
        v = Ni.conj().T @ xv  # k complex
        cols.append(np.concatenate([v.real, v.imag]))
    return np.array(cols).T


def w_basis(xv):
    """W_j: 40 x n real matrix. Column i = [Re;Im] of Wm[:, 2i:2i+2] @ xv."""
    cols = []
    for i in range(n):
        v = Wm[:, 2 * i : 2 * i + 2] @ xv
        cols.append(np.concatenate([v.real, v.imag]))
    return np.array(cols).T


PSI = np.array([psi_basis(x) for x in BASIS_X])  # 4 x 8 x n
WB = np.array([w_basis(x) for x in BASIS_X])  # 4 x 40 x n
L_psi = math.sqrt(sum(float(np.linalg.norm(PSI[j], 2)) ** 2 for j in range(4))) * (1 + MARGIN)
L_w = math.sqrt(sum(float(np.linalg.norm(WB[j], 2)) ** 2 for j in range(4))) * (1 + MARGIN)
k_rows = PSI.shape[1]

# sanity 1: Psi(u) lambda = 0  <=>  lambda (x) x in Ran B^dag ;  sanity 2: W(u) lambda solves B^dag y = lambda (x) x
rng = np.random.default_rng(5)
x = rng.normal(size=2) + 1j * rng.normal(size=2)
u = np.array([x[0].real, x[0].imag, x[1].real, x[1].imag])
Psi_u = np.tensordot(u, PSI, axes=1)
_, ps, pvt = np.linalg.svd(Psi_u)
Z = pvt[k_rows:].T
lam = Z @ rng.normal(size=Z.shape[1])
q = np.kron(lam, x)  # index 2i+a
y = Wm @ q
res_y = float(np.abs(B.conj().T @ y - q).max())
y2 = np.tensordot(u, WB, axes=1) @ lam
res_w = float(np.abs(np.concatenate([y.real, y.imag]) - y2).max())
print(
    f"L_psi={L_psi:.3f} L_w={L_w:.3f} |T|={T_norm:.4f} s={s:.6f} sanity: |B^dag y - q|={res_y:.2e}, |W-lin dev|={res_w:.2e}, sigma_k={ps[k_rows - 1]:.4f}",
    flush=True,
)
assert res_y < 1e-8 and res_w < 1e-8


def x_of(th, ph):
    return np.stack(
        [
            np.cos(th / 2),
            np.zeros_like(th),
            np.sin(th / 2) * np.cos(ph),
            np.sin(th / 2) * np.sin(ph),
        ],
        axis=-1,
    )


def process(cells):
    th_c = 0.5 * (cells[:, 0] + cells[:, 1])
    ph_c = 0.5 * (cells[:, 2] + cells[:, 3])
    hth = 0.5 * (cells[:, 1] - cells[:, 0])
    hph = 0.5 * (cells[:, 3] - cells[:, 2])
    du = 0.5 * hth + 0.5 * np.sin(np.minimum(cells[:, 1], math.pi) / 2) * hph + 1e-12
    u0 = x_of(th_c, ph_c)
    Psi0 = np.tensordot(u0, PSI, axes=([1], [0]))  # c x 8 x n
    W0 = np.tensordot(u0, WB, axes=([1], [0]))  # c x 40 x n
    _, sg, Vt = np.linalg.svd(Psi0, full_matrices=True)
    sigma = sg[:, k_rows - 1] * (1 - MARGIN)
    Z = np.swapaxes(Vt[:, k_rows:, :], 1, 2)  # c x n x kdim
    H0 = np.einsum("cai,ab,cbj->cij", W0, T, W0)
    H0 = 0.5 * (H0 + np.swapaxes(H0, 1, 2))
    HZ = np.einsum("cij,cjk->cik", H0, Z)
    G = np.einsum("cik,cil->ckl", Z, HZ)
    mu = np.linalg.eigvalsh(0.5 * (G + np.swapaxes(G, 1, 2)))[:, 0] * (1 - MARGIN) - 1e-12
    h1 = np.linalg.norm(HZ, ord=2, axis=(1, 2)) * (1 + MARGIN)
    h0 = np.linalg.norm(H0, ord=2, axis=(1, 2)) * (1 + MARGIN)
    w0 = np.linalg.norm(W0, ord=2, axis=(1, 2)) * (1 + MARGIN)
    omega = L_w * du
    eta = T_norm * (2 * w0 * omega + omega**2)
    eps = np.where(sigma > 0, L_psi * du / np.maximum(sigma, 1e-300), np.inf)
    lower = mu * (1 - eps**2) - 2 * h1 * eps - h0 * eps**2 - eta
    ok = (eps < 1.0) & (mu > 0) & (lower > 1e-12)
    return lower, sigma, eps, mu, ok


def split(cells):
    out = []
    for c in cells:
        tm = 0.5 * (c[0] + c[1])
        pm = 0.5 * (c[2] + c[3])
        out += [
            [c[0], tm, c[2], pm],
            [c[0], tm, pm, c[3]],
            [tm, c[1], c[2], pm],
            [tm, c[1], pm, c[3]],
        ]
    return np.array(out)


th_edges = np.linspace(0, math.pi, n_th0 + 1)
ph_edges = np.linspace(0, 2 * math.pi, n_ph0 + 1)
cells = np.array(
    [
        [th_edges[i], th_edges[i + 1], ph_edges[j], ph_edges[j + 1]]
        for i in range(n_th0)
        for j in range(n_ph0)
    ]
)
t0 = time.time()
stats = []
min_lower = np.inf
min_sigma = np.inf
min_mu = np.inf
n_cert = 0
fails = np.zeros((0, 4))
for depth in range(max_depth + 1):
    flist = []
    for k in range(0, len(cells), 4000):
        sub = cells[k : k + 4000]
        lower, sigma, eps, mu, ok = process(sub)
        n_cert += int(ok.sum())
        if ok.any():
            min_lower = min(min_lower, float(lower[ok].min()))
            min_sigma = min(min_sigma, float(sigma[ok].min()))
            min_mu = min(min_mu, float(mu[ok].min()))
        flist.append(sub[~ok])
    fails = np.concatenate(flist) if flist else np.zeros((0, 4))
    stats.append(
        {
            "depth": depth,
            "cells": int(len(cells)),
            "failed": int(len(fails)),
            "elapsed_s": round(time.time() - t0, 1),
        }
    )
    print(stats[-1], flush=True)
    if len(fails) == 0 or depth == max_depth:
        break
    cells = split(fails)
    if len(cells) > 3_000_000:
        print("cell budget exceeded; stopping", flush=True)
        break

uncert = int(len(fails))
area = float(np.sum((fails[:, 1] - fails[:, 0]) * (fails[:, 3] - fails[:, 2]))) if uncert else 0.0
res = {
    "set": which,
    "instance": path,
    "s_target": s,
    "frac_of_trR_over_20": frac,
    "tr_R": tr_R,
    "tr_R_minus_20_s": tr_R - 20 * s,
    "L_psi": L_psi,
    "L_w": L_w,
    "norm_T": T_norm,
    "min_lower_bound_certified_cells": None if not np.isfinite(min_lower) else min_lower,
    "min_sigma_certified": None if not np.isfinite(min_sigma) else min_sigma,
    "min_mu_certified": None if not np.isfinite(min_mu) else min_mu,
    "cells_certified": n_cert,
    "cells_uncertified": uncert,
    "uncertified_area_theta_phi": area,
    "levels": stats,
    "margin": MARGIN,
    "verdict": "CERTIFIED_all_cells" if uncert == 0 else "NOT_CERTIFIED",
}
if uncert:
    res["uncertified_sample"] = fails[:20].tolist()
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print(
    json.dumps(
        {k: v for k, v in res.items() if k not in ("levels", "uncertified_sample")}, indent=1
    )
)
