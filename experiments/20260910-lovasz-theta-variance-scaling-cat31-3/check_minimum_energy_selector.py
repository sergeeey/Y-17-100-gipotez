"""Task 2 (Point 66 next-steps item #2 / skeptic concern), coordinator-extended version:
re-solve the top-5% |Z_ni| rows of the PPL_gate pilot (metrics/ppl_gate_pilot.json) using
the theoretically-required unique min-L2 selector (`minimum_energy()` / CLARABEL QP,
codex-20260914-susceptibility/test_optimal_energy.py) instead of the raw scipy.linprog
HiGHS vertex (CertificateLP.solve), to check whether J_n's apparent growth/level is partly
an artifact of HiGHS's own pivoting behavior on a possibly-degenerate optimal face, rather
than a property of the theoretically-intended x*_i * w*_i itself.

Coordinator addendum (this session): also draw a BULK RANDOM CONTROL sample (same size k,
drawn from the rows NOT in the top-5%) so top-5% vs bulk can be compared directly, and
report rho = Z_min_energy^2 / Z_HiGHS^2 per row for each group. If rho << 1 specifically in
the top-5% group but rho ~= 1 in the bulk-control group, that supports "the tail growth is
partly a HiGHS-pivoting artifact." If rho ~= 1 in both groups, the tail is not a selector
artifact.

READ-ONLY on codex-20260914-susceptibility/ (Unclaimed Work Ownership rule -- the QP
formulation is reproduced from minimum_energy() rather than importing+modifying it, so a
single solve per row can return both the diagnostic fields AND the full x vector). Does not
modify ppl_gate_pilot.py, its JSON, decision.md, or anything under codex-20260914-susceptibility/.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CODEX_DIR = HERE / "codex-20260914-susceptibility"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(CODEX_DIR))

import cvxpy as cp  # noqa: E402
from ppl_gate_pilot import (  # noqa: E402
    GEN_INDEX,
    CertificateLP,
    flip_generator,
    sample_circulant_neighbors,
)

TOP_FRAC = 0.05
SIZES_TO_CHECK = (127, 509)  # 1021 optional per task brief; skipped here for time budget
CONTROL_SEED = 20260916  # fresh seed for the bulk-control row selection, distinct from pilot seeds


def reconstruct_bits(
    n: int, seed: int, branch: str, gen_index: int
) -> tuple[np.ndarray, np.ndarray]:
    """Exactly mirrors ppl_gate_pilot.one_case()'s construction, deterministically, given
    the row's own saved (n, seed, branch) -- branch is cross-checked against what the raw
    draw would produce, not merely trusted."""
    c = sample_circulant_neighbors(n, 0.5, seed)
    c_flip = flip_generator(c, gen_index)
    recomputed_branch = "A" if c[gen_index] < 0.5 else "B"
    assert recomputed_branch == branch, (
        f"branch mismatch on reconstruction: stored={branch} recomputed={recomputed_branch} "
        f"(seed={seed}, n={n}) -- sampling is not reproducing the original row"
    )
    if branch == "A":
        c_g0, c_g1 = c, c_flip
    else:
        c_g0, c_g1 = c_flip, c
    m = (n - 1) // 2
    bits_g0 = c_g0[1 : m + 1].astype(int)
    bits_g1 = c_g1[1 : m + 1].astype(int)
    return bits_g0, bits_g1


def min_energy_full(lp: CertificateLP, bits: np.ndarray, theta: float, gen_index: int) -> dict:
    """Reproduces test_optimal_energy.minimum_energy()'s exact QP (same objective,
    constraints, solver, tolerances) in a single solve, returning both its diagnostic
    fields (face_error, primal_error) AND x[gen_index] -- minimum_energy() itself only
    returns summary energy stats, not the full x vector, so re-implementing rather than
    importing+modifying avoids a second identical solve per row.

    WHY the retry ladder: at n=509 (m~254 free vars per row), CLARABEL's default
    max_iter=500 (the exact value test_optimal_energy.py itself uses, calibrated for its
    OWN n<=2039/12-seeds-per-size pilot, not for hitting every one of 500 n=127 pilot
    seeds) occasionally returns status "user_limit" (iteration cap hit, not converged) --
    NOT a solver failure, a budget-too-small-for-this-specific-row situation. Retried once
    at 5000 iterations before treating it as a genuine failure; failures are recorded as
    NaN (and counted, not silently dropped) rather than crashing the whole run."""
    free = np.flatnonzero(bits == 0)
    aub = -lp.cos[:, free]
    face_sum = (theta - 1.0) / 2.0
    for max_iter in (500, 5000):
        u = cp.Variable(len(free))
        problem = cp.Problem(cp.Minimize(cp.sum_squares(u)), [aub @ u <= 1, cp.sum(u) == face_sum])
        try:
            problem.solve(
                solver="CLARABEL",
                tol_gap_abs=1e-9,
                tol_feas=1e-9,
                tol_gap_rel=1e-9,
                max_iter=max_iter,
                verbose=False,
            )
        except cp.error.SolverError:
            # WHY: a hard SolverError (not just a bad status) has been observed at n=509 on
            # the retry pass -- a genuine numerical failure (overflow in the QP's own
            # squared-norm objective), not merely "needs more iterations." Treated the same
            # as a bad status: try the next max_iter, then give up and record NaN.
            continue
        if problem.status in {cp.OPTIMAL, cp.OPTIMAL_INACCURATE} and u.value is not None:
            reduced = np.asarray(u.value, dtype=float)
            x = np.zeros(lp.n)
            x[0] = 1.0
            x[free + 1] = reduced
            x[lp.n - (free + 1)] = reduced
            face_error = abs(float(x.sum()) - theta)
            primal_error = float(max(0.0, np.max(aub @ reduced - 1.0))) if len(free) else 0.0
            return {
                "x_i": float(x[gen_index]),
                "face_error": face_error,
                "primal_error": primal_error,
                "solver_status": problem.status,
                "solve_failed": False,
            }
    return {
        "x_i": float("nan"),
        "face_error": float("nan"),
        "primal_error": float("nan"),
        "solver_status": problem.status,
        "solve_failed": True,
    }


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

        g0_me = min_energy_full(lp, bits_g0, g0_lp["theta"], gen_index)
        comp_me = min_energy_full(lp, bits_comp, comp_lp["theta"], gen_index)
        solve_failed = g0_me["solve_failed"] or comp_me["solve_failed"]
        x_i_me = g0_me["x_i"]
        w_i_me = comp_me["x_i"]
        z_me = n * x_i_me * w_i_me

        if solve_failed or z_highs == 0:
            rho = float("nan")
        else:
            rho = z_me**2 / z_highs**2

        results.append(
            {
                "group": group_label,
                "seed": seed,
                "branch": branch,
                "Z_ni_stored": row["Z_ni"],
                "reconstruction_matches_stored_row": reconstruction_ok,
                "min_energy_solve_failed": solve_failed,
                "x_i_highs": x_i_highs,
                "w_i_highs": w_i_highs,
                "Z_highs": z_highs,
                "x_i_min_energy": x_i_me,
                "w_i_min_energy": w_i_me,
                "Z_min_energy": z_me,
                "g0_face_error": g0_me["face_error"],
                "g0_primal_error": g0_me["primal_error"],
                "comp_face_error": comp_me["face_error"],
                "comp_primal_error": comp_me["primal_error"],
                "rho_Z2_ratio_minE_over_highs": rho,
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
    n_failed = sum(1 for r in results if r["min_energy_solve_failed"])
    ok = [r for r in results if not r["min_energy_solve_failed"]]
    rho = np.array([r["rho_Z2_ratio_minE_over_highs"] for r in ok])
    n_mismatch = sum(1 for r in results if not r["reconstruction_matches_stored_row"])
    return {
        "n_rows": len(results),
        "n_min_energy_solve_failures": n_failed,
        "n_reconstruction_mismatches": n_mismatch,
        "mean_rho": float(np.mean(rho)) if len(rho) else float("nan"),
        "median_rho": float(np.median(rho)) if len(rho) else float("nan"),
        "min_rho": float(np.min(rho)) if len(rho) else float("nan"),
        "max_rho": float(np.max(rho)) if len(rho) else float("nan"),
        "mean_Z2_highs": float(np.mean([r["Z_highs"] ** 2 for r in ok])) if ok else float("nan"),
        "mean_Z2_min_energy": (
            float(np.mean([r["Z_min_energy"] ** 2 for r in ok])) if ok else float("nan")
        ),
    }


def process_size(n: int, rows: list[dict]) -> dict:
    abs_z = [(abs(r["Z_ni"]), idx) for idx, r in enumerate(rows)]
    abs_z.sort(reverse=True)
    k = max(1, int(np.ceil(TOP_FRAC * len(rows))))
    top_idx = [idx for _, idx in abs_z[:k]]
    top_idx_set = set(top_idx)

    non_top_idx = [i for i in range(len(rows)) if i not in top_idx_set]
    rng = np.random.default_rng(CONTROL_SEED + n)
    control_idx = list(rng.choice(non_top_idx, size=min(k, len(non_top_idx)), replace=False))

    print(
        f"n={n}: {len(rows)} rows total, top {TOP_FRAC:.0%} = {k} rows (tail group), "
        f"{len(control_idx)} rows bulk-control (random, excludes tail group)"
    )

    top_results = process_rows(n, rows, top_idx, "top5pct")
    control_results = process_rows(n, rows, control_idx, "bulk_control")

    top_summary = group_summary(top_results)
    control_summary = group_summary(control_results)

    print(
        f"n={n} TOP5%:   mean_rho={top_summary['mean_rho']:.4f} "
        f"median_rho={top_summary['median_rho']:.4f} "
        f"[{top_summary['min_rho']:.4f}, {top_summary['max_rho']:.4f}] "
        f"mismatches={top_summary['n_reconstruction_mismatches']}/{top_summary['n_rows']}",
        flush=True,
    )
    print(
        f"n={n} BULK:    mean_rho={control_summary['mean_rho']:.4f} "
        f"median_rho={control_summary['median_rho']:.4f} "
        f"[{control_summary['min_rho']:.4f}, {control_summary['max_rho']:.4f}] "
        f"mismatches={control_summary['n_reconstruction_mismatches']}/{control_summary['n_rows']}",
        flush=True,
    )

    return {
        "n": n,
        "n_rows_total": len(rows),
        "top_k": k,
        "top5pct_summary": top_summary,
        "bulk_control_summary": control_summary,
        "top5pct_rows": top_results,
        "bulk_control_rows": control_results,
    }


def main() -> None:
    data = json.loads((HERE / "metrics" / "ppl_gate_pilot.json").read_text(encoding="utf-8"))
    rows_by_n = data["rows_by_n"]

    all_summaries = {}
    for n in SIZES_TO_CHECK:
        rows = rows_by_n[str(n)]
        all_summaries[str(n)] = process_size(n, rows)

    out = {
        "top_frac": TOP_FRAC,
        "sizes_checked": list(SIZES_TO_CHECK),
        "control_seed": CONTROL_SEED,
        "rho_definition": "rho = Z_min_energy^2 / Z_HiGHS^2 per row -- rho<<1 means the "
        "min-L2 selector gives a much smaller |Z| than the raw HiGHS vertex on that row",
        "summaries": all_summaries,
    }
    out_path = HERE / "metrics" / "check_minimum_energy_selector_result.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
