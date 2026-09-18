import json
from pathlib import Path

import numpy as np
from scipy import stats


def weighted_power_law_fit_on_R(points):
    """points: list of (d, R, R_se). Fit log(R)=alpha+beta*log(d)."""
    d = np.array([p[0] for p in points], dtype=float)
    R = np.array([p[1] for p in points])
    se = np.array([p[2] for p in points])
    x = np.log(d)
    y = np.log(R)
    se_log = se / R
    w = 1.0 / se_log**2
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
    return {
        "alpha": float(alpha),
        "beta": float(beta),
        "se_beta": float(se_beta),
        "ci95": [float(beta - 1.96 * se_beta), float(beta + 1.96 * se_beta)],
        "chi2": float(chi2),
        "dof": dof,
        "chi2_p": float(1 - stats.chi2.cdf(chi2, dof)) if dof > 0 else None,
    }


def main():
    result_path = Path(__file__).resolve().parent / "metrics" / "run.json"
    with open(result_path) as f:
        data = json.load(f)

    fits = {}
    for scale_key, label in [
        ("scale_A_n_eq_d", "Scale A (n=d)"),
        ("scale_B_n_eq_d1p5", "Scale B (n=d^1.5)"),
    ]:
        pts = data[scale_key]
        points = [(v["d"], v["R"], v["R_se"]) for v in pts.values()]
        points.sort()
        fit = weighted_power_law_fit_on_R(points)
        fits[scale_key] = {"label": label, "points": points, "fit": fit}
        print(f"{label}: points={points}")
        print(
            f"  beta={fit['beta']:.4f} se={fit['se_beta']:.4f} "
            f"95% CI=[{fit['ci95'][0]:.4f},{fit['ci95'][1]:.4f}] "
            f"chi2={fit['chi2']:.2f}(dof={fit['dof']}) p={fit['chi2_p']}"
        )
        print()

    out_path = Path(__file__).resolve().parent / "metrics" / "redesign_analysis_result.json"
    with open(out_path, "w") as f:
        json.dump(fits, f, indent=2)


if __name__ == "__main__":
    main()
