"""H-B2-3 -- does the K_ref-based transient-growth predictor track a genuine
dimensionless mechanism (time window T, rate W) or just the original matrix
family's own idiosyncrasies?

Reuses, via distinct-name imports (avoids the `run.py`-name collision bug
caught in H-CAT37-2): build_matrix_with_seed_and_n (H-B2-1x population),
resolvent_reference_k (H-B2-2).
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent

W = 0.5  # matches dim_sweep.W / POSITIVE_EIGENVALUE throughout the H-B2 arc
N_GRID = 1000  # matches measure_m1's own convention


def _load_module(name: str, rel_path: str):
    path = EXPERIMENTS / rel_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


multin = _load_module("h_b2_3_multin", "20260907-chernoff-neuralode-nd-multiseed-multin/run.py")
kref_module = _load_module(
    "h_b2_3_kref", "20260908-chernoff-neuralode-nd-kreiss-resolvent-reference/run.py"
)
build_matrix_with_seed_and_n = multin.build_matrix_with_seed_and_n
resolvent_reference_k = kref_module.resolvent_reference_k

with open(
    EXPERIMENTS
    / "20260908-chernoff-neuralode-nd-tighter-predictor-robustness"
    / "metrics"
    / "run.json",
    encoding="utf-8",
) as f:
    H_B2_1X_RESULT = json.load(f)


def measure_m_t_w(a: np.ndarray, t_max: float, w: float, n_grid: int = N_GRID) -> float:
    """M_T,W(B) = max_{0<t<=T} ||exp(tB)||_2 / exp(w*t). Generalizes the arc's
    own `measure_m1` (fixed T_MAX=1.0) to an explicit T parameter."""
    ts = np.linspace(t_max / n_grid, t_max, n_grid)
    ratios = [np.linalg.norm(expm(t * a), ord=2) / np.exp(w * t) for t in ts]
    return float(max(ratios))


def dimensionless_matrix(a: np.ndarray, w: float, t: float) -> np.ndarray:
    """C = T*(A - W*I). See claim.md's Mechanism Claim Gate: M_T,W(A) = M_1,0(C)
    exactly (B and W*I commute, substitute tau=t/T)."""
    n = a.shape[0]
    return t * (a - w * np.eye(n))


def build_rotation_block_matrix(
    n_dim: int, seed: int, coupling_magnitude: float = 15.0
) -> np.ndarray:
    """A structurally DIFFERENT family from `build_matrix_with_seed_and_n`:
    genuinely complex eigenvalue pairs (2x2 rotation blocks, negative real
    part, varying frequency) instead of the original's always-real,
    strictly-upper-triangular-only structure. One block is forced to have
    real part +0.5 (matching W) so the target's normalization stays
    meaningful; the rest decay.

    WHY the coupling is masked by block, not just `np.triu(..., k=1)` (found
    this session, not assumed): a plain element-wise strictly-upper-
    triangular mask cuts THROUGH a 2x2 block's own off-diagonal entry
    (position (i, i+1) inside a block IS in the matrix's strict upper
    triangle), corrupting that block's intended eigenvalues. Diagnosed
    directly: `max_re_eig` of the FULL matrix came back as 3.36, 5.43, etc.
    instead of the intended set {0.5, <=-0.5} -- and the resulting
    ill-conditioned matrices made `resolvent_reference_k` return `inf` for
    several (n, seed) pairs (RuntimeWarning: overflow in SVD). Fixed by
    zeroing coupling entries whose row and column fall in the SAME block --
    a genuinely block-upper-triangular perturbation preserves the diagonal
    blocks' eigenvalues exactly, regardless of its own magnitude.
    """
    rng = np.random.default_rng(np.random.SeedSequence([n_dim, seed, 99999]))
    blocks = []
    remaining = n_dim
    first = True
    while remaining > 0:
        if remaining == 1:
            blocks.append(np.array([[-1.0]]))
            remaining -= 1
            continue
        size = 2
        if first:
            rate, omega = 0.5, 0.0  # the one growing, non-oscillatory mode (matches W)
            first = False
        else:
            rate = rng.uniform(-3.0, -0.5)
            omega = rng.uniform(0.5, 5.0)
        blocks.append(np.array([[rate, -omega], [omega, rate]]))
        remaining -= size
    base = np.zeros((n_dim, n_dim))
    block_id = np.empty(n_dim, dtype=int)
    i = 0
    for bi, blk in enumerate(blocks):
        s = blk.shape[0]
        base[i : i + s, i : i + s] = blk
        block_id[i : i + s] = bi
        i += s
    coupling = rng.uniform(-coupling_magnitude, coupling_magnitude, size=(n_dim, n_dim))
    same_block = block_id[:, None] == block_id[None, :]
    mask = np.triu(np.ones((n_dim, n_dim), dtype=bool), k=1) & ~same_block
    return base + np.where(mask, coupling, 0.0)


def fit_power_law(k_values: np.ndarray, m_values: np.ndarray) -> dict:
    log_k = np.log(k_values)
    log_m = np.log(m_values)
    x = np.column_stack([np.ones_like(log_k), log_k])
    coeffs, *_ = np.linalg.lstsq(x, log_m, rcond=None)
    return {"intercept": float(coeffs[0]), "exponent": float(coeffs[1])}


def predict(k_values: np.ndarray, fit: dict) -> np.ndarray:
    return np.exp(fit["intercept"] + fit["exponent"] * np.log(k_values))


def rmse_log(pred: np.ndarray, actual: np.ndarray) -> float:
    return float(np.sqrt(np.mean((np.log(pred) - np.log(actual)) ** 2)))


def cmd_run():
    # --- Fit on original family, T=1 (matches the arc's own established convention) ---
    train_k, train_m = [], []
    for r in H_B2_1X_RESULT["train_data"]:
        a = build_matrix_with_seed_and_n(r["n_dim"], r["seed"])
        c = dimensionless_matrix(a, W, 1.0)
        k = resolvent_reference_k(c)["k_ref"]
        train_k.append(k)
        train_m.append(measure_m_t_w(a, 1.0, W))
    fit = fit_power_law(np.array(train_k), np.array(train_m))

    results = {"claim": "H-B2-3 transferable dimensionless predictor", "fit": fit}

    # --- Transfer A: same family, new T, on the arc's own held-out test split ---
    transfer_a = {}
    for T in (0.1, 0.3, 1.0, 3.0, 10.0):
        preds, actuals = [], []
        for r in H_B2_1X_RESULT["test_data"]:
            a = build_matrix_with_seed_and_n(r["n_dim"], r["seed"])
            c = dimensionless_matrix(a, W, T)
            k = resolvent_reference_k(c)["k_ref"]
            preds.append(predict(np.array([k]), fit)[0])
            actuals.append(measure_m_t_w(a, T, W))
        transfer_a[str(T)] = {
            "rmse_log": rmse_log(np.array(preds), np.array(actuals)),
            "n": len(preds),
        }
    results["transfer_a_same_family_new_T"] = transfer_a

    # --- Transfer B: new family, T=1 ---
    transfer_b_preds, transfer_b_actuals = [], []
    n_dims_new_family = [10, 16, 20, 30, 40]
    seeds_new_family = range(500, 508)
    for n_dim in n_dims_new_family:
        for seed in seeds_new_family:
            a = build_rotation_block_matrix(n_dim, seed)
            c = dimensionless_matrix(a, W, 1.0)
            k = resolvent_reference_k(c)["k_ref"]
            transfer_b_preds.append(predict(np.array([k]), fit)[0])
            transfer_b_actuals.append(measure_m_t_w(a, 1.0, W))
    results["transfer_b_new_family_T1"] = {
        "rmse_log": rmse_log(np.array(transfer_b_preds), np.array(transfer_b_actuals)),
        "n": len(transfer_b_preds),
    }

    # --- Transfer C: new family, new T ---
    transfer_c = {}
    for T in (0.3, 3.0):
        preds, actuals = [], []
        for n_dim in n_dims_new_family:
            for seed in seeds_new_family:
                a = build_rotation_block_matrix(n_dim, seed)
                c = dimensionless_matrix(a, W, T)
                k = resolvent_reference_k(c)["k_ref"]
                preds.append(predict(np.array([k]), fit)[0])
                actuals.append(measure_m_t_w(a, T, W))
        transfer_c[str(T)] = {
            "rmse_log": rmse_log(np.array(preds), np.array(actuals)),
            "n": len(preds),
        }
    results["transfer_c_new_family_new_T"] = transfer_c

    # --- Compute-cost comparison, one representative matrix ---
    a_sample = build_matrix_with_seed_and_n(40, H_B2_1X_RESULT["test_data"][0]["seed"])
    t0 = time.perf_counter()
    c_sample = dimensionless_matrix(a_sample, W, 1.0)
    _ = resolvent_reference_k(c_sample)["k_ref"]
    predictor_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    _ = measure_m_t_w(a_sample, 1.0, W, n_grid=N_GRID)
    direct_time = time.perf_counter() - t0

    results["compute_cost_seconds"] = {
        "predictor_path_one_matrix": predictor_time,
        "direct_grid_path_one_matrix": direct_time,
        "n_grid_used_for_direct": N_GRID,
    }

    Path(HERE / "metrics").mkdir(exist_ok=True)
    with open(HERE / "metrics" / "run.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(json.dumps(results, indent=2, default=str))
    return results


if __name__ == "__main__":
    cmd_run()
