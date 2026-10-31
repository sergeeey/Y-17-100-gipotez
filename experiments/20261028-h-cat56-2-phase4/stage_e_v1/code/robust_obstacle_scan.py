# WHY: minimal experiment for the robust (epsilon) theorem R of S_MINUS_BOREL_AND_NURDIN_v1.md (section B).
# For a direction c in C^2 (up to real scale) let V_c := span_R{ e_a (x) c : a in S } in C^{12x2} ~ R^48,
# let T: y -> (A_a^H y)_{a in S} (real-linear, R^40 -> R^48), and N_c := Pi_{V_c^perp} T.
# ker N_c = Y_S(c) (exact).  Robust constant kappa(c) := 1 / sigma_min(N_c restricted to (ker N_c)^perp).
# If sup over c of kappa(c) is finite (uniform in c on the sphere), the robust argument can use a uniform
# constant; if kappa blows up along some c (e.g. where dim Y_S(c) jumps from 4 to 6), the uniform version
# of the approximate-membership step fails and a different argument is needed.
# Output: logs/robust_obstacle_scan.json  (grid over the 3-sphere of c, real 4-vector parametrisation).
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from ys_space import load_A  # noqa: E402

S_MINUS = list(range(4, 16))
A = load_A(S_MINUS)
mats = [A[i] for i in S_MINUS]  # each 20 x 2 complex


def T_real(Ms):
    """Real 48x40 matrix of y -> (A_a^H y)_a in R^{48}; y = [Re y; Im y]."""
    rows = []
    for Ai in Ms:
        Ad = Ai.conj().T  # 2 x 20
        # Re(Ad y) = Re(Ad) Re y - Im(Ad) Im y ; Im(Ad y) = Im(Ad) Re y + Re(Ad) Im y
        Rr, Ii = Ad.real, Ad.imag
        rows.append(np.hstack([Rr, -Ii]))  # Re part, 2 rows
        rows.append(np.hstack([Ii, Rr]))  # Im part, 2 rows
    return np.vstack(rows)  # 12*4 = 48 rows


T = T_real(mats)  # 48 x 40


def V_basis(c):
    """Orthonormal basis (48 x 12) of V_c = span_R{ e_a (x) c }."""
    cols = []
    for a in range(len(S_MINUS)):
        v = np.zeros(48)
        # block a occupies real coordinates [4a, 4a+4): (Re c0, Re c1, Im c0, Im c1) ordering as in T_real
        # T_real rows per a: Re(c-row0), Re(c-row1), Im(c-row0), Im(c-row1) for the two complex components
        # The complex vector e_a(x)c lies in C^2 block a -> real rep [Re c0, Re c1, Im c0, Im c1]
        v[4 * a + 0] = c[0].real
        v[4 * a + 1] = c[1].real
        v[4 * a + 2] = c[0].imag
        v[4 * a + 3] = c[1].imag
        cols.append(v)
    Vm = np.array(cols).T
    Q, _ = np.linalg.qr(Vm)
    return Q


def kappa(c):
    Vb = V_basis(c)
    Pperp = np.eye(48) - Vb @ Vb.T
    N = Pperp @ T
    U, s, Vh = np.linalg.svd(N)
    tol = 1e-9 * max(1.0, s[0])
    r = int((s > tol).sum())
    dimY = 40 - r
    if r == 0:
        return float("inf"), dimY, 0.0
    return float(1.0 / s[r - 1]), dimY, float(s[r - 1])


# grid over S^3 (real 4-vector u = (Re c0, Im c0, Re c1, Im c1)), c = (u0 + i u1, u2 + i u3)
rng = np.random.default_rng(1)
samples = []
for th in np.linspace(0, np.pi, 19):
    for ph in np.linspace(0, 2 * np.pi, 37)[:-1]:
        for ps in np.linspace(0, 2 * np.pi, 13)[:-1]:
            # hopf-type grid: c0 = cos(th/2) e^{i ps}, c1 = sin(th/2) e^{i ph}
            c0 = np.cos(th / 2) * np.exp(1j * ps)
            c1 = np.sin(th / 2) * np.exp(1j * ph)
            samples.append(np.array([c0, c1]))
for _ in range(400):
    u = rng.standard_normal(4)
    u /= np.linalg.norm(u)
    samples.append(np.array([u[0] + 1j * u[1], u[2] + 1j * u[3]]))

rows = []
dims = {}
worst = (0.0, None)
for c in samples:
    if np.linalg.norm(c) < 1e-12:
        continue
    k, dimY, smin = kappa(c)
    dims[dimY] = dims.get(dimY, 0) + 1
    rows.append((k, dimY))
    if k > worst[0]:
        worst = (k, c.tolist())

finite = [k for (k, _) in rows if np.isfinite(k)]
out = {
    "samples": len(rows),
    "dim_Y_S(c)_histogram": {str(k): v for k, v in sorted(dims.items())},
    "kappa_max_over_samples": float(max(finite)) if finite else None,
    "kappa_median": float(np.median(finite)) if finite else None,
    "kappa_worst_direction_real_imag": [[float(z.real), float(z.imag)] for z in worst[1]]
    if worst[1]
    else None,
    "note": "kappa(c) = 1/sigma_min of Pi_{V_c^perp} T restricted to ker^perp. Large kappa = non-uniform robust constant.",
}
json.dump(out, open(os.path.join(STAGE, "logs", "robust_obstacle_scan.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
