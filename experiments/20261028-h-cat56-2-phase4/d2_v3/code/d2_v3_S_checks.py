"""D2 v3, closure of audit finding З5: all checks restricted to the index set S = {4..15} (0-based).

Restrictions compared with d2_v3_checks.py (which used range(16)):
  - x and the tangent directions h are supported on S (zeros outside S);
  - M_x = sum_{a in S} x_a A_a, N_E and the F_U family use only the S-parameters
    (other theta coordinates are held at 0).
Checks:
  S1  Lemma 1 identity with x in R^S (|S| = 12), random block E >= 0
  S2  Schur equivalence E PSD <=> R PSD (ran B in ran P), restricted to S-type D
  S3  Lemma 4 (rank-one): y in Y_S(z) constructed by solving A_a^dag y = lambda_a z, lambda real
      => rank N_{yy}^{S} <= 1; generic y => rank > 1
  S4  F_U null outcome with h supported on S and h^T N_S h = 0 => p(t h) = 0
  S5  F_U null outcome with h supported on S and h^T N_S h > 0 => CFIM(t h) -> (N h)(N h)^T/(h N h)
  S6  the S x S block of the 16-parameter identity equals the S-only identity (consistency)
Run: python -I d2_v3_S_checks.py
"""

import sys
import numpy as np
from scipy.linalg import expm, sqrtm

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
S = list(range(4, 16))  # S- = {4..15}, 0-based
A = [A_all[a] for a in S]  # the 12 S-parameter matrices
nS = len(S)
d = 22
Q = np.diag([1 / 3, 2 / 3]).astype(complex)
rho0 = np.zeros((d, d), complex)
rho0[:2, :2] = Q
rng = np.random.default_rng(20261031)
results = []


def report(name, ok, detail):
    results.append(ok)
    print(("PASS" if ok else "FAIL"), name, "|", detail)


def herm_psd(n, rank=None):
    r = n if rank is None else rank
    X = rng.normal(size=(n, r)) + 1j * rng.normal(size=(n, r))
    return X @ X.conj().T


def rand_c(m, n):
    return rng.normal(size=(m, n)) + 1j * rng.normal(size=(m, n))


def N_block(D):
    """N_S(D)_{ab} = Re tr(D A_a Q A_b^dag) for the S-parameters."""
    return np.array(
        [[np.real(np.trace(D @ A[a] @ Q @ A[b].conj().T)) for b in range(nS)] for a in range(nS)]
    )


def bracket_and_identity(P, B, D, x):
    M = sum(x[a] * A[a] for a in range(nS))
    Pp = np.linalg.pinv(P)
    p = np.real(np.trace(Q @ P))
    dp = np.real(np.trace(B @ M @ Q))
    NX = np.real(np.trace(D @ M @ Q @ M.conj().T))
    lhs = NX - dp**2 / p
    c = B @ M @ Q
    R = D - B.conj().T @ Pp @ B
    T1 = np.real(np.trace(Pp @ c @ np.linalg.inv(Q) @ c.conj().T))
    T2 = dp**2 / p
    rhs = np.real(np.trace(R @ M @ Q @ M.conj().T)) + (T1 - T2)
    return lhs, rhs, T1 - T2, R


# ---- S1: Lemma 1 identity on S ----
worst = 0.0
for _ in range(60):
    P = herm_psd(2) + 0.2 * np.eye(2)
    Pi = P @ np.linalg.pinv(P)
    Z = Pi @ rand_c(2, 20)
    B = sqrtm(P) @ Z
    Dm = Z.conj().T @ Z + herm_psd(20) * 0.05
    x = rng.normal(size=nS)
    lhs, rhs, gap, _ = bracket_and_identity(P, B, Dm, x)
    worst = max(worst, abs(lhs - rhs) / max(1.0, abs(lhs)))
    assert gap >= -1e-7 * max(1.0, abs(gap))
report(
    "S1 Lemma-1 identity with x in R^S (12 directions)", worst < 1e-10, f"max rel err {worst:.2e}"
)

# ---- S2: Schur equivalence E PSD <=> R PSD, S-type D ----
agree, n_psd, n_not = 0, 0, 0
for kind in ["P_full", "P_rank1"]:
    for _ in range(100):
        P = herm_psd(2) + 0.2 * np.eye(2) if kind == "P_full" else herm_psd(2, rank=1)
        Pi = P @ np.linalg.pinv(P)
        B = sqrtm(P) @ (Pi @ rand_c(2, 20))
        Hm = (rand_c(20, 20) + rand_c(20, 20).conj().T) / 2 * 0.005
        Hm = Hm + rng.choice([-0.2, 0.2]) * np.eye(20)
        Dm = B.conj().T @ np.linalg.pinv(P) @ B + Hm
        Em = np.block([[P, B], [B.conj().T, Dm]])
        Rm = Dm - B.conj().T @ np.linalg.pinv(P) @ B
        okE = np.min(np.linalg.eigvalsh(Em)) > -1e-9
        okR = np.min(np.linalg.eigvalsh(Rm)) > -1e-9
        agree += int(okE == okR)
        n_psd += int(okE)
        n_not += int(not okE)
report(
    "S2 Schur equivalence (S-type setting)",
    agree == 200 and n_psd > 0 and n_not > 0,
    f"agreements {agree}/200; E PSD {n_psd}, not PSD {n_not}",
)

# ---- S3: Lemma 4 on S: y in Y_S(z) => rank N_yy^S <= 1; generic y => rank > 1 ----
# Construct y with A_a^dag y = lambda_a z (lambda real, z fixed) : real-linear system in (Re y, Im y, lambda).
z = rng.normal(size=2) + 1j * rng.normal(size=2)
rows, rhs_ = [], []
for a in range(nS):
    # A_a^dag y : (2x20)(20) -> 2 complex entries; unknown y complex (20), lambda_a real
    Ad = A[a].conj().T  # 2x20
    for i in range(2):
        # real and imaginary parts of (Ad y)_i - lambda_a z_i = 0
        row_re = np.zeros(40 + nS)
        row_im = np.zeros(40 + nS)
        # y = yr + i*yi ; (Ad y)_i = sum_r Ad[i,r] (yr_r + i yi_r)
        row_re[:20] = Ad[i, :].real
        row_re[20:40] = -Ad[i, :].imag
        row_im[:20] = Ad[i, :].imag
        row_im[20:40] = Ad[i, :].real
        row_re[40 + a] = -z[i].real
        row_im[40 + a] = -z[i].imag
        rows.append(row_re)
        rows.append(row_im)
Mat = np.array(rows)
_, sv, vh = np.linalg.svd(Mat)
ker = vh[np.sum(sv > 1e-10) :]
if ker.shape[0] == 0:
    # no nontrivial solution: take the y=0 solution only
    y_sub = np.zeros(20, complex)
else:
    coef = rng.normal(size=ker.shape[0])
    sol = ker.T @ coef
    y_sub = sol[:20] + 1j * sol[20:40]
N_sub = N_block(np.outer(y_sub, y_sub.conj()))
rank_sub = np.linalg.matrix_rank(N_sub, tol=1e-9 * max(1.0, np.max(np.abs(N_sub))))
y_gen = rand_c(20, 1)[:, 0]
N_gen = N_block(np.outer(y_gen, y_gen.conj()))
rank_gen = np.linalg.matrix_rank(N_gen, tol=1e-9 * max(1.0, np.max(np.abs(N_gen))))
report(
    "S3 Lemma 4 on S (rank-one <=> Y_S)",
    rank_sub <= 1 and rank_gen > 1,
    f"constructed y in Y_S(z): rank N^S = {rank_sub} (kernel dim {ker.shape[0]}); "
    f"generic y: rank N^S = {rank_gen}",
)

# ---- S4 / S5: F_U with theta supported on S (other coordinates held at 0) ----
Bs = [Ai / 2 for Ai in A_all]
Xs = []
for Bi in Bs:
    X = np.zeros((d, d), complex)
    X[:2, 2:] = -Bi.conj().T
    X[2:, :2] = Bi
    Xs.append(X)


def th_full(hS):
    th = np.zeros(16)
    for k, a in enumerate(S):
        th[a] = hS[k]
    return th


def rho_FU(th):
    X = sum(th[i] * Xs[i] for i in range(16))
    U = expm(X)
    return U @ rho0 @ U.conj().T


def p_null(th, y):
    w = np.zeros(d, complex)
    w[2:] = y
    return np.real(w.conj() @ rho_FU(th) @ w)


# S4: y with A_S^dag y = 0 (all S-directions annihilate y)
Lm = np.zeros((4 * nS, 0))  # placeholder (unused)
Lrows = []
yy = rand_c(20, 1)[:, 0]
# find real hS with sum_k hS_k A_k^dag y = 0
Lmat = np.zeros((4, nS))
for k in range(nS):
    v = A[k].conj().T @ yy
    Lmat[:, k] = np.concatenate([v.real, v.imag])
_, s4, vh4 = np.linalg.svd(Lmat)
kern4 = vh4[4:]
if kern4.shape[0] == 0:
    hS0 = np.zeros(nS)
else:
    hS0 = kern4.T @ rng.normal(size=kern4.shape[0])
    hS0 /= np.linalg.norm(hS0)
N_y = N_block(np.outer(yy, yy.conj()))
hNh0 = hS0 @ N_y @ hS0
max_p = max(abs(p_null(t * th_full(hS0), yy)) for t in [0.1, 0.3, 1.0])
report(
    "S4 F_U, S-directions, h^T N h = 0 => p(t h) = 0",
    max_p < 1e-12 and abs(hNh0) < 1e-12,
    f"h^T N h = {hNh0:.2e}; max |p(t h)| = {max_p:.2e}",
)

# S5: generic y and h supported on S
y2 = rand_c(20, 1)[:, 0]
N2 = N_block(np.outer(y2, y2.conj()))
h2 = rng.normal(size=nS)
hN2h = h2 @ N2 @ h2
pred = np.outer(N2 @ h2, N2 @ h2) / hN2h
errs = []
for t in [1e-2, 1e-3, 1e-4]:
    hs = t * h2
    th = th_full(hs)
    g = np.zeros(nS)
    eps = 1e-7 * t
    for k in range(nS):
        e = np.zeros(nS)
        e[k] = eps
        g[k] = (p_null(th_full(hs + e), y2) - p_null(th_full(hs - e), y2)) / (2 * eps)
    p0 = p_null(th, y2)
    Fl = np.outer(g, g) / p0
    errs.append(np.max(np.abs(Fl - pred)) / np.max(np.abs(pred)))
report(
    "S5 F_U, S-directions, h^T N h > 0: CFIM -> (Nh)(Nh)^T/(hNh)",
    errs[-1] < 1e-3 and errs[-1] < errs[-2] < errs[-3],
    "relative error at t = 1e-2, 1e-3, 1e-4: " + ", ".join(f"{e:.2e}" for e in errs),
)

# ---- S6: consistency: S x S block of the 16-parameter N equals the S-only N ----
Dtest = herm_psd(20)
N16 = np.array(
    [
        [np.real(np.trace(Dtest @ A_all[a] @ Q @ A_all[b].conj().T)) for b in range(16)]
        for a in range(16)
    ]
)
N_S_from16 = N16[np.ix_(S, S)]
N_S_direct = N_block(Dtest)
report(
    "S6 S x S block of N (16 params) equals N computed with S-parameters only",
    np.allclose(N_S_from16, N_S_direct, rtol=1e-12, atol=1e-12),
    f"max abs diff {np.max(np.abs(N_S_from16 - N_S_direct)):.2e}",
)

print("ALL PASS" if all(results) else "SOME FAILED")
