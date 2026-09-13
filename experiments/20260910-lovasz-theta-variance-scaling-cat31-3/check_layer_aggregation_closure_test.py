"""Point 49 (2026-09-14): Layer-aggregated closure test -- does the K_s(L) machinery
(points 46-48) + point 44's own truncated-moment U_s(q) actually let S_n=sum_q w_q C_q be
BOUNDED from above by sum_q w_q U_{s(q)}(q), using ONLY the first s(q) real per-layer moments
at EVERY Hamming layer q, not just the central layer point 44 used?

Direct test of a user objection: "applying K_s(L) per-layer to bound C_q, then aggregating
S_n=sum_q w_q C_q <= sum_q w_q U_{s(q)}(q), requires ANALYTIC CONTROL of the real data's
moments M_r(q) for r up to s(q)~0.44*sqrt(n) on EVERY layer q -- no known technique provides
this." This script checks that claim by actually computing M_r(q) at EVERY layer (not just
center) and running the aggregation, reusing ALREADY-VERIFIED machinery unchanged:
  - solve_orbit_reduced        (check_necklace_orbit_reduction.py)          -- theta, unchanged
  - apply_L_to_layer           (check_higher_moments_M1_M6.py)              -- unchanged, already
                                general over q (point 38 only ever CALLED it at q=N//2; the
                                function itself takes combos/masks/mask_to_idx/ground_set for
                                an arbitrary layer already)
  - gamma_l_array, solve_moment_lp (check_truncated_moment_lp_bound.py)      -- unchanged

No new theta-solves: solve_orbit_reduced(n) is called exactly once per n, exactly as in every
other script in this experiment; every per-layer M_r(q) is computed from the SAME already-solved
theta_full array, matching point 33/38's own "no new theta-solves needed" property, now applied
at every layer instead of only the center.

n-range actually run: 23,29,31,37,41,43 (UPDATED 2026-09-14 -- an earlier draft of this docstring
said "23,29,31,37" only and claimed N=20/22 "would take substantially longer"; both n=41 (N=19)
and n=43 (N=20) were in fact run to completion, in ~174s and ~166s of theta-solve time plus
~104s/~204s of all-layer moment+LP time respectively -- well within this session's budget, and
this stale claim is corrected here rather than left standing next to data that contradicts it,
per a skeptic-fallback finding). n=47 (N=22) was NOT attempted: it is the single largest, most
informative point for the A_n trend (highest fraction of non-tautological, L(q)>6 layers), but
was left for a future pass rather than pushed through in this session -- honest scope limit, not
a claimed cost barrier the n=43 run already disproves. apply_L_to_layer's pure-Python double loop
costs O(v_q*d_q) per application, summed over every layer q as O(2^N * N) per moment order -- a
vectorized replacement was deliberately NOT written: reusing the ALREADY-VERIFIED slow version
is preferred over introducing new, unverified fast code, per this project's own reuse discipline.

Cross-check performed BEFORE trusting any new number (Substrate Gate): the exact S_n=sum_q w_q
C_q computed here must reproduce point 15's own already-committed n^2*S_n values (13.82, 17.45,
18.46, 21.36 for n=23,29,31,37) to high precision -- if this fails, nothing below is trusted. NOTE:
point 15 committed no reference value for n=41,43, so the substrate_check field for those two is
null/absent in the output JSON, not PASS -- an unavailable check, not a passed or skipped one;
their trust instead rests on the separate central-layer R_6 cross-check against point 44's own
committed values (see decision.md Point 49), which does cover n=41,43.
"""

from __future__ import annotations

import importlib.util
import json
import time
from itertools import combinations
from math import comb
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


nm = _load("necklace_mod_p49", HERE / "check_necklace_orbit_reduction.py")
hm6 = _load("higher_moments_m6_mod_p49", HERE / "check_higher_moments_M1_M6.py")
lp = _load("trunc_lp_mod_p49", HERE / "check_truncated_moment_lp_bound.py")

apply_L_to_layer = hm6.apply_L_to_layer  # unchanged, already general over q
gamma_l_array = lp.gamma_l_array  # unchanged
solve_moment_lp = lp.solve_moment_lp  # unchanged

# point 15's own committed n^2*S_n values (decision.md line ~1066), used as a Substrate Gate
# cross-check before trusting anything computed in this point.
KNOWN_N2_SN = {23: 13.82, 29: 17.45, 31: 18.46, 37: 21.36}

R_MAX = 6  # matches point 44's own moment order; K_s(L)<=~1.005-1.01 at these L's per points 46-48


def layer_data(x: np.ndarray, ground: list[int], q: int):
    combos = list(combinations(ground, q))
    masks = [sum(1 << b for b in c) for c in combos]
    mask_to_idx = {mk: i for i, mk in enumerate(masks)}
    f = np.array([x[mk] - x[mk | 1] for mk in masks], dtype=np.float64)
    return combos, masks, mask_to_idx, f


def run_one(n: int) -> dict:
    print(f"\n=== n={n} ===", flush=True)
    t0 = time.time()
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))
    print(f"  [theta via necklace-orbit reduction: {time.time() - t0:.1f}s]", flush=True)

    m = (n - 1) // 2
    ground = list(range(1, m))
    ground_set = set(ground)
    N = len(ground)

    layers = []
    t1 = time.time()
    for q in range(0, N + 1):
        combos, masks, mask_to_idx, f = layer_data(x, ground, q)
        v_q = len(f)
        L_q = min(q, N - q)
        w_q = comb(N, q) / (2**N)

        if v_q <= 1:
            # single point in the layer -> variance is exactly 0 by construction, no LP needed
            layers.append(
                {
                    "q": q,
                    "v_q": v_q,
                    "L_q": L_q,
                    "w_q": w_q,
                    "C_q_exact": 0.0,
                    "s_used": 0,
                    "U_s": 0.0,
                    "R_s": None,
                }
            )
            continue

        f_centered = f - f.mean()
        C_q_exact = float(np.var(f_centered))

        s_used = min(R_MAX, L_q)
        moments = []
        Lf = f_centered
        for _r in range(s_used):
            Lf = apply_L_to_layer(Lf, combos, masks, mask_to_idx, ground_set)
            moments.append(float(np.dot(f_centered, Lf)) / v_q)

        if C_q_exact <= 0.0:
            # degenerate layer (e.g. q=0 or q=N excluded above already; guard any other
            # exact-zero layer found empirically) -- LP is not meaningful, record trivially
            layers.append(
                {
                    "q": q,
                    "v_q": v_q,
                    "L_q": L_q,
                    "w_q": w_q,
                    "C_q_exact": C_q_exact,
                    "s_used": s_used,
                    "U_s": 0.0,
                    "R_s": None,
                    "moments": moments,
                }
            )
            continue

        gammas = gamma_l_array(N, q)
        up = solve_moment_lp(gammas, moments, maximize=True)
        U_s = up["value"] if up.get("success") else float("nan")
        R_s = U_s / C_q_exact if up.get("success") else float("nan")

        layers.append(
            {
                "q": q,
                "v_q": v_q,
                "L_q": L_q,
                "w_q": w_q,
                "C_q_exact": C_q_exact,
                "s_used": s_used,
                "moments": moments,
                "U_s": U_s,
                "R_s": R_s,
                "lp_success": up.get("success"),
            }
        )
        print(
            f"  q={q:3d} L={L_q:2d} v_q={v_q:6d} s={s_used} C_q={C_q_exact:.6f} "
            f"U_s={U_s:.6f} R_s={R_s:.4f}",
            flush=True,
        )

    elapsed = time.time() - t1
    print(f"  [all layers done in {elapsed:.1f}s]", flush=True)

    S_n_exact = sum(row["w_q"] * row["C_q_exact"] for row in layers)
    S_n_bound = sum(row["w_q"] * row["U_s"] for row in layers)
    A_n = S_n_bound / S_n_exact if S_n_exact > 0 else float("nan")

    n2_Sn = (n**2) * S_n_exact
    known = KNOWN_N2_SN.get(n)
    substrate_check = None
    if known is not None:
        rel_err = abs(n2_Sn - known) / known
        substrate_check = {
            "known_n2_Sn": known,
            "computed_n2_Sn": n2_Sn,
            "rel_err": rel_err,
            "passed": rel_err < 1e-2,
        }
        print(
            f"  [SUBSTRATE CHECK] n^2*S_n computed={n2_Sn:.4f} vs point-15 committed={known:.4f} "
            f"rel_err={rel_err:.2e} -> {'PASS' if substrate_check['passed'] else 'FAIL'}",
            flush=True,
        )

    print(
        f"  S_n_exact={S_n_exact:.8f}  S_n_bound={S_n_bound:.8f}  "
        f"A_n=S_n_bound/S_n_exact={A_n:.6f}",
        flush=True,
    )

    return {
        "n": n,
        "N": N,
        "layers": layers,
        "S_n_exact": S_n_exact,
        "S_n_bound": S_n_bound,
        "A_n": A_n,
        "n2_Sn_exact": n2_Sn,
        "substrate_check": substrate_check,
        "total_elapsed_s": time.time() - t0,
    }


def run(n_values: list[int]) -> list[dict]:
    METRICS.mkdir(exist_ok=True)
    out_path = METRICS / "layer_aggregation_closure_test.json"
    results: list[dict] = []
    if out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            results = json.load(f).get("rows", [])
    done_ns = {r["n"] for r in results}
    for n in n_values:
        if n in done_ns:
            print(f"=== n={n} already done, skipping ===", flush=True)
            continue
        results.append(run_one(n))
        results.sort(key=lambda r: r["n"])
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"rows": results}, f, indent=2)

    print("\n--- Summary: A_n = S_n_bound / S_n_exact ---")
    for r in sorted(results, key=lambda r: r["n"]):
        sc = r["substrate_check"]
        sc_str = f" [substrate:{'PASS' if sc and sc['passed'] else 'FAIL/NA'}]"
        print(f"n={r['n']:3d}  S_n_exact={r['S_n_exact']:.8f}  A_n={r['A_n']:.6f}{sc_str}")
    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        run([int(x) for x in sys.argv[1:]])
    else:
        run([23, 29, 31, 37])
    print("\nDone.", flush=True)
