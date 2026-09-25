# ruff: noqa  (style lint waived: independent implementer code kept as written; only this comment line was added)
"""Exact complex linear algebra mod p, complex numbers as (re, im) residue pairs.

A complex matrix is an int64 array Z of shape (2, n, m): Z[0]=re, Z[1]=im.
The ring is F_p[x]/(x^2+1) (no sqrt(-1) in F_p is assumed; conj = (re,-im)).
"""

import numpy as np


def mm(A, B, p, chunk=7):
    """Real integer matmul mod p with chunked reduction (p < 2^30 => no int64 overflow)."""
    n = A.shape[1]
    R = np.zeros((A.shape[0], B.shape[1]), dtype=np.int64)
    for c in range(0, n, chunk):
        R = (R + A[:, c : c + chunk] @ B[c : c + chunk, :]) % p
    return R


def cmul(A, B, p):
    re = (mm(A[0], B[0], p) - mm(A[1], B[1], p)) % p
    im = (mm(A[0], B[1], p) + mm(A[1], B[0], p)) % p
    return np.stack([re, im])


def cadd(A, B, p):
    return (A + B) % p


def csub(A, B, p):
    return (A - B) % p


def cdag(A, p):
    return np.stack([A[0].T.copy(), (-A[1].T) % p])


def ci(A, p):
    """multiply by i : (a+bi)i = -b + ai"""
    return np.stack([(-A[1]) % p, A[0].copy()])


def cscal(A, a, b, p):
    """multiply every entry by the complex scalar a+bi"""
    a = int(a) % p
    b = int(b) % p
    re = (a * A[0] % p - b * A[1] % p) % p
    im = (a * A[1] % p + b * A[0] % p) % p
    return np.stack([re, im])


def ctrace(A, p):
    return int(np.trace(A[0]) % p), int(np.trace(A[1]) % p)


def is_zero(A):
    return not A.any()


def cinv_scalar(a, b, p):
    n = (a * a + b * b) % p
    if n == 0:
        raise ZeroDivisionError("norm zero mod p")
    ni = pow(n, p - 2, p)
    return (a * ni) % p, ((-b) * ni) % p


# ---------- linear algebra over F_p (real coordinate vectors) ----------


def rref(M, p):
    M = M.copy() % p
    rows, cols = M.shape
    piv = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        k = nz[0] + r
        if k != r:
            M[[r, k]] = M[[k, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        col = M[:, c].copy()
        col[r] = 0
        M = (M - (col[:, None] * M[r][None, :]) % p) % p
        piv.append(c)
        r += 1
    return M, piv


def rank_modp(M, p):
    """rank only, eliminating rows below the pivot"""
    M = M.copy() % p
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        k = nz[0] + r
        if k != r:
            M[[r, k]] = M[[k, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        col = M[r + 1 :, c].copy()
        M[r + 1 :] = (M[r + 1 :] - (col[:, None] * M[r][None, :]) % p) % p
        r += 1
    return r


def nullspace_modp(M, p):
    """basis (rows) of {u : M u = 0 mod p}"""
    R, piv = rref(M, p)
    n = M.shape[1]
    free = [c for c in range(n) if c not in set(piv)]
    basis = []
    for f in free:
        v = np.zeros(n, dtype=np.int64)
        v[f] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-R[i, f]) % p
        basis.append(v)
    if not basis:
        return np.zeros((0, n), dtype=np.int64), len(piv)
    return np.array(basis, dtype=np.int64), len(piv)


def det_modp(F, p):
    F = F.copy() % p
    n = F.shape[0]
    det = 1
    for c in range(n):
        nz = np.nonzero(F[c:, c])[0]
        if len(nz) == 0:
            return 0
        k = nz[0] + c
        if k != c:
            F[[c, k]] = F[[k, c]]
            det = (-det) % p
        det = (det * int(F[c, c])) % p
        inv = pow(int(F[c, c]), p - 2, p)
        col = F[c + 1 :, c].copy()
        F[c + 1 :] = (F[c + 1 :] - (col[:, None] * ((F[c] * inv) % p)[None, :]) % p) % p
    return det % p


def crank_field(Zre, Zim, p):
    """Rank over K = F_p[i] of a complex matrix; valid as a FIELD rank only when p % 4 == 3."""
    assert p % 4 == 3
    R0 = Zre.copy() % p
    R1 = Zim.copy() % p
    rows, cols = R0.shape
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        nz = np.nonzero((R0[r:, c] != 0) | (R1[r:, c] != 0))[0]
        if len(nz) == 0:
            continue
        k = nz[0] + r
        if k != r:
            R0[[r, k]] = R0[[k, r]]
            R1[[r, k]] = R1[[k, r]]
        ia, ib = cinv_scalar(int(R0[r, c]), int(R1[r, c]), p)
        n0 = (ia * R0[r] % p - ib * R1[r] % p) % p
        n1 = (ia * R1[r] % p + ib * R0[r] % p) % p
        R0[r], R1[r] = n0, n1
        c0 = R0[r + 1 :, c].copy()
        c1 = R1[r + 1 :, c].copy()
        t0 = (c0[:, None] * R0[r][None, :] % p - c1[:, None] * R1[r][None, :] % p) % p
        t1 = (c0[:, None] * R1[r][None, :] % p + c1[:, None] * R0[r][None, :] % p) % p
        R0[r + 1 :] = (R0[r + 1 :] - t0) % p
        R1[r + 1 :] = (R1[r + 1 :] - t1) % p
        r += 1
    return r


# ---------- the tower ----------


def cond_matrix(Bs, k, r, p):
    """Real-linear (over F_p in (re,im) coordinates) conditions on new B (k x r complex):
    B_i^dagger B Hermitian for every earlier B_i.  Columns indexed by the 2kr real unknowns
    u = (Re B entries row-major, Im B entries row-major)."""
    n = 2 * k * r
    cols = []
    Bdags = [cdag(Bi, p) for Bi in Bs]
    for t in range(n):
        comp, idx = divmod(t, k * r)
        E = np.zeros((2, k, r), dtype=np.int64)
        E[comp, idx // r, idx % r] = 1
        conds = []
        for Bd in Bdags:
            X = cmul(Bd, E, p)
            re, im = X[0], X[1]
            for a in range(r):
                for b in range(a + 1, r):
                    conds.append((re[a, b] - re[b, a]) % p)
            for a in range(r):
                for b in range(a, r):
                    conds.append((im[a, b] + im[b, a]) % p)
        cols.append(conds)
    return np.array(cols, dtype=np.int64).T


def build_tower(d, r, s, p, seed):
    k = d - r
    rng = np.random.default_rng(seed)
    B1 = rng.integers(0, p, size=(2, k, r), dtype=np.int64)
    Bs = [B1]
    stage_dims = []
    for j in range(2, s + 1):
        C = cond_matrix(Bs, k, r, p)
        basis, rk = nullspace_modp(C, p)
        stage_dims.append(basis.shape[0])
        if basis.shape[0] == 0:
            Bs.append(np.zeros((2, k, r), dtype=np.int64))
            continue
        coeffs = rng.integers(0, p, size=(1, basis.shape[0]), dtype=np.int64)
        u = mm(coeffs, basis, p)[0]
        Bj = np.stack([u[: k * r].reshape(k, r), u[k * r :].reshape(k, r)])
        Bs.append(Bj)
    return Bs, stage_dims


# ---------- the pipeline ----------


def herm_coords(H, p):
    d = H.shape[1]
    iu = np.triu_indices(d, 1)
    return np.concatenate([H[0].diagonal(), H[0][iu], H[1][iu]])


def sigma_basis(r, d, p):
    sig = []
    for a in range(r):
        S = np.zeros((2, d, d), dtype=np.int64)
        S[0, a, a] = 1
        sig.append(S)
    for a in range(r):
        for b in range(a + 1, r):
            S = np.zeros((2, d, d), dtype=np.int64)
            S[0, a, b] = 1
            S[0, b, a] = 1
            sig.append(S)
            S2 = np.zeros((2, d, d), dtype=np.int64)
            # -i E_ab + i E_ba : entry (a,b) = 0 - 1 i, entry (b,a) = 0 + 1 i
            S2[1, a, b] = p - 1
            S2[1, b, a] = 1
            sig.append(S2)
    return sig


def compute_L(B, d, r, p, Q):
    """Full-matrix SLD solve. Returns G, drho, L, info."""
    k = d - r
    G = np.zeros((2, d, d), dtype=np.int64)
    G[:, :r, r:] = cdag(B, p)
    G[:, r:, :r] = B
    rho0 = np.zeros((2, d, d), dtype=np.int64)
    for a in range(r):
        rho0[0, a, a] = Q[a] % p
    comm = csub(cmul(G, rho0, p), cmul(rho0, G, p), p)  # [G, rho0]
    # -i * comm : -i(a+bi) = b - a i
    drho = np.stack([comm[1].copy(), (-comm[0]) % p])
    q = np.array(list(Q) + [0] * k, dtype=np.int64)
    S = (q[:, None] + q[None, :]) % p
    mask = S != 0
    invS = np.zeros((d, d), dtype=np.int64)
    for m in range(d):
        for n in range(d):
            if mask[m, n]:
                invS[m, n] = pow(int(S[m, n]), p - 2, p)
    # (q_m + q_n)/2 L_mn = D_mn  ->  L_mn = 2 D_mn / (q_m + q_n) ; zero where q_m+q_n = 0
    kk_D_zero = is_zero(drho[:, ~mask])  # D must vanish where the equation is degenerate
    L = np.stack([(2 * drho[0] % p) * invS % p, (2 * drho[1] % p) * invS % p])
    return G, rho0, drho, L, kk_D_zero


def pipeline(d, r, s, p, Bs, Q=None, compute_V=True, field_check=False, log=print):
    k = d - r
    if Q is None:
        Q = list(range(1, r + 1))
    inv2 = pow(2, p - 2, p)
    out = {}
    Ls = []
    sld_ok = True
    herm_ok = True
    struct_ok = True
    kkD_ok = True
    A_scalar = None
    A_ok = True
    for idx, B in enumerate(Bs):
        G, rho0, drho, L, kkD = compute_L(B, d, r, p, Q)
        kkD_ok &= kkD
        lhs = cscal(cadd(cmul(rho0, L, p), cmul(L, rho0, p), p), inv2, 0, p)
        sld_ok &= bool((lhs == drho).all())
        herm_ok &= bool((L == cdag(L, p)).all())
        struct_ok &= is_zero(L[:, :r, :r]) and is_zero(L[:, r:, r:])
        A = L[:, r:, :r]
        struct_ok &= bool((L[:, :r, r:] == cdag(A, p)).all())
        # find scalar c with A = c B : use first entry with invertible norm
        c = None
        for aa in range(k):
            for bb in range(r):
                br, bi = int(B[0, aa, bb]), int(B[1, aa, bb])
                if (br * br + bi * bi) % p != 0:
                    ir, ii = cinv_scalar(br, bi, p)
                    ar, ai = int(A[0, aa, bb]), int(A[1, aa, bb])
                    c = ((ar * ir - ai * ii) % p, (ar * ii + ai * ir) % p)
                    break
            if c is not None:
                break
        A_ok &= bool((cscal(B, c[0], c[1], p) == A).all())
        if A_scalar is None:
            A_scalar = c
        else:
            A_ok &= A_scalar == c
        Ls.append(L)
    out["sld_ok"] = sld_ok
    out["L_hermitian"] = herm_ok
    out["L_structure_[[0,Adag],[A,0]]"] = struct_ok
    out["degenerate_block_of_drho_zero"] = kkD_ok
    out["A_equals_c_B_all_i"] = A_ok
    out["c_pair"] = A_scalar
    out["c_is_minus_2i"] = A_scalar == (0, (-2) % p)

    # PCC on full commutators
    fail_pairs = []
    fail_alt = []
    for i in range(s):
        for j in range(i + 1, s):
            C = csub(cmul(Ls[i], Ls[j], p), cmul(Ls[j], Ls[i], p), p)
            if not is_zero(C[:, :r, :r]):
                fail_pairs.append((i + 1, j + 1))
            X = cmul(cdag(Bs[i], p), Bs[j], p)
            if not (X == cdag(X, p)).all():
                fail_alt.append((i + 1, j + 1))
    out["pcc_ok"] = len(fail_pairs) == 0
    out["pcc_fail_pairs"] = fail_pairs
    out["BdagB_hermitian_fail_pairs"] = fail_alt

    # QFIM
    rho0 = np.zeros((2, d, d), dtype=np.int64)
    for a in range(r):
        rho0[0, a, a] = Q[a] % p
    F = np.zeros((s, s), dtype=np.int64)
    im_ok = True
    for i in range(s):
        for j in range(i, s):
            anti = cadd(cmul(Ls[i], Ls[j], p), cmul(Ls[j], Ls[i], p), p)
            tr_re, tr_im = ctrace(cmul(rho0, anti, p), p)
            im_ok &= tr_im == 0
            F[i, j] = F[j, i] = (tr_re * inv2) % p
    out["qfim_trace_imag_zero"] = im_ok
    out["qfim_symmetric"] = bool((F == F.T).all())
    out["qfim_rank"] = rank_modp(F, p)
    out["det_qfim"] = det_modp(F, p)
    out["det_qfim_nonzero"] = out["det_qfim"] != 0

    if compute_V:
        sig = sigma_basis(r, d, p)
        P = [[cmul(Ls[i], S, p) for S in sig] for i in range(s)]
        vecs = []
        herm_all = True
        cx_rows = []
        for i in range(s):
            for si, S in enumerate(sig):
                M = ci(csub(cmul(S, Ls[i], p), P[i][si], p), p)  # i(sigma L - L sigma)
                herm_all &= bool((M == cdag(M, p)).all())
                vecs.append(herm_coords(M, p))
                cx_rows.append(M)
        for i in range(s):
            for j in range(i + 1, s):
                for si, S in enumerate(sig):
                    W = ci(csub(cmul(P[i][si], Ls[j], p), cmul(P[j][si], Ls[i], p), p), p)
                    herm_all &= bool((W == cdag(W, p)).all())
                    vecs.append(herm_coords(W, p))
                    cx_rows.append(W)
        V = np.array(vecs, dtype=np.int64)
        rk = rank_modp(V, p)
        out["n_V_generators"] = V.shape[0]
        out["V_all_hermitian"] = herm_all
        out["dim_V"] = rk
        out["dim_Vperp"] = d * d - rk
        if field_check and p % 4 == 3:
            Zre = np.array([M[0].reshape(-1) for M in cx_rows], dtype=np.int64)
            Zim = np.array([M[1].reshape(-1) for M in cx_rows], dtype=np.int64)
            out["complex_rank_over_Fp2_flattened"] = crank_field(Zre, Zim, p)
    return out
