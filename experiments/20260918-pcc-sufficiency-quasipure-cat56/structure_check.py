"""Why the certified test can or cannot fire: structure of V for quasi-pure states.

A null existence search is only informative if you know whether the detector could have
fired at all. For quasi-pure states the answer is a theorem, derived here and then
verified numerically rather than asserted.

Derivation (all four steps are checked numerically below):

  S1  For a quasi-pure state with parameter-independent spectrum, `Pi_r L_i Pi_r = 0`
      (Yang arXiv:2405.00405, Observation 4). Hence `L_i |psi_a>` lies in the kernel.
  S2  Therefore `M_i,ab = [L_i, P_ab]` has NOTHING in the support-support or
      kernel-kernel blocks: it is purely support<->kernel off-block.
  S3  Therefore `W_ij,ab = L_i P_ab L_j - L_j P_ab L_i` is purely kernel-kernel
      (it is `(kernel ket)(kernel bra)`).
  S4  So with `k = d - r`: `V` sits inside `Off (+) Herm(kernel)`, of real dimension
      `2rk + k^2`; and PCC makes the W-part traceless, removing one more dimension.
      Hence `dim V <= 2rk + k^2 - 1` and

          dim V_perp = d^2 - dim V >= (r+k)^2 - 2rk - k^2 + 1 = r^2 + 1.

  S5  Observation 2 fires only when `dim V_perp < d`. Combining with S4, a certified
      counterexample among quasi-pure states REQUIRES

          r^2 + 1 < d.

      In particular at `d = 4, r = 2` (the smallest below-threshold Eq. (16) case, and
      the pre-registered primary configuration) `r^2 + 1 = 5 > 4 = d`: the certified test
      CANNOT fire there, for any state in the class, for a structural reason -- not for
      want of sampling.

The last section sweeps `s` upward at fixed `(d, r)` to see whether `dim V` ever reaches
its structural ceiling `2rk + k^2 - 1`, which is what a certified counterexample would
need at the first arithmetically-allowed size.

Run:  python structure_check.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pcc_core as pc

OUT = Path(__file__).parent / "metrics" / "structure_check.json"


def _blocks(mat: np.ndarray, proj_r: np.ndarray, proj_k: np.ndarray) -> dict[str, float]:
    return {
        "rr": float(np.linalg.norm(proj_r @ mat @ proj_r)),
        "kk": float(np.linalg.norm(proj_k @ mat @ proj_k)),
        "off": float(np.linalg.norm(proj_r @ mat @ proj_k) + np.linalg.norm(proj_k @ mat @ proj_r)),
    }


def block_structure(model: pc.Model) -> dict:
    """Numerically verify S1-S3 for one model."""
    ana = pc.analyse(model)
    _, psis = pc.support_eigenvectors(model.rho, model.rank)
    proj_r = psis @ psis.conj().T
    proj_k = np.eye(model.d) - proj_r
    slds = ana.slds
    # WHY a COMMON scale, not each matrix's own norm: under PCC some W_ij,ab vanish
    # identically (they do at d_sys = 2, where every covariant derivative of a qubit pure
    # state is parallel). Dividing such a matrix by its own norm divides noise by noise
    # and produces a meaningless O(1) "violation" -- the first version of this check did
    # exactly that and reported a spurious failure at d = 4.
    worst = {"sld_rr": 0.0, "M_rr": 0.0, "M_kk": 0.0, "W_off": 0.0, "W_rr": 0.0}
    sld_scale = max(float(np.linalg.norm(lo)) for lo in slds)
    for lo in slds:
        worst["sld_rr"] = max(
            worst["sld_rr"], float(np.linalg.norm(proj_r @ lo @ proj_r)) / sld_scale
        )
    r = model.rank
    ms, ws = [], []
    for a in range(r):
        for b in range(r):
            p_ab = np.outer(psis[:, a], psis[:, b].conj())
            for i in range(model.s):
                ms.append((slds[i] @ p_ab - p_ab @ slds[i], a, b))
                for j in range(i + 1, model.s):
                    ws.append(slds[i] @ p_ab @ slds[j] - slds[j] @ p_ab @ slds[i])
    # WHY an SLD-derived reference scale rather than max||W||: when k = d - r = 1, PCC
    # forces every W to vanish IDENTICALLY (W is rank-<=1 inside a 1-dimensional kernel
    # block and traceless, hence zero). Normalising by max||W|| then divides round-off by
    # round-off and manufactures an O(1) "violation". The first version of this check did
    # exactly that and reported a spurious failure at d=3, r=2.
    m_ref = sld_scale
    w_ref = sld_scale**2
    n_w_vanishing = sum(float(np.linalg.norm(w)) < 1e-10 * w_ref for w in ws)
    for m, _, _ in ms:
        bl = _blocks(m, proj_r, proj_k)
        worst["M_rr"] = max(worst["M_rr"], bl["rr"] / m_ref)
        worst["M_kk"] = max(worst["M_kk"], bl["kk"] / m_ref)
    for w in ws:
        blw = _blocks(w, proj_r, proj_k)
        worst["W_off"] = max(worst["W_off"], blw["off"] / w_ref)
        worst["W_rr"] = max(worst["W_rr"], blw["rr"] / w_ref)
    # Split dim V into its two orthogonal pieces (S2/S3 make the split well defined).
    def _dim(mats: list[np.ndarray], ref: float) -> int:
        """Rank against an ABSOLUTE reference scale.

        WHY not `sv > sv[0] * tol` : this is the third place in this experiment where a
        relative-to-its-own-largest-value threshold inverted on an identically-zero set.
        At k = 1 every W vanishes exactly, so `sv[0]` is round-off and a relative cut
        reports full rank for a set of zero matrices. The reference scale is derived from
        the SLD norms, which never vanish.
        """
        if not mats:
            return 0
        vecs = np.array([pc.herm_to_real_vec(pc.herm(m)) for m in mats])
        sv = np.linalg.svd(vecs, compute_uv=False)
        return int(np.sum(sv > ref * pc.TOL_REL))

    sigmas = pc._sigma_ops(psis)
    m_ops, w_ops = [], []
    for _, _, _, sig in sigmas:
        for i in range(model.s):
            m_ops.append(1j * (sig @ slds[i] - slds[i] @ sig))
            for j in range(i + 1, model.s):
                w_ops.append(1j * (slds[i] @ sig @ slds[j] - slds[j] @ sig @ slds[i]))
    k = ana.d - ana.rank
    dim_m, dim_w = _dim(m_ops, m_ref), _dim(w_ops, w_ref)
    return {
        "label": model.label,
        "d": ana.d,
        "r": ana.rank,
        "s": ana.s,
        "k_kernel_dim": k,
        "dim_V_M": dim_m,
        "dim_V_M_ceiling_2rk": 2 * ana.rank * k,
        "dim_V_W": dim_w,
        "dim_V_W_ceiling_k2_minus_1": max(k * k - 1, 0),
        "split_sums_to_dim_V": bool(dim_m + dim_w == ana.dim_v),
        "block_violations": worst,
        "n_W_matrices": len(ws),
        "n_W_identically_zero": int(n_w_vanishing),
        "dim_V": ana.dim_v,
        "dim_V_perp": ana.dim_v_perp,
        "structural_ceiling_dim_V": 2 * ana.rank * (ana.d - ana.rank) + (ana.d - ana.rank) ** 2 - 1,
        "bound_r2_plus_1": ana.rank**2 + 1,
        "bound_holds": bool(ana.dim_v_perp >= ana.rank**2 + 1),
        "pass": bool(
            max(worst.values()) < 1e-10
            and ana.dim_v_perp >= ana.rank**2 + 1
            and dim_m + dim_w == ana.dim_v
            and dim_m <= 2 * ana.rank * k
            and dim_w <= max(k * k - 1, 0)
        ),
    }


def reparametrisation_invariance(model: pc.Model, rng: np.random.Generator) -> dict:
    """dim V_perp must not depend on the basis or on an ancilla relabelling.

    This is simultaneously the `convention flip` no-collapse test and the second,
    independent reconstruction path any candidate counterexample would have to survive.
    """
    ana0 = pc.analyse(model)
    u = pc.random_unitary(model.d, rng)
    rotated = pc.Model(
        rho=u @ model.rho @ u.conj().T,
        drho=[u @ x @ u.conj().T for x in model.drho],
        gens=[u @ g @ u.conj().T for g in model.gens],
        rank=model.rank,
        label=model.label + "+unitary",
    )
    ana1 = pc.analyse(rotated)
    # Second, coarser path: rescale every generator (the SLDs scale, V does not rotate).
    scaled = pc.Model(
        rho=model.rho,
        drho=[3.7 * x for x in model.drho],
        gens=[3.7 * g for g in model.gens],
        rank=model.rank,
        label=model.label + "+rescaled",
    )
    ana2 = pc.analyse(scaled)
    return {
        "label": model.label,
        "dim_V_perp": [ana0.dim_v_perp, ana1.dim_v_perp, ana2.dim_v_perp],
        "pcc_violations": [ana0.pcc_violation, ana1.pcc_violation, ana2.pcc_violation],
        "invariant": bool(ana0.dim_v_perp == ana1.dim_v_perp == ana2.dim_v_perp),
        "pass": bool(ana0.dim_v_perp == ana1.dim_v_perp == ana2.dim_v_perp),
    }


def high_precision_rank(model: pc.Model, dps: int = 40) -> dict:
    """Recompute dim V with mpmath at `dps` digits -- an independent numerical route."""
    import mpmath as mp

    ana = pc.analyse(model)
    _, psis = pc.support_eigenvectors(model.rho, model.rank)
    sigmas = pc._sigma_ops(psis)
    mats = []
    for _, _, _, sig in sigmas:
        for i in range(model.s):
            mats.append(1j * (sig @ ana.slds[i] - ana.slds[i] @ sig))
        for i in range(model.s):
            for j in range(i + 1, model.s):
                mats.append(
                    1j * (ana.slds[i] @ sig @ ana.slds[j] - ana.slds[j] @ sig @ ana.slds[i])
                )
    vecs = np.array([pc.herm_to_real_vec(pc.herm(m)) for m in mats])
    with mp.workdps(dps):
        mat = mp.matrix(vecs.tolist())
        sv = mp.svd_r(mat, compute_uv=False)
        vals = [float(sv[i]) for i in range(len(sv))]
    top = max(vals)
    # WHY thresholds stop at 1e-12: the INPUT is float64, so the numerically-zero
    # singular values sit at ~1e-16 relative. mpmath cannot recover precision the input
    # never had; asking for rank at 1e-20 counts float64 round-off as signal. That is a
    # property of the input, not of the rank, and is stated rather than hidden -- the
    # first version of this check used 1e-14/1e-20 and "failed" for exactly that reason.
    thresholds = (1e-4, 1e-6, 1e-8, 1e-10, 1e-12)
    ranks = {f"{t:.0e}": int(sum(v > top * t for v in vals)) for t in thresholds}
    srt = sorted(vals, reverse=True)
    below = srt[ana.dim_v] if ana.dim_v < len(srt) else 0.0
    return {
        "label": model.label,
        "dps": dps,
        "float64_dim_V": ana.dim_v,
        "mpmath_rank_at_thresholds": ranks,
        "last_kept_singular_value_rel": float(srt[ana.dim_v - 1] / top) if ana.dim_v else None,
        "first_dropped_singular_value_rel": float(below / top),
        "float64_input_noise_floor_rel": 1e-15,
        "agrees": bool(all(v == ana.dim_v for v in ranks.values())),
        "pass": bool(all(v == ana.dim_v for v in ranks.values())),
    }


def ceiling_sweep(rng: np.random.Generator) -> list[dict]:
    """Does dim V ever reach its structural ceiling 2rk + k^2 - 1?

    That is what a certified counterexample needs at the first size where `r^2 + 1 < d`.
    """
    rows = []
    for d, r in ((6, 2), (7, 2), (8, 2), (6, 1), (8, 3)):
        k = d - r
        ceiling = 2 * r * k + k * k - 1
        need = d * d - d + 1  # dim V needed for dim V_perp < d
        for s in (2, 3, 4, 5, 6, 8):
            best, got = 0, 0
            for _ in range(8):
                m = pc.sample_generic_quasipure(d, r, s, rng)
                if m is None:
                    continue
                got += 1
                best = max(best, pc.analyse(m).dim_v)
            rows.append(
                {
                    "d": d,
                    "r": r,
                    "s": s,
                    "samples": got,
                    "max_dim_V_seen": best,
                    "structural_ceiling": ceiling,
                    "dim_V_needed_for_certified": need,
                    "ceiling_below_need": bool(ceiling < need),
                    "reached_ceiling": bool(best == ceiling),
                    "certified_possible_arithmetically": bool(r * r + 1 < d),
                }
            )
    return rows


def main() -> None:
    rng = np.random.default_rng(560_918)
    models = []
    for mk in (
        lambda: pc.sample_bipartite_quasipure(2, 2, 2, rng),
        lambda: pc.sample_bipartite_quasipure(3, 2, 2, rng),
        lambda: pc.sample_bipartite_quasipure(4, 2, 2, rng),
        lambda: pc.sample_generic_quasipure(3, 2, 2, rng),
        lambda: pc.sample_generic_quasipure(4, 2, 2, rng),
        lambda: pc.sample_generic_quasipure(6, 2, 4, rng),
        lambda: pc.sample_generic_quasipure(7, 3, 3, rng),
    ):
        for _ in range(3):
            m = mk()
            if m is not None:
                models.append(m)

    # Derived, then verified: for a GENERIC quasi-pure state with k = d - r = 1, the a != b
    # part of PCC forces all the ratios c_a to coincide, collapsing the QFIM to rank 1.
    # The Eq. (16) bipartite class does NOT suffer this, because its a != b conditions are
    # automatically satisfied by the ancilla block structure and impose nothing.
    k1_rows = []
    for d, r, s in ((3, 2, 2), (4, 3, 2), (3, 2, 3), (5, 4, 2)):
        gen_ranks, bip_ranks = [], []
        for _ in range(25):
            m = pc.sample_generic_quasipure(d, r, s, rng)
            if m is not None:
                gen_ranks.append(pc.analyse(m).qfim_rank)
        for _ in range(25):
            m = pc.sample_bipartite_quasipure(2, r, s, rng)  # k per sector = 1 as well
            if m is not None:
                bip_ranks.append(pc.analyse(m).qfim_rank)
        k1_rows.append(
            {
                "d": d,
                "r": r,
                "s": s,
                "kernel_dim_k": d - r,
                "generic_qfim_ranks": sorted(set(gen_ranks)),
                "bipartite_dsys2_qfim_ranks": sorted(set(bip_ranks)),
                "generic_collapses_to_rank1": bool(gen_ranks and set(gen_ranks) == {1}),
            }
        )

    blocks = [block_structure(m) for m in models]
    invar = [reparametrisation_invariance(m, rng) for m in models]
    # Cover every model FAMILY, not just the first few of one family, so the
    # 'how small is small' evidence spans both classes and all tested sizes.
    seen: set[str] = set()
    hiprec = []
    for m in models:
        if m.label in seen:
            continue
        seen.add(m.label)
        hiprec.append(high_precision_rank(m))
    sweep = ceiling_sweep(rng)

    payload = {
        "block_structure": {"rows": blocks, "pass": all(b["pass"] for b in blocks)},
        "reparametrisation_invariance": {
            "rows": invar,
            "pass": all(i["pass"] for i in invar),
        },
        "high_precision_rank": {"rows": hiprec, "pass": all(h["pass"] for h in hiprec)},
        "ceiling_sweep": sweep,
        "qfim_degeneracy_at_k1": {
            "rows": k1_rows,
            "claim": "generic quasi-pure + PCC + (d - r) = 1  =>  QFIM has rank 1, i.e. the "
            "multiparameter problem degenerates; the Eq. (16) bipartite class does not, "
            "because its a != b PCC conditions are vacuous",
        },
        "conclusion": {
            "bound": "dim V_perp >= r^2 + 1 for every quasi-pure state satisfying PCC",
            "certified_counterexample_requires": "r^2 + 1 < d",
            "preregistered_primary_config": "d=4, r=2 -> r^2+1 = 5 > 4 = d, so the "
            "certified test cannot fire there for ANY state in the class",
        },
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("block_structure   pass:", payload["block_structure"]["pass"])
    print("QFIM at k=1 (generic vs bipartite d_sys=2):")
    for row in k1_rows:
        print(
            f"  d={row['d']} r={row['r']} s={row['s']} k={row['kernel_dim_k']}: "
            f"generic QFIM ranks {row['generic_qfim_ranks']}, "
            f"bipartite(d_sys=2) QFIM ranks {row['bipartite_dsys2_qfim_ranks']}"
        )
    print("reparam_invariance pass:", payload["reparametrisation_invariance"]["pass"])
    print("high_precision     pass:", payload["high_precision_rank"]["pass"])
    print("\nmax block violation:", max(max(b["block_violations"].values()) for b in blocks))
    print(
        "min (dim V_perp - (r^2+1)):", min(b["dim_V_perp"] - b["bound_r2_plus_1"] for b in blocks)
    )
    print("\nceiling sweep (max dim V seen vs structural ceiling vs need):")
    for row in sweep:
        mark = "  <-- REACHES CEILING" if row["reached_ceiling"] else ""
        print(
            f"  d={row['d']} r={row['r']} s={row['s']}: "
            f"dimV<={row['max_dim_V_seen']:3d}  ceiling={row['structural_ceiling']:3d}  "
            f"need>={row['dim_V_needed_for_certified']:3d}  "
            f"possible={row['certified_possible_arithmetically']}{mark}"
        )


if __name__ == "__main__":
    main()
