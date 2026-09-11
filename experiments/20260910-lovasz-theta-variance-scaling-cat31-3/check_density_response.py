"""Density-response diagnostic: independent cross-check of the "susceptibility" lambda_n
from an external AI analysis (NOT trusted at face value -- the exact symmetry claim below is
independently re-derived here, and the estimator itself is a new, direct measurement, not a
regression proxy like the Q-diagnostic).

Exact symmetry, re-derived (extends the p=0.5 self-complementary argument already used in
this experiment's own substrate gate and in decision.md's cosh-bound section): for a random
circulant graph G ~ G(n,p), theta(G)*theta(Gbar)=n holds PATHWISE (Lovasz 1979, exact for any
vertex-transitive graph). Gbar, as a random graph over the randomness of G~G(n,p), has exactly
the distribution G(n,1-p) (each edge indicator flips independently). Therefore
theta(G(n,1-p)) =d= n/theta(G(n,p)), so with X_n(p) := log(theta(G(n,p))/sqrt(n)):

    X_n(1-p) =d= -X_n(p)   =>   M_n(1-p) = -M_n(p)   where M_n(p) := E[X_n(p)]

i.e. M_n is an EXACTLY odd function of h = p-0.5. This licenses fitting only odd terms
(lambda*h + mu*h^3 + ...) and gives a direct, checkable symmetry to test on the data itself
(M_n(0.5+h) should equal -M_n(0.5-h) up to sampling noise, independent of any model fit).

lambda_n = M_n'(0.5) is estimated two ways per h: (a) symmetric finite difference
(M_n(0.5+h)-M_n(0.5-h))/(2h), which is exact for the linear term and picks up an O(h^2) bias
from the cubic term; (b) compared across two h values to check consistency (Richardson-style
sanity check, not a full extrapolation).

Independent cross-check target: check_q_proxy_diagnostic.py's regression-based estimate
lambda_n ~= sqrt(2*n*explained_variance) -- see decision.md Addendum point on lambda_n~=3.16
at n=1536. This script provides a DIFFERENT kind of measurement (direct response to a
parameter shift, not a within-sample regression), so agreement is a real consistency check,
not circular.

Reuses sample_circulant_neighbors/theta_via_lp from H-CAT31-1 UNCHANGED.
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
METRICS = HERE / "metrics"

RNG_SEED_BASE = 335000  # distinct from 31000/331000/332000/333000/334000 used elsewhere


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h_cat31_1 = _load_module("h_cat31_3_density_response_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = h_cat31_1.sample_circulant_neighbors
theta_via_lp = h_cat31_1.theta_via_lp

H_VALUES = [0.025, 0.05]  # deviations from p=0.5 to test, both signs
N_REPS = [(128, 300), (512, 200)]


def run_one_n(n: int, reps: int) -> dict:
    half = (n - 1) // 2
    p_values = sorted({0.5 + s * h for h in H_VALUES for s in (-1, 1)} | {0.5})
    means: dict[float, float] = {}
    ses: dict[float, float] = {}
    t0 = time.time()
    for p in p_values:
        xs = np.empty(reps)
        for i in range(reps):
            seed = RNG_SEED_BASE + n * 100000 + round(p * 1000) * 100 + i
            c = sample_circulant_neighbors(n, p, seed)
            theta = theta_via_lp(c)
            xs[i] = np.log(theta / np.sqrt(n))
        means[p] = float(xs.mean())
        ses[p] = float(xs.std(ddof=1) / np.sqrt(reps))
    elapsed = time.time() - t0

    # Exact-symmetry check: M_n(0.5+h) should equal -M_n(0.5-h).
    symmetry_check = []
    for h in H_VALUES:
        m_plus = means[round(0.5 + h, 10)]
        m_minus = means[round(0.5 - h, 10)]
        symmetry_check.append(
            {
                "h": h,
                "M(0.5+h)": m_plus,
                "-M(0.5-h)": -m_minus,
                "diff": m_plus - (-m_minus),
                "se_plus": ses[round(0.5 + h, 10)],
                "se_minus": ses[round(0.5 - h, 10)],
            }
        )

    # Finite-difference lambda_n estimate per h.
    lambda_estimates = []
    for h in H_VALUES:
        m_plus = means[round(0.5 + h, 10)]
        m_minus = means[round(0.5 - h, 10)]
        lam = (m_plus - m_minus) / (2 * h)
        se_lam = np.sqrt(ses[round(0.5 + h, 10)] ** 2 + ses[round(0.5 - h, 10)] ** 2) / (2 * h)
        lambda_estimates.append({"h": h, "lambda_hat": float(lam), "se": float(se_lam)})

    result = {
        "n": n,
        "half_m": half,
        "reps": reps,
        "p_values": p_values,
        "means": means,
        "ses": ses,
        "symmetry_check": symmetry_check,
        "lambda_estimates": lambda_estimates,
        "elapsed_seconds": elapsed,
    }
    print(
        f"n={n:5d} reps={reps:4d} M(0.5)={means[0.5]:+.5f}+-{ses[0.5]:.5f} "
        f"lambda(h=0.025)={lambda_estimates[0]['lambda_hat']:.4f}+-{lambda_estimates[0]['se']:.4f} "
        f"lambda(h=0.05)={lambda_estimates[1]['lambda_hat']:.4f}+-{lambda_estimates[1]['se']:.4f} "
        f"elapsed={elapsed:.1f}s",
        flush=True,
    )
    for sc in symmetry_check:
        print(
            f"    symmetry h={sc['h']}: M(0.5+h)={sc['M(0.5+h)']:+.5f} "
            f"-M(0.5-h)={sc['-M(0.5-h)']:+.5f} diff={sc['diff']:.5f}",
            flush=True,
        )
    return result


def run() -> dict:
    rows = [run_one_n(n, reps) for n, reps in N_REPS]
    return {"rows": rows}


if __name__ == "__main__":
    out = run()
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "density_response.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
