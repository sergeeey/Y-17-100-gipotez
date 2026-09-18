"""
H-CAT31-3 PARK revival for C1/C2/C3: analysis of the pooled (old+new, equalized
to ~800-1000 reps) R_n/lambda_n data at n=509,1021,2039.

Per Point 95's own revival plan (decision.md), steps 3-4:
  3. Reformulate as a 95% CI on the scaling exponent b in n*R_n ~ n^b, via a
     PROPER bootstrap (not normal-approximation), pre-registered stopping
     rule: this IS the stopping point (rep counts already equalized to the
     named target), no further reps regardless of outcome.
  4. Use a bootstrap-based (BCa or studentized) CI for n*R_n itself, since it
     sits near a boundary (0) and is visibly skewed (per the skeptic's own
     note in Point 95).

PRE-REGISTERED DECISION RULE (restated from rn_revival_combined.py, written
BEFORE this analysis was run):
  - LEAD (supports C1+C2): 95% CI on b excludes 1 AND is close to/consistent
    with 0.
  - CONCERNING (supports C3): CI excludes 0 and is close to/consistent with 1.
  - STILL INCONCLUSIVE: CI contains both 0 and 1.
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

TARGET_N = [509, 1021, 2039]
pooled = {}
for n_str, d in raw.items():
    n = int(n_str)
    pooled[n] = (np.array(d["x"]), np.array(d["q"]))

print("=== Point estimates on pooled data ===")
point_est = {}
for n in TARGET_N:
    x, q = pooled[n]
    dec = compute_decomposition(x, q, n)
    point_est[n] = dec
    print(
        f"n={n:5d} reps={len(x):4d}: lambda_n={dec['lambda_n_hat']:.4f}  "
        f"n*W1={dec['n_times_w1_hat']:.4f}  n*R_n={dec['n_times_r_n_hat']:.4f}"
    )


# --- BCa bootstrap for n*R_n at each n individually ---
def bca_ci(x, q, n, statistic_fn, n_boot=5000, alpha=0.05, seed=0):
    """BCa bootstrap CI. statistic_fn(x,q,n) -> scalar."""
    rng = np.random.default_rng(seed)
    reps = len(x)
    theta_hat = statistic_fn(x, q, n)

    # bootstrap replicates
    boot_vals = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, reps, size=reps)
        boot_vals[b] = statistic_fn(x[idx], q[idx], n)

    # bias-correction z0
    prop_less = np.mean(boot_vals < theta_hat)
    prop_less = np.clip(prop_less, 1e-6, 1 - 1e-6)
    z0 = stats.norm.ppf(prop_less)

    # acceleration via jackknife
    jack_vals = np.empty(reps)
    for i in range(reps):
        mask = np.ones(reps, dtype=bool)
        mask[i] = False
        jack_vals[i] = statistic_fn(x[mask], q[mask], n)
    jack_mean = jack_vals.mean()
    num = np.sum((jack_mean - jack_vals) ** 3)
    den = 6.0 * (np.sum((jack_mean - jack_vals) ** 2) ** 1.5)
    a_hat = num / den if den != 0 else 0.0

    z_alpha_lo = stats.norm.ppf(alpha / 2)
    z_alpha_hi = stats.norm.ppf(1 - alpha / 2)

    def adjusted_percentile(z_alpha):
        num_p = z0 + z_alpha
        denom_p = 1 - a_hat * num_p
        p = stats.norm.cdf(z0 + num_p / denom_p)
        return p

    p_lo = adjusted_percentile(z_alpha_lo)
    p_hi = adjusted_percentile(z_alpha_hi)
    p_lo = np.clip(p_lo, 0.0001, 0.9999)
    p_hi = np.clip(p_hi, 0.0001, 0.9999)

    lo = np.percentile(boot_vals, 100 * p_lo)
    hi = np.percentile(boot_vals, 100 * p_hi)
    return theta_hat, lo, hi, boot_vals, z0, a_hat


def stat_n_rn(x, q, n):
    return compute_decomposition(x, q, n)["n_times_r_n_hat"]


def stat_lambda(x, q, n):
    return compute_decomposition(x, q, n)["lambda_n_hat"]


print("\n=== BCa bootstrap CI for n*R_n (5000 reps each) ===")
bca_results = {}
for n in TARGET_N:
    x, q = pooled[n]
    theta_hat, lo, hi, boot_vals, z0, a_hat = bca_ci(x, q, n, stat_n_rn, n_boot=5000, seed=n + 1)
    bca_results[n] = {"n_times_r_n": theta_hat, "ci_lo": lo, "ci_hi": hi, "z0": z0, "a_hat": a_hat}
    print(
        f"n={n:5d}: n*R_n={theta_hat:.4f}  BCa 95% CI=[{lo:.4f},{hi:.4f}]  "
        f"z0={z0:.4f}  a_hat={a_hat:.4f}"
    )


# --- Nested bootstrap for the exponent b in n*R_n ~ n^b ---
# Weighted fit using BCa-derived SE as the per-point uncertainty (symmetrized
# from the BCa CI half-width, for use in the WLS weight only -- the exponent's
# OWN CI comes from the nested bootstrap below, not from this WLS SE).
def weighted_fit_b(ns, ys, ses):
    x = np.log(np.array(ns, dtype=float))
    y = np.log(np.array(ys))
    se_log = np.array(ses) / np.array(ys)
    w = 1.0 / se_log**2
    X = np.column_stack([np.ones_like(x), x])
    W = np.diag(w)
    XtW = X.T @ W
    cov = np.linalg.inv(XtW @ X)
    beta = cov @ XtW @ y
    return float(beta[1])  # slope b


ses_for_weight = {
    n: (bca_results[n]["ci_hi"] - bca_results[n]["ci_lo"]) / (2 * 1.96) for n in TARGET_N
}
point_b = weighted_fit_b(
    TARGET_N,
    [point_est[n]["n_times_r_n_hat"] for n in TARGET_N],
    [ses_for_weight[n] for n in TARGET_N],
)
print(f"\nPoint estimate of b (weighted fit, BCa-derived SE as weights): {point_b:.4f}")

print("\n=== Nested bootstrap for b's own CI (2000 outer reps) ===")
N_OUTER = 2000
rng_outer = np.random.default_rng(999)
b_boot = np.empty(N_OUTER)
for k in range(N_OUTER):
    n_rn_k = {}
    for n in TARGET_N:
        x, q = pooled[n]
        idx = rng_outer.integers(0, len(x), size=len(x))
        n_rn_k[n] = compute_decomposition(x[idx], q[idx], n)["n_times_r_n_hat"]
    # guard against non-positive resampled n*R_n (can't log) -- use the SAME
    # weighted fit machinery but skip degenerate resamples (extremely rare
    # given the point estimates are all well above zero)
    vals = [n_rn_k[n] for n in TARGET_N]
    if min(vals) <= 0:
        b_boot[k] = np.nan
        continue
    b_boot[k] = weighted_fit_b(TARGET_N, vals, [ses_for_weight[n] for n in TARGET_N])

valid = ~np.isnan(b_boot)
n_valid = valid.sum()
b_boot_valid = b_boot[valid]
ci_lo, ci_hi = np.percentile(b_boot_valid, [2.5, 97.5])
print(f"Valid outer bootstrap reps: {n_valid}/{N_OUTER}")
print(f"Percentile 95% CI on b: [{ci_lo:.4f}, {ci_hi:.4f}]")
print(
    f"Point estimate b={point_b:.4f}, bootstrap mean={b_boot_valid.mean():.4f}, "
    f"median={np.median(b_boot_valid):.4f}"
)

# BCa for b itself
z0_b = stats.norm.ppf(np.clip(np.mean(b_boot_valid < point_b), 1e-6, 1 - 1e-6))
print(f"z0 for b's own bootstrap distribution: {z0_b:.4f} (skew indicator)")

out = {
    "point_estimates": {n: point_est[n] for n in TARGET_N},
    "bca_n_rn": bca_results,
    "point_b": point_b,
    "b_bootstrap_ci95_percentile": [float(ci_lo), float(ci_hi)],
    "b_bootstrap_mean": float(b_boot_valid.mean()),
    "b_bootstrap_median": float(np.median(b_boot_valid)),
    "b_bootstrap_z0": float(z0_b),
    "n_valid_outer_boot": int(n_valid),
}
Path(EXP_DIR / "metrics" / "rn_revival_analysis_result.json").write_text(
    json.dumps(out, indent=2, default=str)
)
print("\nWritten to metrics/rn_revival_analysis_result.json")
