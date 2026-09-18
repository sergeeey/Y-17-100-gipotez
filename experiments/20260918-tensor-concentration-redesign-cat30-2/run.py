"""
H-CAT30-2 (redesign of H-CAT30-1, per its own Relaxation Map): n=n(d) scaling
so the search is genuinely d-dimensional (span{a_i}=R^d generically once
n>=d), removing the span-confinement degeneracy that killed H-CAT30-1.

r=3, p=2 (open regime p<2r=6). T_i = a_i^{otimes 3}, unit a_i, so
||T_i||_{I_2}=1 exactly and Sigma||T_i||_{I_2}^2 = n(d) exactly.

Measures R(d) = E||sum g_i T_i||_{I_2} / sqrt(n(d)) (NOT the raw LHS -- per
skeptic's own redesign spec) on TWO independent n(d) scalings:
  Scale A: n(d) = d            (boundary case, span{a_i}=R^d generically)
  Scale B: n(d) = round(d^1.5)  (n grows faster than d)

>=8 independent draws of the tensor family A per (scale, d) point. Error bars
use the between-family standard error of each family's own within-family MC
mean (NOT a full two-level within+between variance decomposition -- the
within-family Monte Carlo noise is averaged out inside each family's mean
before the between-family SE is computed, not propagated separately).

Certified upper bound (matricization SVD, verified sigma_max(M) >=
||S||_{I_2} always -- see verify_matricization_upper_bound.py, imported here
rather than reimplemented) computed on a subset of draws per family as a
validity check on the power-iteration lower bound, not as the primary
estimate.
"""

import json
import time

import numpy as np
from tensor_injective_norm import estimate_injective_norm
from verify_matricization_upper_bound import matricization_upper_bound


def run_one_point(d, n, n_families, n_gaussian_draws, n_upper_check, seed):
    """Returns per-family mean R values (list of length n_families), each the
    mean over n_gaussian_draws MC draws for that family, plus a sandwich
    validity ratio computed on a few draws."""
    rng = np.random.default_rng(seed)
    family_means = []
    sandwich_ratios = []
    for fam in range(n_families):
        A = rng.standard_normal((n, d))
        A = A / np.linalg.norm(A, axis=1, keepdims=True)
        draws = []
        for k in range(n_gaussian_draws):
            g = rng.standard_normal(n)
            val, _ = estimate_injective_norm(A, g, n_restarts=40, n_iter=60, rng=rng)
            draws.append(val)
            if k < n_upper_check:
                upper = matricization_upper_bound(A, g, d)
                if val > 1e-12:
                    sandwich_ratios.append(upper / val)
        family_means.append(float(np.mean(draws)))
    return family_means, sandwich_ratios


def summarize_point(family_means, n_d):
    """Two-level variance: within-family MC noise averaged out by using each
    family's OWN mean; between-family variance is the variance of those
    family means across families (this IS the correct error bar for a
    'draw a fresh random family' estimand, per the reviewer's own critique
    of H-CAT30-1's single-family design)."""
    family_means = np.array(family_means)
    grand_mean = family_means.mean()
    between_family_se = family_means.std(ddof=1) / np.sqrt(len(family_means))
    R = grand_mean / np.sqrt(n_d)
    R_se = between_family_se / np.sqrt(n_d)
    return {
        "grand_mean": float(grand_mean),
        "between_family_se": float(between_family_se),
        "R": float(R),
        "R_se": float(R_se),
        "n_families": len(family_means),
        "family_means": family_means.tolist(),
    }


def run_scale(
    scale_name, d_values, n_of_d, n_families=8, n_gaussian_draws=15, n_upper_check=3, base_seed=0
):
    results = {}
    for idx, d in enumerate(d_values):
        n = n_of_d(d)
        t0 = time.time()
        family_means, sandwich_ratios = run_one_point(
            d, n, n_families, n_gaussian_draws, n_upper_check, seed=base_seed + 1000 * idx
        )
        summary = summarize_point(family_means, n)
        summary["d"] = d
        summary["n"] = n
        summary["sandwich_ratio_mean"] = (
            float(np.mean(sandwich_ratios)) if sandwich_ratios else None
        )
        summary["sandwich_ratio_max"] = float(np.max(sandwich_ratios)) if sandwich_ratios else None
        summary["elapsed_s"] = time.time() - t0
        results[d] = summary
        print(
            f"[{scale_name}] d={d:4d} n={n:5d}  R={summary['R']:.4f} +/- {summary['R_se']:.4f}  "
            f"sandwich_ratio_mean={summary['sandwich_ratio_mean']}  "
            f"elapsed={summary['elapsed_s']:.1f}s"
        )
    return results


if __name__ == "__main__":
    from pathlib import Path

    scale_a = run_scale("A: n=d", d_values=[10, 20, 40, 80], n_of_d=lambda d: d, base_seed=1)
    scale_b = run_scale(
        "B: n=d^1.5", d_values=[5, 10, 20, 30], n_of_d=lambda d: round(d**1.5), base_seed=2
    )

    out = {"scale_A_n_eq_d": scale_a, "scale_B_n_eq_d1p5": scale_b}
    out_path = Path(__file__).resolve().parent / "metrics" / "run.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWritten to {out_path}")
