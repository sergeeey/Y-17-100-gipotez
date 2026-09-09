"""run.py -- H-CAT31-2: tail/arithmetic structure of Lovasz theta for random dense circulant
graphs, near-prime vs composite n, per reports/2026-09-09-breakthrough-routes.md Route 2's own
first bounded test.

Reuses H-CAT31-1's sample_circulant_neighbors/theta_via_lp UNCHANGED via distinct-name import
(both already independently cross-validated in H-CAT31-1's own tests against known closed
forms) -- no new theta-computation machinery is introduced here.

For each of 3 pre-specified (prime, composite) n pairs, samples N_REPS random dense circulant
graphs per n, computes X = log(theta(G)/sqrt(n)), and characterizes the TAIL of that
distribution (variance, range, top-decile contribution to E[cosh(X)-1]) -- H-CAT31-1 only ever
reported the mean.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"

N_REPS = 500
BOOTSTRAP_RESAMPLES = 2000
BOOTSTRAP_SEED = 31200


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("h_cat31_2_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
theta_via_lp = h_cat31_1.theta_via_lp

# (prime, composite) pairs, taken verbatim from reports/2026-09-09-breakthrough-routes.md --
# chosen by that document before this experiment's data existed, not cherry-picked here.
PAIRS = [(127, 129), (251, 255), (509, 511)]


def complement_neighbors(c: np.ndarray) -> np.ndarray:
    """Connection-offset vector of the complement circulant graph: every non-self offset flips."""
    n = len(c)
    c_bar = np.zeros(n)
    c_bar[1:] = 1.0 - c[1:n]
    return c_bar


def top_decile_contribution(x: np.ndarray) -> float:
    """Fraction of sum(cosh(x)-1) coming from the top 10% of |x| values -- the tail-concentration
    signal claim.md's reformulation motivates (E[theta]/sqrt(n)-1 = E[cosh(X)-1])."""
    vals = np.cosh(x) - 1.0
    total = vals.sum()
    if total <= 0:
        return float("nan")
    n_top = max(1, int(np.ceil(0.10 * len(x))))
    order = np.argsort(-np.abs(x))
    top_sum = vals[order[:n_top]].sum()
    return float(top_sum / total)


def bootstrap_ci_top_decile(x: np.ndarray, n_resamples: int, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    n = len(x)
    stats = np.empty(n_resamples)
    for i in range(n_resamples):
        idx = rng.integers(0, n, size=n)
        stats[i] = top_decile_contribution(x[idx])
    lo, hi = np.percentile(stats, [2.5, 97.5])
    return float(lo), float(hi)


def sample_n(n: int, n_reps: int, seed_base: int, p: float = 0.5) -> dict:
    xs = []
    max_positive_control_violation = 0.0
    for i in range(n_reps):
        seed = seed_base + i
        c = sample_circulant_neighbors(n, p, seed)
        theta = theta_via_lp(c)
        c_bar = complement_neighbors(c)
        theta_bar = theta_via_lp(c_bar)
        pc_violation = abs(theta * theta_bar / n - 1.0)
        max_positive_control_violation = max(max_positive_control_violation, pc_violation)
        x = float(np.log(theta / np.sqrt(n)))
        xs.append(x)

    x_arr = np.array(xs)
    lo, hi = bootstrap_ci_top_decile(x_arr, BOOTSTRAP_RESAMPLES, BOOTSTRAP_SEED + n)

    return {
        "n": n,
        "n_reps": n_reps,
        "mean_X": float(x_arr.mean()),
        "var_X": float(x_arr.var(ddof=1)),
        "range_X": float(x_arr.max() - x_arr.min()),
        "top_decile_contribution": top_decile_contribution(x_arr),
        "top_decile_contribution_ci95": [lo, hi],
        "max_positive_control_violation": max_positive_control_violation,
        "mean_theta_over_sqrt_n": float(np.exp(x_arr).mean()),
    }


def cmd_run() -> dict:
    pair_results = []
    seed_base = 312000
    for prime_n, composite_n in PAIRS:
        prime_result = sample_n(prime_n, N_REPS, seed_base)
        seed_base += N_REPS + 1000
        composite_result = sample_n(composite_n, N_REPS, seed_base)
        seed_base += N_REPS + 1000

        var_ratio = composite_result["var_X"] / prime_result["var_X"]
        td_ratio = (
            composite_result["top_decile_contribution"] / prime_result["top_decile_contribution"]
        )
        ci_overlap = not (
            composite_result["top_decile_contribution_ci95"][1]
            < prime_result["top_decile_contribution_ci95"][0]
            or prime_result["top_decile_contribution_ci95"][1]
            < composite_result["top_decile_contribution_ci95"][0]
        )

        pair_results.append(
            {
                "prime_n": prime_n,
                "composite_n": composite_n,
                "prime": prime_result,
                "composite": composite_result,
                "composite_over_prime_var_ratio": var_ratio,
                "composite_over_prime_top_decile_ratio": td_ratio,
                "top_decile_ci95_overlap": ci_overlap,
                "composite_has_higher_var": var_ratio > 1.0,
                "composite_has_higher_top_decile": td_ratio > 1.0,
            }
        )

    max_pc_violation = max(
        max(
            pr["prime"]["max_positive_control_violation"],
            pr["composite"]["max_positive_control_violation"],
        )
        for pr in pair_results
    )
    positive_control_passed = max_pc_violation <= 1e-6

    var_directions = [pr["composite_has_higher_var"] for pr in pair_results]
    td_directions = [pr["composite_has_higher_top_decile"] for pr in pair_results]
    consistent_var_direction = all(var_directions) or not any(var_directions)
    consistent_td_direction = all(td_directions) or not any(td_directions)

    substantial_var_effect = all(
        (
            pr["composite_over_prime_var_ratio"] >= 1.5
            or pr["composite_over_prime_var_ratio"] <= 1 / 1.5
        )
        for pr in pair_results
    )
    substantial_td_effect = all(
        (
            pr["composite_over_prime_top_decile_ratio"] >= 1.5
            or pr["composite_over_prime_top_decile_ratio"] <= 1 / 1.5
        )
        for pr in pair_results
    )
    all_ci_disjoint = all(not pr["top_decile_ci95_overlap"] for pr in pair_results)

    if not positive_control_passed:
        verdict = "CRITERION_INVALID"
    elif consistent_td_direction and substantial_td_effect and all_ci_disjoint:
        verdict = "LEAD"
    elif consistent_var_direction and substantial_var_effect:
        verdict = "LEAD"
    else:
        verdict = "REJECTED"

    out = {
        "claim": "H-CAT31-2 -- tail/arithmetic structure of Lovasz theta, near-prime vs "
        "composite n",
        "pairs": pair_results,
        "positive_control": {
            "max_violation_of_theta_times_thetabar_over_n": max_pc_violation,
            "threshold": 1e-6,
            "passed": positive_control_passed,
        },
        "consistent_var_direction_across_pairs": consistent_var_direction,
        "consistent_top_decile_direction_across_pairs": consistent_td_direction,
        "all_top_decile_ci95_disjoint": all_ci_disjoint,
        "verdict": verdict,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
