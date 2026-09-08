# decision.md — 20260908-chernoff-neuralode-nd-kreiss-estimate-bias-check (H-B2-1y)

## Result

**ARTIFACT_HYPOTHESIS_SUPPORTED — a real, substantial, quantified effect.** The shallow `K(A)`
estimate (this arc's production computation, `EPS_VALUES` down to 0.02) systematically and
increasingly underestimates the true Kreiss constant as the apparent (shallow) `K(A)` grows:

| Quantity | Value |
|---|---|
| `log(bias_factor) ~ log(shallow_K)` slope | **1.62** (R²=0.63) |
| `M1 ~ K(A)` exponent, shallow K, this 16-matrix subset | 2.193 |
| `M1 ~ K(A)` exponent, deep K, SAME subset | **0.722** |
| Bias factor range across the 16 matrices | 1.57x to **84.3x** |

**The bias is not small or uniform — it is large and grows with the matrix's own apparent K(A).**
The worst case (seed=329, N=50): shallow `K(A)=221.5`, deep `K(A)=18,669` — the production
estimate was low by a factor of **84**. The best case (seed=307, N=40, the smallest-K matrix in
the population): bias only 1.57x — nearly converged already. This confirms `H-B2-1v`'s own finding
(convergence depth scales with the matrix's true K) in a new, quantitative, directly load-bearing
way: it is not just that large-K matrices haven't fully converged — the GAP between the shallow
estimate and a deeper one grows roughly as `shallow_K^1.6`, meaning the shallow-K-based regression
in `H-B2-1w`/`H-B2-1x` was fitting against a systematically MORE compressed version of reality at
the high end of the range than at the low end.

## Interpretation — What This Means For the K^2 Finding

The `M1 ~ K(A)^~2.2-2.5` pattern (`H-B2-1w`, `H-B2-1x`) is **substantially explained by this
artifact**, not a clean physical law. Using a deeper (still not fully converged — see caveat
below) `K(A)` measurement on the exact same 16 matrices, the fitted exponent drops from 2.19 to
**0.72** — closer to the classical linear relationship implied by the Kreiss Matrix Theorem's own
`e*n*K(A)` bound than to a quadratic law. This directly answers the question the literature search
(this session, before this experiment) could not: there is no need to find a new theorem for
"why K-squared" — the apparent K-squared behavior looks like it emerges FROM the measurement bias
itself, not from new physics.

## Honest Caveat — the Deep Exponent (0.72) Is Itself Uncertain, Not the New Final Answer

1. **Small sample, huge dynamic range.** 16 points, with bias factors spanning nearly two orders
   of magnitude (1.6x to 84x) — the deep-K exponent fit is dominated by a few high-leverage points
   (the two largest-K matrices, seeds 304 and 329, both N=50, both with bias >70x). No confidence
   interval is reported here (unlike `H-B2-1x`'s careful 95%-CI discipline) — this experiment was
   scoped as a DIAGNOSTIC (does the artifact hypothesis survive at all), not a final precision
   re-estimate. A proper CI on the deep-K exponent is a natural next step, not done here.
2. **"Deep" is still not "true" — VERIFIED directly, not assumed.** Checked which `eps` level in
   `DEEP_EPS_VALUES` produced each matrix's winning ratio (`max(deep_ratios_by_eps)`): **16 out of
   16 matrices** hit their maximum at the SMALLEST tested `eps=0.00001`, with the ratio still
   climbing steeply at that boundary in every single case (e.g. seed=329: 223.7 at eps=0.02 ->
   18,669.2 at eps=0.00001, roughly doubling with each halving of `eps` all the way down, no
   inflection visible). This is the exact same "100% boundary hits, no plateau" pattern `H-B2-1u`
   found for its own shallow estimate — confirming `deep_k` here is a LESS shallow lower bound, not
   a converged one. The bias factors reported here (1.6x-84x) are themselves demonstrably
   UNDERSTATED — the true bias is larger still, and grows faster for the already-highest-K
   matrices (seed=329's ratio nearly doubled between the last two eps steps alone, more than the
   smaller-K matrices did). This means the deep-K exponent of 0.72 should be read as "moved
   correctly in direction, itself still an underestimate of how far the correction should go" —
   the true corrected exponent could plausibly sit anywhere from here up toward 1, or even further,
   not a settled final value.
3. **The exponent moved BELOW 1 (0.72), not just toward 1.** This is worth flagging honestly, not
   glossed over: the classical Kreiss bound structure suggests M1 should scale AT LEAST linearly
   with the true K(A) in general expectation (informally), so a sub-linear fitted exponent of 0.72
   could indicate (a) genuine sub-linear behavior for this specific matrix family, (b) remaining
   noise/small-sample instability given the huge leverage of 2 extreme points, or (c) the "deep"
   K(A) is STILL sufficiently biased (per caveat 2) that the fit hasn't yet reached its true
   asymptotic value. Not resolved here — reported as an open observation, not explained away.

## FL Step 8a — Skeptic-Style Self-Check (informal)

**Concern anticipated:** "with only 16 points and 2 extreme high-leverage points driving both the
bias-slope AND the exponent-shift results, could this whole finding be an artifact of those 2
points specifically, not a general pattern?" **Response, checked directly:** removing the two most
extreme points (seeds 304, 329) by eye from the printed per-matrix table still shows a clear,
monotonic-ish bias growth across the remaining 14 points (e.g. seed=307 bias=1.57 -> seed=336
bias=15.9, a real trend well before the two most extreme cases) — the pattern is not manufactured
by 2 outliers alone, though they do amplify the fitted slope's exact magnitude. A rigorous
leave-two-out refit is a natural follow-up, not performed here (scope discipline — this was a
diagnostic, the qualitative direction is what was pre-registered as the falsifiable question).

## Kill Analysis

**What this experiment killed:** the interpretation of `M1 ~ K(A)^2.2-2.5` as a clean,
measurement-independent physical law for this matrix family. It is, at minimum, SUBSTANTIALLY
contaminated by the shallow K(A) estimate's own growing underestimation bias.

**What this experiment did NOT kill:** `H-B2-1w`'s `K_MODEL_WINS` predictive result — the shallow
`K(A)` (however biased) is STILL a monotonic, useful correlate of the true `K(A)`, and the fitted
regression using it STILL beat both comparators on held-out RMSE. A biased-but-monotonic feature
can still be a good PREDICTOR even when its regression coefficient does not correspond to a clean
physical exponent. The predictive win and the "K-squared law" interpretation are separable, and
only the latter is weakened here.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1w`'s `K_MODEL_WINS` verdict — predictive performance is
   unaffected; only the mechanistic interpretation of the exponent is revised.
2. Does NOT establish 0.72 (or any other value) as the TRUE exponent — see the honest caveats
   above; this is a diagnostic result pointing away from "clean K-squared law," not a replacement
   precise estimate.
3. Does NOT mean `H-B2-1u`'s own reported efficiency ratios need a numeric correction in this
   experiment — but it DOES substantially strengthen `H-B2-1u`'s own caveat that reported
   efficiency values are upper bounds likely far from the truth: for the two most extreme matrices
   here, the TRUE ceiling (using deep K) would be dozens of times larger than what was reported,
   meaning true efficiency is correspondingly far lower than even the already-conservative
   "median 3.7-6.3%" figure for those specific matrices.
4. Does NOT mean deeper K(A) measurement is now a solved problem — `pseudopy.NonnormalAuto`
   remains expensive (~100-150s/matrix even at this depth) and still not fully converged; a
   genuinely precise K(A) estimate for this matrix family remains an open computational challenge.

## Relaxation Map / Next Steps (not auto-launched)

- Report this finding back to the user as the answer to "why K-squared" — the honest answer is
  "it looks like it mostly wasn't a real law, it was a measurement artifact; the corrected
  picture is closer to (and possibly below) linear, though the exact corrected exponent remains
  uncertain given the small diagnostic sample here."
- A properly-scoped follow-up (if wanted): a larger sample (30+ matrices) with the SAME deep-K
  method, WITH confidence intervals (matching `H-B2-1x`'s own discipline), to get a trustworthy
  corrected exponent estimate — a real cost/compute commitment (each deep-K matrix takes
  100-150s), not undertaken automatically here.
- Consider whether `H-B2-1w`'s predictive model should be re-fit using deep-K features for a
  cleaner, less-biased predictor — separate question from the mechanistic one answered here.

## Pearl Registry Update

Major finding: for this matrix family, the shallow (production) `K(A)` estimate's bias grows
approximately as `bias_factor ~ shallow_K^1.6` — meaning any interpretation of `H-B2-1u/1w/1x`'s
shallow-K-based numbers as precise physical quantities (not just useful, monotonic predictive
features) should be treated with substantial caution, especially for the highest-K matrices in any
population (bias factors of 10-84x observed here). Any future experiment in this arc computing a
"true" K(A)-dependent quantity should budget for deep measurement (100-150s/matrix via
`pseudopy.NonnormalAuto`) rather than reusing the arc's cheaper shallow `EPS_VALUES` convention,
if precision (not just monotonic ranking) matters for that use case.
