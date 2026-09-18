"""
C4 (K_n=O(1)) history check, per user's own instruction: run the SAME n=127-
exclusion robustness check on K_n's own 4-point weighted power-law fit that
Point 76 (decision.md) already ran for J_n -- flagged in Point 76's own text
as NOT yet done for K_n ("K_n's non-growth finding is reinforced (not run
through the same leverage check here...)").

Reuses ppl_gate_pilot.py's own weighted_power_law_fit function UNCHANGED
(read-only import), and the raw K_n/K_n_SE values already stored in
metrics/ppl_gate_pilot.json (no new LP computation).
"""

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ppl = _load_module("ppl_gate_pilot", HERE / "ppl_gate_pilot.py")
weighted_power_law_fit = ppl.weighted_power_law_fit

with open("metrics/ppl_gate_pilot.json") as f:
    d = json.load(f)

summaries = {s["n"]: s for s in d["summaries"]}
all_ns = [127, 509, 1021, 2039]

# --- reproduce the stored 4-point fit exactly, as a sanity check ---
ns4 = all_ns
kn4 = [summaries[n]["n2E_delta2_K_n"] for n in ns4]
kn4_se = [summaries[n]["K_n_SE"] for n in ns4]
fit4 = weighted_power_law_fit(ns4, kn4, kn4_se, "K_n")
stored = d["power_law_fit_Kn"]
print("=== Sanity check: reproduce stored 4-point K_n fit ===")
print(f"  reproduced slope_b={fit4['slope_b']:.6f}  vs stored {stored['slope_b']:.6f}")
print(f"  reproduced CI={fit4['slope_b_95CI']}  vs stored {stored['slope_b_95CI']}")
assert abs(fit4["slope_b"] - stored["slope_b"]) < 1e-9, "MISMATCH -- do not trust further output"
print("  MATCH -- proceeding with the leverage check.\n")

# --- leverage decomposition (same style as Point 76's own J_n check) ---
x = np.log(np.array(ns4, dtype=float))
y = np.log(np.array(kn4, dtype=float))
rel_se = np.array(kn4_se) / np.array(kn4)
w = 1.0 / rel_se**2
x_bar_w = np.sum(w * x) / np.sum(w)
dx = x - x_bar_w
y_bar_w = np.sum(w * y) / np.sum(w)
dy = y - y_bar_w
numerator_terms = w * dx * dy
denominator_terms = w * dx**2
print("=== Leverage decomposition (Point 76's own style, applied to K_n) ===")
for i, n in enumerate(ns4):
    print(
        f"  n={n:5d}: {100 * numerator_terms[i] / numerator_terms.sum():.1f}% of numerator, "
        f"{100 * denominator_terms[i] / denominator_terms.sum():.1f}% of denominator"
    )

# --- refit excluding n=127 ---
ns3 = [509, 1021, 2039]
kn3 = [summaries[n]["n2E_delta2_K_n"] for n in ns3]
kn3_se = [summaries[n]["K_n_SE"] for n in ns3]
fit3 = weighted_power_law_fit(ns3, kn3, kn3_se, "K_n_excl127")

print("\n=== K_n fit excluding n=127 (509,1021,2039 only) ===")
print(f"  slope_b = {fit3['slope_b']:.4f} +/- {fit3['slope_b_SE']:.4f}")
print(f"  95% CI = {fit3['slope_b_95CI']}")
print(f"  delta_chi2 = {fit3['delta_chi2_dof1']:.3f}, p = {fit3['delta_chi2_p_value']:.3f}")
print(f"  chi2_flat (dof={fit3['chi2_flat_model_dof']}) = {fit3['chi2_flat_model']:.3f}")

print("\n=== Comparison ===")
print(
    f"  4-point (incl. n=127): b={fit4['slope_b']:.4f}+/-{fit4['slope_b_SE']:.4f}, "
    f"CI={fit4['slope_b_95CI']}, p={fit4['delta_chi2_p_value']:.3f}"
)
print(
    f"  3-point (excl. n=127): b={fit3['slope_b']:.4f}+/-{fit3['slope_b_SE']:.4f}, "
    f"CI={fit3['slope_b_95CI']}, p={fit3['delta_chi2_p_value']:.3f}"
)

out = {
    "fit4_reproduced": fit4,
    "fit3_excl127": fit3,
    "leverage_pct_numerator": {
        str(n): float(100 * numerator_terms[i] / numerator_terms.sum()) for i, n in enumerate(ns4)
    },
    "leverage_pct_denominator": {
        str(n): float(100 * denominator_terms[i] / denominator_terms.sum())
        for i, n in enumerate(ns4)
    },
}
Path("kn_leverage_check_result.json").write_text(json.dumps(out, indent=2))
