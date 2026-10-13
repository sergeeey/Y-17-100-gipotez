"""Constant Yang-Baxter equation toolkit (braid form R1 R2 R1 = R2 R1 R2, R = check-R = P R_YBE).

Basis convention: |ij> has index i*N + j (lexicographic), matching arXiv:2310.03816 eq. (Rcheck).
"""

import numpy as np

# ----------------------------------------------------------------------------------------
# basic placement / residuals
# ----------------------------------------------------------------------------------------


def flip(N):
    P = np.zeros((N * N, N * N))
    for i in range(N):
        for j in range(N):
            P[j * N + i, i * N + j] = 1.0
    return P


def braid_residual(R, N):
    """R1R2R1 - R2R1R2 with R1=R(x)1, R2=1(x)R (N^3 x N^3)."""
    I = np.eye(N)
    A = np.kron(R, I)
    B = np.kron(I, R)
    return A @ B @ A - B @ A @ B


def swap23(N):
    """Permutation of V(x)V(x)V swapping factors 2 and 3."""
    M = N**3
    P = np.zeros((M, M))
    for i in range(N):
        for j in range(N):
            for k in range(N):
                P[i * N * N + k * N + j, i * N * N + j * N + k] = 1.0
    return P


def ybe_residual_R(R, N):
    """Non-braided form R12 R13 R23 - R23 R13 R12 (R = P * check-R, as in the task statement)."""
    I = np.eye(N)
    R12 = np.kron(R, I)
    R23 = np.kron(I, R)
    P23 = swap23(N)
    R13 = P23 @ R12 @ P23
    return R12 @ R13 @ R23 - R23 @ R13 @ R12


def rel_res(R, N):
    """Scale-invariant residual: ||F(R)|| / ||R||^3."""
    return np.linalg.norm(braid_residual(R, N)) / max(np.linalg.norm(R), 1e-300) ** 3


# ----------------------------------------------------------------------------------------
# Jacobian of braid residual wrt R (holomorphic), used by solver and tangent-space dimension
# ----------------------------------------------------------------------------------------
_cache = {}


def _dstack(N):
    if N in _cache:
        return _cache[N]
    I = np.eye(N)
    K = N**4
    M = N**3
    DA = np.zeros((K, M, M))
    DB = np.zeros((K, M, M))
    for k in range(K):
        E = np.zeros((N * N, N * N))
        E[k // (N * N), k % (N * N)] = 1.0
        DA[k] = np.kron(E, I)
        DB[k] = np.kron(I, E)
    _cache[N] = (DA, DB)
    return DA, DB


def jac_F(R, N):
    """Jacobian dF/dR as (M*M, N^4) complex matrix; column k = d F / d R_flat[k]."""
    DA, DB = _dstack(N)
    I = np.eye(N)
    A = np.kron(R, I)
    B = np.kron(I, R)
    BA = B @ A
    AB = A @ B
    # d(ABA - BAB) = dA.B.A + A.dB.A + A.B.dA - dB.A.B - B.dA.B - B.A.dB
    dF = DA @ BA + (A @ DB) @ A + AB @ DA - DB @ AB - (B @ DA) @ B - BA @ DB
    # shapes: (K,M,M)
    K = dF.shape[0]
    return dF.reshape(K, -1).T


# ----------------------------------------------------------------------------------------
# Lie algebra of 'additive' symmetries L(R) = {h : [R, h(x)1 + 1(x)h] = 0}
# ----------------------------------------------------------------------------------------


def delta_h(h, N):
    I = np.eye(N)
    return np.kron(h, I) + np.kron(I, h)


def L_algebra(R, N, tol=1e-7):
    """Return (basis of L as list of NxN matrices, singular values). tol relative to top singular value."""
    cols = []
    for k in range(N * N):
        h = np.zeros((N, N))
        h[k // N, k % N] = 1.0
        D = delta_h(h, N)
        cols.append((R @ D - D @ R).reshape(-1))
    Mx = np.array(cols).T
    u, s, vh = np.linalg.svd(Mx)
    scale = max(s[0], np.linalg.norm(R) * np.sqrt(2 * N), 1e-300)  # absolute scale: R, D = delta_h are O(1)
    null = [vh[i].conj().reshape(N, N) for i in range(len(s)) if s[i] < tol * scale]
    return null, s / scale


def cc_class(R, N, tol=1e-7, gap_tol=1e-4, rng=None):
    """Classify R by L(R). Returns dict with dimL and label.
    label: 'U1-free'   : L = scalars (no nonscalar h)
           'distinct'  : L contains h with N distinct eigenvalues  => locally conjugate to a charge-conserving
                         (strict if no AP coincidence, ACC if AP) matrix [enzuigiri criterion, 2609.38290 Thm]
           'degenerate': L has nonscalar h but every element has repeated eigenvalue
    """
    rng = rng or np.random.default_rng(0)
    null, s = L_algebra(R, N, tol)
    d = len(null)
    if d <= 1:
        return dict(dimL=d, label="U1-free", min_gap=None)
    best = 0.0
    for _ in range(5):
        c = rng.normal(size=d) + 1j * rng.normal(size=d)
        h = sum(ci * b for ci, b in zip(c, null))
        ev = np.linalg.eigvals(h)
        scale = np.abs(ev).max()
        gaps = [abs(ev[i] - ev[j]) for i in range(N) for j in range(i + 1, N)]
        best = max(best, min(gaps) / max(scale, 1e-300))
    return dict(dimL=d, label="distinct" if best > gap_tol else "degenerate", min_gap=best)


# ----------------------------------------------------------------------------------------
# spectral / Jordan / tangent invariants
# ----------------------------------------------------------------------------------------


def cluster_eigs(ev, tol):
    ev = list(ev)
    groups = []
    for e in ev:
        for g in groups:
            if abs(g[0] - e) < tol * max(1.0, abs(g[0])):
                g.append(e)
                break
        else:
            groups.append([e])
    return groups


def spectral_signature(R, N, tol=1e-5):
    """Sorted list of (algebraic mult, geometric mult) pairs per distinct eigenvalue + eigenvalue ratios info."""
    ev = np.linalg.eigvals(R)
    groups = cluster_eigs(ev, tol)
    sig = []
    for g in groups:
        lam = np.mean(g)
        s = np.linalg.svd(R - lam * np.eye(N * N), compute_uv=False)
        geom = int(np.sum(s < 1e-5 * max(s[0], np.linalg.norm(R), 1e-300)))
        sig.append((len(g), geom, lam))
    sig.sort(key=lambda t: (-t[0], -t[1]))
    return sig


def tangent_dim(R, N, tol=1e-7):
    """dim of Zariski tangent space of {F=0} at R (includes scaling direction)."""
    J = jac_F(R, N)
    s = np.linalg.svd(J, compute_uv=False)
    rank = int(np.sum(s > tol * s[0]))
    return N**4 - rank, s


def invariants(R, N):
    # scale-normalise (YBE is homogeneous): |det R| = 1, so eigenvalue clustering tolerances are relative
    R = R / abs(np.linalg.det(R)) ** (1.0 / (N * N))
    sig = spectral_signature(R, N)
    cc = cc_class(R, N)
    td, s = tangent_dim(R, N)
    dimL = cc["dimL"]
    orbit = N * N - dimL
    moduli = td - 1 - orbit
    return dict(
        spec=[(a, g) for a, g, _ in sig],
        spec_full=sig,
        dimL=dimL,
        cc=cc["label"],
        tangent=td,
        orbit=orbit,
        moduli=moduli,
        detabs=abs(np.linalg.det(R)),
        rank=int(np.linalg.matrix_rank(R, tol=1e-8)),
    )


# ----------------------------------------------------------------------------------------
# block builder: arXiv:2310.03816 block form [a1][2x2 on |01>,|10>][3x3 on |02>,|11>,|20>][2x2 on |12>,|21>][a3]
# ----------------------------------------------------------------------------------------


def build_acc(a1, B12, B13, B23, a3):
    R = np.zeros((9, 9), dtype=complex)
    R[0, 0] = a1
    idx12 = [1, 3]
    idx13 = [2, 4, 6]
    idx23 = [5, 7]
    for blk, idx in ((B12, idx12), (B13, idx13), (B23, idx23)):
        blk = np.array(blk, dtype=complex)
        for a, i in enumerate(idx):
            for b, j in enumerate(idx):
                R[i, j] = blk[a, b]
    R[8, 8] = a3
    return R


def fam_generic(a, x1, x3, branch=0):
    # b = x1 x3 * beta,  beta^2 a (a-1) + beta (a-1) + a = 0
    disc = np.sqrt(complex((a - 1) ** 2 - 4 * a * a * (a - 1)))
    beta = (-(a - 1) + (1 if branch == 0 else -1) * disc) / (2 * a * (a - 1))
    b = beta * x1 * x3
    B13 = [
        [a, x1, b],
        [x3 * (a - 1) / b, (x1 * x3 + b) / b, x3],
        [x3**2 * x1**2 / b**3, -x1 * (a * b + x1 * x3) / (a * b**2), -x1 * x3 / (a * b)],
    ]
    return build_acc(1, np.eye(2), B13, np.eye(2), 1)


def fam_generic_beta(a, x1, x3, branch=0):
    # second printed form, sol:case1, with b13 = beta x1 x3 (should coincide with fam_generic)
    disc = np.sqrt(complex((a - 1) ** 2 - 4 * a * a * (a - 1)))
    beta = (-(a - 1) + (1 if branch == 0 else -1) * disc) / (2 * a * (a - 1))
    B13 = [
        [a, x1, beta * x1 * x3],
        [(a - 1) / (beta * x1), (beta + 1) / beta, x3],
        [1 / (beta**3 * x1 * x3), -(a * beta + 1) / (a * beta**2 * x3), -1 / (a * beta)],
    ]
    return build_acc(1, np.eye(2), B13, np.eye(2), 1)


def fam_3_1_1(a, c, x4):
    B12 = [[0, a**2 / c], [c, 1 - a**2]]
    B13 = [
        [0, 0, a**4 / c**2],
        [0, a, a * (a**2 - 1) ** 2 / x4],
        [c**2, x4, (a + 1) * (a - 1) ** 2],
    ]
    return build_acc(1, B12, B13, B12, 1)


def fam_3_1_2(a, c, x4, w):
    B12 = [[0, w * a / c], [c, 1 - w * a]]
    B13 = [
        [0, 0, w**2 * a**2 / c**2],
        [0, a, (w**2 - a) * (a - 1) * a / x4],
        [c**2, x4, (1 - w * a) * (1 - a)],
    ]
    B23 = [[0, a**2 / c], [w**2 * a * c, w * a * (a - 1)]]
    return build_acc(1, B12, B13, B23, w * a**2)


def fam_5_2_1(b, c, x3):
    B13 = [[1 - b * c, 0, b / c], [-x3 * c**2, 1, x3], [c**2, 0, 0]]
    B23 = [[1 - b * c, b], [c, 0]]
    return build_acc(1, np.eye(2), B13, B23, 1)


def fam_5_2_2(b, c, x3):
    B13 = [[1 - b * c, 0, -(b**2)], [x3 * c / b, 1, x3], [-c / b, 0, 0]]
    B23 = [[1 - b * c, b], [c, 0]]
    return build_acc(1, np.eye(2), B13, B23, -b * c)


def fam_5_4_a(b, c, x3):
    B12 = [[1 - b * c, b], [c, 0]]
    B13 = [[1 - b * c, 0, b / c], [-x3 * c**2, 1, x3], [c**2, 0, 0]]
    return build_acc(1, B12, B13, B12, 1)


def fam_5_4_b(b, c, x3):
    B12 = [[1 - b * c, b], [c, 0]]
    B13 = [[1 - b * c, 0, b / c], [x3 * c / b, -b * c, x3], [c**2, 0, 0]]
    return build_acc(1, B12, B13, B12, 1)


def fam_5_5_1_1(c, x2, w):
    B12 = [[1 - w, w / c], [c, 0]]
    B13 = [[0, 0, w / c**2], [x2, 1, -x2 * w / c**2], [c**2, 0, 1 - w]]
    B23 = [[0, w**2 / c], [c * w**2, 1 - w]]
    return build_acc(1, B12, B13, B23, 1)


def fam_5_5_1_2(c, x2, s):
    B12 = [[s + 1, -s / c], [c, 0]]
    B13 = [[0, 0, -s / c**2], [x2, 1, x2 * s / c**2], [c**2, 0, s + 1]]
    B23 = [[0, -1 / c], [s * c, s + 1]]
    return build_acc(1, B12, B13, B23, s)


def fam_5_7(b, x2, x3, eps):
    B12 = [[0, b], [1 / b, 0]]
    B13 = [[0, 0, b**2], [x2, eps, x3], [1 / b**2, 0, 0]]
    return build_acc(1, B12, B13, B12, 1)


def fam_6_2_1a(c, x4, eps):
    B12 = [[0, 1 / c], [c, 0]]
    B13 = [[0, 0, 1 / c**2], [0, eps, 0], [c**2, x4, 0]]
    return build_acc(1, B12, B13, B12, 1)


def fam_6_2_1p(c, x4, w):
    B12 = [[0, 1 / c], [c, 0]]
    B13 = [[0, 0, 1 / c**2], [0, w, 0], [c**2, x4, 0]]
    B23 = [[0, w**2 / c], [w**2 * c, w - 1]]
    return build_acc(1, B12, B13, B23, w)


def fam_6_2_2(c, x4, w):
    B12 = [[0, 1 / (c * w)], [c, w + 2]]
    B13 = [[0, 0, 1 / (c**2 * w**2)], [0, 1, 0], [c**2, x4, 0]]
    B23 = [[0, 1 / c], [w * c, 0]]
    return build_acc(1, B12, B13, B23, w**2)


def table1_families(rng):
    """Instances of every Table-1 family of arXiv:2310.03816 with random parameters. Returns {name: R}."""

    def z():
        return complex(rng.normal(), rng.normal())

    w = np.exp(2j * np.pi / 3)
    out = {}
    a = 0.3 + 0.2j
    out["I   generic (b-branch 0)"] = fam_generic(a, z(), z(), 0)
    out["I   generic (b-branch 1)"] = fam_generic(a + 0.5, z(), z(), 1)
    out["I   generic, beta-form"] = fam_generic_beta(a - 0.7, z(), z(), 0)
    out["III.1.1"] = fam_3_1_1(z(), z(), z())
    for ww in (w, w**2):
        out["III.1.2 w=%s" % ("w" if ww == w else "w^2")] = fam_3_1_2(z(), z(), z(), ww)
    out["V.2.1"] = fam_5_2_1(z(), z(), z())
    out["V.2.2"] = fam_5_2_2(z(), z(), z())
    out["V.4.a"] = fam_5_4_a(z(), z(), z())
    out["V.4.b"] = fam_5_4_b(z(), z(), z())
    for ww in (w, w**2):
        out["V.5.1.1 w=%s" % ("w" if ww == w else "w^2")] = fam_5_5_1_1(z(), z(), ww)
    for s in (1j, -1j):
        out["V.5.1.2 s=%s" % ("i" if s == 1j else "-i")] = fam_5_5_1_2(z(), z(), s)
    for e in (1, -1):
        out["V.7 eps=%d" % e] = fam_5_7(z(), z(), z(), e)
        out["VI.2.1a eps=%d" % e] = fam_6_2_1a(z(), z(), e)
    for ww in (w, w**2):
        out["VI.2.1p w=%s" % ("w" if ww == w else "w^2")] = fam_6_2_1p(z(), z(), ww)
        out["VI.2.2 w=%s" % ("w" if ww == w else "w^2")] = fam_6_2_2(z(), z(), ww)
    return out


# ----------------------------------------------------------------------------------------
# Hietarinta 2x2 families (as printed in arXiv:2409.05375 eq. Hietarinta4by4; braided form)
# ----------------------------------------------------------------------------------------


def hiet_families(rng):
    def z():
        return complex(rng.normal(), rng.normal())

    k, p, q, s = z(), z(), z(), z()
    F = {}
    F["H3,1"] = np.array([[k, 0, 0, 0], [0, 0, p, 0], [0, q, 0, 0], [0, 0, 0, s]], dtype=complex)
    F["H2,1"] = np.array(
        [[k * k, 0, 0, 0], [0, k * k - p * q, k * p, 0], [0, k * q, 0, 0], [0, 0, 0, k * k]],
        dtype=complex,
    )
    F["H2,2"] = np.array(
        [[k * k, 0, 0, 0], [0, k * k - p * q, k * p, 0], [0, k * q, 0, 0], [0, 0, 0, -p * q]],
        dtype=complex,
    )
    F["H2,3"] = np.array([[k, p, q, s], [0, 0, k, p], [0, k, 0, q], [0, 0, 0, k]], dtype=complex)
    F["H1,1"] = np.array(
        [
            [p * p + 2 * p * q - q * q, 0, 0, p * p - q * q],
            [0, p * p - q * q, p * p + q * q, 0],
            [0, p * p + q * q, p * p - q * q, 0],
            [p * p - q * q, 0, 0, p * p - 2 * p * q - q * q],
        ],
        dtype=complex,
    )
    F["H1,2"] = np.array(
        [[p, 0, 0, k], [0, p - q, p, 0], [0, q, 0, 0], [0, 0, 0, -q]], dtype=complex
    )
    F["H1,3"] = np.array(
        [
            [k * k, -k * p, k * p, p * q],
            [0, 0, k * k, k * q],
            [0, k * k, 0, -k * q],
            [0, 0, 0, k * k],
        ],
        dtype=complex,
    )
    F["H1,4"] = np.array([[0, 0, 0, p], [0, k, 0, 0], [0, 0, k, 0], [q, 0, 0, 0]], dtype=complex)
    F["H0,1"] = np.array([[1, 0, 0, 1], [0, 0, -1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], dtype=complex)
    F["H0,2"] = np.array([[1, 0, 0, 1], [0, 1, 1, 0], [0, -1, 1, 0], [-1, 0, 0, 1]], dtype=complex)
    F["P (flip)"] = flip(2).astype(complex)
    return F


# ----------------------------------------------------------------------------------------
# fast Jacobian (block-copy form of the E_{IJ} (x) 1 placement); verified against jac_F_ref
# ----------------------------------------------------------------------------------------
jac_F_ref = jac_F


def jac_F_fast(R, N):
    K2 = N * N
    M = N ** 3
    I3 = np.eye(N)
    A = np.kron(R, I3)
    B = np.kron(I3, R)
    BA = B @ A
    AB = A @ B
    K4 = K2 * K2

    def Ta(X, I, J):  # (E_IJ (x) 1) X
        out = np.zeros((K2, N, M), dtype=complex)
        out[I] = X.reshape(K2, N, M)[J]
        return out.reshape(M, M)

    def Tb(X, I, J):  # X (E_IJ (x) 1)
        out = np.zeros((M, K2, N), dtype=complex)
        out[:, J, :] = X.reshape(M, K2, N)[:, I, :]
        return out.reshape(M, M)

    def Tc(X, I, J):  # (1 (x) E_IJ) X
        out = np.zeros((N, K2, M), dtype=complex)
        out[:, I, :] = X.reshape(N, K2, M)[:, J, :]
        return out.reshape(M, M)

    def Td(X, I, J):  # X (1 (x) E_IJ)
        out = np.zeros((M, N, K2), dtype=complex)
        out[:, :, J] = X.reshape(M, N, K2)[:, :, I]
        return out.reshape(M, M)

    dF = np.empty((K4, M, M), dtype=complex)
    for I in range(K2):
        for J in range(K2):
            k = I * K2 + J
            dF[k] = (Ta(BA, I, J) + A @ Tc(A, I, J) + Tb(AB, I, J)
                     - Tc(AB, I, J) - B @ Ta(B, I, J) - Td(BA, I, J))
    return dF.reshape(K4, -1).T
