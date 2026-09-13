"""Point 34: a genuine analytic attempt at ||L^{r/2} delta_i||^2 (route C's real target, per
the user's own plan). Exact new identity, verified to machine precision
(check_cross_layer_identity.py, not committed separately -- folded into this point):

    L(delta_i)(S) = Lq(X)(S) - Lq1(X)(S union {i})      for S in layer q

(a swap of S in layer q induces the IDENTICAL swap of S union {i} in layer q+1, since i is
never touched -- so the same swap-Laplacian structure applies to both terms). This reduces
M_2(delta_i) = ||L(delta_i)||^2 to a question about X's OWN cross-layer swap-smoothness, not a
new object invented for delta_i.

This script checks whether the decomposition actually HELPS: is there cancellation between the
two terms (correlation near 1, making M_2(delta_i) substantially smaller than the "independent"
sum ||LqX||^2+||Lq1X||^2), or do they behave independently (no help)? Computes, over the FULL
layer q: ||LqX||^2, ||Lq1X_shifted||^2, their correlation, and M_2(delta_i) both directly and
via the decomposition (self-consistency check on the identity itself).
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
    "necklace_mod_cancel", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)


def build_x_array(n: int):
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))
    return x, m


def apply_L_to_layer(values: np.ndarray, combos, masks, mask_to_idx, ground_set) -> np.ndarray:
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


def check_one(n: int):
    x, m = build_x_array(n)
    ground = list(range(1, m))
    N = len(ground)
    ground_set = set(ground)
    q = N // 2

    combos_q = list(combinations(ground, q))
    masks_q = [sum(1 << b for b in c) for c in combos_q]
    mask_to_idx_q = {mk: i for i, mk in enumerate(masks_q)}

    X_q = np.array([x[mk] for mk in masks_q])
    g_q = np.array([x[mk | 1] for mk in masks_q])  # g(S):=X(S union {i}), domain = layer q
    delta_q = X_q - g_q

    LqX = apply_L_to_layer(X_q, combos_q, masks_q, mask_to_idx_q, ground_set)
    # applying the SAME layer-q swap structure to g gives L_{q+1}(X)(S union {i}) exactly,
    # since a swap of S in layer q induces the identical swap of S union {i} in layer q+1
    # (verified exactly in check_cross_layer_identity.py, 1e-16 agreement)
    Lq1X_shifted = apply_L_to_layer(g_q, combos_q, masks_q, mask_to_idx_q, ground_set)

    Ldelta_direct = apply_L_to_layer(delta_q, combos_q, masks_q, mask_to_idx_q, ground_set)
    Ldelta_via_decomp = LqX - Lq1X_shifted

    v_q = len(masks_q)
    # M2 = ||L delta||^2 / v  (L already annihilates the mean component)
    M2_direct = float(np.dot(Ldelta_direct, Ldelta_direct)) / v_q
    M2_via_decomp = float(np.dot(Ldelta_via_decomp, Ldelta_via_decomp)) / v_q

    norm_LqX_sq = float(np.dot(LqX, LqX)) / v_q
    norm_Lq1X_sq = float(np.dot(Lq1X_shifted, Lq1X_shifted)) / v_q
    cross_term = float(np.dot(LqX, Lq1X_shifted)) / v_q
    correlation = (
        cross_term / np.sqrt(norm_LqX_sq * norm_Lq1X_sq)
        if norm_LqX_sq * norm_Lq1X_sq > 0
        else float("nan")
    )

    result = {
        "n": n,
        "N": N,
        "q": q,
        "M2_direct": M2_direct,
        "M2_via_decomp": M2_via_decomp,
        "identity_consistency_err": abs(M2_direct - M2_via_decomp),
        "norm_LqX_sq": norm_LqX_sq,
        "norm_Lq1X_shifted_sq": norm_Lq1X_sq,
        "cross_term": cross_term,
        "correlation": correlation,
        "sum_if_independent": norm_LqX_sq + norm_Lq1X_sq,
    }
    print(
        f"n={n:3d} N={N:2d} q={q:2d}  "
        f"M2_direct={M2_direct:.6f}  M2_via_decomp={M2_via_decomp:.6f}  "
        f"||LqX||^2={norm_LqX_sq:.6f}  ||Lq1X_shift||^2={norm_Lq1X_sq:.6f}  "
        f"cross={cross_term:.6f}  corr={correlation:.4f}  "
        f"sum_if_independent={result['sum_if_independent']:.6f}",
        flush=True,
    )
    return result


if __name__ == "__main__":
    rows = [check_one(n) for n in (23, 29, 31, 37)]

    xs = [math.log(r["n"]) for r in rows]
    ys = [math.log(r["norm_LqX_sq"]) for r in rows]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    slope = num / den if den != 0 else float("nan")
    print(f"\nlog-log slope of ||LqX||^2 vs n: {slope:.4f}")

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "cross_layer_cancellation.json", "w", encoding="utf-8") as f:
        json.dump({"rows": rows, "loglog_slope_LqX_sq": slope}, f, indent=2)
