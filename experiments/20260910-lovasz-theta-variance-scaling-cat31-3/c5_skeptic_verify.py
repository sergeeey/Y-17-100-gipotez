import json
from pathlib import Path

import numpy as np
from sympy import isprime

HERE = Path(__file__).resolve().parent

with open(HERE / "metrics" / "run.json") as f:
    d = json.load(f)

print("=== Gate 1: primality of the 9 sweep n values ===")
for r in d["sweep"]:
    n = r["n"]
    print(f"  n={n}: prime={isprime(n)}  factorization hint: {n}")

print(
    "\n=== Check: is mean_theta_over_sqrt_n the arithmetic mean of ratio, "
    "or exp(mean_log_ratio)? ==="
)
for r in d["sweep"]:
    n = r["n"]
    ratio = r["mean_theta_over_sqrt_n"]
    mean_log = r.get("mean_log_ratio")
    if mean_log is not None:
        exp_mean_log = np.exp(mean_log)
        print(
            f"  n={n}: mean_theta_over_sqrt_n={ratio:.6f}  exp(mean_log_ratio)={exp_mean_log:.6f}  "
            f"mean_log_ratio={mean_log:.6f}  MATCH_exp={abs(ratio - exp_mean_log) < 1e-6}"
        )
    else:
        print(f"  n={n}: NO mean_log_ratio field found. Available keys: {list(r.keys())}")
