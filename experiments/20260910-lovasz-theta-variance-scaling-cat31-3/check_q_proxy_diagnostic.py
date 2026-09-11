"""Cheap structurally-motivated diagnostic for H-CAT31-3's surviving n^-0.91 law.

Tests the hypothesis (from an external Perplexity-generated analysis, NOT trusted at face
value -- independently re-derived and checked here) that most of Var(X_n),
X_n = log(theta(G)/sqrt(n)), is explained by fluctuation in Q = number of "on" generator
bits (edge-orbit density) rather than by *which* generators are on.

Re-derivation (done independently, not copied from the pasted text): with
m = (n-1)//2 independent Bernoulli(1/2) generator bits and Q ~ Bin(m, 1/2), define the
antisymmetric density proxy D_n = 0.5*log((m-Q)/Q). Writing Q = m/2 + delta,
D_n = 0.5*log((m/2-delta)/(m/2+delta)) ~= -2*delta/m for |delta| << m, so
Var(D_n) ~= (4/m^2)*Var(delta) = (4/m^2)*(m/4) = 1/m ~= 2/n. If D_n explains most of X_n's
variance, Var(X_n) should also be close to a 1/n law with a similar constant -- a genuine,
falsifiable, cheap-to-check structural hypothesis, not a fitted curve.

Reuses sample_circulant_neighbors/theta_via_lp from H-CAT31-1 UNCHANGED (Minimal Relaxation
Rule) -- only records one extra per-replicate scalar (Q) that the original sweep discarded.
Uses a SUBSET of already-tested n values (not a wider range), avoiding the most expensive
n=3000 point to keep this cheap. Per explicit user direction: compare structurally-motivated
models, do not launch a bigger sweep.
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

RNG_SEED_BASE = 332000  # distinct from H-CAT31-1 (31000) and H-CAT31-3's own sweep (331000)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("h_cat31_3_qdiag_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
theta_via_lp = h_cat31_1.theta_via_lp

# Subset of H-CAT31-3's own sweep n's -- reusing already-validated points, not a wider range.
N_REPS = [(32, 300), (128, 300), (512, 200), (1536, 100)]


def run() -> dict:
    rows = []
    for n, reps in N_REPS:
        m = (n - 1) // 2
        t0 = time.time()
        Q_arr = np.empty(reps)
        X_arr = np.empty(reps)
        for i in range(reps):
            seed = RNG_SEED_BASE + n * 1000 + i
            c = sample_circulant_neighbors(n, 0.5, seed)
            q = round(c[1 : m + 1].sum())  # number of "on" generator bits
            theta = theta_via_lp(c)
            Q_arr[i] = q
            X_arr[i] = np.log(theta / np.sqrt(n))
        elapsed = time.time() - t0

        # Guard against Q in {0, m} (D_n undefined) -- expected negligible at these m.
        valid = (Q_arr > 0) & (Q_arr < m)
        n_dropped = reps - int(valid.sum())
        Qv, Xv = Q_arr[valid], X_arr[valid]
        D = 0.5 * np.log((m - Qv) / Qv)

        # OLS: X = a + b*D + residual
        slope, intercept = np.polyfit(D, Xv, 1)
        pred = intercept + slope * D
        resid = Xv - pred
        var_X = float(np.var(Xv, ddof=1))
        var_D = float(np.var(D, ddof=1))
        var_resid = float(np.var(resid, ddof=1))
        r, _p_value = stats.pearsonr(D, Xv)
        r2 = float(r**2)

        rows.append(
            {
                "n": n,
                "m": m,
                "reps": reps,
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
                "n_times_var_X": n * var_X,
                "n_times_var_residual": n * var_resid,
                "elapsed_seconds": elapsed,
            }
        )
        print(
            f"n={n:5d} reps={reps:4d}(-{n_dropped}) r^2={r2:.4f} b={slope:.4f} "
            f"var_X={var_X:.6e} var_resid={var_resid:.6e} "
            f"resid_frac={var_resid / var_X:.3f} n*var_X={n * var_X:.4f} "
            f"n*var_resid={n * var_resid:.4f} elapsed={elapsed:.1f}s",
            flush=True,
        )
    return {"rows": rows}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "q_proxy_diagnostic.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
