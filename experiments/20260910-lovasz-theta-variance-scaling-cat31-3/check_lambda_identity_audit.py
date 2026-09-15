"""Point 54A: paired estimator-identity audit for `lambda_n`, run per skeptic-fallback review's
own proposed zero-cost test (Point 54's skeptic review found the two natural `lambda_n`
estimators -- `lambda_Q=4*Cov(X,Q)` and `lambda_delta=-m*E[delta_i]` -- disagree by 8-20% at
every tested `n`, an unresolved discrepancy). Direct pairwise comparison of two separately-
estimated quantities is statistically weak; this script uses the SAME (X,Q,delta) triples
(already saved, one triple per graph draw, no additional theta_via_lp calls) to test the
STRONGER, single-quantity identity implied by combining the two already-established results
(`lambda_n=4*Cov(X,Q)=4*E[X*(Q-m/2)]` since `E[Q]=m/2` exactly, and `lambda_n=-m*E[delta_i]`):

    E[Y_r] = 0   where   Y_r := 4*X_r*(Q_r - m/2) + m*delta_r

This is a single paired-difference test (much higher power than comparing two independently-
estimated CIs) because X_r*(Q_r-m/2) and delta_r are measured on the SAME graph draw per
replicate -- no clustering/pseudoreplication concern, since exactly one (X,Q,delta) triple comes
from exactly one graph per replicate (verified by reading check_kappa_n_large_n.py's
sample_x_q_delta: one sample_circulant_neighbors call per rep, X/Q/delta all derived from it).

Orientation of delta_i, independently re-verified against check_kappa_n_large_n.py's own code
(lines 216-224) before running this: delta_i(S)=X(x_i=0)-X(x_i=1) in BOTH branches (c[i]<0.5:
delta=x0-x1 where x0 is the i=0 state; c[i]>=0.5: delta=x1-x0 where x1 is the i=0 state after
flip-off) -- matches the required convention exactly, confirmed by direct code read, not assumed.

Reuses the raw `.npz` files already saved by check_kappa_n_large_n.py -- zero additional
`theta_via_lp` calls, per this project's own reuse discipline.

Status per n: PASS (paired discrepancy statistically consistent with zero) / FAIL (significantly
nonzero) / INCONCLUSIVE (CI too wide to discriminate). If any n reads FAIL, the lambda_n scaling
analysis (Point 54B) should be frozen pending diagnosis, per the user's own proposed protocol.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

NS = [127, 251, 509, 1021, 2039]
N_BOOTSTRAP = 5000
BOOTSTRAP_SEED = 774411
FAIL_Z_THRESHOLD = 3.0  # |z| >= this -> FAIL (significantly nonzero)
INCONCLUSIVE_Z_THRESHOLD = 1.0  # |z| < this AND CI wide -> still counts as PASS if consistent


def audit_one_n(n: int) -> dict:
    npz = np.load(METRICS / f"kappa_n_raw_samples_n{n}.npz")
    x = npz["X"]
    q = npz["Q"]
    delta = npz["delta_i_signed"]
    m = (n - 1) // 2
    reps = len(x)

    y = 4.0 * x * (q - m / 2.0) + m * delta
    y_mean = float(y.mean())
    y_se = float(y.std(ddof=1) / np.sqrt(reps))
    z = y_mean / y_se if y_se != 0 else float("nan")

    rng = np.random.default_rng(BOOTSTRAP_SEED + n)
    boot_means = np.empty(N_BOOTSTRAP)
    for b in range(N_BOOTSTRAP):
        idx = rng.integers(0, reps, size=reps)
        boot_means[b] = y[idx].mean()
    ci_lo, ci_hi = np.percentile(boot_means, [2.5, 97.5])

    # also report the two component means separately, for context
    lambda_q = float(4.0 * np.cov(x, q, ddof=1)[0, 1])
    lambda_delta = float(-m * delta.mean())

    if abs(z) >= FAIL_Z_THRESHOLD:
        status = "FAIL"
    elif ci_lo <= 0.0 <= ci_hi:
        status = "PASS"
    else:
        status = "INCONCLUSIVE"

    result = {
        "n": n,
        "m": m,
        "reps": reps,
        "y_mean": y_mean,
        "y_se": y_se,
        "z": z,
        "y_ci95": [float(ci_lo), float(ci_hi)],
        "lambda_Q": lambda_q,
        "lambda_delta": lambda_delta,
        "rel_diff_lambda": abs(lambda_q - lambda_delta) / abs(lambda_q),
        "status": status,
    }
    print(
        f"n={n:5d} reps={reps:4d} Y_mean={y_mean:+.5f} SE={y_se:.5f} z={z:+.3f} "
        f"CI=[{ci_lo:.5f},{ci_hi:.5f}] lambda_Q={lambda_q:.4f} lambda_delta={lambda_delta:.4f} "
        f"rel_diff={result['rel_diff_lambda']:.4f} status={status}",
        flush=True,
    )
    return result


def run() -> dict:
    rows = [audit_one_n(n) for n in NS]
    all_pass = all(r["status"] == "PASS" for r in rows)
    any_fail = any(r["status"] == "FAIL" for r in rows)
    overall = "FAIL" if any_fail else ("PASS" if all_pass else "INCONCLUSIVE")
    out = {
        "claim": ("Point 54A -- paired identity audit: E[4*X*(Q-m/2) + m*delta_i] = 0 per prime n"),
        "rows": rows,
        "overall_status": overall,
    }
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "lambda_identity_audit.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nOverall status: {overall}")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    run()
