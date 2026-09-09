# claim.md — 20260910-remy-tumorigenesis-p21cip-ruleperturbation-h19

**Graph node:** `H-B7-19` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-17` (PARTIALLY-ROBUST for `RBL2`'s own rule). `H-B7-17`'s own Relaxation Map
explicitly named `p21CIP`'s rule — "the other clamped node" — as an untested target.

## EstimandOps L0 Gate

**Classification: PREDICTIVE.** Same deterministic-system framing as H-B7-13..18.

## Design rationale — why p21CIP, and why a table-based (not symbolic) perturbation this time

**Choice of target:** `p21CIP` is the OTHER node clamped throughout this whole observability
sub-arc (`do(p21CIP=0, RBL2=0)`), symmetric to `RBL2` (already tested in H-B7-17). Testing it
completes the "both clamped nodes, single-bit perturbed" pair.

**p21CIP's own rule** (`.bnet` source, line 51): `TP53&!CyclinE1&!AKT | Growth_inhibitors&
!CyclinE1&!AKT` — 4 input symbols (`TP53`, `CyclinE1`, `AKT`, `Growth_inhibitors`), hence
`2^4=16` rows, too many to hand-derive a symbolic replacement expression for each single-bit flip
the way H-B7-17 did for `RBL2`'s 4-row table (a process that already produced a caught, corrected
hand-arithmetic error once this session, in H-B7-15's own tests). Instead of 16 hand-derived
expressions, this experiment builds a GENERIC table-based rule representation: the rule's truth
table is computed ONCE from the real boolean expression (not hand-derived), each single-bit
perturbation is a table with exactly one flipped row, and evaluation is by direct lookup — no
further boolean algebra required, eliminating that entire class of error.

**Hand-verifiable simplification, used only as a spot-check (not the actual computation
mechanism):** `TP53&!CyclinE1&!AKT | Growth_inhibitors&!CyclinE1&!AKT` factors (distributive law)
to `!CyclinE1 & !AKT & (TP53 | Growth_inhibitors)` — True at exactly 3 of 16 rows (`CyclinE1=
False, AKT=False`, and `TP53`/`Growth_inhibitors` not both False). Used to spot-check the
AUTOMATED table construction against 2-3 hand-computed rows, not to derive all 16 perturbations
by hand.

## Compute-First Check (why this is cheap, no new orbit-walk needed — same reasoning as H-B7-17)

`p21CIP` is the OTHER clamped node — forced to a constant by `clamp_rule` for the duration of the
`k`-round clamp, regardless of its own rule. H-B7-15's exhaustive 7-state-per-branch orbit is
therefore provably unaffected by any `p21CIP` rule perturbation; only post-release dynamics
differ. Reuses H-B7-15's exact `k=1..6` domain unchanged.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | H-B7-15's exhaustive 12-state domain (2 branches × k=1..6), re-evaluated under each of 16 single-bit-flip perturbations of `p21CIP`'s post-release rule (plus the unperturbed baseline) |
| **Falsifiable predicate** | Does `M1={Growth_arrest,Proliferation}` at `j=1` remain fully sufficient under each perturbed rule (after excluding `CRITERION_INVALID` cases via H-B7-17's own floor-based transition-exists check)? |
| **Measurable outcome** | `n_collisions` for M1/M2 at j=0/j=1, classification (ROBUST/FRAGILE/CRITERION_INVALID), per perturbation |

## Kill Criterion (set BEFORE running)

- **ROBUST:** `j*=1` sufficiency survives ALL meaningfully-testable perturbations (transition
  exists AND M1 resolves it).
- **PARTIALLY-ROBUST:** survives some but not all.
- **FRAGILE:** breaks under all/most meaningfully-testable perturbations.
- Perturbations with no underlying transition (floor shows 0 collisions, per H-B7-17's own
  corrected discipline) are classified `CRITERION_INVALID` and excluded from the ROBUST/FRAGILE
  count, not folded into either.
- **Substrate Gate check:** the clamp-phase orbit (12 states total) must be identical across all
  17 conditions (baseline + 16 perturbations) — if not, a bug in rule substitution, not a finding.

## What This Does NOT Mean

1. Tests only `p21CIP`'s rule, single-bit truth-table flips — does NOT test `CyclinE1`'s rule (the
   other named feedback-loop component, 32-row table, still untested) or multi-bit perturbations.
2. Does NOT combine with asynchronous update (H-B7-16) — a separate, more expensive follow-up.
3. A ROBUST verdict does not establish general structural robustness of the whole network — only
   that `j*=1` sufficiency is not fragile to THIS node's rule form.

## MCID

Not applicable — exact, exhaustive existence question, matching H-B7-15/17's scope.
