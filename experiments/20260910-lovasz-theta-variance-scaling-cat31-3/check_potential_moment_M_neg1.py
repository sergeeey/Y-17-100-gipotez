"""Point 42: cheap differentiating test related to the exchangeable-pairs bridge sketched in
point 41. Solve L*g = delta_i - mean(delta_i) via conjugate gradient (using the ALREADY VERIFIED
apply_L_to_layer matrix-vector product, no new machinery), then compute the negative spectral
moment M_{-1} := <g, Lg> = <g, delta_i> = sum_l E_l/gamma_l (using the defining equation, no
second L-application needed).

IMPORTANT FRAMING CORRECTION (external-review discipline, same as points 32/36/37/39): this
quantity is NOT itself a proof or even direct evidence of a sharper variance bound. Point 41's
own naive-F identity Var(h)=Var(h) was already shown to be tautological with this specific
choice of F=g(X)-g(X'); M_{-1} is a SEPARATE, purely descriptive diagnostic of the SHAPE of the
spectral measure E_l relative to the eigenvalues gamma_l -- specifically, how far the
harmonic-weighted spectral mass has moved away from being concentrated at the smallest nonzero
eigenvalue gamma_1 (the "spectral-gap extremizer"). A falling ratio M_{-1}/(C_q/gamma_1) is a
real, [EMPIRICAL] fact about increasing spectral separation from that extremizer -- it does
NOT by itself imply Var(X_n)=O(1/n), and should not be sold as a confirmed mechanism.

L's positive-semi-definiteness on the zero-mean subspace (required for conjugate gradient to be
a valid method here) is NOT re-derived in this script -- it was already established at points
15-18 (Eberlein-polynomial spectrum gamma_l=l(N+1-l)/(q(N-q)), l=1..min(q,N-q), all strictly
positive, cross-checked there against 30+ direct numpy.linalg.eigvalsh diagonalizations). The
swap-averaging operator P below is imported directly from check_higher_moments_M_r.py (the
already-reviewed, already-cross-checked implementation, T_q_direct vs 2*M1 verified there to
machine precision) rather than being reimplemented locally, per skeptic-fallback review finding
on an earlier draft of this script (which DID reimplement it locally with no positive control).
"""

from __future__ import annotations

import importlib.util
import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

necklace_spec = importlib.util.spec_from_file_location(
    "necklace_mod_mneg1", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)

hm_spec = importlib.util.spec_from_file_location(
    "higher_moments_mod_mneg1", HERE / "check_higher_moments_M_r.py"
)
hm = importlib.util.module_from_spec(hm_spec)
hm_spec.loader.exec_module(hm)


def apply_L_to_layer(values, combos, masks, mask_to_idx, ground_set):
    """L = I - P, using the canonical, already-reviewed apply_P from
    check_higher_moments_M_r.py (imported above as `hm`), not reimplemented here."""
    return values - hm.apply_P(values, combos, masks, mask_to_idx, list(ground_set))


def conjugate_gradient(apply_L, b, tol=1e-10, max_iter=2000):
    """Solve L g = b for g (b already zero-mean / orthogonal to L's kernel), via CG using
    only matrix-vector products through apply_L. Returns (g, n_iterations, final_residual)."""
    x = np.zeros_like(b)
    r = b - apply_L(x)
    p = r.copy()
    rs_old = float(np.dot(r, r))
    b_norm = float(np.dot(b, b)) or 1.0
    for it in range(max_iter):
        Ap = apply_L(p)
        denom = float(np.dot(p, Ap))
        if abs(denom) < 1e-300:
            break
        alpha = rs_old / denom
        x += alpha * p
        r -= alpha * Ap
        rs_new = float(np.dot(r, r))
        if rs_new / b_norm < tol:
            return x, it + 1, (rs_new / b_norm) ** 0.5
        beta = rs_new / rs_old
        p = r + beta * p
        rs_old = rs_new
    return x, max_iter, (rs_old / b_norm) ** 0.5


def run_one(n: int) -> dict:
    print(f"=== n={n} ===", flush=True)
    t0 = time.time()
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))
    theta_time = time.time() - t0

    ground = list(range(1, m))
    N = len(ground)
    ground_set = set(ground)
    q = N // 2
    d = q * (N - q)

    t1 = time.time()
    combos_q = list(combinations(ground, q))
    masks_q = [sum(1 << b for b in c) for c in combos_q]
    mask_to_idx_q = {mk: i for i, mk in enumerate(masks_q)}
    v_q = len(masks_q)

    delta_q = np.array([x[mk] - x[mk | 1] for mk in masks_q])
    h = delta_q - delta_q.mean()
    C_q = float(np.var(delta_q))

    def apply_L(f):
        return apply_L_to_layer(f, combos_q, masks_q, mask_to_idx_q, ground_set)

    g, n_iter, residual = conjugate_gradient(apply_L, h)
    # M_{-1} = <g, Lg> = <g, h> by the defining equation Lg=h (no second L-application needed)
    M_neg1 = float(np.dot(g, h)) / v_q

    gamma_1 = 1 * (N + 1 - 1) / d  # smallest nonzero Johnson eigenvalue, l=1
    crude_ceiling = C_q / gamma_1
    ratio = M_neg1 / crude_ceiling if crude_ceiling else float("nan")

    elapsed = time.time() - t1
    result = {
        "n": n,
        "N": N,
        "q": q,
        "d": d,
        "gamma_1": gamma_1,
        "C_q": C_q,
        "M_neg1": M_neg1,
        "crude_ceiling_Cq_over_gamma1": crude_ceiling,
        "ratio_M_neg1_over_ceiling": ratio,
        "cg_iterations": n_iter,
        "cg_residual": residual,
        "theta_time_s": theta_time,
        "solve_time_s": elapsed,
    }
    print(
        f"  C_q={C_q:.6f} gamma_1={gamma_1:.6f} M_-1={M_neg1:.6f} "
        f"ceiling={crude_ceiling:.6f} ratio={ratio:.4f} "
        f"[CG {n_iter} iters, residual {residual:.2e}] "
        f"[theta {theta_time:.1f}s + solve {elapsed:.1f}s]",
        flush=True,
    )
    return result


def run(n_values: list[int]) -> list[dict]:
    metrics_dir = HERE / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    out_path = metrics_dir / "potential_moment_M_neg1.json"
    all_results: list[dict] = []
    if out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            all_results = json.load(f).get("rows", [])
    done_ns = {r["n"] for r in all_results}
    for n in n_values:
        if n in done_ns:
            print(f"=== n={n} already done, skipping ===", flush=True)
            continue
        all_results.append(run_one(n))
        all_results.sort(key=lambda r: r["n"])
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"rows": all_results}, f, indent=2)
    return all_results


if __name__ == "__main__":
    import sys

    n_values = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else [23, 29, 31, 37]
    run(n_values)
    print("\nDone.", flush=True)
