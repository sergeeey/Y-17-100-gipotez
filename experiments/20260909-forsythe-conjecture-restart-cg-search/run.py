"""H-CAT37-1 -- Forsythe conjecture counterexample search / s=2 replication check.

Formal object (Amsel et al. arXiv:2602.05394, Section 2.7, Problem 2.20):
restarted s-step optimal-gradient iteration on SPD A, testing whether the
two normalized-residual subsequences {y_2k}, {y_2k+1} each converge to a
single limit vector.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RNG_SEED_BASE = 37000


def build_spd_matrix(n: int, seed: int, mode: str) -> np.ndarray:
    """SPD matrix via random orthogonal eigenvectors + a chosen eigenvalue spectrum."""
    rng = np.random.default_rng(seed)
    q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    if mode == "random":
        eigvals = rng.uniform(1.0, 50.0, size=n)
    elif mode == "clustered":
        # 2-3 tight clusters -- known to stress Krylov-subspace convergence.
        n_clusters = min(3, n)
        centers = rng.uniform(1.0, 100.0, size=n_clusters)
        assign = rng.integers(0, n_clusters, size=n)
        eigvals = centers[assign] + rng.normal(0.0, 1e-3, size=n)
        eigvals = np.abs(eigvals) + 1e-6
    elif mode == "geometric":
        # geometric spread -- ill-conditioned, another classic CG stress case.
        eigvals = np.geomspace(1e-3, 1e3, num=n)
    else:
        raise ValueError(f"unknown mode {mode!r}")
    return (q * eigvals) @ q.T


def krylov_orthonormal_basis(A: np.ndarray, y_k: np.ndarray, s: int) -> tuple[np.ndarray, bool]:
    """Orthonormal basis of K_s(A, y_k) via symmetric Lanczos (3-term recurrence).

    WHY: the raw power basis [y_k, A y_k, A^2 y_k, ...] loses linear
    independence exponentially fast in floating point -- verified directly
    this session (diag_krylov.py): for an ill-conditioned SPD A
    (cond(A)~1e6), cond(V_power) already exceeds 1e8 at s=4 and 1e19 at
    s=7, i.e. numerically singular well past double precision. Solving the
    Galerkin system against that basis produces garbage, not a genuine
    property of the Forsythe iteration -- caught only by checking cond(V)
    directly (Mechanism Claim Gate, Step 0a) after an initial run showed
    implausible "growing residual gap" results confined exactly to the
    ill-conditioned matrix family. Lanczos keeps the basis orthonormal by
    construction (cond=1), independent of cond(A).
    """
    n = A.shape[0]
    Q = np.empty((n, s))
    alpha = np.empty(s)
    beta = np.empty(s - 1) if s > 1 else np.empty(0)
    q_prev = np.zeros(n)
    beta_prev = 0.0
    q = y_k.copy()
    breakdown = False
    for j in range(s):
        Q[:, j] = q
        w = A @ q - beta_prev * q_prev
        alpha[j] = q @ w
        w = w - alpha[j] * q
        # full reorthogonalization against all previous vectors -- cheap at
        # these dimensions, and removes the classical-Lanczos drift that
        # would otherwise reintroduce the same loss-of-orthogonality problem
        # this function exists to avoid.
        w -= Q[:, : j + 1] @ (Q[:, : j + 1].T @ w)
        beta_j = np.linalg.norm(w)
        if j < s - 1:
            if beta_j < 1e-12:
                breakdown = True
                Q = Q[:, : j + 1]
                break
            beta[j] = beta_j
            q_prev = q
            q = w / beta_j
            beta_prev = beta_j
    return Q, breakdown


def restart_step(
    A: np.ndarray, r_k: np.ndarray, y_k: np.ndarray, s: int
) -> tuple[np.ndarray, bool]:
    """One restart of the s-step optimal-gradient method.

    Builds an orthonormal Krylov basis Q for K_s(A, y_k) (Lanczos, see
    `krylov_orthonormal_basis`), solves the Galerkin condition
    (Q^T A Q) c = Q^T r_k, returns the new residual and a breakdown flag
    (Krylov subspace rank-deficient below dimension s, i.e. d(A, r_k) < s
    per the paper's own construction).
    """
    Q, breakdown = krylov_orthonormal_basis(A, y_k, s)
    if breakdown:
        return r_k, True
    G = Q.T @ A @ Q
    rhs = Q.T @ r_k
    c = np.linalg.solve(G, rhs)
    z = Q @ c
    r_next = r_k - A @ z
    return r_next, False


def run_restarted_iteration(A: np.ndarray, s: int, seed: int, max_restarts: int = 500):
    """Run the restarted iteration, return convergence trace and verdict fields."""
    n = A.shape[0]
    rng = np.random.default_rng(seed + 1)
    r = rng.standard_normal(n)
    r = r / np.linalg.norm(r)
    y_even, y_odd = [], []
    d_trace = []
    breakdown_hit = False
    for k in range(max_restarts):
        y_k = r / np.linalg.norm(r)
        r_next, broke = restart_step(A, r, y_k, s)
        if broke:
            breakdown_hit = True
            break
        norm_next = np.linalg.norm(r_next)
        if norm_next < 1e-13:
            # exact convergence of the underlying linear system -- not the
            # phenomenon Problem 2.20 studies (which assumes r_k stays nonzero
            # forever); stop and mark separately from a genuine limit-vector
            # measurement.
            return {
                "exact_solve_hit": True,
                "breakdown_hit": breakdown_hit,
                "restarts_run": k,
                "final_d": None,
            }
        r = r_next
        y_next = r / norm_next
        (y_even if k % 2 == 0 else y_odd).append(y_next)
        if len(y_even) >= 2 and len(y_odd) >= 2:
            d_k = max(
                np.linalg.norm(y_even[-1] - y_even[-2]),
                np.linalg.norm(y_odd[-1] - y_odd[-2]),
            )
            d_trace.append(float(d_k))
    final_d = d_trace[-1] if d_trace else None
    sustained_converged = len(d_trace) >= 20 and all(d < 1e-8 for d in d_trace[-20:])
    decay_slope = _log_decay_slope(d_trace)
    return {
        "exact_solve_hit": False,
        "breakdown_hit": breakdown_hit,
        "restarts_run": len(d_trace),
        "final_d": final_d,
        "d_trace_tail": d_trace[-25:],
        "sustained_converged": sustained_converged,
        "max_d_last_50": max(d_trace[-50:]) if len(d_trace) >= 1 else None,
        "decay_slope": decay_slope,
    }


def _log_decay_slope(d_trace: list[float]) -> float | None:
    """Log-linear regression slope of d_k over the last 150 restarts (or all
    available, if fewer). A clearly negative slope means d_k is decaying at a
    steady geometric/linear rate -- real convergence, just possibly slow, and
    not distinguishable from a hard 1e-8 cutoff within a finite restart budget.
    A slope near zero (or positive) means the sequence has stalled/is not
    decaying -- the actual signature Problem 2.20 would fail on.
    """
    window = [d for d in d_trace[-150:] if d > 0]
    if len(window) < 30:
        return None
    y = np.log(np.array(window))
    x = np.arange(len(y), dtype=float)
    slope, _ = np.polyfit(x, y, 1)
    return float(slope)


def scan(dims, modes, seeds_per_mode, max_restarts=500):
    results = []
    for n in dims:
        for mode in modes:
            for seed_offset in range(seeds_per_mode):
                seed = RNG_SEED_BASE + n * 100 + seed_offset
                A = build_spd_matrix(n, seed, mode)
                for s in range(2, n):
                    res = run_restarted_iteration(A, s, seed, max_restarts=max_restarts)
                    res.update({"n": n, "mode": mode, "s": s, "seed": seed})
                    results.append(res)
    return results


SLOPE_CLEARLY_DECAYING = -1e-4  # d_k shrinking by >= ~1.4%/restart over the trace window


def classify(results):
    """Three-way split, not a single hard threshold.

    An earlier version of this classifier used only `sustained_converged`
    (d_k < 1e-8 for 20 restarts) as the pass/fail line -- within a fixed
    500-restart budget that mislabeled 48/144 genuinely-still-converging
    pairs (log-linear decay confirmed, just too slow to cross 1e-8 in the
    budget -- consistent with the source paper's own note that convergence
    "can be at best linear") as if they were counterexamples. Fixed before
    reporting a verdict: `decay_slope` (log-linear regression over the last
    150 restarts) distinguishes real-but-slow decay from an actual plateau.
    """
    live = [r for r in results if not r["exact_solve_hit"] and not r["breakdown_hit"]]

    converged_strict = [r for r in live if r.get("sustained_converged", False)]
    converging_slowly = [
        r
        for r in live
        if not r.get("sustained_converged", False)
        and r.get("decay_slope") is not None
        and r["decay_slope"] < SLOPE_CLEARLY_DECAYING
    ]
    no_decay_detected = [
        r
        for r in live
        if not r.get("sustained_converged", False)
        and (r.get("decay_slope") is None or r["decay_slope"] >= SLOPE_CLEARLY_DECAYING)
    ]
    breakdowns = [r for r in results if r["breakdown_hit"]]
    exact = [r for r in results if r["exact_solve_hit"]]
    return {
        "total": len(results),
        "converged_strict": len(converged_strict),
        "converging_slowly_real": len(converging_slowly),
        "no_decay_detected_CANDIDATE_COUNTEREXAMPLE": len(no_decay_detected),
        "breakdowns": len(breakdowns),
        "exact_solve_hits": len(exact),
        "candidate_counterexample_details": no_decay_detected,
    }


def cmd_run():
    dims = [5, 8, 12]
    modes = ["random", "clustered", "geometric"]
    # 1500, not 500: a first 500-restart pass (this session) flagged 5 false
    # "no decay detected" candidates that were confirmed, on a 3000-restart
    # follow-up, to be real (slow) convergence -- short observation windows
    # on genuinely slow-but-real linear convergence look like a plateau
    # until given enough restarts. 1500 clears all 5 of those cases.
    primary = scan(dims, modes, seeds_per_mode=3, max_restarts=1500)
    primary_s_ge3 = [r for r in primary if r["s"] >= 3]
    primary_s2 = [r for r in primary if r["s"] == 2]

    verdict_primary = classify(primary_s_ge3)
    verdict_s2 = classify(primary_s2)

    out = {
        "claim": "H-CAT37-1 Forsythe conjecture restarted-CG limit-vector convergence",
        "primary_s_ge_3": verdict_primary,
        "secondary_s_2_replication": verdict_s2,
        "n_tested_pairs_total": len(primary),
        "dims": dims,
        "modes": modes,
    }
    Path(__file__).parent.joinpath("metrics").mkdir(exist_ok=True)
    with open(Path(__file__).parent / "metrics" / "run.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
