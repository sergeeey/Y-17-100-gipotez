import json, numpy as np
path = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261027-h-cat56-2-submission-package-v1/data/instance_d22_r2_s16.jsonl"
with open(path, encoding="utf-8") as fh:
    rec = json.loads(fh.readline())
blocks = rec["blocks"]
assert len(blocks) == 16 and all(len(b) == 80 for b in blocks)
A = []
for b in blocks:
    b = np.array(b, dtype=float)
    A.append((b[:40] + 1j*b[40:]).reshape(20, 2))   # re then im, row-major 20x2
d = 22
Q = np.diag([1/3, 2/3])
rho = np.zeros((d, d), complex); rho[:2, :2] = Q
def L_of(Ai):
    L = np.zeros((d, d), complex)
    L[:2, 2:] = Ai.conj().T
    L[2:, :2] = Ai
    return L
L = [L_of(Ai) for Ai in A]
# (1) family consistent with L: V(theta) = [[I2],[sum theta_i A_i / 2]], rho = V Q V^dag
def V(th):
    top = np.eye(2, dtype=complex)
    bot = sum(th[i]*A[i] for i in range(16)) / 2
    return np.vstack([top, bot])
def rho_th(th):
    v = V(th); return v @ Q @ v.conj().T
th0 = np.zeros(16)
print("rho(0) == rho on A0:", np.allclose(rho_th(th0), rho))
# SLD check: d_i rho at theta0 vs (L_i rho + rho L_i)/2
maxerr = 0
for i in range(16):
    e = np.zeros(16); e[i] = 1e-6
    drho_fd = (rho_th(e) - rho_th(-e)) / (2e-6)
    sld = (L[i] @ rho + rho @ L[i]) / 2
    maxerr = max(maxerr, np.max(np.abs(drho_fd - sld)))
print("max |d_i rho - (L_i rho + rho L_i)/2| over i=1..16:", maxerr)
# (2) identity: per-null-outcome N_E from the definition vs limit of CFIM along h
rng = np.random.default_rng(11)
S = list(range(4, 16))  # S- = {4..15}, 0-based (as in CONVENTION_RESOLUTION and the certificate)
worst_id = 0; worst_lim = 0
for trial in range(3):
    G = rng.normal(size=(20, 20)) + 1j*rng.normal(size=(20, 20))
    E = np.zeros((d, d), complex); E[2:, 2:] = G @ G.conj().T / 20   # null POVM element (support in ker rho)
    NE = np.array([[np.real(np.trace(E @ L[a] @ rho @ L[b])) for b in range(16)] for a in range(16)])
    # identity with quantum-side form Re(a_a^dag Q a_b) computed on the 2x2 level: Re tr(E00 A_a Q A_b^dag)
    alt = np.array([[np.real(np.trace(E[2:, 2:] @ A[a] @ Q @ A[b].conj().T)) for b in range(16)] for a in range(16)])
    worst_id = max(worst_id, np.max(np.abs(NE - alt)))
    # D2 limit along h: p_E(theta0 + t h) and its gradient, numerically
    h = rng.normal(size=16)
    for t in [1e-3, 1e-4]:
        th = t*h
        pE = lambda th_: np.real(np.trace(rho_th(th_) @ E))
        g = np.zeros(16)
        for u in range(16):
            e = np.zeros(16); e[u] = 1e-7
            g[u] = (pE(th + e) - pE(th - e)) / (2e-7)
        Fl = np.outer(g, g) / pE(th)
        # restrict to S- block to keep the comparison in the 12x12 quantum block
        Fl_S = Fl[np.ix_(S, S)]
        pred = np.outer(NE @ h, NE @ h) / (h @ NE @ h)
        pred_S = pred[np.ix_(S, S)]
        worst_lim = max(worst_lim, np.max(np.abs(Fl_S - pred_S)) / np.max(np.abs(pred_S)))
    p_ratio = pE(t*h) / (t*t*(h @ NE @ h) / 4)
    print(f"trial {trial}: |N_E - Re tr(E00 A Q A^dag)| = {np.max(np.abs(NE-alt)):.2e}; p/(t^2 hNh/4) at t=1e-4 = {p_ratio:.6f}")
print("worst identity error:", worst_id)
print("worst relative error of D2 limit vs (N_E h)(N_E h)^T/(h N_E h), S-block:", worst_lim)
