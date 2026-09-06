# claim.md — 20260906-remy-tumorigenesis-crossbranch-h11

**Graph node:** `H-B7-11` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-9`/`H-B7-10` (Relaxation Map: "checking whether the same pattern (p21CIP+RBL2
suffice) generalizes to one of the 7 other multistable branches in the model").

## EstimandOps L0 Gate

**Classification: CAUSAL.** Same structure as `H-B7-8`: a permanent `do(p21CIP=0, RBL2=0)`
intervention, compared against this branch's own `Growth_arrest`-phenotype starting fixed point and
its own independently `pyboolnet`-verified `Proliferation` attractor. The 4 identifiability
assumptions are trivially satisfied for the same reason as every prior experiment in this bridge.

**Compute-First check performed BEFORE designing this experiment (per `H-B7-3`'s own established
discipline):** re-enumerated all 16 input branches via `pyboolnet.compute_attractors()` first (see
`data/branch_scoping.md`). Found only ONE other branch with genuine phenotype divergence (`GA, GA,
PR`) besides the one used throughout `H-B7-4`–`H-B7-10`: `(DNA_damage=0, EGFR_stimulus=1,
FGFR3_stimulus=1, Growth_inhibitors=1)`. This scoping ALSO surfaced and corrected a minor factual
error in `H-B7-4`'s own original count (7, not 8, of 16 branches are multistable — documented as a
dated correction addendum in `H-B7-4`'s `Data_README.md`, not a silent rewrite).

## Why This Branch, Specifically

It is the ONLY other branch offering the same structural precondition (phenotype divergence within
one branch) that made the original branch usable for Kauffman-hypothesis testing at all — differing
from the tested branch by exactly ONE input bit (`EGFR_stimulus`: 0→1), verified to produce
`GROWTH_ARREST`/`PROLIFERATION` states differing from their branch-1 counterparts at exactly that one
bit position. This is the cleanest possible generalization test: minimal setup difference, maximal
comparability.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Remy et al. 2015 network, SECOND bistable branch `(DNA_damage=0, EGFR_stimulus=1, FGFR3_stimulus=1, Growth_inhibitors=1)`, `p21CIP` and `RBL2` clamped to 0 permanently, starting from this branch's own `GROWTH_ARREST_STATE_2` |
| **Falsifiable predicate** | The double clamp reaches an attractor with this branch's own `Proliferation` phenotype node reading `1` — the same qualitative pattern `H-B7-8` established on the FIRST branch |
| **Measurable outcome** | Final attractor's phenotype-node values, cross-checked against `PROLIFERATION_STATE_2` (independently `pyboolnet`-verified in `data/branch_scoping.md`) |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: no prior cross-branch generalization
test in this project. Every H-B7-4–10 experiment used the SAME single branch. This is the first test
of whether any finding in this bridge generalizes beyond that one branch.

## Kill Criterion (set BEFORE running)

- **CONFIRMED (pattern generalizes):** the permanent `do(p21CIP=0, RBL2=0)` clamp, on this second
  branch, reaches an attractor with `Proliferation=1` — the SAME qualitative escape `H-B7-8`
  established, on a DIFFERENT branch.
- **REJECTED (pattern does NOT generalize):** the clamp relapses to a `Growth_arrest`-phenotype
  attractor on this branch — would mean the `p21CIP`/`RBL2` sufficiency finding is specific to the
  first branch's exact configuration (e.g. its specific `EGFR_stimulus=0` signaling context), not a
  general property of this model's `Growth_arrest = p21CIP | RBL2 | RB1` OR-gate structure.

## What This Does NOT Mean

1. A CONFIRMED result on 2 of 7 multistable branches (both of the ONLY 2 phenotype-divergent
   branches that exist) is a strong but not exhaustive generalization — the other 5 multistable
   branches lack a `Proliferation` attractor entirely (per `data/branch_scoping.md`) and cannot be
   tested this way.
2. A REJECTED result would not contradict `H-B7-7`/`H-B7-8`'s own CONFIRMED verdicts on the first
   branch — those stand on their own; this experiment asks a strictly additional generalization
   question.
3. Does NOT test the transient version on this second branch — that remains a further, separate step
   if this permanent test succeeds.

## MCID

Binary: does this branch's own `Proliferation` phenotype node read `1` in the reached attractor? No
partial-credit threshold — cross-checked against `pyboolnet`'s independently-computed
`PROLIFERATION_STATE_2`.
