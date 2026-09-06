# claim.md — 20260906-chernoff-neuralode-2d-combined-stress

**Graph node:** `H-B2-1e` (new, per Minimal Relaxation Rule — see note below) · **Bridge:** `B2-CHERNOFF-UDE` · **Tier:** Standard
**Parents:** `H-B2-1c` (non-normal, CONFIRMED) and `H-B2-1d` (mixed-sign spectrum, CONFIRMED)

> **Role of this experiment:** combines the TWO previously-and-separately-confirmed generalizations
> (non-normality from `H-B2-1c`, mixed-sign spectrum from `H-B2-1d`) into ONE test — the natural
> completion of the `H-B2-1*` stress-test arc, closer to a realistic Neural-ODE/ResNet Jacobian (which
> the literature cited in `H-B2-1d`'s claim.md says is BOTH non-normal in general AND can have unstable
> directions). This is a deliberate exception to strict Minimal-Relaxation single-assumption changes:
> two ALREADY-INDIVIDUALLY-CONFIRMED axes are combined to test for an INTERACTION EFFECT, not two new,
> individually-untested assumptions at once — the interaction question itself is the falsifiable target.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `A = [[0.5, 10], [0, -2]]` — upper-triangular (non-normal, per `H-B2-1c`'s construction), eigenvalues `+0.5` (growth, per `H-B2-1d`) and `-2` (decay) |
| **Falsifiable predicate** | The `K_j=0` mechanism survives BOTH complications simultaneously — non-normality (numerically-measured `M1`/`M2`, no closed-form shortcut) AND growth (`w>0` required) — without a qualitatively new failure mode appearing only under their combination |
| **Measurable outcome** | Numerically-measured `M1`, `M2` (via `scipy.linalg.expm`, no symmetry shortcut available here); bound vs. true empirical error, order-1/order-2 blocks |

## Why This Combination, Not a Further Escalation

`H-B2-1c` tested non-normality alone (both eigenvalues decaying). `H-B2-1d` tested mixed sign alone
(matrix symmetric, so `M1=M2=1` provably). Neither tested WHETHER non-normality and growth interact
badly together — e.g. a non-normal matrix's transient growth (already measured `~2.56x` in `H-B2-1c`)
could plausibly COMPOUND with the genuine exponential growth from the positive eigenvalue, producing a
much worse `M1`/`M2` than either effect alone would suggest, or (more concerning) could break the
straightforward `w` choice that worked cleanly in `H-B2-1d`. This is exactly the kind of interaction a
real Neural-ODE/ResNet Jacobian would present (both non-normal AND partially unstable), and finding out
now, cheaply, is more informative than either escalating an already-tested single axis (arbitrary) or
stopping the `H-B2-1*` arc without checking the two known complications together.

## FL Step -4: Source Trace

Unchanged from `H-B2-1c`/`H-B2-1d` — Theorem 3.1 and the literature motivating non-normality/instability
are already source-traced there; no new citations needed for this combination test.

## Natural Language Statement

> "We test whether the K_j=0/Theorem 3.1 mechanism survives the COMBINATION of non-normality and a
> mixed-sign (growing+decaying) spectrum, checking for an interaction effect beyond what either
> complication alone (H-B2-1c, H-B2-1d) showed."

## L0 Classification

**Descriptive**, unchanged from the `H-B2-1*` family.

## What This Does NOT Mean

1. Does NOT test a higher-dimensional or realistically-scaled case — still a 2x2 toy.
2. A finding of a much worse (but still valid, order-matching) bound would NOT be a failure — same
   graceful-degradation standard as `H-B2-1c`.
3. If the mechanism genuinely BREAKS here (bound violated, or order mismatch) — THAT would be the
   first real limit found in the `H-B2-1*` family, and would be the informative result, not a failure
   of the experiment.

## MCID

Same bar as the rest of the family: finite `(M1, M2, w)` found, bound holds for all tested `n`,
efficiency stable (order-matching) across `n`, for both block orders.
