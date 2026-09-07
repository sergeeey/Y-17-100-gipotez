"""H-B3-1m: V2 two-part detection rule (tau>=0.5 AND a Pettitt level-shift test) -- H-B3-1b's
own Relaxation Map Row 2, the last of its 3 originally-named fixes to be tried.

Reuses H-B3-1/H-B3-1b's own pipeline (load_series, rolling_stat, betti1_entropy_series,
expanding_kendall_tau, first_crossing, ar1_surrogate, LAKES, WINDOW_FRAC, EMBED_DIM, EMBED_DELAY,
TAU_THRESHOLD, DATA) UNCHANGED via dynamic import -- Minimal Relaxation Rule: only the crossing
RULE (single tau condition -> tau AND Pettitt) and the resulting floor/verdict logic are new.

Pettitt's test is implemented from scratch here (no already-installed dependency provides it --
checked). Positive/negative-control validation lives in
tests/test_lakes_tda_ews_changepoint_v2.py and MUST pass before this run's results are trusted,
per this project's own precedent for `ar1_surrogate`/`iaaft_surrogate`.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pyreadr

HERE = Path(__file__).resolve().parent

_B_DIR = HERE.parent / "20260906-may1972-tda-ews-obrienlakes"
_SPEC_B = importlib.util.spec_from_file_location("lakes_tda_ews_obrienlakes_run", _B_DIR / "run.py")
obrien = importlib.util.module_from_spec(_SPEC_B)
_SPEC_B.loader.exec_module(obrien)

METRICS = HERE / "metrics"

PETTITT_ALPHA = 0.05  # standard significance level, matches V1's own SURROGATE_ALPHA convention


def pettitt_test(x: np.ndarray) -> tuple[float, float, int]:
    """Pettitt (1979) non-parametric single-change-point test.

    U_t = sum_{i<=t} sum_{j>t} sign(x_i - x_j), for t = 0..n-2 (0-indexed: t is the last index
    of the "before" segment). K = max|U_t|; approximate two-sided p-value (Pettitt 1979):
    p = 2*exp(-6*K^2 / (n^3 + n^2)). Returns (K, p_value, changepoint_index).
    """
    n = len(x)
    if n < 3:
        return 0.0, 1.0, 0
    sign_matrix = np.sign(x[:, None] - x[None, :])  # n x n, [i,j] = sign(x_i - x_j)
    u = np.array([sign_matrix[: t + 1, t + 1 :].sum() for t in range(n - 1)])
    abs_u = np.abs(u)
    changepoint_index = int(np.argmax(abs_u))
    k = float(abs_u[changepoint_index])
    p_value = 2.0 * np.exp(-6.0 * k**2 / (n**3 + n**2))
    return k, float(min(p_value, 1.0)), changepoint_index


def two_part_crossing(
    raw_stat: np.ndarray,
    tau_series: np.ndarray,
    threshold: float = obrien.TAU_THRESHOLD,
    alpha: float = PETTITT_ALPHA,
) -> int | None:
    """V2 rule: a series counts as 'crossing' only if BOTH (a) its expanding tau reaches
    `threshold`, AND (b) Pettitt's test on the RAW statistic (evaluated CAUSALLY -- only data up
    to and including the tau-crossing index, matching the tau rule's own expanding-window
    causality) finds a significant level shift."""
    tau_idx = obrien.first_crossing(tau_series, threshold)
    if tau_idx is None:
        return None
    window_so_far = raw_stat[: tau_idx + 1]
    valid = window_so_far[~np.isnan(window_so_far)]
    if len(valid) < 10:
        return None
    _, p_value, _ = pettitt_test(valid)
    return tau_idx if p_value < alpha else None


def floor_false_positive_rate_v2(
    x: np.ndarray, window: int, reps: int, seed: int
) -> tuple[float, float]:
    """Fraction of AR(1) surrogates (no mechanism) that STILL two-part-cross under V2.

    Returns (rate, se) where se is the binomial standard error sqrt(p(1-p)/reps) -- reported
    per FL Step 8a skeptic Finding 3: at the original reps=30 the 95% CI half-width (~18pp) sat
    inside the pre-registered 50% decision boundary. `reps` and `seed` are now caller-controlled
    (was hard-coded reps=30, seed=0 shared across all three lakes -- skeptic Finding 4) so a
    genuinely per-lake-independent, adequately-powered floor estimate can be produced.
    """
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(reps):
        surrogate = obrien.ar1_surrogate(x, rng)
        var = obrien.rolling_stat(surrogate, window, "var")
        ac1 = obrien.rolling_stat(surrogate, window, "ac1")
        tau_var = obrien.expanding_kendall_tau(var)
        tau_ac1 = obrien.expanding_kendall_tau(ac1)
        if (
            two_part_crossing(var, tau_var) is not None
            or two_part_crossing(ac1, tau_ac1) is not None
        ):
            hits += 1
    rate = hits / reps
    se = float(np.sqrt(rate * (1.0 - rate) / reps))
    return rate, se


FLOOR_REPS = 500  # was 30 -- FL Step 8a skeptic Finding 3: reps=30 gave a 95% CI half-width of
# ~18pp, placing the pre-registered 50% decision boundary inside the noise band. 500 reps gives
# SE=sqrt(0.25/500)~=2.2pp, 95% CI half-width~=4.4pp -- comfortably resolves the boundary.


def cmd_run() -> dict:
    rdata = pyreadr.read_r(str(obrien.DATA))
    results = {}

    for lake_index, (lake_key, cfg) in enumerate(obrien.LAKES.items()):
        dates, pca1 = obrien.load_series(rdata, lake_key)
        n = len(pca1)
        window = round(obrien.WINDOW_FRAC * n)
        window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)

        ac1 = obrien.rolling_stat(pca1, window, "ac1")
        var = obrien.rolling_stat(pca1, window, "var")
        betti = obrien.betti1_entropy_series(pca1, window)

        tau_ac1 = obrien.expanding_kendall_tau(ac1)
        tau_var = obrien.expanding_kendall_tau(var)
        tau_betti = obrien.expanding_kendall_tau(betti)

        window_end_dates = dates[window - 1 :]

        def crossing_date(raw_stat: np.ndarray, tau_series: np.ndarray) -> float | None:
            idx = two_part_crossing(raw_stat, tau_series)
            return float(window_end_dates[idx]) if idx is not None else None

        cross_ac1 = crossing_date(ac1, tau_ac1)
        cross_var = crossing_date(var, tau_var)
        cross_betti = crossing_date(betti, tau_betti)
        classical_cross = min([c for c in (cross_ac1, cross_var) if c is not None], default=None)

        lead_months = None
        if cross_betti is not None and classical_cross is not None:
            lead_months = (classical_cross - cross_betti) * 12.0

        # per-lake seed (skeptic Finding 4: original code shared seed=0 across all 3 lakes,
        # correlating their surrogate innovation sequences -- ~1.5, not 3, independent trials)
        lake_seed = 1000 * (lake_index + 1)
        new_floor_fp_rate, new_floor_se = floor_false_positive_rate_v2(
            pca1, window, reps=FLOOR_REPS, seed=lake_seed
        )

        results[lake_key] = {
            "role": cfg["role"],
            "n_points": n,
            "window": window,
            "documented_transition": cfg["transition"],
            "classical_ac1_crossing": cross_ac1,
            "classical_var_crossing": cross_var,
            "classical_earliest_crossing": classical_cross,
            "tda_betti_crossing": cross_betti,
            "lead_months_tda_minus_classical": lead_months,
            "false_positive": (
                cfg["role"] == "negative"
                and (cross_ac1 is not None or cross_var is not None or cross_betti is not None)
            ),
            "new_floor_ar1_false_positive_rate": new_floor_fp_rate,
            "new_floor_ar1_false_positive_rate_se": new_floor_se,
            "new_floor_ar1_false_positive_rate_ci95": [
                max(0.0, new_floor_fp_rate - 1.96 * new_floor_se),
                min(1.0, new_floor_fp_rate + 1.96 * new_floor_se),
            ],
            "floor_reps": FLOOR_REPS,
            "floor_seed": lake_seed,
            "original_floor_ar1_false_positive_rate": obrien.floor_false_positive_rate(
                pca1, window, reps=30, seed=0
            ),
        }

    max_new_floor = max(r["new_floor_ar1_false_positive_rate"] for r in results.values())

    if max_new_floor >= 0.5:
        verdict = "CRITERION_INVALID"
    else:
        lz = results["lower_zurich"]
        pass_lz = (
            lz["lead_months_tda_minus_classical"] is not None
            and lz["lead_months_tda_minus_classical"] > 0
        )
        no_false_positives = (
            not results["windermere"]["false_positive"]
            and not results["loch_leven"]["false_positive"]
        )
        verdict = "PROMOTE" if (pass_lz and no_false_positives) else "REJECT"

    out = {
        "config": {
            "window_frac": obrien.WINDOW_FRAC,
            "embed_dim": obrien.EMBED_DIM,
            "embed_delay": obrien.EMBED_DELAY,
            "tau_threshold": obrien.TAU_THRESHOLD,
            "pettitt_alpha": PETTITT_ALPHA,
            "detection_rule": "tau>=threshold AND Pettitt p<alpha on raw statistic (causal)",
        },
        "results": results,
        "max_new_floor_fp_rate": max_new_floor,
        "verdict": verdict,
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
