# H-CAT31-2 — decision.md

## Result

**Positive control passed cleanly:** `max |theta(G)*theta(Gbar)/n - 1| = 6.4e-14`, six orders of
magnitude below the pre-registered `1e-6` threshold, across all 6 `n` values (3000 total sampled
graphs, each checked against its own complement). `theta_via_lp` (reused unchanged from
`H-CAT31-1`) remains exact at this scale.

**No consistent arithmetic signal found, at either statistic checked:**

| Pair | var(X) ratio (composite/prime) | top-decile-contribution ratio | 95% CIs disjoint? |
|---|---|---|---|
| (127, 129) | 0.996 | 0.976 | No |
| (251, 255) | 0.865 | 0.874 | No |
| (509, 511) | 0.984 | 1.025 | No |

- **Variance direction is consistent** (composite always has slightly LOWER variance than its
  prime partner, all 3 pairs) but the effect is far from substantial (largest deviation from 1.0
  is 13.5%, well under the pre-registered `>=50%` bar for "substantial").
- **Top-decile-contribution direction is NOT consistent** (2 of 3 pairs: composite lower; 1 of 3:
  composite higher) — no signal at all on the specific tail-concentration statistic the
  reformulation `E[theta]/sqrt(n)-1 = E[cosh(X)-1]` was designed to probe.
- **Every pair's 95% bootstrap CI on the top-decile contribution overlaps its partner's** — the
  observed differences are consistent with sampling noise at `N_REPS=500` per `n`.

## Verdict

**REJECTED.** Neither pre-registered LEAD condition (consistent + substantial top-decile-
contribution difference with disjoint CIs, OR consistent + substantial variance difference) is
met. At this sample size (`N_REPS=500` per `n`, 3 pairs), there is no detectable trace of the
prime-vs-composite arithmetic class of `n` in either the variance or the tail-concentration
structure of `theta(G)/sqrt(n)`'s logarithm.

**What this does and does not close:**

- Closes: the SPECIFIC, pre-registered first test from `reports/2026-09-09-breakthrough-
  routes.md` Route 2 — divisor-richness of `n` (prime vs composite, at these 3 near-pairs, this
  sample size) shows no measurable footprint in the tail of `theta(G)/sqrt(n)`.
- Does NOT close: the report's broader Route 2 question (whether ANY arithmetic feature of `n`
  predicts extremes) — only this one specific, cheap first test. A different arithmetic feature
  (e.g. number of divisors rather than prime/composite binary, or a larger/different pair set)
  is untested. Per claim.md's own scope note, the report's harder "continuation filter" test
  (held-out predictive power) was never going to be reached without a positive signal at this
  first stage, and none was found.
- Confirms (side effect, not the main claim): `H-CAT31-1`'s own mean-ratio finding (`theta(G)/
  sqrt(n)` close to 1) is not concealing a bimodal or heavy-tailed structure that differs sharply
  by `n`'s arithmetic class — the individual-graph distributions at all 6 tested `n` look
  broadly similar in shape, which is itself a small piece of evidence (not proof) that the mean
  finding is not an averaging artifact hiding structured variance.

## FL Step 8a

**Not run.** Per `falsification-ladder.md`, Step 8a is mandatory for PROMOTE-shaped or surprising
findings — this is a clean REJECTED/null result with a passed positive control and a
straightforward, pre-registered decision rule; there is no surprising or promotable claim here to
subject to adversarial review. Skipping is per the rule's own scope, not an oversight.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the specific hypothesis that prime-vs-composite arithmetic class of `n`
produces a detectable, consistent difference in the tail/variance structure of `theta(G)/sqrt(n)`
at the 3 pre-specified near-pairs, at `N_REPS=500` per `n`.

**What was NOT killed:**
- The underlying reformulation itself (`E[theta]/sqrt(n)-1 = E[cosh(X)-1]`, an exact identity
  given the ensemble's complementation symmetry) — this is algebra, not a falsifiable empirical
  claim, and stands regardless of this experiment's result.
- `H-CAT31-1`'s own CONFIRMED finding (mean ratio near 1, flat log-log slope) — unaffected;
  Part B here is a genuinely different statistic (tail, not mean).
- The general possibility that SOME arithmetic feature of `n` matters — only prime-vs-composite,
  at these specific pairs and this sample size, was tested.

**Relaxation Map:**
- **Weaken the arithmetic predicate:** instead of a binary prime/composite split, use a
  continuous divisor-count or divisor-sum feature and test correlation with tail statistics
  across a wider, randomly-sampled set of `n` (not just 3 hand-picked pairs) — addresses the
  report's own "n=3 pairs is far too few" caveat directly.
- **Increase sample size:** `N_REPS=500` gives bootstrap CIs wide enough that even a real
  30-40% effect could hide inside them; a 5-10x larger `N_REPS` (2500-5000) would meaningfully
  narrow the CIs before concluding "no effect," not just "no effect detectable at this budget."
- **Remove the near-pair constraint:** the report's own pairs were chosen for being numerically
  close (differ by 2-4), which also makes `theta`'s scale nearly identical between partners — a
  wider spread of `n` values might make a real but small effect easier to separate from noise.

## Revival Condition

Not a hard kill (no theorem-level contradiction found, only a null result at a specific, cheap
first test) — parking as `weak_alive` (Rescue Review vocabulary) is more honest than `killed`.
**Revival condition:** a materially larger `N_REPS` (per the Relaxation Map above) OR a
continuous divisor-based feature (rather than binary prime/composite) shows a signal on a WIDER,
non-cherry-picked set of `n` values. Absent that, this specific narrow question (prime vs
composite, these 3 pairs) is adequately answered by this experiment and does not need repeating.

## Scope note

Direct execution of `reports/2026-09-09-breakthrough-routes.md` Route 2's own pre-specified first
bounded test, run because the report's two higher-priority routes (`H-B3-2` = Route 3, `H-B2-3` =
Route 4) are both already REJECTED and Route 1 (Forsythe minimal-counterexample construction) is
blocked pending a multi-session certificate-reproduction effort (ADR-091). Reuses `H-CAT31-1`'s
own cross-validated `theta_via_lp`/`sample_circulant_neighbors` unchanged — no new theta-
computation machinery introduced. A clean, honestly-reported null result, not a dead end for the
broader project: two concrete follow-up directions are named in the Relaxation Map above, neither
launched here.
