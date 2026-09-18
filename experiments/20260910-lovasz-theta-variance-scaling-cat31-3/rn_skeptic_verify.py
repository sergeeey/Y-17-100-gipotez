"""Independently re-verify the skeptic's three KILL findings on the R_n
revival analysis:
1. Direct n*Var(X_n) exponent fit (should be ~-0.04, supporting C0).
2. Corrected log-SE from BCa CI directly (equivariant), not delta method.
3. Leave-one-out on the corrected fit.
"""

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy import stats

EXP_DIR = Path(__file__).resolve().parent


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fc = _load_module("first_chaos_canonical", EXP_DIR / "check_first_chaos_decomposition_large_n.py")
compute_decomposition = fc.compute_decomposition

with open(EXP_DIR / "metrics" / "rn_revival_pooled_raw.json") as f:
    raw = json.load(f)
with open(EXP_DIR / "metrics" / "rn_revival_analysis_result.json") as f:
    prior = json.load(f)

TARGET_N = [509, 1021, 2039]
pooled = {int(k): (np.array(v["x"]), np.array(v["q"])) for k, v in raw.items()}


def weighted_fit_b(ns, ys, se_logs):
    x = np.log(np.array(ns, dtype=float))
    y = np.log(np.array(ys))
    w = 1.0 / np.array(se_logs) ** 2
    X = np.column_stack([np.ones_like(x), x])
    W = np.diag(w)
    cov = np.linalg.inv(X.T @ W @ X)
    beta = cov @ X.T @ W @ y
    se_b = np.sqrt(cov[1, 1])
    return float(beta[1]), float(se_b)


# --- Part 1: direct n*Var exponent fit ---
print("=== Part 1: direct n*Var(X_n) fit (KILL #1 check) ===")
n_var = {}
for n in TARGET_N:
    dec = compute_decomposition(*pooled[n], n)
    n_var[n] = dec["n_times_w1_hat"] + dec["n_times_r_n_hat"]
    print(
        f"  n={n}: n*W1={dec['n_times_w1_hat']:.4f}  n*R_n={dec['n_times_r_n_hat']:.4f}  "
        f"n*Var={n_var[n]:.4f}"
    )


# BCa CI for n*Var directly (reuse the same BCa machinery)
def bca_ci(x, q, n, statistic_fn, n_boot=5000, alpha=0.05, seed=0):
    rng = np.random.default_rng(seed)
    reps = len(x)
    theta_hat = statistic_fn(x, q, n)
    boot_vals = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, reps, size=reps)
        boot_vals[b] = statistic_fn(x[idx], q[idx], n)
    prop_less = np.clip(np.mean(boot_vals < theta_hat), 1e-6, 1 - 1e-6)
    z0 = stats.norm.ppf(prop_less)
    jack_vals = np.empty(reps)
    for i in range(reps):
        mask = np.ones(reps, dtype=bool)
        mask[i] = False
        jack_vals[i] = statistic_fn(x[mask], q[mask], n)
    jack_mean = jack_vals.mean()
    num = np.sum((jack_mean - jack_vals) ** 3)
    den = 6.0 * (np.sum((jack_mean - jack_vals) ** 2) ** 1.5)
    a_hat = num / den if den != 0 else 0.0
    z_lo, z_hi = stats.norm.ppf(0.025), stats.norm.ppf(0.975)

    def adj(za):
        p = z0 + za
        return stats.norm.cdf(z0 + p / (1 - a_hat * p))

    p_lo, p_hi = np.clip(adj(z_lo), 1e-4, 1 - 1e-4), np.clip(adj(z_hi), 1e-4, 1 - 1e-4)
    lo, hi = np.percentile(boot_vals, 100 * p_lo), np.percentile(boot_vals, 100 * p_hi)
    return theta_hat, lo, hi


def stat_n_var(x, q, n):
    d = compute_decomposition(x, q, n)
    return d["n_times_w1_hat"] + d["n_times_r_n_hat"]


var_bca = {}
for n in TARGET_N:
    x, q = pooled[n]
    theta_hat, lo, hi = bca_ci(x, q, n, stat_n_var, n_boot=5000, seed=n + 100)
    var_bca[n] = (theta_hat, lo, hi)
    print(f"  n={n}: BCa 95% CI for n*Var = [{lo:.4f},{hi:.4f}]")

# fit using EQUIVARIANT log-SE (correct approach, per skeptic's KILL #2)
se_log_var = {n: (np.log(var_bca[n][2]) - np.log(var_bca[n][1])) / (2 * 1.96) for n in TARGET_N}
b_var, se_b_var = weighted_fit_b(
    TARGET_N, [n_var[n] for n in TARGET_N], [se_log_var[n] for n in TARGET_N]
)
ci_var = [b_var - 1.96 * se_b_var, b_var + 1.96 * se_b_var]
print(f"\n  b_Var (equivariant log-SE) = {b_var:.4f} +/- {se_b_var:.4f}  95% CI={ci_var}")

# --- Part 2: corrected n*R_n fit using equivariant log-SE from BCa ---
print("\n=== Part 2: n*R_n fit with CORRECTED equivariant log-SE (KILL #2 check) ===")
bca_rn = prior["bca_n_rn"]
se_log_rn = {}
n_rn_val = {}
for n_str, v in bca_rn.items():
    n = int(n_str)
    lo, hi = v["ci_lo"], v["ci_hi"]
    theta = v["n_times_r_n"]
    se_log_rn[n] = (np.log(hi) - np.log(lo)) / (2 * 1.96)
    n_rn_val[n] = theta
    print(
        f"  n={n}: n*R_n={theta:.4f}  delta-method se/y={(hi - lo) / (2 * 1.96) / theta:.4f}  "
        f"equivariant log-SE={se_log_rn[n]:.4f}"
    )

b_rn_corrected, se_b_rn_corrected = weighted_fit_b(
    TARGET_N, [n_rn_val[n] for n in TARGET_N], [se_log_rn[n] for n in TARGET_N]
)
ci_rn_corrected = [
    b_rn_corrected - 1.96 * se_b_rn_corrected,
    b_rn_corrected + 1.96 * se_b_rn_corrected,
]
print(
    f"\n  b_R_n (corrected) = {b_rn_corrected:.4f} +/- {se_b_rn_corrected:.4f}  "
    f"95% CI={ci_rn_corrected}"
)

# --- Part 3: leave-one-out on corrected n*R_n fit ---
print("\n=== Part 3: leave-one-out on corrected n*R_n fit (KILL #3 check) ===")
for excl in TARGET_N:
    ns2 = [n for n in TARGET_N if n != excl]
    y2 = [n_rn_val[n] for n in ns2]
    se2 = [se_log_rn[n] for n in ns2]
    b2, se_b2 = weighted_fit_b(ns2, y2, se2)
    ci2 = [b2 - 1.96 * se_b2, b2 + 1.96 * se_b2]
    print(f"  exclude n={excl}: b={b2:.4f}+/-{se_b2:.4f}  CI={ci2}")

out = {
    "n_var": n_var,
    "var_bca": var_bca,
    "b_var": b_var,
    "se_b_var": se_b_var,
    "ci_var": ci_var,
    "b_rn_corrected": b_rn_corrected,
    "se_b_rn_corrected": se_b_rn_corrected,
    "ci_rn_corrected": ci_rn_corrected,
}
Path(EXP_DIR / "metrics" / "rn_skeptic_verify_result.json").write_text(
    json.dumps(out, indent=2, default=str)
)
