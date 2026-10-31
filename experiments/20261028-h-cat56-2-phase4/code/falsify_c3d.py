"""Independent falsification of: max over x, unit y in Y_S(x) of y^dag R y <= 0.9 trR/20.
Construction independent of phi_rows: unknowns (Re y, Im y, lambda_i real) and the complex equations
A_i^dag y - lambda_i x = 0, written as a real (4|S|) x (40+|S|) system. Kernel -> y-part -> orthonormalise.
Also: check of the cell speed bound du used in c3d_cell_certificate_adapted.py (line 107).
Run: python -I falsify_c3d.py
"""

import json, math, sys
import numpy as np
from scipy.optimize import minimize

BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
RPATH = (
    BASE
    + r"\20261028-h-cat56-2-phase3\metrics\inputs\s14_R_4-5-6-7-8-9-10-11-12-13-14-15_nx250.npz"
)

with open(INST, encoding="utf-8") as fh:
    rec = json.loads(fh.readline())
As = []
for flat in rec["blocks"]:
    flat = np.asarray(flat, float)
    re = flat[:40].reshape(20, 2)
    im = flat[40:80].reshape(20, 2)
    As.append(-2j * (re + 1j * im))
S = list(range(4, 16))
R0 = np.load(RPATH)["R"]
R = 0.5 * (R0 + R0.conj().T)
trR = float(np.trace(R).real)
target = 0.9 * trR / 20
print("trR", trR, "target", target)


def kernel_Y(x):
    """Real basis (orthonormal in R^40 ~ C^20) of Y_S(x)."""
    n = len(S)
    rows = []
    for k, i in enumerate(S):
        Ah = As[i].conj().T  # 2 x 20
        for c in range(2):
            # complex equation: Ah[c] . y - lambda_k x[c] = 0 ; y = yr + i yi
            a = Ah[c]
            lam_col = np.zeros(n)
            row_re = np.concatenate([a.real, -a.imag, lam_col.copy()])
            row_im = np.concatenate([a.imag, a.real, lam_col.copy()])
            row_re[40 + k] = -x[c].real
            row_im[40 + k] = -x[c].imag
            rows += [row_re, row_im]
    B = np.array(rows)  # 48 x 52
    _, s, Vt = np.linalg.svd(B)
    full = np.zeros(B.shape[1])
    full[: len(s)] = s
    tol = 1e-9 * s[0]
    K = Vt[full < tol].T  # 52 x k
    Yp = K[:40]
    Q, sv, _ = np.linalg.svd(Yp, full_matrices=False)
    Q = Q[:, sv > 1e-9]
    return Q, full


def worst(x):
    Q, full = kernel_Y(x)
    Y = Q[:20] + 1j * Q[20:]  # 20 x k complex columns; real span = Y_S(x)
    # quadratic form on real coordinates c: (Y c)^dag R (Y c) = c^T Re(Y^dag R Y) c
    G = (Y.conj().T @ R @ Y).real
    G = 0.5 * (G + G.T)
    return float(np.linalg.eigvalsh(G)[-1]), Q.shape[1], full


def xa(th, ph):
    return np.array([math.cos(th / 2), math.sin(th / 2) * np.exp(1j * ph)])


# sanity: kernel vectors actually satisfy A^dag y = real*x
rng = np.random.default_rng(1)
x = xa(1.1, 2.3)
Q, _ = kernel_Y(x)
y = (Q[:20] + 1j * Q[20:]) @ rng.normal(size=Q.shape[1])
for i in S:
    c = As[i].conj().T @ y
    mu = c / x
    assert abs(mu[0] - mu[1]) < 1e-8 * abs(c).max() and abs(mu[0].imag) < 1e-8 * abs(c).max(), mu
print("sanity ok, kernel dim", Q.shape[1])

# dense grid
best = (-1, None)
dims = {}
smin = (np.inf, None)
NT, NP = (
    int(sys.argv[1]) if len(sys.argv) > 1 else 180,
    int(sys.argv[2]) if len(sys.argv) > 2 else 360,
)
for th in np.linspace(0, math.pi, NT + 1):
    for ph in np.linspace(0, 2 * math.pi, NP, endpoint=False):
        v, d, full = worst(xa(th, ph))
        dims[d] = dims.get(d, 0) + 1
        if v > best[0]:
            best = (v, (th, ph))
        s36 = full[47 - 0]  # 48th singular value of the 48x52 system
        if s36 < smin[0]:
            smin = (s36, (th, ph))
print("grid max", best, "kernel dims", dims, "min sigma_48", smin)

# local refinement from top grid points + random restarts
starts = [best[1]] + [(rng.uniform(0, math.pi), rng.uniform(0, 2 * math.pi)) for _ in range(40)]
glob = best
for st in starts:
    r = minimize(
        lambda p: -worst(xa(p[0], p[1]))[0],
        np.array(st),
        method="Nelder-Mead",
        options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 3000},
    )
    v = -r.fun
    if v > glob[0]:
        glob = (v, tuple(r.x))
print("refined max", glob, "target", target, "ratio", glob[0] / target)


# du check for the adapted certificate (line 107): sup |u - u0| over a cell vs code du
def u_of(th, ph):
    return np.array(
        [math.cos(th / 2), 0.0, math.sin(th / 2) * math.cos(ph), math.sin(th / 2) * math.sin(ph)]
    )


worst_ratio = 0
for tl, w_th, w_ph in [
    (math.pi - 0.02, 0.02, 0.02),
    (2.0, 0.01, 0.01),
    (math.pi - 0.02, 0.005, 0.04),
]:
    th_lo, th_hi, ph_lo, ph_hi = tl, tl + w_th, 1.0, 1.0 + w_ph
    hth, hph = w_th / 2, w_ph / 2
    du_code = 0.5 * hth + math.sin(min(th_hi, math.pi) / 2) * hph  # fixed formula (c3d line 107)
    u0 = u_of(th_lo + hth, ph_lo + hph)
    sup = max(
        np.linalg.norm(u_of(a, b) - u0)
        for a in np.linspace(th_lo, th_hi, 41)
        for b in np.linspace(ph_lo, ph_hi, 41)
    )
    print(
        f"cell th[{th_lo:.3f},{th_hi:.3f}] dph={w_ph}: sup|du|={sup:.6e} code du={du_code:.6e} ratio={sup / du_code:.4f}"
    )
