"""Point 31: cheap empirical check of a NEW probabilistic-vertex-stability idea for H-CAT31-3's
LP-dual route (decision.md points 6, 8, 9 established that WORST-CASE vertex-movement bounds
are structurally unavailable via RIP/norm inequalities -- "LP optima sit at polytope vertices,
and vertex identity can change discontinuously under an arbitrarily small perturbation," no
tool found to bound ||y2*-y1*|| tightly). The new angle (not tried in points 6-9): instead of a
worst-case bound, ask whether the LP's ACTIVE SET (which Fx>=0 constraints are tight at the
optimum) actually jumps OFTEN or RARELY when a single generator constraint is dropped. If jumps
were rare, E[(Delta_i theta)^2] could be small ON AVERAGE via a probabilistic/concentration
argument, even though a single worst-case jump is O(1) (already established).

CAUGHT AND FIXED a real sign bug during development, kept here for transparency (audit-
verification-gate.md discipline: verify before trusting your own output). The LP constraint is
`A_ub@x <= b_ub` (`A_ub=-ReF`, `b_ub=0`), so `A_ub@x - b_ub <= 0` at any feasible x, and a TIGHT
(active) constraint has this quantity near ZERO from below. The first version checked
`slacks[k] < ACTIVE_TOL` (a positive threshold) -- which is true for EVERY negative slack, not
just near-zero ones, so it flagged ALL constraints as "active" and produced a spurious
jump_fraction=0.000 across every n tested. Caught by manually printing raw slack values for one
instance before trusting the aggregate result. Fixed to `abs(slacks[k]) < ACTIVE_TOL`, which
gives the intended near-zero test regardless of sign convention.

Uses the SAME LP as theta_via_lp (paper's time-domain primal, Table 1, arXiv:2603.29571):
    max sum(x)  s.t.  x_k=x_{n-k}, x_0=1, Fx>=0, x_k=0 for generator k "on" (edge present)
but solves it directly here (not via the theta_via_lp wrapper) so the primal solution x* and
the inequality-constraint slacks (Fx)_k are available to determine the active set.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

METRICS_DIR = Path(__file__).resolve().parent / "metrics"
ACTIVE_TOL = 1e-7  # slack below this counts as "tight" / active


def solve_lp(n: int, edges_on: set[int]):
    """Returns (theta, x*, active_set) for the time-domain primal LP with the given edge set."""
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
        return None, None, None
    x_star = res.x
    slacks = a_ub @ x_star - b_ub  # <=0 by feasibility (A_ub@x<=b_ub); ~0 means constraint tight
    active_set = frozenset(int(kk) for kk in range(n) if abs(slacks[kk]) < ACTIVE_TOL)
    return -res.fun, x_star, active_set


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
        n_jump = 0
        n_total = 0
        jump_deltas = []
        nojump_deltas = []
        for rep in range(reps_per_n):
            edges = sample_circulant(n, 0.5, rng)
            if not edges:
                continue
            theta_full, _x_full, active_full = solve_lp(n, edges)
            if theta_full is None:
                continue
            # test a couple of currently-on generators per graph, not all (cheap)
            on_list = sorted(edges)
            test_idx = on_list[: min(3, len(on_list))]
            for i_drop in test_idx:
                edges_rest = edges - {i_drop, n - i_drop if n - i_drop != i_drop else i_drop}
                # keep i_drop's mirror consistent: dropping generator i means freeing BOTH
                # i and n-i together (they're the same random bit, per sample_circulant_neighbors)
                theta_rest, _x_rest, active_rest = solve_lp(n, edges_rest)
                if theta_rest is None:
                    continue
                delta = theta_rest - theta_full
                # "jump" = active set changes beyond the trivially-freed constraints
                trivial = {i_drop, n - i_drop}
                active_full_reduced = active_full - trivial
                active_rest_reduced = active_rest - trivial
                jumped = active_full_reduced != active_rest_reduced
                n_total += 1
                if jumped:
                    n_jump += 1
                    jump_deltas.append(delta**2)
                else:
                    nojump_deltas.append(delta**2)

        row = {
            "n": n,
            "n_total_tests": n_total,
            "n_jump": n_jump,
            "jump_fraction": n_jump / n_total if n_total else float("nan"),
            "mean_delta_sq_given_jump": float(np.mean(jump_deltas)) if jump_deltas else None,
            "mean_delta_sq_given_nojump": float(np.mean(nojump_deltas)) if nojump_deltas else None,
            "n_jump_cases": len(jump_deltas),
            "n_nojump_cases": len(nojump_deltas),
        }
        all_rows.append(row)
        print(
            f"n={n:4d}  tests={n_total:4d}  jump_frac={row['jump_fraction']:.3f}  "
            f"E[delta^2|jump]={row['mean_delta_sq_given_jump']}  "
            f"E[delta^2|no_jump]={row['mean_delta_sq_given_nojump']}",
            flush=True,
        )
    return all_rows


if __name__ == "__main__":
    results = run(n_values=[11, 15, 21, 29, 37], reps_per_n=20)
    METRICS_DIR.mkdir(exist_ok=True)
    with open(METRICS_DIR / "vertex_stability_probability_check.json", "w", encoding="utf-8") as f:
        json.dump({"results": results}, f, indent=2)
