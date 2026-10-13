"""Serial, throttled-friendly LM solver for braid-form YBE (dim 3) restricted to a support mask, with early abort.
Variables: R (on mask) and S=R^{-1} (same mask; masks used are unions of total-charge blocks so S has the same support).
Equations: F(R)=R1R2R1-R2R1R2=0, RS=I, w.R=1.  NO multiprocessing."""
import time
import numpy as np
from ybe import jac_F_fast, braid_residual, rel_res, flip

N = 3
K2 = 9
K4 = 81


def grading_mask(q, mod=None):
    """mask[(a,b),(c,d)] = 1 iff q[a]+q[b] == q[c]+q[d] (mod `mod` if given). Basis index i*3+j (check-R convention: R maps
    |cd> to |ab> -> row=(a,b), col=(c,d))."""
    M = np.zeros((9, 9), dtype=bool)
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    s1, s2 = q[a] + q[b], q[c] + q[d]
                    ok = (s1 - s2) % mod == 0 if mod else s1 == s2
                    M[a * 3 + b, c * 3 + d] = ok
    return M


def residual(R, S, w):
    F = braid_residual(R, N).reshape(-1)
    G = (R @ S - np.eye(K2)).reshape(-1)
    c = np.array([np.sum(w * R) - 1.0])
    return np.concatenate([F, G, c])


def lm_mask(R0, w, idx, maxit=150, tol=1e-13, mu0=1e-2, abort=True):
    """idx = flat indices (into 81) of free entries. Returns (R, f, it, reason)."""
    m = len(idx)
    R = R0.copy()
    try:
        S = np.linalg.inv(R)
    except np.linalg.LinAlgError:
        return None, np.inf, 0, "singular0"
    r = residual(R, S, w)
    f = np.linalg.norm(r)
    mu = mu0
    nF = N ** 6
    hist = []
    for it in range(1, maxit + 1):
        JF = jac_F_fast(R, N)[:, idx]
        GR = np.kron(np.eye(K2), S.T)[:, idx]
        GS = np.kron(R, np.eye(K2))[:, idx]
        a = w.reshape(1, -1)[:, idx]
        rF, rG, rc = r[:nF], r[nF:nF + K4], r[-1]
        H = np.zeros((2 * m, 2 * m), dtype=complex)
        H[:m, :m] = JF.conj().T @ JF + GR.conj().T @ GR + a.conj().T @ a
        H[:m, m:] = GR.conj().T @ GS
        H[m:, :m] = H[:m, m:].conj().T
        H[m:, m:] = GS.conj().T @ GS
        g = np.concatenate([JF.conj().T @ rF + GR.conj().T @ rG + a.conj().ravel() * rc, GS.conj().T @ rG])
        improved = False
        for _ in range(12):
            try:
                d = np.linalg.solve(H + mu * np.eye(2 * m), -g)
            except np.linalg.LinAlgError:
                mu *= 10
                continue
            Rn = R.copy().reshape(-1)
            Sn = S.copy().reshape(-1)
            Rn[idx] += d[:m]
            Sn[idx] += d[m:]
            Rn = Rn.reshape(K2, K2)
            Sn = Sn.reshape(K2, K2)
            rn = residual(Rn, Sn, w)
            fn = np.linalg.norm(rn)
            if fn < f:
                R, S, r, f = Rn, Sn, rn, fn
                mu = max(mu / 5, 1e-14)
                improved = True
                break
            mu *= 4
        hist.append(f)
        if f < tol:
            return R, f, it, "ok"
        if not improved or mu > 1e8:
            return R, f, it, "stall"
        if abort:
            if np.abs(S).max() > 1e5:
                return R, f, it, "S-blowup"
            if it >= 40 and f > 5e-3:
                return R, f, it, "slow"
            if it >= 40 and it % 20 == 0 and f > 1e-7 and hist[-1] > 0.7 * hist[-21]:
                return R, f, it, "sublinear"
    return R, f, maxit, "maxit"


def random_masked_start(mask, rng, mode="gauss"):
    R0 = (rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9))) * mask
    if mode == "near_id":
        R0 = np.eye(9) * mask + rng.uniform(0.1, 1.0) * R0
    elif mode == "near_flip":
        R0 = flip(3) * mask + rng.uniform(0.1, 1.0) * R0
    w = (rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9))) * mask
    s = np.sum(w * R0)
    return R0 / s, w


def lm_det(R0, idx, maxit=150, tol=1e-13, mu0=1e-2, abort=True, rmax=1e3):
    """LM on unknown R only (free entries idx), equations F(R)=0 and det R = 1 (excludes singular R, fixes scale up to a
    9th root of unity).  Complex Gauss-Newton with analytic Jacobians."""
    m = len(idx)
    R = R0.copy()
    nF = N ** 6

    def resid(R):
        return np.concatenate([braid_residual(R, N).reshape(-1), [np.linalg.det(R) - 1.0]])

    r = resid(R)
    f = np.linalg.norm(r)
    mu = mu0
    hist = []
    for it in range(1, maxit + 1):
        JF = jac_F_fast(R, N)[:, idx]
        dt = np.linalg.det(R)
        try:
            Jd = (dt * np.linalg.inv(R).T).reshape(1, -1)[:, idx]
        except np.linalg.LinAlgError:
            return R, f, it, "singular"
        J = np.vstack([JF, Jd])
        H = J.conj().T @ J
        g = J.conj().T @ r
        improved = False
        for _ in range(12):
            try:
                d = np.linalg.solve(H + mu * np.eye(m), -g)
            except np.linalg.LinAlgError:
                mu *= 10
                continue
            Rn = R.copy().reshape(-1)
            Rn[idx] += d
            Rn = Rn.reshape(K2, K2)
            rn = resid(Rn)
            fn = np.linalg.norm(rn)
            if fn < f:
                R, r, f = Rn, rn, fn
                mu = max(mu / 5, 1e-14)
                improved = True
                break
            mu *= 4
        hist.append(f)
        if f < tol:
            return R, f, it, "ok"
        if not improved or mu > 1e8:
            return R, f, it, "stall"
        if abort:
            if np.abs(R).max() > rmax:
                return R, f, it, "R-blowup"
            if it >= 40 and f > 5e-3:
                return R, f, it, "slow"
            if it >= 60 and it % 20 == 0 and f > 1e-7 and hist[-1] > 0.7 * hist[-21]:
                return R, f, it, "sublinear"
    return R, f, maxit, "maxit"


def random_det_start(mask, rng, mode="gauss"):
    R0 = (rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9))) * mask
    if mode == "near_id":
        R0 = np.eye(9) * mask + rng.uniform(0.1, 1.0) * R0
    elif mode == "near_flip":
        R0 = flip(3) * mask + rng.uniform(0.1, 1.0) * R0
    d = np.linalg.det(R0)
    return R0 * d ** (-1.0 / 9)
