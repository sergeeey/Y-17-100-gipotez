"""Exact Cauchy-Schwarz lower bound on Var(X_n), independently re-derived and applied to
ALREADY-COLLECTED, verified data (check_density_response.py's own lambda_hat estimates) --
NOT to any externally-supplied "new experiment" numbers, which are not verifiable and not
used here (see decision.md's explicit discussion of why).

Derivation (verified step by step, not copied from the pasted external text):

For X_n = f(z_1,...,z_m), z_i iid Bernoulli(p), Q = sum z_i, the score-function identity for
an exponential family gives

    d/dp E_p[X_n] = Cov_p(X_n, Q) / (p(1-p))

(standard: log P_p(z) = Q*log(p) + (m-Q)*log(1-p), so d/dp log P_p(z) = (Q-mp)/(p(1-p)), and
d/dp E_p[X_n] = E_p[X_n * d/dp log P_p(z)] = Cov_p(X_n,Q)/(p(1-p)) since E_p[Q]=mp).

At p=1/2: M_n'(1/2) = 4*Cov(X_n, Q).

By Cauchy-Schwarz, Cov(X_n,Q)^2 <= Var(X_n)*Var(Q), and Var(Q) = m/4 at p=1/2, so

    Var(X_n) >= Cov(X_n,Q)^2 / Var(Q) = (M_n'(1/2)/4)^2 / (m/4) = M_n'(1/2)^2 / (4m)
             ~= M_n'(1/2)^2 / (2n)   (m ~= n/2)

This is an EXACT (not heuristic/concave-tangent) lower bound, using only Cauchy-Schwarz --
no LP structure, no concentration assumption. It uses M_n'(1/2), which check_density_response.py
already measured directly (finite-difference lambda_hat), so no new expensive computation is
needed to apply it.
"""

from __future__ import annotations

import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

density_response = json.load(open(METRICS / "density_response.json", encoding="utf-8"))
main_sweep = json.load(open(METRICS / "run.json", encoding="utf-8"))

measured_var = {row["n"]: row["var_log_ratio"] for row in main_sweep["sweep"]}

print(
    f"{'n':>6} {'h':>7} {'lambda_hat':>12} {'m=(n-1)//2':>10} {'CS lower bound':>16} "
    f"{'measured V_n':>14} {'bound/measured':>14}"
)
rows = []
for row in density_response["rows"]:
    n = row["n"]
    m = (n - 1) // 2
    for est in row["lambda_estimates"]:
        h = est["h"]
        lam = est["lambda_hat"]
        lower_bound = lam**2 / (4 * m)
        v_n = measured_var[n]
        ratio = lower_bound / v_n
        rows.append(
            {
                "n": n,
                "h": h,
                "lambda_hat": lam,
                "m": m,
                "cs_lower_bound": lower_bound,
                "measured_V_n": v_n,
                "bound_over_measured": ratio,
            }
        )
        print(f"{n:6d} {h:7.3f} {lam:12.4f} {m:10d} {lower_bound:16.6f} {v_n:14.6f} {ratio:14.3f}")

with open(METRICS / "cauchy_schwarz_lower_bound.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)

print("\n--- gcd check for n=3000 sensitivity test indices (documented limitation) ---")
n3000_half = (3000 - 1) // 2
test_idx = sorted({1, max(1, n3000_half // 3), max(1, 2 * n3000_half // 3)})
for i in test_idx:
    print(f"  gcd({i}, 3000) = {gcd(i, 3000)}")
print(
    f"test_indices used: {test_idx} -- half_m={n3000_half} (antipodal bit n/2=1500 NOT included,\n"
    f"  matching sample_circulant_neighbors' own separate handling of even-n antipodal generator)"
)
