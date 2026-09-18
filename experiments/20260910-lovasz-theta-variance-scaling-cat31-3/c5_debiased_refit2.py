import importlib.util
import json
from pathlib import Path

import numpy as np

EXP_DIR = Path(__file__).resolve().parent


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ppl = _load_module("ppl_gate_pilot", EXP_DIR / "ppl_gate_pilot.py")
weighted_power_law_fit = ppl.weighted_power_law_fit

with open(EXP_DIR / "metrics" / "run.json") as f:
    d = json.load(f)

ns, g_hats, se_g_hats = [], [], []
for r in d["sweep"]:
    n = r["n"]
    ratio = r["mean_theta_over_sqrt_n"]
    x_bar = r["mean_log_ratio"]
    var_x = r["var_log_ratio"]
    rel_se = r["var_log_ratio_relative_se"]
    g_hat = np.sqrt(n) * (ratio - 1 - x_bar)
    floor = np.sqrt(n) * var_x / 2
    se_g = np.sqrt(n) * (var_x / 2) * rel_se
    ns.append(n)
    g_hats.append(g_hat)
    se_g_hats.append(se_g)
    print(f"n={n:5d}: g_hat={g_hat:.4f}  se={se_g:.4f}  floor={floor:.4f}  rel_se={rel_se:.4f}")

fit = weighted_power_law_fit(ns, g_hats, se_g_hats, "g_hat")
print("\n=== Full 9-point weighted fit on debiased g_hat ===")
print(f"  b={fit['slope_b']:.4f} +/- {fit['slope_b_SE']:.4f}  CI={fit['slope_b_95CI']}")
print(
    f"  chi2_power={fit['chi2_power_law_model']:.3f} (dof={fit['chi2_power_law_model_dof']})  "
    f"delta_chi2_p={fit['delta_chi2_p_value']:.4f}"
)
z0 = fit["slope_b"] / fit["slope_b_SE"]
zhalf = (fit["slope_b"] - (-0.5)) / fit["slope_b_SE"]
print(f"  z vs b=0: {z0:.3f}   z vs b=-0.5: {zhalf:.3f}")

print("\n=== Leave-one-out on the debiased fit ===")
for excl in ns:
    ns2 = [n for n in ns if n != excl]
    g2 = [g_hats[i] for i, n in enumerate(ns) if n != excl]
    se2 = [se_g_hats[i] for i, n in enumerate(ns) if n != excl]
    fit2 = weighted_power_law_fit(ns2, g2, se2, "g_hat_loo")
    z2 = (fit2["slope_b"] - (-0.5)) / fit2["slope_b_SE"]
    print(
        f"  excl n={excl:5d}: b={fit2['slope_b']:.4f}+/-{fit2['slope_b_SE']:.4f}  "
        f"z_vs_-0.5={z2:.3f}"
    )

# also compare against V_n's own stored fit exponent, if present
print("\n=== V_n's own already-stored fit, for comparison (KILL#1 check: b_g should = 0.5+b_V) ===")
if "fit" in d or "weighted_ols" in d:
    print("top-level keys:", list(d.keys()))
