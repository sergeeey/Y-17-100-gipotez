# decision.md — 20260906-remy-tumorigenesis-threehit-h6

**Graph node:** `H-B7-6` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-06

## Verdict

- [x] **REJECTED** — the combined permanent `do(RAS=1, TP53=0, p21CIP=0)` clamp reaches a NEW attractor
  (distinct bit-string from both `H-B7-4`'s `Growth_arrest` and `Proliferation`), but the model's own
  explicit phenotype-readout nodes confirm it is still, semantically, a `Growth_arrest`-type state:
  `Growth_arrest=1`, `Proliferation=0` in the reached attractor.

**Correction to the pre-registered kill criterion (Hindsight Distortion Gap discipline, not a silent
rewrite):** `claim.md`'s kill criterion said CONFIRMED if the clamp reaches "`Proliferation` (or a
new, non-`Growth_arrest` attractor)" — worded ambiguously around BIT-STRING novelty vs. PHENOTYPE
novelty. The reached state IS bit-string-novel (never seen in `H-B7-4`/`H-B7-5`) but is NOT
phenotype-novel: the network itself carries an explicit `Growth_arrest` node
(`Growth_arrest = p21CIP | RBL2 | RB1`) and an explicit `Proliferation` node
(`Proliferation = CyclinE1 | CyclinA`), and both are readable directly from the reached state.
Resolving the ambiguity by INTENT (the model's own semantic phenotype labels, not raw bit-string
distinctness) — the correct, non-verdict-shopped verdict is REJECTED.

**Statement:** *Removing the third redundant repressor (`p21CIP=0`, on top of `RAS=1, TP53=0`) still
fails to reach the `Proliferation` phenotype. The reached attractor reveals WHY at the level of the
network's own explicit phenotype definition: `Growth_arrest` is a THREE-WAY REDUNDANT OR gate over
`p21CIP`, `RBL2`, and `RB1` — clamping only `p21CIP` leaves `RBL2` (which came up to 1 in the new
attractor) sufficient on its own to keep `Growth_arrest=1`.*

## Evidence Summary — Mechanism, Verified Two Independent Ways

**1. Read directly from the `.bnet` source** (`grep` on `remy_tumorigenesis.bnet`):
```
Growth_arrest,  p21CIP | RBL2 | RB1
Proliferation,  CyclinE1 | CyclinA
RB1,            !p16INK4a&!CyclinE1&!CyclinD1&!CyclinA
RBL2,           !CyclinE1&!CyclinD1
p16INK4a,       !RB1&Growth_inhibitors
CyclinD1,       !p21CIP&!p16INK4a&RAS | !p21CIP&!p16INK4a&AKT
```
In this branch, `Growth_inhibitors=1` is fixed, so `p16INK4a = !RB1` exactly. Substituting into
`CyclinD1`'s rule: `CyclinD1=1` requires `p16INK4a=0`, i.e. `RB1=1`. But `RB1=1` requires (by RB1's
own rule) `!CyclinD1=1`, i.e. `CyclinD1=0` — a direct self-contradiction at any FIXED POINT (not
necessarily mid-transient). **Algebraic conclusion: `CyclinD1` cannot be `1` at any fixed point of
this branch, regardless of `RAS`, `p21CIP`, or `TP53`.**

**2. Confirmed independently via `pyboolnet`** on the UNCLAMPED wild-type network restricted to this
exact branch (`DNA_damage=0, EGFR_stimulus=0, FGFR3_stimulus=1, Growth_inhibitors=1`) — all 3 of this
branch's own real attractors (previously scoped in `H-B7-4`) checked directly:

| Attractor | `CyclinD1` | `Growth_arrest` | `Proliferation` | `RB1` | `RBL2` | `p21CIP` |
|---|---|---|---|---|---|---|
| Growth_arrest (original) | **0** | 1 | 0 | 1 | 1 | 1 |
| Growth_arrest (second, previously unnamed) | **0** | 1 | 0 | 0 | 1 | 1 |
| **Proliferation (the real one)** | **0** | 0 | 1 | 0 | 0 | 0 |

**`CyclinD1=0` at all three — including the genuine `Proliferation` attractor itself.** This
independently confirms the algebraic derivation: `CyclinD1` is a structural dead end for escaping
arrest in this branch; the real `Proliferation` attractor is reached via `CyclinE1`/`CyclinA`
directly (through the `E2F3_medium`/`E2F1_medium`/`CDC25A` axis), NOT through `CyclinD1`.

**Why `RAS=1` (all three experiments, `H-B7-4`/`5`/`6`) could never bootstrap this on its own:**
`RAS` has two other direct targets besides `CyclinD1` — `E2F1_medium`
(`!RBL2&!RB1&RAS | ...`) and `E2F3_medium` (`!RB1&RAS | ...`) — but BOTH require `!RBL2&!RB1` as a
precondition. This is a chicken-and-egg loop: `RAS` can only activate `E2F` once `RBL2`/`RB1` are
ALREADY off, which is exactly the escape `RAS` is being asked to cause. Permanently clamping upstream
inputs (`RAS`, `TP53`, `p21CIP`) cannot break this loop from the `Growth_arrest` fixed point — the
network's real `Proliferation` attractor exists in a different reachable region, not accessible via
this straight-line perturbation.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The pipeline correctly composes three simultaneous permanent clamps (`apply_combined_clamp`,
  tested against a hand-traced synthetic "genuine three-hit" network with an explicit redundant
  blocker `D`, mirroring the real mechanism, before trusting the real network's result).
- [x] `Growth_arrest`'s redundancy is not merely empirical (as `H-B7-5` first showed for the
  `TP53`↔`p21CIP` pair) but STRUCTURAL and NAMED IN THE SOURCE: an explicit `p21CIP | RBL2 | RB1`
  three-way OR gate.
- [x] `CyclinD1` is PROVABLY (algebraically, then independently confirmed via `pyboolnet` on all 3
  real attractors of this branch, including the genuine `Proliferation` one) never active at any
  fixed point of this branch — a structural, branch-wide fact, not an artifact of the clamps tested.

### What Was NOT Confirmed
- [x] The three-hit combination does not reach `Proliferation`. The REASON is now understood at the
  level of the network's own phenotype-gate logic, not merely "still didn't work": the real escape
  route (`CyclinE1`/`CyclinA` via `E2F`/`CDC25A`) requires `RBL2`/`RB1` to be off FIRST, which `RAS`
  cannot cause because `RAS`'s own effect on `E2F` requires that precondition already met.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Three permanent hits, none targeting `RBL2`/`RB1` directly | Four-hit permanent `do(RAS=1, TP53=0, p21CIP=0, RBL2=0)` — directly removes the remaining redundant OR-branch identified here | Most surgical next step: completes the removal of all three named `Growth_arrest` OR-branches simultaneously |
| Permanent clamps only | A TRANSIENT kick of `RBL2=0`/`RB1=0` (or directly `CyclinE1=1`/`CDC25A=1`) for a few steps, then released, on top of permanent `RAS=1,TP53=0,p21CIP=0` — targets the chicken-and-egg bootstrapping problem directly, echoing the permanent-vs-transient distinction already explored in `H-B7-2`/`H-B7-3` | Potentially more mechanistically elegant than a 4th permanent knockout — worth testing in parallel, not instead of, the four-hit permanent version |

## What This Does NOT Mean

1. Does NOT mean Kauffman's hypothesis is false in this model — the `Proliferation` attractor is
   real (verified independently via `pyboolnet`) and reachable in principle; this experiment narrows
   HOW it can be reached (not via `RAS`/`TP53`/`p21CIP` permanent clamps alone) rather than showing it
   is unreachable.
2. Does NOT mean the `p21CIP`/`RBL2`/`RB1` redundancy is a general property of real bladder cancer
   biology — it is a property of THIS specific Boolean abstraction's explicit phenotype-gate logic,
   though the underlying biology (Rb-family redundancy, E2F bistability) it abstracts is real and
   well-documented.
3. Does NOT prove `CyclinD1` is irrelevant to real bladder cancer — only that, in THIS model's Boolean
   logic, it cannot be active at any fixed point of THIS branch, a mathematical fact about the rule
   set as written, checked two independent ways (algebra + `pyboolnet`).

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified, `pyboolnet`-cross-checked mechanism.
The `CyclinD1=0`-at-every-fixed-point claim itself was independently verified by `pyboolnet` (not
merely asserted), serving the same evidentiary role a positive control would in a different kind of
experiment.

## Pearl Card Update

**New information (highest-value finding in the B7 series so far):** `Growth_arrest`'s redundancy in
this model is not an emergent pattern discovered by trial-and-error across 3 experiments — it is
NAMED EXPLICITLY in the network's own rule set (`p21CIP | RBL2 | RB1`), and the reason `RAS`
activation cannot bootstrap past it is a provable structural fact (a self-referential loop between
`RB1`, `p16INK4a`, and `CyclinD1`, confirmed algebraically and then independently via `pyboolnet` on
ALL 3 real attractors of the branch, including the genuine `Proliferation` fixed point). This reframes
`H-B7-4`→`H-B7-5`→`H-B7-6` as a single coherent chain: each experiment removed one node from an
explicit 3-way OR gate, and the terminal finding is that the remaining escape route runs through
`CyclinE1`/`CyclinA` directly, not through `RAS`→`CyclinD1` at all.
