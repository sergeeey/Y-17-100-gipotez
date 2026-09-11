"""First numeric attempt at the Johnson-graph angle for S_n = E[Var(delta_i | Q)], proposed
(not yet evaluated) in decision.md point 14's "next informative step" note.

Idea: within a fixed Hamming layer q (S subset of the m-1-element ground set excluding i,
|S|=q), the layer's subsets form the vertex set of a Johnson graph J(N,q) (N=m-1), with edges
connecting S,S' that differ by one SWAP (remove one element a in S, add one element b not in
S). This is a genuinely different move from every earlier LP-sensitivity attempt (points 6, 8,
9a), which only ever moved a single coordinate in/out, never swapped two.

This script does NOT assume any spectral/Poincare formula from memory (integrity.md: no
phantom formulas). It computes, directly from the SAME already-validated exact delta data used
throughout this experiment (necklace-orbit theta, cross-validated to 8.88e-14):

  C_q = Var(delta_i(S) | |S|=q)                          -- already known (point 14)
  T_q = E[(delta_i(S) - delta_i(S'))^2]  over uniform S in layer q and a uniform single swap S'

and reports the ratio C_q/T_q as a function of q and N=m-1. If a clean, q/N-dependent pattern
appears (e.g. consistent with a Poincare-type constant q(N-q)/N), that is evidence the swap-walk
genuinely controls the within-layer heterogeneity and a real bound might follow. If the ratio is
noisy/inconsistent, that is an equally informative negative result: the swap structure does not
cleanly explain C_q and a different theoretical tool is needed.

Starts at n=23 (m=11, N=10) -- the necklace-orbit method's own original cross-validation point,
cheapest possible sanity check before spending compute on larger n.
"""

from __future__ import annotations

import importlib.util
import json
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

necklace_mod = importlib.util.spec_from_file_location(
    "necklace_mod_johnson", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)


def swap_energy_per_layer(n: int) -> list[dict]:
    m = (n - 1) // 2
    ground = list(range(1, m))  # bits 1..m-1, excluding the fixed generator i=bit0
    N = len(ground)

    res = nm.solve_orbit_reduced(n, verbose=False)
    theta_full = res["theta_full"]
    x = np.log(theta_full / np.sqrt(n))

    n_subsets = 1 << m
    delta = np.empty(n_subsets)
    for mask in range(n_subsets):
        if mask & 1:
            continue
        delta[mask] = x[mask] - x[mask | 1]

    rows = []
    for q in range(N + 1):
        masks_this_layer = [sum(1 << b for b in combo) for combo in combinations(ground, q)]
        if not masks_this_layer:
            continue
        deltas = delta[masks_this_layer]
        c_q = float(np.var(deltas))

        sq_diffs = []
        for mask, combo in zip(masks_this_layer, combinations(ground, q)):
            in_set = set(combo)
            out_set = [b for b in ground if b not in in_set]
            d_s = delta[mask]
            for a in combo:
                base = mask & ~(1 << a)
                for b in out_set:
                    mask_swapped = base | (1 << b)
                    sq_diffs.append((d_s - delta[mask_swapped]) ** 2)
        t_q = float(np.mean(sq_diffs)) if sq_diffs else float("nan")

        rows.append(
            {
                "q": q,
                "N": N,
                "C_q": c_q,
                "T_q": t_q,
                "ratio_C_over_T": c_q / t_q if t_q and t_q > 0 else float("nan"),
                "n_swaps_averaged": len(sq_diffs),
                "n_masks_in_layer": len(masks_this_layer),
            }
        )
    return rows


def run(n_values: list[int]) -> dict:
    all_rows = {}
    for n in n_values:
        print(f"\n--- n={n} ---", flush=True)
        rows = swap_energy_per_layer(n)
        all_rows[n] = rows
        for r in rows:
            print(
                f"  q={r['q']:3d}/{r['N']:3d}  C_q={r['C_q']:.6f}  T_q={r['T_q']:.6f}  "
                f"C/T={r['ratio_C_over_T']:.4f}  (n_swaps={r['n_swaps_averaged']})",
                flush=True,
            )
    return all_rows


if __name__ == "__main__":
    out = run([23, 29, 31, 37])
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "johnson_swap_energy.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
