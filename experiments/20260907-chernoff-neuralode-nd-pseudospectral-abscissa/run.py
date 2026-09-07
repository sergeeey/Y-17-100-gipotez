"""run.py — H-B2-1r: does the pseudospectral abscissa alpha_eps(A) explain M1 at N_DIM in
{40,50}, where BOTH kappa(V) (H-B2-1m/o) and omega(A) (H-B2-1n/p/q) are now confirmed null?
Deferred from H-B2-1n's own claim.md as "the more complete descriptor... expensive, deferred
unless the cheaper test is uninformative" -- both cheaper tests are now confirmed uninformative
at large N, so this is the correct next step.

Reuses H-B2-1m's build_matrix_with_seed_and_n and H-B2-1k's dim_sweep.measure_m1 UNCHANGED via
dynamic import (Minimal Relaxation Rule) -- pseudospectral_abscissa() is the only new numerical
routine in this arc, and carries its own correctness tests (see tests/) verifying it against a
known-exact case (normal matrix) and a known-sensitive case (strongly non-normal matrix) BEFORE
being trusted on the real population.
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

N_DIM_VALUES = (3, 4, 8, 12, 40, 50)  # small-N sanity check + the two confirmed-null large N
N_SEEDS = 15  # matches H-B2-1m/1n's original scale -- first pass on an expensive computation
ALPHA = 0.05

EPS = 1.0  # pseudospectral perturbation radius; ~2% of the matrix's spectral range (-50 to 0.5),
# well above float precision, well below COUPLING_MAGNITUDE=15 -- a documented design choice,
# not claimed to be uniquely "correct"
RE_MIN, RE_MAX = -5.0, 60.0
IM_MAX = 15.0
N_RE, N_IM = 100, 100  # grid resolution -- see BUG note below for why this was raised from 40x40


def pseudospectral_abscissa(
    a: np.ndarray,
    eps: float = EPS,
    re_min: float = RE_MIN,
    re_max: float = RE_MAX,
    im_max: float = IM_MAX,
    n_re: int = N_RE,
    n_im: int = N_IM,
) -> float:
    """alpha_eps(A) = max{Re(z) : sigma_min(zI-A) <= eps}, via grid search over the complex
    plane, scanning Re(z) from high to low and stopping at the first Re(z) with ANY Im(z) hit
    (assumes a connected eps-pseudospectrum near its rightmost extent -- a documented
    approximation, not a rigorous guarantee for pathological cases).

    BUG FOUND AND FIXED same-session, before any verdict was trusted: the original version
    searched `re` all the way down to a hardcoded `re_min=-5.0`. For 3 of 15 seeds at N_DIM=3
    (real run, first pass), this returned exactly 0.0 -- a value BELOW the proven universal
    lower bound alpha_eps(A) >= alpha(A) + eps (from a rank-1 perturbation argument: for any
    eigenvalue lambda with unit eigenvector x, E = eps*exp(i*theta)*x*x^H gives (A+E)x =
    (lambda+eps*exp(i*theta))x, so the full eps-disk boundary around EVERY eigenvalue is in
    sigma_eps(A), for ANY matrix, normal or not). This project's matrix family always has a
    second-largest eigenvalue at exactly -1 (fixed SPECTRAL_RANGE upper end), whose OWN
    eps-disk reaches re=-1+eps=0.0 -- for some random couplings, the coarse original grid found
    a grid point inside THAT disk before finding one inside the dominant eigenvalue's disk
    (radius exactly eps=1, comparable to the original grid spacing of ~1.6), returning a
    spuriously low value from the WRONG eigenvalue instead of undercounting from the right one.
    Root-caused via a same-session re-check of the real run's own alpha_eps_range values against
    this lower bound (the original test suite only checked >= spectral_abscissa, a WEAKER bound
    that this bug did not violate for most seeds, which is why it was not caught before the run).

    Fix: `re_min` is now clamped to never go below the matrix's own spectral abscissa (computed
    from its actual eigenvalues, not assumed) -- since z=alpha(A) is itself always in sigma_eps(A)
    trivially (dist 0 <= eps), the search is now MATHEMATICALLY GUARANTEED to never return below
    the true spectral abscissa, regardless of remaining grid coarseness elsewhere. Grid
    resolution was also raised (100x100, IM_MAX narrowed to 15) to reduce (not eliminate) the
    separate, milder issue of coarse-grid underestimation this same diagnosis surfaced."""
    n = a.shape[0]
    spectral_abscissa = float(np.max(np.linalg.eigvals(a).real))
    effective_re_min = max(re_min, spectral_abscissa)
    ident = np.eye(n, dtype=complex)
    a_complex = a.astype(complex)
    re_grid = np.linspace(re_max, effective_re_min, n_re)
    im_grid = np.linspace(-im_max, im_max, n_im)
    for re in re_grid:
        for im in im_grid:
            z = complex(re, im)
            m = z * ident - a_complex
            smin = np.linalg.svd(m, compute_uv=False)[-1]
            if smin <= eps:
                return float(re)
    return spectral_abscissa  # guaranteed hit here (dist 0 <= eps), so this is never reached


def cmd_run() -> dict:
    per_n_slice = {}

    for n_dim in N_DIM_VALUES:
        alphas = []
        m1s = []
        per_seed = {}
        for seed in range(N_SEEDS):
            a = multin.build_matrix_with_seed_and_n(n_dim, seed)
            alpha_eps = pseudospectral_abscissa(a)
            m1 = dim_sweep.measure_m1(a, dim_sweep.T_MAX, dim_sweep.W)
            alphas.append(alpha_eps)
            m1s.append(m1)
            per_seed[str(seed)] = {"alpha_eps": alpha_eps, "m1": m1}

        rho, p = spearmanr(alphas, m1s)
        per_n_slice[str(n_dim)] = {
            "n_dim": n_dim,
            "n_seeds": N_SEEDS,
            "spearman_rho": float(rho),
            "spearman_p": float(p),
            "alpha_eps_range": [float(min(alphas)), float(max(alphas))],
            "alpha_eps_std": float(np.std(alphas)),
            "per_seed": per_seed,
        }

    large_n_slices = {n: per_n_slice[str(n)] for n in (40, 50)}
    large_n_significant = [
        n for n, v in large_n_slices.items() if v["spearman_p"] < ALPHA and v["spearman_rho"] > 0
    ]

    verdict = "CONFIRMED" if large_n_significant else "REJECTED"

    result = {
        "config": {
            "n_dim_values": list(N_DIM_VALUES),
            "n_seeds": N_SEEDS,
            "eps": EPS,
            "grid": {
                "re_min": RE_MIN,
                "re_max": RE_MAX,
                "im_max": IM_MAX,
                "n_re": N_RE,
                "n_im": N_IM,
            },
        },
        "per_n_slice": per_n_slice,
        "large_n_criterion": {
            "n_dim_tested": [40, 50],
            "individually_significant_positive": large_n_significant,
        },
        "verdict": verdict,
        "verdict_note": (
            "CONFIRMED: at least one of N=40/N=50 individually significant, positive sign -- "
            "pseudospectral abscissa explains some of the gap kappa(V)/omega(A) left open. "
            "REJECTED: neither significant -- even the theoretically richer descriptor does not "
            "explain M1 at large N for this matrix family."
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "per_n_slice"}, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
