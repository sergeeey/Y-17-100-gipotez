# claim.md — 20260907-chernoff-neuralode-nd-scale

**Graph node:** `H-B2-1j` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard
**Parent:** `H-B2-1g` (LAB.md's own open-items list after the 7-confirmation `H-B2-1*` series:
"систематический скан коэффициента связи [done: `H-B2-1h`], множественные seed [done: `H-B2-1i`],
**N=50+**" — the one remaining named-but-untested dimension.)

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Same framing as every prior `H-B2-1*` experiment: does a
formally valid, order-matching Chernoff-type bound continue to hold and match order at a NEW,
larger fixed dimensionality — not an intervention, not a causal claim.

## Why This Experiment, Specifically

Every `H-B2-1*` experiment to date (`a` through `i`) used `N_DIM ∈ {1, 2, 8}`. `H-B2-1f→H-B2-1g`
already found dimensionality does NOT monotonically increase practical difficulty in an obvious
way (M1 at N=8, weak coupling, was SMALLER than at N=2) — but this was tested at only two small
dimensions. Whether the bound's VALIDITY and ORDER-MATCHING survive a substantially larger
dimension (N=50) — where numerical conditioning, matrix-power accumulation error, and transient
growth all have more room to compound — has never been tested.

## Scope Decision — Explicit

`COUPLING_MAGNITUDE=15.0` (matching `H-B2-1g`'s own tested value, NOT `H-B2-1f`'s weaker 3.0) and
`SEED=0` (matching every prior `H-B2-1*` experiment) are held FIXED. Per the Minimal Relaxation
Rule, only `N_DIM` changes (8 → 50) relative to `H-B2-1g`. The eigenvalue spectrum is extended in
the SAME spirit as every prior construction (one positive growing mode, many negative decaying
modes spanning a wide range) rather than a qualitatively different spectrum shape.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Theorem 3.1's bound and its empirical convergence order, evaluated on a NEW `N_DIM=50` stiff linear ODE construction (one positive eigenvalue 0.5, 49 negative eigenvalues linearly spaced `[-1, -50]`, random upper-triangular coupling `U(-15,15)`, seed=0 — otherwise identical construction to every prior `H-B2-1*` experiment) |
| **Falsifiable predicate** | The bound holds for ALL tested step counts `n ∈ {50,...,6400}` for BOTH order-1 and order-2 block methods, AND the empirical convergence order matches the theoretical order (1 and 2 respectively) as tightly as it did at `N_DIM=8` (`H-B2-1g`: 1.0026, 2.0007) |
| **Measurable outcome** | `mechanism_holds_strong_coupling` (bool), `empirical_order_estimate` for both orders, `M1` at N=50 vs. N=8's 158.93 (does the transient-growth constant grow further with dimension at fixed coupling, or not — informs whether `H-B2-1f`'s counterintuitive N=2→N=8 shrinkage was a fluke of small N or a real pattern) |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md` / `null_results/INDEX.md`: no prior `H-B2-1*` experiment at
`N_DIM > 8`. Confirmed genuinely untested, matching LAB.md's own open-items list.

## Kill Criterion (set BEFORE running)

- **CONFIRMED:** bound holds for ALL tested `n` at BOTH orders, AND empirical order is within
  10% of the theoretical value (1.0 and 2.0) — matching the standard used in every prior
  `H-B2-1*` verdict.
- **REJECTED:** the bound fails at any tested `n`, OR the empirical order deviates by more than
  10% from theoretical — would indicate the mechanism's validity is dimension-sensitive in a way
  not previously observed.

## What This Does NOT Mean

1. Does NOT generalize beyond this SPECIFIC eigenvalue-spread convention and coupling magnitude
   — a qualitatively different N=50 spectrum (e.g. clustered eigenvalues, complex pairs) could
   behave differently.
2. Does NOT imply anything about real Neural-ODE/ResNet layers of comparable width — a
   controlled numerical experiment on a toy stiff system, per every prior `H-B2-1*` scope limit.
3. A CONFIRMED verdict here would NOT retroactively strengthen `H-B2-1g`'s own "formally valid,
   practically vacuous" finding (efficiency ~1.5e-7 at N=8) — this experiment does not measure
   efficiency at N=50 as its primary question, though the M1 comparison is informative for it.

## MCID

Whether `mechanism_holds_strong_coupling` remains true at N=50 (matching all 9 prior `H-B2-1*`
confirmations) — a binary fact, not a continuous threshold.
