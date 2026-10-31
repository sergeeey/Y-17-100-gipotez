# WHY: differential numerical control with a POSITIVE reference (S+ at theta = 0, many outcomes) and a sensitivity test.
# Harness:  given a finite POVM {E_k} on C^22 and a parameter set S, compute
#           F_E(0) = sum_k dp_k dp_k^T / p_k  (regular outcomes) and  F^Q(0) = Re tr(rho0 L_a L_b),
#           with rho0 = Q (+) 0, L_a = [[0, A_a^H],[A_a,0]], d_a rho = [X_a, rho0], X_a = [[0,-G^H],[G,0]], G = A/2.
# POVM:     the S+ certificate's moments M_j (float, from exact_sdp2_M.pkl) are turned into rank-one elements by
#           lemma D (Cholesky + Householder), u = (x_j ; sum_a chat_a B_{j,a}), E = omega u u^H  (1764 outcomes).
# Controls:
#   POS:  S+ parameters, the S+ POVM -> deficit must be ~ 0 (saturation known to exist).
#   NEG:  S- parameters, the SAME S+ POVM -> deficit must be clearly > 0 (it is a different parameter set).
#   SENS: S+ POVM perturbed by relative 1e-3 -> deficit must become visibly > 0 (harness sensitivity).
# This is a numerical harness check, not a proof.  Output: logs/control_differential.json.
import json
import os
import pickle
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from ys_space import load_A  # noqa: E402

D = pickle.load(open(os.path.join(STAGE, "logs", "exact_bases2.pkl"), "rb"))
S = pickle.load(open(os.path.join(STAGE, "logs", "exact_sdp2_M.pkl"), "rb"))
dirs, bases = D["dirs"], D["bases_exact"]
Mf = S["M"]
J = len(dirs)


def cf(s):
    return float(Fraction(str(s)))


X = np.array(
    [[complex(cf(a0r), cf(a0i)), complex(cf(a1r), cf(a1i))] for (a0r, a0i), (a1r, a1i) in dirs]
)
B = []
for j in range(J):
    m = len(bases[j])
    Bj = np.zeros((20, m), complex)
    for v in range(m):
        for r in range(20):
            Bj[r, v] = complex(cf(bases[j][v][r][0]), cf(bases[j][v][r][1]))
    B.append(Bj)


def lemmaD_elements(M, x, Bj):
    """Rank-one elements (22-vectors) and weights from a PD moment matrix M (n x n, n = m+1), via lemma D."""
    n = M.shape[0]
    C = np.linalg.cholesky(M)
    w = C.T[:, n - 1]
    nw = np.linalg.norm(w)
    u = w / nw
    h = np.ones(n) / np.sqrt(n)
    if np.allclose(u, h):
        O = np.eye(n)
    else:
        v = u - h
        O = np.eye(n) - 2.0 * np.outer(v, v) / (v @ v)
    Cp = C @ O
    s = nw / np.sqrt(n)
    omega = s * s
    out = []
    for k in range(n):
        chat = Cp[:, k] / s  # last coordinate 1
        y = Bj @ chat[: n - 1]  # 20-vector
        uvec = np.concatenate(
            [x * chat[n - 1], y]
        )  # (x ; y), x-part with coefficient 1 (scaling absorbed)
        out.append((omega, uvec))
    return out


def povm_splus(eps=0.0, rng=None):
    els = []
    for j in range(J):
        M = Mf[j].real
        if eps and rng is not None:
            M = M * (1 + eps * rng.standard_normal(M.shape))
            M = 0.5 * (M + M.T)
        for omega, uvec in lemmaD_elements(M, X[j], B[j]):
            els.append((omega, uvec))
    return els


def family_data(Aset):
    n = len(Aset)
    Q = np.diag([1 / 3, 2 / 3])
    rho0 = np.zeros((22, 22), complex)
    rho0[:2, :2] = Q
    Ls, drho = [], []
    for Ai in Aset:
        G = Ai / 2
        Xa = np.zeros((22, 22), complex)
        Xa[:2, 2:] = -G.conj().T
        Xa[2:, :2] = G
        L = np.zeros((22, 22), complex)
        L[:2, 2:] = Ai.conj().T
        L[2:, :2] = Ai
        Ls.append(L)
        drho.append(Xa @ rho0 - rho0 @ Xa)
    FQ = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            FQ[a, b] = np.trace(rho0 @ (Ls[a] @ Ls[b] + Ls[b] @ Ls[a]) / 2).real
    return rho0, drho, FQ


def harness(els, Aset):
    rho0, drho, FQ = family_data(Aset)
    n = len(Aset)
    Fm = np.zeros((n, n))
    tot_w = 0.0
    I22 = np.zeros((22, 22), complex)
    for omega, uvec in els:
        E = omega * np.outer(uvec, uvec.conj())
        I22 += E
        p = np.trace(rho0 @ E).real
        if p <= 1e-14:
            continue
        g = np.array([np.trace(E @ drho[a]).real for a in range(n)])
        Fm += np.outer(g, g) / p
    compl = float(np.abs(I22 - np.eye(22)).max())
    tF = float(np.trace(FQ))
    tFm = float(np.trace(Fm))
    return {
        "completeness_max_err": compl,
        "trace_QFIM": tF,
        "trace_classical_FI": tFm,
        "deficit": tF - tFm,
        "relative_deficit": (tF - tFm) / tF,
        "matrix_max_abs_err_QFIM_minus_CFI": float(np.abs(FQ - Fm).max()),
        "n_outcomes": len(els),
    }


A_plus = load_A(list(range(0, 12)))
A_minus = load_A(list(range(4, 16)))
Aplus = [A_plus[i] for i in range(0, 12)]
Aminus = [A_minus[i] for i in range(4, 16)]
els_plus = povm_splus()
res = {}
res["POS_splus_params_splus_povm"] = harness(els_plus, Aplus)
res["NEG_sminus_params_splus_povm"] = harness(els_plus, Aminus)
rng = np.random.default_rng(1)


def recomplete(els):
    # E_k -> S^{-1/2} E_k S^{-1/2}, S = sum_k E_k : keeps a valid complete POVM
    Ssum = sum(om * np.outer(u, u.conj()) for om, u in els)
    w_, U_ = np.linalg.eigh((Ssum + Ssum.conj().T) / 2)
    Sih_ = U_ @ np.diag(1 / np.sqrt(w_)) @ U_.conj().T
    return [(om, Sih_ @ u) for om, u in els]


# sensitivity curve: the harness must detect growing perturbations (deficit grows with the size of the break)
for eps_s in (1e-3, 1e-2, 3e-2):
    # 0.1 breaks positive definiteness of the moments (Cholesky fails), so the curve stops at 3e-2
    els_pert = recomplete(povm_splus(eps=eps_s, rng=np.random.default_rng(1)))
    res[f"SENS_eps_{eps_s:g}_splus_params"] = harness(els_pert, Aplus)
res["notes"] = [
    "POS must give relative deficit ~ 0 (saturation at theta=0 by the S+ construction).",
    "NEG: S+ POVM evaluated on S- parameters: deficit must be clearly positive.",
    "SENS: 1e-3 relative perturbation of moments must produce a visible deficit (harness is sensitive).",
    "Numerical harness check only; not a proof.",
]
json.dump(res, open(os.path.join(STAGE, "logs", "control_differential.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
