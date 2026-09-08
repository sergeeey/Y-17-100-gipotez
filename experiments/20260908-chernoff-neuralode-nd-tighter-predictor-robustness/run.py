"""run.py — H-B2-1x: robustness follow-up to H-B2-1w's K(A)-based predictive model. Does the
fitted log(K(A)) exponent (~1.94 on 20 training points) hold up with a 4x larger training set and
95% confidence intervals, and does the larger model still win on a GENUINELY FRESH held-out set
(not H-B2-1w's own 400-414, to avoid re-using already-revealed test data)?

Reuses UNCHANGED via dynamic import: build_matrix_with_seed_and_n (H-B2-1m),
pseudospectral_abscissa (H-B2-1r), measure_m1 (H-B2-1k/dimension-sweep),
kreiss_constant_estimate (H-B2-1u). EXPANDED TRAIN reuses H-B2-1t's own stored alpha_eps/M1 for
all 80 (N_DIM, seed) pairs (seeds 300-339); K(A) reused unchanged from H-B2-1u for seeds 300-309,
computed fresh only for the additional 310-339 (60 new computations, Minimal Relaxation Rule).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1x_multin", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_R_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
_SPEC_R = importlib.util.spec_from_file_location("chernoff_1x_alpha", _R_DIR / "run.py")
alpha_mod = importlib.util.module_from_spec(_SPEC_R)
_SPEC_R.loader.exec_module(alpha_mod)

_K_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-dimension-sweep"
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1x_dimsweep", _K_DIR / "run.py")
dim_sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(dim_sweep)

_U_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-kreiss-mechanism"
_SPEC_U = importlib.util.spec_from_file_location("chernoff_1x_kreiss", _U_DIR / "run.py")
kreiss_mod = importlib.util.module_from_spec(_SPEC_U)
_SPEC_U.loader.exec_module(kreiss_mod)

with open(_U_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1U_RESULT = json.load(f)

_T_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-pseudospectral-fresh-confirmatory"
with open(_T_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1T_RESULT = json.load(f)

_W_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-tighter-predictor-m1"
with open(_W_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1W_RESULT = json.load(f)

TRAIN_N_DIM_VALUES = (40, 50)
TRAIN_SEEDS_WITH_K = tuple(range(300, 310))  # already have K(A), from H-B2-1u
TRAIN_SEEDS_NEED_K = tuple(range(310, 340))  # new K(A) computation, alpha_eps/m1 already stored

TEST_N_DIM_VALUES = (40, 50)
TEST_SEED_START, TEST_SEED_END = (
    420,
    435,
)  # fresh -- zero overlap w/ 0-39/40-99/0-59/100-159/300-339/400-414


def build_expanded_train_data() -> list[dict]:
    rows = []
    for n_dim in TRAIN_N_DIM_VALUES:
        for seed in TRAIN_SEEDS_WITH_K:
            k_est = H_B2_1U_RESULT["per_n_slice"][str(n_dim)]["per_seed"][str(seed)]["k_estimate"]
            t_row = H_B2_1T_RESULT["per_n_slice"][str(n_dim)]["per_seed"][str(seed)]
            rows.append(
                {
                    "n_dim": n_dim,
                    "seed": seed,
                    "k_estimate": k_est,
                    "alpha_eps": t_row["alpha_eps"],
                    "m1": t_row["m1"],
                }
            )
        for seed in TRAIN_SEEDS_NEED_K:
            a = multin.build_matrix_with_seed_and_n(n_dim, seed)
            k_est = kreiss_mod.kreiss_constant_estimate(a)["k_estimate"]
            t_row = H_B2_1T_RESULT["per_n_slice"][str(n_dim)]["per_seed"][str(seed)]
            rows.append(
                {
                    "n_dim": n_dim,
                    "seed": seed,
                    "k_estimate": k_est,
                    "alpha_eps": t_row["alpha_eps"],
                    "m1": t_row["m1"],
                }
            )
    return rows


def build_fresh_test_data() -> list[dict]:
    rows = []
    for n_dim in TEST_N_DIM_VALUES:
        for seed in range(TEST_SEED_START, TEST_SEED_END):
            a = multin.build_matrix_with_seed_and_n(n_dim, seed)
            k_est = kreiss_mod.kreiss_constant_estimate(a)["k_estimate"]
            alpha_eps = alpha_mod.pseudospectral_abscissa(a, eps=1.0)
            m1 = dim_sweep.measure_m1(a, dim_sweep.T_MAX, dim_sweep.W)
            rows.append(
                {
                    "n_dim": n_dim,
                    "seed": seed,
                    "k_estimate": k_est,
                    "alpha_eps": alpha_eps,
                    "m1": m1,
                }
            )
    return rows


def _fit_ols_with_se(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """OLS coefficients + their standard errors (classical formula: sigma^2 * (X'X)^-1)."""
    n, p = x.shape
    coeffs, *_ = np.linalg.lstsq(x, y, rcond=None)
    resid = y - x @ coeffs
    dof = max(n - p, 1)
    sigma2 = float(resid @ resid) / dof
    xtx_inv = np.linalg.inv(x.T @ x)
    se = np.sqrt(np.diag(sigma2 * xtx_inv))
    return coeffs, se


def _rmse(pred: np.ndarray, actual: np.ndarray) -> float:
    return float(np.sqrt(np.mean((pred - actual) ** 2)))


def cmd_run() -> dict:
    train = build_expanded_train_data()
    test = build_fresh_test_data()

    log_m1_train = np.log(np.array([r["m1"] for r in train]))
    log_k_train = np.log(np.array([r["k_estimate"] for r in train]))
    log_n_train = np.log(np.array([r["n_dim"] for r in train], dtype=float))

    log_m1_test = np.log(np.array([r["m1"] for r in test]))
    log_k_test = np.log(np.array([r["k_estimate"] for r in test]))
    log_n_test = np.log(np.array([r["n_dim"] for r in test], dtype=float))

    x_train = np.column_stack([np.ones_like(log_k_train), log_k_train, log_n_train])
    coeffs, se = _fit_ols_with_se(x_train, log_m1_train)
    # 95% CI, normal approximation (t-critical ~1.96 for n=80, p=3, dof=77, close enough)
    ci_low = coeffs - 1.96 * se
    ci_high = coeffs + 1.96 * se

    x_test = np.column_stack([np.ones_like(log_k_test), log_k_test, log_n_test])
    pred_expanded = x_test @ coeffs
    rmse_expanded_model = _rmse(pred_expanded, log_m1_test)

    # H-B2-1w's original 20-point model, re-applied to THIS fresh test set for a fair comparison
    original_coeffs = np.array(H_B2_1W_RESULT["fitted_coefficients"]["k_model_intercept_logK_logN"])
    pred_original = x_test @ original_coeffs
    rmse_original_model = _rmse(pred_original, log_m1_test)

    k_exponent = float(coeffs[1])
    k_exponent_ci = [float(ci_low[1]), float(ci_high[1])]
    ci_brackets_2 = bool(ci_low[1] <= 2.0 <= ci_high[1])
    ci_brackets_1 = bool(ci_low[1] <= 1.0 <= ci_high[1])

    if ci_brackets_2 and not ci_brackets_1:
        verdict = "K_SQUARED_PATTERN_ROBUST"
    elif ci_brackets_1:
        verdict = "EXPONENT_UNCERTAIN_INCLUDES_LINEAR"
    else:
        verdict = "EXPONENT_SHIFTED_AWAY_FROM_2"

    result = {
        "config": {
            "n_train": len(train),
            "n_test": len(test),
            "test_seed_range": [TEST_SEED_START, TEST_SEED_END],
        },
        "fitted_coefficients": coeffs.tolist(),
        "standard_errors": se.tolist(),
        "ci_95_low": ci_low.tolist(),
        "ci_95_high": ci_high.tolist(),
        "k_exponent": k_exponent,
        "k_exponent_ci_95": k_exponent_ci,
        "ci_brackets_2": ci_brackets_2,
        "ci_brackets_1": ci_brackets_1,
        "rmse_expanded_model_on_fresh_test": rmse_expanded_model,
        "rmse_original_h_b2_1w_model_on_same_fresh_test": rmse_original_model,
        "verdict": verdict,
        "train_data": train,
        "test_data": test,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in result.items() if k not in ("train_data", "test_data")}, indent=2
        )
    )
    return result


if __name__ == "__main__":
    cmd_run()
