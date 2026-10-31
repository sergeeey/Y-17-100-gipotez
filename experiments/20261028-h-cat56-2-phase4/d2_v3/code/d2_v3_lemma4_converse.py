"""Converse of Lemma 4 on S = {4..15} (0-based), checked by search, not by construction.

Lemma 4 (converse): if rank N^S(yy^dag) <= 1 then there exist z in C^2 and real lambda_a
(a in S) with A_a^dag y = lambda_a * Q^{-1/2} z, i.e. y in Y_S.

Test: minimise  f(y) = sigma_2(N^S) / sigma_1(N^S)  over y in C^20 (||y|| = 1) from many random
starts. Each minimiser with f ~ 0 is a rank-<=1 point. For each such point check membership in
Y_S: T_a := A_a^dag y (a in S); membership <=> exists z with T_a = lambda_a z, lambda_a real.
Also record how often f reaches ~0 with NON-real ratios (that would falsify the converse).

Run: python -I d2_v3_lemma4_converse.py
"""

import sys
import numpy as np
from scipy.optimize import minimize

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
A = [A_all[a] for a in S]
nS = len(S)
Q = np.diag([1 / 3, 2 / 3]).astype(complex)
Qh = np.diag(np.sqrt([1 / 3, 2 / 3])).astype(complex)  # Q^{1/2}
rng = np.random.default_rng(20261101)


def vec_to_y(v):
    y = v[:20] + 1j * v[20:]
    return y / np.linalg.norm(y)


def N_S(y):
    """N^S_{ab} = Re tr(D A_a Q A_b^dag), D = y y^dag, a,b in S (real symmetric 12x12)."""
    D = np.outer(y, y.conj())
    return np.array(
        [[np.real(np.trace(D @ A[a] @ Q @ A[b].conj().T)) for b in range(nS)] for a in range(nS)]
    )


def f(v):
    y = vec_to_y(v)
    s = np.linalg.svd(N_S(y), compute_uv=False)
    return (s[1] / s[0]) ** 2


def membership(y):
    """Return (max residual of 'T_a = lambda_a z with real lambda', z-unit-norm choice)."""
    T = np.array([A[a].conj().T @ y for a in range(nS)])  # nS x 2 complex
    norms = np.linalg.norm(T, axis=1)
    a0 = int(np.argmax(norms))
    if norms[a0] < 1e-12:
        return 0.0  # y in Y_S(0)
    z = T[a0] / norms[a0]
    worst = 0.0
    for a in range(nS):
        c = np.vdot(z, T[a])  # complex coefficient c_a with T_a ~ c_a z
        resid_line = np.linalg.norm(T[a] - c * z)
        worst = max(worst, resid_line, abs(c.imag))
    return worst


def ker_realified_rank(y):
    """Real rank of the realified Gram matrix = rank N^S (sanity: must equal numpy rank)."""
    G = []
    for a in range(nS):
        g = Qh @ A[a].conj().T @ y
        G.append(np.concatenate([g.real, g.imag]))
    return np.linalg.matrix_rank(np.array(G), tol=1e-10)


# ---- search ----
n_starts = 60
hits = []
for s in range(n_starts):
    v0 = rng.normal(size=40)
    res = minimize(f, v0, method="BFGS", options={"gtol": 1e-12, "maxiter": 2000})
    val = res.fun
    if val < 1e-9:
        y = vec_to_y(res.x)
        hits.append(
            (val, membership(y), ker_realified_rank(y), np.linalg.matrix_rank(N_S(y), tol=1e-7))
        )

print(f"starts: {n_starts}; minimisers with sigma2/sigma1 < 1e-9: {len(hits)}")
if hits:
    worst_membership = max(h[1] for h in hits)
    rank_agree = all(h[2] == h[3] for h in hits)
    print(f"max membership residual over rank-<=1 minimisers: {worst_membership:.3e}")
    print(f"realified rank == numpy rank of N^S on all hits: {rank_agree}")
    ok = worst_membership < 1e-6 and rank_agree
else:
    print("no rank-<=1 minimiser found: search is inconclusive (not a proof)")
    ok = None

# ---- control: the forward construction (y in Y_S(z)) must give membership residual ~ 0 ----
z = rng.normal(size=2) + 1j * rng.normal(size=2)
Mat = []
for a in range(nS):
    Ad = A[a].conj().T
    for i in range(2):
        r_re = np.zeros(40 + nS)
        r_im = np.zeros(40 + nS)
        r_re[:20] = Ad[i].real
        r_re[20:40] = -Ad[i].imag
        r_im[:20] = Ad[i].imag
        r_im[20:40] = Ad[i].real
        r_re[40 + a] = -z[i].real
        r_im[40 + a] = -z[i].imag
        Mat.append(r_re)
        Mat.append(r_im)
Mat = np.array(Mat)
_, sv, vh = np.linalg.svd(Mat)
ker = vh[np.sum(sv > 1e-10) :]
sol = ker.T @ rng.normal(size=ker.shape[0])
y_ctrl = sol[:20] + 1j * sol[20:40]
if np.linalg.norm(y_ctrl) > 1e-10:
    y_ctrl = y_ctrl / np.linalg.norm(y_ctrl)
    print(
        f"control y in Y_S(z): membership residual {membership(y_ctrl):.3e}; "
        f"sigma2/sigma1 = {f(np.concatenate([y_ctrl.real, y_ctrl.imag])):.3e}"
    )
print("RESULT:", "PASS" if ok else ("INCONCLUSIVE" if ok is None else "FAIL"))
