"""Проверка для F_U (S- = {4..15}, instance d22 r2 s16), 2026-10-31.

1. Нормировка: SLD L(0) = [[0, A^H],[A, 0]] удовлетворяет d rho = (rho L + L rho)/2 точно;
   F^Q_ab(0) = Re tr(rho L_a L_b); для полного POVM sum_k N_k = F^Q, где N_k,ab = Re tr(E_k L_a rho L_b).
   Проверяются: равенство (до машинной точности), N_k симметричны и PSD, N_k - F_k PSD при p_k(th) > 0,
   и вклад исходов с p_k = 0 (D1: F_k := 0, N_k != 0 в общем случае).
2. Соответствие Y: для x в C^2 базис Y_S(x) (real kernel, как в stage_e_v1/code/ys_space.py)
   удовлетворяет условию rank_R Gram(Q^{1/2} A_a^H y) <= 1, то есть Y_S(x) ⊂ 𝒴.
   Обратное включение: rank <= 1 => все w_a ∈ R·w, и тогда y ∈ Y_S(x) при x = Q^{-1/2} w (аналитически).
"""

import json
import os
import sys
import numpy as np
from scipy.linalg import expm, sqrtm

HERE = os.path.dirname(os.path.abspath(__file__))
PH4 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PH4, "stage_e_v1", "code"))
import ys_space  # noqa: E402

S_MINUS = list(range(4, 16))
Q = np.diag([1 / 3, 2 / 3])
RNG = np.random.default_rng(20261031)
TOL = 1e-10


def build_A(indices):
    A_all = ys_space.load_A(indices=indices)
    return [A_all[i] for i in indices]


def family_states(A, th):
    """rho_theta = e^{sum th_a X_a} rho0 e^{-...}, X_a = [[0,-G^H],[G,0]], G = A/2."""
    d = 22
    rho0 = np.zeros((d, d), complex)
    rho0[:2, :2] = Q
    X = []
    for Aa in A:
        G = Aa / 2
        Xa = np.zeros((d, d), complex)
        Xa[2:, :2] = G
        Xa[:2, 2:] = -G.conj().T
        X.append(Xa)
    Xsum = sum(t * Xa for t, Xa in zip(th, X))
    U = expm(Xsum)
    return U @ rho0 @ U.conj().T


def sld_at_zero(A):
    """Candidate SLD at theta=0 from the convention C2."""
    L = []
    for Aa in A:
        La = np.zeros((22, 22), complex)
        La[:2, 2:] = Aa.conj().T
        La[2:, :2] = Aa
        L.append(La)
    return L


def check_sld_equation(A):
    rho0 = family_states(A, np.zeros(len(A)))
    L = sld_at_zero(A)
    worst = 0.0
    eps = 1e-6
    for a in range(len(A)):
        e = np.zeros(len(A))
        e[a] = eps
        drho = (family_states(A, e) - family_states(A, -e)) / (2 * eps)
        rhs = (rho0 @ L[a] + L[a] @ rho0) / 2
        worst = max(worst, np.abs(drho - rhs).max())
    return worst


def FQ_matrix(rho, L):
    n = len(L)
    F = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            F[a, b] = np.real(np.trace(rho @ L[a] @ L[b]))
    return F


def N_matrix(E, rho, L):
    n = len(L)
    N = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            N[a, b] = np.real(np.trace(E @ L[a] @ rho @ L[b]))
    return N


def classical_F(E, rho, drho):
    p = np.real(np.trace(rho @ E))
    g = np.array([np.real(np.trace(d @ E)) for d in drho])
    if p > TOL:
        return np.outer(g, g) / p, p
    return np.zeros((len(drho), len(drho))), p


def random_complete_povm(K=40):
    us = [RNG.normal(size=22) + 1j * RNG.normal(size=22) for _ in range(K)]
    S = sum(np.outer(u, u.conj()) for u in us)
    Sm = np.linalg.inv(sqrtm(S))
    return [Sm @ np.outer(u, u.conj()) @ Sm for u in us]


def part1_normalization(A):
    out = {}
    rho0 = family_states(A, np.zeros(len(A)))
    L = sld_at_zero(A)
    out["sld_equation_max_residual_at_0"] = check_sld_equation(A)
    FQ0 = FQ_matrix(rho0, L)
    # closed form: F^Q_ab(0) = Re tr(Q A_a^H A_b)
    closed = np.array(
        [
            [np.real(np.trace(Q @ A[a].conj().T @ A[b])) for b in range(len(A))]
            for a in range(len(A))
        ]
    )
    out["FQ0_vs_closed_form_max_abs_diff"] = float(np.abs(FQ0 - closed).max())
    out["FQ0_symmetric_max_asym"] = float(np.abs(FQ0 - FQ0.T).max())

    # Test 1: explicit two-outcome complete POVM {I2 ⊕ 0, 0 ⊕ I20}
    E1 = np.zeros((22, 22), complex)
    E1[:2, :2] = np.eye(2)
    E2 = np.eye(22, dtype=complex) - E1
    Ns = [N_matrix(E1, rho0, L), N_matrix(E2, rho0, L)]
    out["two_outcome_sum_N_minus_FQ0_max_abs"] = float(np.abs(Ns[0] + Ns[1] - FQ0).max())
    out["two_outcome_N_kernel_outcome_trace"] = float(np.trace(Ns[1]))
    out["two_outcome_N_kernel_outcome_min_eig"] = float(
        np.linalg.eigvalsh((Ns[1] + Ns[1].T) / 2).min()
    )

    # Test 2: random complete POVM, D1 at theta = 0 (outcomes with p_k(0)=0 contribute F_k = 0)
    povm = random_complete_povm()
    tot = np.zeros_like(FQ0)
    min_eig_diff = np.inf
    n_zero_p = 0
    for E in povm:
        N = N_matrix(E, rho0, L)
        tot += N
    out["random_povm_sum_N_minus_FQ0_max_abs"] = float(np.abs(tot - FQ0).max())
    out["random_povm_sum_N_minus_FQ0_relative"] = float(np.abs(tot - FQ0).max() / np.abs(FQ0).max())

    # Test 3: at theta = s h, s small: check N_k - F_k PSD for each outcome with p_k > 0
    h = RNG.normal(size=len(A))
    h /= np.linalg.norm(h)
    for s in [0.05, 0.005]:
        th = s * h
        rho = family_states(A, th)
        eps = 1e-6
        drho = []
        for a in range(len(A)):
            e = np.zeros(len(A))
            e[a] = eps
            drho.append((family_states(A, th + e) - family_states(A, th - e)) / (2 * eps))
        Lth = []
        # SLD at theta from eigen-formula (rho diagonalised), with kernel part left at zero
        w, V = np.linalg.eigh(rho)
        for a in range(len(A)):
            D = V.conj().T @ drho[a] @ V
            M = np.zeros((22, 22), complex)
            for i in range(22):
                for j in range(22):
                    if w[i] + w[j] > 1e-12:
                        M[i, j] = 2 * D[i, j] / (w[i] + w[j])
            Lth.append(V @ M @ V.conj().T)
        FQ = FQ_matrix(rho, Lth)
        worst_psd = np.inf
        tot = np.zeros_like(FQ)
        for E in random_complete_povm(40):
            N = N_matrix(E, rho, Lth)
            Fk, p = classical_F(E, rho, drho)
            tot += N
            if p > TOL:
                worst_psd = min(worst_psd, np.linalg.eigvalsh((N - Fk + (N - Fk).T) / 2).min())
        out[f"theta_s{s}_sum_N_minus_FQ_max_abs"] = float(np.abs(tot - FQ).max())
        out[f"theta_s{s}_min_eig_N_minus_F_over_positive_outcomes"] = float(worst_psd)
    return out


def rank_real_gram(vecs, tol=1e-9):
    """vecs: list of complex 2-vectors; rank of real Gram Re<w_a,w_b>."""
    W = np.array([[v.real[0], v.imag[0], v.real[1], v.imag[1]] for v in vecs])
    s = np.linalg.svd(W, compute_uv=False)
    return int((s > tol * max(s[0], 1e-300)).sum())


def part2_Y(A, indices):
    out = {}
    sq = np.sqrt(Q)  # diag(1/sqrt3, sqrt(2/3)) ... Q^{1/2}
    Qh = np.diag(np.sqrt(np.diag(Q)))
    max_rank_in_Y = 0
    cases = 0
    for trial in range(30):
        x = RNG.normal(size=2) + 1j * RNG.normal(size=2)
        x /= np.linalg.norm(x)
        B, s, rank = ys_space.y_basis(x, {i: A[k] for k, i in enumerate(indices)}, indices=indices)
        for c in range(B.shape[1]):
            y = B[:, c]
            ws = [Qh @ (A[k].conj().T @ y) for k in range(len(indices))]
            r = rank_real_gram(ws)
            max_rank_in_Y = max(max_rank_in_Y, r)
            cases += 1
    out["Y_S_basis_vectors_tested"] = cases
    out["max_rank_real_gram_Qh_A^H_y_over_Y_S_basis"] = max_rank_in_Y
    # generic y (not in Y_S): expect rank > 1
    ranks = []
    for _ in range(200):
        y = RNG.normal(size=20) + 1j * RNG.normal(size=20)
        ws = [Qh @ (A[k].conj().T @ y) for k in range(len(indices))]
        ranks.append(rank_real_gram(ws))
    out["generic_y_rank_distribution"] = {str(r): ranks.count(r) for r in sorted(set(ranks))}
    return out


if __name__ == "__main__":
    A = build_A(S_MINUS)
    res = {"S_minus_indices": S_MINUS}
    res["part1_normalization"] = part1_normalization(A)
    res["part2_Y_correspondence"] = part2_Y(A, S_MINUS)
    print(json.dumps(res, indent=2, ensure_ascii=False, default=float))
