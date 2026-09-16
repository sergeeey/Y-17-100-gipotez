"""Coordinator-requested paired forensic diff (Task 1 addendum): for each of a set of
n=127 seeds, build BOTH the v3 (canonical, current) construction AND each v1-reconstruction
candidate (H1: post-hoc bit overwrite: H2: sequential draw skipping gen_index's rng call --
see diagnose_v1_v3.py for the full hypothesis writeups) and walk the SAME computation chain
step by step:

    seed -> G0 bits -> G1 bits -> complement(G1) bits
         -> theta(G0) -> theta(G1) -> theta(complement(G1))
         -> x_i -> w_i -> Z = n*x_i*w_i -> Z^2

For each seed and each hypothesis, report the FIRST field in this chain where the
hypothesis's value differs from v3's (bit arrays compared exactly; scalars compared at
1e-9 absolute/relative tolerance). This is the actual diagnosis asked for -- not just
"the final J_n differs" but "here is where in the pipeline it first differs."

Read-only on ppl_gate_pilot.py and codex-20260914-susceptibility/ (imports only).
Does not modify decision.md, registry, or commit anything.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from ppl_gate_pilot import (  # noqa: E402
    GEN_INDEX,
    SEED_BASE,
    CertificateLP,
    flip_generator,
    sample_circulant_neighbors,
)

N = 127
N_SEEDS = 25  # coordinator: "первые 20-30 из уже используемой seed-схемы"
ATOL = 1e-9


def seeds_for(n: int, reps: int) -> list[int]:
    return [SEED_BASE + n * 100_000 + rep for rep in range(reps)]


def v3_chain(lp: CertificateLP, n: int, seed: int, gen_index: int) -> dict:
    """The actual, current, canonical construction (identical logic to
    ppl_gate_pilot.one_case), returning every intermediate object in the chain."""
    m = lp.m
    c = sample_circulant_neighbors(n, 0.5, seed)
    c_flip = flip_generator(c, gen_index)
    if c[gen_index] < 0.5:
        branch = "A"
        c_g0, c_g1 = c, c_flip
    else:
        branch = "B"
        c_g0, c_g1 = c_flip, c
    bits_g0 = c_g0[1 : m + 1].astype(int)
    bits_g1 = c_g1[1 : m + 1].astype(int)
    bits_comp = 1 - bits_g1

    g0 = lp.solve(bits_g0)
    g1 = lp.solve(bits_g1)
    comp = lp.solve(bits_comp)

    x_i = float(g0["x"][gen_index])
    w_i = float(comp["x"][gen_index])
    z = n * x_i * w_i
    return {
        "branch": branch,
        "bits_g0": bits_g0,
        "bits_g1": bits_g1,
        "bits_comp": bits_comp,
        "theta_g0": float(g0["theta"]),
        "theta_g1": float(g1["theta"]),
        "theta_comp": float(comp["theta"]),
        "x_i": x_i,
        "w_i": w_i,
        "Z": z,
        "Z2": z**2,
    }


def h1_chain(lp: CertificateLP, n: int, seed: int, gen_index: int) -> dict:
    """H1: same vectorized draw as v3, post-hoc overwrite bit[gen_index]=0 for G0,
    =1 for G1 (see diagnose_v1_v3.py case_h1 for the full rationale)."""
    m = lp.m
    c = sample_circulant_neighbors(n, 0.5, seed)  # IDENTICAL call to v3
    bits_g0 = c[1 : m + 1].astype(int).copy()
    bits_g0[gen_index - 1] = 0
    bits_g1 = bits_g0.copy()
    bits_g1[gen_index - 1] = 1
    bits_comp = 1 - bits_g1

    g0 = lp.solve(bits_g0)
    g1 = lp.solve(bits_g1)
    comp = lp.solve(bits_comp)

    x_i = float(g0["x"][gen_index])
    w_i = float(comp["x"][gen_index])
    z = n * x_i * w_i
    return {
        "bits_g0": bits_g0,
        "bits_g1": bits_g1,
        "bits_comp": bits_comp,
        "theta_g0": float(g0["theta"]),
        "theta_g1": float(g1["theta"]),
        "theta_comp": float(comp["theta"]),
        "x_i": x_i,
        "w_i": w_i,
        "Z": z,
        "Z2": z**2,
    }


def sample_sequential_skip(n: int, p: float, seed: int, gen_index: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    c = np.zeros(n, dtype=float)
    half = (n - 1) // 2
    for k in range(1, half + 1):
        if k == gen_index:
            continue
        if rng.random() < p:
            c[k] = 1.0
            c[n - k] = 1.0
    return c


def h2_chain(lp: CertificateLP, n: int, seed: int, gen_index: int) -> dict:
    """H2: sequential draw, SKIPPING the rng call for gen_index entirely (stream-shifted
    relative to v3 for every OTHER bit -- see diagnose_v1_v3.py case_h2)."""
    m = lp.m
    c = sample_sequential_skip(n, 0.5, seed, gen_index)
    bits_g0 = c[1 : m + 1].astype(int).copy()
    bits_g1 = bits_g0.copy()
    bits_g1[gen_index - 1] = 1
    bits_comp = 1 - bits_g1

    g0 = lp.solve(bits_g0)
    g1 = lp.solve(bits_g1)
    comp = lp.solve(bits_comp)

    x_i = float(g0["x"][gen_index])
    w_i = float(comp["x"][gen_index])
    z = n * x_i * w_i
    return {
        "bits_g0": bits_g0,
        "bits_g1": bits_g1,
        "bits_comp": bits_comp,
        "theta_g0": float(g0["theta"]),
        "theta_g1": float(g1["theta"]),
        "theta_comp": float(comp["theta"]),
        "x_i": x_i,
        "w_i": w_i,
        "Z": z,
        "Z2": z**2,
    }


CHAIN_FIELDS = [
    "bits_g0",
    "bits_g1",
    "bits_comp",
    "theta_g0",
    "theta_g1",
    "theta_comp",
    "x_i",
    "w_i",
    "Z",
    "Z2",
]


def first_divergence(v3: dict, hyp: dict) -> str | None:
    """Walk CHAIN_FIELDS IN ORDER, return the name of the first field that differs
    (arrays: exact elementwise equality; scalars: abs+rel tolerance ATOL), or None if
    the two chains are identical end to end."""
    for field in CHAIN_FIELDS:
        a, b = v3[field], hyp[field]
        if isinstance(a, np.ndarray):
            if not np.array_equal(a, b):
                return field
        else:
            if abs(a - b) > ATOL + ATOL * abs(a):
                return field
    return None


def main() -> None:
    n = N
    seeds = seeds_for(n, N_SEEDS)
    lp = CertificateLP(n)
    gen_index = GEN_INDEX

    per_seed = []
    first_div_counts = {"H1": {}, "H2": {}}

    for seed in seeds:
        v3 = v3_chain(lp, n, seed, gen_index)
        h1 = h1_chain(lp, n, seed, gen_index)
        h2 = h2_chain(lp, n, seed, gen_index)

        div_h1 = first_divergence(v3, h1)
        div_h2 = first_divergence(v3, h2)

        first_div_counts["H1"][div_h1 or "IDENTICAL"] = (
            first_div_counts["H1"].get(div_h1 or "IDENTICAL", 0) + 1
        )
        first_div_counts["H2"][div_h2 or "IDENTICAL"] = (
            first_div_counts["H2"].get(div_h2 or "IDENTICAL", 0) + 1
        )

        per_seed.append(
            {
                "seed": seed,
                "v3_branch": v3["branch"],
                "v3_Z": v3["Z"],
                "H1_first_divergence": div_h1 or "IDENTICAL (no divergence end-to-end)",
                "H1_Z": h1["Z"],
                "H2_first_divergence": div_h2 or "IDENTICAL (no divergence end-to-end)",
                "H2_Z": h2["Z"],
            }
        )

    print(f"=== Paired forensic diff, n={n}, {N_SEEDS} seeds ===\n")
    print(
        f"{'seed':>12} {'br':>2} {'v3_Z':>10} {'H1 first-diverge':>28} {'H1_Z':>10} "
        f"{'H2 first-diverge':>18} {'H2_Z':>10}"
    )
    for row in per_seed:
        print(
            f"{row['seed']:>12} {row['v3_branch']:>2} {row['v3_Z']:>10.4f} "
            f"{row['H1_first_divergence']:>28} {row['H1_Z']:>10.4f} "
            f"{row['H2_first_divergence']:>18} {row['H2_Z']:>10.4f}"
        )

    print("\n=== First-divergence field tally across all seeds ===")
    print("H1 (post-hoc overwrite):", first_div_counts["H1"])
    print("H2 (sequential skip, stream-shifted):", first_div_counts["H2"])

    print("\n=== Diagnosis ===")
    if first_div_counts["H1"].get("IDENTICAL", 0) == len(seeds):
        print(
            "H1: the chain NEVER diverges from v3, at ANY step, for ANY of the "
            f"{len(seeds)} tested seeds -- G0/G1/complement bits, all three thetas, x_i, "
            "w_i, Z, Z^2 are bit-for-bit / numerically identical throughout. This is a "
            "STRUCTURAL result, not a coincidence of these particular seeds: H1's "
            "'post-hoc overwrite bit[gen_index]=0' is algebraically the SAME operation as "
            "v3's branch-conditional flip_generator call (forcing an already-0 bit to 0 is "
            "a no-op; forcing an already-1 bit to 0 is exactly what flip_generator does). "
            "H1 is therefore REJECTED as an explanation for the discrepancy -- not merely "
            "'doesn't match empirically' but 'cannot produce a different graph at all, by "
            "construction'."
        )
    else:
        print("H1: chain diverges on some seeds -- see tally above (unexpected; re-check).")

    h2_first_fields = {k for k in first_div_counts["H2"] if k != "IDENTICAL"}
    if h2_first_fields:
        print(
            f"H2: diverges at {sorted(h2_first_fields)} -- i.e. at the level of the RAW BIT "
            "ARRAYS themselves (G0/G1/complement), before any LP is even solved. This "
            "confirms the divergence mechanism for H2 is in graph CONSTRUCTION / RNG "
            "stream consumption, not in the optimizer or in aggregation code -- consistent "
            "with the earlier aggregate result (diagnose_v1_v3.py) that H2 gives J_n(127)"
            "~73.7, still far from v1's reported 5.9, ruling H2 out too as a full "
            "explanation even though it does produce genuinely different graphs."
        )
    else:
        print("H2: never diverges either (unexpected; re-check sample_sequential_skip).")

    out = {
        "n": n,
        "n_seeds": N_SEEDS,
        "chain_fields_in_order": CHAIN_FIELDS,
        "atol": ATOL,
        "first_divergence_tally": first_div_counts,
        "per_seed": [
            {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in row.items()}
            for row in per_seed
        ],
    }
    out_path = HERE / "metrics" / "forensic_diff_v1_v3_result.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
