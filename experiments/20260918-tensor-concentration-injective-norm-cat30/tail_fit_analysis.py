"""Supplementary analysis: the full-range d=5..160 fit is contaminated by a
small-d transient (d=5,10,20 dropping sharply, per the pilot's own printed
means) and its own chi2 test (p=7.6e-6) already says a single power law does
not fit the WHOLE range well. Refit restricted to the asymptotic tail
d in {40,80,160} to test the actually-relevant claim: is the LARGE-d behavior
flat (consistent with conjecture) or still trending?  Also test the flat-
constant null directly via a weighted chi2 goodness-of-fit, same style as
H-CAT31-3 Point 95's own n*R_n weighted-constant test.
"""

import json
from pathlib import Path

import numpy as np
from scipy import stats


def weighted_power_law_fit(d_values, results):
    x = np.log(np.array(d_values, dtype=float))
    y = np.array([np.log(results[str(d)]["mean"]) for d in d_values])
    se_log = np.array([results[str(d)]["se"] / results[str(d)]["mean"] for d in d_values])
    w = 1.0 / (se_log**2)
    X = np.column_stack([np.ones_like(x), x])
    W = np.diag(w)
    XtW = X.T @ W
    cov = np.linalg.inv(XtW @ X)
    beta_hat = cov @ (XtW @ y)
    alpha, beta = beta_hat
    se_beta = np.sqrt(cov[1, 1])
    y_pred = X @ beta_hat
    resid = y - y_pred
    chi2 = np.sum(w * resid**2)
    dof = len(x) - 2
    return alpha, beta, se_beta, chi2, dof


def weighted_constant_chi2(d_values, results):
    """Test H0: mean is the SAME constant across these d (ignore log(d) trend
    entirely), weighted chi2 goodness of fit -- same style as H-CAT31-3 Point 95."""
    means = np.array([results[str(d)]["mean"] for d in d_values])
    ses = np.array([results[str(d)]["se"] for d in d_values])
    w = 1.0 / ses**2
    const = np.sum(w * means) / np.sum(w)
    chi2 = np.sum(w * (means - const) ** 2)
    dof = len(d_values) - 1
    p = 1 - stats.chi2.cdf(chi2, dof)
    return const, chi2, dof, p


def main():
    pilot_path = Path(__file__).resolve().parent / "metrics" / "run.json"
    with open(pilot_path) as f:
        data = json.load(f)
    results = data["results"]
    d_all = sorted(int(d) for d in results.keys())

    print("=== Full range d in {5,10,20,40,80,160} ===")
    _a, b, se_b, chi2, dof = weighted_power_law_fit(d_all, results)
    print(
        f"beta={b:.4f} se={se_b:.4f} 95% CI=[{b - 1.96 * se_b:.4f},{b + 1.96 * se_b:.4f}] "
        f"chi2={chi2:.2f}(dof={dof}) p={1 - stats.chi2.cdf(chi2, dof):.2e}"
    )

    print("\n=== Asymptotic tail d in {40,80,160} only ===")
    d_tail = [d for d in d_all if d >= 40]
    _a2, b2, se_b2, chi2_2, dof2 = weighted_power_law_fit(d_tail, results)
    ci = [b2 - 1.96 * se_b2, b2 + 1.96 * se_b2]
    p_tail = (1 - stats.chi2.cdf(chi2_2, dof2)) if dof2 > 0 else float("nan")
    print(
        f"beta={b2:.4f} se={se_b2:.4f} 95% CI=[{ci[0]:.4f},{ci[1]:.4f}] "
        f"chi2={chi2_2:.2f}(dof={dof2}) p={p_tail:.3f}"
    )

    print("\n=== Weighted flat-constant test, tail d in {40,80,160} ===")
    const, chi2c, dofc, pc = weighted_constant_chi2(d_tail, results)
    print(f"weighted constant={const:.4f}  chi2={chi2c:.3f}(dof={dofc})  p={pc:.3f}")

    print("\n=== Weighted flat-constant test, ALL d (sanity, expect to fail given transient) ===")
    const_all, chi2c_all, dofc_all, pc_all = weighted_constant_chi2(d_all, results)
    print(
        f"weighted constant={const_all:.4f}  chi2={chi2c_all:.3f}(dof={dofc_all})  p={pc_all:.2e}"
    )

    out = {
        "full_range_fit": {
            "beta": b,
            "se_beta": se_b,
            "ci95": [b - 1.96 * se_b, b + 1.96 * se_b],
            "chi2": chi2,
            "dof": dof,
        },
        "tail_fit_d_ge_40": {
            "beta": b2,
            "se_beta": se_b2,
            "ci95": ci,
            "chi2": chi2_2,
            "dof": dof2,
        },
        "tail_flat_constant_test": {"const": const, "chi2": chi2c, "dof": dofc, "p": pc},
        "all_flat_constant_test": {
            "const": const_all,
            "chi2": chi2c_all,
            "dof": dofc_all,
            "p": pc_all,
        },
    }
    out_path = Path(__file__).resolve().parent / "metrics" / "tail_fit_analysis_result.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
