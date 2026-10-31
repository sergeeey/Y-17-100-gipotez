# WHY: independent NUMERICAL control (not a proof) for Theorem Q / N.  Maximise the trace of the classical
# Fisher information of a K-outcome POVM at a point theta = s*h, and report the deficit tr F^Q - max tr F_E.
#  - SLD and QFIM are computed directly from the family: rho_theta = expm(sum theta X) rho0 expm(-...), and
#    L_a from  rho L + L rho = 2 d_a rho  in the eigenbasis of rho (exact formula, no Omega-integral).
#  - POVM: E_k = S^{-1/2} v_k v_k^H S^{-1/2}, S = sum v_k v_k^H  (automatically complete).
# Control: S+ = {0..11} at small s should reach deficit ~ 0 for growing K; S- = {4..15} should keep a deficit.
# Output: logs/control_min_deficit_<set>.json.  NOT a certificate: it can only suggest a counterexample.
import json
import os
import sys

import numpy as np
from scipy.linalg import expm, sqrtm
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from ys_space import load_A  # noqa: E402

which = sys.argv[1] if len(sys.argv) > 1 else "minus"
K = int(sys.argv[2]) if len(sys.argv) > 2 else 24
s = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
S_SET = list(range(4, 16)) if which == "minus" else list(range(0, 12))
A = load_A(S_SET)
n = len(S_SET)
D = 22
R = 2
Q = np.diag([1 / 3, 2 / 3])
rho0 = np.zeros((D, D), complex)
rho0[:R, :R] = Q


def gen_X(Ai):
    X = np.zeros((D, D), complex)
    X[:R, R:] = -Ai.conj().T / 2
    X[R:, :R] = Ai / 2
    return X


Xs = [gen_X(A[i]) for i in S_SET]
h = np.ones(n) / np.sqrt(n)  # direction (fixed)
Th = sum(hk * Xk for hk, Xk in zip(h, Xs)) * s
U = expm(Th)
rho = U @ rho0 @ U.conj().T
# derivative of rho along each parameter at theta: d_a rho = U[ Omega_a, rho0 ] U^H, with Omega_a = U^H d_a U.
# Use finite differences of the exact family for robustness:
eps = 1e-6
drho = []
for a in range(n):
    Ua_p = expm(Th + eps * Xs[a])
    Ua_m = expm(Th - eps * Xs[a])
    drho.append((Ua_p @ rho0 @ Ua_p.conj().T - Ua_m @ rho0 @ Ua_m.conj().T) / (2 * eps))
# SLD in eigenbasis of rho
lam, W = np.linalg.eigh(rho)
L = []
for a in range(n):
    dr = W.conj().T @ drho[a] @ W
    Lt = np.zeros((D, D), complex)
    for i in range(D):
        for j in range(D):
            if lam[i] + lam[j] > 1e-12:
                Lt[i, j] = 2 * dr[i, j] / (lam[i] + lam[j])
    L.append(W @ Lt @ W.conj().T)
# checks: SLD equation and QFIM
sld_err = max(np.abs(rho @ L[a] + L[a] @ rho - 2 * drho[a]).max() for a in range(n))
FQ = np.zeros((n, n))
for a in range(n):
    for b in range(n):
        FQ[a, b] = np.trace(rho @ (L[a] @ L[b] + L[b] @ L[a]) / 2).real
trFQ = float(np.trace(FQ))

dpar = np.array([[np.trace(0 * rho)] for _ in range(1)])  # placeholder to keep shapes explicit


def unpack(x):
    re = x[: D * K].reshape(K, D)
    im = x[D * K :].reshape(K, D)
    return re + 1j * im


def fisher_trace(x):
    V = unpack(x)  # K x D vectors
    Sm = V.T @ V.conj()  # sum v v^H  (D x D)
    w, Uu = np.linalg.eigh((Sm + Sm.conj().T) / 2)
    Sih = Uu @ np.diag(1 / np.sqrt(np.maximum(w, 1e-14))) @ Uu.conj().T
    tot = 0.0
    Fm = np.zeros((n, n))
    for k in range(K):
        u = Sih @ V[k]
        Ek_p = np.outer(u, u.conj())
        p = np.trace(rho @ Ek_p).real
        if p <= 1e-14:
            continue
        g = np.array([np.trace(Ek_p @ drho[a]).real for a in range(n)])
        Fm += np.outer(g, g) / p
    return np.trace(Fm)


rng = np.random.default_rng(0)
best = None
for trial in range(3):
    x0 = rng.standard_normal(2 * D * K) * 0.3
    res = minimize(lambda x: -fisher_trace(x), x0, method="L-BFGS-B", options={"maxiter": 400})
    val = -res.fun
    if best is None or val > best:
        best = val
deficit = trFQ - best
out = {
    "set": which,
    "S": S_SET,
    "K_outcomes": K,
    "s": s,
    "direction": "uniform (1/sqrt(12) each)",
    "sld_equation_max_err": float(sld_err),
    "trace_QFIM": trFQ,
    "best_trace_classical_FI_found": float(best),
    "deficit_found": float(deficit),
    "note": "numerical control, lower bound on the achievable classical FI only; not a proof",
}
json.dump(
    out, open(os.path.join(STAGE, "logs", f"control_min_deficit_{which}_K{K}.json"), "w"), indent=1
)
print(json.dumps(out, indent=1))
