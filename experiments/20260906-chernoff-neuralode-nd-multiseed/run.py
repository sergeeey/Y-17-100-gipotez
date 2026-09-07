"""H-B2-1i: seed-ensemble test of M1 at fixed coupling_magnitude=15 (H-B2-1g's own value).

Is M1=158.93 (H-B2-1g, seed=0) typical, or a particularly unlucky/lucky draw? H-B2-1g's own
Relaxation Map named this untested; H-B2-1h deliberately left it open (varied coupling, not
seed, for its own comparability).

Reuses H-B2-1h's `build_matrix`/`measure_m1` (byte-for-byte the same formulas, already verified
against H-B2-1f/g's own committed numbers) but parameterizes SEED instead of coupling_magnitude
-- Minimal Relaxation Rule: one assumption changed at a time.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

_H_DIR = HERE.parent / "20260906-chernoff-neuralode-nd-coupling-sweep"
_SPEC_H = importlib.util.spec_from_file_location("chernoff_1h_run", _H_DIR / "run.py")
h2_1h = importlib.util.module_from_spec(_SPEC_H)
_SPEC_H.loader.exec_module(h2_1h)

EIGENVALUES = h2_1h.EIGENVALUES
N_DIM = h2_1h.N_DIM
W = h2_1h.W
T_MAX = h2_1h.T_MAX
COUPLING_MAGNITUDE = 15.0  # H-B2-1g's own tested value -- ONE assumption changed (seed, not this)

N_SEEDS = 30
SEEDS = tuple(range(N_SEEDS))

REFERENCE_SEED = 0  # H-B2-1g's own seed
REFERENCE_M1 = 158.93114443726702  # H-B2-1g's own committed value (provenance-verified in H-B2-1h)


def build_matrix_with_seed(seed: int, coupling_magnitude: float = COUPLING_MAGNITUDE) -> np.ndarray:
    """Same construction as H-B2-1h's build_matrix, but seed is the varied parameter."""
    rng = np.random.default_rng(seed)
    a = np.diag(EIGENVALUES)
    coupling = rng.uniform(-coupling_magnitude, coupling_magnitude, size=(N_DIM, N_DIM))
    return a + np.triu(coupling, k=1)


def _quartiles(values: np.ndarray) -> dict:
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    iqr = q3 - q1
    return {
        "q1": q1,
        "median": float(np.percentile(values, 50)),
        "q3": q3,
        "iqr": iqr,
        "tukey_lower_fence": q1 - 1.5 * iqr,
        "tukey_upper_fence": q3 + 1.5 * iqr,
    }


def cmd_run() -> dict:
    per_seed = {}
    for seed in SEEDS:
        a = build_matrix_with_seed(seed)
        m1 = h2_1h.measure_m1(a, T_MAX, W)
        per_seed[str(seed)] = {"seed": seed, "m1": m1}

    m1_values = np.array([per_seed[str(s)]["m1"] for s in SEEDS], dtype=float)
    stats = _quartiles(m1_values)

    reference_m1_this_run = per_seed[str(REFERENCE_SEED)]["m1"]

    if stats["q1"] <= REFERENCE_M1 <= stats["q3"]:
        verdict = "TYPICAL"
    elif stats["tukey_lower_fence"] <= REFERENCE_M1 <= stats["tukey_upper_fence"]:
        verdict = "MODERATE"
    else:
        verdict = "OUTLIER"

    result = {
        "per_seed": per_seed,
        "distribution_stats": {
            "n_seeds": N_SEEDS,
            "mean": float(np.mean(m1_values)),
            "std": float(np.std(m1_values)),
            "min": float(np.min(m1_values)),
            "max": float(np.max(m1_values)),
            **stats,
        },
        "reference_seed": REFERENCE_SEED,
        "reference_m1_expected_from_h_b2_1g": REFERENCE_M1,
        "reference_m1_this_run": reference_m1_this_run,
        "provenance_check_ok": abs(reference_m1_this_run - REFERENCE_M1) < 1.0,
        "verdict": verdict,
        "coupling_magnitude": COUPLING_MAGNITUDE,
        "eigenvalues": EIGENVALUES.tolist(),
    }

    out_path = HERE / "metrics" / "run.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
