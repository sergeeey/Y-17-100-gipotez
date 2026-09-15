"""Point 54B: susceptibility (`lambda_n`) scaling, run ONLY after Point 54A's identity audit
passed at every tested n (check_lambda_identity_audit.py, overall_status=PASS, max|z|=1.78) --
per the user's own proposed protocol, this analysis was frozen until that gate cleared.

Why this matters more than kappa_n: `Var(X_n) >= W_1 = lambda_n^2/(4m)` (already established,
point 12b), and `m =~ n/2`, so `n*Var(X_n) >= n*W_1 ~ lambda_n^2/2`. If `|lambda_n|` diverges
without bound, `n*Var(X_n)` diverges too, directly FALSIFYING the target hypothesis
`Var(X_n)=O(1/n)` -- not merely closing one proof route, unlike every other point in this
sequence (48-54). This is the single highest-leverage question currently open in this
experiment.

Since lambda_Q=4*Cov(X,Q) and lambda_delta=-m*E[delta] are two correlated (same-sample, not
independent) unbiased estimators of the same lambda_n (confirmed by Point 54A), this script
computes the variance-minimizing linear combination via their empirical bootstrap covariance
(GLS-style combination weight), which has strictly lower variance than either estimator alone
whenever they are not perfectly correlated -- reusing the already-saved `.npz` files, zero new
theta_via_lp calls.

Also computes LOCAL power-law slopes between fixed-ratio n-pairs (127->509, 251->1021,
509->2039, each spanning very close to a factor of ~4.0-4.07 in n) rather than only one global
fit -- per the user's own point, whether a_local trends toward 0 (a plateau, consistent with
lambda_n=O(1)) is a materially different signature than a_local staying roughly constant
(persistent slow divergence), and a single global slope cannot distinguish these shapes from 5
points alone.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

NS = [127, 251, 509, 1021, 2039]
N_BOOTSTRAP = 5000
BOOTSTRAP_SEED = 774422


def optimal_combined_lambda(n: int) -> dict:
    npz = np.load(METRICS / f"kappa_n_raw_samples_n{n}.npz")
    x = npz["X"]
    q = npz["Q"]
    delta = npz["delta_i_signed"]
    m = (n - 1) // 2
    reps = len(x)

    lambda_q = 4.0 * np.cov(x, q, ddof=1)[0, 1]
    lambda_delta = -m * delta.mean()

    rng = np.random.default_rng(BOOTSTRAP_SEED + n)
    boot_q = np.empty(N_BOOTSTRAP)
    boot_d = np.empty(N_BOOTSTRAP)
    for b in range(N_BOOTSTRAP):
        idx = rng.integers(0, reps, size=reps)
        boot_q[b] = 4.0 * np.cov(x[idx], q[idx], ddof=1)[0, 1]
        boot_d[b] = -m * delta[idx].mean()

    var_q = float(np.var(boot_q, ddof=1))
    var_d = float(np.var(boot_d, ddof=1))
    cov_qd = float(np.cov(boot_q, boot_d, ddof=1)[0, 1])

    # GLS-optimal weight on lambda_q minimizing Var(w*lambda_q + (1-w)*lambda_delta)
    denom = var_q + var_d - 2 * cov_qd
    w = (var_d - cov_qd) / denom if denom != 0 else 0.5
    w = float(np.clip(w, 0.0, 1.0))  # guard against extrapolation outside [0,1] from noise

    lambda_opt = w * lambda_q + (1 - w) * lambda_delta
    var_opt = w**2 * var_q + (1 - w) ** 2 * var_d + 2 * w * (1 - w) * cov_qd
    se_opt = math.sqrt(max(var_opt, 0.0))

    boot_opt = w * boot_q + (1 - w) * boot_d
    ci_lo, ci_hi = np.percentile(boot_opt, [2.5, 97.5])

    return {
        "n": n,
        "m": m,
        "reps": reps,
        "lambda_Q": float(lambda_q),
        "lambda_delta": float(lambda_delta),
        "var_Q": var_q,
        "var_delta": var_d,
        "cov_Q_delta": cov_qd,
        "weight_on_Q": w,
        "lambda_opt": float(lambda_opt),
        "se_opt": se_opt,
        "lambda_opt_ci95": [float(ci_lo), float(ci_hi)],
        "se_Q_alone": math.sqrt(var_q),
        "se_delta_alone": math.sqrt(var_d),
        "variance_reduction_vs_better_single": 1 - var_opt / min(var_q, var_d),
    }


def weighted_power_law_fit(ns, vals, ses):
    log_n = np.log(np.array(ns, dtype=float))
    log_v = np.log(np.array(vals, dtype=float))
    sigma_log = np.array(ses) / np.array(vals)  # delta method, relative SE approx
    W = np.diag(1.0 / sigma_log**2)
    Xmat = np.vstack([log_n, np.ones_like(log_n)]).T
    XtWX = Xmat.T @ W @ Xmat
    XtWy = Xmat.T @ W @ log_v
    beta = np.linalg.solve(XtWX, XtWy)
    cov_beta = np.linalg.inv(XtWX)
    slope, intercept = beta[0], beta[1]
    se_slope = math.sqrt(cov_beta[0, 0])
    dof = len(ns) - 2
    t_crit = stats.t.ppf(0.975, dof) if dof > 0 else float("nan")
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "se_slope": float(se_slope),
        "ci95": [float(slope - t_crit * se_slope), float(slope + t_crit * se_slope)],
        "dof": dof,
        "z_from_zero": float(slope / se_slope),
    }


def local_slope(n1, v1, n2, v2):
    return math.log(v2 / v1) / math.log(n2 / n1)


def run():
    rows = [optimal_combined_lambda(n) for n in NS]
    for r in rows:
        print(
            f"n={r['n']:5d} lambda_Q={r['lambda_Q']:+.4f}(se={r['se_Q_alone']:.4f}) "
            f"lambda_delta={r['lambda_delta']:+.4f}(se={r['se_delta_alone']:.4f}) "
            f"w_Q={r['weight_on_Q']:.3f} lambda_opt={r['lambda_opt']:+.4f} "
            f"se_opt={r['se_opt']:.4f} CI={r['lambda_opt_ci95']} "
            f"var_reduction={r['variance_reduction_vs_better_single']:.3f}",
            flush=True,
        )

    abs_lambda_opt = [abs(r["lambda_opt"]) for r in rows]
    se_opt = [r["se_opt"] for r in rows]
    global_fit = weighted_power_law_fit(NS, abs_lambda_opt, se_opt)
    print(f"\nGlobal weighted power-law fit on |lambda_opt|: {global_fit}")

    # local slopes between fixed-ratio pairs (~4x each)
    n_by = {r["n"]: r for r in rows}
    pairs = [(127, 509), (251, 1021), (509, 2039)]
    local_slopes = []
    for n1, n2 in pairs:
        a = local_slope(n1, abs(n_by[n1]["lambda_opt"]), n2, abs(n_by[n2]["lambda_opt"]))
        local_slopes.append({"n1": n1, "n2": n2, "local_slope": a})
        print(f"local slope {n1}->{n2}: {a:.4f}")

    out = {
        "claim": "Point 54B -- lambda_n scaling via variance-optimal combined estimator",
        "rows": rows,
        "global_weighted_fit_abs_lambda_opt": global_fit,
        "local_slopes": local_slopes,
    }
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "lambda_optimal_scaling.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    return out


if __name__ == "__main__":
    run()
