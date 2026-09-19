# H-CAT31-4 — controls.md (PRE-REGISTERED before any solve)

## Substrate Gate (FL Step 2a) — must return READY before any sweep result counts

1. `theta_via_lp` on the 5-cycle equals `sqrt(5)` within 1e-6.
2. `theta(G) * theta(Gbar) = n` within 1e-4 on a random instance at prime `n = 67` (the identity
   is tight for vertex-transitive graphs; it also underlies the `E[X_n] = 0` control below).
3. Every LP solve must return `success`; a `nan` is a solver failure, it is logged and the
   instance is RE-DRAWN with the next seed only for `nan` (count reported). More than 2% `nan` at
   any `n` = `BLOCKED-INFRASTRUCTURE` for that `n`, never a result.

A `BLOCKED-INFRASTRUCTURE` or `UNTRUSTED-ENVIRONMENT` outcome is not evidence about the claim.

## Positive control (the fit machinery can recover a known exponent)

Synthetic `V_n = C/n` with multiplicative log-normal noise matching the design's relative SE
(`sqrt(2/(reps-1))` per `n`), 2000 simulated sweeps on the same `n` grid, analysed with the exact
fit routine used for the real data. Pass: the CI contains `-1` in between 92% and 98% of
simulations (nominal 95%).

## Power control (can the design see a slope of -0.913?)

Same simulation with true slope `-0.9126`. Report the fraction of simulated CIs that exclude `-1`.
Pass if this fraction is at least 0.60; otherwise the run is declared `UNDERPOWERED` in advance
and a P-MINUS-ONE result cannot be read as evidence for `-1`.

## Negative control (sampler and estimator can register zero)

At `p = 0` (empty graph) on `n = 67` with 5 seeds, `theta` is identical across seeds and the
variance is below 1e-10.

## Symmetry control (sampler bug detector)

At `p = 1/2` the ensemble is invariant under `G <-> Gbar` and `theta(G)*theta(Gbar) = n`, hence
`E[X_n] = 0` exactly. For each `n`, `|mean(X_n)| / (sd(X_n)/sqrt(reps)) <= 3.5`. A violation at
any `n` flags a sampler/solver defect and the sweep is not interpreted until it is explained.

## Sensitivity and no-collapse variants (all reported, none can change the locked category)

1. leave-one-out over the 8 primes (slope range);
2. drop the two smallest primes; 3. drop the two largest primes;
4. unweighted OLS instead of weighted;
5. Var estimated by median absolute deviation (robust) instead of sample variance;
6. bootstrap CI (2000 resamples of instances, refit each time) versus the t-interval;
7. a second, independent seed block for `n in {509, 1021, 2053}` (seeds offset by 5,000,000)
   to check that the point estimates replicate.

## Independent verification of the headline numbers

`analyze.py` and a separate `verify.py` (different implementation: `statsmodels`-free plain
numpy normal equations vs. `scipy.stats.linregress` with bootstrap weights) must agree on the
slope to 1e-6 given the same input rows.

## Stop rules

Compute budget is roughly 45 minutes wall clock on 12 processes. If `n = 4093` is not finished by
90 minutes, report the sweep without it, say so, and do not change the locked category
definitions. No re-runs after seeing the slope to "improve" it; a second seed block is allowed
only as control 7 above.
