"""H-CAT31-4 analysis: prime-n variance law. Categories are locked in claim.md.

Usage: python analyze.py            # writes metrics/analysis.json
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"
COMPOSITE_BAND = (-0.9751, -0.8501)
COMPOSITE_SLOPE = -0.9126
N_BOOT = 2000
BOOT_SEED = 991


def load_thetas(name: str) -> dict[int, np.ndarray]:
    path = METRICS / name
    out: dict[int, list[float]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            out.setdefault(rec["n"], []).append(rec["theta"])
    return {n: np.array(v) for n, v in sorted(out.items())}


def bootstrap_var_ci(x: np.ndarray, seed: int, n_boot: int = N_BOOT) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(n_boot, len(x)))
    v = np.var(x[idx], axis=1, ddof=1)
    lo, hi = np.percentile(v, [2.5, 97.5])
    return float(lo), float(hi)


def wls_fit(ns: np.ndarray, var: np.ndarray, se_log: np.ndarray) -> dict:
    """Weighted OLS of log(var) on log(n), weights 1/se_log^2, t-interval with residual scaling.
    Same normal-equation form as H-CAT31-3/run.py::fit_exponent."""
    log_n = np.log(ns)
    log_v = np.log(var)
    w = 1.0 / np.maximum(se_log**2, 1e-12)
    X = np.vstack([log_n, np.ones_like(log_n)]).T
    W = np.diag(w)
    XtWX = X.T @ W @ X
    beta = np.linalg.solve(XtWX, X.T @ W @ log_v)
    resid = log_v - X @ beta
    dof = len(ns) - 2
    sigma2 = float(resid @ W @ resid) / dof
    cov = sigma2 * np.linalg.inv(XtWX)
    se = float(np.sqrt(cov[0, 0]))
    t = float(stats.t.ppf(0.975, dof))
    return {
        "slope": float(beta[0]),
        "intercept": float(beta[1]),
        "se": se,
        "ci95": [float(beta[0] - t * se), float(beta[0] + t * se)],
        "dof": dof,
    }


def summarise(data: dict[int, np.ndarray]) -> list[dict]:
    rows = []
    for n, thetas in data.items():
        x = np.log(thetas / np.sqrt(n))
        var = float(np.var(x, ddof=1))
        lo, hi = bootstrap_var_ci(x, BOOT_SEED + n)
        mean_x = float(x.mean())
        se_mean = float(x.std(ddof=1) / np.sqrt(len(x)))
        rows.append(
            {
                "n": n,
                "reps": len(x),
                "var": var,
                "var_ci95": [lo, hi],
                "se_log_var": (hi - lo) / (2 * 1.96 * var),
                "mean_x": mean_x,
                "mean_x_z": mean_x / se_mean,
                "n_times_var": n * var,
                "mad_var": float((1.4826 * np.median(np.abs(x - np.median(x)))) ** 2),
            }
        )
    return rows


def fit_rows(rows: list[dict], use_mad: bool = False) -> dict:
    ns = np.array([r["n"] for r in rows], dtype=float)
    var = np.array([r["mad_var" if use_mad else "var"] for r in rows])
    se = np.array([r["se_log_var"] for r in rows])
    return wls_fit(ns, var, se)


def classify(fit: dict) -> str:
    lo, hi = fit["ci95"]
    if (hi - lo) / 2 > 0.10:
        return "UNDERPOWERED"
    if lo <= -1.0 <= hi:
        if not (lo <= COMPOSITE_SLOPE <= hi):
            return "P-MINUS-ONE (sub-case P-DISCREPANT)"
        return "P-MINUS-ONE"
    if hi < -1.0:
        return "P-OTHER"
    overlaps = not (hi < COMPOSITE_BAND[0] or lo > COMPOSITE_BAND[1])
    return "P-CONSISTENT" if overlaps else "P-OTHER"


def simulate(true_slope: float, rows: list[dict], n_sims: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    ns = np.array([r["n"] for r in rows], dtype=float)
    sigma = np.sqrt(2.0 / (np.array([r["reps"] for r in rows]) - 1.0))
    c = np.exp(np.mean(np.log([r["var"] for r in rows]) - true_slope * np.log(ns)))
    contains = 0
    excludes_minus_one = 0
    for _ in range(n_sims):
        v = c * ns**true_slope * np.exp(rng.normal(0.0, sigma))
        f = wls_fit(ns, v, sigma)
        lo, hi = f["ci95"]
        contains += int(lo <= true_slope <= hi)
        excludes_minus_one += int(not (lo <= -1.0 <= hi))
    return {
        "true_slope": true_slope,
        "n_sims": n_sims,
        "coverage_of_truth": contains / n_sims,
        "fraction_ci_excludes_minus1": excludes_minus_one / n_sims,
    }


def main() -> None:
    data = load_thetas("thetas_main.jsonl")
    rows = summarise(data)
    fit = fit_rows(rows)
    out: dict = {"rows": rows, "primary_fit": fit, "category": classify(fit)}

    out["fit_unweighted"] = fit_rows([{**r, "se_log_var": 1.0} for r in rows])  # equal weights
    out["fit_mad"] = fit_rows(rows, use_mad=True)

    slopes_loo = []
    for i in range(len(rows)):
        sub = [r for j, r in enumerate(rows) if j != i]
        slopes_loo.append({"dropped_n": rows[i]["n"], "slope": fit_rows(sub)["slope"]})
    out["leave_one_out"] = slopes_loo
    out["drop_two_smallest"] = fit_rows(rows[2:])
    out["drop_two_largest"] = fit_rows(rows[:-2])
    out["split_small_n_le_509"] = fit_rows([r for r in rows if r["n"] <= 509])
    out["split_large_n_ge_1021"] = fit_rows([r for r in rows if r["n"] >= 1021])
    nv = [r["n_times_var"] for r in rows]
    rho = stats.spearmanr([r["n"] for r in rows], nv)
    out["spearman_n_vs_nVar"] = {"rho": float(rho.statistic), "p": float(rho.pvalue)}

    # bootstrap of the slope itself (resample instances, refit)
    rng = np.random.default_rng(4242)
    slopes = []
    for _ in range(N_BOOT):
        bs_rows = []
        for n, th in data.items():
            x = np.log(th / np.sqrt(n))
            xb = x[rng.integers(0, len(x), len(x))]
            v = float(np.var(xb, ddof=1))
            bs_rows.append({"n": n, "var": v, "se_log_var": np.sqrt(2.0 / (len(x) - 1))})
        slopes.append(fit_rows(bs_rows)["slope"])
    out["bootstrap_slope_ci95"] = [
        float(np.percentile(slopes, 2.5)),
        float(np.percentile(slopes, 97.5)),
    ]

    block2_path = METRICS / "thetas_block2.jsonl"
    if block2_path.exists():
        b2 = summarise(load_thetas("thetas_block2.jsonl"))
        main_by_n = {r["n"]: r for r in rows}
        out["block2_vs_main"] = [
            {
                "n": r["n"],
                "var_main": main_by_n[r["n"]]["var"],
                "var_block2": r["var"],
                "ratio": r["var"] / main_by_n[r["n"]]["var"],
            }
            for r in b2
        ]

    out["controls"] = {
        "positive_control_truth_minus1": simulate(-1.0, rows, 2000, 1),
        "power_control_truth_composite": simulate(COMPOSITE_SLOPE, rows, 2000, 2),
        "symmetry_control_max_abs_z": max(abs(r["mean_x_z"]) for r in rows),
    }
    (METRICS / "analysis.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("primary_fit", "category", "controls")}, indent=2))
    for r in rows:
        print(
            f"n={r['n']:5d} reps={r['reps']:4d} var={r['var']:.5e} nVar={r['n_times_var']:.4f} "
            f"meanX_z={r['mean_x_z']:+.2f}"
        )


if __name__ == "__main__":
    main()
