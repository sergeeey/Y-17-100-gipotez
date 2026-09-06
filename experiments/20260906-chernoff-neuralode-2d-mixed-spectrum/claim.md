# claim.md — 20260906-chernoff-neuralode-2d-mixed-spectrum

**Graph node:** `H-B2-1d` (new, per Minimal Relaxation Rule) · **Bridge:** `B2-CHERNOFF-UDE` · **Tier:** Standard
**Parent:** `H-B2-1b` (2D symmetric matrix, both eigenvalues negative/decaying — CONFIRMED)

> **Role of this experiment:** ONE assumption changed from `H-B2-1b`: eigenvalue SIGN structure —
> both-negative (pure decay) → one positive, one negative (mixed growth/decay). Everything else
> (symmetric `A`, same block construction, same `K_j=0` argument) unchanged from `H-B2-1b`, isolating
> this one question from the non-normality question already tested separately in `H-B2-1c`.

## Why This Specific Next Step (Source-Traced, Not an Arbitrary Escalation)

Before picking a next parameter to vary, searched the literature (FL Step -4) on what real
Neural-ODE/ResNet Jacobians actually look like, rather than arbitrarily widening the eigenvalue ratio:

- **`[VERIFIED]` via `WebSearch`:** ResNet input-output Jacobians at trained checkpoints show "a
  non-negligible number of singular values above 1, indicating that residual units are unstable in
  certain directions" (Li et al., "Demystifying ResNet", ICLR 2017 submission,
  openreview.net/pdf?id=SJAr0QFxe) — i.e. real trained networks have GROWING directions, not only
  decaying ones, contradicting the all-negative-eigenvalue assumption used in `H-B2-1`/`H-B2-1b`/`H-B2-1c`.
- **`[VERIFIED]` via `WebSearch`:** Neural ODEs are explicitly documented to develop "stiffness" —
  "widely separated timescales and Jacobians with large negative eigenvalues", quantified via a
  stiffness index `S = κ(J)(t1-t0)` where `κ(J)` is the Jacobian's condition number (multiple ScienceDirect/
  arXiv sources on stiff Neural ODEs, 2024-2025).

Both findings point toward the SAME gap in `H-B2-1b`'s test: it assumed a "nice," uniformly-decaying,
well-conditioned matrix. The MORE informative and better-motivated next step is not an arbitrarily
larger eigenvalue ratio, but a **mixed-sign spectrum** (one growing, one decaying direction) — directly
matching the "unstable in certain directions" finding, and a genuinely different regime for the `K_j=0`
mechanism: `‖e^{tA}‖` now GROWS with `t` (not decays), requiring `w>0` in Theorem 3.1's condition 1 for
the first time in this experiment family (all prior `H-B2-1*` experiments had `w=0` suffice).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Symmetric `2x2` `A` with eigenvalues `+0.5` (growth) and `-2` (decay), same orthogonal-rotation construction as `H-B2-1b` |
| **Falsifiable predicate** | The `K_j=0` mechanism still gives a valid, order-matching bound when `‖e^{tA}‖` genuinely grows with `t` (requiring `w>0`, not `w=0` as in all prior experiments in this family) |
| **Measurable outcome** | Numerically-determined `M1, w` for the growing case; bound vs. true empirical error, order-1 and order-2 blocks |

## FL Step -4: Source Trace (this experiment's own citations)

- Li et al., "Demystifying ResNet" (ICLR 2017 submission), openreview.net/pdf?id=SJAr0QFxe —
  `[VERIFIED]` via direct WebSearch result text (not re-fetched/re-verified page-by-page here; treated
  as `[WEAK-MEDIUM]` confidence, sufficient for MOTIVATING this experiment's design choice, not as a
  quantitative input to any computation).
- Stiff Neural ODE literature (multiple 2024-2025 sources, ScienceDirect/arXiv) — same confidence level,
  same role (motivating, not quantitative input).
- Theorem 3.1 / `K_j=0` mechanism: unchanged, already source-traced in `H-B2-1`.

## Natural Language Statement

> "We test whether the K_j=0/Theorem 3.1 mechanism still gives a valid, order-matching bound when the
> matrix A has a MIXED spectrum (one growing eigenvalue, one decaying), requiring w>0 for the first
> time in this experiment family, motivated by literature showing real trained ResNets have unstable
> (growing) directions and Neural ODEs develop stiffness from widely-separated eigenvalues."

## L0 Classification

**Descriptive**, unchanged from the `H-B2-1*` family.

## What This Does NOT Mean

1. Does NOT use the cited papers' own quantitative findings (e.g. specific singular value distributions)
   as inputs to this computation — they motivate the DESIGN CHOICE (test a mixed-sign spectrum) only.
2. Does NOT test a non-normal mixed-spectrum case (that would be TWO changed assumptions from `H-B2-1b`
   at once — normality AND sign structure — violating the Minimal Relaxation Rule; deliberately kept
   symmetric here, non-normality already isolated and confirmed separately in `H-B2-1c`).
3. A finding that `w` must be large, or that the bound becomes very loose, does NOT kill the mechanism —
   same standard as `H-B2-1c`: graceful degradation (looser constant) is a pass, not a fail, as long as
   the bound remains valid and order-matching.

## MCID

Same bar as `H-B2-1b`/`H-B2-1c`: a finite `(M1, w)` found, bound holds for all tested `n`, efficiency
stable (order-matching) across `n`, for both block orders.
