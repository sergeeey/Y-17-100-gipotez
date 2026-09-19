"""Independent routes for claim C-ID / C-LB: dim P, dim Q by nullspace, LB, full-d model."""

from __future__ import annotations

import h2_core as h
import numpy as np


def _nullity(mat: np.ndarray, rel: float = 1e-9) -> int:
    sv = np.linalg.svd(mat, compute_uv=False)
    n_cols = mat.shape[1]
    top = float(sv[0]) if sv.size else 0.0
    if top == 0.0:
        return n_cols
    return n_cols - int(np.sum(sv > rel * top))


def dim_p(blocks: list[np.ndarray]) -> int:
    """dim_R {Y in C^{k x r}: A_i^dag Y Hermitian for all i}."""
    k, r = blocks[0].shape
    n = 2 * k * r
    cols = []
    for t in range(n):
        e = np.zeros(n)
        e[t] = 1.0
        y = (e[: k * r] + 1j * e[k * r :]).reshape(k, r)
        cols.append(
            np.concatenate([h.cvec(b.conj().T @ y - (b.conj().T @ y).conj().T) for b in blocks])
        )
    return _nullity(np.array(cols).T)


def dim_q(blocks: list[np.ndarray]) -> int:
    """dim_R {Z in Herm(k): A_i^dag Z A_j Hermitian for all i<j}."""
    k = blocks[0].shape[0]
    s = len(blocks)
    basis = []
    for a in range(k):
        z = np.zeros((k, k), dtype=complex)
        z[a, a] = 1.0
        basis.append(z)
    for a in range(k):
        for b in range(a + 1, k):
            z = np.zeros((k, k), dtype=complex)
            z[a, b] = z[b, a] = 1.0
            basis.append(z)
            z = np.zeros((k, k), dtype=complex)
            z[a, b] = -1j
            z[b, a] = 1j
            basis.append(z)
    cols = []
    for z in basis:
        parts = []
        for i in range(s):
            for j in range(i + 1, s):
                m = blocks[i].conj().T @ z @ blocks[j]
                parts.append(h.cvec(m - m.conj().T))
        cols.append(np.concatenate(parts))
    return _nullity(np.array(cols).T)


def lb(k: int, r: int, s: int) -> int:
    """Rigorous rank-nullity lower bound on dim V_perp (claim C-LB)."""
    return r * r + max(s, 2 * k * r - s * r * r) + max(1, k * k - (s * (s - 1) // 2) * r * r)


def to_model(blocks: list[np.ndarray], q: np.ndarray, rng: np.random.Generator | None):
    """Full d x d pcc_core.Model: A = -2i B => B = iA/2, G = [[0,B^dag],[B,0]], rho0 = diag(q,0)."""
    pc = h.load_old("pcc_core")
    k, r = blocks[0].shape
    d = k + r
    rho0 = np.diag(np.concatenate([q, np.zeros(k)])).astype(complex)
    gens = []
    for a in blocks:
        b = 0.5j * a
        g = np.zeros((d, d), dtype=complex)
        g[r:, :r] = b
        g[:r, r:] = b.conj().T
        gens.append(pc.herm(g))
    if rng is not None:
        u = pc.random_unitary(d, rng)
        rho0 = u @ rho0 @ u.conj().T
        gens = [u @ g @ u.conj().T for g in gens]
    drho = [-1j * (g @ rho0 - rho0 @ g) for g in gens]
    return pc.Model(
        rho=pc.herm(rho0),
        drho=[pc.herm(x) for x in drho],
        gens=gens,
        rank=r,
        label=f"generic(d={d},r={r},s={len(blocks)})",
    )
