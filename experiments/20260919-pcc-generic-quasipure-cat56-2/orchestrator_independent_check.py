"""Independent re-check of the H-CAT56-2 counterexample, written by the orchestrator from the
paper's DEFINITIONS, sharing no code with h2_core.py / pcc_core.py / fp_certify.py.

Full d x d matrices throughout:
  rho = diag(p, 0),  d(rho)_i = [[0, B_i],[B_i^dag, 0]]  (quasi-pure: Pi_r d(rho) Pi_r = 0),
  SLD L_i solved from  d(rho)_i = (rho L_i + L_i rho)/2  in the eigenbasis (support-kernel block),
  PCC checked on the FULL commutators: Pi_r [L_i, L_j] Pi_r = 0,
  V = span_R { i W_{ij,ab}^{(alpha)}, i M_{i,ab}^{(alpha)} }  with the paper's sigma operators,
  dim V from an SVD of the real vectorisation in Herm(d), with the singular-value gap reported.
The B_i are drawn by a different sampler than the agent's (random-orthogonal-rotated nullspace
draws with a fresh RNG), and PCC is verified afterwards on the built L_i, not assumed.
"""

from __future__ import annotations

import json
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np


def herm_vec(m: np.ndarray) -> np.ndarray:
    d = m.shape[0]
    iu = np.triu_indices(d, 1)
    return np.concatenate([m.diagonal().real, np.sqrt(2) * m[iu].real, np.sqrt(2) * m[iu].imag])


def draw_blocks(k: int, r: int, s: int, rng: np.random.Generator) -> list[np.ndarray]:
    """A_1..A_s (k x r) with A_i^dag A_j Hermitian for all pairs (real-linear nullspace draws)."""
    n = 2 * k * r
    blocks = [rng.normal(size=(k, r)) + 1j * rng.normal(size=(k, r))]
    for j in range(1, s):
        rows = []
        for i in range(j):
            cols = []
            for t in range(n):
                x = np.zeros(n)
                x[t] = 1.0
                xm = (x[: k * r] + 1j * x[k * r :]).reshape(k, r)
                m = blocks[i].conj().T @ xm
                a = m - m.conj().T  # anti-Hermitian part must vanish
                cols.append(np.concatenate([a.real.ravel(), a.imag.ravel()]))
            rows.append(np.array(cols).T)
        big = np.vstack(rows)
        _, sv, vt = np.linalg.svd(big)
        rank = int(np.sum(sv > 1e-11 * sv[0]))
        null = vt[rank:]
        if null.shape[0] == 0:
            raise RuntimeError(f"no PCC completion at j={j}")
        x = rng.normal(size=null.shape[0]) @ null
        blocks.append((x[: k * r] + 1j * x[k * r :]).reshape(k, r))
    return blocks


def build_state(blocks: list[np.ndarray], p: np.ndarray):
    """rho and d(rho)_i built from the SLD blocks: L_i = [[0, A_i^dag],[A_i, 0]]."""
    k, r = blocks[0].shape
    d = r + k
    rho = np.zeros((d, d), dtype=complex)
    rho[:r, :r] = np.diag(p)
    drho = []
    for a in blocks:
        b = 0.5 * np.diag(p) @ a.conj().T  # support-kernel block of d(rho): (rho L + L rho)/2
        m = np.zeros((d, d), dtype=complex)
        m[:r, r:] = b
        m[r:, :r] = b.conj().T
        drho.append(m)
    return rho, drho


def sld_from_rho(rho: np.ndarray, drho: np.ndarray, r: int) -> np.ndarray:
    """SLD solved independently from the defining equation in the eigenbasis (rho is diagonal here
    but the code uses eigh so it does not assume that)."""
    w, u = np.linalg.eigh(rho)
    dd = u.conj().T @ drho @ u
    denom = w[:, None] + w[None, :]
    lam = np.zeros_like(dd)
    mask = denom > 1e-12
    lam[mask] = 2 * dd[mask] / denom[mask]
    return u @ lam @ u.conj().T


def analyse(k: int, r: int, s: int, seed: int, rotate: bool) -> dict:
    rng = np.random.default_rng(seed)
    d = r + k
    blocks = draw_blocks(k, r, s, rng)
    p = np.array([0.6, 0.4] if r == 2 else np.linspace(1, 2, r) / np.linspace(1, 2, r).sum())
    rho, drho = build_state(blocks, p)
    if rotate:  # random unitary change of basis of the whole Hilbert space
        q, _ = np.linalg.qr(rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)))
        rho = q @ rho @ q.conj().T
        drho = [q @ m @ q.conj().T for m in drho]
    w, u = np.linalg.eigh(rho)
    order = np.argsort(w)[::-1]
    psi = u[:, order[:r]]  # support eigenvectors |psi_a>, columns
    pi_r = psi @ psi.conj().T

    lsld = [sld_from_rho(rho, m, r) for m in drho]
    # SLD equation residual on the (support x anything) part
    sld_res = max(
        float(np.max(np.abs(pi_r @ ((rho @ lm + lm @ rho) / 2 - m))))
        for lm, m in zip(lsld, drho, strict=True)
    )
    quasi = max(float(np.max(np.abs(pi_r @ m @ pi_r))) for m in drho)
    pcc = max(
        float(np.max(np.abs(pi_r @ (lsld[i] @ lsld[j] - lsld[j] @ lsld[i]) @ pi_r)))
        for i in range(s)
        for j in range(i + 1, s)
    )
    qf = np.array(
        [
            [np.real(np.trace(rho @ (lsld[i] @ lsld[j] + lsld[j] @ lsld[i])) / 2) for j in range(s)]
            for i in range(s)
        ]
    )
    ev = np.linalg.eigvalsh(qf)

    # paper's sigma operators on the support
    def proj(a: int, b: int) -> np.ndarray:
        return np.outer(psi[:, a], psi[:, b].conj())

    sigmas = []
    for a in range(r):
        sigmas.append(proj(a, a))
    for a in range(r):
        for b in range(a + 1, r):
            sigmas.append(proj(a, b) + proj(b, a))
            sigmas.append(-1j * (proj(a, b) - proj(b, a)))
    rows = []
    for i in range(s):
        for sg in sigmas:
            mm = sg @ lsld[i] - lsld[i] @ sg  # M_{i,ab} = [sigma, L_i]  (anti-Hermitian)
            rows.append(herm_vec(1j * mm))
    n_m = len(rows)
    for i in range(s):
        for j in range(i + 1, s):
            for sg in sigmas:
                ww = lsld[i] @ sg @ lsld[j] - (lsld[i] @ sg @ lsld[j]).conj().T
                rows.append(herm_vec(1j * ww))
    mat = np.array(rows)
    sv = np.linalg.svd(mat, compute_uv=False)
    top = sv[0]
    # dimension = number of singular values above a tolerance tied to the LARGEST one
    out = {"k": k, "r": r, "s": s, "d": d, "seed": seed, "rotated": rotate}
    for tol in (1e-6, 1e-8, 1e-10, 1e-12):
        out[f"dimV_tol{tol:g}"] = int(np.sum(sv > tol * top))
    dim = out["dimV_tol1e-08"]
    out["dimVperp"] = d * d - dim
    out["fires_dimVperp_lt_d"] = bool(d * d - dim < d)
    # gap around the cut: smallest kept vs largest dropped
    kept = sv[dim - 1]
    dropped = sv[dim] if dim < len(sv) else 0.0
    out["sv_kept_min"] = float(kept)
    out["sv_dropped_max"] = float(dropped)
    out["gap_ratio"] = float(kept / dropped) if dropped > 0 else float("inf")
    out["n_generators"] = int(mat.shape[0])
    out["n_M_generators"] = n_m
    out["sld_equation_residual"] = sld_res
    out["quasi_pure_residual"] = quasi
    out["pcc_residual_full_commutator"] = pcc
    out["qfim_min_eig"] = float(ev[0])
    out["qfim_max_eig"] = float(ev[-1])
    out["qfim_full_rank"] = bool(ev[0] > 1e-9 * ev[-1])
    out["trace_I_orthogonal_to_V"] = float(np.max(np.abs(mat @ herm_vec(np.eye(d, dtype=complex)))))
    return out


def main() -> None:
    cases = [
        # (k, r, s): the claimed firing config, then controls
        (20, 2, 16),  # d=22 claimed counterexample
        (19, 2, 16),  # d=21: bound says it can never fire
        (20, 2, 8),  # d=22 with small s: should not fire
        (18, 2, 14),  # d=20
        (21, 2, 17),  # d=23
    ]
    seeds = [777001, 777002]
    results = []
    for k, r, s in cases:
        for seed in seeds:
            for rot in (False, True):
                res = analyse(k, r, s, seed, rot)
                results.append(res)
                print(
                    f"d={res['d']} r={r} s={s} seed={seed} rot={rot} dimV={res['dimV_tol1e-08']}"
                    f" dimVperp={res['dimVperp']} fires={res['fires_dimVperp_lt_d']}"
                    f" gap={res['gap_ratio']:.2e} pcc={res['pcc_residual_full_commutator']:.1e}"
                    f" qfim_full={res['qfim_full_rank']} tolsweep="
                    f"{[res[f'dimV_tol{t:g}'] for t in (1e-6, 1e-8, 1e-10, 1e-12)]}",
                    flush=True,
                )
    out = os.path.join(os.path.dirname(__file__), "metrics", "orchestrator_independent_check.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)


if __name__ == "__main__":
    sys.exit(main())
