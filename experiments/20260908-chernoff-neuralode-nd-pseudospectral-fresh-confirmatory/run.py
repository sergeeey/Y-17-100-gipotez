"""run.py — H-B2-1t: fresh-seed confirmatory replication of pseudospectral abscissa at N=40,50
(user's own Priority 2, gated on H-B2-1s's Priority 1 cross-implementation check passing).
kappa(V) and omega(A) are pre-registered COMPARATORS on the identical fresh matrices, not new
hypotheses -- their arc-wide status (hard_killed at N>=40, H-B2-1q) is stated in claim.md BEFORE
this code ran.

Reuses eigenvector_condition_number (H-B2-1l), numerical_abscissa (H-B2-1n), pseudospectral_abscissa
(H-B2-1r), build_matrix_with_seed_and_n (H-B2-1m), and measure_m1 (H-B2-1k) UNCHANGED via dynamic
import (Minimal Relaxation Rule) -- nothing computational is new in this experiment, only the
seed range and the three-way side-by-side comparison on identical fresh data.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_K_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-dimension-sweep"
_SPEC_K = importlib.util.spec_from_file_location("chernoff_1k_run", _K_DIR / "run.py")
dim_sweep = importlib.util.module_from_spec(_SPEC_K)
_SPEC_K.loader.exec_module(dim_sweep)

_L_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-eigenvector-conditioning"
_SPEC_L = importlib.util.spec_from_file_location("chernoff_1l_run", _L_DIR / "run.py")
eig_cond = importlib.util.module_from_spec(_SPEC_L)
_SPEC_L.loader.exec_module(eig_cond)

_M_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("chernoff_1m_run", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_N_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-numerical-abscissa"
_SPEC_N = importlib.util.spec_from_file_location("chernoff_1n_run", _N_DIR / "run.py")
omega_mod = importlib.util.module_from_spec(_SPEC_N)
_SPEC_N.loader.exec_module(omega_mod)

_R_DIR = HERE.parent / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
_SPEC_R = importlib.util.spec_from_file_location("chernoff_1r_run", _R_DIR / "run.py")
alpha_mod = importlib.util.module_from_spec(_SPEC_R)
_SPEC_R.loader.exec_module(alpha_mod)

N_DIM_VALUES = (40, 50)  # user's own "primary large-N regime"
SEED_START = 300  # fresh -- zero overlap with EVERY prior range in the arc (0-39, 40-99, 0-59,
SEED_END = 340  # 100-159), not just at N=40,50 specifically. 40 seeds/slice, 80 total pairs.
ALPHA = 0.05


def cmd_run() -> dict:
    per_n_slice = {}

    for n_dim in N_DIM_VALUES:
        kappa_v = []
        omega_a = []
        alpha_eps = []
        m1s = []
        per_seed = {}
        for seed in range(SEED_START, SEED_END):
            a = multin.build_matrix_with_seed_and_n(n_dim, seed)
            k = eig_cond.eigenvector_condition_number(a)
            o = omega_mod.numerical_abscissa(a)
            ae = alpha_mod.pseudospectral_abscissa(a)
            m1 = dim_sweep.measure_m1(a, dim_sweep.T_MAX, dim_sweep.W)
            kappa_v.append(k)
            omega_a.append(o)
            alpha_eps.append(ae)
            m1s.append(m1)
            per_seed[str(seed)] = {
                "kappa_v": k,
                "omega_a": o,
                "alpha_eps": ae,
                "m1": m1,
            }

        def _slice_stats(descriptor_values: list[float], m1_values: list[float]) -> dict:
            rho, p = spearmanr(descriptor_values, m1_values)
            return {
                "rho": float(rho),
                "p": float(p),
                "significant_positive": bool(p < ALPHA and rho > 0),
            }

        per_n_slice[str(n_dim)] = {
            "n_dim": n_dim,
            "n_seeds": SEED_END - SEED_START,
            "seed_range": [SEED_START, SEED_END],
            "kappa_v_vs_m1": _slice_stats(kappa_v, m1s),
            "omega_a_vs_m1": _slice_stats(omega_a, m1s),
            "alpha_eps_vs_m1": _slice_stats(alpha_eps, m1s),
            "per_seed": per_seed,
        }

    primary_criterion_met = all(
        v["alpha_eps_vs_m1"]["significant_positive"] for v in per_n_slice.values()
    )
    verdict = "CONFIRMED" if primary_criterion_met else "REJECTED"

    comparator_predictions_held = all(
        not v["kappa_v_vs_m1"]["significant_positive"]
        and not v["omega_a_vs_m1"]["significant_positive"]
        for v in per_n_slice.values()
    )

    result = {
        "config": {
            "n_dim_values": list(N_DIM_VALUES),
            "seed_range": [SEED_START, SEED_END],
            "n_seeds_per_slice": SEED_END - SEED_START,
            "population_note": (
                "Fresh seeds 300-339 -- zero overlap with every prior seed range used anywhere "
                "in the H-B2-1* arc (0-39, 40-99, 0-59, 100-159), at any N_DIM."
            ),
        },
        "per_n_slice": per_n_slice,
        "primary_criterion": {
            "descriptor": "pseudospectral_abscissa",
            "pre_registered_threshold": ALPHA,
            "met": primary_criterion_met,
        },
        "comparator_predictions": {
            "expected": (
                "kappa(V) and omega(A) remain non-significant at N=40,50 (H-B2-1q hard_killed)"
            ),
            "held": comparator_predictions_held,
        },
        "verdict": verdict,
        "verdict_note": (
            "CONFIRMED: pseudospectral abscissa individually significant, positive, at BOTH "
            "N=40 and N=50 on fresh seeds never used elsewhere in this arc -- replicates "
            "H-B2-1r/H-B2-1s on independent data. REJECTED: loses significance at either slice "
            "-- would require investigating why 3 prior verification passes missed this."
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_n_slice"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
