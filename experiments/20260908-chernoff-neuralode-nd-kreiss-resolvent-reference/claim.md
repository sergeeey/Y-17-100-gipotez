# H-B2-2 — claim.md

## Origin

H-B2-1z's own correction (ADR-077, external discovery audit + independent reconfirmation
this session) established that `kappa(lambda_1)` is NOT the true K(A) in general: on
N=40,seed=314, an independent direct resolvent-norm search found `K(A) >= 108.87` while
`kappa(lambda_1) = 50.11` — a 2.17x undershoot, because the true supremum for THAT matrix
is achieved at a FINITE eps (x~0.72), not in the eps->0 limit that `kappa(lambda_1)`
represents. The user chose (technical fix, not a strategy pause) to replace the whole
pseudopy-sampling pipeline with a direct resolvent-norm reference and refit Claim 2.

A quick follow-up check (this session, before writing this claim.md) on 7 matrices found
that only 1 of 7 (seed=314) has an interior maximum exceeding `kappa(lambda_1)`; the other
6 (including 4 of H-B2-1y's own 16-matrix sample) have `kappa(lambda_1)` matching the true
max to within numerical noise. This experiment checks whether that 1-in-7 pattern holds
across the FULL population, not just a small sample.

## EstimandOps L0

**Question type:** Descriptive. "What fraction of the H-B2-1x population has a true K(A)
exceeding kappa(lambda_1), by how much, and does refitting M1~K(A) with this new reference
change the exponent/RMSE picture again?" No causal claim.

## The reference computation

`K_ref(A) = max(kappa(lambda_1), line_search_floored(A))`, where:
- `kappa(lambda_1)`: closed form (H-B2-1z, unchanged), handles the eps->0 limit exactly,
  with no numerical precision loss (unlike letting an SVD-based line search approach x=0
  directly, which was found in this session's own pre-check to just noisily re-discover
  kappa with less precision).
- `line_search_floored(A)`: `max_{x in [1e-4, 60]} x / sigma_min((alpha(A)+x)*I - A)`,
  log-spaced coarse grid (300 points) + local refinement (`scipy.optimize.minimize_scalar`,
  bounded, `xatol=1e-10`). Catches interior maxima like seed=314's x~0.72 that
  `kappa(lambda_1)` alone misses. `x_floor=1e-4` deliberately stays well clear of the
  near-x=0 SVD precision-loss region (this session's own pre-check confirmed going to
  `x_lo=1e-8` never exceeds `kappa(lambda_1)` for matrices where kappa already dominates
  -- there is nothing being cut off by the floor).

No `pseudopy`, no tricontour, no triangulated grid anywhere in this computation.

## The claim (falsifiable)

1. **Primary:** Across the FULL H-B2-1x population (80 train + 30 test, 110 matrices
   total), the fraction of matrices where `K_ref(A) > kappa(lambda_1) * 1.001` (i.e. the
   line-search component actually dominates, not just numerical noise) is reported exactly,
   not assumed from the 7-matrix pre-check.
2. **Positive control:** `K_ref` for N=40,seed=314 must reproduce the audit's own number
   (108.84, independently reconfirmed by this session at 108.868) to within the precision
   of this experiment's own grid+refinement — this matrix is already in the population, no
   separate re-computation needed, just a direct read of that row's result.
3. **Secondary:** refit M1~K(A) using `K_ref` (single-feature and two-feature, matching
   H-B2-1x's own model shape) on the same 80/30 train/test split H-B2-1x/1w/1z used;
   compare exponent and RMSE against H-B2-1x (shallow), H-B2-1y (deep, 16-matrix), and
   H-B2-1z (kappa(lambda_1), 80-matrix).

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "the floored line search (x>=1e-4) does not miss any interior
maximum below the floor that `kappa(lambda_1)` doesn't already capture at least as well."
**Check:** already run informally before writing this file (see `Origin` above) — for the
6 non-seed-314 matrices tested, letting the search go all the way to `x_lo=1e-8` (well
below the floor) never exceeded `kappa(lambda_1)`, it just converged toward it noisily.
**HOLDS**, cited here rather than re-run as a separate step, per the Mechanism Claim Gate's
own cost discipline (a script already run this session, not re-run redundantly). A formal
re-verification on a larger sample is folded into the main run (any matrix where the
floored search's best point sits suspiciously close to `x_floor` itself is flagged in the
output, not silently accepted).

## What this does NOT mean

1. Does NOT prove `K_ref` equals the true supremum K(A) exactly — it is a real-axis-only
   search (no complex-plane sweep across the full population, that would be far more
   expensive); an earlier same-session complex-plane check on 3 matrices found LOWER values
   than the real-axis search due to grid coarseness, not genuine off-axis dominance, but
   this was not resolved to a fully rigorous conclusion — `K_ref` remains a lower bound,
   just a much tighter one than `kappa(lambda_1)` alone or any prior pseudopy estimate.
2. Does NOT retroactively change H-B2-1y's own verdict — independent of this correction.
3. Does NOT establish which specific structural feature of seed=314 (vs. the 6 other tested
   matrices) causes its interior maximum — an open question, not investigated here.
4. A refit exponent from this experiment, even if it changes again, is still fitted on
   N_DIM in {40,50} only — same scope limitation as every experiment in this arc.
