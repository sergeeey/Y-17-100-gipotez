# WHY: numerical check of the model convention used by S+ (THEOREM_S_PLUS_EXISTENCE_v6.md, sections 0-1).
# Reads the canonical instance exactly as FORMAT.md specifies (flat[c*2+a] = Re, flat[40+c*2+a] = Im),
# builds A_i = -2i B_i (= 2 Im - 2i Re), the SLD L_i = [[0, A_i^dag],[A_i, 0]], the generator
# X_i = [[0, -A_i^dag/2],[A_i/2, 0]] and the state family rho(theta) = e^{X(theta)} rho0 e^{-X(theta)},
# rho0 = diag(Q, 0), Q = diag(1/3, 2/3) (normalised version of the FORMAT state diag(1,2), Tr = 3).
# Checks, numerically (float64, high-precision finite differences are not needed: the derivative is analytic):
#   (a) X_i is anti-Hermitian, so e^{X} is unitary;
#   (b) d/dtheta_i rho at 0, by central finite difference of the matrix exponential, equals [X_i, rho0];
#   (c) the SLD equation  d_i rho = (rho L_j + L_j rho)/2  holds for the claimed L_j (for j = i);
#   (d) QFIM: Tr(rho (L_i L_j + L_j L_i)/2)  ==  Re Tr(Q A_i^dag A_j) for all pairs in S+ = {0..11}.
#   (e) the instance blocks decoded with FORMAT.md agree with the loader used by ys_space.py (A = 2 im - 2i re).
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INST = os.path.join(
    HERE,
    "..",
    "..",
    "..",
    "20261027-h-cat56-2-submission-package-v1",
    "data",
    "instance_d22_r2_s16.jsonl",
)
INST = os.path.normpath(INST)
K, R = 20, 2
S_PLUS = list(range(12))

row = json.loads(open(INST, encoding="utf-8").readline())
blocks = [np.array(x, dtype=float) for x in row["blocks"]]


def decode_FORMAT(flat):
    Re = np.array([[flat[c * 2 + a] for a in range(2)] for c in range(20)])
    Im = np.array([[flat[40 + c * 2 + a] for a in range(2)] for c in range(20)])
    return Re, Im


A = {}
for i in S_PLUS:
    Re, Im = decode_FORMAT(blocks[i])
    B = Re + 1j * Im  # B_i = Re + i Im
    A[i] = -2j * B  # A_i = -2i B_i
    # (e) loader agreement with ys_space.load_A
    flat = blocks[i]
    re_ = flat[:40].reshape(20, 2)
    im_ = flat[40:80].reshape(20, 2)
    assert np.allclose(A[i], 2.0 * im_ - 2j * re_), "loader mismatch"

D = K + R
Q = np.diag([1.0 / 3.0, 2.0 / 3.0])


def embed_L(Ai):
    L = np.zeros((D, D), dtype=complex)
    L[:R, R:] = Ai.conj().T
    L[R:, :R] = Ai
    return L


def gen_X(Ai):
    X = np.zeros((D, D), dtype=complex)
    X[:R, R:] = -Ai.conj().T / 2
    X[R:, :R] = Ai / 2
    return X


rho0 = np.zeros((D, D), dtype=complex)
rho0[:R, :R] = Q


def expm_antiherm(X):
    # X anti-Hermitian: e^X = V diag(e^{i w}) V^dag with (iX) Hermitian = V diag(w) V^dag ... careful: iX Hermitian
    H = 1j * X
    w, V = np.linalg.eigh(H)  # iX = V diag(w) V^dag  ->  X = V diag(-i w) V^dag
    return V @ np.diag(np.exp(-1j * w)) @ V.conj().T


res = {"instance": INST, "checks": {}}
# (a) anti-Hermitian generators
res["checks"]["a_antiherm_max_dev"] = max(
    np.abs(gen_X(A[i]) + gen_X(A[i]).conj().T).max() for i in S_PLUS
)

# (b),(c): derivative and SLD equation for the first generator and all of S+ (separately)
h = 1e-6
max_deriv_err = 0.0
max_sld_err = 0.0
for i in S_PLUS:
    X = gen_X(A[i])

    def rho_of(t):
        U = expm_antiherm(t * X)
        return U @ rho0 @ U.conj().T

    drho_num = (rho_of(h) - rho_of(-h)) / (2 * h)
    drho_an = X @ rho0 - rho0 @ X
    max_deriv_err = max(max_deriv_err, np.abs(drho_num - drho_an).max())
    L = embed_L(A[i])
    rhs = (rho0 @ L + L @ rho0) / 2
    max_sld_err = max(max_sld_err, np.abs(drho_an - rhs).max())
res["checks"]["b_derivative_vs_commutator_max_err"] = float(max_deriv_err)
res["checks"]["c_SLD_equation_max_err"] = float(max_sld_err)

# (d) QFIM
max_qfim_err = 0.0
Fmat = np.zeros((len(S_PLUS), len(S_PLUS)))
for ii, i in enumerate(S_PLUS):
    for jj, j in enumerate(S_PLUS):
        Li, Lj = embed_L(A[i]), embed_L(A[j])
        F_sld = np.trace(rho0 @ (Li @ Lj + Lj @ Li) / 2).real
        F_formula = np.trace(Q @ A[i].conj().T @ A[j]).real
        Fmat[ii, jj] = F_sld
        max_qfim_err = max(max_qfim_err, abs(F_sld - F_formula))
res["checks"]["d_QFIM_sld_vs_formula_max_err"] = float(max_qfim_err)
res["checks"]["QFIM_S+_min_eig"] = float(np.linalg.eigvalsh((Fmat + Fmat.T) / 2).min())

print(json.dumps(res, indent=1))
