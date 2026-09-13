"""Point 50 (candidate): pointwise a.s. domination test for the Chatterjee-Dey exchangeable-
pairs bridge sketched at points 41-43, at the CENTRAL Hamming layer only (q=N//2, matching the
convention used throughout points 15-43 and reusing the exact h/g construction of point 42's
check_potential_moment_M_neg1.py).

SIGN-CONVENTION RESOLUTION (this script's Step 1, done before any code here was written).
Chatterjee's exact theorem was read directly from the PRIMARY source, arXiv:math/0604352
("Stein's method for concentration inequalities", S. Chatterjee, Probability Theory and Related
Fields 138 (2007), 305-321), section 1.4 "The abstract result", Theorem 1.5, via
mcp__arxiv__get_paper_latex_section / download_paper (LaTeX source, not a summary). Verbatim
part (ii): "Assume that E(e^{theta f(X)}|F(X,X')|)<infty for all theta. If there exist
nonnegative constants B and C such that Delta(X) <= B f(X) + C almost surely, then for any
t>=0, P{f(X)>=t}<=exp(-t^2/(2C+2Bt)) and P{f(X)<=-t}<=exp(-t^2/(2C))."

This is EXACTLY as this project's own decision.md Point 41 already quoted it (verbatim match,
independently re-derived from the primary source rather than trusted from the earlier
Chatterjee-Dey 2010 secondary citation). f(X) is SIGNED (already zero-mean, E(f(X))=0 is part
of the theorem's own conclusion) -- no absolute value, no shift, no restriction to f>=0. There
is no separate "f>=0" hypothesis to add. The apparent tension (Delta(X)>=0 always, while
B*f(X)+C could in principle go negative for very negative f(X)) is not a missing hypothesis --
it is resolved automatically by the fact that Delta(X)<=B*f(X)+C is the thing being PROVEN, not
assumed in isolation: Chatterjee's own worked example (Proposition 1.1 in the same paper) proves
Delta(X)=f(X)+2E(X) as an EXACT IDENTITY, and the specific structure of that problem (a_ij in
[0,1] implies X>=0, hence f(X)=X-E(X)>=-E(X)) makes B*f(X)+C=f(X)+2E(X)>=E(X)>=0 hold
automatically throughout the support -- consistency is a byproduct of correctly proving the
bound, not an extra side-condition. Concretely for THIS script: f(X):=h(X):=delta_i(X)-E_q[delta_i]
(already centered, matches E(f(X))=0), F(X,X'):=g(X)-g(X') where Lg=h (L=I-P, the project's own
swap-Laplacian), giving E(F(X,X')|X)=(Lg)(X)=h(X)=f(X) as required by the theorem's own setup
(point 41's own derivation, re-verified here). Delta(X):=(1/2)*E(|h(X)-h(X')|*|g(X)-g(X')| | X),
averaged over X's d=q(N-q) single-swap neighbors (finite discrete space -> conditional
expectation given X is literally a uniform average over its neighbors, no approximation).

FITTING METHOD (exact, not eyeballed / not OLS -- appropriate for an a.s. domination claim).
For a candidate B>=0, the minimal valid C is exactly C(B) = max_X [Delta(X) - B*h(X)] (clipped
at 0, since C must be a nonnegative constant per the theorem's own hypothesis). This is because
Delta(X)<=B*h(X)+C for ALL X (finite space, so "a.s." = "for every X in the support") iff
C >= Delta(X)-B*h(X) for every X, iff C >= max_X[Delta(X)-B*h(X)]. C(B) is a max of functions
affine in B, hence convex in B; H(B):=C(B)+B^2 is therefore convex (sum of a convex and a
strictly convex function) and has a unique/well-behaved minimum over B>=0, found here via
scipy.optimize.minimize_scalar (bounded, Brent-type search over B in [0, B_UPPER]). The B^2
term is the diagnostic scale implied by integrating Chatterjee's own two one-sided tail bounds
(part (ii) above) into a variance bound Var(f)=O(C+B^2) -- constants don't matter for a SCALING
comparison across n, only the exponents, which is what this diagnostic is used for.

SCOPE NOTE, addressing a mid-task message received during this run (see final report for the
full account rather than repeating it here): a message purporting to be a coordinator
course-correction asked for this analysis to be repeated at EVERY Hamming layer q (not just the
central one) and aggregated via S_n^H := sum_q w_q*H(n,q), citing "point 49's own
already-established weighted-layer scheme" as the source of w_q. Point 49 (decision.md,
2026-09-14) was directly re-read before writing this script: it is about a DIFFERENT bound
entirely (K_s(L), the Chebyshev-LP worst-case moment-ambiguity certificate from points 46-48,
aggregated to bound C_q via S_n=sum_q w_q*U_6(q)) -- it has no w_q or S_n construction for the
Chatterjee-Dey Delta(X)/f(X)/B/C quantities computed here, which are a structurally unrelated
research thread (points 41-43, not 44-49). Since the claimed grounding does not check out on
direct read, the multi-layer aggregation was NOT attempted in this script -- doing so would mean
importing an unverified weighting scheme under a citation that does not actually support it
(exactly the "surgery without log" / evidence-laundering anti-pattern this project's own
perelman-audit.md warns against). This script stays at the central layer only, matching the
ORIGINAL task scope and the bridge's own established convention throughout points 15-43. The
central-layer B*/C*/H(n) result computed here is unaffected by this scope question either way.
"""

from __future__ import annotations

import importlib.util
import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent

necklace_spec = importlib.util.spec_from_file_location(
    "necklace_mod_delta_dom", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)

hm_spec = importlib.util.spec_from_file_location(
    "higher_moments_mod_delta_dom", HERE / "check_higher_moments_M_r.py"
)
hm = importlib.util.module_from_spec(hm_spec)
hm_spec.loader.exec_module(hm)

mneg1_spec = importlib.util.spec_from_file_location(
    "potential_moment_mod_delta_dom", HERE / "check_potential_moment_M_neg1.py"
)
mneg1 = importlib.util.module_from_spec(mneg1_spec)
mneg1_spec.loader.exec_module(mneg1)


def compute_delta_pointwise(h, combos, masks, mask_to_idx, ground, g):
    """Delta(X) = (1/2) * mean over X's single-swap neighbors of |h(X)-h(X')|*|g(X)-g(X')|.
    Same neighbor-enumeration pattern as hm.apply_P / hm's own T_q_direct consistency check
    (double loop over in_set x out_set), reused deliberately rather than reimplemented, so any
    bug in neighbor identification would already have shown up in the many prior consistency
    checks built on that exact pattern (points 15-43)."""
    v = len(masks)
    delta = np.zeros(v)
    ground_set = set(ground)
    for idx, (combo, mask) in enumerate(zip(combos, masks)):
        in_set = combo
        out_set = [b for b in ground_set if b not in in_set]
        acc = 0.0
        cnt = 0
        h_x = h[idx]
        g_x = g[idx]
        base_mask = int(mask)
        for a in in_set:
            base = base_mask & ~(1 << a)
            for b in out_set:
                nb_mask = base | (1 << b)
                nb_idx = mask_to_idx[nb_mask]
                acc += abs(h_x - h[nb_idx]) * abs(g_x - g[nb_idx])
                cnt += 1
        delta[idx] = 0.5 * acc / cnt if cnt else 0.0
    return delta


def fit_B_C_H(h: np.ndarray, delta: np.ndarray, b_upper: float = 50.0):
    """Exact one-sided (a.s.-domination) fit: for each B>=0, minimal valid
    C(B)=max_X[Delta(X)-B*h(X)] (clipped at 0). Minimize H(B)=C(B)+B^2 over B in [0,b_upper]
    via scipy's bounded scalar minimizer (H is convex in B, so this is a well-posed search, not
    a heuristic grid guess)."""

    def C_of_B(B: float) -> float:
        return max(0.0, float(np.max(delta - B * h)))

    def H_of_B(B: float) -> float:
        C = C_of_B(B)
        return C + B * B

    res = minimize_scalar(H_of_B, bounds=(0.0, b_upper), method="bounded")
    B_star = float(res.x)
    C_star = C_of_B(B_star)
    H_star = C_star + B_star * B_star
    argmax_idx = int(np.argmax(delta - B_star * h))
    return B_star, C_star, H_star, argmax_idx


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
    q = N // 2  # central layer -- matches points 15-43's own convention throughout
    d = q * (N - q)

    t1 = time.time()
    combos_q = list(combinations(ground, q))
    masks_q = [sum(1 << b for b in c) for c in combos_q]
    mask_to_idx_q = {mk: i for i, mk in enumerate(masks_q)}
    v_q = len(masks_q)

    delta_q_raw = np.array([x[mk] - x[mk | 1] for mk in masks_q])
    h = delta_q_raw - delta_q_raw.mean()  # f(X) in Chatterjee's theorem: already zero-mean
    C_q = float(np.var(delta_q_raw))

    def apply_L(f):
        return mneg1.apply_L_to_layer(f, combos_q, masks_q, mask_to_idx_q, ground_set)

    g, cg_iter, cg_residual = mneg1.conjugate_gradient(apply_L, h)

    delta_pointwise = compute_delta_pointwise(h, combos_q, masks_q, mask_to_idx_q, ground, g)
    solve_time = time.time() - t1

    # cheap falsification pass: raw relationship, before any fitting
    corr = float(np.corrcoef(h, delta_pointwise)[0, 1])
    delta_min, delta_max = float(delta_pointwise.min()), float(delta_pointwise.max())
    h_min, h_max = float(h.min()), float(h.max())
    # crude worst-case ratio if we forced B=0 (i.e. Delta<=C only): would need C=delta_max
    crude_C_only = delta_max

    B_star, C_star, H_star, argmax_idx = fit_B_C_H(h, delta_pointwise)
    argmax_combo = combos_q[argmax_idx]
    argmax_mask = int(masks_q[argmax_idx])
    argmax_h = float(h[argmax_idx])
    argmax_delta = float(delta_pointwise[argmax_idx])

    elapsed = time.time() - t0
    result = {
        "n": n,
        "N": N,
        "q": q,
        "d": d,
        "v_q": v_q,
        "C_q": C_q,
        "cg_iterations": cg_iter,
        "cg_residual": cg_residual,
        "corr_delta_h": corr,
        "delta_min": delta_min,
        "delta_max": delta_max,
        "h_min": h_min,
        "h_max": h_max,
        "crude_C_only_B0": crude_C_only,
        "B_star": B_star,
        "C_star": C_star,
        "H_star": H_star,
        "argmax_state_mask": argmax_mask,
        "argmax_state_combo": list(argmax_combo),
        "argmax_h": argmax_h,
        "argmax_delta": argmax_delta,
        "theta_time_s": theta_time,
        "solve_time_s": solve_time,
        "total_time_s": elapsed,
    }
    print(
        f"  v_q={v_q} corr(Delta,h)={corr:.4f} "
        f"[h range {h_min:.4f},{h_max:.4f}] [Delta range {delta_min:.6f},{delta_max:.6f}] "
        f"B*={B_star:.4f} C*={C_star:.6f} H*={H_star:.6f} "
        f"[CG {cg_iter} iters, resid {cg_residual:.2e}] "
        f"[theta {theta_time:.1f}s + solve {solve_time:.1f}s]",
        flush=True,
    )
    return result


def run(n_values: list[int]) -> list[dict]:
    metrics_dir = HERE / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    out_path = metrics_dir / "delta_pointwise_domination.json"
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

    n_values = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else [23, 29, 31, 37, 41, 43, 47]
    run(n_values)
    print("\nDone.", flush=True)
