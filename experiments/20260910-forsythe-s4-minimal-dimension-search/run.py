"""H-CAT37-2 -- targeted (optimization-driven) search for an s=4 Forsythe
counterexample at dimension n in {5, 6, 7}, below the published dimension-8
construction (Colbrook, Stepaniants, Townsend, arXiv:2609.04659).

Reuses H-CAT37-1's restart-iteration machinery unchanged (import, not
duplication) -- only the search STRATEGY differs (optimization vs random
sampling).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution


def _load_h_cat37_1_run():
    # Both experiment folders have a module literally named `run.py` --
    # sys.path.insert + `from run import ...` would hit a circular-import
    # collision when THIS file is itself imported as `run` (e.g. by its own
    # tests). Load the sibling module under a distinct name instead.
    path = (
        Path(__file__).resolve().parents[1]
        / "20260909-forsythe-conjecture-restart-cg-search"
        / "run.py"
    )
    spec = importlib.util.spec_from_file_location("h_cat37_1_run", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run_restarted_iteration = _load_h_cat37_1_run().run_restarted_iteration

S = 4
SEEDS_PER_EVAL = 3
EVAL_RESTARTS = 800
EXTENDED_RESTARTS = 5000
LOG_BOUND = 3.0  # diagonal entries in [exp(-3), exp(3)] ~= [0.05, 20]


def diag_matrix_from_log_params(log_params: np.ndarray) -> np.ndarray:
    entries = np.exp(log_params)
    return np.diag(entries)


def objective(log_params: np.ndarray, base_seed: int) -> float:
    """Returns -mean(score) across SEEDS_PER_EVAL fixed seeds --
    differential_evolution minimizes, so this pushes toward maximizing score,
    i.e. toward non-convergence.

    WHY this needed fixing (found this session, not assumed): a first version
    penalized every exact_solve_hit with a FLAT -1.0. A pilot run showed 100%
    of the initial random population hit exact_solve_hit within 7-16 restarts
    (out of an 800-restart budget) at all three tested n -- the objective was
    therefore constant (-1.0) almost everywhere the optimizer looked, giving
    differential_evolution zero gradient to work with; it could not have been
    doing anything but returning an arbitrary point. Fixed by rewarding SLOWER
    exact-solves continuously (restarts_run / EVAL_RESTARTS, in [0,1)) instead
    of collapsing them all to the same value -- this gives the search a real
    signal toward whatever parameter region delays trivial convergence, which
    is presumably closer to (not necessarily at) the boundary of interest."""
    A = diag_matrix_from_log_params(log_params)
    scores = []
    for i in range(SEEDS_PER_EVAL):
        res = run_restarted_iteration(A, S, base_seed + i, max_restarts=EVAL_RESTARTS)
        if res["breakdown_hit"]:
            scores.append(-1.0)  # rare, no natural gradient available
        elif res["exact_solve_hit"]:
            # -1.0 (immediate) up to ~-0.1 (took nearly the whole budget)
            scores.append(-1.0 + min(0.9, res["restarts_run"] / EVAL_RESTARTS))
        else:
            slope = res.get("decay_slope")
            scores.append(slope if slope is not None else -1.0)
    return -float(np.mean(scores))


def search_dimension(n: int, base_seed: int, maxiter: int = 40, popsize: int = 10):
    bounds = [(-LOG_BOUND, LOG_BOUND)] * n
    result = differential_evolution(
        objective,
        bounds,
        args=(base_seed,),
        maxiter=maxiter,
        popsize=popsize,
        seed=base_seed,
        tol=1e-6,
        polish=True,
    )
    best_log_params = result.x
    best_slope_estimate = -result.fun
    return best_log_params, best_slope_estimate


def extended_check(log_params: np.ndarray, base_seed: int, n_seeds: int = 5):
    """Re-check the optimizer's best candidate at EXTENDED_RESTARTS with
    fresh, independent seeds -- guards against the same short-observation-
    window artifact H-CAT37-1 itself caught (a slope that looks near-zero at
    800 restarts can still resolve to real decay given more restarts)."""
    A = diag_matrix_from_log_params(log_params)
    rows = []
    for i in range(n_seeds):
        res = run_restarted_iteration(A, S, base_seed + 1000 + i, max_restarts=EXTENDED_RESTARTS)
        rows.append(
            {
                "seed": base_seed + 1000 + i,
                "exact_solve_hit": res["exact_solve_hit"],
                "breakdown_hit": res["breakdown_hit"],
                "decay_slope": res.get("decay_slope"),
                "restarts_run": res["restarts_run"],
            }
        )
    return rows


def cmd_run():
    out = {"claim": "H-CAT37-2 targeted search for s=4 counterexample, n in {5,6,7}", "s": S}
    for n in (5, 6, 7):
        base_seed = 372000 + n * 100
        best_log_params, best_slope_estimate = search_dimension(n, base_seed)
        extended_rows = extended_check(best_log_params, base_seed)
        resolved_all = all(
            r["exact_solve_hit"] or (r["decay_slope"] is not None and r["decay_slope"] < -1e-4)
            for r in extended_rows
        )
        out[f"n={n}"] = {
            "best_diag_entries": np.exp(best_log_params).tolist(),
            "eval_slope_estimate_800_restarts": best_slope_estimate,
            "extended_check_5000_restarts": extended_rows,
            "resolved_to_convergence": resolved_all,
        }
        print(f"n={n}: eval_slope={best_slope_estimate:.6f}, resolved={resolved_all}")

    Path(__file__).parent.joinpath("metrics").mkdir(exist_ok=True)
    with open(Path(__file__).parent / "metrics" / "run.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    return out


if __name__ == "__main__":
    cmd_run()
