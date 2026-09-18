"""
C5: is g_n := E[theta(G_n)] - sqrt(n) = O(n^{-1/2})?

Per Point 94's own established inequality (decision.md:215-230, independently
re-verified there against all 9 sweep points): V_n <= 2*(E[theta]/sqrt(n)-1)
= 2*g_n/sqrt(n). If g_n=O(n^{-1/2}), then V_n=O(1/n) -- this is the C5 route
to the headline theorem C0.

This is a genuinely NEW test (not previously run in this project): fit the
scaling exponent of g_n vs n directly, using the project's own established
9-point sweep (metrics/run.json, n=32..3000), reusing the SAME weighted
power-law fit methodology (ppl_gate_pilot.py's weighted_power_law_fit)
already validated and used throughout this project for exponent CIs.

SE approximation, stated explicitly (delta method, not raw per-graph data --
run.json stores only mean_theta_over_sqrt_n and var_log_ratio=Var(X_n) per n,
not raw per-graph theta samples for this specific 9-point sweep): for ratio
close to 1 (true here, 0.995-1.073 across all 9 points), Var(ratio) ~=
Var(X_n) since X_n=log(ratio)~=ratio-1 for ratio near 1. So
SE(mean_ratio) ~= sqrt(Var(X_n)/n_reps), and SE(g_n) = sqrt(n)*SE(mean_ratio).

PRE-REGISTERED DECISION RULE (written before computing the fit):
  - LEAD (supports C5/C0): 95% CI on the exponent of |g_n| vs n is <= -0.5
    at its UPPER bound (i.e., excludes anything slower than n^{-1/2}) --
    or at minimum, is consistent with -0.5 and excludes 0 (no decay).
  - AGAINST C5: CI's upper bound stays clearly above -0.5 (decay is real but
    too slow), or excludes -0.5 entirely toward 0.
  - INCONCLUSIVE: CI straddles both -0.5 and a much shallower rate.
"""

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(".")


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ppl = _load_module("ppl_gate_pilot", HERE / "ppl_gate_pilot.py")
weighted_power_law_fit = ppl.weighted_power_law_fit

with open("metrics/run.json") as f:
    d = json.load(f)

rows = []
for r in d["sweep"]:
    n = r["n"]
    ratio = r["mean_theta_over_sqrt_n"]
    var_x = r["var_log_ratio"]
    n_reps = r["n_reps"]
    g_n = (ratio - 1.0) * np.sqrt(n)
    se_ratio = np.sqrt(var_x / n_reps)  # delta-method approx, ratio~=1+X_n near ratio=1
    se_g_n = np.sqrt(n) * se_ratio
    rows.append({"n": n, "n_reps": n_reps, "ratio": ratio, "g_n": g_n, "se_g_n": se_g_n})
    print(f"n={n:5d} reps={n_reps:4d} ratio={ratio:.6f} g_n={g_n:+.4f} se_g_n={se_g_n:.4f}")

# g_n changes sign (positive at small n, near/below zero at n=2048,3000) -- fit |g_n| vs n
# on the points where g_n is clearly positive and bounded away from the noise floor, per
# this project's own established practice of flagging low-power points rather than
# silently including sign-ambiguous ones in a log-log fit (log requires g_n>0).
print()
usable = [r for r in rows if r["g_n"] > r["se_g_n"]]  # g_n at least 1 SE above zero
excluded = [r for r in rows if r not in usable]
print(f"Usable points (g_n > 1 SE above 0): {[r['n'] for r in usable]}")
print(f"Excluded (g_n consistent with 0 or negative, cannot log-fit): {[r['n'] for r in excluded]}")

ns = [r["n"] for r in usable]
gs = [r["g_n"] for r in usable]
ses = [r["se_g_n"] for r in usable]
fit = weighted_power_law_fit(ns, gs, ses, "g_n")

print("\n=== Weighted power-law fit: log(g_n) = a + b*log(n) ===")
print(f"  n points used: {len(ns)}")
print(f"  slope_b = {fit['slope_b']:.4f} +/- {fit['slope_b_SE']:.4f}")
print(f"  95% CI = {fit['slope_b_95CI']}")
print(
    f"  delta_chi2 = {fit['delta_chi2_dof1']:.3f}, "
    f"p (vs flat, b=0) = {fit['delta_chi2_p_value']:.3f}"
)
print(f"  chi2_flat (dof={fit['chi2_flat_model_dof']}) = {fit['chi2_flat_model']:.3f}")
print(f"  chi2_power (dof={fit['chi2_power_law_model_dof']}) = {fit['chi2_power_law_model']:.3f}")

# also test against the specific target b=-0.5
b, se_b = fit["slope_b"], fit["slope_b_SE"]
z_vs_half = (b - (-0.5)) / se_b
print(
    f"\n  z-distance from target b=-0.5: {z_vs_half:.3f} (|z|<1.96 means -0.5 is inside the 95% CI)"
)

out = {"rows": rows, "usable_ns": ns, "fit": fit, "z_vs_neg_half": z_vs_half}
Path("c5_mean_gap_result.json").write_text(json.dumps(out, indent=2, default=str))
