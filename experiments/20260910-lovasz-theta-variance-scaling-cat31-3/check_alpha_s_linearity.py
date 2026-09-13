"""Point 39a: directly test a load-bearing claim in an external LLM's re-analysis of points
35-38 -- that alpha_s (the log-log decay exponent of M_s vs n) grows LINEARLY in s, used there
to argue the moment-bound route is "fundamentally obstructed" (stuck at a fixed exponent)
regardless of the (s,k) choice in the tail bound Sum_{l<k}E_l + M_s/gamma_k^s.

Cheap, uses ONLY already-computed data (metrics/higher_moments_M1_M6.json, all 7 n). No new
theta-solves. Checks/refutes rather than accepting the external claim on faith, per
audit-verification-gate.md (external [VERIFIED] = our [INFERRED] until independently checked).
"""

from __future__ import annotations

import itertools
import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def loglog_slope(xs: list[float], ys: list[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx, my = statistics.mean(lx), statistics.mean(ly)
    num = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    den = sum((x - mx) ** 2 for x in lx)
    return num / den if den else float("nan")


def run() -> dict:
    with open(METRICS / "higher_moments_M1_M6.json", encoding="utf-8") as f:
        rows = json.load(f)["rows"]
    rows.sort(key=lambda r: r["n"])
    ns = [r["n"] for r in rows]
    print(f"n values: {ns}\n", flush=True)

    alphas = {}
    for s in range(1, 7):
        vals = [r[f"M{s}"] for r in rows]
        slope = loglog_slope(ns, vals)
        alphas[s] = -slope
        print(f"M{s}: alpha_{s} = {-slope:.4f}", flush=True)

    diffs = [alphas[s + 1] - alphas[s] for s in range(1, 6)]
    print(f"\nconsecutive differences alpha_(s+1)-alpha_s: {[f'{d:.4f}' for d in diffs]}")

    s_vals = list(range(1, 7))
    a_vals = [alphas[s] for s in s_vals]
    ms, ma = statistics.mean(s_vals), statistics.mean(a_vals)
    num = sum((s - ms) * (a - ma) for s, a in zip(s_vals, a_vals))
    den = sum((s - ms) ** 2 for s in s_vals)
    lin_slope = num / den
    lin_intercept = ma - lin_slope * ms
    predicted = [lin_intercept + lin_slope * s for s in s_vals]
    residuals = [a - p for a, p in zip(a_vals, predicted)]
    ss_res = sum(r**2 for r in residuals)
    ss_tot = sum((a - ma) ** 2 for a in a_vals)
    r2 = 1 - ss_res / ss_tot if ss_tot else float("nan")
    print(f"\nLinear fit alpha_s ~= {lin_intercept:.4f} + {lin_slope:.4f}*s, R^2={r2:.5f}")

    implied_theta = {s: (alphas[s] - alphas[1]) / (s - 1) for s in range(2, 7)}
    print("\nimplied (1-theta) per pair (constant would confirm linearity):")
    for s, v in implied_theta.items():
        print(f"  s={s}: {v:.4f}")

    diff_monotone_decreasing = all(diffs[i] > diffs[i + 1] for i in range(len(diffs) - 1))
    print(f"\nDifferences strictly decreasing (concave, NOT linear): {diff_monotone_decreasing}")

    # Permutation p-value (reviewer suggestion, point 39): under the null that the 5
    # differences are exchangeable (no trend), what's the chance of observing them in
    # perfectly sorted decreasing order? Exact: 1/5! for a full strict sort, computed by
    # brute-force enumeration (not hardcoded) so it's correct even if a future run has ties.
    n_diffs = len(diffs)
    n_sorted_perms = sum(
        1
        for perm in itertools.permutations(diffs)
        if all(perm[i] > perm[i + 1] for i in range(n_diffs - 1))
    )
    total_perms = math.factorial(n_diffs)
    p_value_fully_sorted = n_sorted_perms / total_perms
    print(
        f"\nPermutation p-value (exact chance of a fully-sorted-decreasing sequence under "
        f"exchangeability null): {p_value_fully_sorted:.5f} ({n_sorted_perms}/{total_perms})"
    )

    result = {
        "n_values": ns,
        "alpha_s": alphas,
        "consecutive_diffs": diffs,
        "linear_fit": {
            "intercept": lin_intercept,
            "slope": lin_slope,
            "r2": r2,
            "residuals": residuals,
        },
        "implied_one_minus_theta_per_pair": implied_theta,
        "diffs_strictly_decreasing": diff_monotone_decreasing,
        "permutation_p_value_fully_sorted": p_value_fully_sorted,
    }
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "alpha_s_linearity_check.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    return result


if __name__ == "__main__":
    run()
