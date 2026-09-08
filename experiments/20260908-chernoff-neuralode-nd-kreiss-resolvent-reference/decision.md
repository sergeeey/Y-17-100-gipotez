# H-B2-2 — decision.md

## Result

### Positive control (seed=314, N=40)

`K_ref = 108.868` — matches this session's own independent scratchpad script (108.868,
before this experiment existed) and the external audit's own number (108.838) to within
grid/refinement precision. Confirms the combined `max(kappa, floored line search)` design
correctly recovers the audit's counter-example without reusing any of its code.

### Primary claim — how much of the population does the line search actually dominate?

**5 of 110 matrices (4.5%)**, dominance ratio (`K_ref/kappa`) range **1.016–2.173**:

| n_dim | seed | kappa(lambda_1) | K_ref | ratio |
|---|---|---:|---:|---:|
| 40 | 314 | 50.11 | 108.87 | **2.173** |
| 40 | 305 | 39.74 | 49.94 | 1.257 |
| 40 | 427 | 121.01 | 131.25 | 1.085 |
| 50 | 428 | 544.06 | 571.79 | 1.051 |
| 50 | 334 | 171.90 | 174.73 | 1.016 |

**seed=314 is the extreme case, not a representative one.** The other 4 dominant matrices
undershoot by only 1.6-26%, far less dramatic than the audit's own 2.17x example. This
directly answers the open question from ADR-077: `kappa(lambda_1)` is a GOOD proxy for
K(A) on 95.5% of this population, and even among the 4.5% where it undershoots, most of
that undershoot is small — seed=314 is close to a worst case, not typical.

### Secondary claim — does refitting M1~K(A) with K_ref change the picture again?

| model | K(A) proxy | features | exponent (log K) | RMSE on fresh test |
|---|---|---|---:|---:|
| H-B2-1x (reference) | shallow, pseudospectrum-sampled | 3-feature | 2.354 | 0.365 |
| H-B2-1y (16-matrix) | deep, pseudospectrum-sampled | 2-feature | 0.722 | n/a |
| H-B2-1z single-feature | kappa(lambda_1) | 2-feature | 0.656 | 0.524 |
| H-B2-1z two-feature | kappa(lambda_1) | 3-feature | 0.622 | 0.522 |
| **H-B2-2 single-feature** | **K_ref (this experiment)** | **2-feature** | **0.670** | **0.523** |
| **H-B2-2 two-feature** | **K_ref (this experiment)** | **3-feature** | **0.637** | **0.522** |

**Barely moved.** Correcting the 5 affected matrices' K(A) values (raising them, in some
cases substantially — seed=314 more than doubled) shifted the fitted exponent by only
+0.01 to +0.015 relative to H-B2-1z's kappa-only fit, and RMSE is unchanged to 3 decimal
places. This makes sense given the correction affects <5% of the training population,
and the fit is dominated by the other 95.5%. **H-B2-1z's core exponent finding (well below
quadratic, ~0.6-0.7) is ROBUST to the ADR-077 correction** — the correction was real and
necessary for interpretive honesty (kappa(lambda_1) is not the true K(A) in general), but
it does not materially change the arc's own headline predictive/exponent numbers.

## FL Step 8a — self-review (mandatory reviewer did not reach a verdict)

`Agent(reviewer)` was invoked once, scoped narrowly to just this experiment's 4 files, and
hit its 12-turn limit without producing a report (third consecutive reviewer timeout this
session — H-B2-1z hit it twice). No `SendMessage` tool was available in this environment to
resume it, and a fresh `Agent()` call would only duplicate work with no memory of partial
progress (per this session's own memory: "resume-stalled-agent-with-sendmessage"). Not
treated as reviewer approval — self-review substituted, documented honestly below rather
than silently absorbed, per the standing lesson from an earlier incident this same project
("don't let agent caps silently substitute for FL Step 8a").

Two concerns were checked directly, matching what a reviewer would likely have flagged:

1. **Is `x/sigma_min((alpha+x)I-A)` actually a valid lower bound for K(A)?** Proven, not
   just asserted: for any real `x>0`, let `z=alpha+x` and `eps_z=sigma_min(zI-A)`. By
   definition `z` lies in the `eps_z`-pseudospectrum of A (since `sigma_min(zI-A)<=eps_z`
   trivially holds with equality). `alpha_{eps_z}(A)`, the rightmost real part over that
   pseudospectrum, is therefore `>= Re(z) = alpha(A)+x`, so `x <= alpha_{eps_z}(A)-alpha(A)`,
   giving `x/eps_z <= (alpha_{eps_z}(A)-alpha(A))/eps_z <= K(A)` by definition of the
   supremum. This holds for EVERY `x`, regardless of whether `x` happens to be exactly the
   pseudospectral abscissa at that eps level — the formula is a valid lower bound
   unconditionally, not merely under some assumption about `z` being the extremal point.
2. **Could the 300-point log-spaced grid + narrow local-refinement window miss a sharper,
   narrower peak between grid points?** Checked directly: re-ran all 5 line-search-dominant
   matrices with a 10x denser grid (3000 points, wider refinement window). Result: IDENTICAL
   to 4 decimal places on every matrix (e.g. seed=314: 108.8680 both times). The local
   refinement step (a continuous bounded optimizer, not just grid-point selection) is
   robust to grid density here — no narrow-peak risk found in practice for this matrix
   family. Script not committed (a quick confirmatory check, not a new claim requiring its
   own artifact) — result recorded here per integrity.md's Verify-Output principle.

Not independently checked (real, disclosed limitation, not glossed over): the complex-plane
question (real-axis-only vs. full 2D search) remains open exactly as claim.md's own "What
This Does NOT Mean" #1 already stated before this experiment ran.

## FL Step 0a Mechanism Claim Gate

Pre-registered in claim.md, based on a same-session pre-check (7 matrices, `x_lo=1e-8`
never exceeded `kappa(lambda_1)` for the 6 non-dominant ones) — **HOLDS**, confirmed at
population scale by `test_line_search_floor_does_not_silently_clip_a_real_interior_maximum`
(seed=314's found `x_star` sits at ~0.72, over 7000x the floor, not pinned against it).

## Kill Analysis

**What was killed:** the assumption (implicit in the audit's own presentation, and in
this experiment's own initial framing) that seed=314's 2.17x undershoot was representative
of the whole population. It is not — it is close to the worst case among 110 matrices; the
median/typical undershoot when the line search dominates at all is much smaller (1.05-1.26x
for 4 of the 5 affected matrices), and 95.5% of matrices are unaffected entirely.

**What was NOT killed:** the correction's core interpretive point (kappa(lambda_1) is not
provably the true K(A) in general, ADR-077) — that remains true and was never about
population-average magnitude, only about the incorrectness of the "closes the question"
claim for ANY matrix, which a single counter-example already settles regardless of how
rare it turns out to be.

## What This Does NOT Mean

1. Does NOT prove `K_ref` equals the true supremum K(A) exactly — real-axis-only search,
   per claim.md's own hedge; a full complex-plane sweep across the population was not run
   (too expensive), only a small same-session check that did not fully resolve the
   question (grid coarseness there, not genuine off-axis dominance, explained the observed
   gap — see claim.md "What This Does NOT Mean" #1).
2. Does NOT explain WHY these specific 5 matrices (out of 110) have an interior maximum
   while the other 105 do not — an open structural question, not investigated here.
3. Does NOT mean the pseudopy-based pipeline (H-B2-1u through 1y) was without value — it
   correctly identified the qualitative bias direction; this experiment's contribution is
   a cheaper, more precise REPLACEMENT going forward, not a retroactive verdict on past
   work's usefulness at the time it was done.

## Go/No-Go

**PROMOTE.** Positive control reproduces the audit's own number; the population-scale
finding (4.5% affected, mostly mildly) is genuinely new information not available from
either H-B2-1z or the audit's single counter-example alone; the refit shows H-B2-1z's
exponent finding is robust to the correction, closing the "newly open" question ADR-077
left unresolved.

## Pearl Registry Update

New row: `K_ref = max(kappa(lambda_1), floored real-axis line search)` is a reusable,
general, cheap (no pseudopy) reference computation for K(A) in this matrix family — worth
recording as the arc's final answer to "how do we get a numerically reliable K(A)",
superseding both the pseudopy-sampling approach (H-B2-1u-1y) and kappa(lambda_1) alone
(H-B2-1z) as the recommended method for any future work in this arc needing K(A).
