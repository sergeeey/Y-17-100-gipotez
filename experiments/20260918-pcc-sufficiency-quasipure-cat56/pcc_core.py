"""Core numerics for H-CAT56-1 (PCC-SUFFICIENCY-QUASIPURE-v1).

Implements, directly from Yang, Imai & Pezze, arXiv:2601.21801 (LaTeX source read
directly, `main-final.tex`):

* SLD from the defining Lyapunov equation `(L_i rho + rho L_i)/2 = d_i rho`, solved
  by the spectral element formula `<e_k|L_i|e_l> = 2<e_k|d_i rho|e_l>/(w_k + w_l)`,
  with the standard `0` convention on the kernel-kernel block where `w_k + w_l = 0`.
* PCC, Eq. (8) of the paper (`\\label{eq:PCC}`):
  `<psi_a|[L_i, L_j]|psi_b> = 0` for all `i != j`, `a, b` in the support.
* Theorem 1 (Simultaneous Hollowization, `\\label{thm:Simultaneous...}`), Eqs. (9)/(10)
  (`eq:W-opt` / `eq:M-opt`): a rank-one `E_w = |pi_w><pi_w|` saturates the outcome-wise
  bound iff `<pi_w|W_ij,ab|pi_w> = 0` and `<pi_w|M_i,ab|pi_w> = 0`, with
  `P_ab = |psi_a><psi_b|`, `M_i,ab = [L_i, P_ab]`, `W_ij,ab = L_i P_ab L_j - L_j P_ab L_i`.
* The real Hermitian span `V = span_R{i W^(alpha)_ij,ab, i M^(alpha)_i,ab}` and
  `n = dim V_perp - 1 = d^2 - 1 - dim V` (paper: "n = dim V_perp - 1 <= d^2 - 1").
* Eq. (15) sufficiency threshold (`eq:suff-ineq`):
  `n >= max_{mu in [1, d-2]} 2 mu (d + 1/2 - mu) + (d - 2)`.
* Observation 2 (`obs: dim-bound`): if `n < d - 1` the QCRB cannot be saturated.
  This is a theorem and is the only *proof-grade* non-saturability verdict available here.
* The paper's own global-saturation criterion (End Matter, "Numerical algorithms"):
  a complete optimal rank-one POVM exists iff `I/d` is a convex combination of rank-one
  projectors lying inside `V_perp`.

Every formula above was transcribed from the primary LaTeX source, not from a summary.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.linalg import eigh, expm
from scipy.optimize import least_squares

# ---------------------------------------------------------------------------
# Pre-registered numerical tolerances (controls.md: 1e-8 relative to operator norm).
# ---------------------------------------------------------------------------
TOL_REL = 1e-8
EIG_ZERO = 1e-9  # w_k + w_l below this is treated as the kernel-kernel block


# ---------------------------------------------------------------------------
# Small linear-algebra helpers
# ---------------------------------------------------------------------------
def herm(a: np.ndarray) -> np.ndarray:
    """Hermitian part (kills accumulated round-off asymmetry)."""
    return 0.5 * (a + a.conj().T)


def random_hermitian(d: int, rng: np.random.Generator) -> np.ndarray:
    g = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    return herm(g) / np.sqrt(2 * d)


def random_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    g = (rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))) / np.sqrt(2)
    q, r = np.linalg.qr(g)
    return q * (np.diag(r) / np.abs(np.diag(r)))


def herm_to_real_vec(a: np.ndarray) -> np.ndarray:
    """Isometry Herm(d) -> R^{d^2} for the real inner product <A,B> = Tr(AB)."""
    d = a.shape[0]
    iu = np.triu_indices(d, 1)
    return np.concatenate(
        [np.real(np.diag(a)), np.sqrt(2) * np.real(a[iu]), np.sqrt(2) * np.imag(a[iu])]
    )


# ---------------------------------------------------------------------------
# SLD
# ---------------------------------------------------------------------------
def spectral_sld(rho: np.ndarray, drho: np.ndarray) -> np.ndarray:
    """SLD via the spectral element formula. Kernel-kernel block set to 0."""
    w, v = eigh(herm(rho))
    dr = v.conj().T @ herm(drho) @ v
    s = w[:, None] + w[None, :]
    safe = np.where(np.abs(s) > EIG_ZERO, s, 1.0)
    lam = np.where(np.abs(s) > EIG_ZERO, 2.0 * dr / safe, 0.0)
    return herm(v @ lam @ v.conj().T)


def sld_residual(sld: np.ndarray, rho: np.ndarray, drho: np.ndarray) -> float:
    """||(L rho + rho L)/2 - d rho||_F, the defining equation's own residual."""
    return float(np.linalg.norm(0.5 * (sld @ rho + rho @ sld) - drho))


def support_eigenvectors(rho: np.ndarray, rank: int) -> tuple[np.ndarray, np.ndarray]:
    """Return (eigenvalues, eigenvectors as columns) of the `rank` largest eigenvalues."""
    w, v = eigh(herm(rho))
    order = np.argsort(w)[::-1][:rank]
    return w[order], v[:, order]


# ---------------------------------------------------------------------------
# Quasi-pure state models
# ---------------------------------------------------------------------------
@dataclass
class Model:
    """A local estimation model at lambda = 0: rho, its s derivatives, generators."""

    rho: np.ndarray
    drho: list[np.ndarray]
    gens: list[np.ndarray]
    rank: int
    label: str = ""
    meta: dict = field(default_factory=dict)

    @property
    def d(self) -> int:
        return self.rho.shape[0]

    @property
    def s(self) -> int:
        return len(self.drho)

    def rho_at(self, lam: np.ndarray) -> np.ndarray:
        """rho(lambda) = V(lambda) rho_0 V(lambda)^dag, used for finite-difference checks."""
        gen = sum(lk * gk for lk, gk in zip(lam, self.gens, strict=True))
        u = expm(-1j * gen)
        return u @ self.rho @ u.conj().T

    def fd_drho(self, eps: float = 1e-5) -> list[np.ndarray]:
        out = []
        for i in range(self.s):
            e = np.zeros(self.s)
            e[i] = eps
            out.append((self.rho_at(e) - self.rho_at(-e)) / (2 * eps))
        return out


def _solve_constraints(
    x0: np.ndarray, residual_fn, max_nfev: int = 400
) -> tuple[np.ndarray, float]:
    sol = least_squares(residual_fn, x0, xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=max_nfev)
    return sol.x, float(np.max(np.abs(sol.fun)))


def sample_bipartite_quasipure(
    d_sys: int,
    rank: int,
    s: int,
    rng: np.random.Generator,
    enforce_pcc: bool = True,
) -> Model | None:
    """Eq. (16) of the paper: rho = (U_lam x I) rho_0 (U_lam^dag x I), classical ancilla.

    Ordering is primary (x) ancilla. `d = d_sys * rank`. PCC for this class reduces to
    Eq. (17), `Im <D_i phi_a|D_j phi_a> = 0`, which at lambda = 0 with
    `U = exp(-i sum_j lam_j H_j)` is exactly `<phi_a|[H_i, H_j]|phi_a> = 0`.
    """
    ham = [random_hermitian(d_sys, rng) for _ in range(s)]
    comms = [1j * (ham[i] @ ham[j] - ham[j] @ ham[i]) for i in range(s) for j in range(i + 1, s)]

    phis = []
    for _ in range(rank):
        z0 = rng.normal(size=2 * d_sys)

        def res(x: np.ndarray, _c=comms) -> np.ndarray:
            vec = (x[:d_sys] + 1j * x[d_sys:]).astype(complex)
            nrm = np.linalg.norm(vec)
            out = [nrm**2 - 1.0]
            if enforce_pcc and nrm > 1e-12:
                unit = vec / nrm
                out += [float(np.real(unit.conj() @ (c @ unit))) for c in _c]
            elif enforce_pcc:
                out += [1.0] * len(_c)
            return np.array(out)

        xs, viol = _solve_constraints(z0, res)
        vec = xs[:d_sys] + 1j * xs[d_sys:]
        vec = vec / np.linalg.norm(vec)
        if enforce_pcc and viol > 1e-9:
            return None
        phis.append(vec)

    q = rng.uniform(0.15, 1.0, size=rank)
    q = q / q.sum()
    d = d_sys * rank
    rho0 = np.zeros((d, d), dtype=complex)
    anc = np.eye(rank)
    for a in range(rank):
        rho0 += q[a] * np.kron(np.outer(phis[a], phis[a].conj()), np.outer(anc[a], anc[a]))
    gens = [np.kron(h, np.eye(rank)) for h in ham]
    drho = [-1j * (g @ rho0 - rho0 @ g) for g in gens]
    return Model(
        rho=herm(rho0),
        drho=[herm(x) for x in drho],
        gens=gens,
        rank=rank,
        label=f"bipartite(d_sys={d_sys},r={rank},s={s})",
        meta={"q": q.tolist(), "d_sys": d_sys},
    )


def sample_generic_quasipure(
    d: int,
    rank: int,
    s: int,
    rng: np.random.Generator,
    enforce_pcc: bool = True,
    kernel_block: bool = False,
    randomize_basis: bool = True,
) -> Model | None:
    """Generic quasi-pure state, Yang arXiv:2405.00405 Eq. (12): `Pi_r d_i rho Pi_r = 0`.

    With parameter-independent spectrum and `rho_0 = diag(q_1..q_r, 0..0)`, quasi-purity
    is equivalent to the support-support block of every generator being diagonal; the
    SLD then depends only on the kernel-support blocks `B_i = Pi_k G_i Pi_r`, and PCC
    (Eq. 8) is equivalent to `B_i^dag B_j` being Hermitian for every pair `i != j`.
    Both statements are re-verified numerically by the harness rather than assumed.
    """
    k = d - rank
    if k < 1:
        return None

    def unpack(x: np.ndarray) -> list[np.ndarray]:
        blocks = []
        stride = 2 * k * rank
        for i in range(s):
            chunk = x[i * stride : (i + 1) * stride]
            re = chunk[: k * rank].reshape(k, rank)
            im = chunk[k * rank :].reshape(k, rank)
            blocks.append(re + 1j * im)
        return blocks

    x0 = rng.normal(size=2 * k * rank * s)

    def res(x: np.ndarray) -> np.ndarray:
        bs = unpack(x)
        out = [float(np.linalg.norm(x) ** 2 - (2 * k * rank * s))]
        if enforce_pcc:
            for i in range(s):
                for j in range(i + 1, s):
                    m = bs[i].conj().T @ bs[j]
                    diff = m - m.conj().T
                    out += list(np.real(diff).ravel()) + list(np.imag(diff).ravel())
        return np.array(out)

    xs, viol = _solve_constraints(x0, res)
    if enforce_pcc and viol > 1e-9:
        return None
    bmats = unpack(xs)

    q = rng.uniform(0.15, 1.0, size=rank)
    q = q / q.sum()
    rho0 = np.diag(np.concatenate([q, np.zeros(k)])).astype(complex)

    gens = []
    for b in bmats:
        g = np.zeros((d, d), dtype=complex)
        g[rank:, :rank] = b
        g[:rank, rank:] = b.conj().T
        if kernel_block:
            g[rank:, rank:] = random_hermitian(k, rng)
        gens.append(herm(g))

    if randomize_basis:
        u = random_unitary(d, rng)
        rho0 = u @ rho0 @ u.conj().T
        gens = [u @ g @ u.conj().T for g in gens]

    drho = [-1j * (g @ rho0 - rho0 @ g) for g in gens]
    return Model(
        rho=herm(rho0),
        drho=[herm(x) for x in drho],
        gens=gens,
        rank=rank,
        label=f"generic(d={d},r={rank},s={s})",
        meta={"q": q.tolist(), "kernel_block": kernel_block},
    )


# ---------------------------------------------------------------------------
# PCC and Theorem 1 machinery
# ---------------------------------------------------------------------------
@dataclass
class Analysis:
    d: int
    s: int
    rank: int
    sld_residual: float
    pcc_violation: float
    pcc_holds: bool
    dim_v: int
    dim_v_perp: int
    n: int
    rhs: float
    below_threshold: bool
    trace_violation: float
    v_basis: np.ndarray  # (dim_v, d, d) orthonormal Hermitian basis of V
    slds: list[np.ndarray]
    psis: np.ndarray  # (d, rank)
    qfim: np.ndarray
    singular_values: np.ndarray
    singular_spectrum_rel: list
    rank_plateau: dict
    gram_rank: int
    rank_gap_ratio: float
    rank_is_robust: bool
    certified_not_saturable: bool
    qfim_rank: int
    qfim_min_eig: float


def rhs_threshold(d: int) -> float:
    """RHS of Eq. (15): max_{mu in [1, d-2]} 2 mu (d + 1/2 - mu) + (d - 2)."""
    if d < 3:
        return float("-inf")
    return max(2 * mu * (d + 0.5 - mu) + (d - 2) for mu in range(1, d - 1))


def _sigma_ops(psis: np.ndarray) -> list[tuple[str, int, int, np.ndarray]]:
    """sigma^x_ab, sigma^y_ab (a<b) and sigma^z_aa, exactly as defined in the paper."""
    r = psis.shape[1]
    out = []
    for a in range(r):
        p_aa = np.outer(psis[:, a], psis[:, a].conj())
        out.append(("z", a, a, p_aa))
    for a in range(r):
        for b in range(a + 1, r):
            p_ab = np.outer(psis[:, a], psis[:, b].conj())
            p_ba = np.outer(psis[:, b], psis[:, a].conj())
            out.append(("x", a, b, p_ab + p_ba))
            out.append(("y", a, b, -1j * (p_ab - p_ba)))
    return out


def analyse(model: Model, tol_rel: float = TOL_REL) -> Analysis:
    d, s, r = model.d, model.s, model.rank
    slds = [spectral_sld(model.rho, dr) for dr in model.drho]
    res = max(sld_residual(lo, model.rho, dr) for lo, dr in zip(slds, model.drho, strict=True))
    _, psis = support_eigenvectors(model.rho, r)

    # --- PCC, Eq. (8) --------------------------------------------------------
    scale = max(float(np.linalg.norm(lo, 2)) for lo in slds)
    pcc = 0.0
    for i in range(s):
        for j in range(i + 1, s):
            comm = slds[i] @ slds[j] - slds[j] @ slds[i]
            block = psis.conj().T @ comm @ psis
            pcc = max(pcc, float(np.max(np.abs(block))))
    pcc_rel = pcc / max(scale**2, 1e-300)

    # --- V = span_R{i W^(alpha), i M^(alpha)} --------------------------------
    sigmas = _sigma_ops(psis)
    mats: list[np.ndarray] = []
    for _, _, _, sig in sigmas:
        for i in range(s):
            mats.append(1j * (sig @ slds[i] - slds[i] @ sig))  # i M^(alpha)
        for i in range(s):
            for j in range(i + 1, s):
                w = slds[i] @ sig @ slds[j] - slds[j] @ sig @ slds[i]
                mats.append(1j * w)  # i W^(alpha)
    mats = [herm(m) for m in mats]
    mat_scale = max(float(np.linalg.norm(m)) for m in mats) if mats else 1.0
    trace_viol = max(abs(float(np.real(np.trace(m)))) for m in mats) / max(mat_scale, 1e-300)

    vecs = np.array([herm_to_real_vec(m) for m in mats])
    _, sv, vt = np.linalg.svd(vecs, full_matrices=False)
    sv0 = float(sv[0]) if sv.size else 0.0
    cutoff = sv0 * tol_rel
    dim_v = int(np.sum(sv > cutoff))
    v_basis = (
        np.array([_vec_to_herm(vt[i], d) for i in range(dim_v)])
        if dim_v
        else np.zeros((0, d, d), dtype=complex)
    )

    # --- rank diagnostics: is dim V (hence dim V_perp) robust, or a round-off artifact?
    # WHY: the whole certified counterexample test is a rank deficiency of `vecs`. A rank
    # read off at one arbitrary threshold is not evidence; the rank must be flat across
    # several decades of threshold AND agree with an independent numerical route.
    # Pre-registered threshold sweep (NOT tuned after seeing results): if the rank moves
    # anywhere inside this range the sample is NUMERICALLY_AMBIGUOUS, not a counterexample.
    plateau = {
        f"{thr:.0e}": int(np.sum(sv > sv0 * thr)) for thr in (1e-5, 1e-6, 1e-8, 1e-10, 1e-12)
    }
    # WHY 1e-12 and not tol_rel**2 = 1e-16: Gram eigenvalues are SQUARED singular values,
    # so a 1e-16 relative cut sits exactly on the float64 eigenvalue noise floor of
    # `vecs @ vecs.T` and overcounts the rank. Measured: with 1e-16 this route disagreed
    # with the SVD route on ~52% of d=4 samples purely from round-off. 1e-12 on the Gram
    # (= 1e-6 on singular values) is far above that floor and far below the real gap,
    # which is >= 1e9 in singular-value terms on every sample seen here.
    gram_eig = np.linalg.eigvalsh(vecs @ vecs.T)
    gram_rank = int(np.sum(gram_eig > max(gram_eig) * 1e-12)) if gram_eig.size else 0
    if dim_v < sv.size and sv[dim_v] > 0:
        gap = float(sv[dim_v - 1] / sv[dim_v]) if dim_v > 0 else float("inf")
    else:
        gap = float("inf")  # the discarded block is numerically exactly zero
    rank_robust = bool(len(set(plateau.values())) == 1 and gram_rank == dim_v and gap > 1e4)

    dim_v_perp = d * d - dim_v
    n = dim_v_perp - 1
    rhs = rhs_threshold(d)

    qfim = np.array(
        [
            [float(np.real(np.trace(model.rho @ slds[i] @ slds[j]))) for j in range(s)]
            for i in range(s)
        ]
    )
    qfim = 0.5 * (qfim + qfim.T)
    qeig = np.linalg.eigvalsh(qfim)
    qfim_rank = int(np.sum(qeig > max(float(np.max(qeig)), 1e-300) * 1e-10))

    return Analysis(
        d=d,
        s=s,
        rank=r,
        sld_residual=res,
        pcc_violation=pcc_rel,
        pcc_holds=pcc_rel < tol_rel,
        dim_v=dim_v,
        dim_v_perp=dim_v_perp,
        n=n,
        rhs=rhs,
        below_threshold=(n < rhs),
        trace_violation=trace_viol,
        v_basis=v_basis,
        slds=slds,
        psis=psis,
        qfim=qfim,
        singular_values=sv,
        singular_spectrum_rel=(sv / sv0).tolist() if sv0 > 0 else [],
        rank_plateau=plateau,
        gram_rank=gram_rank,
        rank_gap_ratio=gap,
        rank_is_robust=rank_robust,
        certified_not_saturable=bool(dim_v_perp < d),
        qfim_rank=qfim_rank,
        qfim_min_eig=float(np.min(qeig)),
    )


def _vec_to_herm(v: np.ndarray, d: int) -> np.ndarray:
    """Exact inverse of `herm_to_real_vec`."""
    a = np.zeros((d, d), dtype=complex)
    iu = np.triu_indices(d, 1)
    m = len(iu[0])
    a[np.diag_indices(d)] = v[:d]
    a[iu] = (v[d : d + m] + 1j * v[d + m : d + 2 * m]) / np.sqrt(2)
    a = a + np.triu(a, 1).conj().T
    return a
