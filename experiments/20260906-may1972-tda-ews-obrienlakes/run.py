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
import warnings
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


# ───────────────────── V1: per-series surrogate-null detection rule ─────────────────────
# WHY (Relaxation Map, both sibling decision.md files, 2026-09-06): a single fixed tau>=0.5
# threshold sits AT FLOOR (45-90% false-positive rate under a mechanism-free AR(1) null) on
# every real series tested so far. V1 replaces the fixed threshold with a PER-SERIES,
# PER-TIMEPOINT significance test: at each time index, "crossing" means the real tau exceeds
# the (1-alpha) percentile of the SAME AR(1)-surrogate null used for the floor check -- so the
# bar a series must clear is calibrated to its own length and autocorrelation structure, not a
# borrowed literature constant. This is the ONLY assumption changed from H-B3-1/H-B3-1b
# (Minimal Relaxation Rule) -- window, embedding, and statistics are all unchanged.
SURROGATE_ALPHA = 0.05  # one-sided significance level, standard convention (Dakos et al. 2012)


def iaaft_surrogate(x: np.ndarray, rng: np.random.Generator, n_iter: int = 20) -> np.ndarray:
    """V1' null model (Schreiber & Schmitz 1996): Iterative Amplitude Adjusted Fourier Transform.

    WHY (Relaxation Map, H-B3-1c decision.md, 2026-09-06): AR(1) matches only LAG-1 autocorrelation
    -- V1's floor check on real negative-control lakes still false-positived 5/5 because those
    series have structure at other lags / non-stationarities AR(1) cannot represent. IAAFT instead
    preserves the FULL power spectrum (autocorrelation at every lag) AND the exact amplitude
    distribution (histogram of values) of `x`, randomizing only the phase relationships --
    destroys nonlinear/deterministic structure while keeping all LINEAR temporal structure, a
    strictly richer null than AR(1) with no new distributional assumption beyond "linear + this
    exact spectrum + this exact value set" (Theiler et al. 1992 surrogate-testing framework).
    """
    n = len(x)
    sorted_x = np.sort(x)
    target_amplitudes = np.abs(np.fft.rfft(x))
    surrogate = rng.permutation(x)  # white-shuffle start: correct amplitude distribution already
    for _ in range(n_iter):
        phases = np.angle(np.fft.rfft(surrogate))
        spectrum_matched = np.fft.irfft(target_amplitudes * np.exp(1j * phases), n=n)
        ranks = np.argsort(np.argsort(spectrum_matched))
        surrogate = sorted_x[ranks]
    return surrogate


# ───────────────────── V2': detrend-then-surrogate ─────────────────────
# WHY (Relaxation Map, H-B3-1d decision.md, 2026-09-06): V1 (AR(1)) and V1' (IAAFT) failed
# IDENTICALLY (5/5 negative controls false-positive) despite IAAFT being a strictly richer
# STATIONARY linear null (full spectrum + exact amplitude distribution vs lag-1 only). This
# rules out "insufficient spectral richness" and points to a within-season deterministic/
# non-stationary trend that phase-randomization cannot represent (IAAFT's mechanism assumes
# weak stationarity). V2' removes a smooth trend BEFORE generating the null (on the residual),
# then adds the trend back -- the ONLY assumption changed from H-B3-1d (Minimal Relaxation
# Rule): the null-generating PROCEDURE now includes a detrend/retrend step, reusing IAAFT
# (already validated) as the residual surrogate.
DETREND_FRAC = 0.25  # trend window as a fraction of series length -- deliberately narrower
# than WINDOW_FRAC=0.5 (the detection window), so the removed "trend" is slower than any
# potential regime-shift signal the detection window is meant to catch.


def smooth_trend(x: np.ndarray, frac: float = DETREND_FRAC) -> np.ndarray:
    """Centered moving-average trend, window = frac * n (odd, >=5). No new dependency beyond
    pandas (already used by the Peter Lake loader)."""
    import pandas as pd

    n = len(x)
    window = max(round(frac * n), 5)
    if window % 2 == 0:
        window += 1
    return pd.Series(x).rolling(window, center=True, min_periods=1).mean().to_numpy()


def detrend_surrogate(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """V2' null model: subtract a smooth trend, generate an IAAFT surrogate of the RESIDUAL
    (preserves the residual's own spectrum/amplitude distribution, not the trend's), add the
    trend back. The surrogate carries the SAME trend as the real series but a randomized
    residual around it -- if the real series' false-positive rate was driven by the trend
    itself (H-B3-1d's diagnosis), this null should no longer inherit that false signal."""
    trend = smooth_trend(x)
    residual = x - trend
    surrogate_residual = iaaft_surrogate(residual, rng)
    return trend + surrogate_residual


def surrogate_null_curve(
    x: np.ndarray,
    window: int,
    kind: str,
    reps: int,
    seed: int,
    alpha: float = SURROGATE_ALPHA,
    surrogate_fn=ar1_surrogate,
) -> np.ndarray:
    """Per-timepoint (1-alpha) percentile of the expanding-tau curve under `reps` surrogates of
    `x` (kind in {"ac1","var","betti"}), generated by `surrogate_fn` (defaults to `ar1_surrogate`
    for backward compatibility with V1; pass `iaaft_surrogate` for V1'). Same length as the real
    tau series."""
    rng = np.random.default_rng(seed)
    n_out = len(x) - window + 1
    curves = np.full((reps, n_out), np.nan)
    for r in range(reps):
        surrogate = surrogate_fn(x, rng)
        if kind == "betti":
            stat = betti1_entropy_series(surrogate, window)
        else:
            stat = rolling_stat(surrogate, window, kind)
        curves[r] = expanding_kendall_tau(stat)
    # WHY: early time indices (before min_points is reached in EVERY surrogate) are legitimately
    # all-NaN across the reps axis -- nanpercentile warns about this by design, not a bug; the
    # resulting NaN correctly propagates into surrogate_crossing's valid-mask exclusion.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="All-NaN slice encountered")
        return np.nanpercentile(curves, 100 * (1 - alpha), axis=0)


def surrogate_crossing(real_tau: np.ndarray, null_curve: np.ndarray) -> int | None:
    """First index where the real series' tau exceeds ITS OWN per-timepoint surrogate-null
    percentile -- replaces `first_crossing`'s fixed threshold with a self-calibrated one."""
    valid = ~np.isnan(real_tau) & ~np.isnan(null_curve)
    hit = np.where(valid & (real_tau > null_curve))[0]
    return int(hit[0]) if hit.size else None


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
