"""Stage C, route 2: cell-wise rigorous bound for the Phase-3 separation inequality on S-.

Claim to certify:  for every unit x in C^2 and every unit y in Y_S(x) = ker Phi_x,   y^dag R y <= s_cell <= s_target,
with s_target < tr R / 20.  Then  tr R - 20 s_target > 0  and I_20 is not in cone{y y^dag : y in Y_S}  (Phase-3 criterion).

Phi_x is REAL-LINEAR in u = (Re x0, Im x0, Re x1, Im x1):  Phi(u) = sum_j u_j Phi_j  (exact; Phi_j = phi_rows at basis vectors).
For a cell with centre u0 and any u in the cell, Delta = u - u0:
    delta := ||Phi(Delta)||_2 <= L_phi * ||Delta||,   L_phi = sqrt(sum_j ||Phi_j||_2^2)     (Cauchy-Schwarz)
    sigma := 36th singular value of Phi(u0)  (36 rows, so ker Phi(u0) has dimension exactly 4 when sigma > 0)
If eps := delta/sigma < 1: any unit y in ker Phi(u) satisfies Phi(u0) y = -Phi(Delta) y, so ||Q y|| <= eps (Q = projector onto
the row space of Phi(u0)); with P the projector onto K = ker Phi(u0), a = ||P y|| <= 1, b = ||Q y|| <= eps:
    y^T M y <= max(lam_K, 0) + 2 eps ||M Z_K|| + eps^2 ||M||,    lam_K = lambda_max(Z_K^T M Z_K),  M = real form of R.
Cells that fail are bisected in (theta, phi) until max depth.  Floating-point error is covered by explicit safety margins
(MARGIN_*), not by interval arithmetic: label [VERIFIED-float-with-margin].

Bloch parametrisation x = (cos(theta/2), sin(theta/2) e^{i phi}); speed bound: ||Delta u|| <= (1/2) dtheta + (1/2) sin(theta_hi/2) dphi
along a coordinate path inside the rectangle (half-widths), theta_hi <= pi.

Usage: python -I c3_cell_certificate.py <instance.jsonl> <R.npz> <s_target_frac> <n_theta0> <n_phi0> <max_depth> <out.json> [subset]
       subset = S- (default) | S+ | csv
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

MARGIN_REL = float(os.environ.get("MARGIN_REL", "1e-8"))  # relative safety margin (float64 error is ~1e-13)
MARGIN_ABS = 1e-10
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
As = sa.load_A(path)
R = np.load(r_path)["R"]
R = 0.5 * (R + R.conj().T)  # exact Hermitian float matrix used as THE certificate matrix
M = np.block([[R.real, -R.imag], [R.imag, R.real]])
M = 0.5 * (M + M.T)
m_norm = float(np.linalg.norm(M, 2)) * (1 + MARGIN_REL) + MARGIN_ABS
tr_R = float(np.trace(R).real)
s_target = frac * tr_R / 20.0
PHI = np.array([sa.phi_rows(As, S, x) for x in BASIS_X])  # 4 x r x 40
L_phi = math.sqrt(sum(float(np.linalg.norm(PHI[j], 2)) ** 2 for j in range(4))) * (1 + MARGIN_REL)
n_rows = PHI.shape[1]

# sanity: real-linearity of Phi in u (exact identity), checked on random x
rng = np.random.default_rng(3)
dev = 0.0
for _ in range(20):
    x = rng.normal(size=2) + 1j * rng.normal(size=2)
    u = np.array([x[0].real, x[0].imag, x[1].real, x[1].imag])
    dev = max(dev, float(np.abs(np.tensordot(u, PHI, axes=1) - sa.phi_rows(As, S, x)).max()))
print(
    f"{which}: rows={n_rows}, L_phi={L_phi:.4f}, ||M||={m_norm:.5f}, trR={tr_R:.5f}, s_target={s_target:.6f}, lin_dev={dev:.2e}",
    flush=True,
)
assert dev < 1e-9


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
    """Adapted-norm perturbation: w = -Phi0^+ Phi(Delta) (z + w)  =>  |w| <= kappa_K/(1-kappa) |z|."""
    th_c = 0.5 * (cells[:, 0] + cells[:, 1])
    ph_c = 0.5 * (cells[:, 2] + cells[:, 3])
    hth = 0.5 * (cells[:, 1] - cells[:, 0])
    hph = 0.5 * (cells[:, 3] - cells[:, 2])
    du = 0.5 * hth + np.sin(np.minimum(cells[:, 1], math.pi) / 2) * hph + 1e-12  # WHY: |du/dphi| = sin(theta/2) (not half of it); found by blind audit
    u0 = x_of(th_c, ph_c)
    Phi0 = np.tensordot(u0, PHI, axes=([1], [0]))  # n x r x 40
    U, s, Vt = np.linalg.svd(Phi0, full_matrices=True)
    sigma = s[:, n_rows - 1] * (1 - MARGIN_REL) - MARGIN_ABS
    Vr = np.swapaxes(Vt[:, :n_rows, :], 1, 2)  # n x 40 x r
    Pinv = np.einsum("nir,nr,nkr->nik", Vr, 1.0 / np.maximum(s[:, :n_rows], 1e-300), U)  # n x 40 x r (U is r x r)
    ZK = np.swapaxes(Vt[:, n_rows:, :], 1, 2)  # n x 40 x k
    A = np.einsum("nir,jrk->njik", Pinv, PHI)  # n x 4 x 40 x 40
    kappa = du * np.sqrt(np.sum(np.linalg.norm(A, ord=2, axis=(2, 3)) ** 2, axis=1)) * (1 + MARGIN_REL)
    AZ = np.einsum("njik,nkl->njil", A, ZK)
    kappa_K = du * np.sqrt(np.sum(np.linalg.norm(AZ, ord=2, axis=(2, 3)) ** 2, axis=1)) * (1 + MARGIN_REL)
    MZ = np.einsum("ab,nbk->nak", M, ZK)
    G = np.einsum("nak,nal->nkl", ZK, MZ)
    lamK = np.linalg.eigvalsh(0.5 * (G + np.swapaxes(G, 1, 2)))[:, -1] + MARGIN_ABS + MARGIN_REL * m_norm
    mz = np.linalg.norm(MZ, ord=2, axis=(1, 2)) * (1 + MARGIN_REL) + MARGIN_ABS
    ok_gap = (kappa < 1.0) & (sigma > 0)
    rho = np.where(ok_gap, kappa_K / np.maximum(1.0 - kappa, 1e-300), np.inf)
    bound = np.where(ok_gap, np.maximum(lamK, 0.0) + 2 * mz * rho + m_norm * rho**2, np.inf)
    return bound, sigma, rho, bound <= s_target, lamK


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
worst_bound = 0.0
min_sigma = np.inf
n_cert = 0
BATCH = 1000
for depth in range(max_depth + 1):
    fails = []
    for k in range(0, len(cells), BATCH):
        sub = cells[k : k + BATCH]
        bound, sigma, eps, ok, lamK = process(sub)
        n_cert += int(ok.sum())
        if ok.any():
            worst_bound = max(worst_bound, float(bound[ok].max()))
            min_sigma = min(min_sigma, float(sigma[ok].min()))
        fails.append(sub[~ok])
    fails = np.concatenate(fails) if fails else np.zeros((0, 4))
    stats.append(
        {
            "depth": depth,
            "cells": int(len(cells)),
            "failed": int(len(fails)),
            "elapsed_s": time.time() - t0,
        }
    )
    print(stats[-1], flush=True)
    if len(fails) == 0:
        break
    if depth == max_depth:
        break
    cells = split(fails)
    if len(cells) > 4_000_000:
        print("cell budget exceeded; stopping", flush=True)
        break

uncert = int(len(fails))
area = float(np.sum((fails[:, 1] - fails[:, 0]) * (fails[:, 3] - fails[:, 2]))) if uncert else 0.0
res = {
    "set": which,
    "instance": path,
    "s_target": s_target,
    "s_target_frac_of_trR_over_20": frac,
    "tr_R": tr_R,
    "tr_R_minus_20_s_target": tr_R - 20 * s_target,
    "L_phi": L_phi,
    "norm_M": m_norm,
    "worst_certified_cell_bound": worst_bound,
    "min_sigma_certified": None if not np.isfinite(min_sigma) else min_sigma,
    "cells_certified": n_cert,
    "cells_uncertified": uncert,
    "uncertified_area_theta_phi": area,
    "levels": stats,
    "margins": {"rel": MARGIN_REL, "abs": MARGIN_ABS},
    "verdict": "CERTIFIED_all_cells" if uncert == 0 else "NOT_CERTIFIED",
}
if uncert:
    res["uncertified_sample"] = fails[:20].tolist()
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "levels"}, indent=1))
