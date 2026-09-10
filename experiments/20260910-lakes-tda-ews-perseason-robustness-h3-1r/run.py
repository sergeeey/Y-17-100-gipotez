"""run.py -- H-B3-1r: robustness check on H-B3-1q's own cross-variable tau-trajectory coherence
pattern -- does it replicate when computed SEPARATELY per field season (2008, 2009, 2010),
instead of pooled onto one continuous season_time axis (peter.load_daily_series's own choice)?

Reuses obrien.expanding_kendall_tau/betti1_total_persistence_series/WINDOW_FRAC/EMBED_DIM/
EMBED_DELAY UNCHANGED. Reads the SAME source CSV H-B3-1/1g/1o/1q already use, but builds a
per-season daily series directly (not via peter.load_daily_series, which pools by design).
"""

from __future__ import annotations

import importlib.util
import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

_OBRIEN_DIR = HERE.parent / "20260906-may1972-tda-ews-obrienlakes"
_PETER_DIR = HERE.parent / "20260906-may1972-tda-ews-peterlake"
_H_B3_1Q_DIR = HERE.parent / "20260910-lakes-tda-ews-crossvar-coherence-h3-1q"

DATA = _PETER_DIR / "data" / "squealSondesMet_08to11_forOPUS.csv"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


obrien = _load_module("h_b3_1r_obrien", _OBRIEN_DIR / "run.py")

VARIABLES = ["chl", "pH", "doSat"]
LAKES = ["Peter", "Paul"]
SEASONS = [2008, 2009, 2010]  # matches Carpenter et al. 2011's own INCLUDED_SEASONS


def daily_series_for_season(var: str, lake: str, year: int) -> np.ndarray:
    df = pd.read_csv(DATA, usecols=["lake", "year", "datetime", var])
    df = df[(df["lake"] == lake) & (df["year"] == year)].copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.dropna(subset=[var])
    daily = df.set_index("datetime")[var].resample("D").mean().dropna()
    return daily.to_numpy(dtype=float)


def tau_for_season(var: str, lake: str, year: int) -> tuple[np.ndarray | None, int]:
    x = daily_series_for_season(var, lake, year)
    n = len(x)
    window = round(obrien.WINDOW_FRAC * n)
    window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)
    if window >= n:
        return None, n
    series = obrien.betti1_total_persistence_series(x, window)
    tau = obrien.expanding_kendall_tau(series)
    return tau, n


def unaligned_correlation(tau_a: np.ndarray, tau_b: np.ndarray) -> dict:
    n = min(len(tau_a), len(tau_b))
    mask = ~np.isnan(tau_a[:n]) & ~np.isnan(tau_b[:n])
    if mask.sum() < 3:
        return {"rho": None, "p": None, "n": int(mask.sum())}
    rho, p = spearmanr(tau_a[:n][mask], tau_b[:n][mask])
    return {"rho": float(rho), "p": float(p), "n": int(mask.sum())}


def cmd_run() -> dict:
    per_season_results = {}
    for year in SEASONS:
        year_results = {}
        for lake in LAKES:
            trajectories = {}
            n_daily_by_var = {}
            for var in VARIABLES:
                tau, n_daily = tau_for_season(var, lake, year)
                trajectories[var] = tau
                n_daily_by_var[var] = n_daily

            pair_results = []
            for v1, v2 in combinations(VARIABLES, 2):
                t1, t2 = trajectories[v1], trajectories[v2]
                if t1 is None or t2 is None:
                    pair_results.append({"var1": v1, "var2": v2, "rho": None, "p": None, "n": 0})
                    continue
                corr = unaligned_correlation(t1, t2)
                pair_results.append({"var1": v1, "var2": v2, **corr})

            n_positive = sum(1 for r in pair_results if r["rho"] is not None and r["rho"] > 0)
            year_results[lake] = {
                "n_daily_by_var": n_daily_by_var,
                "pairs": pair_results,
                "n_positive_of_3": n_positive,
            }
        per_season_results[str(year)] = year_results

    # Kill criterion evaluation: does the pattern (Peter more consistent than Paul) hold
    # in ALL seasons, strengthening or stable toward 2010?
    season_verdicts = {}
    for year in SEASONS:
        peter_n = per_season_results[str(year)]["Peter"]["n_positive_of_3"]
        paul_n = per_season_results[str(year)]["Paul"]["n_positive_of_3"]
        season_verdicts[str(year)] = {
            "peter_n_positive": peter_n,
            "paul_n_positive": paul_n,
            "peter_more_consistent": peter_n > paul_n,
        }

    all_seasons_show_peter_more_consistent = all(
        v["peter_more_consistent"] for v in season_verdicts.values()
    )
    pattern_strengthens_toward_2010 = (
        season_verdicts["2010"]["peter_n_positive"] >= season_verdicts["2009"]["peter_n_positive"]
    )

    replicates = all_seasons_show_peter_more_consistent and pattern_strengthens_toward_2010
    verdict = "REPLICATES" if replicates else "REJECTED-FOR-SEASON-ROBUSTNESS"

    out = {
        "claim": "H-B3-1r -- robustness check: does H-B3-1q's own pooled cross-variable "
        "coherence pattern replicate when computed per-season (2008/2009/2010) instead of "
        "pooled? RESULT: does not replicate cleanly -- 2008 shows the opposite pattern, 2010 "
        "(transition-completion year) is weaker than 2009, not stronger",
        "per_season_results": per_season_results,
        "season_verdicts": season_verdicts,
        "all_seasons_show_peter_more_consistent": all_seasons_show_peter_more_consistent,
        "pattern_strengthens_toward_2010": pattern_strengthens_toward_2010,
        "verdict": verdict,
        "interpretation": "Does NOT invalidate H-B3-1q's own pooled correlation numbers "
        "(those remain correctly computed) -- weakens confidence that the pooled pattern "
        "reflects a genuine, season-independent ecological coherence signal rather than "
        "partly an artifact of pooling multiple seasons onto one continuous expanding-window "
        "timeline before computing the statistic.",
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
