# H-B2-1z — claim.md

## Origin

H-B2-1y (confirmed) established that the shallow pseudospectrum-sampled K(A) estimate
underestimates a "deeper" (smaller-eps) estimate by a factor growing with K(A) itself
(bias slope ~1.62), and that this bias substantially explains the ~2.2-2.35 fitted
M1~K(A) exponent found in H-B2-1w/1x. But H-B2-1y's own Honest Caveat #2 states the
"deep" estimate itself is NOT converged: all 16/16 sampled matrices hit the smallest
tested eps (1e-5) still climbing, with no plateau. That leaves the user's own framing of
the open question exactly correct: without a K(A) estimator that actually converges, any
K(A)-based regression's physical interpretation stays unclear.

This experiment tests one concrete way to get that convergent estimate: a **closed-form**
quantity that requires no pseudospectrum sampling at all.

## EstimandOps L0

**Question type:** Descriptive. "Does the closed-form eigenvalue condition number
kappa(lambda_1) bound/explain H-B2-1y's non-converging deep_k, and does refitting
M1~K(A) with this exact proxy change the exponent finding again?" No causal claim.

## The claim (falsifiable)

1. **Primary:** For H-B2-1y's own 16 sample matrices, the closed-form dominant-eigenvalue
   condition number `kappa(lambda_1) = 1/|w_1^H v_1|` (unit-normalized right eigenvector
   v_1 and left eigenvector w_1 of the dominant/rightmost eigenvalue) is an **upper bound**
   for `deep_k` in **all 16/16** cases, consistent with `deep_k` being a not-yet-converged
   approach toward `kappa(lambda_1)` as the true eps->0 asymptotic limit, per Trefethen &
   Embree ("Spectra and Pseudospectra", the standard result that this ratio is exactly the
   eps->0 limiting slope of the pseudospectral abscissa growth for a matrix with a SIMPLE
   dominant eigenvalue).
2. **Secondary:** Using `kappa(lambda_1)` (computed for free, no pseudopy, for the FULL
   H-B2-1x population: 80 train + 30 test matrices) in place of the shallow/deep
   pseudospectrum-sampled K(A) in the same log-log M1~K(A) OLS regression H-B2-1w/1x/1y
   used, on the SAME train/test split, gives a fitted exponent and held-out RMSE that can
   be directly compared to H-B2-1x's shallow-K RMSE (0.3652 on its fresh test).

## Kill criterion (pre-registered)

- **Claim 1 REJECTED if:** `deep_k > kappa(lambda_1)` for >=3/16 matrices (would falsify
  "kappa(lambda_1) is the ceiling deep_k is approaching," not just "not yet converged").
- **Claim 1 SUPPORTED if:** `deep_k <= kappa(lambda_1)` for all/nearly all 16, AND the
  Mechanism Claim Gate check (below) independently confirms the pipeline's own
  pseudospectrum extraction converges toward `kappa(lambda_1)` as eps shrinks on a small
  test matrix (not just consistent by coincidence on the 16-matrix sample).
- **Claim 2:** report exponent + RMSE regardless of Claim 1's outcome; no pre-registered
  pass/fail threshold beyond "does it move the H-B2-1y exponent finding further, in the
  same or a different direction" — this is exploratory given it's a genuinely new,
  independent (non-pseudospectrum) K(A) proxy, not a repeat of an already-tested claim.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence** (from the claim above): "kappa(lambda_1) is exactly the eps->0
limit of (alpha_eps(A)-alpha(A))/eps for a matrix with a simple dominant eigenvalue."
This is textbook spectral theory (Trefethen & Embree), but it has never been checked
against THIS project's own numerical pipeline (pseudopy.NonnormalAuto + the
matplotlib.tricontour extraction validated in H-B2-1v/1y) — a correct piece of abstract
math does not guarantee the specific numerical implementation actually exhibits the
predicted limit before hitting floating-point noise.

**Check:** build one small matrix (same family, n_dim=6, seed=9001 — not used anywhere
else in this arc), compute kappa(lambda_1) via the closed-form eig()+inv() formula, then
run the SAME deep_kreiss_estimate pipeline used throughout H-B2-1v/1y with an eps sweep
extended to 1e-7 (two orders of magnitude finer than H-B2-1y's 1e-5 floor). HOLDS if the
sampled ratio increases monotonically and closes to within a few percent of
kappa(lambda_1) by the finest eps tested; FAILS if the ratio overshoots kappa(lambda_1),
plateaus well short of it, or is non-monotonic.

## What this does NOT mean

1. Does NOT claim kappa(lambda_1) equals the true supremum K(A) in general — only that it
   is the eps->0 LOCAL limiting slope for a simple eigenvalue; K(A) could in principle
   exceed it if the ratio is non-monotonic and peaks at some intermediate eps (not what is
   observed here, but not ruled out for other matrix families).
2. Does NOT extend beyond this specific matrix family (fixed dominant eigenvalue 0.5,
   fixed spectral range [-50,-1], random strictly-upper-triangular coupling) — the
   dominant eigenvalue here is deterministic and always simple (gap 1.5 to its nearest
   neighbor, verified below), which is what makes the closed form applicable at all.
3. Does NOT retroactively change H-B2-1y's own verdict (ARTIFACT_HYPOTHESIS_SUPPORTED)
   — that conclusion did not depend on deep_k being fully converged, only on the bias
   growing with K(A) and the exponent moving toward linear on a matched subset, both of
   which hold regardless of this experiment's outcome.
4. A kappa(lambda_1)-based exponent, even if computed, is still an exponent fitted on
   N_DIM in {40,50} only (same population H-B2-1x/1y used) — it says nothing about
   whether the relationship holds at other N_DIM, a question this experiment does not
   reopen.
