"""Verify the pilot-firing states (claim C-EX): reduced pipeline + tolerance sweep + Gram route,
independent nullspace identity, full d x d pipeline of H-CAT56-1. Single process."""

from __future__ import annotations

import json
import time
from pathlib import Path

import caps
import h2_core as h
import h2_ext as x
import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "metrics"
CANDS = HERE / "candidates"


def reduced_report(blocks: list[np.ndarray]) -> dict:
    k, r = blocks[0].shape
    d = k + r
    plateau = {}
    for tol in (1e-5, 1e-6, 1e-8, 1e-10, 1e-12):
        rk = h.ranks(blocks, tol=tol)
        plateau[f"{tol:.0e}"] = [rk["M"]["dim"], rk["W"]["dim"]]
    rk = h.ranks(blocks)
    sm, sw = h.stacks(blocks)
    nrm2 = sum(float(np.linalg.norm(b) ** 2) for b in blocks)
    gm = np.linalg.eigvalsh(sm @ sm.T)
    gw = np.linalg.eigvalsh(sw @ sw.T)
    # WHY 1e-12 * top eigenvalue: Gram eigenvalues are squared singular values, so a cut of
    # (1e-9*scale)^2 = 1e-18 lies below the float64 eigenvalue noise floor (~1e-16 * top). The
    # first run of this script used that cut and disagreed with the SVD rank purely from
    # round-off (same defect family as H-CAT56-1 defect 3); nrm2 kept only for the record.
    _ = nrm2
    gram = [int(np.sum(gm > 1e-12 * gm.max())), int(np.sum(gw > 1e-12 * gw.max()))]
    dp, dq = x.dim_p(blocks), x.dim_q(blocks)
    dv = rk["dim_v"]
    s = len(blocks)
    return {
        "d": d,
        "r": r,
        "k": k,
        "s": s,
        "pcc_violation_rel": h.pcc_violation(blocks),
        "dim_M": rk["M"]["dim"],
        "dim_W": rk["W"]["dim"],
        "dim_V": dv,
        "dim_Vperp": d * d - dv,
        "fires": bool(d * d - dv < d),
        "plateau_M_W": plateau,
        "plateau_flat": bool(len({tuple(v) for v in plateau.values()}) == 1),
        "gram_dims_M_W": gram,
        "gram_agrees": bool(gram == [rk["M"]["dim"], rk["W"]["dim"]]),
        "gap_M": rk["M"]["gap"],
        "gap_W": rk["W"]["gap"],
        "dim_P": dp,
        "dim_Q": dq,
        "identity_rhs": r * r + dp + dq,
        "identity_holds": bool(d * d - dv == r * r + dp + dq),
        "LB": x.lb(k, r, s),
        "vperp_ge_LB": bool(d * d - dv >= x.lb(k, r, s)),
        "qfim_rank": h.qfim_rank(blocks, np.ones(r) / r),
    }


def full_pipeline(blocks: list[np.ndarray], seed: int) -> dict:
    pc = h.load_old("pcc_core")
    r = blocks[0].shape[1]
    rng = np.random.default_rng(seed)
    q = rng.uniform(0.2, 1.0, size=r)
    q = q / q.sum()
    runs = []
    for rot in (False, True):
        model = x.to_model(blocks, q, np.random.default_rng(seed + 1) if rot else None)
        a = pc.analyse(model)
        runs.append(
            {
                "rotated_basis": rot,
                "dim_V": a.dim_v,
                "dim_Vperp": a.dim_v_perp,
                "pcc_holds": bool(a.pcc_holds),
                "pcc_violation": a.pcc_violation,
                "sld_residual": a.sld_residual,
                "qfim_rank": a.qfim_rank,
                "rank_plateau": a.rank_plateau,
                "gram_rank": a.gram_rank,
                "rank_gap_ratio": a.rank_gap_ratio,
                "rank_is_robust": bool(a.rank_is_robust),
                "certified_not_saturable": bool(a.certified_not_saturable),
            }
        )
    return {"q": q.tolist(), "runs": runs}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    CANDS.mkdir(exist_ok=True)
    rows = []
    for d, r, s, seed in ((22, 2, 16, 20260919), (23, 3, 12, 20260919)):
        k = d - r
        t0 = time.time()
        res = h.sample_sequential(k, r, s, np.random.default_rng(seed))
        assert res is not None
        blocks, nulls = res
        rep = reduced_report(blocks)
        rep["nullspace_dims"] = nulls
        rep["seed"] = seed
        rep["full_pipeline"] = full_pipeline(blocks, seed)
        rep["seconds"] = time.time() - t0
        np.savez(
            CANDS / f"cand_d{d}_r{r}_s{s}_seed{seed}.npz",
            **{f"A{i}": b for i, b in enumerate(blocks)},
        )
        rows.append(rep)
        fp = rep["full_pipeline"]["runs"]
        print(
            f"d={d} r={r} s={s}: reduced Vperp={rep['dim_Vperp']} fires={rep['fires']} "
            f"flat={rep['plateau_flat']} gram={rep['gram_agrees']} id={rep['identity_holds']} "
            f"(P={rep['dim_P']},Q={rep['dim_Q']}) LB={rep['LB']} | full dimV="
            f"{[y['dim_V'] for y in fp]} robust={[y['rank_is_robust'] for y in fp]} "
            f"pcc={[y['pcc_holds'] for y in fp]} cert={[y['certified_not_saturable'] for y in fp]} "
            f"qfimrank={[y['qfim_rank'] for y in fp]} sec={rep['seconds']:.1f}",
            flush=True,
        )
    payload = {"rows": rows, "resources": caps.state()}
    tmp = OUT / "verify_candidate.json.tmp"
    tmp.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    tmp.replace(OUT / "verify_candidate.json")
    print("resources:", caps.state())


if __name__ == "__main__":
    main()
