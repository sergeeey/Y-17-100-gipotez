"""Point 45: negative/positive control for point 44's headline finding (R_6=U_6/C_q approx 1).
Before treating "6 moments nearly determine C_q" as informative about Lovasz theta specifically,
check the obvious alternative: is this near-exactness just a generic property of ANY positive
spectrum on this same (N,q,gamma_l) grid -- i.e. an artifact of the LP/grid geometry, not a fact
about our actual f=delta_i?

Per artifact-provenance-gates.md's Gate 3 discipline (a test must be shown to discriminate
something, not just pass on the real case) and this project's own repeated "check before
celebrating" pattern: generate several families of SYNTHETIC nonnegative spectra E_l^synthetic
on the SAME grid used for each real n, compute their own M_1..M_6 from the SAME gamma_l, run
the SAME truncated-moment LP, and compare the resulting R_6^synthetic distribution against the
real R_6 already found in point 44. If most synthetic spectra also give R_6 close to 1, the
near-exactness is mostly generic grid geometry. If synthetic (especially adversarial-looking)
spectra give R_6 substantially >1 while the real spectrum sits near 1, that is genuine evidence
of "Lovasz-specific moment rigidity" -- a materially stronger claim than point 44 alone
supports.

No new theta-solves needed -- pure synthetic data + the already-verified LP machinery from
point 44 (check_truncated_moment_lp_bound.py), reused not reimplemented.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

lp_spec = importlib.util.spec_from_file_location(
    "lp_mod_synth", HERE / "check_truncated_moment_lp_bound.py"
)
lpmod = importlib.util.module_from_spec(lp_spec)
lp_spec.loader.exec_module(lpmod)


def synthetic_families(L: int, rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Each family returns a nonnegative L-vector E_l (unnormalized; C_q=sum is whatever it is,
    matching the real setup where C_q is not fixed in advance)."""
    families = {}

    families["uniform_random_exp"] = rng.exponential(1.0, size=L)
    families["uniform_flat"] = np.ones(L)

    pure_low = np.zeros(L)
    pure_low[0] = 1.0
    families["pure_low_level"] = pure_low

    pure_high = np.zeros(L)
    pure_high[-1] = 1.0
    families["pure_high_level"] = pure_high

    two_point = np.zeros(L)
    two_point[0] = 0.5
    two_point[-1] = 0.5
    families["two_point_mixture"] = two_point

    # broad, smoothly decaying from level 1 (mimics a "spectrum concentrated at low l" prior)
    ls = np.arange(1, L + 1)
    families["decaying_low_to_high"] = 1.0 / ls

    # broad, smoothly growing toward level L (mimics "spectrum concentrated at high l")
    families["growing_low_to_high"] = ls.astype(float)

    return families


def run_family_batch(
    gammas: np.ndarray, family_name: str, n_samples: int, rng: np.random.Generator
) -> list[float]:
    """For random families, draw n_samples independent spectra and return their R_6 values.
    For deterministic families, return a single-element list."""
    L = len(gammas)
    r6_values = []
    for _ in range(n_samples):
        if family_name == "uniform_random_exp":
            E = rng.exponential(1.0, size=L)
        else:
            E = synthetic_families(L, rng)[family_name]
        C_q_synth = float(np.sum(E))
        moments = [float(np.sum(gammas**r * E)) for r in range(1, 7)]
        res = lpmod.solve_moment_lp(gammas, moments, maximize=True)
        if res["success"]:
            r6_values.append(res["value"] / C_q_synth)
        if family_name != "uniform_random_exp":
            break
    return r6_values


def run_one_n(row: dict, n_random_samples: int, seed: int) -> dict:
    n, N, q = row["n"], row["N"], row["q"]
    C_q_real = row["C_q"]
    gammas = lpmod.gamma_l_array(N, q)
    L = len(gammas)
    rng = np.random.default_rng(seed)

    real_moments = [row[f"M{r}"] for r in range(1, 7)]
    real_res = lpmod.solve_moment_lp(gammas, real_moments, maximize=True)
    R6_real = real_res["value"] / C_q_real

    family_results = {}
    for fam in [
        "uniform_random_exp",
        "uniform_flat",
        "pure_low_level",
        "pure_high_level",
        "two_point_mixture",
        "decaying_low_to_high",
        "growing_low_to_high",
    ]:
        n_samp = n_random_samples if fam == "uniform_random_exp" else 1
        vals = run_family_batch(gammas, fam, n_samp, rng)
        family_results[fam] = {
            "n_samples": len(vals),
            "mean_R6": float(np.mean(vals)) if vals else None,
            "std_R6": float(np.std(vals)) if len(vals) > 1 else None,
            "min_R6": float(np.min(vals)) if vals else None,
            "max_R6": float(np.max(vals)) if vals else None,
        }

    result = {
        "n": n,
        "N": N,
        "q": q,
        "L": L,
        "R6_real": R6_real,
        "synthetic_families": family_results,
    }
    print(f"=== n={n} L={L} ===  R6_real={R6_real:.4f}", flush=True)
    for fam, stats in family_results.items():
        if stats["std_R6"] is not None:
            print(
                f"  {fam:24s}: mean={stats['mean_R6']:.4f} std={stats['std_R6']:.4f} "
                f"range=[{stats['min_R6']:.4f},{stats['max_R6']:.4f}] (n={stats['n_samples']})",
                flush=True,
            )
        else:
            print(f"  {fam:24s}: R6={stats['mean_R6']:.4f}", flush=True)
    return result


def run(n_random_samples: int = 500, seed: int = 42) -> list[dict]:
    with open(METRICS / "higher_moments_M1_M6.json", encoding="utf-8") as f:
        rows = sorted(json.load(f)["rows"], key=lambda r: r["n"])

    results = [run_one_n(r, n_random_samples, seed + i) for i, r in enumerate(rows)]

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "lp_bound_synthetic_control.json", "w", encoding="utf-8") as f:
        json.dump(
            {"rows": results, "n_random_samples": n_random_samples, "seed": seed}, f, indent=2
        )
    return results


if __name__ == "__main__":
    run()
    print("\nDone.", flush=True)
