"""H-CAT56-2 main runs. Single process per invocation (resource caps): `python h2_main.py MODE`.

MODE in: random | structured | extended | adaptive | controls | theory
Every mode writes metrics/<mode>.json atomically (tmp + replace)."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import caps
import h2_core as h
import h2_ext as x
import numpy as np
from scipy.optimize import minimize

HERE = Path(__file__).parent
OUT = HERE / "metrics"

REQUIRED = [(6, 2, 4), (7, 2, 4), (8, 2, 5), (10, 3, 5), (11, 3, 5)]
EXTENDED = [
    (22, 2, 16),
    (23, 2, 17),
    (24, 2, 18),
    (23, 3, 12),
    (24, 3, 13),
    (22, 2, 4),
    (22, 2, 10),
]


def save(name: str, payload: dict) -> None:
    OUT.mkdir(exist_ok=True)
    payload["resources"] = caps.state()
    tmp = OUT / f"{name}.json.tmp"
    tmp.write_text(json.dumps(payload, indent=1, default=float), encoding="utf-8")
    tmp.replace(OUT / f"{name}.json")


def robust_rank(blocks: list[np.ndarray]) -> tuple[int, bool]:
    """(dim V, robust?) with the pre-registered tolerance sweep and a gap requirement."""
    dims = set()
    for tol in (1e-5, 1e-6, 1e-8, 1e-10, 1e-12):
        dims.add(h.ranks(blocks, tol=tol)["dim_v"])
    rk = h.ranks(blocks)
    gaps_ok = all((rk[t]["gap"] is None or rk[t]["gap"] > 1e4) for t in ("M", "W"))
    return rk["dim_v"], bool(len(dims) == 1 and gaps_ok)


def one_sample(blocks: list[np.ndarray], d: int, r: int, k: int, s: int) -> dict:
    dv, robust = robust_rank(blocks)
    vperp = d * d - dv
    return {
        "dim_V": dv,
        "dim_Vperp": vperp,
        "robust": robust,
        "fires": bool(vperp < d),
        "pcc_ok": bool(h.pcc_violation(blocks) < 1e-9),
        "qfim_full": bool(h.qfim_rank(blocks, np.ones(r) / r) == s),
        "LB": x.lb(k, r, s),
        "below_LB": bool(vperp < x.lb(k, r, s)),
    }


def summarise(rows: list[dict], d: int, r: int, s: int) -> dict:
    return {
        "d": d,
        "r": r,
        "k": d - r,
        "s": s,
        "n": len(rows),
        "need_dimV": d * d - d + 1,
        "pcc_ok": sum(q["pcc_ok"] for q in rows),
        "qfim_full": sum(q["qfim_full"] for q in rows),
        "robust": sum(q["robust"] for q in rows),
        "max_dimV": max(q["dim_V"] for q in rows),
        "min_dimVperp": min(q["dim_Vperp"] for q in rows),
        "LB": rows[0]["LB"],
        "n_fires_robust_pcc_qfim": sum(
            q["fires"] and q["robust"] and q["pcc_ok"] and q["qfim_full"] for q in rows
        ),
        "n_below_LB": sum(q["below_LB"] for q in rows),
        "distinct_dimV": sorted({q["dim_V"] for q in rows}),
        "r2_plus_s_plus_1": r * r + s + 1,
    }


def run_random(cfgs, n: int, seed: int, name: str) -> None:
    t0 = time.time()
    out = []
    for d, r, s in cfgs:
        k = d - r
        rng = np.random.default_rng(seed + 1000 * d + 10 * r + s)
        rows = []
        for _ in range(n):
            res = h.sample_sequential(k, r, s, rng)
            if res is None:
                continue
            rows.append(one_sample(res[0], d, r, k, s))
        out.append(summarise(rows, d, r, s))
        print(out[-1], flush=True)
    save(name, {"n_per_config": n, "seed": seed, "configs": out, "seconds": time.time() - t0})


def structured_first(kind: str, k: int, r: int, rng: np.random.Generator) -> np.ndarray:
    g = rng.normal(size=(k, r)) + 1j * rng.normal(size=(k, r))
    if kind == "rank1":
        return np.outer(g[:, 0], g[0, :])
    if kind == "real":
        return g.real.astype(complex)
    if kind == "sparse":
        m = np.zeros((k, r), dtype=complex)
        for a in range(r):
            m[a % k, a] = 1.0 + 0.3j
            m[(a + 1) % k, a] += 0.5
        return m
    if kind == "blockdiag":  # Eq.(16)-like: columns supported on disjoint row groups
        m = np.zeros((k, r), dtype=complex)
        rows = np.array_split(np.arange(k), r)
        for a, idx in enumerate(rows):
            m[idx, a] = g[idx, a]
        return m
    raise ValueError(kind)


def run_structured(n: int, seed: int) -> None:
    t0 = time.time()
    out = []
    for d, r, s in REQUIRED:
        k = d - r
        for kind in ("rank1", "real", "sparse", "blockdiag"):
            rng = np.random.default_rng(seed + 100 * d + len(kind))
            rows, qdeg, none = [], 0, 0
            best_s = 0
            for _ in range(n):
                first = structured_first(kind, k, r, rng)
                # structured starts may allow MORE parameters: probe the largest non-degenerate s
                for ss in (s, s + 2, s + 4):
                    res = h.sample_sequential(k, r, ss, rng, first=first)
                    if res is None:
                        none += 1
                        continue
                    blocks = res[0]
                    rq = h.qfim_rank(blocks, np.ones(r) / r)
                    best_s = max(best_s, rq)
                    if rq < ss:
                        qdeg += 1
                        continue
                    rows.append(one_sample(blocks, d, r, k, ss) | {"s": ss})
            out.append(
                {
                    "d": d,
                    "r": r,
                    "k": k,
                    "start": kind,
                    "s_registered": s,
                    "samples_full_qfim": len(rows),
                    "qfim_degenerate_or_none": qdeg + none,
                    "max_qfim_rank_reached": best_s,
                    "max_dimV": max((q["dim_V"] for q in rows), default=None),
                    "min_dimVperp": min((q["dim_Vperp"] for q in rows), default=None),
                    "min_margin_vs_LB": min((q["dim_Vperp"] - q["LB"] for q in rows), default=None),
                    "n_below_LB": sum(q["below_LB"] for q in rows),
                    "n_fires_robust": sum(q["fires"] and q["robust"] and q["pcc_ok"] for q in rows),
                    "need_dimV": d * d - d + 1,
                }
            )
            print(out[-1], flush=True)
    save("structured", {"n": n, "seed": seed, "rows": out, "seconds": time.time() - t0})


def run_adaptive(seed: int) -> None:
    """S-C: SLSQP maximising a smooth surrogate of dim V subject to PCC (equality constraints)."""
    t0 = time.time()
    out = []
    plan = [((6, 2, 4), 4), ((7, 2, 4), 4), ((8, 2, 5), 3), ((10, 3, 5), 2), ((11, 3, 5), 2)]
    for (d, r, s), restarts in plan:
        k = d - r
        n1 = 2 * k * r

        def unpack(v: np.ndarray, k=k, r=r, s=s, n1=n1) -> list[np.ndarray]:
            return [
                (v[i * n1 : i * n1 + k * r] + 1j * v[i * n1 + k * r : (i + 1) * n1]).reshape(k, r)
                for i in range(s)
            ]

        def pcc_res(v: np.ndarray, s=s) -> np.ndarray:
            bl = unpack(v)
            o = []
            for i in range(s):
                for j in range(i + 1, s):
                    m = bl[i].conj().T @ bl[j]
                    dd = m - m.conj().T
                    o += list(dd.real.ravel()) + list(dd.imag.ravel())
            return np.array(o)

        def obj(v: np.ndarray, k=k, r=r, s=s) -> float:
            bl = unpack(v)
            nrm = float(np.sqrt(sum(np.linalg.norm(b) ** 2 for b in bl)))
            sm, sw = h.stacks(bl)
            tm = min(2 * k * r - s, sm.shape[0])
            tw = min(k * k - 1, sw.shape[0])
            svm = np.linalg.svd(sm, compute_uv=False)
            svw = np.linalg.svd(sw, compute_uv=False)
            # v2 (post-registration): sum of the top-T singular values. v1 used the T-th one alone,
            # which is exactly 0 with zero gradient whenever rank < T, so SLSQP never moved
            # (start value == end value in every run of adaptive_v1_inert_surrogate.json).
            return -(float(svm[:tm].sum()) / nrm + float(svw[:tw].sum()) / nrm**2)

        rng = np.random.default_rng(seed + d)
        rows = []
        for rs in range(restarts):
            # start from a PCC point (sequential sampler; structured on odd restarts)
            first = structured_first("blockdiag", k, r, rng) if rs % 2 else None
            res = h.sample_sequential(k, r, s, rng, first=first)
            if res is None:
                continue
            v0 = np.concatenate([np.concatenate([b.real.ravel(), b.imag.ravel()]) for b in res[0]])
            v0 = v0 / np.linalg.norm(v0) * np.sqrt(s * r)
            sol = minimize(
                obj,
                v0,
                # v3 (post-registration): SLSQP aborts at iteration 1 with "Singular matrix C in
                # LSQ subproblem" (redundant PCC constraint rows); trust-constr copes.
                method="trust-constr",
                constraints=[
                    {"type": "eq", "fun": pcc_res},
                    {"type": "eq", "fun": lambda v, t=s * r: float(v @ v - t)},
                ],
                options={"maxiter": 120},
            )
            bl = unpack(sol.x)
            q = one_sample(bl, d, r, k, s)
            q["start_value"] = float(-obj(v0))
            q["end_value"] = float(-sol.fun)
            q["converged"] = bool(sol.success)
            q["pcc_after"] = float(h.pcc_violation(bl))
            rows.append(q)
        row = {
            "d": d,
            "r": r,
            "k": k,
            "s": s,
            "restarts": restarts,
            "runs": len(rows),
            "max_dimV": max((q["dim_V"] for q in rows), default=None),
            "min_dimVperp": min((q["dim_Vperp"] for q in rows), default=None),
            "LB": x.lb(k, r, s),
            "need_dimV": d * d - d + 1,
            "n_valid_pcc_qfim_robust": sum(
                q["pcc_ok"] and q["qfim_full"] and q["robust"] for q in rows
            ),
            "n_below_LB_valid": sum(
                q["below_LB"] and q["pcc_ok"] and q["qfim_full"] and q["robust"] for q in rows
            ),
            "n_fires_valid": sum(
                q["fires"] and q["pcc_ok"] and q["qfim_full"] and q["robust"] for q in rows
            ),
            "surrogate_start_end": [
                (round(q["start_value"], 4), round(q["end_value"], 4)) for q in rows
            ],
            "pcc_after_max": max((q["pcc_after"] for q in rows), default=None),
        }
        out.append(row)
        print(row, flush=True)
    save("adaptive", {"seed": seed, "rows": out, "seconds": time.time() - t0})


def run_theory(seed: int) -> None:
    """C-ID (identity) and C-LB (bound) on many small/medium configs and every s."""
    t0 = time.time()
    rng = np.random.default_rng(seed)
    n_id_fail = n_lb_fail = total = 0
    worst = []
    for r in (2, 3):
        for k in range(2, 13 if r == 2 else 10):
            for s in range(2, 12):
                for _ in range(3):
                    res = h.sample_sequential(k, r, s, rng)
                    if res is None:
                        break
                    bl = res[0]
                    if h.qfim_rank(bl, np.ones(r) / r) < s:
                        break
                    d = k + r
                    dv, robust = robust_rank(bl)
                    if not robust:
                        continue
                    total += 1
                    vperp = d * d - dv
                    idr = r * r + x.dim_p(bl) + x.dim_q(bl)
                    if vperp != idr:
                        n_id_fail += 1
                        worst.append(("id", d, r, s, vperp, idr))
                    if vperp < x.lb(k, r, s):
                        n_lb_fail += 1
                        worst.append(("lb", d, r, s, vperp, x.lb(k, r, s)))
    first = {}
    for r in (2, 3, 4, 5):
        for k in range(2, 200):
            d = r + k
            if min(x.lb(k, r, s) for s in range(2, 2 * k * r + 1)) < d:
                first[r] = d
                break
    save(
        "theory",
        {
            "samples_checked": total,
            "identity_failures": n_id_fail,
            "lb_failures": n_lb_fail,
            "failures": worst,
            "first_d_where_min_s_LB_lt_d": first,
            "seconds": time.time() - t0,
        },
    )
    print("theory:", total, n_id_fail, n_lb_fail, first)


def run_controls(seed: int) -> None:
    t0 = time.time()
    pc = h.load_old("pcc_core")
    rng = np.random.default_rng(seed)
    res: dict = {}
    # (1) rank-detector injection. Certificate fires iff dim V_perp = d^2 - rank < d, i.e.
    # rank >= d^2 - d + 1. Control: rank exactly d^2-d+1 MUST fire, rank d^2-d MUST NOT.
    det = []
    for d in (4, 6, 8, 12, 22):
        fire_hi, fire_lo = 0, 0
        for _ in range(40):
            for tgt, tag in ((d * d - d + 1, "hi"), (d * d - d, "lo")):
                basis = rng.normal(size=(tgt, d * d))
                extra = rng.normal(size=(30, tgt)) @ basis
                sv = np.linalg.svd(np.vstack([basis, extra]), compute_uv=False)
                dim = int(np.sum(sv > 1e-9 * sv[0]))
                fired = (d * d - dim) < d
                if tag == "hi":
                    fire_hi += fired
                else:
                    fire_lo += fired
        det.append({"d": d, "fires_at_rank_d2-d+1": fire_hi, "fires_at_rank_d2-d": fire_lo})
    res["rank_detector_float"] = det
    import exact_certify as ec

    p = ec.prime_1mod4(2**31 - 1)
    rr = np.random.default_rng(seed + 1)
    exact = []
    for tgt in (31, 30):  # d = 6: need rank >= 31
        base = [[int(v) for v in rr.integers(-5, 6, size=36)] for _ in range(tgt)]
        extra = []
        for _ in range(20):
            co = [int(c) for c in rr.integers(-2, 3, size=tgt)]
            extra.append([sum(c * b[j] for c, b in zip(co, base, strict=True)) for j in range(36)])
        rows = base + extra
        rk = ec.rank_mod_p(rows, [[0] * 36 for _ in rows], p)
        exact.append({"injected_rank": tgt, "rank_mod_p": rk, "d": 6, "fires": bool(36 - rk < 6)})
    res["rank_detector_exact_fp"] = exact
    # (2) negative control: Eq.(16) class, theorem-saturable, must never fire
    eq = []
    for d_sys, rank, s in ((4, 2, 3), (6, 2, 3), (11, 2, 4)):
        d = d_sys * rank
        got, fired, pcc_true, vp = 0, 0, 0, []
        for _ in range(20):
            m = pc.sample_bipartite_quasipure(d_sys, rank, s, rng)
            if m is None:
                continue
            a = pc.analyse(m)
            got += 1
            pcc_true += int(a.pcc_holds)
            vp.append(a.dim_v_perp)
            fired += int(a.certified_not_saturable and a.rank_is_robust and a.pcc_holds)
        eq.append(
            {
                "d": d,
                "r": rank,
                "s": s,
                "samples": got,
                "pcc_true": pcc_true,
                "min_dimVperp": min(vp) if vp else None,
                "fires": fired,
            }
        )
    res["eq16_negative_control"] = eq
    # (3) random (non-PCC) blocks: PCC must fail
    viol = []
    for _ in range(200):
        bl = [rng.normal(size=(6, 2)) + 1j * rng.normal(size=(6, 2)) for _ in range(4)]
        viol.append(h.pcc_violation(bl))
    res["random_blocks_pcc"] = {
        "n": 200,
        "pcc_true": int(sum(v < 1e-9 for v in viol)),
        "min_violation": float(min(viol)),
        "median": float(np.median(viol)),
    }
    # (4) small-s generic states at d=22: LB >= d, so must not fire
    small = []
    for s in (4, 10):
        rows = []
        for _ in range(20):
            rs = h.sample_sequential(20, 2, s, rng)
            rows.append(one_sample(rs[0], 22, 2, 20, s))
        small.append(summarise(rows, 22, 2, s))
    res["small_s_d22"] = small
    res["seconds"] = time.time() - t0
    save("controls", res)
    print(json.dumps(res, default=float)[:1500])


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "random":
        run_random(REQUIRED, 200, 20260919, "random")
    elif mode == "extended":
        run_random(EXTENDED, 40, 20260920, "extended")
    elif mode == "structured":
        run_structured(100, 20260921)
    elif mode == "adaptive":
        run_adaptive(20260922)
    elif mode == "controls":
        run_controls(20260923)
    elif mode == "theory":
        run_theory(20260924)
    else:
        raise SystemExit("unknown mode")
