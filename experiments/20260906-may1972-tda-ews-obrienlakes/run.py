"""run.py — H-B3-1 (re-scoped): TDA vs classical EWS lead time on O'Brien et al. 2023 lake data.

PIPELINE (pure functions, no I/O, no verdicts):
    load_series, takens_embed, rolling_stat, expanding_kendall_tau, betti1_entropy_series,
    first_crossing
EXPERIMENT (I/O, controls, verdicts):
    cmd_run

Design pre-registered in claim.md BEFORE inspecting how well it "works":
  - scalar series = pca1 (matches O'Brien et al.'s own single-axis transition dating)
  - rolling window = round(0.5 * n) points (standard EWS convention, Dakos et al. 2012 PLOS ONE)
  - classical EWS statistics = rolling lag-1 autocorrelation, rolling variance
  - TDA statistic = persistence entropy of H1 (Vietoris-Rips on a Takens embedding, dim=3,
    delay=1, computed inside the SAME rolling window as the classical statistics)
  - "signal onset" (threshold crossing), IDENTICAL rule for every statistic family: the first
    time index where the Kendall tau of that statistic, on the EXPANDING window from the first
    valid point up to t, reaches >= 0.5 (a coherent trend) -- same rule for TDA and classical
    EWS, so any lead-time difference is attributable to the signal, not the detection rule.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pyreadr
from ripser import ripser
from scipy.stats import kendalltau

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "wrangled_genus_plank_data_public.Rdata"
METRICS = HERE / "metrics"

WINDOW_FRAC = (
    0.5  # rolling window as a fraction of series length -- pre-registered, standard convention
)
EMBED_DIM = 3  # Takens embedding dimension
EMBED_DELAY = 1  # Takens embedding delay (months)
TAU_THRESHOLD = (
    0.5  # Kendall tau threshold for a "coherent trend" -- same rule for both signal families
)

LAKES = {
    "lower_zurich": {
        "object": "LZ_mth_dat",
        "date_col": "date",
        "transition": 2002.0,
        "role": "positive",
    },
    "windermere": {
        "object": "wind_mth_dat",
        "date_col": "Date",
        "transition": None,
        "role": "negative",
    },
    "loch_leven": {
        "object": "leve_mth_dat",
        "date_col": None,
        "transition": None,
        "role": "negative",
    },
}


# ───────────────────────────── PIPELINE ─────────────────────────────
def load_series(rdata: dict, lake_key: str) -> tuple[np.ndarray, np.ndarray]:
    """Return (dates, pca1) for one lake, dropping rows with NaN pca1, ICE gap rule applied."""
    cfg = LAKES[lake_key]
    df = rdata[cfg["object"]]
    date_col = cfg["date_col"] or next(c for c in df.columns if c.lower() == "date")
    sub = df[[date_col, "pca1"]].dropna()
    dates = sub[date_col].to_numpy(dtype=float)
    pca1 = sub["pca1"].to_numpy(dtype=float)
    order = np.argsort(dates)
    dates, pca1 = dates[order], pca1[order]
    # ICE: a gap > 2x the median spacing is a real hole -- exclude it, don't bridge it silently.
    spacing = np.diff(dates)
    med = np.median(spacing)
    gap_idx = np.where(spacing > 2 * med)[0]
    if gap_idx.size:
        # Use only the longest contiguous run -- composite ICE strategy (exclude, don't impute).
        bounds = [0, *[i + 1 for i in gap_idx], len(dates)]
        runs = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
        start, end = max(runs, key=lambda r: r[1] - r[0])
        dates, pca1 = dates[start:end], pca1[start:end]
    return dates, pca1


def takens_embed(x: np.ndarray, dim: int = EMBED_DIM, delay: int = EMBED_DELAY) -> np.ndarray:
    n = len(x) - (dim - 1) * delay
    if n <= 1:
        raise ValueError(f"series too short for embedding: len={len(x)}, dim={dim}, delay={delay}")
    return np.column_stack([x[i * delay : i * delay + n] for i in range(dim)])


def rolling_stat(x: np.ndarray, window: int, kind: str) -> np.ndarray:
    """Rolling lag-1 autocorrelation or variance, length len(x)-window+1, indexed at the END of
    each window (standard EWS convention -- the statistic is "known" once the window closes)."""
    out = np.full(len(x) - window + 1, np.nan)
    for i in range(len(out)):
        w = x[i : i + window]
        if kind == "var":
            out[i] = np.var(w, ddof=1)
        elif kind == "ac1":
            out[i] = np.corrcoef(w[:-1], w[1:])[0, 1]
        else:
            raise ValueError(kind)
    return out


def betti1_entropy_series(
    x: np.ndarray, window: int, dim: int = EMBED_DIM, delay: int = EMBED_DELAY
) -> np.ndarray:
    """Persistence entropy of H1 (Vietoris-Rips on a Takens embedding of each rolling window)."""
    out = np.full(len(x) - window + 1, np.nan)
    for i in range(len(out)):
        w = x[i : i + window]
        try:
            cloud = takens_embed(w, dim, delay)
        except ValueError:
            continue
        dgms = ripser(cloud, maxdim=1)["dgms"][1]  # H1 diagram
        finite = dgms[np.isfinite(dgms[:, 1])]
        if finite.shape[0] == 0:
            out[i] = 0.0
            continue
        life = finite[:, 1] - finite[:, 0]
        life = life[life > 0]
        if life.size == 0:
            out[i] = 0.0
            continue
        p = life / life.sum()
        out[i] = float(-(p * np.log(p)).sum())  # persistence entropy
    return out


def expanding_kendall_tau(stat: np.ndarray, min_points: int = 8) -> np.ndarray:
    """Kendall tau of `stat` vs time, expanding window [0, t]. NaN until min_points reached."""
    out = np.full(len(stat), np.nan)
    valid = np.where(~np.isnan(stat))[0]
    if valid.size == 0:
        return out
    t = np.arange(len(stat))
    for k, i in enumerate(valid):
        if k + 1 < min_points:
            continue
        idx = valid[: k + 1]
        tau, _ = kendalltau(t[idx], stat[idx])
        out[i] = tau
    return out


def first_crossing(tau_series: np.ndarray, threshold: float = TAU_THRESHOLD) -> int | None:
    hit = np.where(~np.isnan(tau_series) & (tau_series >= threshold))[0]
    return int(hit[0]) if hit.size else None


def ar1_surrogate(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """FL Step 4a floor: an AR(1) red-noise series matched in length, mean, variance and lag-1
    autocorrelation to `x`, but with NO real transition/mechanism by construction. If this floor
    ALSO crosses the tau>=0.5 threshold, the threshold criterion is CRITERION_INVALID for this
    population -- it fires on the null, not on the mechanism."""
    n = len(x)
    phi = np.clip(np.corrcoef(x[:-1], x[1:])[0, 1], -0.99, 0.99)
    sigma = np.std(x, ddof=1) * np.sqrt(max(1 - phi**2, 1e-6))
    out = np.empty(n)
    out[0] = x[0]
    noise = rng.normal(0, sigma, n)
    for i in range(1, n):
        out[i] = np.mean(x) + phi * (out[i - 1] - np.mean(x)) + noise[i]
    return out


def floor_false_positive_rate(x: np.ndarray, window: int, reps: int, seed: int) -> float:
    """Fraction of AR(1) surrogates (no mechanism) that ALSO cross tau>=0.5 on classical EWS."""
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(reps):
        surrogate = ar1_surrogate(x, rng)
        var = rolling_stat(surrogate, window, "var")
        ac1 = rolling_stat(surrogate, window, "ac1")
        tau_var = expanding_kendall_tau(var)
        tau_ac1 = expanding_kendall_tau(ac1)
        if first_crossing(tau_var) is not None or first_crossing(tau_ac1) is not None:
            hits += 1
    return hits / reps


# ───────────────────────────── EXPERIMENT ─────────────────────────────
def cmd_run() -> dict:
    rdata = pyreadr.read_r(str(DATA))
    results = {}
    for lake_key, cfg in LAKES.items():
        dates, pca1 = load_series(rdata, lake_key)
        n = len(pca1)
        window = round(WINDOW_FRAC * n)
        window = max(
            window, EMBED_DIM * EMBED_DELAY + 8
        )  # floor so embedding + tau are both feasible

        ac1 = rolling_stat(pca1, window, "ac1")
        var = rolling_stat(pca1, window, "var")
        betti = betti1_entropy_series(pca1, window)

        tau_ac1 = expanding_kendall_tau(ac1)
        tau_var = expanding_kendall_tau(var)
        tau_betti = expanding_kendall_tau(betti)

        # index i of a rolling-stat array corresponds to a window ending at dates[i + window - 1]
        window_end_dates = dates[window - 1 :]

        def crossing_date(tau_series: np.ndarray) -> float | None:
            idx = first_crossing(tau_series)
            return float(window_end_dates[idx]) if idx is not None else None

        cross_ac1 = crossing_date(tau_ac1)
        cross_var = crossing_date(tau_var)
        cross_betti = crossing_date(tau_betti)
        classical_cross = min([c for c in (cross_ac1, cross_var) if c is not None], default=None)

        lead_months = None
        if cross_betti is not None and classical_cross is not None:
            lead_months = (classical_cross - cross_betti) * 12.0

        floor_fp_rate = floor_false_positive_rate(pca1, window, reps=30, seed=0)

        results[lake_key] = {
            "role": cfg["role"],
            "n_points": n,
            "window": window,
            "date_range": [float(dates[0]), float(dates[-1])],
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
            "floor_ar1_false_positive_rate": floor_fp_rate,
        }

    lz = results["lower_zurich"]
    verdict = (
        "PASS"
        if (
            lz["lead_months_tda_minus_classical"] is not None
            and lz["lead_months_tda_minus_classical"] > 0
            and not results["windermere"]["false_positive"]
            and not results["loch_leven"]["false_positive"]
        )
        else "KILLED"
    )

    out = {
        "config": {
            "window_frac": WINDOW_FRAC,
            "embed_dim": EMBED_DIM,
            "embed_delay": EMBED_DELAY,
            "tau_threshold": TAU_THRESHOLD,
        },
        "results": results,
        "verdict": verdict,
    }
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
