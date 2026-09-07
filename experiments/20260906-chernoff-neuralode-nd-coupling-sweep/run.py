"""H-B2-1h: sweep coupling_magnitude and characterize M1's functional-form scaling.

Reconstructs H-B2-1f/H-B2-1g's own matrix-construction logic (same EIGENVALUES, SEED, N_DIM)
as a LOCAL, explicitly-parameterized `build_matrix(coupling_magnitude)` -- necessary because
H-B2-1g's own `measure_m1_with_w` closes over a module-level global `A` rather than accepting
one as a parameter, so it cannot be called with a different matrix per sweep point. `measure_m1`
mirrors H-B2-1g's own measurement formula exactly (verified by
test_measure_m1_matches_h_b2_1g_own_module_level_result_exactly), just parameterized by `A`.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent

_G_DIR = HERE.parent / "20260906-chernoff-neuralode-nd-strong-coupling"
_SPEC_G = importlib.util.spec_from_file_location("chernoff_1g_run", _G_DIR / "run.py")
h2_1g = importlib.util.module_from_spec(_SPEC_G)
_SPEC_G.loader.exec_module(h2_1g)

EIGENVALUES = h2_1g.EIGENVALUES
N_DIM = h2_1g.N_DIM
SEED = h2_1g.SEED
W = h2_1g.W

COUPLING_VALUES = (3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 21.0, 24.0, 27.0, 30.0)
T_MAX = 1.0


def build_matrix(coupling_magnitude: float) -> np.ndarray:
    """Mirror H-B2-1f/g's own A-construction exactly, parameterized by coupling_magnitude."""
    rng = np.random.default_rng(SEED)
    a = np.diag(EIGENVALUES)
    coupling = rng.uniform(-coupling_magnitude, coupling_magnitude, size=(N_DIM, N_DIM))
    return a + np.triu(coupling, k=1)


def measure_m1(a: np.ndarray, t_max: float, w: float, n_grid: int = 1000) -> float:
    """Mirror H-B2-1g's own measure_m1_with_w formula exactly, parameterized by `a`."""
    ts = np.linspace(t_max / n_grid, t_max, n_grid)
    ratios = [np.linalg.norm(expm(t * a), ord=2) / np.exp(w * t) for t in ts]
    return float(max(ratios))


def _r_squared(y: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def _exp_model(x: np.ndarray, amp: float, rate: float) -> np.ndarray:
    return amp * np.exp(rate * x)


def _consecutive_ratios(m1: np.ndarray) -> list[float]:
    """M1[i+1]/M1[i] at EQUALLY SPACED coupling steps. Constant ratio is the direct
    signature of true exponential growth; a monotonically DECREASING ratio (as coupling
    step is fixed) is direct evidence AGAINST exponential and consistent with polynomial
    growth -- a cheaper, more literal check than any R^2 comparison."""
    return [float(m1[i + 1] / m1[i]) for i in range(len(m1) - 1)]


def _fit_models(coupling: np.ndarray, m1: np.ndarray) -> dict:
    """Fit linear, quadratic, and exponential models, ALL evaluated by raw-space R^2 on M1
    itself, so the three are on equal footing. A naive log-linear-R^2-vs-raw-space-R^2
    comparison is apples-to-oranges (different target variables, different loss functions)
    and was caught and corrected here before being trusted -- see decision.md."""
    # Linear: M1 = a*coupling + b (fit by raw RSS)
    lin_coef = np.polyfit(coupling, m1, 1)
    lin_pred = np.polyval(lin_coef, coupling)
    lin_r2 = _r_squared(m1, lin_pred)

    # Quadratic: M1 = a*coupling^2 + b*coupling + c (fit by raw RSS)
    quad_coef = np.polyfit(coupling, m1, 2)
    quad_pred = np.polyval(quad_coef, coupling)
    quad_r2 = _r_squared(m1, quad_pred)

    # Exponential, log-linear diagnostic: log(M1) = a*coupling + b (fit by LOG-space RSS —
    # the natural test for "does log(M1) look like a straight line", kept as a diagnostic,
    # NOT used for the raw-space model comparison below).
    log_m1 = np.log(m1)
    exp_coef_logspace = np.polyfit(coupling, log_m1, 1)
    exp_pred_log = np.polyval(exp_coef_logspace, coupling)
    exp_r2_logspace = _r_squared(log_m1, exp_pred_log)

    # Exponential, fit DIRECTLY by raw RSS (nonlinear least squares) — the fair counterpart
    # to the linear/quadratic fits above, all three minimizing the SAME (raw M1) loss.
    amp0 = float(np.exp(exp_coef_logspace[1]))
    rate0 = float(exp_coef_logspace[0])
    popt, _ = curve_fit(_exp_model, coupling, m1, p0=[amp0, rate0], maxfev=20000)
    exp_pred_raw_nls = _exp_model(coupling, *popt)
    exp_r2_raw_nls = _r_squared(m1, exp_pred_raw_nls)

    return {
        "linear": {"coef": lin_coef.tolist(), "r_squared": lin_r2},
        "quadratic": {"coef": quad_coef.tolist(), "r_squared": quad_r2},
        "exponential": {
            "coef_logspace": exp_coef_logspace.tolist(),
            "r_squared_logspace": exp_r2_logspace,
            "amp_raw_nls": float(popt[0]),
            "rate_raw_nls": float(popt[1]),
            "r_squared_raw_nls": exp_r2_raw_nls,
        },
        "consecutive_ratios": _consecutive_ratios(m1),
    }


def cmd_run() -> dict:
    per_coupling = {}
    for c in COUPLING_VALUES:
        a = build_matrix(c)
        m1 = measure_m1(a, T_MAX, W)
        per_coupling[str(c)] = {"coupling_magnitude": c, "m1": m1}

    coupling_arr = np.array(COUPLING_VALUES, dtype=float)
    m1_arr = np.array([per_coupling[str(c)]["m1"] for c in COUPLING_VALUES], dtype=float)

    fits = _fit_models(coupling_arr, m1_arr)

    # Kill criterion (per claim.md, PRE-REGISTERED before this run), evaluated FAIRLY: all
    # three models compared by raw-space R^2 on M1 itself (linear/quadratic already fit that
    # way; exponential now ALSO fit by raw nonlinear least squares, not just log-linear
    # regression -- see _fit_models docstring for why the naive log-space-vs-raw-space
    # comparison was rejected before being trusted). The consecutive-ratio diagnostic below is
    # reported as a SEPARATE finding, not folded into this gate -- adding a new override rule
    # to the verdict after seeing the data would be exactly the post-hoc goalpost-move the
    # Minimal Relaxation Rule / AOG discipline forbids. See decision.md for the caveat this
    # diagnostic supports.
    exp_r2_raw = fits["exponential"]["r_squared_raw_nls"]
    lin_r2 = fits["linear"]["r_squared"]
    quad_r2 = fits["quadratic"]["r_squared"]
    ratios = fits["consecutive_ratios"]
    ratio_monotone_decreasing = all(ratios[i] > ratios[i + 1] for i in range(len(ratios) - 1))
    if exp_r2_raw > 0.9 and exp_r2_raw > max(lin_r2, quad_r2):
        verdict = "CONFIRMED"
    elif max(lin_r2, quad_r2) >= exp_r2_raw:
        verdict = "REJECTED"
    else:
        verdict = "AMBIGUOUS"

    # Cross-check against H-B2-1f/g's own already-committed values (regression provenance).
    provenance_check = {
        "coupling_3_m1": per_coupling["3.0"]["m1"],
        "coupling_3_expected_from_h_b2_1f": 2.665,
        "coupling_15_m1": per_coupling["15.0"]["m1"],
        "coupling_15_expected_from_h_b2_1g": 158.93,
    }

    result = {
        "per_coupling": per_coupling,
        "fits": fits,
        "verdict": verdict,
        "ratio_monotone_decreasing": ratio_monotone_decreasing,
        "provenance_check": provenance_check,
        "eigenvalues": EIGENVALUES.tolist(),
        "seed": SEED,
        "w": W,
        "t_max": T_MAX,
    }

    out_path = HERE / "metrics" / "run.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
