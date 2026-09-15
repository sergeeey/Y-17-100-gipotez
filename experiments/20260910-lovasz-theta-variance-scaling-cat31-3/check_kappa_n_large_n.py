"""Cleaner replacement route for the noisy `R_n := Var(X) - W_1` diagnostic Point 53 pushed
into the large-`n` Monte Carlo regime. Point 53's own estimator subtracted two close numbers
(a sample variance and a squared-covariance quantity) and was visibly noisy: `R_n`'s bootstrap
CI crossed zero at `n=509,1021`.

NOT new mathematics -- this script SYNTHESIZES already-established pieces plus one newly-derived
sign relation into a cleaner statistic:

  - `B_n = (m/4)*E[delta_i^2]` -- the standard Efron-Stein bounded-difference quantity, already
    an established identity in this project (decision.md point 12, `delta_i(S)=X(S)-X(S union{i})`
    for `i` not in `S`; `delta_i(S)>=0` always since theta is monotone non-increasing under edge
    addition).
  - `W_1 = lambda_n^2/(4m)`, `lambda_n = M_n'(1/2) = 4*Cov(X,Q)` -- already established EXACTLY
    for prime `n` (decision.md point 12b), via the point-4 prime-transitivity symmetry theorem.
  - `V_n <= (B_n + 2*W_1)/3` -- the sharpened Efron-Stein inequality, already PROVEN and exactly
    verified at `n=9..25` (decision.md point 12a).

  NEWLY DERIVED THIS SESSION (independently re-derived and confirmed by both the user and the
  orchestrating session, via the Fourier-Walsh singleton-coefficient identity
  `f_hat({i}) = -E[D_i f]/2` combined with the already-established `f_hat({i}) = -lambda_n/(2m)`
  for prime `n`): `lambda_n = -m*E[delta_i]` (note the sign: `delta_i>=0` always, `lambda_n` is
  empirically NEGATIVE -- e.g. Point 53 measured `lambda_n` in `[-3.05,-2.02]` across
  `n=127..2039` -- so a version of this claim WITHOUT the minus sign is wrong in sign, though
  right in magnitude: `|lambda_n| = m*E[delta_i]`).

Combining these: `kappa_n := B_n/W_1 = E[delta_i^2]/E[delta_i]^2` (squared coefficient of
variation of the single-generator sensitivity), and the sharpened Efron-Stein bound restates as

    V_n <= (kappa_n+2)/3 * lambda_n^2/(4m)

Since `m =~ n`: if `lambda_n=O(1)` AND `kappa_n=O(1)`, then `Var(X_n)=O(1/n)` follows from this
ALREADY-PROVEN inequality -- no new theorem needed, just two bounded-quantity claims. That is
the target this script measures.

Positive control / Oracle Adequacy Gate -- exact values already committed in decision.md at
`n=37` (point 13's table): `n*W_1=2.598`, `kappa_n=2.004`, `n*Var(X)=3.272`.

Reuses UNCHANGED: `sample_circulant_neighbors`/`theta_via_lp` from H-CAT31-1's `run.py` (same
importlib-loading pattern as `check_first_chaos_decomposition_large_n.py`); the `flip_generator`
logic from `check_single_generator_sensitivity_n3000.py` (toggles both mirrored bits
`c[i]`/`c[n-i]` together, matching how a single random bit controls both).

Do NOT write to decision.md from this script -- the orchestrating session re-derives key
numbers from `metrics/kappa_n_large_n.json` and the per-n `.npz` raw-sample files independently
before writing up any decision.md point (audit-verification-gate.md: an agent's [VERIFIED] is
the orchestrator's [INFERRED] until re-checked).
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import numpy as np
from scipy import stats
from sympy import isprime

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"

# Distinct seed namespace -- checked against every RNG_SEED_BASE/BOOTSTRAP_SEED already used in
# this experiment's other scripts (31000/331000/332000/333000/334000/335000/3331000/3337000/
# 991/9931) before picking these.
RNG_SEED_BASE = 3341000
POSITIVE_CONTROL_SEED_BASE = 3347000
PILOT_SEED_BASE = 3348000
BOOTSTRAP_SEED = 99341
SYNTHETIC_SANITY_SEED = 5551000

h_cat31_1 = None  # loaded in _load_dependencies()
sample_circulant_neighbors = None
theta_via_lp = None


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_dependencies() -> None:
    global h_cat31_1, sample_circulant_neighbors, theta_via_lp
    h_cat31_1 = _load_module("kappa_n_large_n_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
    sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
    theta_via_lp = h_cat31_1.theta_via_lp


# TEST_GENERATOR_INDEX: a SINGLE fixed generator index, not multiple. For prime n, decision.md
# point 4's prime-transitivity theorem proves the multiplicative group Z_n^x acts transitively
# on the m generator coordinates, forcing all m single-generator influences (and hence all
# delta_i distributions) to be statistically EQUIVALENT -- so testing one fixed index and
# testing several and averaging carry the same expected information here, and one index halves
# the LP-solve cost relative to this project's existing multi-index sensitivity scripts
# (check_single_generator_sensitivity*.py), which do NOT restrict to prime n and so cannot rely
# on this argument.
TEST_GENERATOR_INDEX = 1

# n, reps -- SAME as Point 53 (check_first_chaos_decomposition_large_n.py's SWEEP_N_REPS).
# Point 53's own elapsed times at these reps: 2.92s/8.90s/37.45s/167.79s/623.86s (n=127..2039),
# each rep costing ONE theta_via_lp call. This script's reps cost TWO calls (base + flip), so
# projected cost is roughly double: ~5.8/17.8/74.9/335.6/1247.7s. The largest, n=2039 at
# ~1247.7s (~20.8 min), stays under MAX_SECONDS_PER_N=1800s (30 min) with ~27% margin, so no
# rep reduction is applied up front -- the actual elapsed is still checked at runtime below and
# flagged (not silently truncated) if this projection is wrong in practice.
SWEEP_N_REPS = [
    (127, 300),
    (251, 250),
    (509, 200),
    (1021, 150),
    (2039, 80),
]

POSITIVE_CONTROL_N = 37
POSITIVE_CONTROL_REPS = 500  # matches Point 53's own n=37 control rep count
POSITIVE_CONTROL_EXACT = {
    "n_times_w1": 2.598,
    "kappa_n": 2.004,
    "n_times_var_x": 3.272,
}
POSITIVE_CONTROL_EXACT_SOURCE = (
    "decision.md point 13 table (necklace-orbit-reduced exact enumeration, n=29,31,37)"
)
# exact n*R_n at n=37, from the SAME table: n*Var(X) - n*W1 = 3.272 - 2.598 = 0.674
EXACT_N_TIMES_R_N_AT_37 = (
    POSITIVE_CONTROL_EXACT["n_times_var_x"] - POSITIVE_CONTROL_EXACT["n_times_w1"]
)

PILOT_N = 37
PILOT_REPS = 20

N_BOOTSTRAP = 2000
MAX_SECONDS_PER_N = 30 * 60


def substrate_gate_checks() -> dict:
    """Same two closed-form checks this experiment's other large-n scripts already use."""
    c5 = np.zeros(5)
    c5[1] = 1.0
    c5[4] = 1.0
    theta_c5 = theta_via_lp(c5)
    c5_ok = bool(abs(theta_c5 - np.sqrt(5)) < 1e-6)

    n_check = 9
    c = sample_circulant_neighbors(n_check, 0.5, 7710)
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
    checked[PILOT_N] = bool(isprime(PILOT_N))
    all_prime = all(checked.values())
    return {"checked": {str(k): v for k, v in checked.items()}, "all_prime": all_prime}


def flip_generator(c: np.ndarray, i: int) -> np.ndarray:
    """Toggle generator bit i (both mirrored edges c[i], c[n-i] together) -- reused unchanged
    from check_single_generator_sensitivity_n3000.py."""
    n = len(c)
    c2 = c.copy()
    c2[i] = 1.0 - c2[i]
    c2[n - i] = 1.0 - c2[n - i]
    return c2


def sample_x_q_delta(
    n: int, reps: int, seed_base: int, gen_index: int = TEST_GENERATOR_INDEX
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Draw `reps` i.i.d. samples of (X, Q, delta_i_signed) at fixed prime n.

    delta_i_signed follows the established convention delta_i(S) = X(S) - X(S union {i}) for i
    not in S:
      - c[gen_index] == 0 (i off, current draw IS S): delta_signed = X0 - X_flip
        (c_flip = S union {i})
      - c[gen_index] == 1 (i on, current draw is S union {i}): delta_signed = X_flip - X0
        (c_flip = S, i.e. delta_i(S) = X(c_flip) - X(c) = X_flip - X0)
    Both branches compute delta_i(S) for the appropriate S -- NOT |X0-X_flip| -- so the
    established delta_i(S)>=0 monotonicity theorem is a real, checkable claim on this array, not
    true by construction.
    """
    m = (n - 1) // 2
    x = np.empty(reps)
    q = np.empty(reps)
    delta = np.empty(reps)
    for i in range(reps):
        seed = seed_base + n * 100000 + i
        c = sample_circulant_neighbors(n, 0.5, seed)
        theta0 = theta_via_lp(c)
        x0 = np.log(theta0 / np.sqrt(n))
        q[i] = c[1 : m + 1].sum()

        c_flip = flip_generator(c, gen_index)
        theta1 = theta_via_lp(c_flip)
        x1 = np.log(theta1 / np.sqrt(n))

        x[i] = x0
        if c[gen_index] < 0.5:
            delta[i] = x0 - x1
        else:
            delta[i] = x1 - x0
    return x, q, delta


def pilot_sign_check() -> dict:
    """Verify delta_i_signed >= 0 (up to LP-solver floating noise) on a small pilot batch at
    n=37 BEFORE running the full sweep, per this script's own hard requirement -- a silently
    wrong sign must stop the script, not propagate into the full run."""
    _x, _q, delta = sample_x_q_delta(PILOT_N, PILOT_REPS, PILOT_SEED_BASE)
    tol = -1e-6
    min_delta = float(delta.min())
    passed = bool(min_delta >= tol)
    return {
        "n": PILOT_N,
        "reps": PILOT_REPS,
        "min_delta_i_signed": min_delta,
        "max_delta_i_signed": float(delta.max()),
        "mean_delta_i_signed": float(delta.mean()),
        "tolerance": tol,
        "sign_check_passed": passed,
    }


def compute_kappa_decomposition(x: np.ndarray, q: np.ndarray, delta: np.ndarray, n: int) -> dict:
    m = (n - 1) // 2
    cov_xq = float(np.cov(x, q, ddof=1)[0, 1])
    lambda_hat = 4.0 * cov_xq
    w1_hat = lambda_hat**2 / (4.0 * m)
    b_hat = (m / 4.0) * float(np.mean(delta**2))
    kappa_hat = b_hat / w1_hat if w1_hat != 0 else float("nan")
    # internal consistency check: kappa_n = m^2*E[delta^2]/lambda_n^2, algebraically identical
    kappa_hat_alt = (
        (m**2) * float(np.mean(delta**2)) / (lambda_hat**2) if lambda_hat != 0 else float("nan")
    )
    var_x_hat = float(np.var(x, ddof=1))
    u_hat = (b_hat + 2.0 * w1_hat) / 3.0
    return {
        "m": m,
        "cov_xq_hat": cov_xq,
        "lambda_n_hat": lambda_hat,
        "w1_hat": w1_hat,
        "b_hat": b_hat,
        "kappa_hat": kappa_hat,
        "kappa_hat_alt_consistency": kappa_hat_alt,
        "kappa_consistency_abs_diff": abs(kappa_hat - kappa_hat_alt),
        "var_x_hat": var_x_hat,
        "u_hat": u_hat,
        "n_times_u_hat": n * u_hat,
        "u_hat_over_var_x": u_hat / var_x_hat if var_x_hat != 0 else float("nan"),
        "u_bound_holds": bool(u_hat >= var_x_hat),
        "mean_x_hat": float(np.mean(x)),
    }


def r_n_addendum_point_estimates(x: np.ndarray, q: np.ndarray, n: int) -> dict:
    """Point 53's original R_n=Var(X)-W1, plus two improved estimators using the SAME (X,Q)
    samples -- no additional theta_via_lp calls.

    Cross-fit regression residual (a): split by index parity, estimate beta on one half using
    the KNOWN EXACT Var(Z)=m/4 (Z=Q-m/2, Q~Binomial(m,0.5) exactly under this project's p=0.5
    sampler), measure the out-of-sample residual on the other half, swap, average.

    U-statistic estimator (b), formula as literally specified in this task:
        R_U_hat = (1/N)*sum(X_r^2) - (4/m)*[(sum(Y_r))^2 - sum(Y_r^2)] / (N*(N-1))
    with Y_r = X_r*Z_r.

    ALGEBRAIC CHECK (done before trusting this formula, per this script's own mandate --
    see module docstring's Falsification Ladder discipline):
    (sum(Y_r))^2 - sum(Y_r^2) = sum_{r!=s} Y_r*Y_s (all N*(N-1) ordered pairs), so dividing by
    N*(N-1) is the U-statistic average of Y_r*Y_s over r!=s -- an UNBIASED estimator of
    E[Y_r]*E[Y_s] = E[Y]^2 (independent draws) = E[X*Z]^2 = Cov(X,Z)^2 (since E[Z]=0 exactly).
    (1/N)*sum(X_r^2) is an unbiased estimator of E[X^2], NOT Var(X). So R_U_hat is unbiased for
        E[X^2] - (4/m)*Cov(X,Z)^2  =  Var(X) - (4/m)*Cov(X,Z)^2 + (E[X])^2
                                    =  R_n + (E[X])^2   [since W_1 = (4/m)*Cov(X,Z)^2 exactly,
                                                          Cov(X,Z)=Cov(X,Q)]
    i.e. R_U_hat as GIVEN targets E[(X-beta*Z)^2] (no intercept subtracted), which equals the
    true R_n=Var(X)-W_1 ONLY when E[X]=0. On real data E[X]=E[log(theta/sqrt(n))] is small but
    NOT exactly 0 (mean_theta/sqrt(n) approaches 1 as n grows but isn't exactly 1 at finite n --
    see decision.md's own mean-ratio column), so R_U_hat as literally specified carries a small
    upward bias of (E[X])^2. Both the raw (as-specified) and a practical mean-corrected version
    (subtracting the sample (mean(X))^2, targeting R_n directly) are reported below; the
    synthetic sanity check (separate function) demonstrates this bias explicitly on cases with
    E[X]=0 and E[X]!=0.
    """
    m = (n - 1) // 2
    z = q - m / 2.0
    var_z_exact = m / 4.0

    orig_r_n = float(np.var(x, ddof=1)) - (4.0 * float(np.cov(x, q, ddof=1)[0, 1]) ** 2 / m)

    # (a) cross-fit regression residual, split by index parity
    idx_even = np.arange(len(x)) % 2 == 0
    idx_odd = ~idx_even

    def _fit_beta(xh, zh):
        cov_xz = float(np.cov(xh, zh, ddof=1)[0, 1])
        return cov_xz / var_z_exact

    def _residual_mse(beta, xh, zh):
        return float(np.mean((xh - beta * zh) ** 2))

    beta_a = _fit_beta(x[idx_even], z[idx_even])
    resid_b_on_a = _residual_mse(beta_a, x[idx_odd], z[idx_odd])
    beta_b = _fit_beta(x[idx_odd], z[idx_odd])
    resid_a_on_b = _residual_mse(beta_b, x[idx_even], z[idx_even])
    crossfit_r_n = 0.5 * (resid_b_on_a + resid_a_on_b)

    # (b) U-statistic, exact formula as specified
    y = x * z
    N = len(x)
    sum_y = float(np.sum(y))
    sum_y2 = float(np.sum(y**2))
    u_term = (sum_y**2 - sum_y2) / (N * (N - 1))
    r_u_raw = float(np.mean(x**2)) - (4.0 / m) * u_term
    mean_x = float(np.mean(x))
    r_u_corrected = r_u_raw - mean_x**2

    return {
        "n": n,
        "reps": N,
        "orig_var_minus_w1": orig_r_n,
        "crossfit_r_n": crossfit_r_n,
        "crossfit_beta_even_half": beta_a,
        "crossfit_beta_odd_half": beta_b,
        "u_stat_r_n_raw": r_u_raw,
        "u_stat_r_n_corrected": r_u_corrected,
        "mean_x_hat": mean_x,
        "mean_x_hat_squared": mean_x**2,
    }


def synthetic_sanity_check_u_statistic() -> dict:
    """Sanity check the U-statistic formula on synthetic (X,Z) pairs from a KNOWN joint
    Gaussian, BEFORE trusting it on real data -- per this task's own explicit requirement.

    Two scenarios, both with Var(Z) known exactly (matching how Var(Z)=m/4 is known exactly on
    real data, not estimated):
      A) mean_X = 0.0   -- R_U_hat (raw) should recover true R_n cleanly (no bias term).
      B) mean_X = 0.6   -- R_U_hat (raw) should be biased HIGH by approximately mean_X^2=0.36;
                            the mean-corrected version should recover true R_n much more closely.

    For each scenario: generate many independent synthetic datasets (matching a realistic reps
    count), compute R_U_hat (raw and corrected) plus the cross-fit estimator on each, average
    across datasets to approximate E[estimator], and compare to the analytically known true R_n.
    """
    true_beta = 1.3
    true_r_n = 0.05  # residual variance after removing the linear-in-Z part, WITH intercept
    var_z = 4.0  # arbitrary known exact Var(Z), analogous to m/4 on real data
    reps = 300
    n_synthetic_datasets = 800

    def run_scenario(mean_x: float) -> dict:
        raw_vals = []
        corrected_vals = []
        crossfit_vals = []
        for d in range(n_synthetic_datasets):
            local_rng = np.random.default_rng(SYNTHETIC_SANITY_SEED + 17 * d + int(mean_x * 1000))
            z = local_rng.normal(0.0, np.sqrt(var_z), size=reps)
            noise = local_rng.normal(0.0, np.sqrt(true_r_n), size=reps)
            x = mean_x + true_beta * z + noise

            y = x * z
            N = len(x)
            sum_y = float(np.sum(y))
            sum_y2 = float(np.sum(y**2))
            u_term = (sum_y**2 - sum_y2) / (N * (N - 1))
            # The real-data formula's (4/m) factor is specific to Var(Z)=m/4 (so (4/m) =
            # 1/Var(Z) there); the general form used here is 1/Var(Z), algebraically identical
            # to (4/m) exactly when Var(Z)=m/4 -- verified: 1/(m/4) = 4/m.
            r_raw = float(np.mean(x**2)) - u_term / var_z
            mean_x_hat = float(np.mean(x))
            r_corrected = r_raw - mean_x_hat**2
            raw_vals.append(r_raw)
            corrected_vals.append(r_corrected)

            idx_even = np.arange(N) % 2 == 0
            idx_odd = ~idx_even
            beta_a = float(np.cov(x[idx_even], z[idx_even], ddof=1)[0, 1]) / var_z
            resid_b = float(np.mean((x[idx_odd] - beta_a * z[idx_odd]) ** 2))
            beta_b = float(np.cov(x[idx_odd], z[idx_odd], ddof=1)[0, 1]) / var_z
            resid_a = float(np.mean((x[idx_even] - beta_b * z[idx_even]) ** 2))
            crossfit_vals.append(0.5 * (resid_a + resid_b))

        raw_vals = np.array(raw_vals)
        corrected_vals = np.array(corrected_vals)
        crossfit_vals = np.array(crossfit_vals)
        return {
            "mean_x": mean_x,
            "true_r_n": true_r_n,
            "mean_x_squared": mean_x**2,
            "predicted_raw_target": true_r_n + mean_x**2,
            "empirical_mean_raw": float(raw_vals.mean()),
            "empirical_se_raw": float(raw_vals.std(ddof=1) / np.sqrt(len(raw_vals))),
            "empirical_mean_corrected": float(corrected_vals.mean()),
            "empirical_se_corrected": float(
                corrected_vals.std(ddof=1) / np.sqrt(len(corrected_vals))
            ),
            "empirical_mean_crossfit": float(crossfit_vals.mean()),
            "empirical_se_crossfit": float(crossfit_vals.std(ddof=1) / np.sqrt(len(crossfit_vals))),
            "raw_matches_true_r_n": bool(
                abs(raw_vals.mean() - true_r_n) < 3 * raw_vals.std(ddof=1) / np.sqrt(len(raw_vals))
            ),
            "raw_matches_predicted_biased_target": bool(
                abs(raw_vals.mean() - (true_r_n + mean_x**2))
                < 3 * raw_vals.std(ddof=1) / np.sqrt(len(raw_vals))
            ),
            "corrected_matches_true_r_n": bool(
                abs(corrected_vals.mean() - true_r_n)
                < 3 * corrected_vals.std(ddof=1) / np.sqrt(len(corrected_vals))
            ),
            "crossfit_matches_true_r_n": bool(
                abs(crossfit_vals.mean() - true_r_n)
                < 3 * crossfit_vals.std(ddof=1) / np.sqrt(len(crossfit_vals))
            ),
        }

    scenario_a = run_scenario(mean_x=0.0)
    scenario_b = run_scenario(mean_x=0.6)

    return {
        "true_beta": true_beta,
        "true_r_n": true_r_n,
        "var_z_known_exact": var_z,
        "reps_per_synthetic_dataset": reps,
        "n_synthetic_datasets": n_synthetic_datasets,
        "scenario_mean_x_zero": scenario_a,
        "scenario_mean_x_nonzero": scenario_b,
        "conclusion": (
            "R_U_hat as literally specified (raw) is unbiased for E[(X-beta*Z)^2], which equals "
            "the true R_n only when E[X]=0 (scenario A, confirmed). When E[X]!=0 (scenario B), "
            "raw is biased HIGH by ~mean_x^2, matching the algebraic prediction "
            "true_r_n+mean_x^2; the mean-corrected version and the cross-fit estimator both "
            "recover true_r_n much more closely."
        ),
    }


def paired_bootstrap(
    x: np.ndarray, q: np.ndarray, delta: np.ndarray, n: int, n_boot: int, seed: int
) -> dict:
    """Resample the FULL replicate rows (X,Q,delta) JOINTLY -- N_BOOTSTRAP replicates, 95%
    percentile CI on lambda_n, kappa_n, n*U_n, U_n/Var_X (the four tracked series), plus the
    three R_n-addendum estimators (cross-fit uses an even/odd split of RESAMPLED positions,
    since the original index parity isn't meaningful after resampling with replacement)."""
    m = (n - 1) // 2
    rng = np.random.default_rng(seed)
    reps = len(x)
    var_z_exact = m / 4.0

    boot_lambda = np.empty(n_boot)
    boot_kappa = np.empty(n_boot)
    boot_n_u = np.empty(n_boot)
    boot_u_over_var = np.empty(n_boot)
    boot_orig_rn = np.empty(n_boot)
    boot_crossfit_rn = np.empty(n_boot)
    boot_ustat_raw_rn = np.empty(n_boot)
    boot_ustat_corrected_rn = np.empty(n_boot)

    idx_pos_even = np.arange(reps) % 2 == 0
    idx_pos_odd = ~idx_pos_even

    for b in range(n_boot):
        idx = rng.integers(0, reps, size=reps)
        xb, qb, db = x[idx], q[idx], delta[idx]
        zb = qb - m / 2.0

        cov_b = float(np.cov(xb, qb, ddof=1)[0, 1])
        lambda_b = 4.0 * cov_b
        w1_b = lambda_b**2 / (4.0 * m)
        b_b = (m / 4.0) * float(np.mean(db**2))
        kappa_b = b_b / w1_b if w1_b != 0 else float("nan")
        var_x_b = float(np.var(xb, ddof=1))
        u_b = (b_b + 2.0 * w1_b) / 3.0

        boot_lambda[b] = lambda_b
        boot_kappa[b] = kappa_b
        boot_n_u[b] = n * u_b
        boot_u_over_var[b] = u_b / var_x_b if var_x_b != 0 else float("nan")

        boot_orig_rn[b] = var_x_b - w1_b

        beta_e = float(np.cov(xb[idx_pos_even], zb[idx_pos_even], ddof=1)[0, 1]) / var_z_exact
        resid_o = float(np.mean((xb[idx_pos_odd] - beta_e * zb[idx_pos_odd]) ** 2))
        beta_o = float(np.cov(xb[idx_pos_odd], zb[idx_pos_odd], ddof=1)[0, 1]) / var_z_exact
        resid_e = float(np.mean((xb[idx_pos_even] - beta_o * zb[idx_pos_even]) ** 2))
        boot_crossfit_rn[b] = 0.5 * (resid_o + resid_e)

        yb = xb * zb
        sum_y = float(np.sum(yb))
        sum_y2 = float(np.sum(yb**2))
        u_term = (sum_y**2 - sum_y2) / (reps * (reps - 1))
        r_raw_b = float(np.mean(xb**2)) - (4.0 / m) * u_term
        boot_ustat_raw_rn[b] = r_raw_b
        boot_ustat_corrected_rn[b] = r_raw_b - float(np.mean(xb)) ** 2

    def ci(arr):
        lo, hi = np.percentile(arr, [2.5, 97.5])
        return [float(lo), float(hi)]

    return {
        "lambda_n_ci95": ci(boot_lambda),
        "kappa_n_ci95": ci(boot_kappa),
        "n_times_u_n_ci95": ci(boot_n_u),
        "u_n_over_var_x_ci95": ci(boot_u_over_var),
        "orig_r_n_ci95": ci(boot_orig_rn),
        "crossfit_r_n_ci95": ci(boot_crossfit_rn),
        "ustat_raw_r_n_ci95": ci(boot_ustat_raw_rn),
        "ustat_corrected_r_n_ci95": ci(boot_ustat_corrected_rn),
    }


def run_positive_control() -> dict:
    t0 = time.time()
    x, q, delta = sample_x_q_delta(
        POSITIVE_CONTROL_N, POSITIVE_CONTROL_REPS, POSITIVE_CONTROL_SEED_BASE
    )
    elapsed = time.time() - t0
    decomp = compute_kappa_decomposition(x, q, delta, POSITIVE_CONTROL_N)
    addendum = r_n_addendum_point_estimates(x, q, POSITIVE_CONTROL_N)
    ci = paired_bootstrap(
        x, q, delta, POSITIVE_CONTROL_N, N_BOOTSTRAP, BOOTSTRAP_SEED + POSITIVE_CONTROL_N
    )

    # n*W1 CI: deriving from lambda_n_ci95 via w1 = lambda^2/(4m) is not monotone-safe on a CI
    # (squaring), so bootstrap n*W1 directly instead of reusing lambda's CI.
    m = (POSITIVE_CONTROL_N - 1) // 2
    rng = np.random.default_rng(BOOTSTRAP_SEED + POSITIVE_CONTROL_N + 7)
    reps = len(x)
    boot_n_w1 = np.empty(N_BOOTSTRAP)
    for b in range(N_BOOTSTRAP):
        idx = rng.integers(0, reps, size=reps)
        cov_b = float(np.cov(x[idx], q[idx], ddof=1)[0, 1])
        lambda_b = 4.0 * cov_b
        w1_b = lambda_b**2 / (4.0 * m)
        boot_n_w1[b] = POSITIVE_CONTROL_N * w1_b
    n_w1_lo, n_w1_hi = np.percentile(boot_n_w1, [2.5, 97.5])
    n_w1_ci = [float(n_w1_lo), float(n_w1_hi)]

    boot_n_var_x = np.empty(N_BOOTSTRAP)
    rng2 = np.random.default_rng(BOOTSTRAP_SEED + POSITIVE_CONTROL_N + 11)
    for b in range(N_BOOTSTRAP):
        idx = rng2.integers(0, reps, size=reps)
        boot_n_var_x[b] = POSITIVE_CONTROL_N * float(np.var(x[idx], ddof=1))
    n_var_x_lo, n_var_x_hi = np.percentile(boot_n_var_x, [2.5, 97.5])
    n_var_x_ci = [float(n_var_x_lo), float(n_var_x_hi)]

    kappa_lo, kappa_hi = ci["kappa_n_ci95"]

    gate = {
        "n_times_w1": {
            "estimate": POSITIVE_CONTROL_N * decomp["w1_hat"],
            "ci95": n_w1_ci,
            "exact_reference": POSITIVE_CONTROL_EXACT["n_times_w1"],
            "ci_contains_exact": bool(
                n_w1_ci[0] <= POSITIVE_CONTROL_EXACT["n_times_w1"] <= n_w1_ci[1]
            ),
        },
        "kappa_n": {
            "estimate": decomp["kappa_hat"],
            "ci95": [kappa_lo, kappa_hi],
            "exact_reference": POSITIVE_CONTROL_EXACT["kappa_n"],
            "ci_contains_exact": bool(kappa_lo <= POSITIVE_CONTROL_EXACT["kappa_n"] <= kappa_hi),
        },
        "n_times_var_x": {
            "estimate": POSITIVE_CONTROL_N * decomp["var_x_hat"],
            "ci95": n_var_x_ci,
            "exact_reference": POSITIVE_CONTROL_EXACT["n_times_var_x"],
            "ci_contains_exact": bool(
                n_var_x_ci[0] <= POSITIVE_CONTROL_EXACT["n_times_var_x"] <= n_var_x_ci[1]
            ),
        },
    }
    gate["all_three_pass"] = bool(
        gate["n_times_w1"]["ci_contains_exact"]
        and gate["kappa_n"]["ci_contains_exact"]
        and gate["n_times_var_x"]["ci_contains_exact"]
    )

    result = {
        "n": POSITIVE_CONTROL_N,
        "reps": POSITIVE_CONTROL_REPS,
        "elapsed_seconds": elapsed,
        "decomposition": decomp,
        "r_n_addendum": addendum,
        "exact_n_times_r_n_reference": EXACT_N_TIMES_R_N_AT_37,
        "r_n_addendum_ci": {
            "orig_r_n_ci95": ci["orig_r_n_ci95"],
            "crossfit_r_n_ci95": ci["crossfit_r_n_ci95"],
            "ustat_raw_r_n_ci95": ci["ustat_raw_r_n_ci95"],
            "ustat_corrected_r_n_ci95": ci["ustat_corrected_r_n_ci95"],
        },
        "bootstrap_ci": ci,
        "oracle_adequacy_gate_3way": gate,
        "source": POSITIVE_CONTROL_EXACT_SOURCE,
    }
    print(
        f"[positive control] n={POSITIVE_CONTROL_N} reps={POSITIVE_CONTROL_REPS} "
        f"n*W1_hat={gate['n_times_w1']['estimate']:.4f} CI={n_w1_ci} "
        f"kappa_hat={decomp['kappa_hat']:.4f} CI=[{kappa_lo:.4f},{kappa_hi:.4f}] "
        f"n*VarX_hat={gate['n_times_var_x']['estimate']:.4f} CI={n_var_x_ci} "
        f"3-way-gate-pass={gate['all_three_pass']} elapsed={elapsed:.1f}s",
        flush=True,
    )
    return result


def run_sweep() -> tuple[list[dict], list[str]]:
    rows = []
    incomplete_ns = []
    for n, reps in SWEEP_N_REPS:
        t0 = time.time()
        x, q, delta = sample_x_q_delta(n, reps, RNG_SEED_BASE)
        elapsed = time.time() - t0

        if elapsed > MAX_SECONDS_PER_N:
            incomplete_ns.append(n)
            print(
                f"n={n:5d} reps={reps:4d} STOP-CONDITION-TRIGGERED elapsed={elapsed:.1f}s "
                f"(exceeded MAX_SECONDS_PER_N={MAX_SECONDS_PER_N}s) -- reporting result for this "
                f"n, flagged incomplete/over-budget",
                flush=True,
            )

        decomp = compute_kappa_decomposition(x, q, delta, n)
        addendum = r_n_addendum_point_estimates(x, q, n)
        ci = paired_bootstrap(x, q, delta, n, N_BOOTSTRAP, BOOTSTRAP_SEED + n)

        n_times_w1_hat = n * decomp["w1_hat"]
        # n*W1 CI via direct bootstrap (squaring in w1 makes reusing lambda's CI unsafe)
        m = (n - 1) // 2
        rng = np.random.default_rng(BOOTSTRAP_SEED + n + 7)
        boot_n_w1 = np.empty(N_BOOTSTRAP)
        for b in range(N_BOOTSTRAP):
            idx = rng.integers(0, reps, size=reps)
            cov_b = float(np.cov(x[idx], q[idx], ddof=1)[0, 1])
            lambda_b = 4.0 * cov_b
            boot_n_w1[b] = n * (lambda_b**2 / (4.0 * m))
        n_w1_lo, n_w1_hi = np.percentile(boot_n_w1, [2.5, 97.5])

        row = {
            "n": n,
            "n_reps": reps,
            "elapsed_seconds": elapsed,
            **decomp,
            "n_times_w1_hat": n_times_w1_hat,
            "n_times_w1_ci95": [float(n_w1_lo), float(n_w1_hi)],
            "r_n_addendum": addendum,
            "bootstrap_ci": ci,
            "flagged_incomplete_slow": n in incomplete_ns,
        }
        rows.append(row)
        lam_lo, lam_hi = ci["lambda_n_ci95"]
        kap_lo, kap_hi = ci["kappa_n_ci95"]
        u_lo, u_hi = ci["n_times_u_n_ci95"]
        uv_lo, uv_hi = ci["u_n_over_var_x_ci95"]
        print(
            f"n={n:5d} reps={reps:4d} lambda_n={decomp['lambda_n_hat']:.4f} "
            f"CI=[{lam_lo:.4f},{lam_hi:.4f}] | kappa_n={decomp['kappa_hat']:.4f} "
            f"CI=[{kap_lo:.4f},{kap_hi:.4f}] | n*U_n={decomp['n_times_u_hat']:.4f} "
            f"CI=[{u_lo:.4f},{u_hi:.4f}] | U_n/VarX={decomp['u_hat_over_var_x']:.4f} "
            f"CI=[{uv_lo:.4f},{uv_hi:.4f}] elapsed={elapsed:.1f}s",
            flush=True,
        )

        np.savez(
            METRICS / f"kappa_n_raw_samples_n{n}.npz",
            X=x,
            Q=q,
            delta_i_signed=delta,
        )
    return rows, incomplete_ns


def honest_power_law_fit(ns: np.ndarray, vals: np.ndarray, ses: np.ndarray | None = None) -> dict:
    """OLS slope + SE on log|val| vs log(n) -- same diligence Point 53's own review applied
    (do not just eyeball CI overlap; compute a real slope with a standard error)."""
    log_n = np.log(ns)
    log_val = np.log(np.abs(vals))
    slope, intercept = np.polyfit(log_n, log_val, 1)
    n_pts = len(ns)
    pred = slope * log_n + intercept
    resid = log_val - pred
    dof = n_pts - 2
    if dof > 0:
        sigma2 = float(np.sum(resid**2) / dof)
        x_mean = float(np.mean(log_n))
        sxx = float(np.sum((log_n - x_mean) ** 2))
        se_slope = float(np.sqrt(sigma2 / sxx))
        t_crit = float(stats.t.ppf(0.975, dof))
        ci = [float(slope - t_crit * se_slope), float(slope + t_crit * se_slope)]
    else:
        se_slope = float("nan")
        ci = [float("nan"), float("nan")]
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "slope_se": se_slope,
        "slope_ci95": ci,
        "dof": dof,
    }


def run() -> dict:
    _load_dependencies()
    substrate = substrate_gate_checks()
    primes = verify_primes()

    if not substrate["substrate_ready"] or not primes["all_prime"]:
        out = {
            "status": "BLOCKED-INFRASTRUCTURE",
            "substrate_gate": substrate,
            "prime_verification": primes,
        }
        METRICS.mkdir(exist_ok=True)
        with open(METRICS / "kappa_n_large_n.json", "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, default=str)
        print(json.dumps(out, indent=2, default=str))
        return out

    pilot = pilot_sign_check()
    if not pilot["sign_check_passed"]:
        out = {
            "status": "BLOCKED-SIGN-CONVENTION-BUG",
            "substrate_gate": substrate,
            "prime_verification": primes,
            "pilot_sign_check": pilot,
        }
        METRICS.mkdir(exist_ok=True)
        with open(METRICS / "kappa_n_large_n.json", "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, default=str)
        print(json.dumps(out, indent=2, default=str))
        return out
    print(f"[pilot sign check] PASSED: {pilot}", flush=True)

    synthetic_sanity = synthetic_sanity_check_u_statistic()
    print(
        f"[synthetic sanity check] scenario A (mean_x=0): "
        f"raw={synthetic_sanity['scenario_mean_x_zero']['empirical_mean_raw']:.4f} "
        f"(true={synthetic_sanity['true_r_n']}) matches="
        f"{synthetic_sanity['scenario_mean_x_zero']['raw_matches_true_r_n']} | "
        f"scenario B (mean_x=0.6): raw="
        f"{synthetic_sanity['scenario_mean_x_nonzero']['empirical_mean_raw']:.4f} "
        f"predicted_biased="
        f"{synthetic_sanity['scenario_mean_x_nonzero']['predicted_raw_target']:.4f} "
        f"corrected={synthetic_sanity['scenario_mean_x_nonzero']['empirical_mean_corrected']:.4f}",
        flush=True,
    )

    METRICS.mkdir(exist_ok=True)

    total_t0 = time.time()
    positive_control = run_positive_control()
    sweep_rows, incomplete_ns = run_sweep()
    total_elapsed = time.time() - total_t0

    ns = np.array([r["n"] for r in sweep_rows], dtype=float)
    lambda_vals = np.array([r["lambda_n_hat"] for r in sweep_rows], dtype=float)
    kappa_vals = np.array([r["kappa_hat"] for r in sweep_rows], dtype=float)
    lambda_fit = honest_power_law_fit(ns, lambda_vals)
    kappa_fit = honest_power_law_fit(ns, kappa_vals)

    out = {
        "claim": (
            "H-CAT31-3 kappa_n/lambda_n cleaner replacement route for the R_n diagnostic, "
            "large-n Monte Carlo (n=127..2039)"
        ),
        "substrate_gate": substrate,
        "prime_verification": primes,
        "pilot_sign_check": pilot,
        "synthetic_sanity_check_u_statistic": synthetic_sanity,
        "positive_control_n37": positive_control,
        "sweep": sweep_rows,
        "incomplete_ns": incomplete_ns,
        "lambda_n_power_law_fit_vs_n": lambda_fit,
        "kappa_n_power_law_fit_vs_n": kappa_fit,
        "total_elapsed_seconds": total_elapsed,
    }
    with open(METRICS / "kappa_n_large_n.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    run()
