# claim.md — 20260906-kauffman-cellcycle-perturbation-h2

**Graph node:** `H-B7-2` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-1` (CONFIRMED reproduction of the wild-type attractors). This is the experiment that
actually engages Kauffman's Cancer Attractor hypothesis, named explicitly in `H-B7-1`'s own Relaxation
Map as the item that turns a tooling-validation exercise into a real test.

## EstimandOps L0 Gate (MANDATORY, run BEFORE choosing tier — per project rule)

**Classification: CAUSAL.** This is an intervention question, not a description of an existing
dataset and not a prediction from an unknown model: "if we FORCE `Rb` (or `p27`) to be permanently
off — a `do(Rb≡0)` intervention in Pearl's sense — instead of letting it follow its own update rule,
does the resulting dynamics, started from a growth-factor-absent state (`CycD=0`), settle into a
cycling attractor instead of quiescence?" This is compared against a natural-dynamics comparator (no
clamping) — a genuine intervention-vs-comparator causal structure, not a mere observation.

**Why the usual identifiability machinery is trivially satisfied here (stated, not skipped):** the
four EstimandOps causal assumptions are usually hard to verify in observational/statistical settings.
Here the "population" is a FULLY SPECIFIED, deterministic, exhaustively-enumerable mechanistic model
(the same Boolean network verified in `H-B7-1`), not a sample from an unknown data-generating process:

| Assumption | Status here |
|---|---|
| Consistency | Trivial — the intervened system's dynamics ARE computed by direct simulation, not estimated |
| Positivity | Trivial — every state in the `CycD=0` region is reachable and simulatable; no missing support |
| Exchangeability (no unmeasured confounders) | Trivial — the ENTIRE mechanism (all 10 update rules) is known and specified; there is no variable outside the model that could confound |
| SUTVA | Trivial — single deterministic system, no interference between "units" (there are no separate units) |

This is causal inference in the Pearl/structural-equation sense on a KNOWN mechanism (do-calculus on a
fully specified SCM), not statistical causal inference under uncertainty — the gate is answered
honestly as "trivially satisfied by construction," not skipped, per the project's L0-gate mandate.

## Estimand (L1, lightweight — full EstimandOps population/ICE machinery does not apply to a closed
deterministic system; stated proportionally, per the Structure-Bias Guard)

- **Population:** all 512 states of the Fauré 2006 network with `CycD=0` (the growth-factor-absent
  region already isolated in `H-B7-1`'s attractor basin analysis).
- **Intervention:** `do(Rb≡0)` — Rb's own update rule is replaced by the constant function `0` for
  all time (a permanent loss-of-function, modeling Rb inactivation/deletion). A second, separate
  intervention `do(p27≡0)` is tested identically (Minimal Relaxation Rule: two related interventions
  run as two clearly-labeled arms of the SAME experiment, not conflated into one).
- **Comparator:** natural dynamics — Rb (resp. p27) follows its own update rule unchanged, as verified
  in `H-B7-1`.
- **Endpoint:** attractor TYPE reached from each of the 512 `CycD=0` initial states (point vs.
  complex/cyclic), and, if complex, whether it structurally resembles the wild-type cycling attractor
  (same states/period) or is a genuinely new attractor.
- **Summary measure:** categorical (attractor type reached), reported per-state and as a basin
  fraction — no continuous statistic needed, this is exhaustive enumeration, not sampling.
- **ICE:** not applicable — no missing data, no dropout, deterministic finite system.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Fauré et al. 2006 network (same `.bnet` file verified in `H-B7-1`), with `Rb` or `p27` permanently clamped to 0 |
| **Falsifiable predicate** | Under `do(Rb≡0)` (or `do(p27≡0)`), states starting with `CycD=0` no longer all reach the quiescent point attractor — at least some reach a cycling/complex attractor |
| **Measurable outcome** | For each of the 512 `CycD=0` initial states under each intervention: attractor type reached (point/complex), and whether the complex attractor (if any) matches the wild-type cycling attractor's state set |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md` and `pearl_registry/INDEX.md`: no prior perturbation/intervention
work on Boolean networks in this project (only `H-B7-1`'s unperturbed reproduction exists). Rb and
p27 loss-of-function are well-documented, real tumor-suppressor mechanisms in cancer biology
(textbook-level, not asserted from memory without backing — Rb inactivation and p27 loss are named
directly in the Fauré et al. 2006 paper's own description of the model's inhibitor components, per
`H-B7-1`'s Gate-1 source trace). Testing them computationally in THIS model, in THIS project, is new.

## Natural Language Statement

> "We estimate whether permanently clamping Rb (or, separately, p27) to 0 — modeling loss-of-function
> of these tumor suppressors — changes the attractor reached from every growth-factor-absent
> (`CycD=0`) initial state, compared to the unperturbed network's uniform convergence to the
> quiescent point attractor (established in `H-B7-1`)."

## L0 Classification (restated)

**Causal** (do-operator intervention vs. natural-dynamics comparator on a fully specified mechanistic
model).

## Kill Criterion (set BEFORE running)

- **CONFIRMED (supports Kauffman's hypothesis in this model):** under `do(Rb≡0)` OR `do(p27≡0)`, at
  least one `CycD=0` initial state now reaches a COMPLEX (cycling) attractor instead of the wild-type
  quiescent point attractor — the SAME network, without restructuring, reveals a pathological-looking
  attractor once perturbed. This is the operationalization of "cancer as a pre-existing attractor made
  accessible," not a separately engineered model.
- **REJECTED (for that specific intervention):** the `CycD=0` region still converges uniformly to a
  point attractor despite the clamp — the perturbation alone is insufficient to destabilize quiescence
  in this model.
- Both interventions (Rb, p27) are scored independently — a REJECT on one does not REJECT the other
  (Minimal Relaxation Rule: they are two separate, clearly-labeled sub-experiments).

## What This Does NOT Mean

1. A CONFIRMED result does NOT prove Kauffman's hypothesis is true of real biology in general — it
   shows the operationalization holds in ONE small, published, simplified model. Real cell-cycle
   control involves far more regulators than these 10.
2. Does NOT test combined perturbations (e.g., both Rb AND p27 lost simultaneously) — a further,
   two-assumptions-changed step if single perturbations are uninformative (Minimal Relaxation Rule
   would require its own experiment ID).
3. A REJECTED result does NOT mean Kauffman's hypothesis is false in general — it means THIS
   perturbation, in THIS model, is insufficient; real cancers typically involve multiple concurrent
   lesions, which a single-node clamp does not represent.

## MCID

Binary per intervention: does ≥1 of the 512 `CycD=0` states reach a complex attractor (yes = supports
the operationalized hypothesis for that intervention) or do all 512 still reach the point attractor
(no)? No partial-credit threshold needed — this is exhaustive enumeration, not a sampled estimate.
