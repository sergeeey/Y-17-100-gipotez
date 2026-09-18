"""Independently re-verify the skeptic's claims about the K_n leverage check:
1. Full leave-one-out (all 4 exclusions, not just n=127).
2. Hat-leverage values h_ii.
3. The "78% growth needed for significance" foreordained-power claim.
4. The n=8191 additional-point SE projection.
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

with open("metrics/ppl_gate_pilot.json") as f:
    d = json.load(f)
summaries = {s["n"]: s for s in d["summaries"]}
all_ns = [127, 509, 1021, 2039]
kn = {n: summaries[n]["n2E_delta2_K_n"] for n in all_ns}
kn_se = {n: summaries[n]["K_n_SE"] for n in all_ns}

print("=== Full leave-one-out ===")
for excl in all_ns:
    ns = [n for n in all_ns if n != excl]
    y = [kn[n] for n in ns]
    se = [kn_se[n] for n in ns]
    fit = weighted_power_law_fit(ns, y, se, "K_n")
    print(
        f"  exclude n={excl:5d}: b={fit['slope_b']:.4f}+/-{fit['slope_b_SE']:.4f}  "
        f"CI={fit['slope_b_95CI']}  p={fit['delta_chi2_p_value']:.3f}"
    )

print("\n=== Hat-leverage h_ii for the FULL 4-point fit ===")
x = np.log(np.array(all_ns, dtype=float))
rel_se = np.array([kn_se[n] / kn[n] for n in all_ns])
w = 1.0 / rel_se**2
X = np.column_stack([np.ones_like(x), x])
W = np.diag(w)
# hat matrix H = X (X'WX)^-1 X' W  ; leverage h_ii = H[i,i]
XtWX_inv = np.linalg.inv(X.T @ W @ X)
H = X @ XtWX_inv @ X.T @ W
h_ii = np.diag(H)
for n, h in zip(all_ns, h_ii):
    print(f"  n={n:5d}: h_ii={h:.4f}")
print(f"  sum(h_ii) = {h_ii.sum():.4f} (should equal 2, the number of parameters)")

print("\n=== Foreordained-power check: growth needed for 3-point (excl-127) significance ===")
ns3 = [509, 1021, 2039]
y3 = [kn[n] for n in ns3]
se3 = [kn_se[n] for n in ns3]
fit3 = weighted_power_law_fit(ns3, y3, se3, "K_n_excl127")
se_b3 = fit3["slope_b_SE"]
threshold_b = 1.96 * se_b3
# required K_2039/K_509 ratio for b=threshold_b: ratio = (2039/509)^threshold_b
required_ratio = (2039 / 509) ** threshold_b
observed_ratio = kn[2039] / kn[509]
print(f"  SE_b (3pt, excl 127) = {se_b3:.4f}  =>  significance threshold |b| > {threshold_b:.4f}")
print(f"  required K_2039/K_509 ratio for that threshold: {required_ratio:.3f}")
print(f"  observed K_2039/K_509 ratio: {observed_ratio:.3f}")

print("\n=== Projected SE_b if one point at n~=8191 (500 reps, same relative SE ~10%) is added ===")
n_new = 8191
rel_se_new = 0.10  # matching the observed ~10% relative SE at existing points
all_ns_ext = [*all_ns, n_new]
x_ext = np.log(np.array(all_ns_ext, dtype=float))
rel_se_ext = np.array([*(kn_se[n] / kn[n] for n in all_ns), rel_se_new])
w_ext = 1.0 / rel_se_ext**2
x_bar_ext = np.sum(w_ext * x_ext) / np.sum(w_ext)
dx_ext = x_ext - x_bar_ext
sum_w_dx2_ext = np.sum(w_ext * dx_ext**2)
se_b_ext = 1.0 / np.sqrt(sum_w_dx2_ext)
print(f"  Sum(w*dx^2) with n=8191 added: {sum_w_dx2_ext:.1f}  =>  projected SE_b = {se_b_ext:.4f}")

# compare to doubling reps at all 4 existing points (SE halves at each => rel_se/sqrt(2))
rel_se_doubled = rel_se / np.sqrt(2)
w_doubled = 1.0 / rel_se_doubled**2
x_bar_d = np.sum(w_doubled * x) / np.sum(w_doubled)
dx_d = x - x_bar_d
sum_w_dx2_d = np.sum(w_doubled * dx_d**2)
se_b_doubled = 1.0 / np.sqrt(sum_w_dx2_d)
print(f"  Projected SE_b if reps DOUBLED at all 4 existing points instead: {se_b_doubled:.4f}")
