"""Independent validation of the cell bound used in c3d (simple loop implementation, pinv instead of SVD products).

For random cells (random centre on the Bloch sphere, random half-widths) it computes the cell bound B(cell) by the
formula  B = max(lamK,0) + 2 ||M Z|| rho + ||M|| rho^2,  rho = kappa_K/(1-kappa)  (requires kappa < 1)
and then samples points u inside the rectangle, computes the TRUE g(u) = lambda_max(Z_u^T M Z_u) from the exact kernel of Phi(u)
and checks g(u) <= B.  Any violation would mean the inequality chain is wrong (not just the float margins).
Also reports how tight the bound is (max true g inside cell vs B).

Usage: python -I c3e_validate_bound.py <instance.jsonl> <R.npz> <n_cells> <out.json>
"""

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(
    0, os.path.normpath(os.path.join(HERE, "..", "..", "20261027-h-cat56-2-discovery", "code"))
)
import s8_admissible_span as sa  # noqa: E402

inst, rpath, n_cells, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
S = list(range(4, 16))
As = sa.load_A(inst)
R = np.load(rpath)["R"]
R = 0.5 * (R + R.conj().T)
M = np.block([[R.real, -R.imag], [R.imag, R.real]])
M = 0.5 * (M + M.T)
mnorm = np.linalg.norm(M, 2)
rng = np.random.default_rng(11)


def phi_of(th, ph):
    return sa.phi_rows(As, S, np.array([math.cos(th / 2), math.sin(th / 2) * np.exp(1j * ph)]))


# real-linear basis (independent construction: finite combination of phi_rows at 4 vectors)
BX = [np.array(v, complex) for v in ([1, 0], [1j, 0], [0, 1], [0, 1j])]
PHI = [sa.phi_rows(As, S, x) for x in BX]


def phi_u(u):
    return sum(u[j] * PHI[j] for j in range(4))


def kernel(Phi):
    _, s, Vt = np.linalg.svd(Phi)
    return Vt[36:].T


def u_of(th, ph):
    return np.array(
        [math.cos(th / 2), 0.0, math.sin(th / 2) * math.cos(ph), math.sin(th / 2) * math.sin(ph)]
    )


rows = []
viol = 0
checked = 0
for _ in range(n_cells):
    th = math.acos(rng.uniform(-1, 1))
    ph = rng.uniform(0, 2 * math.pi)
    hth = 10 ** rng.uniform(-4.5, -2.2)
    hph = 10 ** rng.uniform(-4.5, -2.2)
    du = 0.5 * hth + math.sin(min(th + hth, math.pi) / 2) * hph
    u0 = u_of(th, ph)
    P0 = phi_u(u0)
    U, s, Vt = np.linalg.svd(P0)
    Z = Vt[36:].T
    Pinv = np.linalg.pinv(P0)
    kappa = du * math.sqrt(sum(np.linalg.norm(Pinv @ PHI[j], 2) ** 2 for j in range(4)))
    kapK = du * math.sqrt(sum(np.linalg.norm(Pinv @ PHI[j] @ Z, 2) ** 2 for j in range(4)))
    if kappa >= 1:
        continue
    rho = kapK / (1 - kappa)
    lamK = np.linalg.eigvalsh(Z.T @ M @ Z)[-1]
    mz = np.linalg.norm(M @ Z, 2)
    B = max(lamK, 0.0) + 2 * mz * rho + mnorm * rho**2
    gmax = -np.inf
    for _ in range(30):
        t = th + rng.uniform(-hth, hth)
        p = ph + rng.uniform(-hph, hph)
        t = min(max(t, 0.0), math.pi)
        Zu = kernel(phi_u(u_of(t, p)))
        g = np.linalg.eigvalsh(Zu.T @ M @ Zu)[-1]
        gmax = max(gmax, g)
    checked += 1
    if gmax > B + 1e-12:
        viol += 1
    rows.append(
        {
            "theta": th,
            "phi": ph,
            "hth": hth,
            "hph": hph,
            "kappa": kappa,
            "rho": rho,
            "B": B,
            "gmax_true": float(gmax),
            "lamK": float(lamK),
        }
    )
res = {
    "cells_checked": checked,
    "violations": viol,
    "max_B_minus_gmax_ratio_tight": None,
    "sample": rows[:10],
}
if rows:
    res["min_slack"] = min(r["B"] - r["gmax_true"] for r in rows)
    res["median_slack"] = float(np.median([r["B"] - r["gmax_true"] for r in rows]))
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "sample"}, indent=1))
