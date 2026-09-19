"""Reduced (block-level) machinery for H-CAT56-2.

For a generic quasi-pure state (Yang arXiv:2405.00405 Eq. 12) with parameter-independent
spectrum, H-CAT56-1 derived (S1-S3, verified numerically there) that in a support/kernel
basis every SLD is  L_i = [[0, A_i^dag], [A_i, 0]]  with  A_i a k x r complex block
(A_i = -2i B_i), that PCC is  A_i^dag A_j Hermitian  (i != j),  and that

    i M_{i,S}  has lower-left block   i A_i S                       (S in Herm(r))
    i W_{ij,S} lives in the kernel block:  i (A_i S A_j^dag - A_j S A_i^dag)

so  dim V = dim V_M + dim V_W  EXACTLY (orthogonal blocks), with  V_M in C^{k x r}
(real dim 2kr) and V_W in traceless Herm(k) (real dim k^2 - 1).  This module computes both
from the A blocks alone, which is ~100x cheaper than the full d x d pipeline of
`pcc_core.analyse`; agreement with that pipeline is tested in `substrate_h2.py`.

Also provides a sampler of the PCC variety that needs NO nonconvex optimisation: PCC is
bilinear, hence LINEAR in A_j once A_1..A_{j-1} are fixed, so a sequential real-nullspace
draw reaches every solution (in particular it is not restricted to one branch).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import caps  # noqa: F401  (must precede numpy: thread env + affinity)
import numpy as np

_OLD = Path(__file__).resolve().parents[1] / "20260918-pcc-sufficiency-quasipure-cat56"


def load_old(name: str):
    """Import a module of the closed H-CAT56-1 folder by path (folder is not modified)."""
    spec = importlib.util.spec_from_file_location(f"h1_{name}", _OLD / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    import sys

    if mod.__name__ in sys.modules:
        return sys.modules[mod.__name__]
    sys.modules[mod.__name__] = mod
    sys.path.insert(0, str(_OLD))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(_OLD))
    return mod


def herm_basis(r: int) -> list[np.ndarray]:
    """Real basis of Herm(r): z_aa, x_ab, y_ab exactly as the paper's sigma operators."""
    out = []
    for a in range(r):
        m = np.zeros((r, r), dtype=complex)
        m[a, a] = 1.0
        out.append(m)
    for a in range(r):
        for b in range(a + 1, r):
            m = np.zeros((r, r), dtype=complex)
            m[a, b] = m[b, a] = 1.0
            out.append(m)
            m = np.zeros((r, r), dtype=complex)
            m[a, b] = -1j
            m[b, a] = 1j
            out.append(m)
    return out


def herm_vec(a: np.ndarray) -> np.ndarray:
    """Isometry Herm(k) -> R^{k^2}."""
    k = a.shape[0]
    iu = np.triu_indices(k, 1)
    return np.concatenate(
        [np.real(np.diag(a)), np.sqrt(2) * np.real(a[iu]), np.sqrt(2) * np.imag(a[iu])]
    )


def cvec(z: np.ndarray) -> np.ndarray:
    return np.concatenate([z.real.ravel(), z.imag.ravel()])


def pcc_violation(blocks: list[np.ndarray]) -> float:
    """max |A_i^dag A_j - (A_i^dag A_j)^dag| over i<j, relative to the EXTERNAL scale
    (sum of squared Frobenius norms), never to the violation's own size."""
    scale = sum(float(np.linalg.norm(b) ** 2) for b in blocks)
    v = 0.0
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            m = blocks[i].conj().T @ blocks[j]
            v = max(v, float(np.max(np.abs(m - m.conj().T))))
    return v / max(scale, 1e-300)


def stacks(blocks: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """Row-stacks whose ranks are dim V_M and dim V_W."""
    r = blocks[0].shape[1]
    s = len(blocks)
    basis = herm_basis(r)
    m_rows = [cvec(1j * (blocks[i] @ sm)) for i in range(s) for sm in basis]
    w_rows = []
    for i in range(s):
        for j in range(i + 1, s):
            for sm in basis:
                x = blocks[i] @ sm @ blocks[j].conj().T
                w = 1j * (x - x.conj().T)
                w_rows.append(herm_vec(0.5 * (w + w.conj().T)))
    return np.array(m_rows), (np.array(w_rows) if w_rows else np.zeros((0, 1)))


def ranks(blocks: list[np.ndarray], tol: float = 1e-9) -> dict:
    """dim V_M, dim V_W with tolerances tied to an EXTERNAL scale (norm of the A blocks),
    plus the kept/dropped singular values so the gap is logged, not assumed."""
    nrm2 = sum(float(np.linalg.norm(b) ** 2) for b in blocks)
    sm, sw = stacks(blocks)
    out = {}
    for tag, mat, ref in (("M", sm, nrm2**0.5 * 1.0), ("W", sw, nrm2)):
        if mat.size == 0:
            out[tag] = {"dim": 0, "sv": [], "kept_min": None, "dropped_max": None, "gap": None}
            continue
        sv = np.linalg.svd(mat, compute_uv=False)
        # M-stack entries are linear in A (scale ref = |A|); W-stack quadratic (scale |A|^2)
        cut = tol * ref
        dim = int(np.sum(sv > cut))
        kept_min = float(sv[dim - 1]) if dim else None
        dropped_max = float(sv[dim]) if dim < sv.size else 0.0
        gap = (
            (kept_min / dropped_max)
            if (kept_min and dropped_max > 0)
            else (float("inf") if kept_min else None)
        )
        out[tag] = {
            "dim": dim,
            "sv": sv.tolist(),
            "kept_min": kept_min,
            "dropped_max": dropped_max,
            "gap": gap,
        }
    out["dim_v"] = out["M"]["dim"] + out["W"]["dim"]
    return out


def sample_sequential(
    k: int,
    r: int,
    s: int,
    rng: np.random.Generator,
    tol: float = 1e-11,
    first: np.ndarray | None = None,
) -> tuple[list[np.ndarray], list[int]] | None:
    """Draw A_1..A_s with PCC exactly (to machine precision) by sequential nullspace draws.

    Returns (blocks, nullspace_dims) or None when a nullspace beyond the trivial real span of
    earlier blocks is empty (then s is too large for a non-degenerate model here)."""
    n = 2 * k * r
    blocks = [
        first if first is not None else (rng.normal(size=(k, r)) + 1j * rng.normal(size=(k, r)))
    ]
    nulls = [n]
    for j in range(1, s):
        rows = []
        for i in range(j):
            # real-linear map x -> Im-part & Re-part of (A_i^dag X - h.c.), X = mat(x)
            cols = []
            for t in range(n):
                e = np.zeros(n)
                e[t] = 1.0
                x = (e[: k * r] + 1j * e[k * r :]).reshape(k, r)
                m = blocks[i].conj().T @ x
                d = m - m.conj().T
                cols.append(cvec(d))
            rows.append(np.array(cols).T)
        big = np.vstack(rows)
        _, sv, vt = np.linalg.svd(big)
        rankc = int(np.sum(sv > tol * sv[0])) if sv.size else 0
        ns = vt[rankc:]
        nulls.append(int(ns.shape[0]))
        if ns.shape[0] == 0:
            return None
        x = rng.normal(size=ns.shape[0]) @ ns
        blocks.append((x[: k * r] + 1j * x[k * r :]).reshape(k, r))
    return blocks, nulls


def qfim_rank(blocks: list[np.ndarray], q: np.ndarray, tol: float = 1e-10) -> int:
    """QFIM F_ij = sum_a q_a Re (A_i^dag A_j)_aa   (L_i = [[0,A^dag],[A,0]])."""
    s = len(blocks)
    f = np.zeros((s, s))
    for i in range(s):
        for j in range(s):
            m = blocks[i].conj().T @ blocks[j]
            f[i, j] = float(np.real(np.sum(q * np.real(np.diag(m)))))
    w = np.linalg.eigvalsh(0.5 * (f + f.T))
    return int(np.sum(w > tol * max(w.max(), 1e-300)))
