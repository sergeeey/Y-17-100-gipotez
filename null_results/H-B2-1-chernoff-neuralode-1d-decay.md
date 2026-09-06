# decision.md — 20260906-chernoff-neuralode-1d-decay

**Graph node:** `H-B2-1` · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [x] **KILLED** — kill_criterion (b) triggered: the Chernoff bound does NOT dominate/inform the
  empirical error; bridge killed as practically useless even though formally valid
- [ ] ARCHIVE

**Falsified statement:** *The quantitative Chernoff-rate theorem (Galkin & Remizov 2021, Theorem 1.2 /
formula (2)) gives a convergence-rate estimate for a 1D linear ResNet/Euler block that is at least as
tight as the true empirical error.* It does not: **the theorem's own guaranteed order is exactly one
full polynomial power of `n` looser than the true empirical order, for BOTH a first-order (`m=1`) and a
second-order (`m=2`) block, at BOTH tested time horizons (`T=1`, `T=3`).**

## Evidence Summary

| Block | `m` | Chernoff-guaranteed order | Empirical order (T=1) | Empirical order (T=3) | Gap |
|---|---|---|---|---|---|
| order-1 (`s(h)=1-h`, standard Euler/ResNet) | 1 | 0 (only qualitative `o(1)`, NO rate) | **1.0015** | **0.9991** | ≈1.00 |
| order-2 (`s(h)=1-h+h²/2`) | 2 | 1 (`o(1/n)`) | **2.0026** | **2.0079** | ≈1.00 |

Both blocks satisfy Chernoff's theorem's three hypotheses (`s(0)=1`, `s'(0)=A=-1`, numerically confirmed
in `tests/test_chernoff_neuralode_1d.py`) — **kill_criterion (a) is NOT triggered, the layer does NOT
formally violate a Chernoff hypothesis.** Kill_criterion (b) IS triggered.

## Why the Gap Is Exactly 1, Not an Artifact

A hand Taylor-expansion of `ln(s(t/n))` for both blocks (documented in the session, cross-checked
against the numerical regression) shows the mechanism precisely:

- `s1(t) = 1 - t`: `ln(s1(t/n))·n = -t - t²/(2n) + O(1/n²)` ⟹ true error `~ e^{-t}·t²/(2n)`, i.e.
  order **1** — but formula (2) with `m=1` only guarantees `o(n^0)`, i.e. order **0**.
- `s2(t) = 1 - t + t²/2`: `ln(s2(t/n))·n = -t + t³/(6n²) + O(1/n³)` ⟹ true error `~ e^{-t}·t³/(6n²)`,
  i.e. order **2** — but formula (2) with `m=2` only guarantees `o(1/n)`, i.e. order **1**.

The pattern (`true order = m`, `guaranteed order = m-1`) held identically for both tested blocks and
both tested time horizons — not a coincidence of one specific case, and not a numerical artifact (the
symbolic derivation and the independent numerical log-log regression agree to within measurement noise
of a floating-point computation, `~0.001-0.008` relative to the exact integer orders 1 and 2).

## Positive/Negative Controls (in `tests/test_chernoff_neuralode_1d.py`, run BEFORE this real result)

- **Positive control:** `iterate_block` converges to the analytic solution as `n→∞` (Chernoff's basic
  qualitative theorem) — confirmed.
- **Negative control:** a block with the WRONG generator sign (`s(h)=1+h`, growth not decay) does NOT
  converge to the decay solution — confirms the harness doesn't spuriously match regardless of input.
- **Regression self-consistency control:** the empirical-order estimator recovers the textbook-known
  order-1 global error rate for plain Euler discretization (well-established numerical ODE theory,
  independent of anything Chernoff-specific) — confirms the log-log regression machinery itself is
  sound before trusting its output on the actual comparison.

## Why Floor-Ceiling (FL Step 4a) Does Not Apply Cleanly Here (Structure-Bias Guard)

This experiment is a **deductive/mathematical verification**, not a population-level empirical claim —
there is no "null model with the mechanism removed" or "privileged-access ceiling" in the Step 4a sense;
the exact analytic solution IS the ground truth (full, not privileged, access — the whole point of
choosing an analytically solvable 1D toy), and there is no floor construction that makes sense for a
symbolic/numerical identity. Forcing the Floor-Ceiling template onto a deductive result would be
exactly the anti-pattern `falsification-ladder.md`'s own Structure-Bias Guard warns against. The
positive/negative controls above serve the equivalent sanity-checking role for this experiment type.

## Kill Analysis (OSA, required for KILLED)

### What Was Killed

- **The specific claim that Galkin & Remizov (2021)'s quantitative Chernoff-rate theorem (Theorem 1.2 /
  formula 2) is a USEFUL, INFORMATIVE tool for predicting Neural-ODE/ResNet discretization error** —
  it is formally correct but systematically one polynomial order looser than what elementary
  Taylor-expansion analysis (already standard, simpler, and older than Chernoff's theorem itself)
  already gives for free, for both tested block orders.
- **The practical value of invoking this specific Chernoff apparatus over standard numerical-ODE
  analysis** for this class of problem (finite-dimensional, analytic-generator toy case) — the
  operator-semigroup machinery adds mathematical prestige, not predictive power, here.

### What Was NOT Killed

- [x] **Chernoff's theorem itself (Theorem 1.1, the general qualitative convergence result)** — remains
  true and correctly verified; only its specific quantitative rate REFINEMENT (Theorem 1.2/formula 2)
  is shown to be loose for this case.
- [x] **The idea that a ResNet/Neural-ODE block CAN be modeled as a "Chernoff function"** — confirmed
  TRUE (hypotheses satisfied) for this linear toy; not killed.
- [x] **The general possibility that SOME semigroup-theoretic tool could give a tighter, more useful
  bound than elementary calculus for Neural-ODE error analysis** — this experiment tested ONE specific,
  correctly-cited theorem, not the entire space of possible operator-theoretic approaches. A different
  (sharper) Chernoff-type rate theorem, if one exists in the literature, was not tested here.

### Relaxation Map (for surviving assumptions)

| Assumption | Modification | New Path | Known kill-evidence? | Cheapest test |
|---|---|---|---|---|
| The specific rate theorem used (Galkin & Remizov 2021, Thm 1.2) | Search for a DIFFERENT, possibly sharper, quantitative Chernoff-type rate theorem in the literature (the same paper's own more general Theorem 3.1, for higher-dimensional/infinite-dimensional cases, was NOT used here — only the simplified 1D corollary) | Re-run the same numerical comparison against Theorem 3.1's general bound, applied to this same 1D case as a sanity check | No — untested, and likely low priority given Theorem 1.2 is already presented in the paper as the 1D specialization of 3.1, so the same looseness likely persists | Read the paper's own Section 3 (pp.15-21) fully and re-derive its 1D specialization independently to check for a tighter form the abstracted Theorem 1.2 may have dropped |
| Problem dimensionality (1D toy) | Test whether the SAME order-gap-of-1 pattern holds in a genuinely multi-dimensional linear ODE (matrix generator, not scalar) — closer to a real Neural-ODE layer | New experiment, moderate scope | No | Repeat the same regression machinery with a 2x2 or 3x3 linear system with known eigen-decomposition (still analytically solvable) |

**Recommendation:** given this was a well-scoped Standard-tier bridge check with a clean, reproducible
KILL on the specific pre-registered criterion, and no strong independent motivation yet for chasing a
sharper theorem (Relaxation Map row 1) before checking multi-dimensionality (row 2) — if this bridge is
revisited, row 2 (matrix case) is the more informative next cheapest test, since it tests whether the
order-gap-of-1 finding is a 1D-specific artifact or a general property of this style of rate theorem.

## What This Does NOT Mean

1. Does NOT mean Chernoff's theorem is wrong — it is a real, correctly-verified, general result; only
   its specific 1D quantitative refinement is shown non-tight for this case.
2. Does NOT mean NO semigroup-theoretic tool could ever usefully bound Neural-ODE/ResNet error — only
   that THIS specific, correctly-sourced tool does not, for this specific tractable case.
3. Does NOT test a real trained neural network, a nonlinear ODE, or a multi-dimensional system — the
   toy was deliberately chosen to be fully analytically tractable, per the pre-registered kill
   criterion's own wording ("1D Neural ODE with analytic solution").
4. Does NOT retroactively validate or invalidate the earlier fabricated citation about Chevyrev & Friz
   (2022) — that citation remains unverified/fabricated and is not used anywhere in this analysis; see
   `claim.md`'s "Correction Filed Before This Experiment Began" section and the `pearl_registry` entry.

## Pearl Card Update

**New information, portable beyond this specific bridge:** for polynomial-Taylor-truncation Chernoff
functions of order `m` (i.e. `s(t)` matching `e^{At}`'s Taylor series exactly to order `m`), the
one-dimensional quantitative Chernoff-rate theorem (formula 2, Galkin & Remizov 2021) systematically
UNDERSTATES the true convergence order by exactly 1 — the true order is `m`, not the theorem's own
guaranteed `m-1`. This was verified both symbolically (Taylor expansion of `ln(s(t/n))`) and numerically
(log-log regression, `n` up to 6400, two time horizons), with the two methods agreeing to within
floating-point/regression noise (~0.001-0.008 relative to the exact integer targets). Filed as a
methodology pearl in `pearl_registry/INDEX.md` — this pattern likely generalizes to any Standard-Ladder
check of a "named theorem's own quantitative refinement" against elementary calculus, not just this
bridge.
