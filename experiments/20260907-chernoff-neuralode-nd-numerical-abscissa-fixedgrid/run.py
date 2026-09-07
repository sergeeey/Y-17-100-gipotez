"""run.py — H-B2-1q: pre-registered FIXED-grid replication of H-B2-1p's disputed N=64 finding.
Grid {56,64,72} was named in H-B2-1p's own decision.md BEFORE this experiment's code existed --
not chosen today in response to any result. Fresh seeds 100-159 (zero overlap with any prior
seed range used at any N_DIM in this arc).

Reuses H-B2-1m's build_matrix_with_seed_and_n, H-B2-1k's dim_sweep.measure_m1, and H-B2-1n's
numerical_abscissa UNCHANGED via dynamic import (Minimal Relaxation Rule).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_K_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-dimension-sweep"
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1k_run", _K_DIR / "run.py")
dim_sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(dim_sweep)

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1m_run", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_N_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-numerical-abscissa"
_SPEC_N = importlib.util.spec_from_file_location("chernoff_1n_run", _N_DIR / "run.py")
abscissa_1n = importlib.util.module_from_spec(_SPEC_N)
_SPEC_N.loader.exec_module(abscissa_1n)

FIXED_GRID_N_DIM_VALUES = (56, 64, 72)  # named in H-B2-1p's decision.md before this code existed
SEED_START = 100  # fresh -- zero overlap with 0-39, 40-99, or 0-59 (all used earlier in the arc)
SEED_END = 160  # exclusive -- 60 fresh seeds per slice, 180 total pairs
PRIMARY_N_DIM = 64  # the specific, pre-registered, disputed value from H-B2-1p
ALPHA = 0.05


def numerical_abscissa(a: np.ndarray) -> float:
    """Reused unchanged from H-B2-1n."""
    return abscissa_1n.numerical_abscissa(a)


def cmd_run() -> dict:
    per_n_slice = {}

    for n_dim in FIXED_GRID_N_DIM_VALUES:
        omegas = []
        m1s = []
        per_seed = {}
        for seed in range(SEED_START, SEED_END):
            a = multin.build_matrix_with_seed_and_n(n_dim, seed)
            omega = numerical_abscissa(a)
            m1 = dim_sweep.measure_m1(a, dim_sweep.T_MAX, dim_sweep.W)
            omegas.append(omega)
            m1s.append(m1)
            per_seed[str(seed)] = {"omega": omega, "m1": m1}

        rho, p = spearmanr(omegas, m1s)
        per_n_slice[str(n_dim)] = {
            "n_dim": n_dim,
            "n_seeds": SEED_END - SEED_START,
            "seed_range": [SEED_START, SEED_END],
            "spearman_rho": float(rho),
            "spearman_p": float(p),
            "omega_range": [float(min(omegas)), float(max(omegas))],
            "omega_std": float(np.std(omegas)),
            "per_seed": per_seed,
        }

    primary = per_n_slice[str(PRIMARY_N_DIM)]
    primary_significant = primary["spearman_p"] < ALPHA and primary["spearman_rho"] > 0

    verdict = "REPLICATED" if primary_significant else "NOT_REPLICATED"

    result = {
        "config": {
            "n_dim_values": list(FIXED_GRID_N_DIM_VALUES),
            "seed_range": [SEED_START, SEED_END],
            "n_seeds_per_slice": SEED_END - SEED_START,
            "primary_n_dim": PRIMARY_N_DIM,
            "population_note": (
                "Grid {56,64,72} pre-registered in H-B2-1p's decision.md before this code "
                "existed. Fresh seeds 100-159 -- zero overlap with any prior seed range used at "
                "any N_DIM in this arc (0-39, 40-99, 0-59 all used earlier)."
            ),
        },
        "per_n_slice": per_n_slice,
        "primary_criterion": {
            "n_dim": PRIMARY_N_DIM,
            "spearman_rho": primary["spearman_rho"],
            "spearman_p": primary["spearman_p"],
            "pre_registered_threshold": ALPHA,
            "note": (
                "PRE-REGISTERED PRIMARY criterion (claim.md, grid+question named in H-B2-1p's "
                "decision.md before this code existed). Tests specifically whether N=64's "
                "disputed H-B2-1p finding (rho=0.298, p=0.021, seeds 0-59) replicates on fresh, "
                "non-adaptively-selected data."
            ),
        },
        "verdict": verdict,
        "verdict_note": (
            "REPLICATED: N=64 significant, positive, on fresh pre-registered-grid data -- the "
            "H-B2-1p finding was real, not drawer-selection. NOT_REPLICATED: N=64 not "
            "significant -- H-B2-1p's N=64 result was drawer-selection; the arc-wide honest "
            "reading becomes 'solid at N in {16,32}, vanishes by N~40, does not measurably "
            "return.'"
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_n_slice"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
