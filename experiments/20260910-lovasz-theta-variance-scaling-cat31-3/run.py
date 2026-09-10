"""H-CAT31-3 -- variance scaling of log(theta(G)/sqrt(n)) for random dense circulant graphs.

Direct follow-up from the deep external novelty audit's own Track 1 finding
(Var(log(theta/sqrt(n))) ~ n^-0.96 on H-CAT31-1's original 9-point sweep). Tests
whether the exponent is consistent with exactly -1 on a wider n range with more
replicates. Reuses `theta_via_lp`/`sample_circulant_neighbors` from H-CAT31-1's
own run.py UNCHANGED (Minimal Relaxation Rule) -- only the sweep design changes.
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"

RNG_SEED_BASE = 331000  # distinct base from H-CAT31-1 (31000) / H-CAT31-2, no seed collision


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("h_cat31_3_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
theta_via_lp = h_cat31_1.theta_via_lp

SWEEP_N_REPS = [
    (32, 300),
    (64, 300),
    (128, 300),
    (256, 250),
    (512, 200),
    (1024, 150),
    (1536, 100),
    (2048, 80),
    (3000, 40),
]

N_BOOTSTRAP = 2000
BOOTSTRAP_SEED = 991


def substrate_gate_checks() -> dict:
    """Cheap re-verification of theta_via_lp against the SAME two closed-form checks
    H-CAT31-1 already used, before trusting any new large-n solve this experiment runs."""
    # theta(C_5) = sqrt(5) exactly -- C_5 is the circulant graph on 5 vertices with
    # offset {1,4} connected (the standard 5-cycle).
    c5 = np.zeros(5)
    c5[1] = 1.0
    c5[4] = 1.0
    theta_c5 = theta_via_lp(c5)
    c5_ok = bool(abs(theta_c5 - np.sqrt(5)) < 1e-6)

    # theta(G)*theta(Gbar) = n identity (Lovasz 1979, tight for vertex-transitive graphs) --
    # spot-check on a small random instance.
    n_check = 9
    c = sample_circulant_neighbors(n_check, 0.5, 770)
    c_bar = np.zeros(n_check)
    half = (n_check - 1) // 2
    for k in range(1, half + 1):
        c_bar[k] = 1.0 - c[k]
        c_bar[n_check - k] = 1.0 - c[n_check - k]
    theta_g = theta_via_lp(c)
    theta_gbar = theta_via_lp(c_bar)
    product = theta_g * theta_gbar
    identity_ok = bool(abs(product - n_check) < 1e-4)

    return {
        "theta_c5": theta_c5,
        "theta_c5_expected": float(np.sqrt(5)),
        "c5_check_passed": c5_ok,
        "theta_g_times_gbar": product,
        "n_check": n_check,
        "identity_check_passed": identity_ok,
        "substrate_ready": c5_ok and identity_ok,
    }


def negative_control_zero_variance() -> dict:
    """At p=0 (empty graph) theta is degenerate (=1, the single-vertex clique bound via LP
    on a graph with no edge constraints beyond x_0=1) for EVERY seed -- Var(log(...)) must
    be exactly 0. Confirms the variance-estimation code can register zero, not just noise."""
    n = 16
    vals = []
    for seed in range(5):
        c = np.zeros(n)  # p=0: no edges at all
        theta = theta_via_lp(c)
        vals.append(theta)
    vals = np.array(vals)
    x = np.log(vals / np.sqrt(n))
    var_x = float(np.var(x, ddof=1)) if len(x) > 1 else 0.0
    return {
        "n": n,
        "theta_values": vals.tolist(),
        "var_log_ratio": var_x,
        "all_identical": bool(np.allclose(vals, vals[0])),
        "control_passed": bool(var_x < 1e-10),
    }


def bootstrap_var_ci(x: np.ndarray, n_boot: int, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    n = len(x)
    boot_vars = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot_vars[b] = np.var(x[idx], ddof=1)
    lo, hi = np.percentile(boot_vars, [2.5, 97.5])
    return float(lo), float(hi)


def run_sweep() -> list[dict]:
    rows = []
    for n, reps in SWEEP_N_REPS:
        t0 = time.time()
        thetas = np.empty(reps)
        for i in range(reps):
            seed = RNG_SEED_BASE + n * 1000 + i
            c = sample_circulant_neighbors(n, 0.5, seed)
            thetas[i] = theta_via_lp(c)
        elapsed = time.time() - t0

        ratio = thetas / np.sqrt(n)
        x = np.log(ratio)
        mean_x = float(x.mean())
        var_x = float(np.var(x, ddof=1))
        se_var_x_relative = float(np.sqrt(2.0 / (reps - 1))) if reps > 1 else float("nan")
        ci_lo, ci_hi = bootstrap_var_ci(x, N_BOOTSTRAP, BOOTSTRAP_SEED + n)

        rows.append(
            {
                "n": n,
                "n_reps": reps,
                "mean_theta_over_sqrt_n": float(ratio.mean()),
                "mean_log_ratio": mean_x,
                "var_log_ratio": var_x,
                "var_log_ratio_relative_se": se_var_x_relative,
                "var_log_ratio_bootstrap_ci95": [ci_lo, ci_hi],
                "elapsed_seconds": elapsed,
            }
        )
        print(
            f"n={n:5d} reps={reps:4d} mean_ratio={ratio.mean():.5f} "
            f"var_log_ratio={var_x:.6e} CI=[{ci_lo:.3e},{ci_hi:.3e}] "
            f"elapsed={elapsed:.1f}s",
            flush=True,
        )
    return rows


def fit_exponent(rows: list[dict]) -> dict:
    ns = np.array([r["n"] for r in rows], dtype=float)
    var_x = np.array([r["var_log_ratio"] for r in rows], dtype=float)
    log_n = np.log(ns)
    log_var = np.log(var_x)

    # Unweighted OLS
    slope_uw, intercept_uw = np.polyfit(log_n, log_var, 1)

    # Weighted OLS: weight by inverse variance of log(Var_hat), approximated via the
    # delta method from the bootstrap CI width (relative SE of Var_hat propagates to an
    # absolute SE on log(Var_hat) of roughly the same relative magnitude for the log transform).
    ci_widths = np.array(
        [
            (r["var_log_ratio_bootstrap_ci95"][1] - r["var_log_ratio_bootstrap_ci95"][0])
            for r in rows
        ]
    )
    log_var_se_approx = ci_widths / (2 * 1.96 * var_x)  # approx SE of log(var_x) via delta method
    weights = 1.0 / np.maximum(log_var_se_approx**2, 1e-12)

    # Weighted least squares via normal equations
    X = np.vstack([log_n, np.ones_like(log_n)]).T
    W = np.diag(weights)
    XtWX = X.T @ W @ X
    XtWy = X.T @ W @ log_var
    beta = np.linalg.solve(XtWX, XtWy)
    slope_w, intercept_w = beta[0], beta[1]

    # Standard error of weighted slope
    n_pts = len(ns)
    resid = log_var - X @ beta
    dof = n_pts - 2
    sigma2 = float((resid @ W @ resid) / dof) if dof > 0 else float("nan")
    cov = sigma2 * np.linalg.inv(XtWX)
    se_slope_w = float(np.sqrt(cov[0, 0]))
    t_crit = float(stats.t.ppf(0.975, dof)) if dof > 0 else float("nan")
    ci_lo_w = float(slope_w - t_crit * se_slope_w)
    ci_hi_w = float(slope_w + t_crit * se_slope_w)

    return {
        "unweighted_ols": {"slope": float(slope_uw), "intercept": float(intercept_uw)},
        "weighted_ols": {
            "slope": float(slope_w),
            "intercept": float(intercept_w),
            "slope_se": se_slope_w,
            "slope_ci95": [ci_lo_w, ci_hi_w],
            "dof": dof,
        },
        "ci_contains_minus_1": bool(ci_lo_w <= -1.0 <= ci_hi_w),
        "ci_excludes_minus_0_5": bool(not (ci_lo_w <= -0.5 <= ci_hi_w)),
        "ci_excludes_minus_2": bool(not (ci_lo_w <= -2.0 <= ci_hi_w)),
    }


def cmd_run() -> dict:
    substrate = substrate_gate_checks()
    if not substrate["substrate_ready"]:
        out = {
            "claim": "H-CAT31-3 -- variance scaling of log(theta/sqrt(n))",
            "status": "BLOCKED-INFRASTRUCTURE",
            "substrate_gate": substrate,
        }
        METRICS.mkdir(exist_ok=True)
        with open(METRICS / "run.json", "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, default=str)
        print(json.dumps(out, indent=2, default=str))
        return out

    neg_control = negative_control_zero_variance()

    sweep_rows = run_sweep()
    fit = fit_exponent(sweep_rows)

    if fit["ci_contains_minus_1"] and fit["ci_excludes_minus_0_5"] and fit["ci_excludes_minus_2"]:
        verdict = "CONFIRMED"
    elif fit["ci_contains_minus_1"]:
        verdict = "WEAKENED-INCONCLUSIVE"
    else:
        verdict = "REJECTED"

    out = {
        "claim": (
            "H-CAT31-3 -- variance scaling of log(theta(G)/sqrt(n)) "
            "for random dense circulant graphs"
        ),
        "substrate_gate": substrate,
        "negative_control": neg_control,
        "sweep": sweep_rows,
        "fit": fit,
        "verdict": verdict,
    }
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "run.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
