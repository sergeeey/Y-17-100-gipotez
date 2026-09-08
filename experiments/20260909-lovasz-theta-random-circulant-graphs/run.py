"""H-CAT31-1 -- Lovasz theta number of random dense circulant graphs.

Formal object (Bandeira et al. arXiv:2603.29571, "Randomstrasse101: Open
Problems of 2025", Entry 9, Conjecture 18): for G ~ random dense circulant
graph on n vertices, does E[theta(G)] = (1+o(1)) sqrt(n)?
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

RNG_SEED_BASE = 31000


def sample_circulant_neighbors(n: int, p: float, seed: int) -> np.ndarray:
    """Symmetric neighbor-offset vector for a random dense circulant graph.

    Samples the neighbors of vertex 0 among {1, ..., floor((n-1)/2)} i.i.d.
    with probability p, then mirrors: k a neighbor implies n-k is too
    (undirected circulant graph). Returns a 0/1 length-n indicator array c
    with c[0] = 0 (no self-loops).
    """
    rng = np.random.default_rng(seed)
    c = np.zeros(n, dtype=float)
    half = (n - 1) // 2
    picks = rng.random(half) < p
    for k in range(1, half + 1):
        if picks[k - 1]:
            c[k] = 1.0
            c[n - k] = 1.0
    if n % 2 == 0:
        # unique "antipodal" offset n/2 -- its own mirror, sample once.
        if rng.random() < p:
            c[n // 2] = 1.0
    return c


def theta_via_eigenvalues(c: np.ndarray) -> float:
    """CAUGHT WRONG this session, kept only for the record (see decision.md).

    The claimed formula theta(G) = n*(-lambda_min)/(d-lambda_min) matches
    `theta_via_lp` EXACTLY on sparse cycles (C_5, C_7) but diverges
    substantially (differences up to ~3.7, not numerical noise) on denser
    random circulant graphs at n>=9 -- verified wrong via an independent
    third check: for one specific n=9 disagreement, the complement graph's
    connection set collapsed to a single offset pair isomorphic to C_9, whose
    theta has a known closed form ((2k+1)cos(pi/(2k+1))/(1+cos(pi/(2k+1))) for
    C_{2k+1}) -- that value matches theta_via_lp via the theta(G)*theta(Gbar)=n
    identity (Lovasz 1979, tight for vertex-transitive graphs), NOT
    theta_via_eigenvalues. The recalled formula was either mis-remembered or
    requires a stronger regularity condition than vertex-transitivity that
    this docstring originally omitted -- not re-derived further, since
    `theta_via_lp` (sourced directly from the paper's own Table 1, not
    memory) is sufficient for this experiment. NOT used in `main_sweep`.
    """
    n = len(c)
    eigvals = np.fft.fft(c).real
    d = float(c.sum())
    lam_min = eigvals.min()
    if abs(d - lam_min) < 1e-12:
        return float("nan")
    return n * (-lam_min) / (d - lam_min)


def theta_via_lp(c: np.ndarray) -> float:
    """Paper's own 'time-domain primal' LP (Table 1, arXiv:2603.29571):
    max sum_i x_i  s.t.  x_k=x_{n-k}, x_0=1, Fx>=0, x_k=0 for (0,k) in E(G).

    Independently confirmed correct this session (matches known theta(C_5)=
    sqrt(5) exactly; matches an independent closed-form check on a C_9-
    isomorphic complement graph via the theta(G)*theta(Gbar)=n identity --
    see decision.md) -- used for the main sweep. `ReF` is built via a
    vectorized outer product, not a Python-level double loop (an earlier
    version's O(n^2) *Python* loop made n=2560 impractically slow -- this is
    the same O(n^2) FLOP count but done in C via numpy, not interpreted).
    """
    n = len(c)
    j = np.arange(n).reshape(-1, 1)
    k = np.arange(n).reshape(1, -1)
    ReF = np.cos(-2 * np.pi * j * k / n)

    A_eq_rows = []
    b_eq = []
    e0 = np.zeros(n)
    e0[0] = 1.0
    A_eq_rows.append(e0)
    b_eq.append(1.0)
    for kk in range(1, (n - 1) // 2 + 1):
        row = np.zeros(n)
        row[kk] = 1.0
        row[n - kk] = -1.0
        A_eq_rows.append(row)
        b_eq.append(0.0)
    for kk in range(1, n):
        if c[kk] > 0.5:
            row = np.zeros(n)
            row[kk] = 1.0
            A_eq_rows.append(row)
            b_eq.append(0.0)
    A_eq = np.array(A_eq_rows)

    A_ub = -ReF
    b_ub = np.zeros(n)

    res = linprog(
        c=-np.ones(n),
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=np.array(A_eq),
        b_eq=np.array(b_eq),
        bounds=(None, None),
        method="highs",
    )
    if not res.success:
        return float("nan")
    return -res.fun


def cross_validate(n_values, seeds_per_n=3, p=0.5):
    rows = []
    for n in n_values:
        for i in range(seeds_per_n):
            seed = RNG_SEED_BASE + n * 10 + i
            c = sample_circulant_neighbors(n, p, seed)
            th_eig = theta_via_eigenvalues(c)
            th_lp = theta_via_lp(c)
            rows.append(
                {
                    "n": n,
                    "seed": seed,
                    "theta_eigenvalue": th_eig,
                    "theta_lp": th_lp,
                    "abs_diff": abs(th_eig - th_lp),
                }
            )
    return rows


def main_sweep(n_reps_pairs, p=0.5):
    """Uses `theta_via_lp` exclusively -- the only one of the two
    implementations independently confirmed correct this session (see
    `theta_via_eigenvalues`'s own docstring for the debunked alternative).
    `n_reps_pairs`: list of (n, seeds_per_n) -- reps taper down at larger n
    to keep total LP runtime reasonable (O(n^2) per solve, verified via
    `time_lp.py` diagnostic: ~2s at n=1000)."""
    rows = []
    for n, seeds_per_n in n_reps_pairs:
        vals = []
        for i in range(seeds_per_n):
            seed = RNG_SEED_BASE + 100000 + n * 100 + i
            c = sample_circulant_neighbors(n, p, seed)
            vals.append(theta_via_lp(c))
        vals = np.array(vals)
        rows.append(
            {
                "n": n,
                "mean_theta": float(vals.mean()),
                "std_theta": float(vals.std()),
                "mean_theta_over_sqrt_n": float(vals.mean() / np.sqrt(n)),
                "n_reps": seeds_per_n,
            }
        )
    return rows


def cmd_run():
    cv_n_values = [7, 9, 11, 13, 17, 21, 25]
    cv_rows = cross_validate(cv_n_values, seeds_per_n=3)
    max_cv_diff = max(r["abs_diff"] for r in cv_rows)

    sweep_n_reps_pairs = [
        (10, 25),
        (20, 25),
        (40, 25),
        (80, 25),
        (160, 25),
        (320, 25),
        (640, 15),
        (1280, 10),
        (2560, 6),
    ]
    sweep_rows = main_sweep(sweep_n_reps_pairs)
    sweep_n_values = [n for n, _ in sweep_n_reps_pairs]

    log_n = np.log(np.array(sweep_n_values, dtype=float))
    log_ratio = np.log(np.array([r["mean_theta_over_sqrt_n"] for r in sweep_rows]))
    slope, intercept = np.polyfit(log_n, log_ratio, 1)

    out = {
        "claim": "H-CAT31-1 Lovasz theta of random dense circulant graphs vs sqrt(n)",
        "cross_validation": {
            "max_abs_diff_eigenvalue_vs_lp": max_cv_diff,
            "n_values_tested": cv_n_values,
            "rows": cv_rows,
        },
        "main_sweep": sweep_rows,
        "log_log_slope_of_ratio_vs_n": float(slope),
        "log_log_intercept": float(intercept),
    }
    Path(__file__).parent.joinpath("metrics").mkdir(exist_ok=True)
    with open(Path(__file__).parent / "metrics" / "run.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
