# WHY: contract STAGE_D items 3 and 4, in ball arithmetic (python-flint arb, prec 192).
# Item 3: for every element k and every i in S+ = {0..11}, with w_i = A_i^dag y_k and
#   lambda_i = Re(x^dag w_i)/|x|^2, the exact condition is w_i = lambda_i x (lambda_i real).
#   Certified: 0 lies in every component ball of w_i - lambda_i x AND of Im(x^dag w_i).
# Item 4: CFIM F^C = sum_k c_k g_k g_k^T / q_k and QFIM F^Q = Re tr(rho_d A_i^dag A_k),
#   with g_k[i] = Re(x^dag rho_d w_i), q_k = x^dag rho_d x, c_k = candidate weight.
#   Closed forms derived by hand from L_i = [[0, A_i^dag],[A_i, 0]], rho = diag(1/3, 2/3) on C^2 (0 elsewhere);
#   cross-checked below against the direct probability formula in float (check_povm280_direct.py logic).
# Instance: A_i = -2i (re + i im) with integer data; exact in arb.
import json

import numpy as np
from flint import arb, ctx

ctx.prec = 192
BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
POVM = BASE + r"\20261028-h-cat56-2-phase3\metrics\inputs\s14_povm_prefix12.npz"
OUT = BASE + r"\20261028-h-cat56-2-phase4\stage_d\metrics_criteria.json"
S = list(range(12))  # S+ = {0..11}

rec = json.loads(open(INST, encoding="utf-8").readline())
Are, Aim = {}, {}
for i in S:
    flat = rec["blocks"][i]
    re_ = [[int(flat[2 * r + a]) for a in range(2)] for r in range(20)]
    im_ = [[int(flat[40 + 2 * r + a]) for a in range(2)] for r in range(20)]
    # A = -2i (re + i im) = 2*im - 2i*re
    Are[i] = [[arb(2 * im_[r][a]) for a in range(2)] for r in range(20)]
    Aim[i] = [[arb(-2 * re_[r][a]) for a in range(2)] for r in range(20)]

d = np.load(POVM)
w, V = d["weights"], d["vectors"]
n = len(w)
rho = [arb(1) / 3, arb(2) / 3]


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ball0(x):
    return float(x.lower()) <= 0.0 <= float(x.upper())


def up(x):
    return float(abs(x).upper())


# --- item 3 ---
n_pairs = 0
n_pairs_zero = 0
max_resid_up = 0.0
n_imlam_zero = 0
max_resid_mid = 0.0
worst = None
g_store = []  # per element: list over i of g_i (real, arb)
for k in range(n):
    x = [(arb(float(V[k, j].real)), arb(float(V[k, j].imag))) for j in range(2)]
    y = [(arb(float(V[k, 2 + r].real)), arb(float(V[k, 2 + r].imag))) for r in range(20)]
    xx = sum((x[j][0] * x[j][0] + x[j][1] * x[j][1] for j in range(2)), arb(0))
    c_k = arb(float(w[k]))
    gk = []
    for i in S:
        wv = []
        for j in range(2):
            acc = (arb(0), arb(0))
            for r in range(20):
                # conj(A[r][j]) * y[r]
                t = cmul((Are[i][r][j], -Aim[i][r][j]), y[r])
                acc = (acc[0] + t[0], acc[1] + t[1])
            wv.append(acc)
        # x^dag w = sum_j conj(x_j) w_j
        xdw = (arb(0), arb(0))
        for j in range(2):
            t = cmul((x[j][0], -x[j][1]), wv[j])
            xdw = (xdw[0] + t[0], xdw[1] + t[1])
        lam = xdw[0] / xx
        ok = ball0(xdw[1])
        n_imlam_zero += int(ok)
        for j in range(2):
            rx = wv[j][0] - lam * x[j][0]
            ry = wv[j][1] - lam * x[j][1]
            ok = ok and ball0(rx) and ball0(ry)
            if max(up(rx), up(ry)) > max_resid_up:
                max_resid_up = max(up(rx), up(ry))
                worst = (k, i, j, float(rx.mid()), float(ry.mid()))
        n_pairs += 1
        n_pairs_zero += int(ok)
        # item 4 ingredients: g_i = Re(x^dag rho_d w_i)
        g = arb(0)
        for j in range(2):
            t = cmul((x[j][0], -x[j][1]), wv[j])
            g = g + rho[j] * t[0]
        gk.append(g)
    g_store.append(
        (c_k, gk, sum((rho[j] * (x[j][0] * x[j][0] + x[j][1] * x[j][1]) for j in range(2)), arb(0)))
    )

print("item 3: pairs (k,i) =", n_pairs)
print("item 3: pairs with 0 in ALL residual and Im(x^dag w) balls:", n_pairs_zero)
print("item 3: pairs with Im(x^dag w) ball containing 0:", n_imlam_zero)
print("item 3: certified max |component of w_i - lambda_i x| upper bound:", max_resid_up)
print("item 3: worst pair (k, i, j, Re, Im of residual midpoint):", worst)

# --- item 4: CFIM and QFIM in arb ---
FC = [[arb(0) for _ in S] for _ in S]
for c_k, gk, q in g_store:
    for a in S:
        for b in S:
            FC[a][b] = FC[a][b] + c_k * gk[a] * gk[b] / q
FQ = [[arb(0) for _ in S] for _ in S]
for a in S:
    for b in S:
        s = arb(0)
        for j in range(2):
            for r in range(20):
                s = s + rho[j] * (Are[a][r][j] * Are[b][r][j] + Aim[a][r][j] * Aim[b][r][j])
        FQ[a][b] = s
D = [[FQ[a][b] - FC[a][b] for b in S] for a in S]
n_entry_zero = sum(1 for a in S for b in S if ball0(D[a][b]))
max_D_up = max(up(D[a][b]) for a in S for b in S)
gersh = max(sum(up(D[a][b]) for b in S) for a in S)
max_FQ = max(up(FQ[a][b]) for a in S for b in S)
print("item 4: entries of F^Q - F^C whose ball contains 0:", n_entry_zero, "of", len(S) * len(S))
print("item 4: certified max |F^Q - F^C| entry upper bound:", max_D_up)
print("item 4: Gershgorin bound on ||F^Q - F^C||_2:", gersh)
print("item 4: max |F^Q| upper:", max_FQ, " relative:", max_D_up / max_FQ)

# --- independent float cross-check of the closed form vs the probability formula ---
rhof = np.zeros((22, 22), complex)
rhof[0, 0], rhof[1, 1] = 1 / 3, 2 / 3
Af = {}
for i in S:
    flat = rec["blocks"][i]
    re_ = np.array([[flat[2 * r + a] for a in range(2)] for r in range(20)], float)
    im_ = np.array([[flat[40 + 2 * r + a] for a in range(2)] for r in range(20)], float)
    Af[i] = -2j * (re_ + 1j * im_)
Lf = {}
for i in S:
    L = np.zeros((22, 22), complex)
    L[:2, 2:] = Af[i].conj().T
    L[2:, :2] = Af[i]
    Lf[i] = L
FCd = np.zeros((12, 12))
for k in range(n):
    v = V[k]
    p = w[k] * (v.conj() @ rhof @ v).real
    dp = np.array([w[k] * (v.conj() @ ((Lf[i] @ rhof + rhof @ Lf[i]) / 2) @ v).real for i in S])
    if p > 0:
        FCd += np.outer(dp, dp) / p
FQd = np.array([[np.trace(rhof @ Lf[a] @ Lf[b]).real for b in S] for a in S])
mid_FC = np.array([[float(FC[a][b].mid()) for b in S] for a in S])
mid_FQ = np.array([[float(FQ[a][b].mid()) for b in S] for a in S])
print("cross-check: max|FC_arb_mid - FC_direct_float| =", np.abs(mid_FC - FCd).max())
print("cross-check: max|FQ_arb_mid - FQ_direct_float| =", np.abs(mid_FQ - FQd).max())
print(
    "cross-check: max|FQ_direct - FC_direct| / max|FQ| =",
    np.abs(FQd - FCd).max() / np.abs(FQd).max(),
)

out = {
    "prec_bits": 192,
    "item3_pairs": n_pairs,
    "item3_pairs_zero_certified": n_pairs_zero,
    "item3_im_lambda_zero_certified": n_imlam_zero,
    "item3_cert_max_residual_upper": max_resid_up,
    "item4_entries_zero_certified": n_entry_zero,
    "item4_cert_max_D_upper": max_D_up,
    "item4_gershgorin_D_upper": gersh,
    "item4_max_FQ_upper": max_FQ,
    "crosscheck_float_FQ_vs_direct": float(np.abs(mid_FQ - FQd).max()),
    "crosscheck_float_FC_vs_direct": float(np.abs(mid_FC - FCd).max()),
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("written", OUT)
