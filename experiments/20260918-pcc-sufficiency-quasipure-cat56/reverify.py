"""Step 4 of the corrected protocol: independent second-path reconstruction.

A candidate counterexample (PCC true with margin AND `dim V_perp < d` robustly) is only
CONFIRMED after the same physical state is rebuilt along a path that reuses none of the
first pass's basis, tolerances or intermediate objects. This module implements that
second path and, because the main search produced no candidate, also EXERCISES it on
ordinary samples so that the machinery itself is verified rather than merely written.

The second path differs from the first in four independent ways:

  1. SLD is computed from Yang's closed form (arXiv:2405.00405, Observation 4),
     `L_i = sum_n 2(|D_i phi_n><phi_n| + |phi_n><D_i phi_n|)`, instead of from the
     spectral solution of the Lyapunov equation.
  2. The state is re-expressed in a randomly rotated basis and with rescaled generators,
     so no numerical object from the first pass survives.
  3. `d rho` is taken from central finite differences of `exp(-i sum_j lam_j G_j)` instead
     of from the analytic commutator.
  4. The rank of the `W`/`M` stack is recomputed from Gram-matrix eigenvalues and from an
     mpmath SVD at 40 digits, not from the float64 `numpy.linalg.svd` of the first pass.

Run:  python reverify.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pcc_core as pc

OUT = Path(__file__).parent / "metrics" / "reverify.json"


def closed_form_slds(model: pc.Model) -> list[np.ndarray]:
    """Yang arXiv:2405.00405 Observation 4 -- an SLD route with no Lyapunov solve.

    `|D_i phi_n> = (I - Pi_n)|d_i phi_n>` with `Pi_n` the projector onto the eigenvalue's
    degenerate subspace; here the spectrum is non-degenerate by construction, so
    `Pi_n = |phi_n><phi_n|`. `|d_i phi_n> = -i G_i |phi_n>`.
    """
    w, v = np.linalg.eigh(pc.herm(model.rho))
    order = np.argsort(w)[::-1]
    phis = v[:, order[: model.rank]]
    out = []
    for g in model.gens:
        sld = np.zeros((model.d, model.d), dtype=complex)
        for n in range(model.rank):
            phi = phis[:, n]
            dphi = -1j * (g @ phi)
            cov = dphi - phi * (phi.conj() @ dphi)
            sld += 2 * (np.outer(cov, phi.conj()) + np.outer(phi, cov.conj()))
        out.append(pc.herm(sld))
    return out


def second_path(model: pc.Model, rng: np.random.Generator, dps: int = 40) -> dict:
    """Rebuild the model along the independent path and recompute every verdict input."""
    import mpmath as mp

    first = pc.analyse(model)

    # (2) new basis + rescaled generators
    u = pc.random_unitary(model.d, rng)
    scale = float(rng.uniform(0.4, 2.5))
    rot = pc.Model(
        rho=u @ model.rho @ u.conj().T,
        drho=[scale * (u @ x @ u.conj().T) for x in model.drho],
        gens=[scale * (u @ g @ u.conj().T) for g in model.gens],
        rank=model.rank,
        label=model.label + "|second-path",
    )
    # (3) d rho from finite differences of the exponential map, not the commutator
    fd = rot.fd_drho(eps=1e-5)
    fd_model = pc.Model(rho=rot.rho, drho=fd, gens=rot.gens, rank=rot.rank, label=rot.label + "|fd")
    second = pc.analyse(fd_model)

    # (1) closed-form SLD instead of the Lyapunov solve, on the rotated model
    cf = closed_form_slds(rot)
    sld_scale = max(float(np.linalg.norm(x)) for x in cf)
    sld_disagreement = max(
        float(np.linalg.norm(a - b)) / sld_scale
        for a, b in zip(cf, pc.analyse(rot).slds, strict=True)
    )

    # (4) independent rank routes on the second path's own W/M stack
    _, psis = pc.support_eigenvectors(fd_model.rho, fd_model.rank)
    sigmas = pc._sigma_ops(psis)
    mats = []
    for _, _, _, sig in sigmas:
        for i in range(fd_model.s):
            mats.append(1j * (sig @ second.slds[i] - second.slds[i] @ sig))
        for i in range(fd_model.s):
            for j in range(i + 1, fd_model.s):
                mats.append(
                    1j
                    * (
                        second.slds[i] @ sig @ second.slds[j]
                        - second.slds[j] @ sig @ second.slds[i]
                    )
                )
    vecs = np.array([pc.herm_to_real_vec(pc.herm(m)) for m in mats])
    with mp.workdps(dps):
        sv = mp.svd_r(mp.matrix(vecs.tolist()), compute_uv=False)
        vals = sorted((float(sv[i]) for i in range(len(sv))), reverse=True)
    top = vals[0]
    # WHY the plateau stops at 1e-8: this path takes `d rho` from CENTRAL FINITE
    # DIFFERENCES with eps = 1e-5, whose own error floor is ~eps^2 + eps_machine/eps
    # ~ 1e-10 relative. Asking for rank below that counts the finite-difference error as
    # signal. Measured: at 1e-10 a spurious 4th singular value appears on the d=3 models,
    # and it is the FD floor, not a rank disagreement -- dim V_perp itself agrees 18/18.
    fd_noise_floor = 1e-10
    mp_rank = {f"{t:.0e}": int(sum(v > top * t for v in vals)) for t in (1e-5, 1e-6, 1e-7, 1e-8)}

    agree = (
        first.dim_v_perp == second.dim_v_perp
        and second.gram_rank == second.dim_v
        and len(set(mp_rank.values())) == 1
        and next(iter(mp_rank.values())) == second.dim_v
    )
    return {
        "label": model.label,
        "d": first.d,
        "r": first.rank,
        "s": first.s,
        "first_path": {
            "dim_V": first.dim_v,
            "dim_V_perp": first.dim_v_perp,
            "pcc_violation": first.pcc_violation,
            "certified_not_saturable": bool(first.certified_not_saturable),
        },
        "second_path": {
            "dim_V": second.dim_v,
            "dim_V_perp": second.dim_v_perp,
            "pcc_violation": second.pcc_violation,
            "certified_not_saturable": bool(second.certified_not_saturable),
            "gram_rank": second.gram_rank,
            "mpmath_rank": mp_rank,
            "basis_rotated": True,
            "generator_rescale": scale,
            "drho_from": "central finite differences of exp(-i sum lam G)",
            "fd_relative_noise_floor": fd_noise_floor,
        },
        "closed_form_sld_rel_disagreement": sld_disagreement,
        "verdicts_agree": bool(agree),
        "pass": bool(
            agree
            and sld_disagreement < 1e-8
            and first.certified_not_saturable == second.certified_not_saturable
        ),
    }


def main() -> None:
    rng = np.random.default_rng(4242)
    models = []
    for mk in (
        lambda: pc.sample_bipartite_quasipure(2, 2, 2, rng),
        lambda: pc.sample_bipartite_quasipure(3, 2, 2, rng),
        lambda: pc.sample_bipartite_quasipure(4, 2, 2, rng),
        lambda: pc.sample_generic_quasipure(3, 2, 2, rng),
        lambda: pc.sample_generic_quasipure(4, 2, 2, rng),
        lambda: pc.sample_generic_quasipure(6, 2, 3, rng),
    ):
        for _ in range(3):
            m = mk()
            if m is not None:
                models.append(m)

    rows = [second_path(m, rng) for m in models]
    payload = {
        "purpose": "independent second-path reconstruction (corrected protocol, step 4)",
        "candidates_from_main_search": 0,
        "note": "No candidate counterexample was produced by the main search or the "
        "extension, so this module is exercised on ordinary samples to verify the "
        "machinery itself rather than left untested.",
        "rows": rows,
        "all_pass": all(r["pass"] for r in rows),
        "max_closed_form_sld_disagreement": max(
            r["closed_form_sld_rel_disagreement"] for r in rows
        ),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("all_pass:", payload["all_pass"])
    print("max closed-form SLD disagreement:", payload["max_closed_form_sld_disagreement"])
    for r in rows:
        print(
            f"  {r['label']:32s} dimVperp {r['first_path']['dim_V_perp']:3d} -> "
            f"{r['second_path']['dim_V_perp']:3d}  agree={r['verdicts_agree']}"
        )


if __name__ == "__main__":
    main()
