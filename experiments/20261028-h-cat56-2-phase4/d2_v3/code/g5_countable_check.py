"""G5 numerical support (countable POVM, d = 22), family F_U, S = {4..15} (0-based).

Not a proof. Checks the ingredients of the analytic argument in D2_G5_TAIL_v1.md:
  G1  identity: sum_k N_k(0) = F^Q(0)                                  (matrix over S-directions)
  G2  per-outcome bound: F_k(th) <= N_k(th) (PSD), th = t*h, all t      (relative tolerance)
  G3  per-outcome limit at th -> 0 along h:
        regular k (p_k(0) > 0):  F_k(th) -> F_k(0)                     (classical FI at 0)
        null k (p_k(0) = 0):     F_k(th) -> (N_k h)(N_k h)^T / (h^T N_k h), N_k = N_k(0)
  G4  sums: sum_k F_k(th) -> sum_k F_lim_k as t -> 0 (no uniform tail assumed)

POVM: K_r regular outcomes (generic p_k(0) > 0) and K_n null outcomes (supported on the
bottom 20-dim block, p_k(0) = 0), normalised so that the total sum is exactly I.

Classical FI matrix: F_k,ab = d_a p_k * d_b p_k / p_k (0 if p_k <= 1e-14).
SLD L_a from eigendecomposition of rho_th; N_k,ab = Re tr(E_k L_a rho L_b).
Run: python -I g5_countable_check.py
"""

import sys

import numpy as np
from scipy.linalg import expm

sys.path.insert(
    0,
    r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261027-h-cat56-2-discovery\code",
)
import s8_admissible_span as sa  # noqa: E402

INST = (
    r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez"
    r"\experiments\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
)
A_all = sa.load_A(INST)
S = list(range(4, 16))
nS = len(S)
d = 22
Q = np.diag([1 / 3, 2 / 3]).astype(complex)
rho0 = np.zeros((d, d), complex)
rho0[:2, :2] = Q

Xs = []
for Ai in A_all:
    Bi = Ai / 2
    X = np.zeros((d, d), complex)
    X[:2, 2:] = -Bi.conj().T
    X[2:, :2] = Bi
    Xs.append(X)


def rho_of(theta):
    U = expm(sum(theta[i] * Xs[i] for i in range(16)))
    return U @ rho0 @ U.conj().T


def theta_of(hS):
    th = np.zeros(16)
    for k, a in enumerate(S):
        th[a] = hS[k]
    return th


def state_data(theta, eps=1e-6):
    rho = rho_of(theta)
    drho = []
    for a in S:
        e = np.zeros(16)
        e[a] = eps
        drho.append((rho_of(theta + e) - rho_of(theta - e)) / (2 * eps))
    lam, V = np.linalg.eigh(rho)
    denom = lam[:, None] + lam[None, :]
    keep = denom > 1e-12
    L = []
    kk_max = 0.0
    for dr in drho:
        D = V.conj().T @ dr @ V
        kk_max = max(kk_max, float(np.max(np.abs(D[~keep]))))
        Ls = np.where(keep, 2 * D / np.where(keep, denom, 1.0), 0.0)
        L.append(V @ Ls @ V.conj().T)
    return rho, np.array(drho), np.array(L), kk_max


def matrices(theta, Ek):
    rho, Dr, Lm, kk = state_data(theta)
    M = np.einsum("aij,jk,bkl->abil", Lm, rho, Lm)
    N = np.real(np.einsum("kil,abli->kab", Ek, M))
    FQ = np.real(np.einsum("ik,abki->ab", rho, np.einsum("aij,bjk->abik", Lm, Lm)))
    p = np.real(np.einsum("kil,li->k", Ek, rho))
    dp = np.real(np.einsum("kil,ali->ka", Ek, Dr))
    Fc = np.zeros_like(N)
    ok = p > 1e-14
    Fc[ok] = dp[ok][:, :, None] * dp[ok][:, None, :] / p[ok][:, None, None]
    return N, Fc, p, FQ, kk


def build_povm(rng, Kr, Kn):
    # null outcomes: supported on the bottom 20-dim block (p_k(0) = 0)
    Un = rng.normal(size=(Kn, 20)) + 1j * rng.normal(size=(Kn, 20))
    wn = 1.0 / (np.arange(1, Kn + 1)) ** 1.5
    En = np.zeros((Kn, d, d), complex)
    En[:, 2:, 2:] = wn[:, None, None] * np.einsum("ki,kj->kij", Un, Un.conj())
    Z = En.sum(0)
    scale = 0.5 / np.linalg.eigvalsh(Z).max()
    En = En * scale
    Z = Z * scale
    wv, wV = np.linalg.eigh(np.eye(d) - Z)
    Wh = wV @ np.diag(np.sqrt(wv)) @ wV.conj().T
    # regular outcomes: random PSD, transformed so that their sum is W = I - Z
    Vr = rng.normal(size=(Kr, d)) + 1j * rng.normal(size=(Kr, d))
    wr = 1.0 / (np.arange(1, Kr + 1)) ** 1.5
    Er = wr[:, None, None] * np.einsum("ki,kj->kij", Vr, Vr.conj())
    G = Er.sum(0)
    gv, gV = np.linalg.eigh(G)
    Gih = gV @ np.diag(gv ** (-0.5)) @ gV.conj().T
    X = Wh @ Gih
    Er = np.einsum("ij,kjl,lm->kim", X, Er, X.conj().T)
    Ek = np.concatenate([Er, En], axis=0)
    assert np.allclose(Ek.sum(0), np.eye(d), atol=1e-10)
    return Ek


rng = np.random.default_rng(20261030)
Kr, Kn = 2400, 600
Ek = build_povm(rng, Kr=Kr, Kn=Kn)
K = Ek.shape[0]
print(f"POVM outcomes: K = {K} (regular {Kr}, null {Kn}); sum-to-I checked (atol 1e-10)")

h = rng.normal(size=nS)
h /= np.linalg.norm(h)

N0, F0c, p0, FQ0, kk0 = matrices(np.zeros(16), Ek)
scaleN = max(1.0, float(np.max(np.abs(N0))))
print(f"SLD kernel-kernel check at theta=0: max |D_kk| = {kk0:.2e}; max|N_k(0)| = {scaleN:.3e}")

g1_err = np.linalg.norm(N0.sum(0) - FQ0) / np.linalg.norm(FQ0)
print(
    f"G1 identity sum_k N_k(0) = F^Q(0): rel err {g1_err:.2e} -> {'PASS' if g1_err < 1e-9 else 'FAIL'}"
)

reg = p0 > 1e-14
null = ~reg
Nh0 = np.einsum("kab,b->ka", N0, h)
hN0h = np.einsum("ka,a->k", Nh0, h)
Flim = np.zeros_like(N0)
Flim[reg] = F0c[reg]
okl = null & (hN0h > 1e-12)
Flim[okl] = Nh0[okl][:, :, None] * Nh0[okl][:, None, :] / hN0h[okl][:, None, None]
Flim_sum = Flim.sum(0)
print(
    f"regular k: {int(reg.sum())}; null k: {int(null.sum())}; null with h^T N_k h > 0: {int(okl.sum())}"
)

worst_g2 = -np.inf
g4_rows = []
for t in [1e-2, 1e-3, 1e-4]:
    Nt, Fct, pt, _, _ = matrices(t * theta_of(h), Ek)
    diff = Nt - Fct
    per_k_min = min(float(np.min(np.linalg.eigvalsh(diff[k]))) for k in range(K))
    worst_g2 = max(worst_g2, -per_k_min / scaleN)
    print(
        f"t={t:.0e}  G2 min_k lambda_min(N_k - F_k) = {per_k_min:.3e} (relative {per_k_min / scaleN:.2e})"
    )
    err_sum = np.linalg.norm(Fct.sum(0) - Flim_sum) / np.linalg.norm(Flim_sum)
    g4_rows.append(err_sum)
    print(f"        G4 rel |sum_k F_k(th) - sum_k F_lim_k| = {err_sum:.3e}")

g2_ok = worst_g2 <= 1e-6
print(f"G2 per-outcome bound F_k <= N_k (relative tol 1e-6): {'PASS' if g2_ok else 'FAIL'}")
g4_ok = g4_rows[-1] < g4_rows[0] and g4_rows[-1] < 1e-3
print(f"G4 sums converge (t=1e-4 error < t=1e-2 error and < 1e-3): {'PASS' if g4_ok else 'FAIL'}")

# G3: per-outcome limits at t = 1e-4
_, Fct, _, _, _ = matrices(1e-4 * theta_of(h), Ek)
idx_reg = np.where(reg)[0]
idx_null = np.where(okl)[0]
e_reg = np.array(
    [np.linalg.norm(Fct[k] - F0c[k]) / max(np.linalg.norm(F0c[k]), 1e-12) for k in idx_reg]
)
e_null = np.array(
    [np.linalg.norm(Fct[k] - Flim[k]) / max(np.linalg.norm(Flim[k]), 1e-12) for k in idx_null]
)
print(
    f"G3 regular k vs F_k(0) (t=1e-4): median rel err {np.median(e_reg):.3e}, max {np.max(e_reg):.3e}"
)
print(
    f"G3 null k vs null formula (t=1e-4): median rel err {np.median(e_null):.3e}, max {np.max(e_null):.3e}"
)
