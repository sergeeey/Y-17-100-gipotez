# H-B7-16 — decision.md

## Result

### Mechanism Claim Gate — HOLDS with an important qualification found in the process

Confirmed (`diag_async_mechanism_check.py`, scratchpad, not part of the committed pipeline):
asynchronous dynamics reaches a stable, readable phenotype, but a SINGLE-POINT readout is
unreliable (a real trajectory flip observed 500 micro-steps after a "settled"-looking state); a
30-round windowed-majority vote is stable (purity 0.97–1.00 across 20 spot-checked trials) and was
adopted as the eventual-fate estimator for the full experiment.

### The synchronous "sharp threshold" blurs into a genuine probabilistic transition

`fate_distribution_by_k_at_j1` (200 trials/condition, both branches):

| k | branch_1 P(Proliferation) | branch_2 P(Proliferation) |
|---|---|---|
| 1 | 7.0% | 7.5% |
| 2 | 18.5% | 18.0% |
| 3 | 46.5% | 39.0% |
| 4 | 60.5% | 58.5% |
| 5 | 75.0% | 74.0% |
| 6 | 82.5% | 86.0% |

Synchronous dynamics gave a step function at `k*=5` (0% below, 100% at/above). Asynchronous
dynamics gives a smooth, monotone S-curve spanning `k=1..6` with real probability mass on BOTH
outcomes at every tested `k` — even `k=1` (deepest into the "safe" zone) shows a real ~7%
Proliferation rate, and `k=6` (deepest into "unsafe") shows a real ~14–18% relapse rate. The
release-timing decision itself is now inherently probabilistic under this update semantics, not
just its observability.

### M1 (2 markers) — DEGRADED-BUT-INFORMATIVE, statistically real but narrowly misses the
### pre-registered practical-significance bar

| | `j=0` | `j=1` | difference |
|---|---|---|---|
| M1 `{Growth_arrest, Proliferation}` accuracy | 79.4% | 88.3% | **+8.92 pp** |

Two-proportion z-test (conservative, treats `j=0`/`j=1` as independent though they share a paired
clamp trajectory — a stricter test would show an even smaller p-value): `z=8.45`, far exceeding
`|z|=1.96` — the improvement is real, not sampling noise, at `N=2400` trials/condition-set.
**However, `8.92 pp` is narrowly BELOW claim.md's own pre-registered `10 pp` MCID for practical
significance**, set before this result was seen. Per this repo's own MCID discipline, this must be
reported honestly as a real-but-borderline effect, not rounded up to "clearly meaningful."

### M2 (4 markers, `+p21CIP, +RBL2`) — a materially different picture from the synchronous case

| | `j=0` | `j=1` | difference |
|---|---|---|---|
| M2 accuracy | 79.4% | **94.96%** | **+15.58 pp** (`z=16.60`) |

M2's improvement clears BOTH the statistical bar and the `10 pp` MCID decisively. More
importantly: **at `j=1`, M2 (94.96%) significantly outperforms M1 (88.29%)** — `+6.67 pp`,
`z=8.40`. This is a genuine, statistically robust divergence from H-B7-13/14/15's own synchronous
finding, where augmenting M1 with `p21CIP`/`RBL2` made ZERO difference (identical collision under
both marker sets, at every tested `j`). **Under asynchronous update, marker augmentation DOES
help** — the "waiting one step is all you need, more markers don't matter" conclusion from the
deterministic case does not transfer.

### Ceiling is no longer tautological

`ceiling_full_state` accuracy: `91.9%` at `j=0`, `98.6%` at `j=1` — NOT `100%`, unlike the
synchronous case where observing the full state trivially guaranteed a correct prediction. Under
genuinely stochastic dynamics, even complete current-state knowledge does not perfectly determine
a stochastic future — a real conceptual difference from H-B7-13/14/15's deterministic ceiling,
correctly reflected in the data rather than assumed away.

## Verdict

**DEGRADED-BUT-INFORMATIVE**, per claim.md's own pre-registered kill criterion — NOT "ROBUST"
(M1 alone does not reach the pre-registered `≥90%` bar at `j=1`; it reaches `88.3%`). The
timing-based observability mechanism from H-B7-14/15 SURVIVES under asynchronous update in a
real, statistically significant, but weakened form — asynchrony introduces genuine irreducible
noise that a 2-marker set cannot fully resolve. The sharper, more complete picture: **the
combination of `j=1` timing AND the 4-marker augmentation (M2) reaches 95%, closer to (but still
below) the 98.6% ceiling** — a materially different, more nuanced conclusion than either
"timing alone suffices" (H-B7-13/14/15, synchronous) or "markers alone suffice" (never
established, since even M2 at `j=0` was only 79.4%).

**Sharpest defensible statement, narrow scope:**

> Under general-asynchronous update, `{Growth_arrest, Proliferation}` observed one async round
> after release predicts the trial's own eventual (windowed-majority) fate with `88.3% ± ~1pp`
> accuracy (`N=2400`), a statistically significant but practically-borderline `8.9pp` improvement
> over instant observation (`79.4%`). Adding the two directly-clamped nodes (`p21CIP`, `RBL2`)
> raises this to `95.0%`, a clearer, decisive improvement — unlike the synchronous case, marker
> augmentation genuinely helps under asynchronous dynamics. Neither marker set reaches the
> `98.6%` ceiling achievable from full-state observation, itself below 100% because the dynamics
> are genuinely stochastic.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the specific expectation (named directly in claim.md's own "ROBUST" branch)
that H-B7-14/15's clean, exact `j*=1` sufficiency would transfer UNCHANGED to asynchronous
dynamics. It does not — accuracy drops from 100% (exact, synchronous) to 88.3% (M1) / 95.0% (M2)
under async, and M1's improvement narrowly misses the pre-registered practical-significance bar.

**What was NOT killed:**
- The QUALITATIVE direction of H-B7-14/15's finding: observing later (j=1) is still better than
  observing at the instant of release (j=0), under BOTH marker sets, with high statistical
  confidence.
- The underlying mechanism (CyclinE1/RBL2 feedback taking time to visibly commit) plausibly still
  operates under async — consistent with M2's stronger performance (the augmented markers ARE the
  feedback loop's own nodes) — though this experiment does not directly trace the mechanism the
  way H-B7-13's original diagnosis did.

**Relaxation Map:**
- **Remove** the "2 markers only" restriction: M2's stronger performance suggests searching for an
  even better marker set (or a slightly larger `j`) could close more of the remaining gap to the
  98.6% ceiling — a concrete, named, cheap next step.
- **Weaken** the "single fixed `j`" assumption: a policy that waits until markers STABILIZE (not a
  fixed round count) was already named as untested in H-B7-14's own Relaxation Map — even more
  relevant now that async shows real within-window purity variation (occasional sub-1.0 purity in
  the Mechanism Claim Gate check).
- **Replace:** rule-perturbation robustness (the OTHER half of the user's named "option 2") remains
  completely untested — a separate, structurally different robustness question.

## Revival Condition

Not applicable in the REJECT sense (this is DEGRADED-BUT-INFORMATIVE, not a kill). Forward-looking
next steps, cheapest first: (1) search a slightly larger marker set or `j` to see how close the gap
to the 98.6% ceiling can be closed; (2) test rule perturbations (the untested half of option 2);
(3) characterize WHY M2 helps mechanistically under async but not sync (a genuine open question,
not yet explained, only observed).

## FL Step 8a — Independent Reviewer (mandatory: statistically substantial new claim, multiple
moving parts — RNG, windowed-majority readout, paired-seed design — any of which could hide a
subtle bug that would misleadingly shift these numbers)

**Partial completion, honestly reported — not all 3 originally-planned checks finished.** A
first reviewer invocation, scoped to 3 checks (RNG-pairing reproducibility, M1/M2 accuracy
correctness + small-scale reproduction, ceiling-not-100%-is-not-a-hash-collision), hit its
per-invocation turn limit twice in a row without completing (a real, logged methodology finding —
see LEDGER: 3 bundled checks requiring code execution exceeded this reviewer type's turn budget
for this task's complexity, where narrower single-check scoping has repeatedly succeeded
elsewhere this session).

**Check 2 (the headline numeric claim) was re-scoped to a single, tightly-focused invocation and
COMPLETED: `[CONFIRMED-REAL]`.** Independently: (a) hand-verified `weighted_accuracy` on an
8-entry synthetic domain (hand-computed 6/8=0.75, function returned 0.75 exactly); (b)
reconstructed the full pipeline from scratch (parsed the .bnet file, built `wild_type_rules`/
`clamped_rules` independently); (c) ran a SMALLER version of the experiment (k∈{4,5}, branch_1
only, N=30/condition, distinct seeds) and confirmed the QUALITATIVE pattern reproduces exactly:
`M2(j=1)=0.9167 ≥ M1(j=1)=0.8833`, both `j=1` values exceed their `j=0` counterparts
(`M1: 0.7833→0.8833`, `M2: 0.7833→0.9167`) — matching the full-scale run's direction and
rough magnitude despite the ~7x smaller sample.

**Check 1 (RNG-pairing) was NOT independently reviewer-verified, but WAS self-checked
(`diag_h16_rng_pairing_check.py`, scratchpad)** after dropping it from the reviewer's scope: the
clamp phase (`start_state → k rounds under clamped_rules → clamp-phase-end state`) is confirmed
deterministic given `(start, k, seed)` — re-derived twice with a fresh `random.Random(seed)` each
time, identical result both times, for `k∈{4,5}` × 2 seeds. This confirms the STRUCTURAL claim
(same seed ⟹ identical clamp-phase-end state, so `j=0`/`j=1` calls with the same seed genuinely
share one clamp trajectory and diverge only in the release-phase micro-steps consumed afterward)
— though this is `[VERIFIED-SELF]`, not independently reviewer-verified.

**Check 3 (ceiling-not-100%-is-not-a-hash-collision) was NOT independently completed and NOT
self-checked** — dropped from scope after the turn-limit issue. This is a real gap in the
verification, named explicitly, not glossed over: the ceiling's sub-100% accuracy interpretation
rests on the author's own reading of the code and data only. Treat the DEGRADED-BUT-INFORMATIVE
verdict as resting on `[CONFIRMED-REAL]` for the core M1-vs-M2 comparison (Check 2), `[VERIFIED-
SELF]` for the RNG-pairing structural correctness (Check 1), and `[HYPOTHESIS]`-tier (asserted,
not independently or self re-derived) for the ceiling-not-100% interpretation specifically
(Check 3) — the raw `overall_accuracy < 1.0` NUMBER itself is directly read from committed
`metrics/run.json`, only the "not a grouping-logic artifact" INTERPRETATION is unverified.

## Skeptic Concerns (self-review, pending independent verification above)

- "N=200/condition — is this Monte Carlo sample size actually enough to trust 88.3% vs 79.4%?" →
  **Checked**: two-proportion z-test gives `z=8.45` at the pooled `N=2400` level — the difference
  is not plausibly sampling noise, though per-condition (N=200) breakdowns were not individually
  significance-tested (a coarser but honest limitation, named here).
- "Same-seed pairing between j=0 and j=1 trials could introduce a subtle correlation that
  invalidates the independence assumption in the z-test" → **Accepted limitation, explicitly
  flagged in the z-test's own reporting above** — a proper paired test (e.g. McNemar's) would
  likely show an even smaller p-value (paired designs reduce variance), so the independence
  assumption here is CONSERVATIVE, not liberal; the qualitative conclusion is not put at risk by
  this simplification.
- "Windowed-majority-vote fate estimator could itself be biased toward whichever fate is 'sticky'
  under async, independent of the true underlying trajectory" → **Not fully ruled out** — an
  alternative fate estimator (e.g. state at a much longer, fixed single timepoint) was not
  cross-checked against the windowed-majority approach at scale, only spot-checked for stability
  in the Mechanism Claim Gate diagnostic. Named as an open limitation, not resolved here.

## Scope note

Continuation of the observability sub-arc within Bridge 7 (H-B7-13 → H-B7-14 → H-B7-15, all
synchronous), addressing the asynchronous-update half of the user's own named "option 2"
(2026-09-10: robustness/generalization). Does not touch H-B7-13/14/15's own synchronous results,
which stand unchanged — this is a separate, new claim about a different update semantics, honestly
reported with genuine statistical uncertainty rather than the prior arc's exact combinatorics.
