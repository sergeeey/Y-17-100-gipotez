"""run.py — H-B2-1w: does a fitted log-linear model using K(A) (Kreiss constant estimate)
predict M1's actual magnitude more precisely than (a) the naive theoretical ceiling e*n*K(A), or
(b) the arc's own established correlational predictor (pseudospectral abscissa alone)?

User's own Step 3, Option A (empirical regression, chosen via AskUserQuestion over Option B --
deriving a new analytic bound). First PREDICTIVE-tier claim in this arc (everything through
H-B2-1v was descriptive). Pre-registered train/test split per claim.md, Anti-Overfitting Gate
discipline -- TEST set values are not touched until the models are fit on TRAIN.

Reuses UNCHANGED via dynamic import: build_matrix_with_seed_and_n (H-B2-1m),
pseudospectral_abscissa (H-B2-1r), measure_m1 (H-B2-1k/dimension-sweep),
kreiss_constant_estimate + KREISS_GRID_KWARGS + EPS_VALUES (H-B2-1u). TRAIN data (K(A), M1 for
seeds 300-309) reused from H-B2-1u's own metrics/run.json; alpha_eps/M1 for the same seeds reused
from H-B2-1t's own metrics/run.json -- zero recomputation for TRAIN.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1w_multin", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_R_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
_SPEC_R = importlib.util.spec_from_file_location("chernoff_1w_alpha", _R_DIR / "run.py")
alpha_mod = importlib.util.module_from_spec(_SPEC_R)
_SPEC_R.loader.exec_module(alpha_mod)

_K_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-dimension-sweep"
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1w_dimsweep", _K_DIR / "run.py")
dim_sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(dim_sweep)

_U_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-kreiss-mechanism"
_SPEC_U = importlib.util.spec_from_file_location("chernoff_1w_kreiss", _U_DIR / "run.py")
kreiss_mod = importlib.util.module_from_spec(_SPEC_U)
_SPEC_U.loader.exec_module(kreiss_mod)

with open(_U_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1U_RESULT = json.load(f)

_T_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-pseudospectral-fresh-confirmatory"
with open(_T_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1T_RESULT = json.load(f)

TRAIN_N_DIM_VALUES = (40, 50)
TRAIN_SEEDS = tuple(range(300, 310))  # H-B2-1u's own 10 seeds, reused exactly

TEST_N_DIM_VALUES = (40, 50)
TEST_SEED_START, TEST_SEED_END = (
    400,
    415,
)  # fresh -- zero overlap with 0-39/40-99/0-59/100-159/300-339


def build_train_data() -> list[dict]:
    """Zero new compute -- pulls (K, alpha_eps, N_DIM, M1) straight from H-B2-1u's and
    H-B2-1t's own stored metrics/run.json for the SAME 20 (N_DIM, seed) pairs."""
    rows = []
    for n_dim in TRAIN_N_DIM_VALUES:
        for seed in TRAIN_SEEDS:
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
    return rows


def build_test_data() -> list[dict]:
    """Fresh compute for genuinely new seeds -- K(A) via H-B2-1u's own kreiss_constant_estimate,
    alpha_eps via H-B2-1r's pseudospectral_abscissa at eps=1 (matching H-B2-1t's own convention),
    M1 via H-B2-1k's own measure_m1 -- all reused unchanged."""
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


def _fit_ols(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Plain OLS via lstsq -- x already includes an intercept column."""
    coeffs, *_ = np.linalg.lstsq(x, y, rcond=None)
    return coeffs


def _rmse(pred: np.ndarray, actual: np.ndarray) -> float:
    return float(np.sqrt(np.mean((pred - actual) ** 2)))


def cmd_run() -> dict:
    train = build_train_data()
    test = build_test_data()

    log_m1_train = np.log(np.array([r["m1"] for r in train]))
    log_k_train = np.log(np.array([r["k_estimate"] for r in train]))
    log_n_train = np.log(np.array([r["n_dim"] for r in train], dtype=float))
    log_alpha_train = np.log(np.array([r["alpha_eps"] for r in train]))

    log_m1_test = np.log(np.array([r["m1"] for r in test]))
    log_k_test = np.log(np.array([r["k_estimate"] for r in test]))
    log_n_test = np.log(np.array([r["n_dim"] for r in test], dtype=float))
    log_alpha_test = np.log(np.array([r["alpha_eps"] for r in test]))

    # Model A: log(M1) ~ intercept + log(K) + log(N)
    x_train_a = np.column_stack([np.ones_like(log_k_train), log_k_train, log_n_train])
    coeffs_a = _fit_ols(x_train_a, log_m1_train)
    x_test_a = np.column_stack([np.ones_like(log_k_test), log_k_test, log_n_test])
    pred_a = x_test_a @ coeffs_a
    rmse_k_model = _rmse(pred_a, log_m1_test)

    # Model B (comparator): log(M1) ~ intercept + log(alpha_eps)
    x_train_b = np.column_stack([np.ones_like(log_alpha_train), log_alpha_train])
    coeffs_b = _fit_ols(x_train_b, log_m1_train)
    x_test_b = np.column_stack([np.ones_like(log_alpha_test), log_alpha_test])
    pred_b = x_test_b @ coeffs_b
    rmse_alpha_only_model = _rmse(pred_b, log_m1_test)

    # Model C (comparator): naive ceiling e*n*K(A) as a direct point prediction of M1
    ceiling_test = np.array([kreiss_mod.EULER_E * r["n_dim"] * r["k_estimate"] for r in test])
    pred_c = np.log(ceiling_test)
    rmse_naive_ceiling = _rmse(pred_c, log_m1_test)

    rmses = {
        "k_model": rmse_k_model,
        "alpha_only_model": rmse_alpha_only_model,
        "naive_ceiling": rmse_naive_ceiling,
    }
    best = min(rmses, key=rmses.get)

    if (
        best == "k_model"
        and rmse_k_model < rmse_alpha_only_model
        and rmse_k_model < rmse_naive_ceiling
    ):
        verdict = "K_MODEL_WINS"
    elif best == "naive_ceiling":
        verdict = "NEITHER_MODEL_BEATS_CEILING"
    else:
        verdict = "K_MODEL_DOES_NOT_ADD_VALUE"

    result = {
        "config": {
            "train_n_dim_values": list(TRAIN_N_DIM_VALUES),
            "train_seeds": list(TRAIN_SEEDS),
            "test_n_dim_values": list(TEST_N_DIM_VALUES),
            "test_seed_range": [TEST_SEED_START, TEST_SEED_END],
            "n_train": len(train),
            "n_test": len(test),
        },
        "fitted_coefficients": {
            "k_model_intercept_logK_logN": coeffs_a.tolist(),
            "alpha_only_model_intercept_logAlpha": coeffs_b.tolist(),
        },
        "rmse_on_log_m1_test": rmses,
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
