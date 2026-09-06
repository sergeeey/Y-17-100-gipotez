"""diag_se.py — post-skeptic diagnostic: is the reported SE of <r> understated?

Skeptic concern (Step 8a, 2026-09-06): run.py computes se = std(r)/sqrt(N-2), assuming i.i.d. r_n.
Adjacent r_n and r_{n+1} share the spacing s_{n+1} → correlated → the i.i.d. SE is too small.

This script does NOT change the claim or run.py. It estimates the effective SE two ways and writes
metrics/diag_se.json:
  1. lag-k autocorrelation of r_n  → Bartlett-style variance inflation  (1 + 2*sum_k rho_k)
  2. non-overlapping block bootstrap (block = 200 ratios, 2000 resamples) of the mean
Same diagnostic on the synthetic GUE control so the two references are compared on equal footing.
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("riemann_run", HERE / "run.py")
run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run)


def autocorr(x: np.ndarray, maxlag: int = 5) -> list[float]:
    x = x - x.mean()
    v = float(np.dot(x, x))
    return [float(np.dot(x[:-k], x[k:]) / v) for k in range(1, maxlag + 1)]


def block_bootstrap_se(x: np.ndarray, block: int, reps: int, rng: np.random.Generator) -> float:
    nblocks = x.size // block
    blocks = x[: nblocks * block].reshape(nblocks, block).mean(axis=1)
    idx = rng.integers(0, nblocks, size=(reps, nblocks))
    return float(blocks[idx].mean(axis=1).std(ddof=1))


def diagnose(r: np.ndarray, rng: np.random.Generator) -> dict:
    rho = autocorr(r)
    inflation = 1 + 2 * sum(rho)  # Bartlett, truncated at lag 5 (rho_k ~ 0 for k >= 2 here)
    se_iid = float(r.std(ddof=1) / math.sqrt(r.size))
    return {
        "n": int(r.size),
        "mean_r": float(r.mean()),
        "se_iid": se_iid,
        "rho_lag1..5": rho,
        "bartlett_inflation": inflation,
        "se_bartlett": se_iid * math.sqrt(max(inflation, 0.0)),
        "se_block_bootstrap": block_bootstrap_se(r, 200, 2000, rng),
    }


def main() -> None:
    rng = np.random.default_rng(0)
    zeros, _ = run.load_zeros()
    r_zeta = run.r_stat(zeros)
    gue = run.synthetic_bulk_eigs(400, 500, np.random.default_rng(0), beta=2)
    r_gue = np.concatenate([run.r_stat(b) for b in gue])

    dz, dg = diagnose(r_zeta, rng), diagnose(r_gue, rng)
    delta = dz["mean_r"] - dg["mean_r"]
    se_bb = math.hypot(dz["se_block_bootstrap"], dg["se_block_bootstrap"])
    se_iid = math.hypot(dz["se_iid"], dg["se_iid"])
    out = {
        "zeta": dz,
        "gue_control": dg,
        "delta_zeta_minus_gue": delta,
        "z_iid_assumption": delta / se_iid,
        "z_block_bootstrap": delta / se_bb,
        "z_vs_surmise_iid": (dz["mean_r"] - run.R_GUE) / dz["se_iid"],
        "z_vs_surmise_block_bootstrap": (dz["mean_r"] - run.R_GUE) / dz["se_block_bootstrap"],
        "note": "skeptic concern 1b: i.i.d. SE understated — adjacent r share a spacing",
    }
    (HERE / "metrics" / "diag_se.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
