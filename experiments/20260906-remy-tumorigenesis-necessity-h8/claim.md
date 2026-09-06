# claim.md — 20260906-remy-tumorigenesis-necessity-h8

**Graph node:** `H-B7-8` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-7` (Relaxation Map / FL Step 8a skeptic WEAKENING: "RAS=1 and TP53=0 are already
true at the `GROWTH_ARREST_STATE` starting point... the actually novel and load-bearing perturbation
is the two-hit `do(p21CIP=0, RBL2=0)`" — necessity test named as the direct next step).

## EstimandOps L0 Gate

**Classification: CAUSAL.** Same structure as every prior H-B7 perturbation: a `do`-intervention
compared against the `Growth_arrest` starting fixed point and against `H-B7-7`'s four-hit comparator
(CONFIRMED). The 4 identifiability assumptions are trivially satisfied for the same reason as every
prior experiment in this bridge (fully specified, exhaustively-verifiable deterministic mechanism,
cross-validated against `pyboolnet` in `H-B7-4`, `H-B7-6`, and `H-B7-7`).

**Relationship to the Minimal Relaxation Rule — this experiment REDUCES scope, it does not expand
it:** `H-B7-7` clamped 4 nodes. This experiment clamps only 2 (`p21CIP`, `RBL2`), leaving `RAS` and
`TP53` to evolve under their OWN wild-type rules rather than being held constant. This is a genuine
necessity test, not a further Relaxation-Map expansion — it directly operationalizes the skeptic's
own Step 8a WEAKENING finding from `H-B7-7`: since `RAS=1` and `TP53=0` are ALREADY the values
present at `GROWTH_ARREST_STATE`, permanently clamping them may have been redundant. The open
question this experiment resolves: do `RAS`/`TP53` STAY at those values dynamically once `p21CIP`/
`RBL2` are removed and the trajectory starts moving (their rules are dynamic —
`RAS = GRB2 | FGFR3 | EGFR`, `TP53 = !MDM2&E2F1_medium&E2F1_high | !MDM2&CHEK1_2_medium&ATM_medium`
— unlike a permanent clamp, nothing prevents them from changing mid-trajectory), or does removing the
clamp allow them to drift, changing the outcome relative to `H-B7-7`?

## Why This Test, Specifically

`H-B7-7`'s own FL Step 8a skeptic pass found, by direct inspection of `GROWTH_ARREST_STATE`, that
`RAS=1` (via `FGFR3` signaling already active in this branch) and `TP53=0` (already off) hold at the
UNCLAMPED starting point. If this observation is right and dynamically stable, `do(p21CIP=0,
RBL2=0)` alone — without touching `RAS`/`TP53` at all — should reach the same `Proliferation`
outcome `H-B7-7` reached with all four nodes clamped. If `RAS` or `TP53` drift away from their
`H-B7-7`-clamped values once the other two constraints are lifted, the necessity claim is wrong and
`RAS=1`/`TP53=0` were load-bearing after all — a genuinely informative negative result either way.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Remy et al. 2015 network, same bistable branch as `H-B7-4`/`5`/`6`/`7` `(DNA_damage=0, EGFR_stimulus=0, FGFR3_stimulus=1, Growth_inhibitors=1)`, starting from `GROWTH_ARREST_STATE`, with ONLY `p21CIP` clamped to 0 and `RBL2` clamped to 0 — `RAS` and `TP53` left unclamped, following their own wild-type rules |
| **Falsifiable predicate** | The double clamp reaches an attractor with the model's own phenotype nodes reading `Growth_arrest=0, Proliferation=1` — the SAME outcome `H-B7-7` reached with all four nodes clamped |
| **Measurable outcome** | Final attractor's `Growth_arrest`/`Proliferation` phenotype-node values, AND the final values of the un-clamped `RAS`/`TP53` nodes (to check whether they drifted), compared against `H-B7-7`'s four-hit result |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: no prior necessity test (reducing an
already-CONFIRMED clamp set) exists in this project. First "does the minimal subset also work"
experiment in the bridge — directly follows from `H-B7-7`'s own skeptic-surfaced observation rather
than from a fresh guess.

## Kill Criterion (set BEFORE running)

- **CONFIRMED (necessity demonstrated — `RAS`/`TP53` clamps were redundant):** the double clamp
  reaches an attractor with `Proliferation=1, Growth_arrest=0`, AND the final (unclamped) values of
  `RAS`/`TP53` are `1`/`0` respectively (i.e. they stayed at the values `H-B7-7` clamped them to,
  confirming they did not need to be forced).
- **REJECTED (necessity NOT demonstrated):** the double clamp still reads `Growth_arrest=1` — meaning
  `RAS=1`/`TP53=0` were, despite appearing already true at the static starting state, dynamically
  load-bearing once the trajectory actually moves (e.g. `RAS` or `TP53` drift to a different value
  mid-trajectory without the permanent clamp holding them in place).
- **PARTIAL (unexpected but informative):** the double clamp reaches `Proliferation=1` but `RAS` or
  `TP53`'s final value differs from `H-B7-7`'s clamped value — would mean the outcome is reachable via
  a DIFFERENT configuration of those two nodes than `H-B7-7`'s, weakening the specific "no-op" framing
  from the skeptic pass without falsifying the broader necessity claim.

## What This Does NOT Mean

1. A CONFIRMED result would show `p21CIP`+`RBL2` alone are SUFFICIENT relative to THIS specific
   starting fixed point (`GROWTH_ARREST_STATE`) — not a general claim that `RAS`/`TP53` are irrelevant
   to this network's biology in every branch or every starting condition.
2. A REJECTED result would not contradict `H-B7-7`'s own CONFIRMED verdict (that result used a
   different, larger clamp set and stands on its own) — it would only mean the specific WEAKENING
   framing from `H-B7-7`'s skeptic pass was too strong, sharpening rather than reversing the finding.
3. Does NOT test a TRANSIENT version of this same double clamp — that remains a separate, still-named
   next step from `H-B7-6`'s original Relaxation Map.

## MCID

Binary: does the model's own `Proliferation` phenotype node read `1` in the reached attractor, AND do
`RAS`/`TP53`'s final values match `H-B7-7`'s clamped values? No partial-credit threshold on the
phenotype axis — exhaustive attractor identity comparison, cross-checked against `pyboolnet`'s
independently-computed ground truth (inherited from `H-B7-4`/`H-B7-7`).
