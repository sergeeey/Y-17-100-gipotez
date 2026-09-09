# H-B2-3 — claim.md

## Origin

Route 4 of the user's 2026-09-09 direction-scoping report
(`reports/2026-09-09-breakthrough-routes.md`): "полезная грубость может соответствовать
времени наблюдения." The whole H-B2-1/H-B2-2 arc (closed 2026-09-08,
CONFIRMED-WITH-CAVEATS) fit `M1 ~ K(A)^exponent` where `M1` is transient growth measured on
a FIXED window `T_MAX=1.0` (`experiments/20260907-chernoff-neuralode-nd-dimension-sweep/
run.py:25`, unchanged throughout the arc; H-B2-1u's own claim.md already carries an honest
caveat that `T_MAX=1.0` might be truncating the true peak, never systematically tested).
Two competing explanations for why the crude resolvent-based predictor worked at all:
(a) it measures a scale genuinely tied to the finite observation window `T`, or (b) it
merely learned features specific to the one matrix-generating family used throughout the
arc (`build_matrix_with_seed_and_n`: diagonal `{0.5} + linspace(-50,-1)` eigenvalues,
strictly-upper-triangular random coupling, magnitude 15.0). This experiment is designed to
separate the two.

## EstimandOps L0

**Question type:** Predictive. "Does a predictor for finite-window transient growth
`M_T(B)`, fit ONCE on the original matrix family at `T=1`, generalize (a) to other `T`
values on the SAME family and (b) to a STRUCTURALLY DIFFERENT matrix family at any `T`,
without refitting?" This is explicitly a generalization/transfer test, not a descriptive
in-sample fit — the whole point is testing whether the fitted relationship holds outside
the exact conditions it was fitted under.

## The dimensionless reduction (the actual proposed mechanism, checked below)

Target, per the user's framing: `M_T(B) = max_{0<=t<=T} ||exp(tB)||_2`. This arc's own
established convention additionally normalizes by the known asymptotic growth rate `W`
(the fixed positive eigenvalue, `W=0.5` throughout) to isolate transient overshoot from
trivial exponential growth:

```
M_T,W(B) = max_{0<=t<=T} ||exp(tB)||_2 / exp(W*t)
```

**Mechanism Claim Gate (Step 0a) — the triggering sentence:** "`M_T,W(B) = M_1,0(C)` where
`C = T*(B - W*I)`" — i.e. the finite-window, rate-normalized target at ANY `(T,W)` equals
the T=1, W=0 target applied to a single dimensionless rescaled matrix `C`. If true, a
predictor built once for `M_1,0(C)` automatically and correctly answers `M_T,W(B)` for
every `T` and `W`, simply by rescaling the INPUT matrix before computing the same feature
— exactly the dimensional consistency the user's route asked for.

**Check (algebraic, not just asserted):** `B` and `W*I` commute (any matrix commutes with a
scalar multiple of the identity), so `exp(tB)/exp(Wt) = exp(tB)*exp(-Wt*I) = exp(t(B-WI))`.
Substituting `tau = t/T` (so `t=tau*T`, `tau` ranges over `[0,1]` exactly when `t` ranges
over `[0,T]`): `exp(t(B-WI)) = exp(tau * T*(B-WI)) = exp(tau * C)`. Taking the max over the
matching ranges: `max_{0<=t<=T} ||exp(t(B-WI))|| = max_{0<=tau<=1} ||exp(tau*C)|| =
M_1,0(C)`. **HOLDS** — exact algebraic identity, no approximation, no numerical check
needed beyond a direct sanity test that the implementation doesn't contain a transcription
bug (see `tests/`, `test_dimensionless_reduction_identity_holds_numerically`).

## The predictor (reused, not redesigned)

Feature: `K_ref(C)` — H-B2-2's own `resolvent_reference_k` (imported unchanged), applied to
`C = T*(A - W*I)` instead of to `A` directly. Functional form: the arc's own established
single-feature log-log power law, `log(M_T,W) = intercept + exponent * log(K_ref(C))`,
fit via OLS on `log(K_ref(C))` vs `log(M_T,W)` — same methodology as H-B2-2's own
`refit_with_k_ref`, reused for consistency, not reinvented.

**Training set:** the arc's own stored 80-matrix train split (`H_B2_1X_RESULT["train_data"]`,
`build_matrix_with_seed_and_n`), evaluated at `T=1` (matching the arc's own established
convention exactly — no new randomness, no new matrices at the fitting stage).

## The claim (falsifiable)

Freeze the fitted `(intercept, exponent)` from the `T=1`, original-family fit. Test,
WITHOUT REFITTING:

1. **Transfer A (same family, new T):** the arc's own stored 30-matrix test split, at
   `T in {0.1, 0.3, 3, 10}` (in addition to the already-established `T=1` baseline). Compare
   predicted vs directly-computed `M_T,W`.
2. **Transfer B (new family, T=1):** a structurally different family — 2x2 rotation blocks
   (genuinely complex eigenvalue pairs, decay rate `-1` real part, frequency drawn per
   block) plus random coupling, breaking the original family's always-real-triangular-
   eigenvalue structure. Same `(intercept, exponent)`, no refit.
3. **Transfer C (new family, new T):** combine 1 and 2.
4. **Compute-cost comparison:** wall-clock cost of the predictor path (one `resolvent_reference_k`
   call per matrix per T) vs a direct grid-based `M_T,W` computation at comparable accuracy
   (matching `n_grid` in `measure_m1`'s own convention).

**CONFIRMED (transferable method):** RMSE (in log space, matching the arc's own reporting
convention) on Transfer B/C does not degrade drastically relative to Transfer A (same
order of magnitude, not a qualitative collapse) — evidence the predictor is tracking a
genuine dimensionless mechanism, not overfitting the original generator.

**REJECTED (idea closed, per the user's own pre-registered closure criterion):** the
advantage vanishes outside the original generator (RMSE degrades by an order of magnitude
or more on Transfer B/C relative to Transfer A), OR the predictor costs more compute than
direct approximation at matched accuracy.

## What this does NOT mean

1. A CONFIRMED verdict does NOT establish the predictor works for arbitrary matrix
   families — one alternative family (rotation blocks) is tested, not an exhaustive survey.
2. Does NOT re-litigate H-B2-1/H-B2-2's own established finding that `K_ref` only loosely
   bounds `M1` (efficiency 3.7-31%) — this experiment asks a different question
   (transferability across `T`/family), not tightness of the bound.
3. The dimensionless reduction identity (`M_T,W(B) = M_1,0(T(B-WI))`) is exact algebra, not
   itself under test — what IS under test is whether the fitted power-law relationship
   `M ~ K_ref^exponent`, calibrated once, remains accurate when evaluated on the rescaled
   input across new `T`/family conditions.
