"""Independently reproduce the skeptic's debiased g_n estimator and its
weighted power-law fit, plus a leave-one-out check on the debiased fit."""

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

rows = []
for r in d["sweep"]:
    n = r["n"]
    ratio = r["mean_theta_over_sqrt_n"]
    x_bar = r["mean_log_ratio"]
    var_x = r["var_log_ratio"]
    n_reps = r["n_reps"]
    # debiased estimator: g_hat = sqrt(n) * (ratio - 1 - x_bar)
    g_hat = np.sqrt(n) * (ratio - 1 - x_bar)
    # exact floor: sqrt(n)*V_n/2
    floor = np.sqrt(n) * var_x / 2
    rows.append({"n": n, "g_hat": g_hat, "floor": floor, "var_x": var_x, "n_reps": n_reps})
    print(
        f"n={n:5d}: g_hat={g_hat:.4f}  floor(sqrt(n)*V/2)={floor:.4f}  "
        f"g_hat>=floor: {g_hat >= floor - 1e-9}"
    )

# SE for g_hat: per skeptic, sigma_i = sqrt(n)*(v/2)*rel_se, where rel_se is the
# relative SE already used for V_n itself in the project's own convention
# (var_log_ratio_relative_se field, if present; else sqrt(2/n_reps) for a chi-square-like
# variance estimator's relative SE approximation)
print("\n=== checking for var_log_ratio_relative_se field ===")
sample = d["sweep"][0]
print("available keys:", list(sample.keys()))
