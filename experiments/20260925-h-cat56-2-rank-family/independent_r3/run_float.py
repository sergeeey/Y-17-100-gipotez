# ruff: noqa  (style lint waived: independent implementer code kept as written; only this comment line was added)
"""Float (complex128) version of the same pipeline, independent of the exact code paths."""

import sys

import numpy as np


def cond_matrix(Bs, k, r):
    n = 2 * k * r
    cols = []
    for t in range(n):
        comp, idx = divmod(t, k * r)
        E = np.zeros((k, r), dtype=complex)
        E[idx // r, idx % r] = 1.0 if comp == 0 else 1.0j
        conds = []
        for Bi in Bs:
            X = Bi.conj().T @ E
            for a in range(r):
                for b in range(a + 1, r):
                    conds.append(X[a, b].real - X[b, a].real)
            for a in range(r):
                for b in range(a, r):
                    conds.append(X[a, b].imag + X[b, a].imag)
        cols.append(conds)
    return np.array(cols).T


def build_tower(d, r, s, rng, tol=1e-9):
    k = d - r
    B1 = rng.standard_normal((k, r)) + 1j * rng.standard_normal((k, r))
    B1 /= np.linalg.norm(B1)
    Bs = [B1]
    info = []
    for j in range(2, s + 1):
        C = cond_matrix(Bs, k, r)
        U, S, Vt = np.linalg.svd(C, full_matrices=True)
        rank = int((S > tol * S[0]).sum())
        below = S[rank - 1]
        above = S[rank] if rank < len(S) else 0.0
        null = Vt[rank:]
        info.append((j, null.shape[0], below, above))
        u = rng.standard_normal(null.shape[0]) @ null
        B = (u[: k * r] + 1j * u[k * r :]).reshape(k, r)
        B /= np.linalg.norm(B)
        Bs.append(B)
    return Bs, info


def coords(H):
    d = H.shape[0]
    iu = np.triu_indices(d, 1)
    return np.concatenate([H.real.diagonal(), H.real[iu], H.imag[iu]])


def sigmas(r, d):
    out = []
    for a in range(r):
        S = np.zeros((d, d), dtype=complex)
        S[a, a] = 1
        out.append(S)
    for a in range(r):
        for b in range(a + 1, r):
            S = np.zeros((d, d), dtype=complex)
            S[a, b] = S[b, a] = 1
            out.append(S)
            S = np.zeros((d, d), dtype=complex)
            S[a, b] = -1j
            S[b, a] = 1j
            out.append(S)
    return out


def run(d, r, s, seed):
    k = d - r
    rng = np.random.default_rng(seed)
    Bs, info = build_tower(d, r, s, rng)
    Q = np.arange(1, r + 1, dtype=float)
    rho0 = np.diag(np.concatenate([Q, np.zeros(k)])).astype(complex)
    q = np.concatenate([Q, np.zeros(k)])
    S = q[:, None] + q[None, :]
    mask = np.abs(S) > 0
    Ls = []
    cs = []
    sld_res = 0.0
    struct_res = 0.0
    for B in Bs:
        G = np.zeros((d, d), dtype=complex)
        G[:r, r:] = B.conj().T
        G[r:, :r] = B
        drho = -1j * (G @ rho0 - rho0 @ G)
        L = np.zeros((d, d), dtype=complex)
        L[mask] = 2 * drho[mask] / S[mask]
        sld_res = max(sld_res, np.abs((rho0 @ L + L @ rho0) / 2 - drho).max())
        A = L[r:, :r]
        struct_res = max(
            struct_res,
            np.abs(L[:r, :r]).max(),
            np.abs(L[r:, r:]).max(),
            np.abs(L[:r, r:] - A.conj().T).max(),
            np.abs(L - L.conj().T).max(),
        )
        cs.append((A * B.conj()).sum() / (np.abs(B) ** 2).sum())
        Ls.append(L)
    print("SLD residual max = %.2e ; structure/Hermitian residual = %.2e" % (sld_res, struct_res))
    print(
        "A_i = c_i B_i, c_i (least squares):",
        np.round(cs[:3], 12),
        "... max|c+2i| = %.2e" % max(abs(c + 2j) for c in cs),
    )
    for j, nn, below, above in info:
        print(
            "  stage j=%d nullity=%d  smallest retained sv=%.3e  largest dropped sv=%.3e"
            % (j, nn, below, above)
        )
    pcc = 0.0
    for i in range(s):
        for j in range(i + 1, s):
            C = Ls[i] @ Ls[j] - Ls[j] @ Ls[i]
            pcc = max(pcc, np.abs(C[:r, :r]).max())
    print(
        "PCC max |Pi [Li,Lj] Pi| = %.2e   (scale of |L|max = %.2e)"
        % (pcc, max(np.abs(L).max() for L in Ls))
    )
    F = np.zeros((s, s))
    for i in range(s):
        for j in range(s):
            F[i, j] = 0.5 * np.trace(rho0 @ (Ls[i] @ Ls[j] + Ls[j] @ Ls[i])).real
    ev = np.linalg.eigvalsh(F)
    print(
        "QFIM eig min/max = %.3e / %.3e  det = %.3e  cond=%.2e"
        % (ev[0], ev[-1], np.linalg.det(F), ev[-1] / ev[0])
    )
    sig = sigmas(r, d)
    rows = []
    cx = []
    for i in range(s):
        for sg in sig:
            M = 1j * (sg @ Ls[i] - Ls[i] @ sg)
            rows.append(coords(M))
            cx.append(M.reshape(-1))
    for i in range(s):
        for j in range(i + 1, s):
            for sg in sig:
                W = 1j * (Ls[i] @ sg @ Ls[j] - Ls[j] @ sg @ Ls[i])
                rows.append(coords(W))
                cx.append(W.reshape(-1))
    Vm = np.array(rows)
    herm = max(
        np.abs(np.array(cx)[t].reshape(d, d) - np.array(cx)[t].reshape(d, d).conj().T).max()
        for t in range(len(cx))
    )
    print("generators: %d ; max Hermiticity defect %.2e" % (Vm.shape[0], herm))
    sv = np.linalg.svd(Vm, compute_uv=False)
    svc = np.linalg.svd(np.array(cx), compute_uv=False)
    svc_ = np.maximum(sv, 1e-17 * sv[0])
    ratios = svc_[:-1] / svc_[1:]
    g = int(np.argmax(ratios))
    rank = g + 1
    print(
        "largest ratio sv[i]/sv[i+1] at i=%d : sv[%d]=%.6e  sv[%d]=%.6e  ratio=%.3e"
        % (g, g, sv[g], g + 1, sv[g + 1], ratios[g])
    )
    print("singular values around cutoff (index: value):")
    for t in range(max(0, rank - 4), min(len(sv), rank + 5)):
        print("   %d: %.6e" % (t, sv[t]))
    print("sv max = %.3e ; sv[0]/sv[rank-1] = %.3e" % (sv[0], sv[0] / sv[rank - 1]))
    tol = np.sqrt(sv[rank - 1] * sv[rank])
    print(
        "tolerance used (geometric mean of the two sides of the gap) = %.3e ; relative to sv[0]: %.3e"
        % (tol, tol / sv[0])
    )
    r_real = int((sv > tol).sum())
    r_cplx = int((svc > tol).sum())
    print(
        "numerical dim V (real coords, sv>tol) = %d ; complex flattened rank = %d ; d^2 = %d ; dim V-perp = %d (complex-rank version %d)"
        % (r_real, r_cplx, d * d, d * d - r_real, d * d - r_cplx)
    )
    print("second-largest ratio (for gap-uniqueness):", np.sort(ratios)[-2])
    print("next-largest of dropped sv:", sv[rank], " smallest kept:", sv[rank - 1])
    return


if __name__ == "__main__":
    for d, r, s, seed in ((23, 3, 12, 1), (23, 3, 12, 2), (8, 2, 5, 1)):
        print("=== FLOAT d=%d r=%d s=%d seed=%d" % (d, r, s, seed))
        run(d, r, s, seed)
        sys.stdout.flush()
