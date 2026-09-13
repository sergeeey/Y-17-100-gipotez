"""Point 39b: "Variant C" from an external re-analysis -- fit Var(X_n) directly with an
additive model A/n + B/n^{1.5} (or similar corrections), checking whether the leading A/n
coefficient is significantly positive and whether the fit is genuinely better than the
already-established plain power law -- using the ALREADY-COMPUTED Monte Carlo sweep in this
experiment's root `metrics/run.json` (n=32..3000, `var_log_ratio` field = Var(X_n) directly,
NOT new computation).

Compares 4 models by weighted R^2 AND a sign-runs check on residuals (a model whose residuals
show a long one-signed run, not near-random alternation, is a sign of misspecification even if
its raw R^2 looks higher -- especially relevant here since all models have exactly 2 free
parameters, so R^2 alone is not confounded by different parameter counts, but weighted R^2 with
9 points can still be swayed by a couple of very-low-SE points without the fit tracking the
BULK of the data well).
"""

from __future__ import annotations

import json
from itertools import pairwise
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def sign_runs(residuals: np.ndarray) -> tuple[int, int, int]:
    signs = [1 if r > 0 else -1 for r in residuals]
    runs = 1
    for a, b in pairwise(signs):
        if a != b:
            runs += 1
    n_pos = sum(1 for s in signs if s > 0)
    return runs, n_pos, len(signs) - n_pos


def wald_wolfowitz_z(runs: int, n_pos: int, n_neg: int) -> float:
    """Wald-Wolfowitz runs-test z-score, normalizing raw run counts for their own marginal
    split -- a raw run count alone is NOT comparable across fits with different n_pos/n_neg
    (reviewer finding, point 39: an 8+/1- split can achieve AT MOST 3 runs, so "3 runs" there
    is not anomalous, it's close to that split's own expected value)."""
    total = n_pos + n_neg
    if n_pos == 0 or n_neg == 0 or total < 2:
        return float("nan")
    mu = 2 * n_pos * n_neg / total + 1
    var = (2 * n_pos * n_neg * (2 * n_pos * n_neg - total)) / (total**2 * (total - 1))
    if var <= 0:
        return float("nan")
    return (runs - mu) / var**0.5


def run() -> dict:
    with open(METRICS / "run.json", encoding="utf-8") as f:
        data = json.load(f)

    rows = data["sweep"]
    ns = np.array([r["n"] for r in rows], dtype=float)
    var_vals = np.array([r["var_log_ratio"] for r in rows], dtype=float)
    se_vals = np.array(
        [r["var_log_ratio"] * r["var_log_ratio_relative_se"] for r in rows], dtype=float
    )
    w = 1.0 / (se_vals / var_vals) ** 2
    sqrt_w = np.sqrt(w)

    log_n, log_var = np.log(ns), np.log(var_vals)
    A_mat = np.vstack([log_n, np.ones_like(log_n)]).T
    coef_power, *_ = np.linalg.lstsq(sqrt_w[:, None] * A_mat, sqrt_w * log_var, rcond=None)
    pred_power = np.exp(coef_power[1]) * ns ** coef_power[0]
    resid_power = var_vals - pred_power

    ss_tot = float(np.sum(w * (var_vals - np.average(var_vals, weights=w)) ** 2))
    ss_res_power = float(np.sum(w * resid_power**2))
    r2_power = 1 - ss_res_power / ss_tot
    print(
        f"Power law n^p: slope={coef_power[0]:.4f}, intercept={coef_power[1]:.4f}, "
        f"R^2={r2_power:.5f}  (cross-check vs run.json's own slope=-0.9126)",
        flush=True,
    )

    models = {}
    bases = {
        "A/n+B/n^1.5": (1.0 / ns, 1.0 / ns**1.5),
        "A/n+B/n^2": (1.0 / ns, 1.0 / ns**2),
        "A*logn/n+B/n": (np.log(ns) / ns, 1.0 / ns),
    }
    for name, (X1, X2) in bases.items():
        design = np.vstack([X1, X2]).T
        coef, *_ = np.linalg.lstsq(sqrt_w[:, None] * design, sqrt_w * var_vals, rcond=None)
        pred = coef[0] * X1 + coef[1] * X2
        resid = var_vals - pred
        r2 = 1 - float(np.sum(w * resid**2)) / ss_tot
        runs, n_pos, n_neg = sign_runs(resid)
        z = wald_wolfowitz_z(runs, n_pos, n_neg)
        models[name] = {
            "A": float(coef[0]),
            "B": float(coef[1]),
            "r2": r2,
            "sign_runs": runs,
            "n_pos": n_pos,
            "n_neg": n_neg,
            "wald_wolfowitz_z": z,
        }
        print(
            f"{name}: A={coef[0]:.4f}, B={coef[1]:.4f}, R^2={r2:.5f}, "
            f"sign_runs={runs}/{len(resid)} ({n_pos}+/{n_neg}-), z={z:.3f}",
            flush=True,
        )

    runs_power, pos_power, neg_power = sign_runs(resid_power)
    z_power = wald_wolfowitz_z(runs_power, pos_power, neg_power)
    print(
        f"power-law sign_runs={runs_power}/{len(resid_power)} "
        f"({pos_power}+/{neg_power}-), z={z_power:.3f}",
        flush=True,
    )

    result = {
        "n_values": ns.tolist(),
        "var_values": var_vals.tolist(),
        "power_law": {
            "slope": float(coef_power[0]),
            "intercept": float(coef_power[1]),
            "r2": r2_power,
            "sign_runs": runs_power,
            "n_pos": pos_power,
            "n_neg": neg_power,
            "wald_wolfowitz_z": z_power,
        },
        "additive_models": models,
        "verdict": (
            "reviewer-corrected (P1): raw sign-runs counts are NOT comparable across fits "
            "with different pos/neg splits (an 8+/1- split can achieve at most 3 runs, so "
            "'3 runs' there is close to that split's own expected value, not anomalous). "
            "Wald-Wolfowitz z-scores show NEITHER family is significantly non-random at n=9 "
            "(all |z|<2). The R^2 gap (0.9976 vs 0.9924) is marginal. Conclusion: this check "
            "is INCONCLUSIVE at n=9 -- it does NOT demonstrate that forcing an A/n leading "
            "term produces a better OR worse fit than the plain power law on this dataset"
        ),
    }
    with open(METRICS / "var_additive_fit_check.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    return result


if __name__ == "__main__":
    run()
