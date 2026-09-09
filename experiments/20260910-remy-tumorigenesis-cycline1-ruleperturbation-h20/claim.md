# claim.md — 20260910-remy-tumorigenesis-cycline1-ruleperturbation-h20

**Graph node:** `H-B7-20` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-17` (`RBL2`, PARTIALLY-ROBUST) and `H-B7-19` (`p21CIP`, ROBUST) — both explicitly
named `CyclinE1` (the third component of the named `CyclinE1/RBL2` feedback loop, H-B7-13's own
diagnosis) as the one remaining untested node.

## EstimandOps L0 Gate

**Classification: PREDICTIVE.** Same deterministic-system framing as H-B7-13..19.

## Design rationale — a REAL structural difference from H-B7-17/19, not a copy-paste extension

**`CyclinE1` is NOT a clamped node.** `p21CIP` and `RBL2` (H-B7-17, H-B7-19) are both forced to a
constant by `clamp_rule` throughout the `k`-round clamp phase, regardless of their own rule — the
Compute-First Check both prior experiments relied on ("the clamp-phase orbit is unaffected by this
node's own rule perturbation") does NOT apply to `CyclinE1`, which evolves under its OWN rule
during the clamp phase too, exactly as much as after release. **This means H-B7-15's fixed
`k=1..6` domain cannot be reused unchanged here — the clamp-phase orbit itself must be re-walked
for EVERY perturbation**, since a perturbed `CyclinE1` rule can change the clamped trajectory's own
dynamics, potentially to a different length, on top of anything it changes post-release.

**`CyclinE1`'s own rule** (`.bnet` line 33): `!p21CIP&!RBL2&E2F3_medium&CDC25A | !p21CIP&!RBL2&
E2F1_medium&CDC25A` — 5 input symbols (`p21CIP`, `RBL2`, `E2F3_medium`, `CDC25A`, `E2F1_medium`),
`2^5=32` rows. Factors (distributive law) to `!p21CIP & !RBL2 & CDC25A & (E2F3_medium |
E2F1_medium)` — True at exactly 3 of 32 rows (spot-checked computationally against the real
expression in this experiment's own tests, not hand-trusted for all 32).

**User's own explicit added requirement, beyond H-B7-17/19's scope:** for each perturbation
classified `FRAGILE`, determine whether it **destabilizes the Proliferation attractor's own
fixed-point status directly** (H-B7-18's methodology) or **only destroys the `j*=1` observability**
of an attractor that still exists and remains reachable. H-B7-18 already showed this distinction
is real and mechanistically load-bearing for `RBL2`'s one fragile row — this experiment checks it
systematically for every fragile row found here, not just one hand-picked case.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | 32 single-bit truth-table perturbations of `CyclinE1`'s own rule, each re-evaluated over its OWN re-walked clamp-phase orbit (both branches) |
| **Falsifiable predicate** | For each perturbation: does `M1={Growth_arrest,Proliferation}` remain sufficient at `j=1` (excluding no-transition cases)? For each FRAGILE case: does `PROLIFERATION_STATE`/`_2` remain a fixed point under the perturbed rules? |
| **Measurable outcome** | Per-perturbation orbit length, classification (ROBUST/FRAGILE/CRITERION_INVALID), and for FRAGILE cases, a second classification (SELF-DESTABILIZING / OBSERVABILITY-ONLY) |

## Kill Criterion (set BEFORE running)

- **ROBUST:** all meaningfully-testable perturbations preserve `j*=1` sufficiency.
- **PARTIALLY-ROBUST:** some but not all.
- **FRAGILE:** most/all meaningfully-testable perturbations break it.
- Each `FRAGILE` row additionally classified `SELF-DESTABILIZING` (breaks the attractor's own
  fixed-point status, à la H-B7-18) or `OBSERVABILITY-ONLY` (attractor survives, only its `j*=1`
  legibility breaks) — a THIRD outcome this experiment introduces, not present in H-B7-17/19's own
  binary framing.
- **Substrate Gate note (real difference from H-B7-17/19):** orbit length is NOT expected to be
  constant across all 33 conditions this time (unlike the two clamped nodes) — this is reported as
  data, not asserted as a sanity check the way H-B7-17/19's "must be identical" was.

## What This Does NOT Mean

1. Does NOT claim the found robustness/fragility pattern generalizes beyond THESE three specific
   nodes (`RBL2`, `p21CIP`, `CyclinE1`) — other nodes in the 35-node network are untested.
2. Does NOT combine with asynchronous update (H-B7-16) — orthogonal, untested combination.
3. A `SELF-DESTABILIZING` vs `OBSERVABILITY-ONLY` classification for one row does not imply the
   SAME classification for other fragile rows of the same node — each is checked independently.

## MCID

Not applicable — exact, exhaustive existence questions (sufficiency, fixed-point consistency).
