"""run.py — H-B2-1z: does the closed-form eigenvalue condition number kappa(lambda_1)
(Trefethen-Embree, exact -- no pseudospectrum sampling) explain and bound H-B2-1y's
non-converging deep_k, and does refitting M1~K(A) with this EXACT proxy (available for
the FULL H-B2-1x population at near-zero cost) change the exponent finding again?

Reuses UNCHANGED via dynamic import: build_matrix_with_seed_and_n (H-B2-1m),
deep_kreiss_estimate + _alpha_eps_via_tricontour (H-B2-1y, itself reusing H-B2-1v's own
validated technique) for the Mechanism Claim Gate check only. shallow_k/m1 for the full
80+30 H-B2-1x population and deep_k for the 16 H-B2-1y matrices are NOT recomputed --
pulled directly from stored metrics/run.json, Minimal Relaxation Rule.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1z_multin", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_Y_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-kreiss-estimate-bias-check"
_SPEC_Y = importlib.util.spec_from_file_location("chernoff_1z_biascheck", _Y_DIR / "run.py")
biascheck = importlib.util.module_from_spec(_SPEC_Y)
_SPEC_Y.loader.exec_module(biascheck)

with open(_Y_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1Y_RESULT = json.load(f)

_X_DIR = HERE.parent / "20260908-chernoff-neuralode-nd-tighter-predictor-robustness"
with open(_X_DIR / "metrics" / "run.json", encoding="utf-8") as f:
    H_B2_1X_RESULT = json.load(f)

# Mechanism Claim Gate matrix -- not used anywhere else in this arc.
MECH_GATE_N_DIM = 6
MECH_GATE_SEED = 9001
MECH_GATE_EPS_VALUES = (0.01, 0.005, 0.002, 0.001, 0.0005, 0.0001, 0.00005, 0.00001, 0.000001, 1e-7)
MECH_GATE_AUTO_KWARGS = {"eps_min": 5e-8, "eps_max": 0.05, "n_circles": 40, "n_points": 120}


def eigenvalue_condition_number(a: np.ndarray) -> dict:
    """kappa(lambda_1) = 1/|w_1^H v_1| for the DOMINANT eigenvalue's unit-normalized right
    eigenvector v_1 and left eigenvector w_1 (row of V^-1) -- the standard Wilkinson
    eigenvalue condition number. Distinct from kappa(V)=cond(V) (H-B2-1m, global, hard_killed
    as an M1 predictor at N_DIM>=40) -- this is a LOCAL, single-eigenvalue quantity."""
    eigvals, v = np.linalg.eig(a)
    dom_idx = int(np.argmax(eigvals.real))
    lam = eigvals[dom_idx]
    vinv = np.linalg.inv(v)
    v_j = v[:, dom_idx]
    v_j = v_j / np.linalg.norm(v_j)
    w_j = vinv[dom_idx, :].conj()
    w_j = w_j / np.linalg.norm(w_j)
    denom = abs(np.vdot(w_j, v_j))
    kappa = float(1.0 / denom) if denom > 0 else float("inf")
    gaps = np.abs(eigvals.real - lam.real)
    gaps = gaps[gaps > 1e-12]
    min_gap = float(gaps.min()) if len(gaps) else float("inf")
    return {"kappa_lambda1": kappa, "lambda1_real": float(lam.real), "min_eig_gap": min_gap}


def mechanism_claim_gate_check() -> dict:
    """Small matrix, fine eps sweep (two orders of magnitude finer than H-B2-1y's 1e-5
    floor), using the SAME validated pipeline (deep_kreiss_estimate) H-B2-1v/1y used --
    not abstract theory, a check against this project's own numerics."""
    a = multin.build_matrix_with_seed_and_n(MECH_GATE_N_DIM, MECH_GATE_SEED)
    kappa_info = eigenvalue_condition_number(a)

    spectral_abscissa = float(np.max(np.linalg.eigvals(a).real))
    import pseudopy

    pspec = pseudopy.NonnormalAuto(a, **MECH_GATE_AUTO_KWARGS)
    ratios = {}
    for eps in MECH_GATE_EPS_VALUES:
        alpha_eps = biascheck._alpha_eps_via_tricontour(pspec, eps)
        ratios[str(eps)] = None if alpha_eps is None else (alpha_eps - spectral_abscissa) / eps
    valid_eps = [(float(k), v) for k, v in ratios.items() if v is not None]
    valid_eps.sort(key=lambda t: t[0], reverse=True)  # largest eps (coarsest) first
    values = [v for _, v in valid_eps]
    monotonic_increasing = all(values[i] <= values[i + 1] + 1e-9 for i in range(len(values) - 1))
    finest_ratio = values[-1] if values else None
    pct_of_kappa_at_finest = (
        100.0 * finest_ratio / kappa_info["kappa_lambda1"] if finest_ratio is not None else None
    )
    return {
        "n_dim": MECH_GATE_N_DIM,
        "seed": MECH_GATE_SEED,
        "spectral_abscissa": spectral_abscissa,
        "kappa_lambda1": kappa_info["kappa_lambda1"],
        "min_eig_gap": kappa_info["min_eig_gap"],
        "ratios_by_eps": ratios,
        "monotonic_increasing": bool(monotonic_increasing),
        "finest_ratio": finest_ratio,
        "pct_of_kappa_at_finest_eps": pct_of_kappa_at_finest,
        "gate_holds": bool(
            monotonic_increasing
            and pct_of_kappa_at_finest is not None
            and pct_of_kappa_at_finest >= 90.0
        ),
    }


def compare_kappa_vs_deep_k() -> dict:
    """For H-B2-1y's own 16 matrices: does kappa(lambda_1) bound deep_k in all 16/16 cases?"""
    rows = []
    for key, row in H_B2_1Y_RESULT["per_matrix"].items():
        a = multin.build_matrix_with_seed_and_n(row["n_dim"], row["seed"])
        kappa_info = eigenvalue_condition_number(a)
        deep_k = row["deep_k"]
        ratio = deep_k / kappa_info["kappa_lambda1"] if kappa_info["kappa_lambda1"] > 0 else None
        rows.append(
            {
                "key": key,
                "n_dim": row["n_dim"],
                "seed": row["seed"],
                "shallow_k": row["shallow_k"],
                "deep_k": deep_k,
                "kappa_lambda1": kappa_info["kappa_lambda1"],
                "min_eig_gap": kappa_info["min_eig_gap"],
                "deep_k_over_kappa": ratio,
                "deep_k_exceeds_kappa": bool(ratio is not None and ratio > 1.0),
            }
        )
    n_exceeds = sum(1 for r in rows if r["deep_k_exceeds_kappa"])
    ratios = [r["deep_k_over_kappa"] for r in rows if r["deep_k_over_kappa"] is not None]
    return {
        "rows": rows,
        "n_matrices": len(rows),
        "n_deep_k_exceeds_kappa": n_exceeds,
        "claim1_supported": bool(n_exceeds == 0),
        "ratio_min": min(ratios) if ratios else None,
        "ratio_max": max(ratios) if ratios else None,
        "ratio_median": sorted(ratios)[len(ratios) // 2] if ratios else None,
    }


def _fit_ols(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    coeffs, *_ = np.linalg.lstsq(x, y, rcond=None)
    return coeffs


def refit_m1_with_kappa() -> dict:
    """Same train/test split H-B2-1x used (80 train, 30 fresh test). Two models, to keep
    two separate comparisons both honest: (1) single-feature (intercept + log(K)) for the
    EXPONENT comparison against H-B2-1y's own single-feature deep-K fit; (2) two-feature
    (intercept + log(K) + log(N_DIM)) for the RMSE comparison, matching H-B2-1x's OWN
    model exactly (verified by reading its run.py: x_train = [1, log_k, log_n], NOT
    single-feature despite the "expanded" name -- that name refers to the expanded 80-row
    TRAINING SET, not an expanded feature set. An earlier draft of this file wrongly
    assumed single-feature and is corrected here). K = kappa(lambda_1), computed for free
    (no pseudopy) for the FULL population, not just 16 matrices."""
    train_rows = []
    for r in H_B2_1X_RESULT["train_data"]:
        a = multin.build_matrix_with_seed_and_n(r["n_dim"], r["seed"])
        kappa_info = eigenvalue_condition_number(a)
        train_rows.append({**r, "kappa_lambda1": kappa_info["kappa_lambda1"]})

    test_rows = []
    for r in H_B2_1X_RESULT["test_data"]:
        a = multin.build_matrix_with_seed_and_n(r["n_dim"], r["seed"])
        kappa_info = eigenvalue_condition_number(a)
        test_rows.append({**r, "kappa_lambda1": kappa_info["kappa_lambda1"]})

    log_kappa_train = np.log(np.array([r["kappa_lambda1"] for r in train_rows]))
    log_m1_train = np.log(np.array([r["m1"] for r in train_rows]))
    log_n_train = np.log(np.array([r["n_dim"] for r in train_rows], dtype=float))

    log_kappa_test = np.log(np.array([r["kappa_lambda1"] for r in test_rows]))
    log_m1_test = np.log(np.array([r["m1"] for r in test_rows]))
    log_n_test = np.log(np.array([r["n_dim"] for r in test_rows], dtype=float))

    # (1) single-feature: intercept + log(kappa) -- for the EXPONENT comparison
    x_train_1f = np.column_stack([np.ones_like(log_kappa_train), log_kappa_train])
    coeffs_1f = _fit_ols(x_train_1f, log_m1_train)
    kappa_exponent = float(coeffs_1f[1])
    x_test_1f = np.column_stack([np.ones_like(log_kappa_test), log_kappa_test])
    rmse_1f = float(np.sqrt(np.mean((x_test_1f @ coeffs_1f - log_m1_test) ** 2)))

    # (2) two-feature: intercept + log(kappa) + log(N_DIM) -- matches H-B2-1x's own model
    # exactly, for the RMSE comparison against its stored reference value
    x_train_2f = np.column_stack([np.ones_like(log_kappa_train), log_kappa_train, log_n_train])
    coeffs_2f = _fit_ols(x_train_2f, log_m1_train)
    x_test_2f = np.column_stack([np.ones_like(log_kappa_test), log_kappa_test, log_n_test])
    rmse_2f = float(np.sqrt(np.mean((x_test_2f @ coeffs_2f - log_m1_test) ** 2)))

    return {
        "n_train": len(train_rows),
        "n_test": len(test_rows),
        "single_feature_kappa_intercept": float(coeffs_1f[0]),
        "single_feature_kappa_exponent": kappa_exponent,
        "single_feature_rmse_kappa_model_on_fresh_test": rmse_1f,
        "two_feature_kappa_intercept": float(coeffs_2f[0]),
        "two_feature_kappa_exponent": float(coeffs_2f[1]),
        "two_feature_n_dim_exponent": float(coeffs_2f[2]),
        "two_feature_rmse_kappa_model_on_fresh_test": rmse_2f,
        "rmse_shallow_k_model_h_b2_1x_reference": H_B2_1X_RESULT[
            "rmse_expanded_model_on_fresh_test"
        ],
        "train_rows": train_rows,
        "test_rows": test_rows,
    }


def cmd_run() -> dict:
    mech_gate = mechanism_claim_gate_check()
    comparison = compare_kappa_vs_deep_k()
    refit = refit_m1_with_kappa()

    if mech_gate["gate_holds"] and comparison["claim1_supported"]:
        verdict = "KAPPA_LAMBDA1_CONFIRMED_AS_CONVERGENT_ANCHOR"
    elif comparison["claim1_supported"] and not mech_gate["gate_holds"]:
        verdict = "CLAIM1_SUPPORTED_BUT_MECHANISM_GATE_INCONCLUSIVE"
    else:
        verdict = "CLAIM1_REJECTED"

    result = {
        "mechanism_claim_gate": mech_gate,
        "kappa_vs_deep_k_comparison": {k: v for k, v in comparison.items() if k != "rows"},
        "kappa_vs_deep_k_rows": comparison["rows"],
        "refit_with_kappa": {
            k: v for k, v in refit.items() if k not in ("train_rows", "test_rows")
        },
        "refit_train_rows": refit["train_rows"],
        "refit_test_rows": refit["test_rows"],
        "verdict": verdict,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                k: v
                for k, v in result.items()
                if k not in ("kappa_vs_deep_k_rows", "refit_train_rows", "refit_test_rows")
            },
            indent=2,
        )
    )
    return result


if __name__ == "__main__":
    cmd_run()
