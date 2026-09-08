"""run.py — H-B2-2: does a direct resolvent-norm reference (no pseudopy, no tricontour)
replace kappa(lambda_1) as the correct K(A) proxy across the FULL H-B2-1x population, and
does refitting M1~K(A) with it change the exponent/RMSE picture again?

K_ref(A) = max(kappa(lambda_1), floored real-axis line search) -- see claim.md for the
full derivation and the pre-check that motivated this specific design (x_floor=1e-4 avoids
near-x=0 SVD precision loss; kappa(lambda_1) handles that limit exactly instead).

Reuses UNCHANGED via dynamic import: build_matrix_with_seed_and_n (H-B2-1m),
eigenvalue_condition_number (H-B2-1z). shallow_k/m1 for the full 80+30 H-B2-1x population
are NOT recomputed -- pulled directly from stored metrics/run.json, Minimal Relaxation Rule.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_2_multin", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_Z_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-kreiss-eigval-condition-anchor"
_SPEC_Z = importlib.util.spec_from_file_location("chernoff_2_eigval_anchor", _Z_DIR / "run.py")
eigval_anchor = importlib.util.module_from_spec(_SPEC_Z)
_SPEC_Z.loader.exec_module(eigval_anchor)

_X_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-tighter-predictor-robustness"
with open(_X_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1X_RESULT = json.load(f)

X_FLOOR = 1e-4
X_HI = 60.0
N_COARSE = 300


def _sigma_min(z: complex, a: np.ndarray) -> float:
    m = z * np.eye(a.shape[0]) - a
    return float(np.linalg.svd(m, compute_uv=False)[-1])


def _neg_ratio(log_x: float, a: np.ndarray, alpha: float) -> float:
    x = np.exp(log_x)
    return -(x / _sigma_min(alpha + x, a))


def line_search_floored(a: np.ndarray, alpha: float) -> dict:
    """max_{x in [X_FLOOR, X_HI]} x/sigma_min((alpha+x)I-a): log-spaced coarse grid +
    local refinement. See claim.md for why X_FLOOR=1e-4 is safe (pre-checked separately)."""
    log_xs = np.linspace(np.log(X_FLOOR), np.log(X_HI), N_COARSE)
    ratios = np.array([-_neg_ratio(lx, a, alpha) for lx in log_xs])
    i = int(np.argmax(ratios))
    lo = log_xs[max(0, i - 2)]
    hi = log_xs[min(N_COARSE - 1, i + 2)]
    res = minimize_scalar(
        _neg_ratio, bounds=(lo, hi), method="bounded", args=(a, alpha), options={"xatol": 1e-10}
    )
    x_star = float(np.exp(res.x))
    r_star = float(-res.fun)
    return {
        "x_star": x_star,
        "ratio": r_star,
        "near_floor": bool(x_star < 10 * X_FLOOR),
    }


def resolvent_reference_k(a: np.ndarray) -> dict:
    alpha = float(np.max(np.linalg.eigvals(a).real))
    kappa_info = eigval_anchor.eigenvalue_condition_number(a)
    kappa = kappa_info["kappa_lambda1"]
    search = line_search_floored(a, alpha)
    k_ref = max(kappa, search["ratio"])
    return {
        "alpha": alpha,
        "kappa_lambda1": kappa,
        "line_search": search,
        "k_ref": k_ref,
        "line_search_dominates": bool(search["ratio"] > kappa * 1.001),
    }


def _fit_ols(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    coeffs, *_ = np.linalg.lstsq(x, y, rcond=None)
    return coeffs


def compute_population_reference() -> dict:
    train_rows = []
    for r in H_B2_1X_RESULT["train_data"]:
        a = multin.build_matrix_with_seed_and_n(r["n_dim"], r["seed"])
        info = resolvent_reference_k(a)
        train_rows.append({**r, **{k: v for k, v in info.items() if k != "line_search"}})

    test_rows = []
    for r in H_B2_1X_RESULT["test_data"]:
        a = multin.build_matrix_with_seed_and_n(r["n_dim"], r["seed"])
        info = resolvent_reference_k(a)
        test_rows.append({**r, **{k: v for k, v in info.items() if k != "line_search"}})

    return {"train_rows": train_rows, "test_rows": test_rows}


def refit_with_k_ref(train_rows: list[dict], test_rows: list[dict]) -> dict:
    log_kref_train = np.log(np.array([r["k_ref"] for r in train_rows]))
    log_m1_train = np.log(np.array([r["m1"] for r in train_rows]))
    log_n_train = np.log(np.array([r["n_dim"] for r in train_rows], dtype=float))

    log_kref_test = np.log(np.array([r["k_ref"] for r in test_rows]))
    log_m1_test = np.log(np.array([r["m1"] for r in test_rows]))
    log_n_test = np.log(np.array([r["n_dim"] for r in test_rows], dtype=float))

    x_train_1f = np.column_stack([np.ones_like(log_kref_train), log_kref_train])
    coeffs_1f = _fit_ols(x_train_1f, log_m1_train)
    x_test_1f = np.column_stack([np.ones_like(log_kref_test), log_kref_test])
    rmse_1f = float(np.sqrt(np.mean((x_test_1f @ coeffs_1f - log_m1_test) ** 2)))

    x_train_2f = np.column_stack([np.ones_like(log_kref_train), log_kref_train, log_n_train])
    coeffs_2f = _fit_ols(x_train_2f, log_m1_train)
    x_test_2f = np.column_stack([np.ones_like(log_kref_test), log_kref_test, log_n_test])
    rmse_2f = float(np.sqrt(np.mean((x_test_2f @ coeffs_2f - log_m1_test) ** 2)))

    return {
        "single_feature_exponent": float(coeffs_1f[1]),
        "single_feature_intercept": float(coeffs_1f[0]),
        "single_feature_rmse_on_fresh_test": rmse_1f,
        "two_feature_kref_exponent": float(coeffs_2f[1]),
        "two_feature_n_dim_exponent": float(coeffs_2f[2]),
        "two_feature_intercept": float(coeffs_2f[0]),
        "two_feature_rmse_on_fresh_test": rmse_2f,
    }


def cmd_run() -> dict:
    population = compute_population_reference()
    refit = refit_with_k_ref(population["train_rows"], population["test_rows"])

    all_rows = population["train_rows"] + population["test_rows"]
    n_dominates = sum(1 for r in all_rows if r["line_search_dominates"])
    dominant_rows = [r for r in all_rows if r["line_search_dominates"]]
    dominance_ratios = [r["k_ref"] / r["kappa_lambda1"] for r in dominant_rows]

    seed_314_row = next((r for r in all_rows if r["n_dim"] == 40 and r["seed"] == 314), None)

    result = {
        "config": {
            "x_floor": X_FLOOR,
            "x_hi": X_HI,
            "n_train": len(population["train_rows"]),
            "n_test": len(population["test_rows"]),
        },
        "dominance_summary": {
            "n_total": len(all_rows),
            "n_line_search_dominates": n_dominates,
            "fraction_dominates": n_dominates / len(all_rows),
            "dominance_ratio_min": min(dominance_ratios) if dominance_ratios else None,
            "dominance_ratio_max": max(dominance_ratios) if dominance_ratios else None,
        },
        "positive_control_seed_314": seed_314_row,
        "refit_with_k_ref": refit,
        "rmse_reference_shallow_h_b2_1x": H_B2_1X_RESULT["rmse_expanded_model_on_fresh_test"],
        "train_rows": population["train_rows"],
        "test_rows": population["test_rows"],
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in result.items() if k not in ("train_rows", "test_rows")},
            indent=2,
        )
    )
    return result


if __name__ == "__main__":
    cmd_run()
