"""
H-CAT30-1 pilot: does E||sum_i g_i T_i||_{I_2} grow with d for r=3, p=2 (open
regime, p<2r=6, per Bandeira et al. arXiv:2603.29571 Conjecture 16), using
T_i = a_i^{otimes 3}, a_i random unit vectors (||T_i||_{I_2}=1 exactly), n
fixed?  Conjecture predicts d^{1/2-1/p}=d^0=1 -> dimension-free (up to
polylog(d,n)).  Pre-registered kill criterion: weighted power-law fit of
log(E-norm) vs log(d); if 95% CI on the exponent excludes 0 and is bounded
away from [-0.1,0.1] -> LEAD (real d-dependence beyond conjectured rate).
Else -> informative-negative (consistent with the conjecture in this probe).
"""

import json
import time

import numpy as np
from scipy import stats
from tensor_injective_norm import estimate_injective_norm


def run(
    n=20, d_values=(5, 10, 20, 40, 80, 160), n_gaussian_draws=60, n_restarts=50, n_iter=70, seed=0
):
    rng = np.random.default_rng(seed)
    results = {}
    for d in d_values:
        t0 = time.time()
        # FIXED random tensor family for this d (deterministic T_i per conjecture statement)
        A = rng.standard_normal((n, d))
        A = A / np.linalg.norm(A, axis=1, keepdims=True)  # unit rows -> ||T_i||_{I_2}=1 exactly

        draws = []
        for _ in range(n_gaussian_draws):
            g = rng.standard_normal(n)
            val, _ = estimate_injective_norm(A, g, n_restarts=n_restarts, n_iter=n_iter, rng=rng)
            draws.append(val)
        draws = np.array(draws)
        mean_est = draws.mean()
        se = draws.std(ddof=1) / np.sqrt(len(draws))
        results[d] = {
            "mean": float(mean_est),
            "se": float(se),
            "std": float(draws.std(ddof=1)),
            "n_draws": len(draws),
            "elapsed_s": time.time() - t0,
            "raw": draws.tolist(),
        }
        print(
            f"d={d:4d}  mean_norm={mean_est:.4f}  se={se:.4f}  "
            f"elapsed={results[d]['elapsed_s']:.1f}s"
        )
    return results


def weighted_power_law_fit(d_values, results):
    """log(mean) = alpha + beta*log(d), weighted by inverse-variance of log(mean)
    via delta method: var(log(mean)) ~ (se/mean)^2."""
    x = np.log(np.array(d_values, dtype=float))
    y = np.array([np.log(results[d]["mean"]) for d in d_values])
    se_log = np.array([results[d]["se"] / results[d]["mean"] for d in d_values])
    w = 1.0 / (se_log**2)

    X = np.column_stack([np.ones_like(x), x])
    W = np.diag(w)
    XtW = X.T @ W
    cov = np.linalg.inv(XtW @ X)
    beta_hat = cov @ (XtW @ y)
    alpha, beta = beta_hat
    se_beta = np.sqrt(cov[1, 1])
    # residual-based sanity: weighted R^2
    y_pred = X @ beta_hat
    resid = y - y_pred
    chi2 = np.sum(w * resid**2)
    dof = len(x) - 2
    return {
        "alpha": float(alpha),
        "beta": float(beta),
        "se_beta": float(se_beta),
        "ci95": [float(beta - 1.96 * se_beta), float(beta + 1.96 * se_beta)],
        "chi2": float(chi2),
        "dof": dof,
        "chi2_p": float(1 - stats.chi2.cdf(chi2, dof)) if dof > 0 else None,
    }


if __name__ == "__main__":
    results = run()
    d_values = sorted(results.keys())
    fit = weighted_power_law_fit(d_values, results)
    print("\nWeighted power-law fit: log(E-norm) = alpha + beta*log(d)")
    print(
        f"  beta = {fit['beta']:.4f}  se={fit['se_beta']:.4f}  "
        f"95% CI = [{fit['ci95'][0]:.4f}, {fit['ci95'][1]:.4f}]"
    )
    print(f"  chi2 = {fit['chi2']:.3f} (dof={fit['dof']}), p = {fit['chi2_p']}")

    out = {"n": 20, "d_values": d_values, "results": results, "fit": fit}
    with open("tensor_conj16_pilot_result.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nWritten to tensor_conj16_pilot_result.json")
