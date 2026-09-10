# H-CAT31-3 — claim.md

## Origin

Direct follow-up from `reports/2026-09-10-deep-external-novelty-audit.md`'s own Track 1 finding
(re-analysis of `H-CAT31-1`'s already-committed `metrics/run.json`): `Var(log(theta(G)/sqrt(n)))`
appeared to scale as `n^-0.96` across the 9 points of the original sweep (`n=10..2560`), matching
`exp(mean_X + var_X/2)` against the committed `mean_theta_over_sqrt_n` to 4-5 digits. Track 2's
primary-source check confirmed the companion paper (Bandeira, Blasiok, Dmitriev, Faure, Kireeva,
Kunisky, "The Lovász number of random circulant graphs," arXiv:2502.16227, Feb 2025) proves the
EXACT mean inequality `E[theta(G)] >= sqrt(n)` but does **not** discuss variance or concentration
of `theta(G)/sqrt(n)` at all — leaving this the single strongest unaddressed candidate across the
whole audit. User directly requested deepening this specific finding: wider `n` range, more
replicates per `n`, and an explicit test of whether the exponent is consistent with exactly `-1`
(i.e. `Var(log(theta/sqrt(n))) =~ C/n`) rather than merely "close to -0.96 on 9 noisy points."

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Estimating how a population variance (`Var` of
`log(theta(G)/sqrt(n))` over the random-circulant-graph ensemble at `p=0.5`) scales with `n`. Not
causal, not a claim about any single graph — a statement about the ensemble's own distribution.

## Origin and design rationale

**Reused unchanged (Minimal Relaxation Rule — only the sweep design changes, not the
computation):** `theta_via_lp` from `experiments/20260909-lovasz-theta-random-circulant-graphs/
run.py` — already cross-validated this session against two independent closed-form checks
(`theta(C_5)=sqrt(5)` exactly; a C_9-isomorphic complement graph via the `theta(G)*theta(Gbar)=n`
identity) and against the primary-source LP formulation (Table 1, arXiv:2603.29571) read
directly from the PDF, not from memory. Not re-validated here — reusing an already-verified
primitive, per this project's own established discipline (e.g. H-B7-28 reusing H-B7-26/27's
`check_isomorphism` unchanged).

**Compute-First Check (timing, before committing to a range):** benchmarked `theta_via_lp` at
`n=500,1000,2000,3000,4096` directly this session: `0.17s, 0.94s, 6.68s, 34.38s, 88.68s`
respectively — scaling far steeper than the module's own `O(n^2)` docstring claim (empirical
local exponent ~2.8-4.0 in this range, likely `scipy.linprog`'s HiGHS solver switching internal
strategy on the dense `n x n` constraint system as `n` grows, not a flaw in this experiment's
own code). **This bounds the feasible range**: `n=4096` at the user's own suggested `N=200-500`
reps would cost 5-12+ hours, infeasible this session. Chose a sweep reaching `n=3000` with
tapered reps at the top end instead (see below) — a real, disclosed compute-budget compromise,
not silently substituted for the requested range.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `Var(log(theta(G)/sqrt(n)))` for `G` a random dense circulant graph on `n` vertices, `p=0.5`, as a function of `n` |
| **Falsifiable predicate** | Does a log-log OLS fit of this variance against `n`, across a wider range and more replicates than the original 9-point sweep, give a slope consistent with exactly `-1`? |
| **Measurable outcome** | Slope +/- 95% CI from OLS on `log(Var_hat(n))` vs `log(n)`; whether the CI contains `-1` and excludes `-0.5`/`-2` (nice alternative exponents that would also look "close to -1" on noisy data) |

## Kill Criterion (set BEFORE running — locked in before any new solve)

Sweep design (n values and rep counts, chosen for a ~35-45 minute total compute budget given the
timing benchmark above, NOT after seeing any new results):

| n | reps |
|---|---|
| 32 | 300 |
| 64 | 300 |
| 128 | 300 |
| 256 | 250 |
| 512 | 200 |
| 1024 | 150 |
| 1536 | 100 |
| 2048 | 80 |
| 3000 | 40 |

For each `n`, compute `X_i = log(theta_i / sqrt(n))` over the reps, then the sample variance
`Var_hat(n)` (ddof=1) and its own bootstrap 95% CI (2000 resamples, per the user's own explicit
request for a bootstrap/finite-size check). Fit `log(Var_hat(n)) = a + b*log(n)` via OLS across
all 9 points, and separately via **weighted** OLS (weights = inverse of each point's own
bootstrap variance, since precision varies sharply with rep count across 2 orders of magnitude
in `n`) — report both, since an unweighted fit could be dominated by the noisiest (largest-n,
fewest-reps) points.

- **CONFIRMED (`Var =~ C/n`, i.e. exponent -1 survives)** if: the weighted-OLS 95% CI for `b`
  contains `-1.0` AND excludes both `-0.5` and `-2.0` (i.e. the data actually discriminates `-1`
  from these two "also plausible on 9 noisy points" alternatives, not just fails to reject them
  all).
- **WEAKENED/INCONCLUSIVE** if the CI contains `-1.0` but ALSO contains `-0.5` or `-2.0` (data too
  noisy to discriminate) — reported honestly as such, not rounded up to CONFIRMED.
- **REJECTED (exponent is NOT `-1`)** if the 95% CI excludes `-1.0` entirely — the point estimate
  and its own CI are reported as the actual finding regardless.

**Positive control:** re-verify `theta_via_lp` against the SAME two closed-form checks
`H-CAT31-1` already used (`theta(C_5)=sqrt(5)`, C_9-isomorphic case via `theta*theta_bar=n`) as a
substrate sanity check before trusting any new large-n solve — cheap, catches an environment/
dependency drift since the original run (`scipy`/`highs` version changes could silently alter LP
behavior).

**Negative control:** at `p=0` (empty graph) or `p=1` (complete graph), `theta` is degenerate
(`n` or `1` respectively) and `Var(log(theta/sqrt(n)))` over repeated seeds must be exactly `0`
(no randomness in the graph, if `theta_via_lp` is correctly deterministic given `c`) — confirms
the variance-estimation code itself can register zero variance, not just report noise as a
default.

## What This Does NOT Mean

1. Does NOT establish a theoretical upper bound of order `1/n` — an empirical exponent estimate,
   however precise, is not a proof. A survives-this-check result is `POSSIBLE-NOVEL-SPECIAL-CASE`
   at best (per the audit's own vocabulary), a candidate for further theoretical work, not a
   theorem.
2. Does NOT extend to `p != 0.5` — the entire self-complementarity argument behind `E[theta]>=
   sqrt(n)` (and by extension, plausibly, this variance-scaling question) is specific to `p=0.5`;
   deliberately not varied here (see the audit report's own explicit warning against this — at
   `p!=0.5` the ensemble is no longer self-complementary and `sqrt(n)` is the wrong normalization
   entirely).
3. Does NOT reach `n=4096` as the user's own suggested upper bound — capped at `n=3000` by a
   disclosed compute-budget constraint, not a silent substitution.
4. Does NOT re-validate `theta_via_lp` from scratch — reuses the already-verified primitive
   (Minimal Relaxation Rule), only re-runs the 2 cheapest closed-form checks as a substrate
   sanity gate.

## MCID

Not formally applicable to a scaling-exponent question — the qualitative bar is the CI-based
discrimination test in the Kill Criterion above (does the data distinguish `-1` from `-0.5`/`-2`,
not just fail to reject `-1` among many untested alternatives).
