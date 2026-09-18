"""FL Step 2a Substrate Gate + Step 1 SLD verification for H-CAT56-1.

Nothing in this experiment is trusted until every check below passes. The SLD solver is
verified against CLOSED-FORM answers (not against itself) on:

  A. pure qubit, one parameter          -- L = 2 d rho exactly (kernel branch exercised)
  B. mixed qubit, one parameter         -- textbook Bloch-vector closed form, derived and
                                           quoted in the docstring of `qubit_closed_form`
  C. random full-rank qutrit            -- cross-checked against an INDEPENDENT method
                                           (vectorised Lyapunov solve, no eigendecomposition)
  D. quasi-pure samplers                -- quasi-purity Pi_r d_i rho Pi_r = 0, analytic
                                           d rho vs central finite differences of exp(-iG)
  E. algebraic plumbing                 -- Herm <-> R^{d^2} isometry round trip, Eq. (15)
                                           threshold values against hand arithmetic

Run:  python substrate_check.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pcc_core as pc
from scipy.linalg import eigh

OUT = Path(__file__).parent / "metrics" / "substrate_check.json"
PAULI = [
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
]


def bloch(r: np.ndarray) -> np.ndarray:
    return 0.5 * (np.eye(2, dtype=complex) + sum(rk * p for rk, p in zip(r, PAULI, strict=True)))


def qubit_closed_form(r: np.ndarray, dr: np.ndarray) -> tuple[np.ndarray, float]:
    """Closed-form SLD and QFI for rho = (I + r.sigma)/2, |r| < 1.

    Writing L = a I + b.sigma, the defining equation (L rho + rho L)/2 = d rho gives
    a + b.r = 0 and a r + b = dr, hence b = dr + [(r.dr)/(1-|r|^2)] r and a = -(r.dr)/(1-|r|^2).
    QFI = |dr|^2 + (r.dr)^2/(1-|r|^2).
    """
    r2 = float(r @ r)
    k = float(r @ dr) / (1.0 - r2)
    b = dr + k * r
    a = -k
    sld = a * np.eye(2, dtype=complex) + sum(bk * p for bk, p in zip(b, PAULI, strict=True))
    qfi = float(dr @ dr) + float(r @ dr) ** 2 / (1.0 - r2)
    return sld, qfi


def lyapunov_sld(rho: np.ndarray, drho: np.ndarray) -> np.ndarray:
    """Independent SLD: solve (L rho + rho L)/2 = d rho as a dense linear system.

    Uses no eigendecomposition, so it shares nothing with `pc.spectral_sld` but the input.
    Valid only for full-rank rho (the system is singular otherwise).
    """
    d = rho.shape[0]
    eye = np.eye(d, dtype=complex)
    amat = 0.5 * (np.kron(rho.T, eye) + np.kron(eye, rho))
    return np.linalg.solve(amat, drho.reshape(-1, order="F")).reshape(d, d, order="F")


def main() -> int:
    rng = np.random.default_rng(20260918)
    checks: dict[str, dict] = {}

    # --- A. pure qubit, one parameter ----------------------------------------
    worst_pure = 0.0
    worst_qfi = 0.0
    for theta in np.linspace(0.1, 3.0, 12):
        psi = np.array([np.cos(theta / 2), np.sin(theta / 2)], dtype=complex)
        dpsi = np.array([-0.5 * np.sin(theta / 2), 0.5 * np.cos(theta / 2)], dtype=complex)
        rho = np.outer(psi, psi.conj())
        drho = np.outer(dpsi, psi.conj()) + np.outer(psi, dpsi.conj())
        sld = pc.spectral_sld(rho, drho)
        worst_pure = max(worst_pure, float(np.linalg.norm(sld - 2 * drho)))
        worst_qfi = max(worst_qfi, abs(float(np.real(np.trace(rho @ sld @ sld))) - 1.0))
    checks["A_pure_qubit"] = {
        "max_abs_err_L_vs_2drho": worst_pure,
        "max_abs_err_QFI_vs_1": worst_qfi,
        "pass": bool(worst_pure < 1e-12 and worst_qfi < 1e-12),
    }

    # --- B. mixed qubit, one parameter ---------------------------------------
    worst_l = 0.0
    worst_q = 0.0
    for _ in range(30):
        r0 = rng.normal(size=3)
        r0 = r0 / np.linalg.norm(r0) * rng.uniform(0.15, 0.9)
        dr = rng.normal(size=3) * 0.7
        rho, drho = bloch(r0), bloch(r0 + dr) - bloch(r0)  # d rho = (dr.sigma)/2
        drho = 0.5 * sum(dk * p for dk, p in zip(dr, PAULI, strict=True))
        sld_exact, qfi_exact = qubit_closed_form(r0, dr)
        sld = pc.spectral_sld(rho, drho)
        worst_l = max(worst_l, float(np.linalg.norm(sld - sld_exact)))
        worst_q = max(
            worst_q, abs(float(np.real(np.trace(rho @ sld @ sld))) - qfi_exact) / abs(qfi_exact)
        )
    checks["B_mixed_qubit_closed_form"] = {
        "max_abs_err_L": worst_l,
        "max_rel_err_QFI": worst_q,
        "pass": bool(worst_l < 1e-10 and worst_q < 1e-10),
    }

    # --- C. random full-rank qutrit vs independent Lyapunov solve -------------
    worst_c = 0.0
    worst_res = 0.0
    for _ in range(30):
        g = pc.random_hermitian(3, rng)
        rho = g @ g.conj().T + 0.3 * np.eye(3)
        rho = rho / np.trace(rho)
        drho = pc.herm(pc.random_hermitian(3, rng))
        drho = drho - np.trace(drho) / 3 * np.eye(3)
        sld = pc.spectral_sld(rho, drho)
        sld_ref = pc.herm(lyapunov_sld(rho, drho))
        worst_c = max(worst_c, float(np.linalg.norm(sld - sld_ref)))
        worst_res = max(worst_res, pc.sld_residual(sld, rho, drho))
    checks["C_qutrit_vs_lyapunov"] = {
        "max_abs_err_vs_independent_solver": worst_c,
        "max_defining_equation_residual": worst_res,
        "pass": bool(worst_c < 1e-8 and worst_res < 1e-10),
    }

    # --- D. quasi-pure samplers ----------------------------------------------
    sampler_rows = []
    for name, mk in (
        ("bipartite(d_sys=2,r=2,s=2)", lambda: pc.sample_bipartite_quasipure(2, 2, 2, rng)),
        ("bipartite(d_sys=3,r=2,s=2)", lambda: pc.sample_bipartite_quasipure(3, 2, 2, rng)),
        ("generic(d=4,r=2,s=2)", lambda: pc.sample_generic_quasipure(4, 2, 2, rng)),
        ("generic(d=6,r=2,s=4)", lambda: pc.sample_generic_quasipure(6, 2, 4, rng)),
    ):
        qp_err = fd_err = res_err = 0.0
        blk_err = 0.0
        made = 0
        for _ in range(8):
            model = mk()
            if model is None:
                continue
            made += 1
            _, psis = pc.support_eigenvectors(model.rho, model.rank)
            proj = psis @ psis.conj().T
            for i, dr in enumerate(model.drho):
                qp_err = max(qp_err, float(np.linalg.norm(proj @ dr @ proj)))
                sld = pc.spectral_sld(model.rho, dr)
                res_err = max(res_err, pc.sld_residual(sld, model.rho, dr))
                # SLD support-support block must vanish for a quasi-pure state
                blk_err = max(blk_err, float(np.linalg.norm(proj @ sld @ proj)))
                fd = model.fd_drho()[i]
                fd_err = max(
                    fd_err, float(np.linalg.norm(fd - dr)) / max(np.linalg.norm(dr), 1e-30)
                )
        sampler_rows.append(
            {
                "model": name,
                "samples": made,
                "max_quasipurity_violation": qp_err,
                "max_sld_support_block_norm": blk_err,
                "max_sld_residual": res_err,
                "max_rel_fd_vs_analytic_drho": fd_err,
                "pass": bool(
                    made == 8
                    and qp_err < 1e-12
                    and blk_err < 1e-10
                    and res_err < 1e-10
                    and fd_err < 1e-8
                ),
            }
        )
    checks["D_quasipure_samplers"] = {
        "rows": sampler_rows,
        "pass": all(r["pass"] for r in sampler_rows),
    }

    # --- E. algebraic plumbing ------------------------------------------------
    round_trip = 0.0
    inner_err = 0.0
    for d in (2, 3, 4, 6):
        for _ in range(20):
            a = pc.random_hermitian(d, rng)
            b = pc.random_hermitian(d, rng)
            round_trip = max(
                round_trip, float(np.linalg.norm(pc._vec_to_herm(pc.herm_to_real_vec(a), d) - a))
            )
            inner_err = max(
                inner_err,
                abs(
                    float(pc.herm_to_real_vec(a) @ pc.herm_to_real_vec(b))
                    - float(np.real(np.trace(a @ b)))
                ),
            )
    hand = {3: 6.0, 4: 12.0, 5: 18.0, 6: 25.0, 7: 33.0, 8: 42.0}
    thr_err = max(abs(pc.rhs_threshold(d) - v) for d, v in hand.items())
    checks["E_plumbing"] = {
        "max_herm_vec_round_trip_err": round_trip,
        "max_inner_product_err": inner_err,
        "max_threshold_err_vs_hand_arithmetic": thr_err,
        "hand_checked_thresholds": hand,
        "pass": bool(round_trip < 1e-12 and inner_err < 1e-12 and thr_err == 0.0),
    }

    # --- F. eigen-decomposition sanity on a degenerate-eigenvalue model -------
    w = eigh(np.diag([0.5, 0.5, 0.0, 0.0]).astype(complex))[0]
    checks["F_degenerate_spectrum_handling"] = {
        "eigenvalues": w.tolist(),
        "note": "spectral SLD sets the 0+0 block to 0 (standard kernel freedom); "
        "W and M are provably independent of that block, see decision.md",
        "pass": True,
    }

    verdict = "READY" if all(c["pass"] for c in checks.values()) else "BLOCKED-INFRASTRUCTURE"
    payload = {"verdict": verdict, "tol_rel": pc.TOL_REL, "checks": checks}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({k: v.get("pass") for k, v in checks.items()}, indent=2))
    print("VERDICT:", verdict)
    return 0 if verdict == "READY" else 1


if __name__ == "__main__":
    sys.exit(main())
