# claim.md — 20260906-remy-tumorigenesis-threehit-h6

**Graph node:** `H-B7-6` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-5` (Relaxation Map: "Three hits: add `do(p21CIP=0)` — directly remove the identified
redundant checkpoint, the mechanistically motivated next step, not a guess").

## EstimandOps L0 Gate

**Classification: CAUSAL.** Same structure as `H-B7-2`/`H-B7-3`/`H-B7-4`/`H-B7-5`: a combined
intervention `do(RAS=1, TP53=0, p21CIP=0)` applied simultaneously and permanently, compared against
the `Growth_arrest` starting fixed point and against the two-hit comparator already tested (`H-B7-5`:
`RAS`+`TP53`, REJECTED). The 4 identifiability assumptions are trivially satisfied for the same reason
as every prior experiment in this bridge (fully specified, exhaustively-verifiable deterministic
mechanism, cross-validated against `pyboolnet` in `H-B7-4`).

**Explicit deviation from the Minimal Relaxation Rule, justified — THIRD such deviation in this
bridge:** this experiment changes THREE assumptions at once relative to wild-type (or one more than
`H-B7-5`'s already-deliberate two). This is not scope creep — `H-B7-5`'s own mechanistic finding
directly named `p21CIP` as the SPECIFIC node sustaining `Growth_arrest` via a `TP53`-independent
route. Adding `do(p21CIP=0)` is not an arbitrary third gene search; it is the targeted removal of the
one mechanism `H-B7-5` identified as the reason the two-hit combination failed. The single-hit
(`H-B7-4`: RAS alone) and two-hit (`H-B7-5`: RAS+TP53) results remain the baselines this is read
against.

## Why `p21CIP`, Specifically, as the Third Hit

`H-B7-5`'s `decision.md` traced the exact mechanism: in the reached `Growth_arrest` attractor,
`p21CIP=1` DESPITE `TP53=0`, because `p21CIP`'s own rule
(`TP53&!CyclinE1&!AKT | Growth_inhibitors&!CyclinE1&!AKT`) has a second, `TP53`-independent disjunct
driven by the branch's own `Growth_inhibitors=1` input. Active `p21CIP` blocks `CyclinD1`
(`!p21CIP&!p16INK4a&RAS`) regardless of `RAS=1`. Clamping `p21CIP=0` directly removes this identified
blocker — the most surgical, mechanistically motivated next perturbation available, not a new blind
search over the network's other ~30 nodes.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Remy et al. 2015 network, same bistable branch as `H-B7-4`/`H-B7-5` `(DNA_damage=0, EGFR_stimulus=0, FGFR3_stimulus=1, Growth_inhibitors=1)`, `RAS` clamped to 1, `TP53` clamped to 0, AND `p21CIP` clamped to 0, simultaneously and permanently |
| **Falsifiable predicate** | The triple clamp, started from the `Growth_arrest` fixed point, settles into `Proliferation` (or a genuinely new attractor distinct from both known ones) rather than `Growth_arrest` |
| **Measurable outcome** | Final attractor reached, compared against `Growth_arrest`, `Proliferation`, and `H-B7-5`'s two-hit result |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: no prior three-hit perturbation
experiment on this or any Boolean network in this project. First three-node combined test in the
bridge, and the first perturbation in this bridge chosen by mechanism-tracing rather than by
biological-literature motivation alone (though `p21CIP` loss is ALSO independently well-documented in
real cancer biology — CDKN1A/p21 loss-of-function is a recognized event in several tumor types).

## Kill Criterion (set BEFORE running)

- **CONFIRMED (cooperativity/checkpoint-removal demonstrated):** the combined `do(RAS=1, TP53=0,
  p21CIP=0)` clamp reaches `Proliferation` (or a new, non-`Growth_arrest` attractor) — succeeding
  where the two-hit combination (`H-B7-5`) did not. This would be the first confirmation in this
  bridge that directly validates the traced mechanism: removing the SPECIFIC identified blocker flips
  the outcome.
- **REJECTED:** the triple clamp still returns to `Growth_arrest` — would mean `p21CIP` was NOT the
  only remaining blocker, and a further mechanism trace (analogous to `H-B7-5`'s own) is required to
  find what else sustains arrest even with all three nodes clamped.

## What This Does NOT Mean

1. A CONFIRMED result validates the specific mechanistic chain traced in `H-B7-5` for THIS branch and
   THIS model — not a general claim that `p21CIP` loss alone or in any combination causes bladder
   cancer progression in real patients.
2. A REJECTED result would not mean the traced mechanism was wrong about `p21CIP`'s role in
   MAINTAINING the `H-B7-5` attractor (that trace is a fact about the rules, already verified
   directly) — only that removing it is not SUFFICIENT, implying a second redundant pathway exists
   that a further trace would need to identify.
3. Does NOT test `p21CIP=0` alone (without `RAS`/`TP53`) — a simpler, lower-priority single-hit
   variant named in `H-B7-5`'s own Relaxation Map as a separate, deprioritized next step.

## MCID

Binary: does the triple clamp reach a different attractor than `Growth_arrest`? No partial-credit
threshold — exhaustive attractor identity comparison, cross-checked against `pyboolnet`'s
independently-computed ground truth (inherited from `H-B7-4`).
