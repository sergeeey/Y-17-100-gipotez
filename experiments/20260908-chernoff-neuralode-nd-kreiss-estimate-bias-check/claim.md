# claim.md — 20260908-chernoff-neuralode-nd-kreiss-estimate-bias-check (H-B2-1y)

**Graph node:** `H-B2-1y` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (targeted diagnostic test
of a specific, named alternative hypothesis about an already-confirmed predictive result)
**Parent:** `H-B2-1x` (K(A) exponent robust and sharpened: 2.354, 95% CI [2.190, 2.518] on 80
training points — clearly super-linear, but the literature search for Option B found no directly
matching theorem for this exponent)

## Why This Experiment, Specifically — User's Own Choice, This Session

A bounded literature search (WebSearch, this session) for a theoretical explanation of the
`M1 ~ K(A)^2.2-2.5` pattern found the classical linear bound (Spijker 1991: `M(A) <= e*n*K(A)`)
and active research on tighter, structure-specific bounds, but NO directly matching quadratic
result. Rather than force-fit a citation (Gate 4 / Scientism Detection, `artifact-provenance-
gates.md`) or invest in an unbounded, uncertain analytical derivation, the user chose the
cheapest differentiating alternative: **test whether the super-linear exponent is a genuine
property of `M1` vs. `K(A)`, or an ARTIFACT of `K(A)` itself being an unconverged, systematically
biased LOWER BOUND** (established in `H-B2-1u`'s Convergence Caveat and independently confirmed
in `H-B2-1v`: the grid/circle-based `K(A)` estimate keeps growing with no plateau as `eps` shrinks,
for large-K matrices specifically).

**The specific mechanism under test:** if the DEGREE of underestimation (`true_K / measured_K`)
itself grows with `measured_K` (i.e., matrices that already show a LARGER apparent `K(A)` are
underestimated by a LARGER relative factor — plausible, since `H-B2-1v` found convergence depth
scales with the matrix's own true `K(A)`), then regressing `M1` against the systematically
UNDER-estimated `measured_K(A)` could produce an apparent super-linear exponent even if the TRUE
relationship between `M1` and the (unreachable) TRUE `K(A)` is closer to the classical linear
form. This is a concrete, falsifiable alternative to "M1 genuinely scales as K(A)-squared."

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Does a deeper (still not fully converged, but substantially less
biased) `K(A)` estimate change the fitted exponent of `M1` against it, on the SAME subset of
matrices? Not a new predictive claim — a diagnostic re-measurement.

## FL Step 0a — Mechanism Claim Gate

**Triggering sentence, checked here, not asserted bare:** "the shallow K(A) estimate's bias grows
with the matrix's own true K(A)" is exactly the kind of behavioral claim this gate exists for.
The check IS this experiment (comparing bias factor against shallow K(A) directly, not assumed).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | 16 matrices, stratified across `H-B2-1x`'s own TRAIN population's `K(A)` range (30.2 to 221.5), reusing EXACT (n_dim, seed) pairs already in that TRAIN set — no new matrices, only a deeper measurement of already-studied ones |
| **Falsifiable predicate** | EITHER (a) `log(bias_factor)` correlates significantly and positively with `log(shallow_K)` AND refitting `M1` against `deep_K` on this subset gives an exponent measurably closer to 1 (linear) than the shallow-K exponent on the SAME subset — supports the artifact hypothesis; OR (b) bias factor is roughly CONSTANT across the K range, and/or the deep-K exponent stays close to the shallow-K exponent — the super-linear pattern is a genuine property of M1 vs. K(A), not an estimation artifact |
| **Measurable outcome** | Per matrix: `shallow_K` (already known), `deep_K` (new, via `pseudopy.NonnormalAuto` + `H-B2-1v`'s validated `matplotlib.tricontour` extraction, eps range extended an order of magnitude deeper than `H-B2-1v`'s own check); `bias_factor = deep_K/shallow_K`; regression of `log(bias_factor)` on `log(shallow_K)`; two exponents (shallow-K-based, deep-K-based) fit on the SAME 16-point subset for a fair, matched comparison |

## FL Step -3: Novelty Check

No prior "deep vs. shallow K(A)" bias-factor analysis anywhere in this arc — `H-B2-1v` checked
convergence behavior (does the SEQUENCE plateau) on 3 matrices, but never regressed the bias
factor against the shallow estimate itself, and never re-fit the M1 exponent using a deeper K.
Confirmed novel application of already-validated tools.

## Kill Criterion (set BEFORE running)

- **Bias factor grows with shallow_K (positive, significant slope) AND deep-K exponent measurably
  lower than shallow-K exponent on this subset:** supports the artifact hypothesis — the
  super-linear pattern is (at least partly) a measurement-depth artifact, not a clean law. Would
  mean `H-B2-1w/1x`'s exponent should be reported with this caveat, and Option B's target
  (deriving "why K^2") is chasing a moving target, not a fixed one.
- **Bias factor roughly constant, OR deep-K exponent stays close to shallow-K exponent:** the
  super-linear pattern survives a deeper measurement — genuine evidence AGAINST the pure-artifact
  explanation, strengthening (not proving) that `M1` really does scale super-linearly with the
  TRUE `K(A)`, not just with however deep this arc's finite compute happens to measure it.

**Honest, pre-registered limitation:** even the "deep" `K(A)` estimate here is NOT the true,
fully-converged Kreiss constant — `H-B2-1v` already showed no plateau even at `eps=0.0001` for
large-K matrices. This experiment tests whether going SUBSTANTIALLY deeper changes the picture
directionally, not whether it reaches the true value. A null result on the artifact hypothesis
(bias factor not increasing) is informative; it cannot fully rule out that an even deeper,
computationally infeasible measurement would eventually show one.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1w`'s `K_MODEL_WINS` verdict regardless of outcome — K(A)
   (however measured) still beat both comparators on the original held-out test.
2. A confirmed artifact does NOT mean `K(A)` is useless as a predictor — it would mean the
   specific EXPONENT value needs a caveat, not that the predictor itself fails.
3. Does NOT constitute a full resolution of Option B either way — this is a diagnostic test of
   ONE specific, named alternative hypothesis, not an exhaustive search for all possible
   explanations.

## MCID

Slope and p-value of `log(bias_factor) ~ log(shallow_K)`; difference between the deep-K and
shallow-K fitted exponents on the same 16-point subset — both reported honestly regardless of
direction.
