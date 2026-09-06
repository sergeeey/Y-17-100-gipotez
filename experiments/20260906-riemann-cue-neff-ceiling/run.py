"""run.py — H-B1-1c: does the H-B1-1a excess match Nishigaki's finite-N_eff CUE prediction?

Reuses the already-validated r_stat()/mean_r() pipeline from the sibling experiment
(20260906-riemann-rstat-gue) instead of reimplementing it -- same tested code, same cached,
sha256-verified data file.

Formulas [VERIFIED against primary source, arxiv.org/pdf/2507.10193v1, pp.12-14]:
    N_e(T)        = (1/sqrt(12*LAMBDA)) * log(T / (2*pi))                        Eq. (42)
    E_R_INF       = 0.5997504209...   (exact sine-kernel / N->inf limit)         p.14
    predicted relative deviation = FIT_COEF * N_e(T) ** FIT_EXP                  Fig. 6 fit
LAMBDA = 1.573151071... is the Bogomolny-Bohigas-Leboeuf-Monastra (2006) arithmetic constant.
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "20260906-riemann-rstat-gue"
DATA = SIBLING / "data" / "zeros1.txt"

_spec = importlib.util.spec_from_file_location("riemann_run", SIBLING / "run.py")
sibling_run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sibling_run)

LAMBDA = 1.573151071
E_R_INF = 0.5997504209  # exact sine-kernel limit, Nishigaki 2025 p.14
FIT_COEF = 0.1896  # Fig. 6 fitted coefficient
FIT_EXP = -3.081  # Fig. 6 fitted exponent


def n_eff(t: float) -> float:
    return (1.0 / math.sqrt(12.0 * LAMBDA)) * math.log(t / (2.0 * math.pi))


def predicted_relative_deviation(t: float) -> float:
    return FIT_COEF * n_eff(t) ** FIT_EXP


def main() -> dict:
    zeros = np.array([float(x) for x in DATA.read_text(encoding="utf-8").split()])
    assert zeros.size == 100_000, f"expected cached 100k zeros, got {zeros.size}"

    r_cumulative = sibling_run.mean_r(zeros)  # same value as H-B1-1a's r_mean = 0.61092...
    r_last_half = sibling_run.mean_r(zeros[50_000:])  # closer to a "window around n" estimate

    t_endpoint = float(zeros[-1])  # gamma_100000, height of the last zero in the cumulative sample
    t_window_center = float(zeros[75_000])  # midpoint height of the last-50k window

    results = {}
    for label, r_obs, t_ref in (
        ("cumulative_first_100k", r_cumulative, t_endpoint),
        ("last_50k_window", r_last_half, t_window_center),
    ):
        observed_dev = r_obs / E_R_INF - 1.0
        predicted_dev = predicted_relative_deviation(t_ref)
        ratio = observed_dev / predicted_dev
        results[label] = {
            "r_observed": r_obs,
            "T_reference": t_ref,
            "N_eff": n_eff(t_ref),
            "observed_relative_deviation": observed_dev,
            "predicted_relative_deviation": predicted_dev,
            "ratio_observed_to_predicted": ratio,
            "verdict": "PASS" if (1 / 3) <= ratio <= 3 else "FAIL",
        }

    out = {
        "constants": {
            "LAMBDA": LAMBDA,
            "E_R_INF": E_R_INF,
            "FIT_COEF": FIT_COEF,
            "FIT_EXP": FIT_EXP,
        },
        "extrapolation_note": (
            "Fig.6 fit calibrated on n=1e8..1e23; this test applies it at n~1e5, "
            "3+ orders of magnitude below the fitted range."
        ),
        "results": results,
    }
    (HERE / "metrics" / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
