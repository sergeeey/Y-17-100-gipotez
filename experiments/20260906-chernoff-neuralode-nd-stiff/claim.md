# claim.md — 20260906-chernoff-neuralode-nd-stiff

**Graph node:** `H-B2-1f` (new, per Minimal Relaxation Rule) · **Bridge:** `B2-CHERNOFF-UDE` · **Tier:** Standard
**Parent:** `H-B2-1e` (2D combined non-normal + mixed-sign, CONFIRMED)

> **Role of this experiment:** ONE assumption changed from `H-B2-1e`: dimension (`2` → `8`), keeping
> the qualitative structure (non-normal, mixed-sign, "stiff" per the Neural-ODE literature already
> cited in `H-B2-1d`'s claim.md) but scaling to a genuinely higher-dimensional case — the natural next
> step named as "genuinely open" in `H-B2-1e`'s decision.md, now attempted directly rather than left
> pending a separate scale decision.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | An `8x8` upper-triangular `A`: diagonal eigenvalues `[0.5, -1, -2, -3, -4, -5, -6, -8]` (one growing, seven decaying, widely separated per the "stiffness" literature already cited in `H-B2-1d`), fixed random off-diagonal coupling (seeded, non-normal) |
| **Falsifiable predicate** | The `K_j=0` mechanism, confirmed at every 2D stress level tested (`H-B2-1c/d/e`), still gives a valid, order-matching bound at `N=8`, without a qualitatively new failure mode appearing only at higher dimension (e.g. `M1`/`M2` blowing up combinatorially with `N`, or the bound's constant becoming so large it is technically valid but practically useless) |
| **Measurable outcome** | Numerically-measured `M1`, `M2` at `N=8`; bound vs. true empirical error for order-1/order-2 blocks; explicit comparison of `M1` growth from `N=2` (`H-B2-1e`: `M1=3.806`) to `N=8` |

## Why N=8, Not Larger

Chosen as a clear, non-trivial step up from `N=2` (4x the dimension) while keeping the experiment fast
and the eigenvalue spread interpretable by inspection, not because 8 is itself special. A further order
of magnitude (`N=50+`, closer to realistic layer widths) is explicitly left as the next open step if this
one succeeds — consistent with `H-B2-1e`'s own naming of "higher dimension" as a real but separate
undertaking, now partially addressed rather than left fully untouched.

## FL Step -4: Source Trace

Unchanged from `H-B2-1d` (stiffness / widely-separated-eigenvalue literature) and `H-B2-1`
(Theorem 3.1) — no new citations needed; this experiment scales an already-motivated construction.

## Natural Language Statement

> "We test whether the K_j=0/Theorem 3.1 mechanism, confirmed through five 2D stress tests, still gives
> a valid, order-matching bound at N=8, with a widely-separated ('stiff') eigenvalue spectrum and
> genuine non-normality, and characterize how the M1 constant scales from N=2 to N=8."

## L0 Classification

**Descriptive**, unchanged from the `H-B2-1*` family.

## What This Does NOT Mean

1. Does NOT reach a realistic neural-network layer width (typically hundreds to thousands) — `N=8` is a
   deliberate, modest step, not a claim of practical scale.
2. Does NOT use empirically-grounded Jacobian statistics — eigenvalues and coupling are still
   hand-chosen (though motivated by the general "stiff, widely-separated, non-normal" qualitative
   picture from the literature), not fit to real trained-network data.
3. A finding that `M1` grows sharply with `N` would NOT necessarily kill the mechanism (the bound could
   still hold, just be less practically informative) — the MCID below is about validity and order, not
   about the constant staying small.

## MCID

Same bar as the rest of the family: finite `(M1, M2)` found, bound holds for all tested `n`, efficiency
stable (order-matching) across `n`, for both block orders, at `N=8`.
