"""Task B (coordinator's narrowed request, 2026-09-16, REPLACES the earlier full min-L2 QP
re-check on n=509/1021): cheap coordinate-RANGE LP check, n=1021 ONLY.

Rationale (coordinator's own framing): the min-L2 QP (check_minimum_energy_selector.py) is
unreliable at n=509 (1/25 solves failed even at max_iter=5000; a follow-up face-width probe
hit 9/10 convergence failures) and was never attempted at n=1021 -- the size that matters
most (heaviest tail, top5pct_share=0.501 per Point 66). Rather than fighting QP convergence,
this script asks a cheaper, more robust question with plain LPs (same solver/method
CertificateLP.solve already uses): how much CAN x_i and w_i vary across the optimal face,
in the worst case? If that range is narrow relative to J_n's own statistical uncertainty,
selector-sensitivity is ruled out at an "excludes a tens-of-percent effect" resolution --
which is the bar the coordinator set, not machine-precision agreement.

For top-K |Z| rows and K random bulk-control rows (from the 180 already-computed n=1021
reps in metrics/ppl_gate_pilot.json), solve 4 plain LPs per row:
  x_i_min, x_i_max  -- min/max of free coordinate gen_index over G0's optimal face
  w_i_min, w_i_max  -- min/max of free coordinate gen_index over complement(G1)'s optimal face
Face definition is IDENTICAL to minimum_energy()/min_energy_full()'s QP face
(aub @ u <= 1, sum(u) == face_sum) -- only the objective changes (linear coordinate
min/max instead of sum-of-squares), so this probes the SAME face, just via LP not QP.

From the two coordinate intervals, the exact interval-arithmetic range of
Z^2 = n^2*(x_i*w_i)^2 is computed via the 4 corner products (x*w is bilinear, so its
extrema over a box occur at corners) -- reported per-row and aggregated per group.

READ-ONLY on codex-20260914-susceptibility/ (Unclaimed Work Ownership rule). Does not
modify ppl_gate_pilot.py, its JSON, decision.md, or anything under
codex-20260914-susceptibility/. Not committed by this script.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
CODEX_DIR = HERE / "codex-20260914-susceptibility"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(CODEX_DIR))

from ppl_gate_pilot import (  # noqa: E402
    GEN_INDEX,
    CertificateLP,
    flip_generator,
    sample_circulant_neighbors,
)

N_CHECK = 1021
TOP_K = 20
BULK_K = 20
CONTROL_SEED = 20260916  # same convention as check_minimum_energy_selector.py
LP_TIME_LIMIT = 45.0  # matches CertificateLP.solve's own linprog time_limit


def reconstruct_bits(
    n: int, seed: int, branch: str, gen_index: int
) -> tuple[np.ndarray, np.ndarray]:
    """Mirrors ppl_gate_pilot.one_case()'s construction exactly; branch is cross-checked
    against what the raw draw would produce, not merely trusted (same discipline as
    check_minimum_energy_selector.py's reconstruct_bits)."""
    c = sample_circulant_neighbors(n, 0.5, seed)
    c_flip = flip_generator(c, gen_index)
    recomputed_branch = "A" if c[gen_index] < 0.5 else "B"
    assert recomputed_branch == branch, (
        f"branch mismatch on reconstruction: stored={branch} recomputed={recomputed_branch} "
        f"(seed={seed}, n={n})"
    )
    if branch == "A":
        c_g0, c_g1 = c, c_flip
    else:
        c_g0, c_g1 = c_flip, c
    m = (n - 1) // 2
    bits_g0 = c_g0[1 : m + 1].astype(int)
    bits_g1 = c_g1[1 : m + 1].astype(int)
    return bits_g0, bits_g1


def coord_range(lp: CertificateLP, bits: np.ndarray, theta: float, gen_index: int) -> dict:
    """Min/max of x[gen_index] over the LP's optimal face (aub@u<=1, sum(u)=face_sum),
    via two plain LPs (scipy HiGHS, same solver+method as CertificateLP.solve)."""
    free = np.flatnonzero(bits == 0)
    pos = np.where(free == (gen_index - 1))[0]
    if len(pos) != 1:
        return {
            "ok": False,
            "reason": "gen_index not free on this face",
            "x_min": float("nan"),
            "x_max": float("nan"),
        }
    j = int(pos[0])
    aub = -lp.cos[:, free]
    face_sum = (theta - 1.0) / 2.0
    m1 = lp.m + 1
    A_eq = np.ones((1, len(free)))
    b_eq = np.array([face_sum])
    c_min = np.zeros(len(free))
    c_min[j] = 1.0
    c_max = -c_min
    opts = {"time_limit": LP_TIME_LIMIT}
    res_min = linprog(
        c_min,
        A_ub=aub,
        b_ub=np.ones(m1),
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=(None, None),
        method="highs",
        options=opts,
    )
    res_max = linprog(
        c_max,
        A_ub=aub,
        b_ub=np.ones(m1),
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=(None, None),
        method="highs",
        options=opts,
    )
    ok = bool(res_min.success and res_max.success)
    x_min = float(res_min.x[j]) if res_min.success else float("nan")
    x_max = float(res_max.x[j]) if res_max.success else float("nan")
    return {
        "ok": ok,
        "status_min": res_min.status,
        "status_max": res_max.status,
        "message_min": res_min.message if not res_min.success else "",
        "message_max": res_max.message if not res_max.success else "",
        "x_min": x_min,
        "x_max": x_max,
    }


def z2_interval(x_lo: float, x_hi: float, w_lo: float, w_hi: float, n: int) -> tuple[float, float]:
    """Exact interval-arithmetic range of Z^2=n^2*(x*w)^2 given x in [x_lo,x_hi], w in
    [w_lo,w_hi] -- x*w is bilinear so its extrema over the box occur at the 4 corners."""
    corners = [x_lo * w_lo, x_lo * w_hi, x_hi * w_lo, x_hi * w_hi]
    xw_min, xw_max = min(corners), max(corners)
    if xw_min >= 0:
        z2_lo, z2_hi = xw_min**2, xw_max**2
    elif xw_max <= 0:
        z2_lo, z2_hi = xw_max**2, xw_min**2
    else:
        z2_lo, z2_hi = 0.0, max(xw_min**2, xw_max**2)
    return float(n**2 * z2_lo), float(n**2 * z2_hi)


def process_rows(n: int, rows: list[dict], indices: list[int], group_label: str) -> list[dict]:
    lp = CertificateLP(n)
    gen_index = GEN_INDEX
    results = []
    started = time.monotonic()
    for j, idx in enumerate(indices):
        row = rows[idx]
        seed = int(row["seed"])
        branch = row["branch"]
        bits_g0, bits_g1 = reconstruct_bits(n, seed, branch, gen_index)
        bits_comp = 1 - bits_g1

        g0_lp = lp.solve(bits_g0)
        comp_lp = lp.solve(bits_comp)
        x_i_highs = float(g0_lp["x"][gen_index])
        w_i_highs = float(comp_lp["x"][gen_index])
        z_highs = n * x_i_highs * w_i_highs

        reconstruction_ok = (
            abs(x_i_highs - row["x_i"]) < 1e-6
            and abs(w_i_highs - row["w_i"]) < 1e-6
            and abs(z_highs - row["Z_ni"]) < 1e-4
        )

        x_range = coord_range(lp, bits_g0, g0_lp["theta"], gen_index)
        w_range = coord_range(lp, bits_comp, comp_lp["theta"], gen_index)
        ranges_ok = x_range["ok"] and w_range["ok"]

        if ranges_ok:
            # sanity: stored HiGHS vertex value should lie within the face's own range
            # (up to LP solve tolerance)
            x_within = (x_range["x_min"] - 1e-6) <= x_i_highs <= (x_range["x_max"] + 1e-6)
            w_within = (w_range["x_min"] - 1e-6) <= w_i_highs <= (w_range["x_max"] + 1e-6)
            z2_lo, z2_hi = z2_interval(
                x_range["x_min"], x_range["x_max"], w_range["x_min"], w_range["x_max"], n
            )
            stored_z2 = row["Z_ni"] ** 2
            rel_width_vs_stored = (z2_hi - z2_lo) / stored_z2 if stored_z2 else float("nan")
        else:
            x_within = w_within = False
            z2_lo = z2_hi = rel_width_vs_stored = float("nan")

        results.append(
            {
                "group": group_label,
                "seed": seed,
                "branch": branch,
                "Z_ni_stored": row["Z_ni"],
                "Z_ni2_stored": row["Z_ni"] ** 2,
                "reconstruction_matches_stored_row": reconstruction_ok,
                "x_range_ok": x_range["ok"],
                "w_range_ok": w_range["ok"],
                "x_i_min": x_range["x_min"],
                "x_i_max": x_range["x_max"],
                "w_i_min": w_range["x_min"],
                "w_i_max": w_range["x_max"],
                "x_i_highs_stored_within_range": x_within,
                "w_i_highs_stored_within_range": w_within,
                "Z2_range_min": z2_lo,
                "Z2_range_max": z2_hi,
                "Z2_range_width": (z2_hi - z2_lo) if ranges_ok else float("nan"),
                "rel_width_vs_stored_Z2": rel_width_vs_stored,
            }
        )
        if (j + 1) % 10 == 0 or j == 0:
            print(
                f"  [{n}/{group_label}] {j + 1}/{len(indices)} done, "
                f"elapsed={time.monotonic() - started:.1f}s",
                flush=True,
            )
    return results


def group_summary(results: list[dict]) -> dict:
    ok_rows = [r for r in results if r["x_range_ok"] and r["w_range_ok"]]
    n_fail = len(results) - len(ok_rows)
    n_mismatch = sum(1 for r in results if not r["reconstruction_matches_stored_row"])
    rel_widths = np.array([r["rel_width_vs_stored_Z2"] for r in ok_rows])
    x_out = sum(1 for r in ok_rows if not r["x_i_highs_stored_within_range"])
    w_out = sum(1 for r in ok_rows if not r["w_i_highs_stored_within_range"])
    return {
        "n_rows": len(results),
        "n_lp_range_failures": n_fail,
        "n_reconstruction_mismatches": n_mismatch,
        "n_stored_x_outside_range": x_out,
        "n_stored_w_outside_range": w_out,
        "mean_rel_width_vs_stored_Z2": float(np.mean(rel_widths))
        if len(rel_widths)
        else float("nan"),
        "median_rel_width_vs_stored_Z2": float(np.median(rel_widths))
        if len(rel_widths)
        else float("nan"),
        "max_rel_width_vs_stored_Z2": float(np.max(rel_widths))
        if len(rel_widths)
        else float("nan"),
        "n_rows_rel_width_gte_0.05": int(np.sum(rel_widths >= 0.05)) if len(rel_widths) else 0,
    }


def main() -> None:
    data = json.loads((HERE / "metrics" / "ppl_gate_pilot.json").read_text(encoding="utf-8"))
    rows = data["rows_by_n"][str(N_CHECK)]
    print(f"n={N_CHECK}: {len(rows)} rows total in pilot JSON")

    abs_z = [(abs(r["Z_ni"]), idx) for idx, r in enumerate(rows)]
    abs_z.sort(reverse=True)
    top_idx = [idx for _, idx in abs_z[:TOP_K]]
    top_idx_set = set(top_idx)

    non_top_idx = [i for i in range(len(rows)) if i not in top_idx_set]
    rng = np.random.default_rng(CONTROL_SEED + N_CHECK)
    control_idx = list(rng.choice(non_top_idx, size=min(BULK_K, len(non_top_idx)), replace=False))

    print(f"top-{TOP_K} by |Z| and {len(control_idx)} bulk-control rows selected")

    top_results = process_rows(N_CHECK, rows, top_idx, "top_k")
    control_results = process_rows(N_CHECK, rows, control_idx, "bulk_control")

    top_summary = group_summary(top_results)
    control_summary = group_summary(control_results)

    print("TOP-K:", json.dumps(top_summary, indent=2))
    print("BULK CONTROL:", json.dumps(control_summary, indent=2))

    out = {
        "n_checked": N_CHECK,
        "top_k": TOP_K,
        "bulk_k": BULK_K,
        "control_seed": CONTROL_SEED,
        "lp_time_limit": LP_TIME_LIMIT,
        "method": (
            "plain LP (scipy.optimize.linprog, method=highs) min/max of the free coordinate "
            "gen_index over each optimal face (aub@u<=1, sum(u)=face_sum) -- NOT the min-L2 QP; "
            "Z^2=n^2*(x_i*w_i)^2 range computed via exact interval-arithmetic corner products"
        ),
        "top_k_summary": top_summary,
        "bulk_control_summary": control_summary,
        "top_k_rows": top_results,
        "bulk_control_rows": control_results,
    }
    out_path = HERE / "metrics" / "check_coordinate_range_n1021_result.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
