# claim.md — 20260906-remy-tumorigenesis-crossbranch-transient-h12

**Graph node:** `H-B7-12` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-11` (Relaxation Map: "Transient version of `do(p21CIP=0, RBL2=0)` on this second
branch, mirroring `H-B7-9`'s test on the first — checks whether the same duration threshold (or a
different one) applies").

## EstimandOps L0 Gate

**Classification: CAUSAL.** Same structure as `H-B7-9`/`H-B7-10`, but on the SECOND branch (`H-B7-11`:
`DNA_damage=0, EGFR_stimulus=1, FGFR3_stimulus=1, Growth_inhibitors=1`). Comparator: this branch's own
`Growth_arrest`-phenotype starting fixed point (`GROWTH_ARREST_STATE_2`, from `H-B7-11`) and its own
independently `pyboolnet`-verified `Proliferation` attractor (`PROLIFERATION_STATE_2`). The 4
identifiability assumptions are trivially satisfied for the same reason as every prior experiment in
this bridge.

**Two combined questions, deliberately tested together (justified deviation from strict one-step-
at-a-time, matching the precedent set in `H-B7-2`'s combined non-normality+mixed-sign test in
bridge B2):** (1) does the transient (not permanent) version of the clamp ALSO escape on this second
branch, mirroring `H-B7-9`'s confirmation on the first? (2) if so, is the exact duration threshold
the SAME `k*=5` `H-B7-10` found on the first branch, or branch-specific? Both are cheaply answered by
the same duration sweep, using the exact same `k` values `H-B7-9`/`H-B7-10` already tested
(`k=1,3,4,5,6,9,10,30`), so no new design decisions are needed — this is a direct replication of the
established protocol on new data, not a new instrument.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Remy et al. 2015 network, SECOND branch (`H-B7-11`), `p21CIP`/`RBL2` clamped to 0 for `k ∈ {1,3,4,5,6,9,10,30}` synchronous steps starting from `GROWTH_ARREST_STATE_2`, then released to fully unperturbed wild-type dynamics |
| **Falsifiable predicate** | (a) at least one tested `k` reaches `Proliferation=1` after release, persisting without further clamping; (b) IF (a) holds, whether the same `k*=5` threshold from `H-B7-10` reproduces exactly on this branch |
| **Measurable outcome** | Final attractor's phenotype-node values per tested `k`, compared against `H-B7-9`/`H-B7-10`'s first-branch boundary cases |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: no prior transient test on the second
branch exists. Direct replication of the `H-B7-9`/`H-B7-10` protocol on new data — not a repeat of an
already-answered question.

## Kill Criterion (set BEFORE running)

- **CONFIRMED-GENERALIZES, SAME THRESHOLD:** at least one `k` escapes, AND the transition point is
  exactly `k*=5` (same as `H-B7-10`) — the threshold is a property of the escape MECHANISM
  (`CyclinE1`/`p21CIP`/`RBL2` feedback timing), not the specific branch.
- **CONFIRMED-GENERALIZES, DIFFERENT THRESHOLD:** at least one `k` escapes, but the transition point
  differs from `k*=5` — the escape generalizes qualitatively, but the exact timing is branch-specific
  (plausibly via `EGFR_stimulus`'s downstream effects on the same feedback loop's speed).
- **REJECTED:** no tested `k` escapes — the transient-escape finding from `H-B7-9`/`H-B7-10` would be
  specific to the first branch, not a property of the underlying mechanism.

## What This Does NOT Mean

1. A CONFIRMED-SAME-THRESHOLD result does not prove `k*=5` is a universal constant of this class of
   mechanism — only that it is invariant to this SPECIFIC one-bit branch difference
   (`EGFR_stimulus`).
2. Does NOT test durations beyond `k=30` or below `k=1` — matches `H-B7-9`/`H-B7-10`'s own tested
   range exactly, for direct comparability.

## MCID

Binary, per tested `k`: does the model's own `Proliferation` phenotype node read `1` in the
post-release attractor for THIS branch? Threshold location (if any) is the headline result, compared
directly against `H-B7-10`'s `k*=5`.
