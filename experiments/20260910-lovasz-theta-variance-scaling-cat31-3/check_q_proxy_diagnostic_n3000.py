"""Extension of check_q_proxy_diagnostic.py to n=3000 -- same logic, isolated run since
n=3000 is the expensive point (~43s/rep at 40 reps, per H-CAT31-3's own sweep timing).
Run separately so it doesn't block the cheaper n=32..1536 points, then merged into
metrics/q_proxy_diagnostic.json by merge_q_proxy_results.py.
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"

RNG_SEED_BASE = 332000  # SAME base as check_q_proxy_diagnostic.py -- n*1000+i makes n=3000
# seeds disjoint from n=32/128/512/1536 seeds by construction (different n multiplier).


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("h_cat31_3_qdiag3000_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
theta_via_lp = h_cat31_1.theta_via_lp

N, REPS = 3000, 40  # matches H-CAT31-3's own sweep rep count at n=3000


def run() -> dict:
    m = (N - 1) // 2
    t0 = time.time()
    Q_arr = np.empty(REPS)
    X_arr = np.empty(REPS)
    for i in range(REPS):
        seed = RNG_SEED_BASE + N * 1000 + i
        c = sample_circulant_neighbors(N, 0.5, seed)
        q = round(c[1 : m + 1].sum())
        theta = theta_via_lp(c)
        Q_arr[i] = q
        X_arr[i] = np.log(theta / np.sqrt(N))
    elapsed = time.time() - t0

    valid = (Q_arr > 0) & (Q_arr < m)
    n_dropped = REPS - int(valid.sum())
    Qv, Xv = Q_arr[valid], X_arr[valid]
    D = 0.5 * np.log((m - Qv) / Qv)

    slope, intercept = np.polyfit(D, Xv, 1)
    pred = intercept + slope * D
    resid = Xv - pred
    var_X = float(np.var(Xv, ddof=1))
    var_D = float(np.var(D, ddof=1))
    var_resid = float(np.var(resid, ddof=1))
    r, _ = stats.pearsonr(D, Xv)
    r2 = float(r**2)

    row = {
        "n": N,
        "m": m,
        "reps": REPS,
        "n_dropped_degenerate_Q": n_dropped,
        "var_X": var_X,
        "var_D_predicted_1_over_m": 1.0 / m,
        "var_D_empirical": var_D,
        "pearson_r": float(r),
        "r_squared": r2,
        "ols_slope_b": float(slope),
        "ols_intercept_a": float(intercept),
        "var_residual": var_resid,
        "residual_fraction_of_var_X": var_resid / var_X if var_X > 0 else float("nan"),
        "n_times_var_X": N * var_X,
        "n_times_var_residual": N * var_resid,
        "elapsed_seconds": elapsed,
    }
    print(
        f"n={N:5d} reps={REPS:4d}(-{n_dropped}) r^2={r2:.4f} b={slope:.4f} "
        f"var_X={var_X:.6e} var_resid={var_resid:.6e} "
        f"resid_frac={var_resid / var_X:.3f} n*var_X={N * var_X:.4f} "
        f"n*var_resid={N * var_resid:.4f} elapsed={elapsed:.1f}s",
        flush=True,
    )
    return row


if __name__ == "__main__":
    row = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "q_proxy_diagnostic_n3000.json", "w", encoding="utf-8") as f:
        json.dump(row, f, indent=2)
    print(json.dumps(row, indent=2))
