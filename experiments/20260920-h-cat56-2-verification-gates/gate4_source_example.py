# ruff: noqa: E501
"""Gate 4 (source positive control): reproduce the published End Matter example of
arXiv:2601.21801 with the SAME generic pipeline used for the H-CAT56-2 counterexample.

Published (WebFetch of the arXiv HTML, 2026-09-20): two-qubit primary system + qubit ancilla,
  rho_0 = q |0,+><0,+| (x) |0><0| + (1-q) |1,phi><1,phi| (x) |1><1|,  |phi> = cos(t/2)|0>+sin(t/2)|1>,
  H_1 = l1 Z(x)Z, H_2 = l2 X(x)X  (commuting),  F^Q = diag(4, 4q + 4(1-q) sin^2 t)
(the paper's stated ordering of the two entries may differ from the parameter ordering used here;
eigenvalues are compared as a SET).

The generic analyser assumes nothing about the quasi-pure block form: SLD is solved from the
defining equation, PCC is checked on the full commutators, V is built from the paper's sigma
operators. What the paper does NOT print is dim V, so that number is a derived one (recorded as
such, not as a reproduction).
"""

from __future__ import annotations

import json
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
from scipy.linalg import expm

X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def kron(*ms: np.ndarray) -> np.ndarray:
    out = np.array([[1.0 + 0j]])
    for m in ms:
        out = np.kron(out, m)
    return out


def ket(v: list[complex]) -> np.ndarray:
    a = np.array(v, dtype=complex)
    return a / np.linalg.norm(a)


def herm_vec(m: np.ndarray) -> np.ndarray:
    iu = np.triu_indices(m.shape[0], 1)
    return np.concatenate([m.diagonal().real, np.sqrt(2) * m[iu].real, np.sqrt(2) * m[iu].imag])


def sld(rho: np.ndarray, drho: np.ndarray) -> np.ndarray:
    w, u = np.linalg.eigh(rho)
    dd = u.conj().T @ drho @ u
    den = w[:, None] + w[None, :]
    lam = np.where(den > 1e-12, 2 * dd / np.where(den > 1e-12, den, 1), 0)
    return u @ lam @ u.conj().T


def analyse(rho: np.ndarray, drhos: list[np.ndarray], r: int) -> dict:
    d = rho.shape[0]
    s = len(drhos)
    w, u = np.linalg.eigh(rho)
    order = np.argsort(w)[::-1]
    psi = u[:, order[:r]]
    pi_r = psi @ psi.conj().T
    lsld = [sld(rho, m) for m in drhos]
    qf = np.array(
        [
            [np.real(np.trace(rho @ (lsld[i] @ lsld[j] + lsld[j] @ lsld[i])) / 2) for j in range(s)]
            for i in range(s)
        ]
    )
    pcc = max(
        (
            float(np.max(np.abs(pi_r @ (lsld[i] @ lsld[j] - lsld[j] @ lsld[i]) @ pi_r)))
            for i in range(s)
            for j in range(i + 1, s)
        ),
        default=0.0,
    )
    quasi = max(float(np.max(np.abs(pi_r @ m @ pi_r))) for m in drhos)

    def proj(a: int, b: int) -> np.ndarray:
        return np.outer(psi[:, a], psi[:, b].conj())

    sigmas = [proj(a, a) for a in range(r)]
    for a in range(r):
        for b in range(a + 1, r):
            sigmas.append(proj(a, b) + proj(b, a))
            sigmas.append(-1j * (proj(a, b) - proj(b, a)))
    rows = []
    for i in range(s):
        for sg in sigmas:
            rows.append(herm_vec(1j * (sg @ lsld[i] - lsld[i] @ sg)))
    for i in range(s):
        for j in range(i + 1, s):
            for sg in sigmas:
                ww = lsld[i] @ sg @ lsld[j] - (lsld[i] @ sg @ lsld[j]).conj().T
                rows.append(herm_vec(1j * ww))
    sv = np.linalg.svd(np.array(rows), compute_uv=False)
    out = {"d": d, "r": r, "s": s, "pcc_residual": pcc, "quasi_pure_residual": quasi}
    out["qfim_eigs"] = sorted(float(x) for x in np.linalg.eigvalsh(qf))
    for tol in (1e-6, 1e-8, 1e-10, 1e-12):
        out[f"dimV_tol{tol:g}"] = int(np.sum(sv > tol * sv[0]))
    dim = out["dimV_tol1e-08"]
    out["dimVperp"] = d * d - dim
    out["dimVperp_ge_d_(saturation_not_excluded)"] = bool(d * d - dim >= d)
    out["gap_ratio"] = float(sv[dim - 1] / sv[dim]) if dim < len(sv) and sv[dim] > 0 else None
    return out


def example(q: float, theta: float, l1: float, l2: float) -> dict:
    zz, xx = kron(Z, Z), kron(X, X)
    h = l1 * zz + l2 * xx
    u2 = expm(-1j * h)  # H1, H2 commute, so d_i U = -i G_i U
    plus = ket([1, 1])
    k0 = ket([1, 0])
    k1 = ket([0, 1])
    phi = ket([np.cos(theta / 2), np.sin(theta / 2)])
    v0 = u2 @ np.kron(k0, plus)
    v1 = u2 @ np.kron(k1, phi)
    a0, a1 = np.outer(k0, k0.conj()), np.outer(k1, k1.conj())
    rho = q * np.kron(np.outer(v0, v0.conj()), a0) + (1 - q) * np.kron(np.outer(v1, v1.conj()), a1)
    drhos = []
    for g in (zz, xx):
        gg = np.kron(g, I2)
        drhos.append(-1j * (gg @ rho - rho @ gg))  # d rho = -i [G, rho], G commutes with U
    res = analyse(rho, drhos, 2)
    res["paper_F_Q_set"] = sorted([4.0, 4 * q + 4 * (1 - q) * np.sin(theta) ** 2])
    res["params"] = {"q": q, "theta": theta, "l1": l1, "l2": l2}
    res["qfim_matches_paper_formula"] = bool(
        np.allclose(res["qfim_eigs"], res["paper_F_Q_set"], atol=1e-8)
    )
    return res


def main() -> int:
    outs = []
    for q, th, l1, l2 in [(0.3, 0.7, 0.4, 0.9), (0.5, 1.1, 0.2, 0.3), (0.8, 0.4, 1.0, 0.6)]:
        r = example(q, th, l1, l2)
        outs.append(r)
        print(
            f"q={q} t={th}: F^Q eig {r['qfim_eigs']} vs paper {r['paper_F_Q_set']} "
            f"match={r['qfim_matches_paper_formula']} pcc={r['pcc_residual']:.1e} "
            f"quasi={r['quasi_pure_residual']:.1e} dimV={r['dimV_tol1e-08']} "
            f"dimVperp={r['dimVperp']} (d={r['d']}) tolsweep="
            f"{[r[f'dimV_tol{t:g}'] for t in (1e-6, 1e-8, 1e-10, 1e-12)]}"
        )
    path = os.path.join(os.path.dirname(__file__), "metrics", "gate4_source_example.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(outs, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
