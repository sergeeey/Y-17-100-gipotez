"""Stage B check 2: point / limit / directional CFIM on the canonical A0 instance.

Family used for the limit computations (constant rank 2, realises the first-order data rho, L_i of A0):
    rho_theta = U_theta rho U_theta^dag,  U_theta = expm(sum_i theta_i X_i),  X_i = [[0,-B_i^dag],[B_i,0]],  B_i = A_i/2.
Check: d_i rho = [X_i, rho] = (1/2){rho, L_i} at theta = 0.
Rank-increasing family with the SAME first-order data (control for "limit depends on the family"):
    rho'_theta = (1 - c |theta|^2) rho_theta + c |theta|^2 sigma,  sigma = kernel projector.
Usage: python -I b2_conventions_A0.py <instance.jsonl> <povm.npz> <out.json>
"""
import json, os, sys
import numpy as np
from scipy.linalg import expm

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.normpath(os.path.join(HERE, "..", "..", "20261027-h-cat56-2-discovery", "code"))
sys.path.insert(0, OLD)
import s8_admissible_span as sa  # noqa: E402
import s11_cone_saturation as s11  # noqa: E402

path, npz, out = sys.argv[1:4]
As = sa.load_A(path)
RHO = np.diag([1 / 3, 2 / 3] + [0.0] * 20).astype(complex)
rng = np.random.default_rng(20261028)
res = {}


def X_of(i):
    B = As[i] / 2
    X = np.zeros((22, 22), dtype=complex)
    X[:2, 2:] = -B.conj().T
    X[2:, :2] = B
    return X


def rho_theta(Xs, th, c2=0.0, sigma=None):
    U = expm(sum(t * X for t, X in zip(th, Xs)))
    r = U @ RHO @ U.conj().T
    if c2:
        d = c2 * float(th @ th)
        r = (1 - d) * r + d * sigma
    return r


def fd_grad_p(Xs, th, E, c2=0.0, sigma=None, eps=1e-6):
    g = np.zeros(len(th))
    for i in range(len(th)):
        e = np.zeros(len(th)); e[i] = eps
        pp = np.real(np.trace(rho_theta(Xs, th + e, c2, sigma) @ E))
        pm = np.real(np.trace(rho_theta(Xs, th - e, c2, sigma) @ E))
        g[i] = (pp - pm) / (2 * eps)
    return g


# ---------- sanity: family realises the SLD first-order data ----------
S2 = [0, 1]
Xs2 = [X_of(i) for i in S2]
Ls2 = s11.sld_ops(As, S2)
err = 0.0
for X, L in zip(Xs2, Ls2):
    err = max(err, np.linalg.norm((X @ RHO - RHO @ X) - 0.5 * (RHO @ L + L @ RHO)))
res["family_first_order_err"] = float(err)

# ---------- part 1: S+ POVM, all outcomes regular -> point = limit ----------
S = list(range(12))
Xs = [X_of(i) for i in S]
z = np.load(npz, allow_pickle=True)
w, V = z["weights"], z["vectors"]
FQ = s11.qfi_subset(As, S)
elems = [wk * np.outer(v, v.conj()) for wk, v in zip(w, V)]
F0 = s11.cfi_of_povm(As, S, elems)


def FC_at(th):
    r = rho_theta(Xs, th)
    p = np.real(np.einsum("ki,ij,kj->k", V.conj(), r, V)) * w
    dr = []
    eps = 1e-6
    for i in range(len(S)):
        e = np.zeros(len(S)); e[i] = eps
        dr.append((rho_theta(Xs, th + e) - rho_theta(Xs, th - e)) / (2 * eps))
    dp = np.array([np.real(np.einsum("ki,ij,kj->k", V.conj(), d, V)) * w for d in dr])  # (12, 280)
    return (dp / p) @ dp.T


h = rng.normal(size=12); h /= np.linalg.norm(h)
rows = []
for t in [1e-2, 1e-3, 1e-4]:
    Ft = FC_at(t * h)
    rows.append({"t": t, "norm(F_C(theta0+t h) - F_C(theta0))": float(np.linalg.norm(Ft - F0)),
                 "norm(F_C(theta0+t h) - F_Q)": float(np.linalg.norm(Ft - FQ))})
res["splus_limit_vs_point"] = {
    "norm(F_C(theta0) - F_Q)": float(np.linalg.norm(F0 - FQ)), "norm(F_Q)": float(np.linalg.norm(FQ)),
    "rows": rows}

# ---------- part 2: a null outcome with rank-one N on S={0,1} ----------
c = 0.7
M = (As[0] - c * As[1]).conj().T  # 2 x 20, y in its kernel => A_0^dag y = c A_1^dag y
_, _, Vh = np.linalg.svd(M)
ker = Vh[2:].conj().T  # 20 x 18
y = ker @ (rng.normal(size=18) + 1j * rng.normal(size=18)); y /= np.linalg.norm(y)
wv = np.concatenate([np.zeros(2), y]); E = np.outer(wv, wv.conj())
a = [As[i].conj().T @ y for i in S2]
Q = np.diag([1 / 3, 2 / 3])
N = np.array([[np.real(a[i].conj() @ Q @ a[j]) for j in range(2)] for i in range(2)])
res["null_demo"] = {"c": c, "N": N.tolist(), "N_eigs": np.linalg.eigvalsh(N).tolist(),
                    "p_E_at_theta0": float(np.real(np.trace(RHO @ E))),
                    "pure_check_norm(A_i^dag y)": [float(np.linalg.norm(x)) for x in a]}
n = np.array([c, 1.0]); n = n / np.linalg.norm(n)
sigma = E.copy()  # kernel projector used for the rank-increasing control
c2 = 0.5
dirs = {"generic h=(1,0.3)": np.array([1.0, 0.3]),
        "h orthogonal to range(N)": np.array([n[1], -n[0]])}
demo = {}
for name, hh in dirs.items():
    hh = hh / np.linalg.norm(hh)
    pred_p = 0.25 * hh @ N @ hh
    pred_F = np.outer(N @ hh, N @ hh) / (hh @ N @ hh) if hh @ N @ hh > 1e-12 else None
    rows = []
    for t in [1e-1, 1e-2]:
        th = t * hh
        p = float(np.real(np.trace(rho_theta(Xs2, th) @ E)))
        g = fd_grad_p(Xs2, th, E)
        Fnull = np.outer(g, g) / p if p > 1e-300 else None
        p2 = float(np.real(np.trace(rho_theta(Xs2, th, c2, sigma) @ E)))
        g2 = fd_grad_p(Xs2, th, E, c2, sigma)
        F2 = np.outer(g2, g2) / p2
        rows.append({"t": t, "p/t^2": p / t**2, "pred hNh/4": float(pred_p),
                     "CFIM_E(unitary family)": None if Fnull is None else Fnull.tolist(),
                     "CFIM_E(rank-increasing family)": F2.tolist(),
                     "p'/t^2 (rank-increasing)": p2 / t**2})
    demo[name] = {"pred_limit (Nh)(Nh)^T/(h^T N h)": None if pred_F is None else pred_F.tolist(),
                  "N": N.tolist(), "rows": rows}
res["null_demo"]["directions"] = demo

# ---------- part 3: directional scalar convention on S- ----------
Sm = list(range(4, 16))
FQm = s11.qfi_subset(As, Sm)
Lm = s11.sld_ops(As, Sm)
dirrows = []
for _ in range(5):
    u = rng.normal(size=12)
    Lu = sum(ui * L for ui, L in zip(u, Lm))
    ev, U = np.linalg.eigh(Lu)
    dRu = 0.5 * (RHO @ Lu + Lu @ RHO)
    FCm = np.zeros((12, 12))
    num = 0.0
    for k in range(22):
        vk = U[:, k]; Ek = np.outer(vk, vk.conj())
        p = float(np.real(np.trace(RHO @ Ek)))
        if p <= 1e-14:
            continue
        dp_all = np.array([np.real(np.trace(0.5 * (RHO @ L + L @ RHO) @ Ek)) for L in Lm])
        FCm += np.outer(dp_all, dp_all) / p
    quQ = float(u @ FQm @ u); quC = float(u @ FCm @ u)
    dirrows.append({"u^T F_Q u": quQ, "u^T F_C u": quC, "rel_dir_deficit": (quQ - quC) / quQ,
                    "min_eig(F_Q-F_C)": float(np.linalg.eigvalsh(FQm - FCm)[0]),
                    "max_eig(F_Q-F_C)": float(np.linalg.eigvalsh(FQm - FCm)[-1]),
                    "rel_matrix_deficit_fro": float(np.linalg.norm(FQm - FCm) / np.linalg.norm(FQm))})
res["directional_scalar_Sminus"] = dirrows
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1)[:6000])
