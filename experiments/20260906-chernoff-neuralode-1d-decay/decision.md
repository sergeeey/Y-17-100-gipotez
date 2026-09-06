# decision.md — 20260906-chernoff-neuralode-1d-decay

**Graph node:** `H-B2-1` · **Date:** 2026-09-06 · **CORRECTED 2026-09-06 (same session, see addendum
at the bottom) — original verdict below is SUPERSEDED, kept verbatim for the historical record per
this project's Hindsight Distortion Gap discipline (never silently rewrite; add a dated correction).**

## Verdict (ORIGINAL — SUPERSEDED, see correction addendum at end of file)

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

---

## CORRECTION ADDENDUM (2026-09-06, same session, continuing the same reading of the same primary source)

### What changed

While continuing to read the SAME primary source (Galkin & Remizov 2021, arXiv:2104.01249) beyond the
pages used for the original test (pp.1-6), pages 15-21 were read (`Read` tool, PDF pages, same method
as before) and reveal **Theorem 3.1** — the paper's actual MAIN result, of which **Theorem 1.2 (used in
the original test above) is an explicitly-labeled simplification/special case** ("Statement (2) is
similar to (1), but (2) is not so elementary even in one-dimensional case... the theorem 3.1 covers
non-trivial cases, such as dim F = ∞ and ‖L‖ = ∞", p.6). The original test used ONLY the simplified
corollary and never checked whether the paper's stronger, more general theorem gives a better bound.

### Re-derivation using Theorem 3.1

Theorem 3.1's condition 3 requires functions `K_j(t) ≥ 0` such that
`‖S(t)f − Σ_{k=0}^m t^k L^k f/k!‖ ≤ t^{m+1} Σ_j K_j(t)‖L^j f‖`. For our polynomial blocks
(`s1(h)=1-h`, `s2(h)=1-h+h²/2`), the left-hand side is **IDENTICALLY ZERO** for every `t`, not merely
small — because each block was constructed to equal exactly the degree-`m` Taylor truncation of
`e^{-t}`, term for term. Choosing `K_j(t) = 0` for all `j` is therefore a legitimate, non-cheating
choice (`0 ≤ 0`), not an approximation.

With `K_j = 0`, `M1 = M2 = 1`, `w = 0` (valid whenever `|block(t/n)| ≤ 1` at the step size actually
used — checked numerically for every tested `(T, n)` pair, see `tests/test_theorem_3_1_correction.py`),
Theorem 3.1's conclusion (formula 13) reduces to the clean closed form:

```
bound_m(t, n) = t^(m+1) / ((m+1)! · n^m)
```

This is **order `m`** — matching the TRUE empirical order exactly, not `m-1` as the simplified
corollary gave.

### Numerical verification (`experiments/20260906-chernoff-neuralode-1d-decay/theorem_3_1_check.py`)

Re-uses the ALREADY-COMPUTED empirical errors from `metrics/run.json` (zero new expensive compute).
For all 4 (T, block) combinations × 8 values of `n` (32 checks total):

| T | block | efficiency (true error / bound) — CONSTANT across all 8 tested `n` |
|---|---|---|
| 1.0 | order-1 | 0.368 ± 0.001 |
| 1.0 | order-2 | 0.370 ± 0.002 |
| 3.0 | order-1 | 0.050 ± 0.000 |
| 3.0 | order-2 | 0.051 ± 0.001 |

**The bound HOLDS in all 32 cases** (`true_error ≤ bound` every time), and — critically — the
efficiency ratio is **CONSTANT as `n` grows**, not drifting toward 0 or ∞. A drifting efficiency would
mean the bound's order doesn't match reality; a constant efficiency is the signature of an EXACT order
match. 4 regression tests (`tests/test_theorem_3_1_correction.py`) lock this in, including a hand-derived
formula cross-check independent of the numerical run.

### Revised Verdict

- [x] **PROMOTE** — kill_criterion (b) is **NOT triggered** when the paper's actual main theorem
  (3.1) is applied correctly, with the legitimate `K_j=0` choice justified by the block's exact
  polynomial construction. Combined with kill_criterion (a) also not triggered (established in the
  original test above), **this bridge, in its 1D toy form, formally holds AND yields a genuinely
  informative, order-matching quantitative bound** — reversing the original KILLED verdict.

### Why This Is Not a Retraction of the Original Test's Own Claim

The original test's claim — "Theorem 1.2 gives a rate estimate one order looser than the true error" —
remains TRUE and independently useful (it is now itself a documented limitation of that specific
simplified corollary, filed as a pearl). What was wrong was the INFERENCE drawn from it: that this
implies "the Chernoff apparatus adds no predictive value here." That inference doesn't survive checking
the paper's stronger theorem. This is analogous to testing a weak baseline, finding it fails, and
concluding the whole METHOD fails — without checking whether a stronger, still-legitimate variant of
the same method succeeds. A concrete instance of "verify the STRONGEST available formalization of a
claim before concluding the underlying idea doesn't work," not previously named as its own gate in this
project's methodology stack.

### Kill Analysis Update (OSA)

**What is now UN-killed:** "The Chernoff apparatus (applied via ITS OWN best-available quantitative
theorem, not an arbitrary simplification of it) gives no useful bound beyond elementary calculus for
this class of problem" — this specific claim is now REVERSED. The apparatus, applied via Theorem 3.1
with the legitimate `K_j=0` construction, gives a bound with the CORRECT order and a REASONABLE
constant (within ~3-20x of the true error, constant in `n`), genuinely informative and non-trivial.

**What remains correctly killed:** Theorem 1.2 (the simplified 1D corollary) specifically IS loose by
exactly one order — that finding stands, unchanged, and is exactly why checking the general theorem
mattered here.

**Relaxation Map status:** row 2 (matrix/multi-dimensional case) from the original Relaxation Map above
is now MORE motivated, not less — if Theorem 3.1 (which explicitly covers `dim F = ∞`) gives a tight,
order-matching bound even in the genuinely multi-dimensional case (not just this 1D toy), that would be
a substantially stronger and more publishable result. Not run in this session (time budget); flagged as
the clear next step if this bridge is revisited.

### Pearl Card Update (Correction)

**New pearl, portable beyond this bridge:** when a named theorem has an explicitly-simplified corollary
(the paper itself often SAYS so — "Statement (2) is similar to (1), but not so elementary"), a
Standard-Ladder check that finds the SIMPLIFIED corollary loose/uninformative must NOT be treated as a
verdict on the underlying apparatus without also checking whether the theorem's OWN stronger/general
form (when it exists in the same source) closes the gap. This is a new, general methodological gate —
tentatively named the "Strongest-Available-Formalization Check" — worth adding to this project's own
methodology stack (`~/.claude/rules/` or a project-level note) given it directly overturned a KILLED
verdict in this very session.
