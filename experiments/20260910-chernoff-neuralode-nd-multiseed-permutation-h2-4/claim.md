# claim.md — 20260910-chernoff-neuralode-nd-multiseed-permutation-h2-4

**Graph node:** `H-B2-4` (bridge `B2-CHERNOFF-NEURALODE`) · **Tier:** Standard
**Parent:** `H-B2-1k` (status `lead`, `CRITERION_INVALID` — the original single-seed sign-change
kill criterion is passed by pure noise with probability ~0.999994, and its own 9 sweep points
were a single deterministic-seed curve, not independent draws). `H-B2-1k`'s own `kill_criterion`
field, verbatim: "needs a multi-seed x multi-N grid with a permutation-test criterion instead" —
this experiment is that exact, previously-named, never-attempted fix.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** "Does `M1(N_DIM)`, at a fixed spectral range, show genuine
across-seed-robust non-monotonic structure as a function of `N_DIM`, beyond what seed-to-seed
noise alone would produce?" No causal claim — `N_DIM` is a construction parameter of a synthetic
matrix family, not an intervention on a real system.

## Origin — closing a real, previously-identified statistical gap, not a fresh guess

`H-B2-1k`'s own decision.md (FL Step 8a skeptic pass, third in a row that session) found two
compounding flaws in the original single-seed sweep: (1) the sign-change kill criterion is passed
by pure noise with near-certainty for 9 points (`P(>=1 sign change | iid noise) ~= 0.999994`,
computed exactly: only 2 of `9! = 362880` orderings are monotonic); (2) each of the 9 sweep points
used `build_matrix`'s own hardcoded `SEED=0`, re-seeded fresh inside the function on every call —
meaning the 9 points were NOT one coherent system probed at 9 dimensions with consistent noise,
but 9 structurally independent random draws sharing only a spectral-range convention. Both
flaws are fixed here: (1) a permutation-test null model replaces the naive sign-change count;
(2) multiple independent seeds are averaged per `N_DIM`, and the SAME per-seed matrix family is
reused across seeds (not re-derived).

**Minimal Relaxation Rule compliance:** ONE change relative to `H-B2-1k` — single-seed becomes
multi-seed with a proper permutation null, everything else (`SPECTRAL_RANGE`, `N_DIM_VALUES`,
`COUPLING_MAGNITUDE`, `T_MAX`, `W`, `measure_m1`'s own formula) reused byte-identical.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "for 9 iid continuous draws, only 2 of `9! = 362880` orderings are
monotonic, so a bare sign-change criterion is passed by pure noise with near-certainty" — this is
`H-B2-1k`'s own already-verified finding (a closed-form combinatorial fact: exactly 2 of `n!`
permutations of `n` distinct reals are monotonic, for any `n >= 2`), reused unchanged, not
re-derived.

## Compute-First Check (done before committing to the full N_SEEDS sweep)

A scratchpad timing diagnostic (3 seeds x 9 N values = 27 matrix-builds + M1 measurements) ran in
~14.5s, ~540ms per (seed, N) pair — extrapolating to 30 seeds x 9 N = 270 pairs gives ~145s,
tractable directly (no new infrastructure, no GPU, pure numpy/scipy `expm`, already the same cost
profile every prior H-B2-1* experiment used).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `M1(N_DIM)` (the same finite-horizon transient-growth ratio measured identically throughout the whole B2 arc) at 9 fixed `N_DIM` values, each measured across 30 independent seeds |
| **Falsifiable predicate** | Does the seed-averaged `M1(N_DIM)` curve show MORE sign changes in its consecutive differences than a permutation null model (which destroys any true `N_DIM`-dependence but preserves each seed's own value distribution) would produce by chance? |
| **Measurable outcome** | Observed sign-change count on the seed-averaged curve, compared against a permutation-null distribution (2000 permutations), reported as a one-sided p-value |

## Kill Criterion (set BEFORE running)

- **CONFIRMED (real non-monotonic structure):** `p < 0.05` — the observed sign-change count on
  the seed-averaged curve is a significant outlier relative to the permutation null.
- **REJECTED (no detectable non-monotonic structure beyond noise):** `p >= 0.05`.
- **Substrate/positive-control note:** the permutation null is constructed by, independently per
  seed, randomly reassigning that seed's own 9 `M1` values to the 9 `N_DIM` labels (a within-seed
  permutation) — this destroys any TRUE dependence on `N_DIM` while preserving each seed's own
  value distribution exactly, giving a legitimate null model for "no real N-dependent effect."

## What This Does NOT Mean

1. Does NOT claim a mechanism for any confirmed non-monotonicity (e.g. eigenvector-conditioning,
   per `H-B2-1l`'s own sharper hypothesis) — this experiment only tests EXISTENCE of the pattern
   with proper statistics, not its cause.
2. Does NOT extend `N_DIM_VALUES` or `SPECTRAL_RANGE` beyond `H-B2-1k`'s own original choices —
   reused unchanged, per Minimal Relaxation Rule (one change: seeds, not the sweep grid itself).
3. Bridge 2 (`B2-CHERNOFF-NEURALODE`) is documented elsewhere as its main arc's own status —
   this experiment closes ONE specific, previously-flagged statistical loose end within that arc
   (`H-B2-1k`'s own named, never-executed fix), not a new bridge-level claim.

## MCID

Not pre-registered as a separate practical-significance bar — the permutation-test p-value IS the
pre-registered decision criterion (statistical, not practical, significance is the question here,
matching `H-B2-1k`'s own original framing).
