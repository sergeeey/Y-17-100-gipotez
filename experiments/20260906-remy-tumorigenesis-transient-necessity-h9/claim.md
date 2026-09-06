# claim.md — 20260906-remy-tumorigenesis-transient-necessity-h9

**Graph node:** `H-B7-9` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-8` (Relaxation Map: "Transient `do(p21CIP=0, RBL2=0)` for a few steps, then
released — tests whether the escape survives release, the sharper reading of Kauffman's strict
claim... has not been run for ANY confirmed escape yet").

## EstimandOps L0 Gate

**Classification: CAUSAL.** Same structure as every prior H-B7 perturbation, but this is the FIRST
transient test applied to a clamp combination already known (via `H-B7-7`/`H-B7-8`) to succeed
PERMANENTLY. Comparator: the `Growth_arrest` starting fixed point, and `H-B7-8`'s own permanent
`do(p21CIP=0, RBL2=0)` result (CONFIRMED). The 4 identifiability assumptions are trivially satisfied
for the same reason as every prior experiment in this bridge.

**Why this is the sharpest available test of Kauffman's ORIGINAL hypothesis in this bridge:**
Kauffman's strict claim (already distinguished from the weaker permanent-clamp reading back in
`H-B7-2`'s own decision.md) is that a pathological state pre-exists as an attractor of the
UNPERTURBED network, reachable via a TEMPORARY push — not a claim about what happens while a gene is
held artificially off forever. `H-B7-3` attempted this test on the small Fauré model and found it
`TASK_INFEASIBLE` (no multi-attractor structure to reveal). `H-B7-4` moved to the Remy model
specifically because it has genuine multistability, but every subsequent H-B7 test on this branch
(`H-B7-4` through `H-B7-8`) used a PERMANENT clamp. This experiment is the first to ask the strict
question on a branch and clamp combination already proven to work permanently: does `Proliferation`
survive being released back to the network's own unperturbed dynamics, or does the system relapse?

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Remy et al. 2015 network, same bistable branch as `H-B7-4`–`8` `(DNA_damage=0, EGFR_stimulus=0, FGFR3_stimulus=1, Growth_inhibitors=1)`, `p21CIP` and `RBL2` clamped to 0 for exactly `k` synchronous steps starting from `GROWTH_ARREST_STATE`, then RELEASED back to their own wild-type rules and run to a fresh attractor under fully unperturbed dynamics |
| **Falsifiable predicate** | For at least one tested `k`, the system settles (after release) into an attractor with `Proliferation=1, Growth_arrest=0` — i.e. the SAME wild-type attractor `H-B7-4`'s `pyboolnet` scoping already showed exists in this branch, now reached via a temporary push rather than a permanent rule change |
| **Measurable outcome** | Final attractor's phenotype-node values for each tested `k`, compared against `H-B7-8`'s permanent-clamp result and the `GROWTH_ARREST_STATE`/`PROLIFERATION_STATE` references |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: `H-B7-3` is the only prior transient
experiment in this bridge, and it targeted a DIFFERENT network (Fauré) with a DIFFERENT, smaller
clamp set (`Rb`/`p27` alone) that turned out to lack the multi-attractor structure needed at all. No
prior transient test exists for the Remy network or for the `p21CIP`/`RBL2` pair specifically — this
is a genuinely new test, not a repeat.

## Kill Criterion (set BEFORE running)

Test durations `k = 1, 3, 10, 30` synchronous steps (matching `H-B7-4`'s own duration set, for direct
comparability), each starting fresh from `GROWTH_ARREST_STATE`.

- **CONFIRMED (strict Kauffman claim supported):** at least one tested `k` reaches `Proliferation=1`
  after release — the pathological state is reachable via a temporary push and PERSISTS once the
  network is returned to its own unperturbed dynamics. This would be the FIRST confirmation of
  Kauffman's STRICT original claim anywhere in this bridge (every prior CONFIRMED result, `H-B7-2`'s
  `do(Rb=0)` and `H-B7-7`/`H-B7-8`'s multi-hit combinations, required the clamp to remain PERMANENT).
- **REJECTED (relapse):** all tested `k` return to `Growth_arrest` after release — would mean the
  `p21CIP`/`RBL2`-mediated escape, while real under a permanent clamp (`H-B7-8`), requires the clamp to
  be sustained; a temporary push alone is insufficient to cross the basin boundary permanently.

## What This Does NOT Mean

1. A CONFIRMED result would validate the STRICT hypothesis for THIS specific branch, clamp pair, and
   set of tested durations — not a general claim that transient perturbations always suffice in this
   model or in real biology.
2. A REJECTED result would not contradict `H-B7-7`/`H-B7-8`'s own CONFIRMED verdicts — those used
   PERMANENT clamps and remain valid on their own terms; this experiment tests a stricter, additional
   claim, not the same one.
3. Does NOT test durations beyond `k=30` — if all four tested durations relapse, a longer duration
   remains formally untested, though `H-B7-4`'s own prior finding (30 steps already well beyond this
   network's natural settling time in every other experiment) makes an even longer clamp an unlikely
   missing ingredient, not formally ruled out.

## MCID

Binary, per tested `k`: does the model's own `Proliferation` phenotype node read `1` in the
post-release attractor? No partial-credit threshold — exhaustive attractor identity comparison,
cross-checked against `pyboolnet`'s independently-computed ground truth (inherited from `H-B7-4`).
