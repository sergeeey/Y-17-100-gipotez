# decision.md — 20260906-kauffman-cellcycle-transient-h3

**Graph node:** `H-B7-3` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-06

## Verdict

- [x] **CONFIRMED (the deduction, not the hypothesis)** — every one of 6 simulated transient
  perturbations (varying clamped node, duration, and starting state, including a mid-trajectory
  state taken from `H-B7-2`'s own permanent-clamp run) returns EXACTLY to the wild-type quiescent
  point attractor `0000001011` once released. `all_cases_returned_to_quiescence: true`.
- **This is a `TASK_INFEASIBLE`-style finding for the STRICT test, not a PROMOTE/REJECT on Kauffman's
  hypothesis.** The deduction made in `claim.md` before running any simulation — that this outcome is
  logically forced by `H-B7-1`'s own already-verified single-attractor structure of the `CycD=0`
  region — is confirmed empirically. The experiment could not have come out any other way in this
  model, and finding that it didn't is the expected, correct result, not a discovery about biology.

**Statement:** *In the Fauré et al. 2006 network, transient (finite-duration) clamping of `Rb`,
`p27`, or both, followed by release back to natural dynamics, always returns the system to the
wild-type quiescent point attractor from any `CycD=0` starting condition. This is a NECESSARY
CONSEQUENCE of `H-B7-1`'s own exhaustive finding that the entire 512-state `CycD=0` region has a
SINGLE global attractor under the network's true rules — there is no second attractor within that
region for a transient perturbation to reveal. The strict form of Kauffman's Cancer Attractor
hypothesis (a pathological state is a pre-existing attractor of the UNPERTURBED network, made
reachable by a temporary push, not a permanent rule change) is therefore UNTESTABLE in this specific
10-node model, regardless of whether the hypothesis is true in general.*

## Evidence Summary

| Case | Clamp | k | Post-release start state | Final attractor | Returned to quiescence? |
|---|---|---|---|---|---|
| all-zero, Rb | Rb=0 | 1 | `0001010111` | point `0000001011` | ✅ |
| all-zero, Rb | Rb=0 | 5 | `0010110011` | point `0000001011` | ✅ |
| all-zero, Rb | Rb=0 | 20 | `0000110011` | point `0000001011` | ✅ |
| all-zero, p27 | p27=0 | 5 | `0000001010` | point `0000001011` | ✅ |
| all-zero, Rb+p27 | Rb=0,p27=0 | 5 | `0010110010` | point `0000001011` | ✅ |
| H-B7-2 mid-trajectory, Rb | Rb=0 | 3 | `0011000100` | point `0000001011` | ✅ |

**6/6 (100%)** — exactly as the pre-registered deduction required. Note the last case in particular:
starting from a state that `H-B7-2`'s PERMANENT clamp had already visited on its way to the new
period-8 cycling attractor, a mere 3-step transient clamp (instead of permanent) still returns to
quiescence — the difference between `H-B7-2`'s CONFIRMED and this experiment's null result is entirely
about whether the clamp is ever released, not about the specific state reached during perturbation.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The Compute-First deduction (stated in `claim.md` before any new simulation code was written):
  transient single/double-node perturbation of `Rb`/`p27` cannot escape the `CycD=0` region's single
  global attractor. Verified against 6 concrete simulated trajectories, not just asserted.
- [x] `run_until_attractor` and `simulate_transient_clamp` are correct — validated first on 5
  hand-checkable synthetic cases (including a case, `A'=!A, B'=A&B` with `A` clamped then released,
  hand-traced to a period-2 cycle) before trusting the real network's result.

### What This Sharpens About the Bridge's Overall Position
- [x] `H-B7-2`'s `do(Rb=0)` result is now precisely characterized: it works ONLY because the clamp is
  PERMANENT — removing `Rb`'s own dynamics from the state space entirely creates a genuinely new
  attractor. A TRANSIENT version of the identical intervention does nothing, confirming `H-B7-2`'s own
  `[WEAKENED]` qualifier was the right call, not overcautious.
- [x] This model (10 nodes, exactly 2 attractors total, no multi-attractor structure within either
  `CycD` branch) is structurally the WRONG kind of model to test Kauffman's strict claim. A model with
  more nodes/redundant regulators, where each `CycD` branch itself contains multiple attractors, would
  be needed.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Fauré et al. 2006 cell-cycle model (2 attractors total, 1 per branch) | Test the SAME transient-perturbation logic on a Boolean network KNOWN to have multiple attractors within one basin/branch — e.g., a network with genuine multistability, not just an input-switch bifurcation | Would need a new model with the right structural property; `pyboolnet`'s repository (already used for `H-B7-1`) lists several other curated models (`zhang_tlgl`, `remy_tumorigenesis`, `krumsiek_myeloid`) worth checking for this property before assuming any of them qualifies |
| Only Rb/p27, and only loss-of-function (=0) | Gain-of-function clamps (node forced =1, e.g. `CycD=1` transiently — though this trivially moves into the other branch, already known to cycle, so not novel) not tested | Low priority — would test the already-implied "flip the input" case, not new information |

## What This Does NOT Mean

1. Does NOT mean Kauffman's Cancer Attractor hypothesis is false — it means it is UNTESTABLE in its
   strict form using THIS specific small model, which lacks the required multi-attractor-per-branch
   structure. Absence of evidence, not evidence of absence.
2. Does NOT invalidate `H-B7-2`'s `do(Rb=0)` CONFIRMED-WEAKENED result — that intervention was
   explicitly PERMANENT, a structurally different (and, per this experiment, NECESSARY) condition for
   the effect to appear at all.
3. Does NOT mean transient perturbations are never informative for Boolean-attractor disease
   hypotheses in general — only that a model needs genuine multistability within a shared basin for
   such a test to be capable of distinguishing anything (a `NO_HEADROOM`-style condition, checked here
   BEFORE the expensive simulation via the Compute-First deduction, not discovered by brute force
   after the fact).

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified mechanism, same reasoning as `H-B7-1`
and `H-B7-2`. The relevant analogue here (stated explicitly per the FL "third-outcome discipline" for
gates that block informativeness) is the Compute-First deduction itself, which plays the same
role as a `TASK_INFEASIBLE`/`NO_HEADROOM` verdict: established BEFORE the run, not used as an excuse
after an uninteresting result.

## Pearl Card Update

**New information (methodological, generalizes beyond this bridge):** before running an expensive
perturbation/intervention simulation, check whether the population/basin structure ALREADY established
by a prior experiment logically forecloses the outcome. Here, `H-B7-1`'s own exhaustive attractor
enumeration (originally run just to validate the pipeline, not with this question in mind) contained
everything needed to PROVE the transient-perturbation result before writing a single line of new
simulation code — the actual run was a verification of that deduction (Gate-3-style: check, don't just
trust reasoning), not a fishing expedition. This is a concrete, worked example of the "compute first"
discipline this project's own methodology stack names but rarely gets to demonstrate this cleanly.
