"""run.py — H-B2-1l: does eigenvector-matrix conditioning kappa(V) explain M1's variation across
H-B2-1i's seed-ensemble and H-B2-1k's N-sweep? Sharpens the informal "eigenvalue clustering"
hypothesis pearled in both those experiments into a specific, classically-motivated quantity
(Trefethen & Embree: ||exp(tA)|| <= kappa(V) * max_i exp(t*Re(lambda_i)) for A = V*Lambda*V^-1).

Reuses H-B2-1i's build_matrix_with_seed and H-B2-1k's build_matrix UNCHANGED via dynamic import
-- no new stochastic draws, only the conditioning computation is new (Minimal Relaxation Rule).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_I_DIR = HERE.parent / "20260906-chernoff-neuralode-nd-multiseed"
_SPEC_I = importlib.util.spec_from_file_location("chernoff_1i_run", _I_DIR / "run.py")
multiseed = importlib.util.module_from_spec(_SPEC_I)
_SPEC_I.loader.exec_module(multiseed)

_K_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-dimension-sweep"
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1k_run", _K_DIR / "run.py")
dim_sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(dim_sweep)


def eigenvector_condition_number(a: np.ndarray) -> float:
    """kappa(V) = ||V|| * ||V^-1||, 2-norm, for A = V*Lambda*V^-1 (np.linalg.eig)."""
    _, v = np.linalg.eig(a)
    return float(np.linalg.cond(v))


def cmd_run() -> dict:
    # Population 1: H-B2-1i's own 30-seed ensemble at fixed N_DIM=8, coupling=15.
    seed_ensemble = {}
    for seed in multiseed.SEEDS:
        a = multiseed.build_matrix_with_seed(seed)
        kappa = eigenvector_condition_number(a)
        m1 = multiseed.h2_1h.measure_m1(a, multiseed.T_MAX, multiseed.W)
        seed_ensemble[str(seed)] = {"seed": seed, "kappa_v": kappa, "m1": m1}

    # Population 2: H-B2-1k's own N-sweep at fixed coupling=15, seed=0.
    n_sweep = {}
    for n_dim in dim_sweep.N_DIM_VALUES:
        a = dim_sweep.build_matrix(n_dim)
        kappa = eigenvector_condition_number(a)
        m1 = dim_sweep.measure_m1(a, dim_sweep.T_MAX, dim_sweep.W)
        n_sweep[str(n_dim)] = {"n_dim": n_dim, "kappa_v": kappa, "m1": m1}

    seed_kappa = np.array([v["kappa_v"] for v in seed_ensemble.values()])
    seed_m1 = np.array([v["m1"] for v in seed_ensemble.values()])
    seed_rho, seed_p = spearmanr(seed_kappa, seed_m1)

    n_kappa = np.array([v["kappa_v"] for v in n_sweep.values()])
    n_m1 = np.array([v["m1"] for v in n_sweep.values()])
    n_rho, n_p = spearmanr(n_kappa, n_m1)

    if seed_rho > 0 and n_rho > 0:
        verdict = "CONFIRMED"
    elif (seed_rho > 0) != (n_rho > 0):
        verdict = "MIXED"
    else:
        verdict = "REJECTED"

    result = {
        "seed_ensemble": seed_ensemble,
        "n_sweep": n_sweep,
        "correlations": {
            "seed_ensemble_spearman_rho": float(seed_rho),
            "seed_ensemble_spearman_p": float(seed_p),
            "seed_ensemble_n": len(seed_ensemble),
            "n_sweep_spearman_rho": float(n_rho),
            "n_sweep_spearman_p": float(n_p),
            "n_sweep_n": len(n_sweep),
        },
        "verdict": verdict,
    }

    out_path = METRICS / "run.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
