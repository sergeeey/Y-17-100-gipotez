# claim.md — 20260910-remy-tumorigenesis-observability-async-h16

**Graph node:** `H-B7-16` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-15` (THEOREM-LEVEL CONFIRMED, minimal `j*=1` sufficiency — but under SYNCHRONOUS
update only, explicitly flagged as untested for asynchrony in every prior claim.md in this arc).

## EstimandOps L0 Gate

**Classification: PREDICTIVE.** Unlike H-B7-13/14/15, the underlying dynamics are now genuinely
STOCHASTIC (general asynchronous update), so this is explicitly a probabilistic prediction question
— not a deterministic/exact one. The estimand shifts from "does M determine the fate exactly" to
"how accurately does M predict the fate's empirical distribution."

## Origin — user's own second named option (2026-09-10)

User named two possible next steps after H-B7-15's theorem-level result: (1) minimality of `j*=1`
— closed for free, see H-B7-15's addendum; (2) *"robustness/generalization: проверить, сохраняется
ли sufficiency при asynchronous update или rule perturbations."* This experiment addresses the
asynchronous-update half of option 2 (rule perturbations remain untested, a separate follow-up).

## Mechanism Claim Gate (Step 0a) — run BEFORE building the full Monte Carlo pipeline

**Triggering sentence:** the implicit design assumption "asynchronous dynamics from this protocol
converges to a readable, stable phenotype within a modest step budget" — untested before this
experiment, and NOT guaranteed (general-asynchronous Boolean networks can in principle cycle or
wander indefinitely).

**Check performed** (`diag_async_mechanism_check.py`, scratchpad): general-asynchronous update
(one uniformly-random node per micro-step, `n_free=35` micro-steps per "round," standard GA
convention), 5 trials each for `k=3,4,5,6` on branch 1, `j=1` round post-release, then a
30-round windowed-majority readout.

**Result: HOLDS, with an important qualification found in the process, not assumed beforehand.**
- Single-point readout (state at exactly `+500` extra micro-steps) is UNSTABLE for some trials —
  e.g. `k=5, trial=0`: `Proliferation=True` at the 1-round observation, but `Proliferation=False`
  after 500 more micro-steps (a genuine within-trajectory flip). A single-snapshot design would
  have been unreliable.
- **Windowed majority vote (30 round-checkpoints) is highly stable**: purity 0.97–1.00 across all
  20 tested (k, trial) combinations — once a trajectory settles into a phenotype region, it
  overwhelmingly stays there. This is the readout method adopted below.
- **Critically, the qualitative OUTCOME DISTRIBUTION differs from synchronous dynamics.**
  Synchronous `k=4` deterministically always relapses to `Growth_arrest` (H-B7-10/12/13). Under
  async, 5 independent trials at `k=4` split 3 `Growth_arrest` / 2 `Proliferation` — real
  stochastic variability where the synchronous case had none. The sharp `k*=5` threshold does not
  straightforwardly carry over; this experiment's job is to characterize how much it blurs, and
  whether `j=1` observability still helps under that blur.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Monte Carlo trials (`N=200` per condition) of the SAME clamp-release protocol under general-asynchronous update, for `k=1..6` (H-B7-15's own established exhaustive-orbit range) on both branches |
| **Falsifiable predicate** | Does `{Growth_arrest, Proliferation}` observed at `j=1` async round post-release predict the trial's own eventual (windowed-majority) fate more accurately than at `j=0` (release instant), and how does that accuracy compare to floor/ceiling baselines? |
| **Measurable outcome** | Per-marker-set weighted classification accuracy (majority-vote-per-bucket), at `j=0` vs `j=1`, compared to floor (`{DNA_damage}`) and ceiling (full 35-node state) |

## Design

Adds: `async_random_step` (one randomly-chosen node updates per micro-step, from `h1.
evaluate_expression` — reused unchanged), `run_async_trial` (clamp for `k` async rounds, release,
observe at `j` rounds, continue 30 more rounds for windowed-majority fate). Reuses H-B7-13's
`FLOOR_M`, `CEILING_M`, `CANDIDATE_M1`, `CANDIDATE_M2`, `PYBOOLNET_NODE_ORDER`, `BRANCH_INPUTS_1/2`,
`GROWTH_ARREST_STATE_1/2`, `CLAMPS` UNCHANGED via distinct-name import.

**Outcome metric (probabilistic generalization of H-B7-13/14/15's exact collision count):** group
trials by their marker-set projection at the tested `j`; within each group, the majority fate is
the group's prediction; purity = majority fraction; overall accuracy = purity averaged across
groups, weighted by group size. A purity of exactly 1.0 everywhere recovers the deterministic
"zero collisions" case exactly.

**`N_TRIALS=200` per (branch, k) condition, `k=1..6` × 2 branches = 12 conditions, 2400 trials
total** — cheap (each trial is ~1000 boolean-node evaluations, pure Python, no external solver).

## Kill Criterion (set BEFORE running)

- **ROBUST:** `j=1` accuracy for M1 is high (`≥90%`) and clearly exceeds `j=0` accuracy across the
  pooled domain — the timing-based observability finding (H-B7-14/15) survives, in a weakened
  (probabilistic, not exact) form, under asynchronous update.
- **DEGRADED-BUT-INFORMATIVE:** `j=1` accuracy exceeds `j=0` but stays well below the deterministic
  case's 100% (e.g. `60–90%`) — the mechanism partially survives, asynchrony genuinely adds
  irreducible noise the marker set cannot resolve.
- **NOT-ROBUST:** `j=1` accuracy is not meaningfully better than `j=0`, or both are close to the
  trivial majority-class baseline — the H-B7-14/15 timing mechanism does NOT transfer to
  asynchronous dynamics; a materially different marker set or protocol would be needed.

## What This Does NOT Mean

1. Does NOT claim asynchronous dynamics is the "more realistic" or biologically correct semantics
   — general-asynchronous is one standard convention among several (random-order, ROA;
   probabilistic asynchronous; etc.), chosen here as the cheapest standard alternative to
   synchronous, not as a claim about which is biologically true.
2. Does NOT test rule perturbations (structural robustness) — a separate, untested half of the
   user's own named option 2.
3. Does NOT re-derive or challenge H-B7-13/14/15's own SYNCHRONOUS results — those stand unchanged;
   this is a new, separate claim about a different update semantics.
4. `N=200` trials per condition is a Monte Carlo sample, not exhaustive — unlike H-B7-15's own
   exact orbit closure, this result carries genuine sampling uncertainty, to be reported honestly
   (e.g. with simple binomial-proportion context), not overclaimed as exact.

## MCID

Practical significance threshold: an accuracy improvement of `j=1` over `j=0` smaller than `10
percentage points` is not considered a practically meaningful timing effect, even if nominally
different — given `N=200`/condition, this threshold is well above sampling noise for the observed
effect sizes.
