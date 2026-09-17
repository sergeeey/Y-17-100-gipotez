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

## Continuation (2026-09-18) — pre-registered continuous divisor-feature test: literal "LEAD," but a mandatory confound check (proposed independently before this specific result was seen) shows it is entirely explained by `n` itself — final honest verdict REJECTED

**Pre-registration (written and fixed BEFORE running any code):** per this experiment's own Revival Condition ("a continuous divisor-based feature... on a WIDER, non-cherry-picked set of `n` values"), tested whether `d(n)` (number of divisors) correlates with `var(X)`/`top_decile_contribution` across 17 odd `n` in `[81,567]`, deliberately chosen to span `d(n)` from 2 to 12 and to avoid recycling the original 3 pairs' exact `n` values. Reused `sample_n()` from this experiment's own `run.py` UNCHANGED (read-only import), `N_REPS=300` per `n`. Kill criterion fixed in advance: `LEAD` if `|Spearman rho(d(n), stat)| ≥ 0.5` with bootstrap 95% CI excluding 0, for EITHER statistic; `REJECTED` otherwise; `CRITERION_INVALID` if the positive control fails.

**Literal result of the pre-registered test:** positive control passed cleanly (`max_violation=9.03e-14`, six orders below the `1e-6` threshold, across all 17×300=5100 sampled graphs). `Spearman(d(n), var_X) = -0.7906` (`p=0.0002`), bootstrap 95% CI `(-0.953, -0.437)` — clears the pre-registered bar. `Spearman(d(n), top_decile) = -0.174` (CI includes 0, no signal on that statistic). **Per the literal, pre-registered criterion: `LEAD`.**

**Mandatory confound check — proposed independently, before this specific numeric result existed, precisely because a raw marginal correlation cannot distinguish "`d(n)` itself matters" from "`d(n)` is correlated with `n`, and `var(X)` is ALREADY known to decrease with `n`" (H-CAT31-1's own confirmed finding).** Checked directly: in this specific 17-`n` sample, `Spearman(n, d(n)) = 0.7685` (`p=0.0003`) — a strong, significant confound, not a minor nuisance. Multiple regression `log(var_X) ~ log(n) + d(n)` (`check_confound.py`): once `log(n)` is controlled for, `d(n)`'s own coefficient is `-0.0051` (`se=0.0107, t=-0.475, p=0.642`) — statistically indistinguishable from zero. Incremental `R²` from adding `d(n)` to a `log(n)`-only model: `0.0003` (`R²=0.9844` vs `0.9842`). An `F`-test for `d(n)`'s incremental contribution: `F=0.226, p=0.642`. **`d(n)` has no detectable explanatory power for `var(X)` beyond what `n` alone already explains — the raw correlation that triggered the literal "LEAD" verdict is entirely a byproduct of `d(n)` and `n` being correlated with each other in this sample, not evidence of an independent arithmetic-feature effect.**

**Corrected final verdict: `REJECTED`, not `LEAD`.** The pre-registered raw-correlation criterion was itself methodologically incomplete — it did not anticipate that a "wide, non-cherry-picked" sample spanning a range of `d(n)` values would, almost automatically, also span a wide range of `n` values (larger numbers have more room to accumulate divisors), making `n` and `d(n)` correlated by simple arithmetic necessity in any such sample, not a specific flaw of this particular selection. This is being corrected NOW, before writing the result down as a positive finding — not retroactively rationalized after an inconvenient result, per AOG-1 discipline: the confound-control regression was specified as necessary BEFORE this specific run's numbers were seen (the general concern — that a naive correlation test cannot separate a `d(n)`-effect from an `n`-effect when the two co-vary — is a standard, textbook statistical point, not a post-hoc excuse invented to explain away this particular "LEAD").

**Kill Analysis:** what is killed — the specific claim that `d(n)` (number of divisors), tested via a raw marginal correlation across this 17-`n` sample, shows an effect on `var(X)` independent of `n`'s own already-established scaling. What is NOT killed — the general possibility that SOME arithmetic feature of `n`, tested with a design that decorrelates it from `n` itself (e.g., matched `n`-bins with varying `d(n)` within each bin, or a much wider `n`-range where `d(n)` can vary more freely at fixed `log(n)`), might still show an effect; this specific test does not address that stronger design. **Revival condition, updated:** a follow-up would need to hold `n` (or `log n`) approximately fixed while varying `d(n)` — e.g., select multiple `n` within a narrow band (say `n∈[490,570]`) with `d(n)` ranging from 2 to 8+, so the confound is broken by design rather than needing to be controlled for statistically after the fact.

**Methodology lesson, `[REPEAT]`-worthy, matching this window's own dominant pattern one more time:** the pre-registered kill criterion for this specific test, though written honestly and fixed before running, was itself under-specified — it should have included the confound-control regression as part of the ORIGINAL pre-registration, not as an add-on check run only after the raw result came back. For any FUTURE correlational test in this project where the tested feature is expected to co-vary with a known covariate (here, `n` itself), the pre-registered criterion should be stated directly in terms of the PARTIAL/incremental effect, not the raw marginal correlation, to avoid needing this kind of after-the-fact (even if honest and pre-specified-in-spirit) rescue.

## Scope note

Direct execution of `reports/2026-09-09-breakthrough-routes.md` Route 2's own pre-specified first
bounded test, run because the report's two higher-priority routes (`H-B3-2` = Route 3, `H-B2-3` =
Route 4) are both already REJECTED and Route 1 (Forsythe minimal-counterexample construction) is
blocked pending a multi-session certificate-reproduction effort (ADR-091). Reuses `H-CAT31-1`'s
own cross-validated `theta_via_lp`/`sample_circulant_neighbors` unchanged — no new theta-
computation machinery introduced. A clean, honestly-reported null result, not a dead end for the
broader project: two concrete follow-up directions are named in the Relaxation Map above, neither
launched here.
