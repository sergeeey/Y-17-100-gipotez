# claim.md — 20260906-chernoff-neuralode-nd-strong-coupling

**Graph node:** `H-B2-1g` (new, per Minimal Relaxation Rule) · **Bridge:** `B2-CHERNOFF-UDE` · **Tier:** Standard
**Parent:** `H-B2-1f` (N=8, weak coupling `[-3,3]`, CONFIRMED — counterintuitive: M1 smaller than N=2 case)

> **Role of this experiment:** ONE assumption changed from `H-B2-1f`: coupling magnitude
> (`[-3,3]` → `[-15,15]`, 5x). Directly tests whether `H-B2-1f`'s counterintuitive finding (M1 at N=8
> smaller than at N=2) was an artifact of weak coupling, or a genuine property of this construction —
> named explicitly as the next step in `H-B2-1f`'s own decision.md.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Same 8x8 upper-triangular structure and eigenvalues as `H-B2-1f`, but off-diagonal coupling drawn from `[-15,15]` instead of `[-3,3]` (same seed) |
| **Falsifiable predicate** | With stronger coupling, does `M1` at N=8 now EXCEED the N=2 combined value (`H-B2-1e`: 3.806), reversing `H-B2-1f`'s counterintuitive finding, or does it remain smaller/comparable, suggesting the earlier finding is robust to coupling strength, not just an artifact of weak coupling? |
| **Measurable outcome** | Measured `M1` at strong coupling vs. `H-B2-1f`'s weak-coupling value (2.665) and `H-B2-1e`'s N=2 value (3.806); bound validity and order-matching at both block orders |

## Natural Language Statement

> "We test whether H-B2-1f's counterintuitive finding (M1 at N=8 smaller than at N=2) survives a 5x
> increase in coupling magnitude, or whether it was specific to the weak-coupling regime tested there."

## L0 Classification

**Descriptive**, unchanged from the `H-B2-1*` family.

## What This Does NOT Mean

1. Does NOT test multiple random seeds — single seed, as in `H-B2-1f`; a seed-sensitivity study is a
   separate, further step if this one is informative.
2. A finding that M1 now DOES exceed the N=2 value would NOT contradict `H-B2-1f` — it would show the
   earlier finding was coupling-strength-dependent, itself an informative result, not an error.

## MCID

Same bar as the rest of the family: finite `(M1, M2)` found, bound holds for all tested `n`, efficiency
stable across `n`, for both block orders.
