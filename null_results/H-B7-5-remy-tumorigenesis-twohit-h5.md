# decision.md — 20260906-remy-tumorigenesis-twohit-h5

**Graph node:** `H-B7-5` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-06

## Verdict

- [x] **REJECTED** — the combined permanent `do(RAS=1, TP53=0)` clamp, started from the `Growth_arrest`
  fixed point, returns to `Growth_arrest` unchanged. Identical outcome to `H-B7-4`'s single-hit
  `RAS`-alone result.
- **This is not just a repeat of the same negative result — the mechanism was traced and identified**,
  turning a second REJECT into a real structural finding about the model, not merely "still didn't work."

**Statement:** *A biologically standard, extensively-studied oncogene/tumor-suppressor cooperating
pair (`RAS` activation + `TP53` loss) is INSUFFICIENT to destabilize the `Growth_arrest` attractor in
this branch of the Remy et al. 2015 network. Tracing the mechanism directly: the reached attractor has
`p21CIP=1` even with `TP53=0` clamped — because `p21CIP`'s rule
(`TP53&!CyclinE1&!AKT | Growth_inhibitors&!CyclinE1&!AKT`) has a SECOND, `TP53`-INDEPENDENT route via
`Growth_inhibitors` (the branch's own external input, fixed at 1 in every multistable branch this model
has), and that route alone is sufficient to keep `p21CIP` active, which blocks `CyclinD1`
(`!p21CIP&!p16INK4a&RAS | ...`) even with `RAS=1`, which in turn keeps `RB1` active and the cell
arrested.*

## Evidence Summary

| Node | Value in the reached attractor | Role |
|---|---|---|
| `RAS` | 1 (clamped) | oncogenic hit — active as intended |
| `TP53` | 0 (clamped) | tumor-suppressor hit — inactive as intended |
| `Growth_inhibitors` | 1 (branch input, unclamped) | **the actual redundant checkpoint** |
| `p21CIP` | 1 | active DESPITE `TP53=0`, via `Growth_inhibitors` alone |
| `CyclinE1`, `AKT` | 0, 0 | both required (as `!CyclinE1&!AKT`) for `Growth_inhibitors` to activate `p21CIP` — confirmed present |
| `CyclinD1` (implied) | blocked | `p21CIP=1` blocks it even with `RAS=1` |
| `RB1` | 1 | stays active, growth arrest maintained |

Verified directly against the actual `.bnet` rules and the actual reached state (not inferred from
memory) — see the traced chain above, each link checked against both the rule text and the state
values.

**A structural fact about the model, not an artifact of this one branch:** every one of the 8
multistable branches identified in `H-B7-4`'s Compute-First check has `Growth_inhibitors=1` — there is
no multistable branch in this model with `Growth_inhibitors=0`. This means the redundant
`Growth_inhibitors → p21CIP` checkpoint is present in EVERY branch where a `Growth_arrest` vs.
`Proliferation` choice exists at all, not a peculiarity of the one branch tested.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] `RAS`+`TP53` cooperativity, while real and well-documented in general cancer biology, is
  insufficient to override this SPECIFIC model's external-growth-signal checkpoint.
- [x] The pipeline correctly composes two simultaneous permanent clamps (`apply_combined_clamp`,
  tested against a hand-traced synthetic "genuine two-hit" network — `A'=A|(B&C)` — where a single
  clamp is provably insufficient and the combined clamp provably flips the outcome, confirming the
  MECHANISM works before concluding the REAL network's negative result is genuine, not a code bug).

### What Was NOT Confirmed
- [x] Kauffman's hypothesis was not confirmed by this pairing either — but the reason is now
  MECHANISTICALLY IDENTIFIED, not just "still no": a specific, named, redundant pathway
  (`Growth_inhibitors → p21CIP ⊣ CyclinD1`) that neither `RAS` nor `TP53` touches.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Two hits (`RAS`, `TP53`) | Three hits: add `do(p21CIP=0)` — directly remove the identified redundant checkpoint, the mechanistically motivated next step, not a guess | Highest-value next experiment — tests the EXACT mechanism just identified, not another arbitrary gene pair |
| `RAS`+`TP53` specifically | `RAS` + `RB1=0` (bypass the checkpoint further downstream, closer to the phenotype) instead of `TP53=0` (further upstream, one step removed from `CyclinD1`) | An alternative single substitution — lower priority than the p21CIP test, which is directly implicated by the traced mechanism |
| Only this one bistable branch tested | Since ALL 8 multistable branches share `Growth_inhibitors=1`, this redundancy likely generalizes to all of them — not yet checked on a second branch | Cheap to check (no new compute, just re-run `pyboolnet`'s branch analysis with `p21CIP` fixed, already cached from `H-B7-4`'s scoping) |

## What This Does NOT Mean

1. Does NOT mean `RAS`+`TP53` cooperativity is biologically wrong — real bladder tumors are not
   subject to the same external `Growth_inhibitors=1` boundary condition this model's specific branch
   imposes; the model's redundancy here is a property of this SPECIFIC simplified abstraction and its
   specific input configuration, not a general refutation of the oncogene pair's real-world relevance.
2. Does NOT mean Kauffman's hypothesis is false in this model — the multistable structure verified in
   `H-B7-4` remains real; this experiment narrows WHICH internal perturbations can reach it (not
   `RAS`+`TP53` alone) rather than showing no perturbation can.
3. Does NOT test whether `p21CIP=0` alone (without `RAS`/`TP53`) is sufficient — that would be a
   different, simpler question (single-hit `p21CIP`), not yet tested and lower priority than the
   three-hit combination that directly follows from this experiment's own finding.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified, previously `pyboolnet`-cross-checked
mechanism (`H-B7-4`). Floor and ceiling do not apply to an exhaustive/deterministic attractor
identity comparison: there is no population to integrate over and no privileged-access variant of
"what attractor does this fully specified mechanism reach" — the mechanism's own rules already are
the ground truth, cross-checked once against `pyboolnet` in `H-B7-4`.

## Pearl Card Update

**New information:** a null result was traced to a specific, verifiable mechanism (a redundant
external-signal-driven checkpoint) rather than left as an unexplained "didn't work" — directly
actionable (names the exact next perturbation) rather than requiring another guess-and-check cycle.
Also surfaces a structural property of the whole model worth remembering: `Growth_inhibitors=1` is a
SHARED feature of every multistable branch this model has, meaning any future perturbation experiment
on this network's bistability should expect to contend with the same `p21CIP`-mediated redundancy,
not treat it as specific to the one branch already tested.
