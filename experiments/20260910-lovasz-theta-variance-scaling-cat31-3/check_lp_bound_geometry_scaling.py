"""Point 45b: does the near-exactness found in point 44 (R_6~1) persist as L grows well beyond
the fixed moment order s=6, or is it specific to the small L<=11 range this experiment's actual
n=23..47 happens to cover? Pure grid geometry -- NO theta-solves needed at all, since this only
needs the gamma_l formula (already canonical) and synthetic spectra, extended to large synthetic
N far beyond what real theta computation could ever reach (N=20,50,100,200,500,1000).

Motivated directly by point 45's own negative-control finding: random and adversarial synthetic
spectra on the L<=11 grids already used in this experiment give R_6 close to 1, just like the
real data -- meaning point 44's near-exactness is mostly a property of L being small relative to
s=6, not something special about Lovasz theta. The open question this leaves: does this
near-exactness persist, degrade slowly, or degrade fast as L/s grows large (L>>6), which is the
actual asymptotic regime relevant to n->infinity (L=min(q,N-q)=Theta(n) grows without bound
while s stays fixed at 6 unless higher moments are computed)?
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

lp_spec = importlib.util.spec_from_file_location(
    "lp_mod_geom", HERE / "check_truncated_moment_lp_bound.py"
)
lpmod = importlib.util.module_from_spec(lp_spec)
lp_spec.loader.exec_module(lpmod)


def worst_case_r6(gammas: np.ndarray, rng: np.random.Generator, n_random: int = 50) -> dict:
    """Approximate the WORST-CASE R_6 over several synthetic families (adversarial search is
    itself an LP-adjacent question; here we just sample broadly and report the max found, which
    is a lower bound on the true worst case, not the true worst case itself -- stated as such)."""
    L = len(gammas)
    worst = 0.0
    worst_family = None

    # deterministic adversarial-flavored families
    ls = np.arange(1, L + 1)
    two_point_low_high = np.zeros(L)
    two_point_low_high[0] = 0.5
    two_point_low_high[-1] = 0.5
    candidates = {
        "pure_low": np.eye(L)[0],
        "pure_high": np.eye(L)[-1],
        "pure_mid": np.eye(L)[L // 2],
        "two_point_low_high": two_point_low_high,
        "decaying": 1.0 / ls,
        "growing": ls.astype(float),
    }
    for name, E in candidates.items():
        C_q = float(np.sum(E))
        moments = [float(np.sum(gammas**r * E)) for r in range(1, 7)]
        res = lpmod.solve_moment_lp(gammas, moments, maximize=True)
        if res["success"]:
            r6 = res["value"] / C_q
            if r6 > worst:
                worst, worst_family = r6, name

    for _ in range(n_random):
        E = rng.exponential(1.0, size=L)
        C_q = float(np.sum(E))
        moments = [float(np.sum(gammas**r * E)) for r in range(1, 7)]
        res = lpmod.solve_moment_lp(gammas, moments, maximize=True)
        if res["success"]:
            r6 = res["value"] / C_q
            if r6 > worst:
                worst, worst_family = r6, "random_exp_sample"

    return {"worst_R6_found": worst, "worst_family": worst_family}


def run(N_values: list[int], seed: int = 7) -> list[dict]:
    rng = np.random.default_rng(seed)
    results = []
    for N in N_values:
        q = N // 2
        gammas = lpmod.gamma_l_array(N, q)
        L = len(gammas)
        stats = worst_case_r6(gammas, rng)
        row = {"N": N, "q": q, "L": L, **stats}
        results.append(row)
        print(
            f"N={N:5d} q={q:5d} L={L:5d}  worst_R6_found={stats['worst_R6_found']:.4f} "
            f"(family={stats['worst_family']})",
            flush=True,
        )

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "lp_bound_geometry_scaling.json", "w", encoding="utf-8") as f:
        json.dump({"rows": results, "seed": seed}, f, indent=2)
    return results


if __name__ == "__main__":
    run([11, 20, 50, 100, 200, 500, 1000])
    print("\nDone.", flush=True)
