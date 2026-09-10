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

### CORRECTION ADDENDUM (2026-09-10, decisive check from the deep external novelty audit,
`reports/2026-09-10-deep-external-novelty-audit.md`)

**The feature `K_ref(C)`, `C = T(B-WI)`, is EXACTLY homogeneous of degree 0 in `C` --
proven algebraically, then confirmed numerically against this experiment's own
`resolvent_reference_k` implementation (`experiments/20260908-.../kreiss-resolvent-reference/run.py`).**

Proof: `kappa_lambda1` (Wilkinson eigenvalue condition number, a ratio of unit-normalized
eigenvectors) does not depend on the scale of the matrix at all -- `kappa_lambda1(c*A) =
kappa_lambda1(A)` exactly, for any `c>0`. The line-search term `x/sigma_min((alpha+x)I-A)`
is also exactly homogeneous of degree 0 under the substitution `x -> c*x'`, since
`sigma_min` scales linearly with `c`: `sigma_min(c*M) = c*sigma_min(M)`. So
`K_ref(c*A) = K_ref(A)` for every `c>0`, in exact arithmetic over an UNBOUNDED search
range for `x`.

**Consequence for the "asymmetric transfer degradation" framing above:** at fixed `W`,
this means `K_ref(T(A-WI))` should be IDENTICAL for every `T`, and the predicted
`log(M)` from the fitted power law should therefore also be constant across `T` -- the
observed multiplicative degradation (30x at T=0.1, 2x at T=10) is then largely an
**arithmetic consequence of comparing a near-constant predicted value against a target
`M_{T,W}` that varies genuinely with `T`** (provably `M_{T,W}->1` as `T->0`, as already
noted above), not new information about which direction of extrapolation is "worse" for
this class of predictor as such.

**However, the numerical IMPLEMENTATION of `K_ref` is NOT exactly degree-0 homogeneous,
because `line_search_floored` searches `x` over a FIXED absolute range
`[X_FLOOR=1e-4, X_HI=60]`, not a range that scales with `T`.** Verified directly (not
against this experiment's own saved data, which did not persist per-matrix `K_ref` values
per `T` -- verified instead on a freshly constructed representative near-nilpotent test
matrix using the real `resolvent_reference_k`/`line_search_floored` code, where the
line-search term dominates `kappa_lambda1`, matching the "line_search_dominates" case
this arc's own H-B2-1u/1y already documented for a nontrivial fraction of real matrices):
scaling that matrix by `c` and recomputing `k_ref(c*A)` gives an EXACTLY constant value
across `c in [1e-4, 10]` (as the algebra predicts), but the value systematically degrades
for `c` outside that range -- at `c=100` the true optimal search point falls just past
`X_HI=60` (mild ~0.3% error); at `c=1000` it falls far past `X_HI`, and `k_ref` collapses
back to the (smaller, wrong) `kappa_lambda1` value, a ~40% underestimate on this test
matrix. The floor `X_FLOOR=1e-4` is symmetric risk at small `c`.

**What this changes and what it does not:** the REJECT verdict for this experiment's own
pre-registered criterion (order-of-magnitude threshold met on new-family+new-T) is
UNCHANGED -- both the provable degree-0 homogeneity (predictor carries no T information)
and the numerical floor/ceiling artifact (predictor's OWN reported value can additionally
drift at extreme T) point the same direction: away from trusting this predictor's T-
extrapolation, for two independent reasons rather than one. What changes is the
INTERPRETATION: "asymmetric degradation, worse toward small T" is not an empirical
discovery about transient-growth predictors in general -- it is arithmetic (constant
prediction vs a target that provably shrinks toward 1) plus, potentially, a specific,
fixable implementation bug (scale the search bounds with the matrix, e.g.
`X_FLOOR/X_HI -> X_FLOOR/X_HI * (spectral scale of A)`) whose exact contribution to the
numbers above was NOT isolated this session (would require re-instrumenting
`resolvent_reference_k` to persist per-matrix, per-T `K_ref` values, which the original
run did not do). Flagged as a concrete, cheap follow-up if this arc is ever revisited.

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
