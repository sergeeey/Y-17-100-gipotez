# decision.md — H-B2-1l (eigenvector conditioning κ(V) vs M1)

## Result

**Verdict: CONFIRMED.** Eigenvector-matrix conditioning `κ(V)` is POSITIVELY correlated with `M1`
in BOTH independently-collected populations, unifying two previously-unexplained findings from
this session under one classically-motivated mechanism.

| Population | n | Spearman ρ | p-value |
|---|---|---|---|
| Seed ensemble (`H-B2-1i`'s own 30 seeds, fixed N=8, coupling=15) | 30 | **0.453** | 0.012 |
| N-sweep (`H-B2-1k`'s own 9 points, fixed coupling=15, seed=0) | 9 | **0.917** | 0.0005 |

Both statistically significant despite small samples (α=0.05), same direction as pre-registered.

## What Was Confirmed

- [x] The mechanism proposed informally in both `H-B2-1i`'s and `H-B2-1k`'s own pearl_registry
  entries ("eigenvalue clustering") has a specific, testable, classically-grounded form
  (`κ(V)`, the eigenvector matrix's condition number, per `‖exp(tA)‖ ≤ κ(V)·max_i exp(t·Re(λ_i))`
  — Trefethen & Embree's non-normal matrix theory), and it holds up under direct test on BOTH
  populations independently.
- [x] The N-sweep correlation (ρ=0.917) is remarkably strong — `κ(V)` explains the large majority
  of `H-B2-1k`'s own non-monotonic `M1(N)` curve. The specific local extrema found there (e.g.
  the 12× jump at N=16, the >6× drop at N=32) are very likely driven by `κ(V)` moving in the same
  pattern, not a separate, unexplained phenomenon.
- [x] The seed-ensemble correlation (ρ=0.453) is weaker but still significant — `κ(V)` explains
  PART of `H-B2-1i`'s own right-skewed `M1` distribution, but leaves substantial unexplained
  variance, consistent with the pre-registered expectation that `κ(V)` is "a mechanism, not
  necessarily the only one."
- [x] No new stochastic draws were needed — this experiment reused `H-B2-1i`'s and `H-B2-1k`'s
  own already-built matrices and already-committed `M1` values (provenance-verified: the
  reference seed=0 case reproduces `H-B2-1i`'s own committed `M1` exactly).

## What Remains Open

- **Why is the N-sweep correlation so much stronger than the seed-ensemble correlation?**
  (0.917 vs 0.453) Not diagnosed here. One plausible account: varying `N_DIM` at fixed spectral
  range changes how densely eigenvalues are packed into a fixed interval in a fairly systematic
  way, while varying `seed` at fixed `N_DIM=8` produces more genuinely random, less structured
  variation in eigenvalue spacing — but this is speculation, not tested.
- `κ(V)` does not fully explain either population's `M1` variation (ρ<1 in both cases) — the
  residual variance's source is unidentified.
- The classical bound this mechanism is based on is an INEQUALITY, not an equality — a strong
  correlation is expected under the mechanism but not mathematically guaranteed at any specific
  strength; this experiment establishes association, not a validated quantitative law.

## Relaxation Map

- **Regress `M1` on `κ(V)` directly** (not just rank correlation) to see whether a power-law or
  linear relationship fits either population, which would sharpen "correlated" into an actual
  quantitative account.
- **Decompose why the N-sweep and seed-ensemble correlations differ in strength** — could
  investigate by computing `κ(V)` under BOTH manipulations jointly (multi-seed AT each N_DIM),
  which would also address `H-B2-1k`'s own open single-seed-limitation caveat.
- **Test on a THIRD, independent population** — e.g. `H-B2-1h`'s own 10-point coupling-magnitude
  sweep — to see if `κ(V)` also explains the exponential-with-deceleration pattern found there.

## Note on Floor–Ceiling (FL Step 4a)

Not applicable in the arm/null-model sense — descriptive correlational analysis of two
already-computed quantities on already-collected data, not a detection rule tested against a
null-model floor.

## FL Step 8a — Skeptic Pass

Not run as a separate agent invocation (Evaluator-Optimizer cap still in effect session-wide).
Manual discipline applied: the mechanism was sharpened to a SPECIFIC, falsifiable, pre-existing
mathematical quantity (not an ad hoc post-hoc metric invented to fit the data) before running;
both populations were checked independently and reported separately (never pooled, since they
vary different things); the weaker seed-ensemble correlation is reported honestly alongside the
much stronger N-sweep one, not averaged into a single flattering number.

**Anticipated FALSIFIED-equivalent concern:** "a positive correlation between two quantities
both derived from the same matrix could be a mathematical near-tautology, not a real mechanistic
finding." **Response: Accepted as a valid framing concern, mitigated by literature grounding** —
`κ(V)` and `M1` are NOT trivially the same quantity by construction (one is a static algebraic
property of the eigendecomposition, the other is a measured dynamic transient-growth quantity
over a time integral); the relationship between them is a real, previously-established
inequality in the numerical-analysis literature (Trefethen & Embree), not invented for this
experiment — the correlation found here is empirical support for an existing theoretical
relationship holding on this specific construction family, not a novel unverified claim.

## EstimandOps — What This Does NOT Mean (restated per claim.md)

1. Does NOT establish causation — both `κ(V)` and `M1` are properties of the same matrix `A`;
   this is a mechanistic-association claim, not a causal claim.
2. Does NOT explain 100% of `M1`'s variation in either population.
3. Does NOT generalize beyond this specific construction family (one positive eigenvalue, many
   negative, random upper-triangular coupling) without further testing.
4. Statistical power is limited (n=9, n=30) — CONFIRMED here is suggestive and grounded in
   established theory, not a strong independent statistical discovery on its own.

## Pearl Card Update

**Unifies two independently-pearled, previously-unexplained observations** (`H-B2-1i`'s
right-skew, `H-B2-1k`'s non-monotonicity) under one classically-grounded mechanism, with
cross-population empirical support. This is the strongest, most theoretically-anchored
mechanistic finding of the `H-B2-1*` arc's "digging into mechanisms" phase — closes both
open pearl_registry falsifiable predictions that proposed this mechanism informally.
