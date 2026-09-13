"""Entry-by-entry consistency check of the external-review claim: is the "restricted
i-preserving operator L*" from point 34 literally IDENTICAL to L_q itself (not merely an
isomorphic-but-distinct operator)?

Point 34's code computed L* by calling apply_L_to_layer(g_q, combos_q, masks_q, mask_to_idx_q,
ground_set) -- the SAME Python call used for L_q(X_q), just with a different input array. That
already establishes L*=L_q by direct code inspection alone -- THIS is the substantive argument
(see decision.md point 36), not this script. This script builds L* a second way -- by literally
enumerating i-preserving swaps on the (q+1)-subset domain S union {i} directly (a separately
coded loop, not calling layer-q's own combos/masks machinery) -- and checks entry-by-entry
agreement against the original apply_L_to_layer route.

Reviewer finding (P2, addressed in decision.md's point 36 as well): the two routes' exact
`0.000e+00` agreement is NOT independent empirical evidence for L*=L_q -- it is algebraically
FORCED by bit-disjointness (bit i never overlaps the ground bits used in combos_q, so both
routes' index arithmetic reduces to the same expression for any a,b). This script therefore
verifies IMPLEMENTATION correctness (no bug hides a divergence between the two code paths), not
an independent mathematical confirmation of the underlying claim -- that argument is the code-
inspection one stated above, and in decision.md's point 36.
"""

from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(
    r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez"
    r"\experiments\20260910-lovasz-theta-variance-scaling-cat31-3"
)

necklace_spec = importlib.util.spec_from_file_location(
    "necklace_mod_verify", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_spec)
necklace_spec.loader.exec_module(nm)


def apply_L_to_layer(values, combos, masks, mask_to_idx, ground_set):
    out = np.empty_like(values)
    for idx, (combo, mask) in enumerate(zip(combos, masks)):
        out_set = [b for b in ground_set if b not in combo]
        acc = 0.0
        cnt = 0
        for a in combo:
            base = int(mask) & ~(1 << a)
            for b in out_set:
                acc += values[mask_to_idx[base | (1 << b)]]
                cnt += 1
        out[idx] = values[idx] - (acc / cnt if cnt else 0.0)
    return out


def verify(n: int):
    m = (n - 1) // 2
    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))

    ground = list(range(1, m))
    N = len(ground)
    ground_set = set(ground)
    q = N // 2

    combos_q = list(combinations(ground, q))
    masks_q = [sum(1 << b for b in c) for c in combos_q]
    mask_to_idx_q = {mk: i for i, mk in enumerate(masks_q)}

    X1 = np.array([x[mk | 1] for mk in masks_q])  # X_1(S) := X(S union {i}), S in layer q

    # Route A (point 34's original route): apply the layer-q operator directly to X1.
    L_route_A = apply_L_to_layer(X1, combos_q, masks_q, mask_to_idx_q, ground_set)

    # Route B (independent construction, NOT reusing layer-q's combos/masks at all): for each
    # S in layer q, build T = S union {i} directly, enumerate ONLY i-preserving swaps of T
    # (i.e. swap an element of T\{i} for an element of the complement excluding i), evaluate
    # X at the resulting (q+1)-set, and average -- entirely independent code path.
    L_route_B = np.empty_like(X1)
    all_ground = set(ground)
    for idx, (combo, mask) in enumerate(zip(combos_q, masks_q)):
        T_mask = mask | 1  # S union {i}
        in_set = combo  # T \ {i}, i.e. the non-i elements currently IN T
        out_set = [
            b for b in all_ground if b not in in_set
        ]  # ground elements NOT in T (i excluded by construction)
        acc = 0.0
        cnt = 0
        for a in in_set:
            base = T_mask & ~(1 << a)  # remove a, i stays (bit0 untouched)
            for b in out_set:
                neighbor_T = base | (1 << b)  # add b, still contains i
                acc += x[neighbor_T]
                cnt += 1
        PT = acc / cnt if cnt else 0.0
        L_route_B[idx] = x[T_mask] - PT

    max_err = float(np.max(np.abs(L_route_A - L_route_B)))
    mean_val = float(np.mean(np.abs(L_route_A)))
    relative = max_err / mean_val if mean_val else float("nan")
    print(
        f"n={n}: max|L_route_A - L_route_B| = {max_err:.3e}  "
        f"(mean|L_route_A|={mean_val:.6f}, relative={relative:.3e})"
    )
    return max_err


if __name__ == "__main__":
    for n in (23, 29, 31, 37):
        verify(n)
