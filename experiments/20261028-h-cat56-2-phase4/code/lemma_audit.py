"""Independent audit of the cell lemma used by c3d_cell_certificate_adapted.py (S-, MARGIN_REL = 1e-8 run).

Lemma (per cell, centre u0 = u(theta_c, phi_c), half-widths h_th, h_ph, du = h_th/2 + sin(th_hi/2) h_ph + 1e-12):
  L1 (radius)     sup over the leaf rectangle of |u(theta,phi) - u0| <= du.
  L2 (sphere)     every UNIT u with |u - u0| <= du (not only inside the rectangle) has
                  g(u) := lambda_max(Z_u^T M Z_u) <= B_up, where Z_u is an orthonormal basis of ker Phi(u).
  L3 (decomposition) for unit y in ker Phi(u): y = z + w, z in K = ker Phi(u0), w in rowspace Phi(u0),
                  |w| <= rho |z|, rho = kappa_K / (1 - kappa).
  L4 (sliver)     the points theta = pi (exact), phi in the leaf, lie within du of u0 (float pi < true pi).

B_up is the RIGOROUS arb upper bound from metrics/interval_top1000.json (192 bit). Here g(u) and all norms are float64,
so a comparison is meaningful only if the slack B_up - g_max is much larger than float64 error (~1e-14).
This is an audit by sampling: it can refute, not prove.

Usage: python -I lemma_audit.py <n_cells> <n_samples_per_cell> <out.json>
"""

import json
import math
import os
import sys

import numpy as np

BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
INST = os.path.join(
    BASE, "20261027-h-cat56-2-submission-package-v1", "data", "instance_d22_r2_s16.jsonl"
)
RPATH = os.path.join(
    BASE,
    "20261028-h-cat56-2-phase3",
    "metrics",
    "inputs",
    "s14_R_4-5-6-7-8-9-10-11-12-13-14-15_nx250.npz",
)
IVAL = os.path.join(BASE, "20261028-h-cat56-2-phase4", "metrics", "interval_top1000.json")
sys.path.insert(0, os.path.join(BASE, "20261027-h-cat56-2-discovery", "code"))
import s8_admissible_span as sa  # noqa: E402

N_CELLS = int(sys.argv[1])
N_SAMP = int(sys.argv[2])
OUT = sys.argv[3]
S = list(range(4, 16))
As = sa.load_A(INST)
R0 = np.load(RPATH)["R"]
R = 0.5 * (R0 + R0.conj().T)
M = np.block([[R.real, -R.imag], [R.imag, R.real]])
M = 0.5 * (M + M.T)
BX = [np.array(v, complex) for v in ([1, 0], [1j, 0], [0, 1], [0, 1j])]
PHI = np.array([sa.phi_rows(As, S, x) for x in BX])  # 4 x 36 x 40


def u_of(th, ph):
    return np.array(
        [math.cos(th / 2), 0.0, math.sin(th / 2) * math.cos(ph), math.sin(th / 2) * math.sin(ph)]
    )


def Phi_u(u):
    return np.tensordot(u, PHI, axes=1)


def kernel(u):
    _, s, Vt = np.linalg.svd(Phi_u(u))
    return Vt[36:].T, s[35]


def g_of(u):
    Z, _ = kernel(u)
    return float(np.linalg.eigvalsh(Z.T @ M @ Z)[-1])


def cell_consts(cell):
    th_lo, th_hi, ph_lo, ph_hi = cell
    thc, phc = 0.5 * (th_lo + th_hi), 0.5 * (ph_lo + ph_hi)
    hth, hph = 0.5 * (th_hi - th_lo), 0.5 * (ph_hi - ph_lo)
    du = 0.5 * hth + math.sin(min(th_hi, math.pi) / 2) * hph + 1e-12
    u0 = u_of(thc, phc)
    _, s, Vt = np.linalg.svd(Phi_u(u0))
    Z0 = Vt[36:].T
    Pinv = np.linalg.pinv(Phi_u(u0))
    A = [Pinv @ PHI[j] for j in range(4)]
    kappa = du * math.sqrt(sum(np.linalg.norm(a, 2) ** 2 for a in A))
    kK = du * math.sqrt(sum(np.linalg.norm(a @ Z0, 2) ** 2 for a in A))
    rho = kK / (1 - kappa) if kappa < 1 else float("inf")
    return {"du": du, "u0": u0, "sigma36": float(s[35]), "Z0": Z0, "rho": rho, "kappa": kappa}


def sample_sphere_ball(u0, du, n, rng):
    """Unit u on S^3 with chord |u - u0| <= du: u = cos t u0 + sin t v, v unit, u0-orthogonal, t <= 2 asin(du/2)."""
    tmax = 2 * math.asin(min(du / 2, 1.0))
    out = []
    for k in range(n):
        v = rng.normal(size=4)
        v -= (v @ u0) * u0
        v /= np.linalg.norm(v)
        frac = rng.uniform(0.9, 1.0) if k % 2 == 0 else rng.uniform(0.0, 1.0)
        t = tmax * frac
        out.append(math.cos(t) * u0 + math.sin(t) * v)
    return out


def main():
    iv = json.load(open(IVAL))["rows"]
    iv.sort(key=lambda r: r["slack"])
    rng = np.random.default_rng(20261029)
    pick = iv[: N_CELLS // 2] + [
        iv[int(i)]
        for i in rng.choice(np.arange(len(iv)), size=N_CELLS - N_CELLS // 2, replace=False)
    ]
    results = []
    worst = {"g_over_B": -1, "w_over_rho": -1, "du_ratio": -1, "sliver_ratio": -1, "min_slack": 1e9}
    for r in pick:
        cell = r["cell"]
        c = cell_consts(cell)
        B_up = r["B_up"]
        th_lo, th_hi, ph_lo, ph_hi = cell
        # L1: rectangle displacement vs du
        g_grid = np.linspace(th_lo, th_hi, 9)
        p_grid = np.linspace(ph_lo, ph_hi, 9)
        du_ratio = (
            max(np.linalg.norm(u_of(a, b) - c["u0"]) for a in g_grid for b in p_grid) / c["du"]
        )
        # L2: sphere ball samples
        samples = sample_sphere_ball(c["u0"], c["du"], N_SAMP, rng)
        g_max = -1e9
        w_ratio = 0.0
        for u in samples:
            Zu, _ = kernel(u)
            g = float(np.linalg.eigvalsh(Zu.T @ M @ Zu)[-1])
            g_max = max(g_max, g)
            # L3: decomposition of a random unit y in ker Phi(u)
            if np.isfinite(c["rho"]) and rng.uniform() < 0.1:
                cc = rng.normal(size=Zu.shape[1])
                y = Zu @ cc
                y /= np.linalg.norm(y)
                z = c["Z0"] @ (c["Z0"].T @ y)
                w = y - z
                nz = np.linalg.norm(z)
                if nz > 1e-12:
                    w_ratio = max(w_ratio, np.linalg.norm(w) / (nz * c["rho"]))
        # L4: sliver at theta = pi (float pi is below true pi)
        sl = 0.0
        if th_hi >= math.pi - 1e-15:
            sl = max(np.linalg.norm(u_of(math.pi, b) - c["u0"]) for b in p_grid) / c["du"]
        slack = B_up - g_max
        rec = {
            "cell": cell,
            "du": c["du"],
            "sigma36": c["sigma36"],
            "rho": c["rho"],
            "B_up_rigorous": B_up,
            "g_max_sampled": g_max,
            "slack_B_minus_g": slack,
            "du_ratio_rect": du_ratio,
            "w_over_rho_max": w_ratio,
            "sliver_ratio": sl,
        }
        results.append(rec)
        worst["g_over_B"] = max(worst["g_over_B"], g_max / B_up)
        worst["w_over_rho"] = max(worst["w_over_rho"], w_ratio)
        worst["du_ratio"] = max(worst["du_ratio"], du_ratio)
        worst["sliver_ratio"] = max(worst["sliver_ratio"], sl)
        worst["min_slack"] = min(worst["min_slack"], slack)
        print(
            f"sig36={c['sigma36']:.4f} B_up={B_up:.6e} g_max={g_max:.6e} slack={slack:.3e} "
            f"du_r={du_ratio:.3f} w/rho={w_ratio:.3f} sliver={sl:.3f}",
            flush=True,
        )
    verdict = (
        "NO_COUNTEREXAMPLE_IN_SAMPLES"
        if worst["g_over_B"] <= 1.0
        and worst["w_over_rho"] <= 1.0
        and worst["du_ratio"] <= 1.0
        and worst["sliver_ratio"] <= 1.0
        else "VIOLATION_FOUND"
    )
    out = {
        "n_cells": len(results),
        "n_samples_per_cell": N_SAMP,
        "worst": worst,
        "verdict": verdict,
        "note": "sampling audit (float evaluation of g and norms); rigorous B_up from interval_top1000.json; not a proof",
        "cells": results,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(json.dumps({k: v for k, v in out.items() if k != "cells"}, indent=1))


if __name__ == "__main__":
    main()
