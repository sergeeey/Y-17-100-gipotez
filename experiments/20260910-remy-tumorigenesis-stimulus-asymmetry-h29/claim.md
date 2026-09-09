# claim.md — 20260910-remy-tumorigenesis-stimulus-asymmetry-h29

**Graph node:** `H-B7-29` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Full
**Parent:** `H-B7-28` (branch isomorphism via `φ=flip(EGFR_stimulus)`, confirmed CONFIRMED across
H-B7-22's own full domain). Direct continuation under the "hold the mechanism" mission
(research-methodology.md's Mechanism Development Mode, question 5: structural asymmetry — is there
an asymmetry explaining why an effect is strong in one place and absent in another, and what
creates it?).

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Comparing graph-structural/boolean-invariant behavior between two
specific candidate bijections on a fully specified deterministic system. Not causal, not a
statistical estimate.

## Origin and design rationale

`EGFR_stimulus` and `FGFR3_stimulus` are structurally similar-LOOKING nodes: both are frozen
self-loops in the `.bnet` source (`EGFR_stimulus,EGFR_stimulus` and
`FGFR3_stimulus,FGFR3_stimulus` — neither ever changes value during any trajectory). H-B7-27/28
established that flipping `EGFR_stimulus` is causally inert (a genuine graph automorphism) across
H-B7-22's entire tested domain. This experiment asks the natural contrast question: is
`FGFR3_stimulus` ALSO inert, or is the H-B7-27/28 finding specific to `EGFR_stimulus`'s particular
algebraic masking?

**Prediction, stated BEFORE testing (per Mechanism Development Mode discipline — reason first,
serialize after):** `FGFR3_stimulus` should NOT be inert. `FGFR3`'s own rule is
`!GRB2 & FGFR3_stimulus & !EGFR` — it reads `FGFR3_stimulus` directly and load-bearingly (unlike
`EGFR`'s rule, which only reads `EGFR_stimulus` under a condition — `!GRB2&!FGFR3` — that H-B7-27/28
proved never holds). The entire `FGFR3≡True` invariant that makes `EGFR_stimulus` irrelevant is
ITSELF built on `FGFR3_stimulus=True` being held fixed. Flipping `FGFR3_stimulus` should collapse
`FGFR3≡True`, which should collapse the whole downstream invariant chain — a genuine asymmetry, not
a coincidence that both nodes happen to be frozen self-loops.

**Compute-First Check (scratchpad, `branch_1/k=1`):** confirmed the prediction, sharply. Flipping
`FGFR3_stimulus` at the same release state is NOT a node-set bijection (`isomorphism_confirmed:
False`). The resulting reachable graph hit `STATE_CAP=30000` (the original, unflipped graph has
956 states) — a partial BFS visited 40528 states before the cap stopped it, with `FGFR3=False` in
~97.6% of those (39574/40528). **The exact count is NOT treated as verified** (`hit_cap=True` means
this is `BLOCKED-INFRASTRUCTURE` for the precise full-domain size, per FL Step 2a — not evidence
against the claim). What IS verified without any cap ambiguity: the flipped graph's size alone,
even truncated, already vastly exceeds the original's 956 states, which alone rules out a
node-set bijection — no cap-sensitive number is needed to establish non-isomorphism.

**Minimal Relaxation Rule compliance:** this is a genuinely new contrast claim (not a relaxation of
a prior REJECT) — testing the OTHER frozen self-loop node as a natural next question from
H-B7-27/28's own findings.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "`FGFR3_stimulus`, unlike `EGFR_stimulus`, is load-bearing: `FGFR3`'s rule
reads it directly and unconditionally (given `!GRB2`, `!EGFR` — both already established elsewhere
in this reachable region), so flipping `FGFR3_stimulus` should collapse the `FGFR3≡True` invariant
the entire H-B7-27/28 mechanism depends on, producing a dramatically larger and non-isomorphic
reachable region rather than an inert coordinate flip."

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The reachable graph from each of H-B7-27's own tested `(branch, k)` release states (`k=1..5`), compared against the reachable graph from the SAME release state with `FGFR3_stimulus` flipped |
| **Falsifiable predicate** | Is `φ'=flip(FGFR3_stimulus)` a graph isomorphism between the original and flipped reachable graphs, the same way `φ=flip(EGFR_stimulus)` is (H-B7-27/28)? |
| **Measurable outcome** | Per-condition: node-set-bijection pass/fail (predicted FAIL for all); `STATE_CAP` hit or not (informational, not a pass/fail criterion); when not capped, exact violation counts for the `FGFR3≡True` invariant in the flipped graph |

## Kill Criterion (set BEFORE running the full sweep)

- **Primary (mandatory, cap-independent):** for EVERY condition (`k=1..5`, both branches),
  `φ'=flip(FGFR3_stimulus)` must FAIL to be a node-set bijection between the original and flipped
  reachable graphs — i.e., the asymmetry prediction is CONFIRMED if the bijection fails everywhere,
  REJECTED if it unexpectedly succeeds anywhere (which would mean `FGFR3_stimulus` is ALSO inert,
  contradicting the stated mechanism).
- **STATE_CAP is explicitly NOT part of the kill criterion** — a capped flipped-graph is expected
  and informative (a much larger reachable set is itself evidence of non-inertness), not a failure.
  Any condition that hits `STATE_CAP` is recorded `BLOCKED-INFRASTRUCTURE` for its exact size only;
  the node-set-bijection-fails-because-cap-alone-exceeds-original-size check does NOT require an
  uncapped count and is evaluated independently.

## What This Does NOT Mean

1. Does NOT claim to have found the network's full symmetry group, or an exhaustive list of which
   nodes are/aren't inert — only tests this one specific contrast (`EGFR_stimulus` vs
   `FGFR3_stimulus`).
2. Does NOT compute exact reachable-set sizes or exact invariant-violation counts for any condition
   that hits `STATE_CAP` — those numbers are reported as capped/partial where they appear at all,
   never as verified exact totals.
3. Does NOT itself resolve the large-deviation/Kramers question, still deliberately deferred.
4. Does NOT retroactively weaken H-B7-27/28's own confirmed `EGFR_stimulus` isomorphism — this is a
   contrast/control finding that STRENGTHENS confidence the H-B7-27/28 mechanism is specific
   (algebraically explained), not a generic artifact of "any frozen input is safe to flip."

## MCID

Not applicable — exact boolean/graph-structural claim, no statistical estimate.
