"""Complex Levenberg-Marquardt solver for the braid-form constant YBE with an explicit inverse variable.

Unknowns: R (N^2 x N^2, complex) and S (= R^{-1}).  Equations: F(R)=R1R2R1-R2R1R2=0, R S = I, w.R = 1 (fixes scaling,
excludes R=0).  Holomorphic system -> complex Gauss-Newton/LM with the analytic Jacobian from ybe.jac_F.
"""

import sys
import time
import numpy as np
from ybe import jac_F_fast, braid_residual, rel_res


def residual(R, S, N, w):
    K = N * N
    F = braid_residual(R, N).reshape(-1)
    G = (R @ S - np.eye(K)).reshape(-1)
    c = np.array([np.sum(w * R) - 1.0])
    return np.concatenate([F, G, c])


def jac(R, S, N, w):
    K2 = N * N
    K4 = K2 * K2
    JF = jac_F(R, N)  # (N^6, K4) wrt R
    I = np.eye(K2)
    JG_R = np.kron(I, S.T)
    JG_S = np.kron(R, I)
    nF = JF.shape[0]
    J = np.zeros((nF + K4 + 1, 2 * K4), dtype=complex)
    J[:nF, :K4] = JF
    J[nF : nF + K4, :K4] = JG_R
    J[nF : nF + K4, K4:] = JG_S
    J[-1, :K4] = w.reshape(-1)
    return J


def normal_eq(R, S, r, N, w):
    """Return (H, g) with H = J^H J, g = J^H r for the stacked system (no explicit J)."""
    K2 = N * N
    K4 = K2 * K2
    nF = N ** 6
    JF = jac_F_fast(R, N)
    GR = np.kron(np.eye(K2), S.T)
    GS = np.kron(R, np.eye(K2))
    a = w.reshape(1, -1)
    rF, rG, rc = r[:nF], r[nF:nF + K4], r[-1]
    H = np.zeros((2 * K4, 2 * K4), dtype=complex)
    H[:K4, :K4] = JF.conj().T @ JF + GR.conj().T @ GR + a.conj().T @ a
    H[:K4, K4:] = GR.conj().T @ GS
    H[K4:, :K4] = H[:K4, K4:].conj().T
    H[K4:, K4:] = GS.conj().T @ GS
    g = np.concatenate([JF.conj().T @ rF + GR.conj().T @ rG + a.conj().ravel() * rc, GS.conj().T @ rG])
    return H, g


def lm_solve(R0, N, w, maxit=300, tol=1e-13, mu0=1e-2, verbose=False):
    K2 = N * N
    K4 = K2 * K2
    R = R0.copy()
    try:
        S = np.linalg.inv(R)
    except np.linalg.LinAlgError:
        return None, np.inf, 0
    r = residual(R, S, N, w)
    f = np.linalg.norm(r)
    mu = mu0
    it = 0
    for it in range(1, maxit + 1):
        H, g = normal_eq(R, S, r, N, w)
        improved = False
        for _ in range(12):
            try:
                d = np.linalg.solve(H + mu * np.eye(2 * K4), -g)
            except np.linalg.LinAlgError:
                mu *= 10
                continue
            Rn = R + d[:K4].reshape(K2, K2)
            Sn = S + d[K4:].reshape(K2, K2)
            rn = residual(Rn, Sn, N, w)
            fn = np.linalg.norm(rn)
            if fn < f:
                R, S, r, f = Rn, Sn, rn, fn
                mu = max(mu / 5, 1e-14)
                improved = True
                break
            mu *= 4
        if verbose:
            print(it, f, mu, flush=True)
        if f < tol:
            break
        if not improved or mu > 1e8:
            break
    return R, f, it


def random_start(N, rng, mode):
    K2 = N * N
    w = rng.normal(size=(K2, K2)) + 1j * rng.normal(size=(K2, K2))
    if mode == "gauss":
        R0 = rng.normal(size=(K2, K2)) + 1j * rng.normal(size=(K2, K2))
    elif mode == "real":
        R0 = rng.normal(size=(K2, K2)) + 0j
        w = w.real + 0j
    elif mode == "near_id":
        R0 = np.eye(K2) + rng.uniform(0.1, 1.0) * (
            rng.normal(size=(K2, K2)) + 1j * rng.normal(size=(K2, K2))
        )
    elif mode == 'upper':
        R0 = np.triu(rng.normal(size=(K2, K2)) + 1j * rng.normal(size=(K2, K2))) + 2 * np.eye(K2) * rng.normal()
    elif mode == 'near_id_small':
        R0 = np.eye(K2) + 0.05 * (rng.normal(size=(K2, K2)) + 1j * rng.normal(size=(K2, K2)))
    elif mode == 'near_flip_small':
        from ybe import flip
        R0 = flip(N) + 0.05 * (rng.normal(size=(K2, K2)) + 1j * rng.normal(size=(K2, K2)))
    else:  # near_flip
        from ybe import flip

        R0 = flip(N) + rng.uniform(0.1, 1.0) * (
            rng.normal(size=(K2, K2)) + 1j * rng.normal(size=(K2, K2))
        )
    s = np.sum(w * R0)
    if abs(s) < 1e-3:
        R0 = R0 + 0.1
        s = np.sum(w * R0)
    return R0 / s, w


def one_start(args):
    N, seed, mode, maxit = args
    rng = np.random.default_rng(seed)
    R0, w = random_start(N, rng, mode)
    R, f, it = lm_solve(R0, N, w, maxit=maxit)
    if R is None:
        return dict(seed=seed, mode=mode, ok=False, f=np.inf, it=0, R=None)
    return dict(
        seed=seed,
        mode=mode,
        ok=bool(f < 1e-10),
        f=float(f),
        it=it,
        R=R,
        rres=float(rel_res(R, N)),
        sminR=float(np.linalg.svd(R, compute_uv=False)[-1] / np.linalg.svd(R, compute_uv=False)[0]),
    )


if __name__ == "__main__":
    N = int(sys.argv[1])
    ns = int(sys.argv[2])
    t = time.time()
    out = [one_start((N, s, "gauss", 200)) for s in range(ns)]
    print("N=%d starts=%d ok=%d time=%.1fs" % (N, ns, sum(o["ok"] for o in out), time.time() - t))
    for o in out[:10]:
        print(o["seed"], o["ok"], "%.2e" % o["f"], o["it"], o.get("rres"), o.get("sminR"))
