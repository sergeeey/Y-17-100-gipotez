"""L2' test: does T_q(X) := E_swap[(X(S)-X(S'))^2] = 2*<X, L_qX> = 2*M_1(X) decay as O(n^-2) at
the central Hamming layer q~N/2?

Motivation (per decision.md point 15's own Johnson-graph swap-Poincare machinery, and point
34/35's M_2(X)=||L_qX||^2 finding): point 15 established, for ANY f on layer q,

    T_q(f) = E[(f(S)-f(S'))^2] = 2*<f, L_qf>                         (exact Dirichlet identity,
                                                                        reversible swap walk)
    Var(f | Q=q) <= T_q(f) * q(N-q) / (2N)                             (Poincare, gap=N/(q(N-q)))

Both were verified/used there only for f=delta_i (single-generator sensitivity). Points 34/35
computed M_2(X) := <X, L_q^2 X> = ||L_qX||^2 (applying the swap-Laplacian to X TWICE, in the
sense of two implicit applications via the squared norm) and found it decays empirically like
n^-1.45. Nobody in this experiment has yet computed M_1(X) := <X, L_qX> (ONE application of the
swap-Laplacian to X, dotted with X itself) -- this script computes exactly that, for the first
time, and checks whether the resulting T_q(X)=2*M_1(X) decays fast enough (O(n^-2)) to combine
with the already-established spectral gap gamma_1=N/(q(N-q))~4/N into Var(X|Q=q)=O(n^-2)*O(n) =
O(1/n) -- a real, structurally-motivated route to (a component of) the target hypothesis
Var(log(theta(G)/sqrt(n))) = O(1/n).

PRE-REGISTERED PREDICTION (Falsification Ladder discipline, stated before any number is
computed): L2' predicts n^2*T_q(X) settles toward a plateau/bounded value as n grows across the
7 already-solved n in {23,29,31,37,41,43,47}. FALSIFIED if a power-law fit of T_q(X) vs n
instead shows continued growth relative to n^-2 -- i.e. the log-log slope of T_q(X) vs n is well
above -2 (equivalently, n^2*T_q(X) itself grows with n, not merely fluctuates near a constant).

Reuse discipline (per this project's own standing practice, points 50/51): `solve_orbit_reduced`
is reused UNCHANGED from check_necklace_orbit_reduction.py; `apply_L_to_layer` is reused
UNCHANGED (byte-identical logic) from check_cross_layer_cancellation.py -- not reimplemented.

Substrate Gate cross-check (before trusting M_1): this script's own ||L_qX||^2 = M_2(X) is
compared against the ALREADY-COMMITTED values in metrics/cross_layer_cancellation.json (n=23,29,
31,37) and metrics/extended_moments_41_43_47.json (n=41,43,47) -- if this script's X_q array and
apply_L_to_layer usage reproduce those independently-verified numbers exactly, that is strong
positive-control evidence the M_1(X) computed alongside it (same X_q, same LqX, just a different
inner product) is trustworthy too.

Independent identity check (not assumed from point 15's proof, verified here for f=X specifically
at the two cheapest n): T_q(X) computed via DIRECT exhaustive swap-pair enumeration (same method
as check_johnson_swap_energy.py, but applied to X instead of delta_i) is compared against
2*M_1(X) computed via the operator route -- point 15's identity was proven in general and
verified for f=delta_i, but never numerically checked for f=X specifically until now.
"""

from __future__ import annotations

import importlib.util
import json
import math
import statistics
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_spec = importlib.util.spec_from_file_location(
    "necklace_mod_Tq_X", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)


def build_x_array(n: int):
    """Reused unchanged from check_cross_layer_cancellation.py (point 34)."""
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))
    return x, m


def apply_L_to_layer(values: np.ndarray, combos, masks, mask_to_idx, ground_set) -> np.ndarray:
    """Reused unchanged (byte-identical logic) from check_cross_layer_cancellation.py."""
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
        Pv = acc / cnt if cnt else 0.0
        out[idx] = values[idx] - Pv
    return out


def direct_T_q_enumeration(X_q, combos_q, masks_q, mask_to_idx_q, ground):
    """Exact T_q(X) via exhaustive enumeration of every swap pair in the layer -- same method
    as check_johnson_swap_energy.py's swap_energy_per_layer, applied to X instead of delta_i.
    Independent of the apply_L_to_layer route (no shared code path)."""
    sq_diffs = []
    for combo, mask in zip(combos_q, masks_q):
        in_set = set(combo)
        out_set = [b for b in ground if b not in in_set]
        x_s = X_q[mask_to_idx_q[int(mask)]]
        for a in in_set:
            base = int(mask) & ~(1 << a)
            for b in out_set:
                neighbor_mask = base | (1 << b)
                sq_diffs.append((x_s - X_q[mask_to_idx_q[neighbor_mask]]) ** 2)
    return float(np.mean(sq_diffs))


# Substrate Gate cross-check targets: ||L_qX||^2 = M_2(X), already committed by points 34/35.
COMMITTED_NORM_LQX_SQ = {
    23: 0.017564887154384076,
    29: 0.012722161043056743,
    31: 0.011606869441590267,
    37: 0.008789302516795137,
    41: 0.007465391701594957,
    43: 0.006776960070470608,
    47: 0.005734673426462185,
}


def run_one(n: int, do_direct_enumeration: bool) -> dict:
    x, m = build_x_array(n)
    ground = list(range(1, m))
    N = len(ground)
    ground_set = set(ground)
    q = N // 2  # central layer, matching every point 15-51 convention

    combos_q = list(combinations(ground, q))
    masks_q = [sum(1 << b for b in c) for c in combos_q]
    mask_to_idx_q = {mk: i for i, mk in enumerate(masks_q)}
    v_q = len(masks_q)

    X_q = np.array([x[mk] for mk in masks_q])

    LqX = apply_L_to_layer(X_q, combos_q, masks_q, mask_to_idx_q, ground_set)

    norm_LqX_sq = float(np.dot(LqX, LqX)) / v_q  # = M_2(X), Substrate Gate cross-check target
    M1 = float(np.dot(X_q, LqX)) / v_q  # = <X, L_qX>, the NEW quantity this point computes
    T_q_X_operator = 2.0 * M1

    committed = COMMITTED_NORM_LQX_SQ.get(n)
    substrate_check_err = abs(norm_LqX_sq - committed) if committed is not None else None
    substrate_check_rel = substrate_check_err / committed if committed and committed != 0 else None

    T_q_X_direct = None
    identity_err = None
    identity_rel_err = None
    if do_direct_enumeration:
        T_q_X_direct = direct_T_q_enumeration(X_q, combos_q, masks_q, mask_to_idx_q, ground)
        identity_err = abs(T_q_X_direct - T_q_X_operator)
        identity_rel_err = identity_err / T_q_X_direct if T_q_X_direct else None

    var_X_q = float(np.var(X_q))  # exact Var(X | Q=q), reported for context
    d = q * (N - q)
    gamma_1 = N / d  # already-established Johnson-scheme spectral gap (point 15)
    poincare_bound_var_X = T_q_X_operator / (2 * gamma_1)  # = T_q(X) * q(N-q) / (2N)

    result = {
        "n": n,
        "N": N,
        "q": q,
        "v_q": v_q,
        "d": d,
        "gamma_1": gamma_1,
        "norm_LqX_sq_M2": norm_LqX_sq,
        "committed_norm_LqX_sq": committed,
        "substrate_check_abs_err": substrate_check_err,
        "substrate_check_rel_err": substrate_check_rel,
        "M1_X": M1,
        "T_q_X_operator": T_q_X_operator,
        "T_q_X_direct_enumeration": T_q_X_direct,
        "identity_abs_err": identity_err,
        "identity_rel_err": identity_rel_err,
        "var_X_given_q": var_X_q,
        "poincare_bound_var_X": poincare_bound_var_X,
        "poincare_tightness": var_X_q / poincare_bound_var_X if poincare_bound_var_X else None,
        "n2_times_Tq_X": n * n * T_q_X_operator,
    }
    print(
        f"n={n:3d} N={N:2d} q={q:2d} v_q={v_q:7d}  M1(X)={M1:.8f}  T_q(X)={T_q_X_operator:.8f}  "
        f"n^2*T_q(X)={result['n2_times_Tq_X']:.4f}  "
        f"substrate_rel_err={substrate_check_rel}  "
        f"Var(X|q)={var_X_q:.6f}  Poincare_bound={poincare_bound_var_X:.6f}  "
        f"tightness={result['poincare_tightness']}",
        flush=True,
    )
    return result


def loglog_slope(xs_n, ys_val):
    xs = [math.log(v) for v in xs_n]
    ys = [math.log(v) for v in ys_val]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den != 0 else float("nan")


if __name__ == "__main__":
    n_values = [23, 29, 31, 37, 41, 43, 47]
    # Direct exhaustive-enumeration identity check only at the two cheapest n (layer sizes
    # 252 and 1716) to keep this an independent cross-check, not a repeat of the full-cost
    # computation at every n -- the identity T_q=2<f,Lf> is already a PROVEN theorem (point 15),
    # this is a numerical spot-check that it also holds for f=X specifically, not a re-derivation.
    direct_check_n = {23, 29}

    rows = [run_one(n, do_direct_enumeration=(n in direct_check_n)) for n in n_values]

    slope_Tq = loglog_slope(n_values, [r["T_q_X_operator"] for r in rows])
    slope_n2Tq = loglog_slope(n_values, [r["n2_times_Tq_X"] for r in rows])

    print(f"\nlog-log slope of T_q(X) vs n: {slope_Tq:.4f}  (prediction: near -2 if L2' holds)")
    print(
        f"log-log slope of n^2*T_q(X) vs n: {slope_n2Tq:.4f}  "
        f"(prediction: near 0 / plateau if L2' holds; positive => growth => FALSIFIED)"
    )

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "value_swap_energy_T_q.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "rows": rows,
                "loglog_slope_Tq_X_vs_n": slope_Tq,
                "loglog_slope_n2Tq_X_vs_n": slope_n2Tq,
            },
            f,
            indent=2,
        )
