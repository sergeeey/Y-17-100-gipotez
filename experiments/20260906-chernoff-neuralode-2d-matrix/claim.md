# claim.md — 20260906-chernoff-neuralode-2d-matrix

**Graph node:** `H-B2-1b` (new, per Minimal Relaxation Rule) · **Bridge:** `B2-CHERNOFF-UDE` · **Tier:** Standard
**Parent:** `H-B2-1` (1D case, originally KILLED, then CORRECTED to CONFIRMED same session — Theorem 3.1
gives an order-matching, constant-efficiency bound when applied with the legitimate `K_j=0` choice)

> **Role of this experiment:** Relaxation Map row 2 from `H-B2-1`'s correction addendum: does the SAME
> mechanism (Theorem 3.1 + exact polynomial Taylor-truncation blocks + legitimate `K_j=0`) still give a
> tight, order-matching bound in a genuinely MULTI-DIMENSIONAL case (`dim F = 2`, not 1), which is
> exactly the regime Theorem 3.1 is stated for and Theorem 1.2 is NOT (Theorem 1.2 is explicitly the
> "one-dimensional real analog"). ONE assumption changed from `H-B2-1`: dimension (1D scalar → 2D
> matrix, symmetric with two distinct real eigenvalues). Everything else (block construction, rep
> logic, bound derivation) is the same mechanism, generalized.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | A 2D linear "ResNet block" `F(h)x = x + hAx` (order-1) and `F(h)x = x + hAx + (hAx)²/2!` (order-2, matrix-polynomial), for a symmetric `2x2` matrix `A` with two distinct real eigenvalues, iterated `n` times, compared to the exact analytic solution `e^{tA}x0` |
| **Falsifiable predicate** | Theorem 3.1 (Galkin & Remizov 2021), applied with the SAME legitimate `K_j=0` choice used in `H-B2-1`'s correction, gives a bound with CONSTANT efficiency (true error / bound) as `n` grows, for BOTH eigenvalue directions simultaneously — not just the slower one |
| **Measurable outcome** | Symbolic + numerical comparison of the bound's order against the true empirical error order, for order-1 and order-2 matrix blocks, at `T=1` |

## Why This Is a Genuine (Not Trivial) Test of the Mechanism

A naive worry: since `A` is symmetric and diagonalizable (`A = P D P^T`), doesn't this reduce to "two
independent scalar problems"? Partially — the NORM analysis does decompose along eigendirections
(`‖F_m(t)‖₂ = max(|f_m(λ₁t)|, |f_m(λ₂t)|)` for a symmetric polynomial-in-`A` block). But this is exactly
the point of the test: **the FASTER eigenvalue (`λ₂ = -2`, decaying twice as fast as `λ₁ = -1`) requires
a SMALLER step size `h=t/n` for the `M2` condition (`|f_m(λh)| ≤ 1`) to hold than the slower eigenvalue
does.** If the step sizes used in `H-B2-1`'s 1D test (chosen based on the single eigenvalue `-1`) are
too coarse for `λ₂=-2`, the `M2` condition could fail at small `n`, invalidating the bound in a way the
1D test could never reveal (1D has only one eigenvalue). This is the genuinely new information a
multi-dimensional case can surface that a scalar toy cannot — not a mere relabeling of the same
computation.

## FL Step -4: Source Trace

Unchanged from `H-B2-1`: Chernoff's theorem and Theorem 3.1, Galkin & Remizov (2021, arXiv:2104.01249),
`[VERIFIED]` via direct primary-source read (same PDF, same pages 15-19, already transcribed in
`H-B2-1`'s decision.md correction addendum). No new source-trace needed — this experiment applies an
already-verified theorem statement to a new (multi-dimensional) case.

## Natural Language Statement

> "We test whether the K_j=0 / Theorem 3.1 mechanism that gave a tight, order-matching bound for a 1D
> Chernoff-function block (H-B2-1) still gives a valid, tight bound for a 2D matrix block with two
> distinct eigenvalues, and specifically whether the FASTER eigenvalue's stricter step-size requirement
> breaks the M2 condition at the step sizes that worked in 1D."

## L0 Classification

**Descriptive** (same as parent H-B2-1) — characterizes a fully-specified numerical scheme against a
known analytical ground truth, no population, no causal claim.

## What This Does NOT Mean

1. Does NOT test a non-normal (non-diagonalizable-by-orthogonal-matrix) `A` — deliberately restricted to
   the symmetric case to keep the norm analysis exact and tractable; a non-normal `A` (where transient
   growth/non-normality effects can dominate) is a separate, harder follow-up not attempted here.
2. Does NOT test a real trained neural network or a nonlinear system.
3. A PASS here would strengthen (not prove in general) that Theorem 3.1's mechanism generalizes beyond
   the 1D toy; a FAIL would show the mechanism is 1D-specific and needs more care (e.g. a
   direction-dependent step size) in genuinely multi-dimensional settings — either way, informative.

## MCID

The bound is "informative" if (a) it holds (true error ≤ bound) for all tested `(n, m)` and (b) the
efficiency ratio is reasonably stable (not blowing up or collapsing by more than ~2 orders of magnitude)
across the tested `n` range for BOTH block orders — same qualitative bar as `H-B2-1`'s correction.
