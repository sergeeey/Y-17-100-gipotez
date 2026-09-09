# claim.md — 20260910-remy-tumorigenesis-fixedpoint-destabilization-h18

**Graph node:** `H-B7-18` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-17` (PARTIALLY-ROBUST — one perturbation, `flip_TF_drop_CyclinE1`, was found
`CRITERION_INVALID`: it abolishes the transient-escape phenomenon entirely, every `k=1..6`
relapsing to `GROWTH_ARREST`, rather than merely shifting the threshold or making it
unobservable. WHY was left as an explicitly named, un-answered open question in H-B7-17's own
Revival Condition.)

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** This is a formal, structural question about a known, fully
specified deterministic system: is a SPECIFIC named state (`PROLIFERATION_STATE`,
`PROLIFERATION_STATE_2`) a fixed point of a SPECIFIC modified rule set? Not predictive (no future
observation being forecast beyond the deterministic system's own definition) and not causal (no
population, no intervention effect estimation) — a fact about the model, checkable exactly.

## Mechanism Claim Gate (Step 0a) — the design-justifying sentence, checked BEFORE building

**Triggering sentence (this experiment's own hypothesis, stated as the thing to check, not
assumed):** *"`flip_TF_drop_CyclinE1` (`RBL2 := !CyclinD1`) destabilizes `PROLIFERATION_STATE`'s
own fixed-point status directly — not merely making it unreachable via the transient-clamp
protocol."*

**Hand-derivation performed BEFORE writing any code (Compute-First Check):**
`PYBOOLNET_NODE_ORDER` index 9 = `CyclinD1`, index 10 = `CyclinE1`. `PROLIFERATION_STATE =
"00000100101001010011001000110010110"` → position 9 = `'0'` (`CyclinD1=False`), position 10 =
`'1'` (`CyclinE1=True`). Original `RBL2` rule (`!CyclinE1 & !CyclinD1`) evaluates to
`!True & !False = False` at this exact state — consistent with the state's own `RBL2=False`
(required for `Proliferation` to hold, since `CyclinA`/`CyclinE1` both need `!RBL2`). Under the
perturbed rule `RBL2 := !CyclinD1 = !False = True` — **the perturbed rule disagrees with the
state's own `RBL2=False`: this state is NOT a fixed point of the perturbed system.**

This experiment computationally VERIFIES this hand-derivation (not just trusts it) and traces
what happens next — does the destabilized trajectory relapse to `Growth_arrest`, or reach some
third, previously-unseen attractor?

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `PROLIFERATION_STATE` (branch 1) and `PROLIFERATION_STATE_2` (branch 2) — the two known escape-attractor states from H-B7-4/7/8/9/10/11 — evaluated under the `flip_TF_drop_CyclinE1`-perturbed rule set |
| **Falsifiable predicate** | Does one synchronous step from each state, under the perturbed rules, equal the SAME state (still a fixed point) or a DIFFERENT one (destabilized)? If destabilized, where does `run_until_attractor` say it eventually settles? |
| **Measurable outcome** | State equality check (exact); the eventual attractor reached from each destabilized starting point |

## Design

Reuses H-B7-1's `synchronous_step`/`run_until_attractor` (H-B7-3's copy), H-B7-4's
`PROLIFERATION_STATE`/`PYBOOLNET_NODE_ORDER`, H-B7-11's `PROLIFERATION_STATE_2`, H-B7-17's exact
`flip_TF_drop_CyclinE1` expression — all UNCHANGED. No new simulation machinery needed: this is a
direct application of already-existing, already-verified functions to a new question.

## Kill Criterion (set BEFORE running)

- **CONFIRMED-SELF-DESTABILIZING:** the perturbed rule set gives `RBL2=True` at
  `PROLIFERATION_STATE`/`_2` (contradicting the state's own `RBL2=False`) — the state is not a
  fixed point, and the subsequent trajectory (traced via `run_until_attractor`) relapses toward
  `Growth_arrest`-phenotype attractors, directly explaining H-B7-17's finding at the mechanism
  level: the transient clamp doesn't just fail to REACH `Proliferation`, `Proliferation` itself
  stops existing as a stable resting point under this specific perturbation.
- **REJECTED:** `PROLIFERATION_STATE`/`_2` remain fixed points under the perturbed rules (hand-
  derivation was wrong) — H-B7-17's finding would need a different explanation entirely.

## What This Does NOT Mean

1. Does NOT claim NO Proliferation-phenotype attractor exists ANYWHERE in the perturbed system's
   full ~2^31-state space — only that these TWO SPECIFIC, previously-known states are no longer
   fixed points. A structurally different Proliferation-phenotype attractor could in principle
   exist elsewhere, unexplored here (exhaustive search over 2^31 states is infeasible).
2. Does NOT generalize to the other 3 perturbations tested in H-B7-17 — this traces exactly ONE
   (`flip_TF_drop_CyclinE1`), the one already flagged as qualitatively different (`CRITERION_
   INVALID`, not `ROBUST`/`FRAGILE`).

## MCID

Not applicable — exact state-equality and fixed-point-consistency check, not an estimated
quantity.
