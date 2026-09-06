# claim.md — 20260906-remy-tumorigenesis-transient-h4

**Graph node:** `H-B7-4` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-3` (Relaxation Map: "Test the SAME transient-perturbation logic on a Boolean network
KNOWN to have multiple attractors within one basin/branch"). This is that follow-up, using a real,
biologically-motivated candidate model verified to have the needed structure BEFORE committing to it.

## EstimandOps L0 Gate

**Classification: CAUSAL.** Same structure as `H-B7-2`/`H-B7-3`: `do(RAS≡1)` applied for a finite
window `k`, then released back to `RAS`'s own update rule, compared against the never-perturbed
comparator. The 4 identifiability assumptions are trivially satisfied for the same reason as every
prior experiment in this bridge (fully specified, exhaustively-verifiable deterministic mechanism).

## Compute-First Check (done BEFORE designing the perturbation)

Installed `pyboolnet` and ran `compute_attractors()` on the full 35-node Remy et al. 2015 bladder
tumorigenesis network (`data/remy_tumorigenesis.bnet`) BEFORE writing any perturbation logic. Found
**25 attractors across 16 input branches** (all combinations of the 4 stimulus nodes `DNA_damage`,
`EGFR_stimulus`, `FGFR3_stimulus`, `Growth_inhibitors`), with **8 of 16 branches showing genuine
multistability** (≥2 attractors under identical external input) — unlike the Fauré network (`H-B7-1`),
which `H-B7-3` showed has exactly one attractor per branch, making the strict Kauffman test
`TASK_INFEASIBLE` there.

**The specific branch chosen:** `(DNA_damage=0, EGFR_stimulus=0, FGFR3_stimulus=1,
Growth_inhibitors=1)` has 3 attractors, two with the `Growth_arrest` phenotype and ONE with the
`Proliferation` phenotype — under the IDENTICAL external signaling condition. This is the exact
structural precondition Kauffman's strict hypothesis requires: two qualitatively different cell fates
(quiescence-like vs. persistent proliferation) coexist as attractors of the SAME network under the
SAME environment, differing only in which one the trajectory has settled into.

**Cross-checked, not assumed:** independently re-verified with THIS project's own from-scratch
pipeline (`H-B7-1`'s `parse_bnet`/`compile_rules`/`synchronous_step`, reused unchanged) that the
`Growth_arrest` state `pyboolnet` reported for this branch really is a fixed point under synchronous
updating — confirmed. Two independent implementations (mine, `pyboolnet`) agree.

## The Test

Starting from the verified `Growth_arrest` fixed point in this branch, apply `do(RAS≡1)` — a transient
oncogenic RAS activation, biologically a highly standard cancer-relevant perturbation (RAS is one of
the most commonly activated oncogenes in human cancer; here it is a downstream signaling node, NOT
one of the 4 external "stimulus" inputs, so this is a genuine INTERNAL perturbation, not a change to
the environment) — for a finite window `k`, then release `RAS` back to its own rule
(`RAS, GRB2 | FGFR3 | EGFR`) and let the system settle. Does it return to `Growth_arrest`, or does it
reach the `Proliferation` attractor (or some other attractor) — all while `DNA_damage`,
`EGFR_stimulus`, `FGFR3_stimulus`, `Growth_inhibitors` remain FIXED at their branch values throughout
(verified post-hoc, not just assumed, since a bug could let them drift)?

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Remy et al. 2015 network, branch `(0,0,1,1)`, `RAS` clamped to 1 for a finite window `k` then released |
| **Falsifiable predicate** | At least one `(k, starting-state)` combination, released from the clamp, settles into the `Proliferation` attractor (or the second `Growth_arrest` attractor) instead of returning to the original `Growth_arrest` fixed point — while the 4 branch-defining input nodes remain unchanged throughout |
| **Measurable outcome** | Final attractor reached for several `k` values, compared against both known attractors in this branch |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: no prior use of `remy_tumorigenesis` or
any bladder-cancer Boolean model in this project. First use of `pyboolnet` (the installed package, not
just its bundled repository files) as an active computation tool in this project, rather than only a
source of `.bnet` rule files.

## Kill Criterion (set BEFORE running)

- **CONFIRMED (supports Kauffman's STRICT hypothesis, faithfully operationalized this time):** at
  least one transient `do(RAS=1)` perturbation, released, reaches `Proliferation` (or the other
  `Growth_arrest` attractor) instead of returning to the starting `Growth_arrest` state — a
  PRE-EXISTING attractor of the UNPERTURBED network, made reachable by a TEMPORARY push, with NO
  permanent rule change and NO change to the external environment. This is the clean, faithful
  confirmation `H-B7-2`/`H-B7-3` could not produce.
- **REJECTED:** every tested `(k, starting state)` combination returns to the original `Growth_arrest`
  fixed point — would mean this branch's basin structure, despite having multiple attractors overall,
  is still not reachable via THIS specific single-node transient perturbation (a narrower, still
  informative negative result — unlike `H-B7-3`, NOT logically forced in advance, since this network
  DOES have the required multi-attractor structure).

## What This Does NOT Mean

1. A CONFIRMED result would show the mechanism works in ONE real, published cancer-pathway model for
   ONE specific perturbation (`RAS`) — not a general law, and not a claim about real bladder cancer
   patients (the model is a simplified, curated abstraction of the pathway biology, not a patient-level
   predictive tool).
2. A REJECTED result would not close the bridge either — other nodes in the same bistable branch
   (`TP53`, `RB1`, `p21CIP` are all plausible alternative single-node perturbation targets) remain
   untested; only `RAS` is tested here per the Minimal Relaxation Rule (one perturbation target per
   experiment).
3. Does NOT test WHY the branch is bistable (the specific feedback loops responsible) — only whether a
   plausible transient perturbation can move between the two known attractors.

## MCID

Binary: does ≥1 tested transient perturbation reach a different attractor than the starting one? No
partial-credit threshold — exhaustive attractor identity via `pyboolnet`'s Gate-3 positive control, and
identical/hashable state comparison for the perturbation outcomes.
