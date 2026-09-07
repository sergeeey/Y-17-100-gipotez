"""run.py — H-B2-1k: is M1(N_DIM) monotonic, at a FIXED spectral range [-50,-1] (only the number
of eigenvalues packed into that range varies)? Isolates dimension from spectral range, unlike
H-B2-1j's own convention (most-negative-eigenvalue = -N_DIM), which confounded the two.

Falsifiable prediction from H-B2-1j's own pearl registry entry (impact 7): if intermediate N is
tested, M1 should show a NON-monotonic profile, not simple decrease-then-increase.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

SPECTRAL_RANGE = (-50.0, -1.0)  # fixed for every N_DIM -- the point of this experiment
POSITIVE_EIGENVALUE = 0.5
W = 0.5
SEED = 0  # matches every prior H-B2-1* experiment
COUPLING_MAGNITUDE = 15.0  # matches H-B2-1g/H-B2-1j's own tested value
T_MAX = 1.0

N_DIM_VALUES = (3, 4, 8, 12, 16, 24, 32, 40, 50)
# N=2 deliberately excluded: with only 1 negative eigenvalue, np.linspace(range[0], range[1], 1)
# returns just the start point (numpy's own documented behavior for num=1), NOT a placement that
# meaningfully spans SPECTRAL_RANGE -- would introduce a construction artifact specific to N=2,
# not a genuine dimensional effect. N=3 is the smallest N where linspace spans the range properly
# (both endpoints hit exactly). Caught by test_build_matrix_holds_spectral_range_fixed_across_n_dim
# BEFORE trusting the real run -- see decision.md.


def build_matrix(n_dim: int) -> np.ndarray:
    """One positive eigenvalue + (n_dim-1) negative eigenvalues linearly spaced across the FIXED
    SPECTRAL_RANGE (not scaled with n_dim, unlike H-B2-1j's own convention), plus random
    upper-triangular coupling U(-COUPLING_MAGNITUDE, COUPLING_MAGNITUDE), seed=SEED."""
    eigenvalues = np.concatenate(
        [[POSITIVE_EIGENVALUE], np.linspace(SPECTRAL_RANGE[0], SPECTRAL_RANGE[1], n_dim - 1)]
    )
    rng = np.random.default_rng(SEED)
    a = np.diag(eigenvalues)
    coupling = rng.uniform(-COUPLING_MAGNITUDE, COUPLING_MAGNITUDE, size=(n_dim, n_dim))
    return a + np.triu(coupling, k=1)


def measure_m1(a: np.ndarray, t_max: float, w: float, n_grid: int = 1000) -> float:
    """Byte-identical formula to every prior H-B2-1* experiment's own M1 measurement."""
    ts = np.linspace(t_max / n_grid, t_max, n_grid)
    ratios = [np.linalg.norm(expm(t * a), ord=2) / np.exp(w * t) for t in ts]
    return float(max(ratios))


def is_monotonic(values: np.ndarray) -> bool:
    diffs = np.diff(values)
    return bool(np.all(diffs > 0) or np.all(diffs < 0))


def cmd_run() -> dict:
    per_n = {}
    for n_dim in N_DIM_VALUES:
        a = build_matrix(n_dim)
        m1 = measure_m1(a, T_MAX, W)
        per_n[str(n_dim)] = {"n_dim": n_dim, "m1": m1}

    m1_values = np.array([per_n[str(n)]["m1"] for n in N_DIM_VALUES])
    consecutive_diffs = np.diff(m1_values).tolist()
    monotonic = is_monotonic(m1_values)

    verdict = "REJECTED" if monotonic else "CONFIRMED"

    result = {
        "per_n": per_n,
        "n_dim_values": list(N_DIM_VALUES),
        "m1_sequence": m1_values.tolist(),
        "consecutive_diffs": consecutive_diffs,
        "is_monotonic": monotonic,
        "verdict": verdict,
        "spectral_range": list(SPECTRAL_RANGE),
        "coupling_magnitude": COUPLING_MAGNITUDE,
        "seed": SEED,
    }

    out_path = METRICS / "run.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
