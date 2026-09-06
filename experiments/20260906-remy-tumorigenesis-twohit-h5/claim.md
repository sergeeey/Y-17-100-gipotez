# claim.md — 20260906-remy-tumorigenesis-twohit-h5

**Graph node:** `H-B7-5` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-4` (Relaxation Map: "Combined `do(RAS=1, TP53=0)` — a genuine two-hit perturbation,
matching multi-hit carcinogenesis theory ... would need its own experiment, framed explicitly as a
2-hit test, not a Minimal-Relaxation-Rule single step").

## EstimandOps L0 Gate

**Classification: CAUSAL.** Same structure as `H-B7-2`/`H-B7-3`/`H-B7-4`: a combined intervention
`do(RAS=1, TP53=0)` applied simultaneously and permanently, compared against the never-perturbed
comparator (`H-B7-4`'s starting `Growth_arrest` fixed point) and against the SINGLE-hit comparators
already tested (`H-B7-4`'s `RAS`-alone result: REJECTED). The 4 identifiability assumptions are
trivially satisfied for the same reason as every prior experiment in this bridge (fully specified,
exhaustively-verifiable deterministic mechanism, now cross-validated against `pyboolnet` in `H-B7-4`).

**Explicit deviation from the Minimal Relaxation Rule, justified:** this experiment changes TWO
assumptions at once relative to `H-B7-4` (clamping `TP53` in addition to `RAS`). This is not an
oversight — `H-B7-4`'s own Relaxation Map named this exact combination as the deliberate next step,
because the scientific question is COOPERATIVITY itself (does a second, independently well-motivated
hit succeed where the first alone did not?), which by definition requires changing two things together,
not one at a time. `RAS` alone (`H-B7-4`) and `TP53` alone (not yet tested, a natural comparator) remain
the single-hit baselines this combined result will be read against.

## Why `TP53`, Specifically, as the Second Hit

`TP53` (`!MDM2&E2F1_medium&E2F1_high | !MDM2&CHEK1_2_medium&ATM_medium`) encodes the p53 tumor
suppressor — one of the most commonly inactivated genes in human cancer, textbook-described as "the
guardian of the genome." `RAS` activation + `TP53` loss is one of the most extensively studied
oncogene/tumor-suppressor cooperativity pairs in cancer biology (used in numerous mouse cancer models),
making this a well-motivated, not arbitrarily chosen, second hit — not a search over all possible
pairs for whichever one happens to flip the outcome.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Remy et al. 2015 network, same bistable branch as `H-B7-4` `(DNA_damage=0, EGFR_stimulus=0, FGFR3_stimulus=1, Growth_inhibitors=1)`, `RAS` clamped to 1 AND `TP53` clamped to 0, simultaneously and permanently |
| **Falsifiable predicate** | The combined clamp, started from the `Growth_arrest` fixed point, settles into `Proliferation` (or a genuinely new attractor distinct from both known ones) rather than `Growth_arrest` |
| **Measurable outcome** | Final attractor reached, compared against `Growth_arrest`, `Proliferation`, and `H-B7-4`'s single-hit `RAS`-only result |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: no prior combined-perturbation
experiment on this or any Boolean network in this project. First genuine two-hit test in the bridge.

## Kill Criterion (set BEFORE running)

- **CONFIRMED (cooperativity demonstrated):** the combined `do(RAS=1, TP53=0)` clamp reaches
  `Proliferation` (or a new, non-`Growth_arrest` attractor) — succeeding where `RAS` alone
  (`H-B7-4`) did not. This would be the first PERMANENT-clamp confirmation in this bridge that
  matches Kauffman's structural spirit closely (a real published cancer model, a biologically
  standard cooperating pair, a genuine pre-existing alternative attractor).
- **REJECTED:** the combined clamp still returns to `Growth_arrest` — would mean even this
  well-motivated two-hit combination is insufficient in this simplified model, a further narrowing
  result (matching `H-B7-4`'s own honest negative framing, not evidence against Kauffman's hypothesis
  in general, only against this specific operationalization).

## What This Does NOT Mean

1. A CONFIRMED result shows cooperativity in ONE simplified model for ONE specific gene pair — not a
   general law of carcinogenesis, and not a claim about real bladder cancer patients.
2. Does NOT test the SAME node pairing transiently (released, not permanent) — that would be a further,
   still-untested variant (this experiment uses a PERMANENT clamp, matching `H-B7-2`'s design pattern
   rather than `H-B7-3`'s transient one, since the goal here is to first establish WHETHER cooperativity
   exists in this model at all, before testing whether it survives a merely transient push).
3. Does NOT search over all possible 2-node combinations for whichever one happens to work — `RAS`+`TP53`
   is pre-registered as the specific, biologically-motivated pair before running anything.

## MCID

Binary: does the combined clamp reach a different attractor than `Growth_arrest`? No partial-credit
threshold — exhaustive attractor identity comparison, cross-checked between this project's own
pipeline and `pyboolnet`'s independently-computed ground truth (inherited from `H-B7-4`).
