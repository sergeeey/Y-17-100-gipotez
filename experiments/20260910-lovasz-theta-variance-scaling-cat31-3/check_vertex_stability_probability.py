"""Point 31: cheap empirical check of a probabilistic-vertex-stability idea for H-CAT31-3's
LP-dual route (decision.md points 6, 8, 9 established that WORST-CASE vertex-movement bounds
are structurally unavailable via RIP/norm inequalities -- "LP optima sit at polytope vertices,
and vertex identity can change discontinuously under an arbitrarily small perturbation," no
tool found to bound ||y2*-y1*|| tightly). The new angle (not tried in points 6-9): instead of a
worst-case bound, ask whether the LP's ACTIVE SET (which Fx>=0 constraints are tight at the
optimum) actually jumps OFTEN or RARELY when a single generator constraint is dropped. If jumps
were rare, E[(Delta_i theta)^2] could be small ON AVERAGE via a probabilistic/concentration
argument, even though a single worst-case jump is O(1) (already established).

Uses the SAME LP as theta_via_lp (paper's time-domain primal, Table 1, arXiv:2603.29571):
    max sum(x)  s.t.  x_k=x_{n-k}, x_0=1, Fx>=0, x_k=0 for generator k "on" (edge present)
but solves it directly here (not via the theta_via_lp wrapper) so the primal solution x* and
the inequality-constraint slacks (Fx)_k are available to determine the active set.

TWO corrections made during development, kept here for transparency (audit-verification-
gate.md discipline: verify before trusting your own output; Hindsight Distortion Gap
discipline: record what was actually found and when, not a cleaned-up version):

1. Sign bug: the first tightness test (`slacks[k] < ACTIVE_TOL`) is true for EVERY negative
   slack, not just near-zero ones, given the LP's sign convention (`A_ub@x - b_ub <= 0` at
   feasibility) -- flagged ALL constraints as "active," producing a spurious jump_fraction=0.000
   at every n. Fixed to `abs(slacks[k]) < ACTIVE_TOL`.

2. Criterion too coarse: the first corrected version compared `active_full - {i,n-i}` against
   `active_rest - {i,n-i}` (subtracting the dropped variable's column indices from the active
   ROW-index sets -- indexes the wrong space, does almost nothing empirically) and counted ANY
   set difference as a "jump." But dropping generator i removes 2 equality constraints
   (x_i=0 and its mirror x_{n-i}=0), so the reduced LP's vertex generically needs 2 MORE tight
   inequalities than before with NOTHING removed -- a trivial degrees-of-freedom adjustment, not
   an interesting structural change. The corrected criterion below only counts a case as a
   genuine "restructure" when at least one PREVIOUSLY-active constraint becomes inactive
   (active_full is NOT a subset of active_rest). Independently confirmed (this session +
   reviewer, different scripts) that changes come in PAIRS because `ReF` has duplicate rows
   (`ReF[j,:]==ReF[n-j,:]` for all j, since cos is even, verified to float-noise precision) --
   inequality constraints j and n-j are literally identical, so any newly-tight constraint
   necessarily activates as a pair.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

METRICS_DIR = Path(__file__).resolve().parent / "metrics"
ACTIVE_TOL = 1e-7  # active slacks are ~1e-16 (float noise), smallest inactive ones are >0.02


def solve_lp(n: int, edges_on: set[int]):
    """Returns (theta, active_set) for the time-domain primal LP with the given edge set."""
    j = np.arange(n).reshape(-1, 1)
    k = np.arange(n).reshape(1, -1)
    ReF = np.cos(-2 * np.pi * j * k / n)

    a_eq_rows = []
    b_eq = []
    e0 = np.zeros(n)
    e0[0] = 1.0
    a_eq_rows.append(e0)
    b_eq.append(1.0)
    for kk in range(1, (n - 1) // 2 + 1):
        row = np.zeros(n)
        row[kk] = 1.0
        row[n - kk] = -1.0
        a_eq_rows.append(row)
        b_eq.append(0.0)
    for kk in range(1, n):
        if kk in edges_on:
            row = np.zeros(n)
            row[kk] = 1.0
            a_eq_rows.append(row)
            b_eq.append(0.0)
    a_eq = np.array(a_eq_rows)

    a_ub = -ReF
    b_ub = np.zeros(n)

    res = linprog(
        c=-np.ones(n),
        A_ub=a_ub,
        b_ub=b_ub,
        A_eq=a_eq,
        b_eq=b_eq,
        bounds=(None, None),
        method="highs",
    )
    if not res.success:
        return None, None
    x_star = res.x
    slacks = a_ub @ x_star - b_ub  # <=0 by feasibility; ~0 means constraint tight
    active_set = frozenset(int(kk) for kk in range(n) if abs(slacks[kk]) < ACTIVE_TOL)
    return -res.fun, active_set


def sample_circulant(n: int, p: float, rng: np.random.Generator) -> set[int]:
    half = (n - 1) // 2
    edges = set()
    for kk in range(1, half + 1):
        if rng.random() < p:
            edges.add(kk)
            edges.add(n - kk)
    if n % 2 == 0 and rng.random() < p:
        edges.add(n // 2)
    return edges


def run(n_values, reps_per_n, seed_base=777000):
    all_rows = []
    for n in n_values:
        rng = np.random.default_rng(seed_base + n)
        n_trivial = 0
        n_restructure = 0
        n_total = 0
        restructure_deltas = []
        trivial_deltas = []
        removed_counts = []
        for _rep in range(reps_per_n):
            edges = sample_circulant(n, 0.5, rng)
            if not edges:
                continue
            theta_full, active_full = solve_lp(n, edges)
            if theta_full is None:
                continue
            # test the 3 smallest currently-on generators per graph, not all (cheap) --
            # proven neutral for prime n only (points 12-13's exact symmetry theorem),
            # unverified for composite n (reviewer P2, not blocking).
            on_list = sorted(edges)
            test_idx = on_list[: min(3, len(on_list))]
            for i_drop in test_idx:
                edges_rest = edges - {i_drop, n - i_drop}
                theta_rest, active_rest = solve_lp(n, edges_rest)
                if theta_rest is None:
                    continue
                delta = theta_rest - theta_full
                removed = active_full - active_rest  # previously active, now inactive
                # "trivial" DOF growth: nothing removed (active_full subset of active_rest).
                # "genuine restructure": at least one previously-active constraint dropped out.
                is_trivial = len(removed) == 0
                n_total += 1
                removed_counts.append(len(removed))
                if is_trivial:
                    n_trivial += 1
                    trivial_deltas.append(delta**2)
                else:
                    n_restructure += 1
                    restructure_deltas.append(delta**2)

        row = {
            "n": n,
            "n_total": n_total,
            "n_trivial_dof_only": n_trivial,
            "n_genuine_restructure": n_restructure,
            "restructure_fraction": n_restructure / n_total if n_total else float("nan"),
            "mean_delta_sq_trivial": float(np.mean(trivial_deltas)) if trivial_deltas else None,
            "mean_delta_sq_restructure": (
                float(np.mean(restructure_deltas)) if restructure_deltas else None
            ),
            "mean_removed_count": float(np.mean(removed_counts)) if removed_counts else None,
        }
        all_rows.append(row)
        print(
            f"n={n:4d} total={n_total:4d} restructure_frac={row['restructure_fraction']:.3f} "
            f"E[d2|trivial]={row['mean_delta_sq_trivial']} "
            f"E[d2|restructure]={row['mean_delta_sq_restructure']} "
            f"mean_removed={row['mean_removed_count']:.3f}",
            flush=True,
        )
    return all_rows


if __name__ == "__main__":
    results = run(n_values=[11, 15, 21, 29, 37], reps_per_n=20)
    METRICS_DIR.mkdir(exist_ok=True)
    with open(METRICS_DIR / "vertex_stability_probability_check.json", "w", encoding="utf-8") as f:
        json.dump({"results": results}, f, indent=2)
