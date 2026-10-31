"""Rigorous ball-arithmetic (python-flint arb, 192 bit) re-evaluation of the S- cell bound for chosen cells.

For each cell (th_lo, th_hi, ph_lo, ph_hi) (doubles taken as exact numbers) it computes a RIGOROUS upper bound B_up of
    B = max(lam_K,0) + 2 ||M Z|| rho + ||M|| rho^2,  rho = kappa_K/(1-kappa),
with the exact (not approximated) centre u0, exact Phi0 = sum u0_j Phi_j, exact pseudo-inverse, exact orthonormal kernel basis Z
(modified Gram-Schmidt of P*Zf in ball arithmetic), and
  kappa   = du * sqrt(sum_j ||A_j||^2),     A_j = Phi0^+ Phi_j
  kappa_K = du * sqrt(sum_j ||A_j Z||^2),
  lam_K   = lambda_max(Z^T M Z), ||M Z||^2 = lambda_max(Z^T M^2 Z), ||M|| = max(lam_max(M), lam_max(-M)).
Upper bounds of lambda_max of a symmetric matrix B: approximate eigenvectors V (float64 eigh), then Gershgorin on V^{-1} B V in ball
arithmetic (similarity invariance; V^{-1} is a rigorous ball inverse). All inputs (instance integers, R doubles, cell edges) are exact.
du = 0.5*h_th + sin(th_hi/2)*h_ph + 1e-12 (the 1e-12 also covers the 1e-16 slivers where float pi < pi at the poles/seam).
The cell lemma itself (perturbation inequality) is NOT proved by this script; it only removes floating-point error from the arithmetic.

Usage: python -I interval_cells.py <leaves.npz | --test K> <out.json>
"""

import json
import math
import sys
import time

import numpy as np
from flint import arb, arb_mat, ctx

ctx.prec = 192
BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
RPATH = (
    BASE
    + r"\20261028-h-cat56-2-phase3\metrics\inputs\s14_R_4-5-6-7-8-9-10-11-12-13-14-15_nx250.npz"
)
sys.path.insert(0, BASE + r"\20261027-h-cat56-2-discovery\code")
import s8_admissible_span as sa  # noqa: E402

S = list(range(4, 16))
As = sa.load_A(INST)
R = np.load(RPATH)["R"]
R = 0.5 * (R + R.conj().T)
Mf = np.block([[R.real, -R.imag], [R.imag, R.real]])
Mf = 0.5 * (Mf + Mf.T)
FRAC = 0.9
trR_f = float(np.trace(R).real)
s_target_f = FRAC * trR_f / 20.0  # same float ops as the certificate
BX = [np.array(v, complex) for v in ([1, 0], [1j, 0], [0, 1], [0, 1j])]
PHIf = np.array([sa.phi_rows(As, S, x) for x in BX])  # 4 x 36 x 40 (exact integers in doubles)


def to_arb_mat(a):
    r, c = a.shape
    return arb_mat(r, c, [arb(float(v)) for v in a.flatten()])


PHI = [to_arb_mat(PHIf[j]) for j in range(4)]
Mb = to_arb_mat(Mf)
M2 = Mb * Mb
I40 = arb_mat(40, 40, [1 if i == j else 0 for i in range(40) for j in range(40)])
tr_exact = sum((arb(float(R[i, i].real)) for i in range(20)), arb(0))
s_target = arb(s_target_f)
final_gap = tr_exact - 20 * s_target  # must be > 0 for the Phase-3 criterion


def np_of(B):
    n, m = B.nrows(), B.ncols()
    return np.array([[float(B[i, j].mid()) for j in range(m)] for i in range(n)])


def lam_max_upper(B):
    """Rigorous upper bound (an exact arb number) for lambda_max of the symmetric matrix B (arb_mat, n x n)."""
    n = B.nrows()
    Bf = np_of(B)
    Bf = 0.5 * (Bf + Bf.T)
    _, V = np.linalg.eigh(Bf)
    Vb = to_arb_mat(V)
    C = Vb.inv() * B * Vb
    best = None
    for i in range(n):
        up = (C[i, i] + sum((abs(C[i, j]) for j in range(n) if j != i), arb(0))).upper()
        if best is None or float(up) > float(best):
            best = up
    return best


mn_up = max(lam_max_upper(Mb), lam_max_upper(-1 * Mb), key=lambda t: float(t))


def cell_bound(cell):
    th_lo, th_hi, ph_lo, ph_hi = (float(v) for v in cell)
    a_tl, a_th, a_pl, a_ph = arb(th_lo), arb(th_hi), arb(ph_lo), arb(ph_hi)
    th_c, ph_c = (a_tl + a_th) / 2, (a_pl + a_ph) / 2
    hth, hph = (a_th - a_tl) / 2, (a_ph - a_pl) / 2
    du = (hth / 2 + (a_th / 2).sin() * hph + arb(1e-12)).upper()
    u0 = [(th_c / 2).cos(), arb(0), (th_c / 2).sin() * ph_c.cos(), (th_c / 2).sin() * ph_c.sin()]
    Phi0 = PHI[0] * u0[0]
    for j in range(1, 4):
        Phi0 = Phi0 + PHI[j] * u0[j]
    G = Phi0 * Phi0.transpose()
    Pinv = Phi0.transpose() * G.inv()  # 40 x 36
    P = I40 - Pinv * Phi0
    u0f = [float(t.mid()) for t in u0]
    Phi0f = sum(u0f[j] * PHIf[j] for j in range(4))
    _, _, Vt = np.linalg.svd(Phi0f)
    Zf = to_arb_mat(Vt[36:].T)
    Z1 = P * Zf
    cols = [[Z1[i, k] for i in range(40)] for k in range(4)]
    Q = []
    for k in range(4):
        v = cols[k][:]
        for q in Q:
            d = sum((q[i] * v[i] for i in range(40)), arb(0))
            v = [v[i] - d * q[i] for i in range(40)]
        nrm = sum((x * x for x in v), arb(0)).sqrt()
        Q.append([x / nrm for x in v])
    Z0 = arb_mat(40, 4, [Q[k][i] for i in range(40) for k in range(4)])
    Z0t = Z0.transpose()
    A = [Pinv * PHI[j] for j in range(4)]  # 40 x 40
    t_full = [lam_max_upper(A[j].transpose() * A[j]) for j in range(4)]
    t_K = []
    for j in range(4):
        X = A[j] * Z0
        t_K.append(lam_max_upper(X.transpose() * X))
    kappa = (du * sum((t for t in t_full), arb(0)).sqrt()).upper()
    kappa_K = (du * sum((t for t in t_K), arb(0)).sqrt()).upper()
    lam_h = lam_max_upper(Z0t * Mb * Z0)
    # WHY: the test must use the UPPER bound of lambda_K, not its midpoint; max(lambda_K, 0) <= max(upper, 0)
    lam_up = lam_h.upper()
    lamK = lam_up if float(lam_up) > 0 else arb(0)
    mz = lam_max_upper(Z0t * M2 * Z0).sqrt().upper()
    one_minus = arb(1) - kappa
    if not (one_minus > 0):
        return None
    rho = (kappa_K / one_minus).upper()
    B = (lamK + 2 * mz * rho + mn_up * rho * rho).upper()
    return {"B_up": B, "kappa": kappa, "rho": rho, "lamK": lamK, "mz": mz}


def float_bound(cell):
    """Plain numpy replica of the certificate formulas without margins (cross-check of the formulas themselves)."""
    th_lo, th_hi, ph_lo, ph_hi = cell
    th_c, ph_c = 0.5 * (th_lo + th_hi), 0.5 * (ph_lo + ph_hi)
    hth, hph = 0.5 * (th_hi - th_lo), 0.5 * (ph_hi - ph_lo)
    du = 0.5 * hth + math.sin(min(th_hi, math.pi) / 2) * hph + 1e-12
    u0 = np.array(
        [
            math.cos(th_c / 2),
            0,
            math.sin(th_c / 2) * math.cos(ph_c),
            math.sin(th_c / 2) * math.sin(ph_c),
        ]
    )
    Phi0 = np.tensordot(u0, PHIf, axes=1)
    U, s, Vt = np.linalg.svd(Phi0)
    Pinv = np.linalg.pinv(Phi0)
    Z = Vt[36:].T
    Aj = [Pinv @ PHIf[j] for j in range(4)]
    kappa = du * math.sqrt(sum(np.linalg.norm(a, 2) ** 2 for a in Aj))
    kK = du * math.sqrt(sum(np.linalg.norm(a @ Z, 2) ** 2 for a in Aj))
    lamK = max(np.linalg.eigvalsh(Z.T @ Mf @ Z)[-1], 0.0)
    mz = np.linalg.norm(Mf @ Z, 2)
    mn = np.linalg.norm(Mf, 2)
    rho = kK / (1 - kappa)
    return lamK + 2 * mz * rho + mn * rho**2, kappa, rho


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    if src == "--test":
        K = int(sys.argv[3])
        rng = np.random.default_rng(5)
        cells, stored = [], [None] * K
        for _ in range(K):
            th = math.acos(rng.uniform(-1, 1))
            ph = rng.uniform(0, 2 * math.pi)
            h = 10 ** rng.uniform(-3.8, -3.0)
            cells.append([max(th - h, 0), min(th + h, math.pi), ph - h, ph + h])
        depths = [None] * K
    else:
        d = np.load(src)
        cells = d["top_cells"].tolist()
        stored = d["top_bound"].tolist()
        depths = d["top_depth"].tolist()
        if "--samples" in sys.argv:
            cells += d["samp_cells"].tolist()
            stored += d["samp_bound"].tolist()
            depths += d["samp_depth"].tolist()
    print(
        "trR exact",
        tr_exact,
        " s_target",
        s_target_f,
        " final gap trR-20s:",
        final_gap,
        " ||M||_up",
        float(mn_up),
        flush=True,
    )
    rows = []
    t0 = time.time()
    for k, c in enumerate(cells):
        t1 = time.time()
        r = cell_bound(c)
        fb = float_bound(c)
        if r is None:
            rows.append({"cell": c, "depth": depths[k], "status": "kappa>=1"})
            continue
        slack = s_target - r["B_up"]
        rows.append(
            {
                "cell": c,
                "depth": depths[k],
                "B_up": float(r["B_up"]),
                "slack_certain_positive": bool(slack > 0),
                "slack": float(slack),
                "stored_float_bound": stored[k],
                "numpy_replica_bound": float(fb[0]),
                "kappa": float(r["kappa"]),
                "rho": float(r["rho"]),
                "sec": round(time.time() - t1, 2),
            }
        )
        if k < 5 or k % 100 == 0:
            print(
                k,
                {
                    kk: rows[-1][kk]
                    for kk in (
                        "B_up",
                        "slack",
                        "stored_float_bound",
                        "numpy_replica_bound",
                        "kappa",
                        "sec",
                    )
                    if kk in rows[-1]
                },
                flush=True,
            )
    ok = [r for r in rows if r.get("slack_certain_positive")]
    summ = {
        "cells": len(rows),
        "certified_rigorous": len(ok),
        "not_certified": len(rows) - len(ok),
        "final_gap_trR_minus_20s_positive": bool(final_gap > 0),
        "final_gap": float(final_gap),
        "min_slack": min((r["slack"] for r in ok), default=None),
        "max_rel_diff_vs_numpy_replica": max(
            (
                abs(r["B_up"] - r["numpy_replica_bound"]) / r["numpy_replica_bound"]
                for r in ok
                if r["numpy_replica_bound"] > 0
            ),
            default=None,
        ),
        "max_stored_minus_Bup_rel": max(
            (
                (r["stored_float_bound"] - r["B_up"]) / r["B_up"]
                for r in ok
                if r["stored_float_bound"] is not None
            ),
            default=None,
        ),
        "min_stored_minus_Bup_rel": min(
            (
                (r["stored_float_bound"] - r["B_up"]) / r["B_up"]
                for r in ok
                if r["stored_float_bound"] is not None
            ),
            default=None,
        ),
        "seconds": round(time.time() - t0, 1),
        "prec_bits": ctx.prec,
    }
    print(json.dumps(summ, indent=1))
    json.dump({"summary": summ, "rows": rows}, open(out, "w"), indent=1)
