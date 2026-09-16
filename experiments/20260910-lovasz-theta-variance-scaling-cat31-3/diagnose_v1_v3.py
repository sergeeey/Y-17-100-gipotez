"""Diagnostic script for the UNRESOLVED ~11x discrepancy between the very first
(now-lost) v1 draft of the PPL_gate pilot and the final canonical v3 at n=127
(v1 reported J_n(127)=5.9, v3 reports J_n(127)=64.66) -- decision.md Point 66,
Errors #1 / Kill Analysis #3.

This does NOT modify ppl_gate_pilot.py. It reuses (read-only, via import) its
already-verified building blocks: CertificateLP, sample_circulant_neighbors,
flip_generator, GEN_INDEX, SEED_BASE -- and reimplements two CANDIDATE
reconstructions of what v1 might have actually done (its source code no
longer exists), then checks which one, if either, reproduces J_n(127)~=5.9.

Hypotheses tested (see task brief):
  H1 -- v1 drew the SAME m bits from sample_circulant_neighbors(n,0.5,seed) as
        v3 (one vectorized rng.random(half) call), then POST-HOC overwrote
        bits[gen_index-1] to 0. Because the RNG draw already happened as one
        batch, this does NOT shift the stream for any other bit -- confirmed
        empirically in this script's own RNG-equivalence check below (numpy
        Generator.random() is stream-order-consistent: rng.random(k) then
        rng.random(j) == rng.random(k+j) elementwise on the same seed).
        Skeptic's algebraic argument (flip_generator only ever touches one
        bit) applies to H1 verbatim: under H1, forcing bit=0 is ALGEBRAICALLY
        IDENTICAL to flip_generator's effect (no-op if already 0, single-bit
        toggle if it was 1) -- so H1 predicts v1's G0 is bit-for-bit IDENTICAL
        to v3's G0 for every seed, for BOTH branches. If H1 is what happened,
        v1 should reproduce v3's J_n almost exactly (mod possibly different
        G1/complement construction -- also checked here, both use v3's own
        "w = certificate of complement(G1), G1 = G0 with tested bit flipped
        on" pairing, matching Point 63).
  H2 -- v1 built c SEQUENTIALLY (one rng.random() draw per k=1..half), and
        literally SKIPPED consuming a random draw for k=gen_index (matching
        the docstring's own "forced bits[0]=0 ... before drawing the rest"
        wording, which reads as sequential construction, not a vectorized
        draw-then-overwrite). Because numpy's Generator.random() stream is
        order-consistent (verified below), skipping position gen_index's draw
        SHIFTS every subsequent bit's value relative to v3's vectorized
        picks array -- i.e. under H2, v1's bit for k=(gen_index+1) equals
        v3's raw draw value for k=gen_index, and so on, producing a
        genuinely DIFFERENT graph (not merely one bit different) for every
        seed where v3's raw c[gen_index] happened to be nonzero at any
        downstream position -- in fact for every seed, since all of bits
        2..half get relabeled.
  H3 -- the tested coordinate itself was different (index confusion between
        "bits[0]" prose and "gen_index=1" code). Tested by sweeping several
        FIXED gen_index values through v3's own correct (honest, both
        branches) construction and checking how much J_n(127) varies with
        the choice of coordinate.

Output: printed report + JSON dump to metrics/diagnose_v1_v3_result.json.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# Reuse (read-only import) the already-verified v3 building blocks.
from ppl_gate_pilot import (  # noqa: E402
    GEN_INDEX,
    SEED_BASE,
    CertificateLP,
    flip_generator,
    sample_circulant_neighbors,
)

N = 127
FULL_REPS = 500  # matches v3's own n=127 budget exactly (Errors: "same seeds as v3")
SEED_SCHEME_NOTE = "SEED_BASE + n*100_000 + rep -- identical to ppl_gate_pilot.py's own scheme"


def seeds_for(n: int, reps: int) -> list[int]:
    return [SEED_BASE + n * 100_000 + rep for rep in range(reps)]


# ---------------------------------------------------------------------------
# RNG stream-order-consistency check (must hold for the H1 vs H2 distinction
# to even be well-posed -- verified once here, printed, not assumed).
# ---------------------------------------------------------------------------
def check_rng_stream_consistency(seed: int, k: int) -> bool:
    rng_bulk = np.random.default_rng(seed)
    bulk = rng_bulk.random(k)
    rng_seq = np.random.default_rng(seed)
    seq = np.array([rng_seq.random() for _ in range(k)])
    rng_split = np.random.default_rng(seed)
    _ = rng_split.random(1)
    rest = rng_split.random(k - 1)
    return bool(np.array_equal(bulk, seq)) and bool(np.array_equal(bulk[1:], rest))


# ---------------------------------------------------------------------------
# H1: same vectorized draw as v3, post-hoc overwrite bits[gen_index-1] = 0.
# ---------------------------------------------------------------------------
def case_h1(lp: CertificateLP, n: int, seed: int, gen_index: int) -> dict:
    m = lp.m
    c = sample_circulant_neighbors(n, 0.5, seed)  # IDENTICAL call to v3
    bits_g0 = c[1 : m + 1].astype(int).copy()
    bits_g0[gen_index - 1] = 0  # forced absent, post-hoc, no RNG re-draw
    bits_g1 = bits_g0.copy()
    bits_g1[gen_index - 1] = 1  # "S union {i}"

    g0 = lp.solve(bits_g0)
    comp = lp.solve(1 - bits_g1)  # complement(G1), same pairing as v3/Point 63
    x_i = float(g0["x"][gen_index])
    w_i = float(comp["x"][gen_index])
    return {"seed": seed, "x_i": x_i, "w_i": w_i, "Z": n * x_i * w_i}


# ---------------------------------------------------------------------------
# H2: sequential draw, SKIP the rng call for k=gen_index entirely (shifts
# every other bit's value relative to v3's vectorized draw).
# ---------------------------------------------------------------------------
def sample_sequential_skip(n: int, p: float, seed: int, gen_index: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    c = np.zeros(n, dtype=float)
    half = (n - 1) // 2
    for k in range(1, half + 1):
        if k == gen_index:
            continue  # forced absent -- NO random draw consumed here
        if rng.random() < p:
            c[k] = 1.0
            c[n - k] = 1.0
    return c


def case_h2(lp: CertificateLP, n: int, seed: int, gen_index: int) -> dict:
    m = lp.m
    c = sample_sequential_skip(n, 0.5, seed, gen_index)
    bits_g0 = c[1 : m + 1].astype(int).copy()
    assert bits_g0[gen_index - 1] == 0
    bits_g1 = bits_g0.copy()
    bits_g1[gen_index - 1] = 1

    g0 = lp.solve(bits_g0)
    comp = lp.solve(1 - bits_g1)
    x_i = float(g0["x"][gen_index])
    w_i = float(comp["x"][gen_index])
    return {"seed": seed, "x_i": x_i, "w_i": w_i, "Z": n * x_i * w_i}


# ---------------------------------------------------------------------------
# H3: v3's own correct (honest, both-branch) construction, swept over several
# FIXED alternate coordinates instead of gen_index=1.
# ---------------------------------------------------------------------------
def case_h3(lp: CertificateLP, n: int, seed: int, gen_index: int) -> dict:
    m = lp.m
    c = sample_circulant_neighbors(n, 0.5, seed)
    c_flip = flip_generator(c, gen_index)
    if c[gen_index] < 0.5:
        c_g0, c_g1 = c, c_flip
    else:
        c_g0, c_g1 = c_flip, c
    bits_g0 = c_g0[1 : m + 1].astype(int)
    bits_g1 = c_g1[1 : m + 1].astype(int)
    g0 = lp.solve(bits_g0)
    comp = lp.solve(1 - bits_g1)
    x_i = float(g0["x"][gen_index])
    w_i = float(comp["x"][gen_index])
    return {"seed": seed, "x_i": x_i, "w_i": w_i, "Z": n * x_i * w_i}


def summarize(zs: list[float]) -> dict:
    z = np.array(zs)
    z2 = z**2
    j_n = float(z2.mean())
    se = float(z2.std(ddof=1) / np.sqrt(len(z2))) if len(z2) > 1 else float("nan")
    return {
        "reps": len(zs),
        "J_n": j_n,
        "J_n_SE": se,
        "mean_Z": float(z.mean()),
        "median_Z": float(np.median(z)),
    }


def run_hypothesis(
    label: str, fn, lp: CertificateLP, n: int, seeds: list[int], gen_index: int
) -> dict:
    started = time.monotonic()
    zs = []
    for i, seed in enumerate(seeds):
        row = fn(lp, n, seed, gen_index)
        zs.append(row["Z"])
        if (i + 1) % 100 == 0:
            print(
                f"  [{label}] {i + 1}/{len(seeds)} done, elapsed={time.monotonic() - started:.1f}s",
                flush=True,
            )
    summary = summarize(zs)
    summary["elapsed_seconds"] = time.monotonic() - started
    print(
        f"  [{label}] FINAL: J_n={summary['J_n']:.3f} SE={summary['J_n_SE']:.3f} "
        f"(reps={summary['reps']}, {summary['elapsed_seconds']:.1f}s)",
        flush=True,
    )
    return summary


def main() -> None:
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else FULL_REPS
    n = N
    seeds = seeds_for(n, reps)
    lp = CertificateLP(n)

    print("=== RNG stream-order-consistency check ===")
    consistent = check_rng_stream_consistency(seeds[0], lp.m)
    print(
        f"numpy Generator.random() is stream-order-consistent (bulk==sequential=="
        f"split): {consistent}"
    )
    print(
        "This means H2 (skip-then-draw-rest, sequential) produces a GENUINELY "
        "different bit sequence than H1 (draw-all-then-overwrite) for every "
        "downstream bit, not just the forced one.\n"
    )

    print(f"=== n={n}, reps={reps} (target: v1's J_n(127)=5.9, v3's J_n(127)=64.66) ===\n")

    results = {}

    print(">>> H1: same vectorized draw as v3, post-hoc overwrite bit[gen_index]=0")
    results["H1_posthoc_overwrite"] = run_hypothesis("H1", case_h1, lp, n, seeds, GEN_INDEX)

    print("\n>>> H2: sequential draw, SKIP the rng call for gen_index (stream-shifted)")
    results["H2_sequential_skip"] = run_hypothesis("H2", case_h2, lp, n, seeds, GEN_INDEX)

    print("\n>>> H3: v3's correct construction, swept over alternate fixed coordinates")
    h3_indices = [1, 2, 3, 5, 10, 20, 40, 63]  # 1=GEN_INDEX (v3 canonical), 63=lp.m (n=127 -> m=63)
    h3_results = {}
    for idx in h3_indices:
        label = f"H3_gen_index={idx}"
        h3_results[str(idx)] = run_hypothesis(label, case_h3, lp, n, seeds, idx)
    results["H3_coordinate_sweep"] = h3_results

    print("\n=== SUMMARY ===")
    target_v1 = 5.9
    target_v3 = 64.66
    print(f"Target v1 J_n(127) ~= {target_v1}, target v3 J_n(127) ~= {target_v3}\n")
    for label, key in [("H1", "H1_posthoc_overwrite"), ("H2", "H2_sequential_skip")]:
        j = results[key]["J_n"]
        se = results[key]["J_n_SE"]
        ratio_to_v1 = j / target_v1
        ratio_to_v3 = j / target_v3
        within_2x_v1 = 0.5 <= ratio_to_v1 <= 2.0
        print(
            f"{label}: J_n={j:.2f}+-{se:.2f}  ratio-to-v1(5.9)={ratio_to_v1:.2f}  "
            f"ratio-to-v3(64.66)={ratio_to_v3:.2f}  within-2x-of-v1={within_2x_v1}"
        )

    print("\nH3 coordinate sweep (v3-correct construction, varying which coordinate is tested):")
    for idx, s in h3_results.items():
        j = s["J_n"]
        ratio_to_v1 = j / target_v1
        print(
            f"  gen_index={idx}: J_n={j:.2f}+-{s['J_n_SE']:.2f}  ratio-to-v1(5.9)={ratio_to_v1:.2f}"
        )

    out = {
        "n": n,
        "reps": reps,
        "seed_scheme": SEED_SCHEME_NOTE,
        "rng_stream_order_consistent": consistent,
        "target_v1_J_n_127": target_v1,
        "target_v3_J_n_127": target_v3,
        "results": results,
    }
    out_path = HERE / "metrics" / "diagnose_v1_v3_result.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
