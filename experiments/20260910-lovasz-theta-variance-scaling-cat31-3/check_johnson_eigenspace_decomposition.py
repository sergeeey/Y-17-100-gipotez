"""Layer-adaptive refinement of point 15's Johnson-graph bound, per direct user request
("попробуй послойно-адаптивную версию границы").

Point 15's bound used ONLY the worst-case (top nontrivial) eigenvalue lambda_1 of the swap walk
per layer -- Var(f) <= T_q/(2*gap), gap=1-lambda_1. That is a single-eigenspace worst case: it
implicitly assumes ALL of delta's within-layer variance sits in the slowest-mixing eigenspace.
If delta's actual energy is spread across several eigenspaces (most of which have a STRICTLY
BETTER gap, since eigenvalues decrease with eigenspace index l for the Johnson scheme), the
naive bound overshoots -- exactly the pattern observed (tightness 0.52->0.40 as n grows, bound
growing faster than C_q).

This script computes, by DIRECT diagonalization + projection (not a recalled formula), the
EXACT distribution of delta's within-layer variance across eigenspaces:

    C_q = Var(delta_i(S)|Q=q) = sum_l  (fraction of variance in eigenspace l)

grouping numerically-close eigenvalues (Johnson-scheme eigenspaces are highly degenerate -- many
eigenvectors share the same eigenvalue) into distinct levels. This is diagnostic: it does not by
itself produce a new independent bound (the level fractions are computed FROM the already-known
C_q, not predicted ahead of it) -- but it tells us WHERE the naive bound's slack comes from, and
whether an adaptive per-level treatment could plausibly tighten it.

Feasible only for small-to-moderate N (dense C(N,q)x C(N,q) diagonalization) -- n=23 (N=10, max
C(10,5)=252) and n=29 (N=13, max C(13,6)=1716) are both cheap; n=37 (N=17, max C(17,8)=24310)
is NOT attempted here (dense eigendecomposition of a 24310x24310 matrix is infeasible).
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
    "necklace_mod_eig", HERE / "check_necklace_orbit_reduction.py"
)
nm = importlib.util.module_from_spec(necklace_mod)
necklace_mod.loader.exec_module(nm)


def layer_decomposition(n: int, max_layer_size: int = 4000) -> list[dict]:
    m = (n - 1) // 2
    ground = list(range(1, m))
    big_n = len(ground)

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
    for q in range(1, big_n):
        subsets = list(combinations(ground, q))
        v = len(subsets)
        if v > max_layer_size:
            print(f"  q={q}: skipped, layer size {v} > {max_layer_size} (dense diag infeasible)")
            continue
        idx = {s: i for i, s in enumerate(subsets)}
        masks = [sum(1 << b for b in s) for s in subsets]
        f = delta[masks]
        f_centered = f - f.mean()
        c_q = float(np.var(f))

        a = np.zeros((v, v))
        for s in subsets:
            s_set = set(s)
            out = [b for b in ground if b not in s_set]
            for rem in s:
                base = s_set - {rem}
                for add in out:
                    nb = tuple(sorted(base | {add}))
                    a[idx[s], idx[nb]] = 1.0
        d = q * (big_n - q)
        p = a / d
        eigvals, eigvecs = np.linalg.eigh(p)

        # group numerically-close eigenvalues into distinct levels (Johnson-scheme degeneracy)
        order = np.argsort(-eigvals)
        eigvals_sorted = eigvals[order]
        eigvecs_sorted = eigvecs[:, order]
        proj = eigvecs_sorted.T @ f_centered  # projection coefficients
        energy = proj**2 / v  # contribution to Var per eigenvector (population variance)

        levels = []
        cur_eig = None
        cur_energy = 0.0
        for lam, e in zip(eigvals_sorted, energy):
            if cur_eig is None or abs(lam - cur_eig) > 1e-6:
                if cur_eig is not None:
                    levels.append((cur_eig, cur_energy))
                cur_eig = lam
                cur_energy = e
            else:
                cur_energy += e
        if cur_eig is not None:
            levels.append((cur_eig, cur_energy))

        total_energy = sum(e for _, e in levels)
        level_rows = [
            {
                "lambda": float(lam),
                "gap": float(1 - lam),
                "energy": float(e),
                "frac_of_var": float(e / total_energy) if total_energy > 0 else 0.0,
            }
            for lam, e in levels
            if abs(lam - 1.0) > 1e-9  # drop the trivial (constant) eigenspace
        ]
        level_rows.sort(key=lambda r: -r["frac_of_var"])

        rows.append(
            {
                "q": q,
                "N": big_n,
                "C_q": c_q,
                "total_energy_check": total_energy,  # should equal C_q (Parseval)
                "n_distinct_levels": len(level_rows),
                "levels": level_rows,
            }
        )
        top = level_rows[0] if level_rows else None
        print(
            f"  q={q:2d}/{big_n:2d}  C_q={c_q:.6f}  Parseval_check={total_energy:.6f}  "
            f"n_levels={len(level_rows)}  top_level: gap={top['gap']:.4f} "
            f"frac={top['frac_of_var']:.4f}"
            if top
            else "  (no levels)"
        )
    return rows


def run(n_values: list[int]) -> dict:
    out = {}
    for n in n_values:
        print(f"\n--- n={n} ---", flush=True)
        out[n] = layer_decomposition(n)
    return out


if __name__ == "__main__":
    result = run([23, 29, 31])
    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "johnson_eigenspace_decomposition.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
