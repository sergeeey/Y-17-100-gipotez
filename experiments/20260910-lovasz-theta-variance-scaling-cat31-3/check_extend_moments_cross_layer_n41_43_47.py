"""Point 35: extend point 33 (higher moments M_1,M_2,M_3, l_eff) and point 34 (cross-layer
cancellation) from n=23..37 to n=41,43,47 -- per direct user request ("попробуй расширить на
n=41,43,47"), matching the n-range already used for other quantities in this experiment (e.g.
points 22-24's tail_concentration_ratio.json).

Combines both computations per n (build the exact X array via check_necklace_orbit_reduction's
solve_orbit_reduced ONCE, reuse it for M_r AND the cross-layer identity check) to avoid paying
the expensive LP-solve cost twice per n -- check_higher_moments_M_r.py and
check_cross_layer_cancellation.py each independently call solve_orbit_reduced, which recomputes
theta from scratch (confirmed: solve_orbit_reduced has no cross-invocation cache, only an
unrelated cross_validation json.dump at its own module level).

Uses the same apply_L_to_layer = (I-P) swap-Laplacian construction as both parent scripts
(mathematically identical to check_higher_moments_M_r.py's apply_P -- L(f) = f - P(f)), and the
canonical l_eff_from_gamma() is imported directly from check_higher_moments_M_r.py (not
reimplemented) so l_eff values are computed by the exact same formula as points n=23..37.

Feasibility note (measured, not estimated): layer sizes grow steeply -- n=37 (already done) has
central-layer size C(17,8)=24310; n=41 is C(19,9)=92378 (3.8x); n=43 is C(20,10)=184756 (7.6x);
n=47 is C(22,11)=705432 (29x). Actual measured wall-clock costs on this machine: n=41 theta
195.6s + moments 18.2s; n=43 theta 213.6s + moments 40.0s; n=47 theta 807.0s + moments 163.6s --
all far cheaper than decision.md's own prior worst-case LP-solve-count estimate for this n-range
suggested (that estimate was about raw LP-solve counts, not wall-clock, and evidently overstated
the practical cost here) -- correcting that over-caution here explicitly rather than silently.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_spec = importlib.util.spec_from_file_location(
    "necklace_mod_ext35", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)

hm_spec = importlib.util.spec_from_file_location(
    "higher_moments_mod_ext35", HERE / "check_higher_moments_M_r.py"
)
hm = importlib.util.module_from_spec(hm_spec)
hm_spec.loader.exec_module(hm)


def build_x_array(n: int):
    t0 = time.time()
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))
    elapsed = time.time() - t0
    print(f"  [theta computed in {elapsed:.1f}s]", flush=True)
    return x, m, elapsed


def apply_L_to_layer(values, combos, masks, mask_to_idx, ground_set):
    """L(f) = f - P(f), identical construction to check_higher_moments_M_r.py's apply_P."""
    out = np.empty_like(values)
    for idx, (combo, mask) in enumerate(zip(combos, masks)):
        out_set = [b for b in ground_set if b not in combo]
        acc = 0.0
        cnt = 0
        for a in combo:
            base = int(mask) & ~(1 << a)
            for b in out_set:
                neighbor = base | (1 << b)
                acc += values[mask_to_idx[neighbor]]
                cnt += 1
        out[idx] = values[idx] - (acc / cnt if cnt else 0.0)
    return out


def run_one(n: int) -> dict:
    print(f"=== n={n} ===", flush=True)
    x, m, theta_time = build_x_array(n)
    ground = list(range(1, m))
    N = len(ground)
    ground_set = set(ground)
    q = N // 2

    t0 = time.time()
    combos_q = list(combinations(ground, q))
    masks_q = [sum(1 << b for b in c) for c in combos_q]
    mask_to_idx_q = {mk: i for i, mk in enumerate(masks_q)}
    v_q = len(masks_q)
    print(f"  layer size |V(q={q})|={v_q}", flush=True)

    X_q = np.array([x[mk] for mk in masks_q])
    g_q = np.array([x[mk | 1] for mk in masks_q])  # g(S) := X(S union {i})
    delta_q = X_q - g_q

    LqX = apply_L_to_layer(X_q, combos_q, masks_q, mask_to_idx_q, ground_set)
    LstarX_shifted = apply_L_to_layer(g_q, combos_q, masks_q, mask_to_idx_q, ground_set)
    Ldelta = apply_L_to_layer(delta_q, combos_q, masks_q, mask_to_idx_q, ground_set)
    L2delta = apply_L_to_layer(Ldelta, combos_q, masks_q, mask_to_idx_q, ground_set)

    # L annihilates the mean exactly, so L(delta_q) == L(delta_q - mean) algebraically --
    # centering delta_q before dotting (not before applying L) gives the identical M1/M2/M3.
    M1 = float(np.dot(delta_q - delta_q.mean(), Ldelta)) / v_q
    M2 = float(np.dot(Ldelta, Ldelta)) / v_q
    M3 = float(np.dot(Ldelta, L2delta)) / v_q
    C_q = float(np.var(delta_q))

    norm_LqX_sq = float(np.dot(LqX, LqX)) / v_q
    norm_Lstar_sq = float(np.dot(LstarX_shifted, LstarX_shifted)) / v_q
    cross_term = float(np.dot(LqX, LstarX_shifted)) / v_q
    correlation = (
        cross_term / np.sqrt(norm_LqX_sq * norm_Lstar_sq)
        if norm_LqX_sq * norm_Lstar_sq > 0
        else float("nan")
    )
    M2_via_decomp = float(np.dot(LqX - LstarX_shifted, LqX - LstarX_shifted)) / v_q
    identity_err = abs(M2 - M2_via_decomp)

    gamma_21 = M2 / M1 if M1 else float("nan")
    gamma_32 = M3 / M2 if M2 else float("nan")
    l_eff_21 = hm.l_eff_from_gamma(gamma_21, N, q)
    l_eff_32 = hm.l_eff_from_gamma(gamma_32, N, q)

    elapsed = time.time() - t0
    result = {
        "n": n,
        "N": N,
        "q": q,
        "v_q": v_q,
        "theta_time_s": theta_time,
        "moments_time_s": elapsed,
        "C_q": C_q,
        "M1": M1,
        "M2": M2,
        "M3": M3,
        "M2_over_M1": gamma_21,
        "M3_over_M2": gamma_32,
        "l_eff_from_M2_M1": l_eff_21,
        "l_eff_from_M2_M1_over_N": l_eff_21 / N,
        "l_eff_from_M3_M2": l_eff_32,
        "l_eff_from_M3_M2_over_N": l_eff_32 / N,
        "norm_LqX_sq": norm_LqX_sq,
        "norm_Lstar_sq": norm_Lstar_sq,
        "cross_term": cross_term,
        "correlation": correlation,
        "identity_consistency_err": identity_err,
    }
    print(
        f"  C_q={C_q:.6f} M1={M1:.6f} M2={M2:.6f} M3={M3:.6f} "
        f"M2/M1={gamma_21:.4f} M3/M2={gamma_32:.4f} "
        f"l_eff={l_eff_21:.4f} (l_eff/N={l_eff_21 / N:.4f}) "
        f"corr(LqX,Lstar)={correlation:.4f} identity_err={identity_err:.2e} "
        f"[theta {theta_time:.1f}s + moments {elapsed:.1f}s]",
        flush=True,
    )
    return result


def run(n_values: list[int]) -> list[dict]:
    METRICS.mkdir(exist_ok=True)
    out_path = METRICS / "extended_moments_41_43_47.json"
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
    n_values = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else [41, 43, 47]
    run(n_values)
    print("\nDone.", flush=True)
