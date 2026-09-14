"""Large-n Monte Carlo extension of the exact first-chaos Walsh-Hadamard decomposition
already established at small n (`check_exact_walsh_decomposition.py`, and the exact
necklace-orbit-reduced values at n=29,31,37 recorded in decision.md points 11-13).

NOT a new mathematical finding. The first-chaos decomposition itself -- W_1 (the
degree-1 Fourier-Walsh weight) and lambda_n = M_n'(1/2) = 4*Cov(X,Q) -- is already
established in this project:
  - W_1 = M_n'(1/2)^2 / (4m) = 4*Cov(X,Q)^2/m  EXACTLY for prime n (decision.md point 12b),
    a consequence of the point-4 symmetry theorem: for prime n, the multiplicative group
    Z_n^x acts transitively on the m generator coordinates via the permutation induced by
    multiplying generator indices by any unit a mod n, forcing all m singleton Fourier-Walsh
    coefficients to be equal.
  - X(S^c) = -X(S) exactly (pathwise), from theta(G)*theta(Gbar)=n (Lovasz 1979, tight for
    vertex-transitive graphs) under bit-complementation -- forces all even-degree
    Fourier-Walsh coefficients to vanish identically, so R_n := Var(X) - W_1 = sum over ODD
    |S|>=3 of (Fourier coefficient)^2.

What IS new here: pushing this same (lambda_n, W_1, R_n) decomposition into the large-n
Monte Carlo regime (n=127..2039), where exact 2^m enumeration is infeasible (m up to ~1019)
but this project's own Monte Carlo sampler (theta_via_lp + sample_circulant_neighbors from
H-CAT31-1's run.py, reused UNCHANGED here) already reaches n up to 3000. Only exact small-n
(n<=53, and specifically n<=37 for the W1/lambda_n pair) values existed before this script.

PRE-REGISTERED DECISION RULE (written before any results are computed, per this project's
Falsification Ladder discipline):
  - If both lambda_n and n*R_n appear STABLE/bounded (no visible growth trend) across the 5
    tested large n, this is strong empirical support for the decomposition
    Var(X_n) = W_1 + R_n = O(1/n).
  - If lambda_n itself grows with n (unboundedly), this is serious evidence AGAINST the
    target hypothesis Var(X_n)=O(1/n) (since n*W_1 ~ lambda_n^2/2, an unbounded lambda_n
    forces n*Var(X_n) to diverge too).
  - If lambda_n looks stable but n*R_n keeps growing, the missing mechanism is localized to
    the higher-chaos (|S|>=3) part specifically.

Do NOT write to decision.md from this script or based on its output -- the orchestrating
session re-derives key numbers from metrics/first_chaos_decomposition_large_n.json
independently before writing up any decision.md point (audit-verification-gate.md: an
agent's [VERIFIED] is the orchestrator's [INFERRED] until re-checked).
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import numpy as np
from sympy import isprime

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"

RNG_SEED_BASE = 3331000  # distinct base from run.py's own 331000 (H-CAT31-3 sweep) and
# H-CAT31-1's 31000 / H-CAT31-2 -- no seed collision with any existing sweep in this project.
POSITIVE_CONTROL_SEED_BASE = 3337000  # distinct again, for the n=37 independent-method check


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("first_chaos_large_n_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
theta_via_lp = h_cat31_1.theta_via_lp

# n, reps -- reps taper as n grows to bound wall-clock cost (LP solve cost grows with n).
SWEEP_N_REPS = [
    (127, 300),
    (251, 250),
    (509, 200),
    (1021, 150),
    (2039, 80),
]

# n=37: exact necklace-orbit-reduced value already committed in decision.md (point 13's
# table, n=29,31,37 block): n*W1 = 2.598. This is a DIFFERENT computational method
# (exhaustive/necklace-reduced exact enumeration) than the Monte Carlo + covariance
# estimator used here, so a match is genuine independent verification, not a re-run of the
# same function on the same input (the Point-52 pitfall this experiment's own skeptic
# review already flagged and this script is explicitly designed to avoid).
POSITIVE_CONTROL_N = 37
POSITIVE_CONTROL_REPS = 500
POSITIVE_CONTROL_EXACT_N_TIMES_W1 = 2.598

N_BOOTSTRAP = 2000
BOOTSTRAP_SEED = 9931

MAX_SECONDS_PER_N = 30 * 60  # stop condition: flag (don't silently truncate) if a single
# n's batch is projected to exceed this


def substrate_gate_checks() -> dict:
    """Same two closed-form checks H-CAT31-1/H-CAT31-3's own run.py already use, re-verified
    here before trusting any new large-n solve this script performs."""
    c5 = np.zeros(5)
    c5[1] = 1.0
    c5[4] = 1.0
    theta_c5 = theta_via_lp(c5)
    c5_ok = bool(abs(theta_c5 - np.sqrt(5)) < 1e-6)

    n_check = 9
    c = sample_circulant_neighbors(n_check, 0.5, 7700)
    c_bar = np.zeros(n_check)
    half = (n_check - 1) // 2
    for k in range(1, half + 1):
        c_bar[k] = 1.0 - c[k]
        c_bar[n_check - k] = 1.0 - c[n_check - k]
    theta_g = theta_via_lp(c)
    theta_gbar = theta_via_lp(c_bar)
    product = theta_g * theta_gbar
    identity_ok = bool(abs(product - n_check) < 1e-4)

    return {
        "theta_c5": theta_c5,
        "theta_c5_expected": float(np.sqrt(5)),
        "c5_check_passed": c5_ok,
        "theta_g_times_gbar": product,
        "n_check": n_check,
        "identity_check_passed": identity_ok,
        "substrate_ready": c5_ok and identity_ok,
    }


def verify_primes() -> dict:
    checked = {}
    for n, _ in SWEEP_N_REPS:
        checked[n] = bool(isprime(n))
    checked[POSITIVE_CONTROL_N] = bool(isprime(POSITIVE_CONTROL_N))
    all_prime = all(checked.values())
    return {"checked": {str(k): v for k, v in checked.items()}, "all_prime": all_prime}


def sample_x_and_q(n: int, reps: int, seed_base: int) -> tuple[np.ndarray, np.ndarray]:
    """Draw `reps` i.i.d. samples of (X, Q) at fixed prime n.

    X = log(theta(G)/sqrt(n)), Q = count of 'on' generators among the m free bits.
    For prime n (odd), sample_circulant_neighbors's `half = (n-1)//2 = m` and its internal
    `picks` boolean array IS exactly the m free bits -- c[k]=1 for k in 1..half iff
    picks[k-1] is True (verified by reading sample_circulant_neighbors's source: the n%2==0
    antipodal-offset branch never fires for odd/prime n). So Q = sum(c[1:half+1]) recovers
    sum(picks) exactly without needing to re-derive picks separately.
    """
    m = (n - 1) // 2
    x = np.empty(reps)
    q = np.empty(reps)
    for i in range(reps):
        seed = seed_base + n * 100000 + i
        c = sample_circulant_neighbors(n, 0.5, seed)
        theta = theta_via_lp(c)
        x[i] = np.log(theta / np.sqrt(n))
        q[i] = c[1 : m + 1].sum()
    return x, q


def compute_decomposition(x: np.ndarray, q: np.ndarray, n: int) -> dict:
    m = (n - 1) // 2
    cov_xq = float(np.cov(x, q, ddof=1)[0, 1])
    lambda_n_hat = 4.0 * cov_xq
    w1_hat = 4.0 * cov_xq**2 / m
    var_x_hat = float(np.var(x, ddof=1))
    r_n_hat = var_x_hat - w1_hat
    return {
        "m": m,
        "cov_xq_hat": cov_xq,
        "lambda_n_hat": lambda_n_hat,
        "w1_hat": w1_hat,
        "var_x_hat": var_x_hat,
        "r_n_hat": r_n_hat,
        "n_times_w1_hat": n * w1_hat,
        "n_times_r_n_hat": n * r_n_hat,
        "r_n_over_var_x": float(r_n_hat / var_x_hat) if var_x_hat != 0 else float("nan"),
    }


def paired_bootstrap_ci(x: np.ndarray, q: np.ndarray, n: int, n_boot: int, seed: int) -> dict:
    """Resample the (X,Q) PAIRS jointly (they're correlated per-sample, not independent) --
    N_BOOTSTRAP replicates, 95% percentile CI on lambda_n, n*W1, n*R_n."""
    m = (n - 1) // 2
    rng = np.random.default_rng(seed)
    reps = len(x)
    boot_lambda = np.empty(n_boot)
    boot_n_w1 = np.empty(n_boot)
    boot_n_rn = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, reps, size=reps)
        xb = x[idx]
        qb = q[idx]
        cov_b = np.cov(xb, qb, ddof=1)[0, 1]
        lambda_b = 4.0 * cov_b
        w1_b = 4.0 * cov_b**2 / m
        var_b = np.var(xb, ddof=1)
        rn_b = var_b - w1_b
        boot_lambda[b] = lambda_b
        boot_n_w1[b] = n * w1_b
        boot_n_rn[b] = n * rn_b

    def ci(arr):
        lo, hi = np.percentile(arr, [2.5, 97.5])
        return [float(lo), float(hi)]

    return {
        "lambda_n_ci95": ci(boot_lambda),
        "n_times_w1_ci95": ci(boot_n_w1),
        "n_times_r_n_ci95": ci(boot_n_rn),
    }


def run_positive_control() -> dict:
    """Independent-method check: run THIS script's Monte Carlo estimator at n=37, where an
    exact (different-method) value of n*W1 is already committed in decision.md. Confirm the
    bootstrap 95% CI contains that exact value. Genuinely independent because it compares
    Monte Carlo sampling + covariance estimation against an already-published
    exact-enumeration result from earlier, unrelated code -- not a re-run of the same
    function on the same input."""
    t0 = time.time()
    x, q = sample_x_and_q(POSITIVE_CONTROL_N, POSITIVE_CONTROL_REPS, POSITIVE_CONTROL_SEED_BASE)
    elapsed = time.time() - t0
    decomp = compute_decomposition(x, q, POSITIVE_CONTROL_N)
    ci = paired_bootstrap_ci(
        x, q, POSITIVE_CONTROL_N, N_BOOTSTRAP, BOOTSTRAP_SEED + POSITIVE_CONTROL_N
    )
    lo, hi = ci["n_times_w1_ci95"]
    contains_exact = bool(lo <= POSITIVE_CONTROL_EXACT_N_TIMES_W1 <= hi)
    result = {
        "n": POSITIVE_CONTROL_N,
        "reps": POSITIVE_CONTROL_REPS,
        "elapsed_seconds": elapsed,
        "decomposition": decomp,
        "bootstrap_ci": ci,
        "exact_n_times_w1_reference": POSITIVE_CONTROL_EXACT_N_TIMES_W1,
        "exact_reference_source": (
            "decision.md point 13 table (necklace-orbit-reduced exact enumeration, n=29,31,37)"
        ),
        "ci_contains_exact_value": contains_exact,
        "control_passed": contains_exact,
    }
    print(
        f"[positive control] n={POSITIVE_CONTROL_N} reps={POSITIVE_CONTROL_REPS} "
        f"n*W1_hat={decomp['n_times_w1_hat']:.4f} CI=[{lo:.4f},{hi:.4f}] "
        f"exact_ref={POSITIVE_CONTROL_EXACT_N_TIMES_W1} "
        f"contains_exact={contains_exact} elapsed={elapsed:.1f}s",
        flush=True,
    )
    return result


def run_sweep() -> tuple[list[dict], list[str]]:
    rows = []
    incomplete_ns = []
    for n, reps in SWEEP_N_REPS:
        t0 = time.time()
        x, q = sample_x_and_q(n, reps, RNG_SEED_BASE)
        elapsed = time.time() - t0

        if elapsed > MAX_SECONDS_PER_N:
            incomplete_ns.append(n)
            print(
                f"n={n:5d} reps={reps:4d} STOP-CONDITION-TRIGGERED elapsed={elapsed:.1f}s "
                f"(exceeded MAX_SECONDS_PER_N={MAX_SECONDS_PER_N}s) -- reporting partial "
                f"result for this n, flagged incomplete",
                flush=True,
            )

        decomp = compute_decomposition(x, q, n)
        ci = paired_bootstrap_ci(x, q, n, N_BOOTSTRAP, BOOTSTRAP_SEED + n)

        row = {
            "n": n,
            "n_reps": reps,
            "elapsed_seconds": elapsed,
            **decomp,
            "bootstrap_ci": ci,
            "flagged_incomplete_slow": n in incomplete_ns,
        }
        rows.append(row)
        lam_lo, lam_hi = ci["lambda_n_ci95"]
        w1_lo, w1_hi = ci["n_times_w1_ci95"]
        rn_lo, rn_hi = ci["n_times_r_n_ci95"]
        print(
            f"n={n:5d} reps={reps:4d} lambda_n={decomp['lambda_n_hat']:.4f} "
            f"CI=[{lam_lo:.4f},{lam_hi:.4f}] | n*W1={decomp['n_times_w1_hat']:.4f} "
            f"CI=[{w1_lo:.4f},{w1_hi:.4f}] | n*R_n={decomp['n_times_r_n_hat']:.4f} "
            f"CI=[{rn_lo:.4f},{rn_hi:.4f}] | R_n/Var_X={decomp['r_n_over_var_x']:.4f} "
            f"elapsed={elapsed:.1f}s",
            flush=True,
        )
    return rows, incomplete_ns


def classify_decision_rule(rows: list[dict]) -> dict:
    """Apply the pre-registered decision rule from the module docstring. 'Stable/bounded'
    operationalized as: the sequence's OLS trend in n is not clearly monotonically diverging
    relative to its own CI widths -- reported quantitatively (slope + whether CIs overlap
    across the n range), final classification stated as this script's own read, subject to
    independent re-verification by the orchestrating session (per this script's own header)."""
    ns = np.array([r["n"] for r in rows], dtype=float)
    lambda_vals = np.array([r["lambda_n_hat"] for r in rows], dtype=float)
    n_rn_vals = np.array([r["n_times_r_n_hat"] for r in rows], dtype=float)
    n_w1_vals = np.array([r["n_times_w1_hat"] for r in rows], dtype=float)

    lambda_slope = float(np.polyfit(ns, lambda_vals, 1)[0]) if len(ns) >= 2 else float("nan")
    n_rn_slope = float(np.polyfit(ns, n_rn_vals, 1)[0]) if len(ns) >= 2 else float("nan")
    n_w1_slope = float(np.polyfit(ns, n_w1_vals, 1)[0]) if len(ns) >= 2 else float("nan")

    # CI-overlap check across the FULL tested range (first vs last n) as a simple stability
    # signal, reported alongside the slope (not a substitute for it).
    lambda_ci_first = rows[0]["bootstrap_ci"]["lambda_n_ci95"]
    lambda_ci_last = rows[-1]["bootstrap_ci"]["lambda_n_ci95"]
    lambda_ci_overlap = bool(
        lambda_ci_first[0] <= lambda_ci_last[1] and lambda_ci_last[0] <= lambda_ci_first[1]
    )
    n_rn_ci_first = rows[0]["bootstrap_ci"]["n_times_r_n_ci95"]
    n_rn_ci_last = rows[-1]["bootstrap_ci"]["n_times_r_n_ci95"]
    n_rn_ci_overlap = bool(
        n_rn_ci_first[0] <= n_rn_ci_last[1] and n_rn_ci_last[0] <= n_rn_ci_first[1]
    )

    if lambda_ci_overlap and n_rn_ci_overlap:
        outcome = "STABLE-SUPPORTS-O(1/n)"
    elif not lambda_ci_overlap:
        outcome = "LAMBDA_N-GROWING-EVIDENCE-AGAINST-O(1/n)"
    else:
        outcome = "LAMBDA_N-STABLE-BUT-R_N-GROWING-HIGHER-CHAOS-MECHANISM"

    return {
        "lambda_n_ols_slope_vs_n": lambda_slope,
        "n_times_r_n_ols_slope_vs_n": n_rn_slope,
        "n_times_w1_ols_slope_vs_n": n_w1_slope,
        "lambda_n_ci_overlap_first_vs_last": lambda_ci_overlap,
        "n_times_r_n_ci_overlap_first_vs_last": n_rn_ci_overlap,
        "outcome": outcome,
    }


def run() -> dict:
    substrate = substrate_gate_checks()
    primes = verify_primes()

    if not substrate["substrate_ready"] or not primes["all_prime"]:
        out = {
            "status": "BLOCKED-INFRASTRUCTURE",
            "substrate_gate": substrate,
            "prime_verification": primes,
        }
        METRICS.mkdir(exist_ok=True)
        with open(METRICS / "first_chaos_decomposition_large_n.json", "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, default=str)
        print(json.dumps(out, indent=2, default=str))
        return out

    total_t0 = time.time()
    positive_control = run_positive_control()
    sweep_rows, incomplete_ns = run_sweep()
    decision = classify_decision_rule(sweep_rows) if len(sweep_rows) >= 2 else {}
    total_elapsed = time.time() - total_t0

    out = {
        "claim": (
            "H-CAT31-3 first-chaos decomposition (lambda_n, W_1, R_n) extended to "
            "large-n Monte Carlo regime (n=127..2039)"
        ),
        "substrate_gate": substrate,
        "prime_verification": primes,
        "positive_control_n37": positive_control,
        "sweep": sweep_rows,
        "incomplete_ns": incomplete_ns,
        "decision_rule_classification": decision,
        "total_elapsed_seconds": total_elapsed,
    }
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "first_chaos_decomposition_large_n.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    run()
