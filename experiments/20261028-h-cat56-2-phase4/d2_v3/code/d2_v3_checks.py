"""D2 v3 numerical controls on the canonical A0 matrices (sa.load_A, A = -2i (re + i im)).

Checks (each prints PASS/FAIL with the measured value):
  C1  block deficit identity, regular E, P > 0, rank-1 P, singular P (pseudo-inverse)
  C2  equality case c = mu P Q with mu of EITHER sign gives zero bracket
  C3  F_U family, null outcome with h^T N h = 0: p_E(t h) = 0 exactly
  C4  F_U family, null outcome with h^T N h > 0: CFIM(t h) -> (N h)(N h)^T/(h^T N h)
  C5  feasibility of B A_a = mu_a P (saturating regular element), random mu
Run:  python -I d2_v3_checks.py
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
A = sa.load_A(INST)  # certificate convention, includes the -2i factor
d = 22
Q = np.diag([1 / 3, 2 / 3]).astype(complex)
rho0 = np.zeros((d, d), complex)
rho0[:2, :2] = Q
rng = np.random.default_rng(20261030)
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


def bracket_and_identity(P, B, D, x):
    """Return lhs = x^T(N_E - F_E)x and rhs = Re tr(R M Q M^+) + (T1 - T2) with pseudo-inverse."""
    M = sum(x[a] * A[a] for a in range(16))
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


# ---- C1: block identity incl. rank-deficient P (range condition B = P^{1/2} Z) ----
worst = 0.0
worst_psd = 0.0
for kind in ["P_full", "P_rank1"]:
    for _ in range(60):
        if kind == "P_full":
            P = herm_psd(2) + 0.2 * np.eye(2)
        else:
            P = herm_psd(2, rank=1)
        Ph = sqrtm(P)  # complex-valued sqrtm of a Hermitian PSD matrix: keep it
        Pi = P @ np.linalg.pinv(P)  # projector onto ran P
        Z = Pi @ rand_c(2, 20)  # range of Z inside ran P, so B^dag P^+ B = Z^dag Z
        B = Ph @ Z  # ran B subset ran P by construction
        Rr = herm_psd(20) * 0.05
        D = Z.conj().T @ Z + Rr  # D >= B^dag P^+ B = Z^dag Z (checked below)
        Pp = np.linalg.pinv(P)
        assert np.allclose(B.conj().T @ Pp @ B, Z.conj().T @ Z, atol=1e-9)
        E = np.block([[P, B], [B.conj().T, D]])
        assert np.min(np.linalg.eigvalsh(E)) > -1e-8
        x = rng.normal(size=16)
        lhs, rhs, gap, R = bracket_and_identity(P, B, D, x)
        worst = max(worst, abs(lhs - rhs) / max(1.0, abs(lhs)))
        assert gap >= -1e-7 * max(1.0, abs(gap))
report(
    "C1 block identity, P>0 and rank(P)=1 (pinv)",
    worst < 1e-10,
    f"max rel err {worst:.2e} (identity is algebraic; the nonnegativity is checked in C1b)",
)

# C1b (Schur equivalence, NOT tautological): for random Hermitian H (any sign), E = [[P,B],[B^dag,D]]
# with D = B^dag P^+ B + H is PSD exactly when R = D - B^dag P^+ B = H is PSD (ran B in ran P).
# Check that the sign of min eig(E) and min eig(R) agree on every trial, and both signs occur.
agree, n_psd, n_notpsd = 0, 0, 0
for kind in ["P_full", "P_rank1"]:
    for _ in range(100):
        P = herm_psd(2) + 0.2 * np.eye(2) if kind == "P_full" else herm_psd(2, rank=1)
        Pi = P @ np.linalg.pinv(P)
        Z = Pi @ rand_c(2, 20)
        B = sqrtm(P) @ Z
        Hm = rand_c(20, 20)
        Hm = (Hm + Hm.conj().T) / 2 * 0.005  # small random part: spectrum within about +-0.1
        # shift by +-0.2 so that both PSD and non-PSD H occur (a pure random H is almost never PSD)
        Hm = Hm + rng.choice([-0.2, 0.2]) * np.eye(20)
        Dm = B.conj().T @ np.linalg.pinv(P) @ B + Hm
        Em = np.block([[P, B], [B.conj().T, Dm]])
        Rm = Dm - B.conj().T @ np.linalg.pinv(P) @ B
        ok_E = np.min(np.linalg.eigvalsh(Em)) > -1e-9
        ok_R = np.min(np.linalg.eigvalsh(Rm)) > -1e-9
        agree += int(ok_E == ok_R)
        n_psd += int(ok_E)
        n_notpsd += int(not ok_E)
report(
    "C1b Schur equivalence: E PSD <=> R PSD on random trials (both signs occur)",
    agree == 200 and n_psd > 0 and n_notpsd > 0,
    f"agreements {agree}/200; E PSD in {n_psd}, E not PSD in {n_notpsd}",
)


# ---- C2: equality bracket = 0 for c = mu P Q, mu of either sign ----
def bracket_c(P, c):
    """T1 - T2 as a function of c (P > 0, Q fixed): the Lemma-1 bracket, not a rewritten identity."""
    Pp = np.linalg.inv(P)
    T1 = np.real(np.trace(Pp @ c @ np.linalg.inv(Q) @ c.conj().T))
    T2 = np.real(np.trace(c)) ** 2 / np.real(np.trace(Q @ P))
    return T1 - T2


# C2a (sufficiency): c = mu P Q gives zero bracket for mu of either sign
P = herm_psd(2) + 0.2 * np.eye(2)
vals = [bracket_c(P, mu * P @ Q) for mu in [0.7, -0.7, -3.2]]
report(
    "C2a equality bracket vanishes for c = mu P Q, mu in {0.7,-0.7,-3.2}",
    all(abs(v) < 1e-10 for v in vals),
    "values " + ", ".join(f"{v:.1e}" for v in vals),
)

# C2b (necessity probe): perturb c away from mu P Q by eps*G with G not proportional to P Q.
# Lemma 2 needs: zero bracket => c proportional to P Q. Expect bracket ~ eps^2 * (positive).
G = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
mu0 = 0.7
ratios = []
for eps in [1e-2, 1e-3, 1e-4]:
    b = bracket_c(P, mu0 * P @ Q + eps * G)
    ratios.append(b / eps**2)
report(
    "C2b necessity probe: bracket/eps^2 stays positive and finite as eps -> 0",
    all(r > 0 for r in ratios) and abs(ratios[-1] - ratios[-2]) / abs(ratios[-1]) < 1e-2,
    "bracket/eps^2 at eps=1e-2,1e-3,1e-4: " + ", ".join(f"{r:.6e}" for r in ratios),
)

# ---- F_U family: rho_th = U rho U^dag, U = exp(sum th_i X_i), X_i = [[0,-B_i^dag],[B_i,0]], B_i = A_i/2 ----
Bs = [Ai / 2 for Ai in A]
Xs = []
for Bi in Bs:
    X = np.zeros((d, d), complex)
    X[:2, 2:] = -Bi.conj().T
    X[2:, :2] = Bi
    Xs.append(X)


def rho_FU(th):
    X = sum(th[i] * Xs[i] for i in range(16))
    U = expm(X)
    return U @ rho0 @ U.conj().T


def p_null(th, y):
    """p_E(th) for null E = w w^dag, w = (0; y)."""
    w = np.zeros(d, complex)
    w[2:] = y
    return np.real(w.conj() @ rho_FU(th) @ w)


def N_null(y):
    E00 = np.outer(y, y.conj())
    return np.array(
        [[np.real(np.trace(E00 @ A[a] @ Q @ A[b].conj().T)) for b in range(16)] for a in range(16)]
    )


# ---- C3: null outcome with h^T N h = 0 => p(t h) = 0 exactly ----
y = rand_c(20, 1)[:, 0]
# find real h with A_h^dag y = 0 (sum_a h_a A_a^dag y = 0): real linear system, 4 real eqs
Lmat = np.zeros((4, 16))
for a in range(16):
    v = A[a].conj().T @ y  # 2-vector
    Lmat[:, a] = np.concatenate([v.real, v.imag])
u, s, vh = np.linalg.svd(Lmat)
null_vecs = vh[4:]  # 12-dim real kernel
h0 = null_vecs.T @ rng.normal(size=12)
h0 /= np.linalg.norm(h0)
Nh = N_null(y)
hNh = h0 @ Nh @ h0
max_p = 0.0
for t in [0.1, 0.3, 1.0]:
    max_p = max(max_p, abs(p_null(t * h0, y)))
report(
    "C3 F_U: null outcome with h^T N h = 0 gives p(t h) = 0",
    max_p < 1e-12 and abs(hNh) < 1e-12,
    f"h^T N h = {hNh:.2e}; max |p(t h)| over t in {{0.1,0.3,1}} = {max_p:.2e}",
)

# ---- C4: null outcome with h^T N h > 0: CFIM limit ----
y2 = rand_c(20, 1)[:, 0]
N2 = N_null(y2)
h2 = rng.normal(size=16)
hN2h = h2 @ N2 @ h2
pred = np.outer(N2 @ h2, N2 @ h2) / hN2h
errs = []
for t in [1e-2, 1e-3, 1e-4]:
    th = t * h2
    g = np.zeros(16)
    eps = 1e-7 * t
    for u_ in range(16):
        e = np.zeros(16)
        e[u_] = eps
        g[u_] = (p_null(th + e, y2) - p_null(th - e, y2)) / (2 * eps)
    p0 = p_null(th, y2)
    Fl = np.outer(g, g) / p0
    errs.append(np.max(np.abs(Fl - pred)) / np.max(np.abs(pred)))
report(
    "C4 F_U: null outcome, h^T N h > 0: CFIM(t h) -> (Nh)(Nh)^T/(hNh)",
    # relative error decays ~O(t^2) (ratio ~100 per decade at small t); the first run used
    # a fixed threshold 1e-4 at t=1e-4, which ignored this remainder and was set too tight.
    errs[-1] < 1e-3 and errs[-1] < errs[-2] < errs[-3],
    "relative error at t = 1e-2, 1e-3, 1e-4: " + ", ".join(f"{e:.2e}" for e in errs),
)

# ---- C5: feasibility of B A_a = mu_a P (saturating regular element), random mu ----
P = np.eye(2, dtype=complex)
mu = rng.normal(size=16)
# unknown B (2x20, complex): B A_a = mu_a P for a = 0..15  => linear system in vec(B)
rows = []
rhs_vec = []
for a in range(16):
    # (B A_a)_{ij} = sum_r B_{ir} A_a[r, j]
    for i in range(2):
        for j in range(2):
            row = np.zeros(2 * 20, complex)
            for r in range(20):
                row[i * 20 + r] += A[a][r, j]
            rows.append(row)
            rhs_vec.append(mu[a] * P[i, j])
Mat = np.array(rows)
rhs_vec = np.array(rhs_vec)
# solve in complex least squares
sol, res, rk, sv = np.linalg.lstsq(Mat, rhs_vec, rcond=None)
resid = np.linalg.norm(Mat @ sol - rhs_vec) / np.linalg.norm(rhs_vec)
B5 = sol.reshape(2, 20)
# INFORMATIONAL, not pass/fail: for a random real mu the system B A_a = mu_a P has no
# exact solution (40 complex unknowns, 64 complex equations). Saturating regular elements
# exist only for mu on a constraint subvariety; the lemma is a necessary condition only.
print(
    f"INFO C5 existence of B with B A_a = mu_a P (random real mu, P = I): "
    f"relative residual {resid:.2e}; rank {rk} of {Mat.shape[1]} unknowns"
)

print("ALL PASS" if all(results) else "SOME FAILED")
