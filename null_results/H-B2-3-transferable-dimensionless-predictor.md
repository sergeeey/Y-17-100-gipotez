# H-B2-3 — decision.md

## Result

### A real construction bug caught before any transfer number was trusted

The first run of `build_rotation_block_matrix` used a plain element-wise
`np.triu(coupling, k=1)` mask, matching the original family's own convention. Diagnostic
(`diag_h_b2_3.py`, run before trusting the pilot's `Infinity` RMSE values) showed
`max_re_eig` of the FULL matrix ranged from 0.5 to 5.98 instead of the intended fixed set
{0.5, growth block; <=-0.5, decay blocks} — a plain upper-triangular mask cuts THROUGH a
2x2 rotation block's own off-diagonal entry, corrupting that block's eigenvalues. The
resulting pathologically ill-conditioned matrices made `resolvent_reference_k` return
`inf` for several `(n, seed)` pairs (`RuntimeWarning: overflow in SVD`), propagating to
`Infinity` in the reported RMSE. Fixed by masking coupling to zero within any single
block (block-upper-triangular, not element-upper-triangular) — this preserves the
diagonal blocks' eigenvalues exactly regardless of the coupling's own magnitude, verified:
`max_re_eig` is now `0.500` for every tested `(n, seed)`.

### Primary finding

| condition | RMSE (log space) | multiplicative degradation vs T=1 same-family baseline |
|---|---:|---:|
| same family, T=1 (baseline) | 0.52 | -- |
| same family, T=0.1 | 3.94 | ~30x |
| same family, T=0.3 | 2.28 | ~7x |
| same family, T=3.0 | 1.10 | ~1.8x |
| same family, T=10.0 | 1.19 | ~2x |
| new family, T=1 | 1.75 | ~3.4x |
| new family, T=0.3 | 5.83 | ~200x |
| new family, T=3.0 | 3.61 | ~22x |

**Asymmetric within-family degradation.** Extrapolating to LARGER T (3, 10) is mild
(~2x); extrapolating to SMALLER T (0.1, 0.3) is severe (~7-30x). This is itself
informative, not just noise: `M_T,W -> 1` as `T -> 0` (the transient-growth phenomenon
has not had time to develop), a regime the power-law form `M ~ K_ref^exponent` (fit at
T=1, where transient overshoot is already substantial) was never designed to cover.

**New-family transfer degrades further, worst on the double extrapolation.** Transfer B
(new family, T=1 only) is a real but moderate ~3.4x degradation over baseline — worse than
same-family/T=1, comparable to or better than same-family's own worst-T extrapolations.
Transfer C (new family AND new T together) is the worst case measured: ~200x at T=0.3,
~22x at T=3.0 -- both meet or exceed the pre-registered "order of magnitude" REJECTED
threshold.

**Compute cost holds up.** Predictor path: 0.053s per matrix (one `resolvent_reference_k`
call). Direct grid path: 1.00s per matrix (1000-point `expm` sweep, matching the arc's own
`n_grid` convention). The predictor is **~19x faster**, unaffected by the accuracy
findings above -- the cost half of the claim is not the part that fails.

## Verdict

**REJECTED**, per claim.md's own pre-registered closure criterion ("the advantage vanishes
outside the original generator... RMSE degrades by an order of magnitude or more"). Two of
three tested new-family conditions (Transfer C at both T values) clearly meet this
threshold; Transfer B alone (new family, T=1) is a real but more moderate degradation,
consistent with -- not contradicting -- the REJECTED verdict once combined with Transfer C.

**This does NOT mean the dimensionless reduction itself is wrong** -- the algebraic
identity `M_T,W(B) = M_1,0(T(B-WI))` is exact (verified numerically to 1e-6, see `tests/`)
and holds regardless of matrix family. What fails is the SPECIFIC fitted power-law
relationship between `K_ref` and `M`, calibrated once at `T=1` on one matrix family --
exactly explanation (b) from claim.md's Origin section (the predictor learned features
specific to the original generator and to the T=1 transient regime), not explanation (a)
(a universally scale-consistent mechanism). The dimensionless rescaling is necessary
machinery, correctly implemented, but not sufficient on its own to make the fitted
relationship transferable.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the specific claim that ONE power-law fit, calibrated at `T=1` on the
`build_matrix_with_seed_and_n` family, transfers without refitting to substantially
different `T` or to a structurally different matrix family. It does not, at the
"order of magnitude" bar this experiment itself set before running.

**What was NOT killed:** (1) the dimensionless reduction identity itself -- exact algebra,
verified, and correctly reduces the finite-window problem to a single rescaled matrix
regardless of what happens next; (2) the predictor's raw compute-cost advantage (~19x),
independent of the accuracy findings; (3) the possibility that REFITTING `K_ref -> M`
separately per matrix family (using the SAME dimensionless feature, just not insisting on
one universal exponent) could still be useful -- not tested here, a real, cheap follow-up
if this line is revisited.

**Revival condition:** refit the power-law per family (still reusing the dimensionless
`K_ref(T(B-WI))` feature, abandoning only the claim of ONE universal fit) and check whether
the FUNCTIONAL FORM (not the fitted constants) transfers -- i.e. does log(M) remain
linear in log(K_ref) within the new family, even if the slope/intercept differ? That is a
weaker, more defensible claim this experiment did not test and does not rule out.

## Skeptic Concerns (self-review, FL Step 8a — a construction bug already caught and fixed
via direct diagnosis substitutes for part of an external adversarial pass; the remaining
concerns below are genuine limitations of the design, not defects)

- "One alternative family (rotation blocks) is not a representative sample of 'matrix
  families in general'" → **Accepted limitation**, stated in claim.md before running (item 1
  under "What this does NOT mean").
- "The T=0.1/0.3 same-family degradation might indicate n_grid=1000 is too coarse to
  resolve the transient peak at very short T, not a genuine model failure" → **Plausible,
  not ruled out** -- at T=0.1, the grid spacing is `T/n_grid = 1e-4`, ten times finer in
  absolute terms than at T=1's `1e-3` spacing, so under-resolution seems unlikely to be the
  dominant effect, but this was not independently verified with a finer grid. Named as an
  open uncertainty, not resolved.
- "The rotation-block family's coupling magnitude (15.0, same as the original family) may
  not be a fair comparison -- a different family 'naturally' calling for a different
  coupling scale could bias the transfer result" → **Accepted limitation**, the coupling
  magnitude was deliberately kept identical to isolate the effect of eigenvalue structure
  alone, but this is a choice, not a neutral default.

## Scope note

Route 4 of the user's 2026-09-09 direction-scoping report, first experiment executed under
that direction (`начни B2`). Extends the closed H-B2-1/H-B2-2 arc without reopening or
contradicting its own established finding (K_ref loosely bounds M1, efficiency 3.7-31%) --
this experiment asks a different, transferability-focused question.
