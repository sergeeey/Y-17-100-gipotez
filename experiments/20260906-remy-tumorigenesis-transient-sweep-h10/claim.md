# claim.md — 20260906-remy-tumorigenesis-transient-sweep-h10

**Graph node:** `H-B7-10` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-9` (Relaxation Map: "A finer sweep (e.g. `4,5,6,7,8,9`) to pin down the exact
threshold — cheap, no new pipeline code, reuses `simulate_transient_clamp_multi` with a denser
`TESTED_DURATIONS`").

## EstimandOps L0 Gate

**Classification: CAUSAL.** Identical structure to `H-B7-9` — same intervention family
(`do(p21CIP=0, RBL2=0)` for `k` steps then released), same branch, same comparators
(`GROWTH_ARREST_STATE`, `PROLIFERATION_STATE`, the "second" `Growth_arrest` fixed point `H-B7-9`
identified). The 4 identifiability assumptions are trivially satisfied for the same reason as every
prior experiment in this bridge, and were already established in `H-B7-9`.

**Minimal Relaxation Rule compliance — genuinely ONE assumption changed:** `H-B7-9` tested
`k ∈ {1,3,10,30}`. This experiment changes ONLY the duration granularity to `k ∈ {4,5,6,7,8,9}` —
no new clamp targets, no new branch, no new pipeline logic. `simulate_transient_clamp_multi` is
reused UNCHANGED from `H-B7-9`'s own module.

## Why This Sweep, Specifically

`H-B7-9` found a clean binary split: `k=3` relapses to a second `Growth_arrest` fixed point, `k=10`
reaches `Proliferation`. The exact transition point was not determined — anywhere from `k=4` to
`k=10` was consistent with the data. This experiment tests every integer duration in the untested gap
to pin the transition down exactly, which is directly informative about the underlying mechanism: `H-
B7-6`'s traced escape route (removing `p21CIP`/`RBL2` lets `CyclinE1`/`CDC25A`/`E2F` positive feedback
take over) predicts the transition should correspond to the number of synchronous steps this specific
feedback loop needs to complete and become self-sustaining before release — a mechanistically
meaningful number, not an arbitrary cutoff.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Remy et al. 2015 network, same bistable branch as `H-B7-4`–`9`, `p21CIP`/`RBL2` clamped to 0 for exactly `k ∈ {4,...,9}` synchronous steps starting from `GROWTH_ARREST_STATE`, then released to fully unperturbed wild-type dynamics |
| **Falsifiable predicate** | There exists a single integer `k*` in `{4,...,9}` such that all `k < k*` relapse (to `Growth_arrest`, per the phenotype node) and all `k ≥ k*` reach `Proliferation` — i.e. a clean monotone threshold, not an alternating or non-monotone pattern |
| **Measurable outcome** | Final attractor's phenotype-node values for each of the 6 tested durations, compared against `H-B7-9`'s already-established boundary cases (`k=3` relapse, `k=10` escape) |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: `H-B7-9` is the only prior transient
test of this clamp pair; this experiment fills the specific gap it left open (exact threshold
location) and was pre-registered as the next step there. Not a repeat.

## Kill Criterion (set BEFORE running)

- **CONFIRMED (clean monotone threshold):** exactly one integer `k*` in `{4,...,9}` separates
  relapse from escape — all tested `k < k*` give `Growth_arrest`, all `k ≥ k*` give `Proliferation`.
- **REJECTED (non-monotone / no clean threshold):** the pattern is NOT monotone in `k` — e.g. some
  intermediate `k` relapses after a shorter or equal `k` already escaped, or the outcome is not
  binary (a third, distinct attractor appears) — would indicate the escape depends on more than
  simple duration (e.g. parity, or a more complex trajectory-dependent effect), a genuinely
  interesting negative result in its own right.

## What This Does NOT Mean

1. A CONFIRMED clean threshold at some specific `k*` does NOT generalize to other clamp pairs,
   branches, or models — it is a property of this specific mechanism's feedback-loop completion time.
2. Does NOT give a real-time (e.g. minutes/hours) duration — "steps" in this discrete synchronous
   Boolean abstraction have no direct physical time unit.
3. Does NOT test whether the SAME threshold holds from a different starting state within the
   `Growth_arrest` basin (e.g. from the "second" `Growth_arrest` fixed point `H-B7-9` found) — this
   sweep starts only from the original `GROWTH_ARREST_STATE`, matching `H-B7-9`'s own starting point.

## MCID

Binary, per tested `k`: does the model's own `Proliferation` phenotype node read `1` in the
post-release attractor? Threshold location itself (`k*`) is the headline result, cross-checked
against `H-B7-9`'s own already-independently-verified boundary cases.
