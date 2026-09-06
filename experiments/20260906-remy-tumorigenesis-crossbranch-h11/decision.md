# decision.md — 20260906-remy-tumorigenesis-crossbranch-h11

**Graph node:** `H-B7-11` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-07

## Verdict

- [x] **CONFIRMED** — the permanent `do(p21CIP=0, RBL2=0)` clamp, already established as sufficient
  on the FIRST branch (`H-B7-8`), ALSO reaches the `Proliferation` phenotype on the SECOND branch
  `(DNA_damage=0, EGFR_stimulus=1, FGFR3_stimulus=1, Growth_inhibitors=1)` — byte-identical to the
  independently `pyboolnet`-verified `PROLIFERATION_STATE_2`.
- **This is the first cross-branch generalization confirmed in this bridge.** Every prior H-B7-4–10
  experiment used the SAME single branch.

**Statement:** *The `p21CIP`/`RBL2`-suffices-for-escape finding is not specific to the one branch
tested throughout `H-B7-4`–`H-B7-10` — it generalizes to the only other branch of this network that
offers the same structural precondition (genuine `Growth_arrest`/`Proliferation` phenotype
divergence), differing by exactly one input bit (`EGFR_stimulus`).*

## Evidence Summary

| Field | Value |
|---|---|
| Branch tested | `(DNA_damage=0, EGFR_stimulus=1, FGFR3_stimulus=1, Growth_inhibitors=1)` |
| `final_state_pyboolnet_order` | `00000100101001010111001000110010110` |
| `PROLIFERATION_STATE_2` (independently `pyboolnet`-verified) | `00000100101001010111001000110010110` |
| Match | **Byte-identical** |
| `branch_inputs_preserved` | `True` |

**Same mechanism, not a coincidental byte match:** the branch-1 and branch-2 `Proliferation` states
differ at EXACTLY one bit position (`EGFR_stimulus`, position 17 in `PYBOOLNET_NODE_ORDER`) — every
other node, including `CyclinE1`, `CyclinA`, `CDC25A`, `E2F1_medium`, `E2F3_medium`, `p16INK4a`
(the exact escape-route nodes `H-B7-6`/`H-B7-10` traced), is identical between the two branches'
`Proliferation` attractors.

## Compute-First Scoping (before designing this experiment)

Re-enumerated all 16 input branches via `pyboolnet.compute_attractors()` (see
`data/branch_scoping.md`). Found exactly ONE other branch with genuine phenotype divergence besides
the one used throughout `H-B7-4`–`H-B7-10`. **This scoping also caught and corrected a minor factual
error** in `H-B7-4`'s original count: 7, not 8, of the 16 branches are multistable (total attractor
count of 25 matches exactly, confirming same underlying computation — only the multistable-branch
tally was off by one). Documented as a dated correction addendum in `H-B7-4`'s own `Data_README.md`,
per Hindsight Distortion Gap discipline (not a silent rewrite). The "two branches with different
phenotypes" claim was already correct.

## FL Step 8a — Skeptic Verdict (context-asymmetric: claim.md + code + data only, no session history)

**Verdict: `CONFIRMED-REAL`.** Skeptic agent (isolated context) reviewed the claim, code, data, and
tests. Lacking Bash access, it hand-verified the arithmetic (fixed-point checks, honest-derivation
check for the clamped nodes, a 7-step manual trace of the trajectory) and wrote an executable
verification script for the one check it could not close by hand (exhaustive attractor enumeration
on the second branch). That script was then actually RUN by the main session:

| Check | Result |
|---|---|
| `GROWTH_ARREST_STATE_2` is a genuine wild-type fixed point (hand-verified, all 35 rules) | ✅ |
| `PROLIFERATION_STATE_2` is a genuine fixed point of the CLAMPED rules | ✅ |
| **Honest derivation** — `p21CIP`/`RBL2` at `PROLIFERATION_STATE_2` ALSO independently evaluate to `False` under their own real (unclamped) rule formulas, not merely held by the clamp | ✅ both `False`, matching the clamp value |
| `PYBOOLNET_NODE_ORDER` is branch-independent (same 35 sorted node names regardless of input values) | ✅ confirmed |
| Bit-for-bit determinism (2 fresh runs) | ✅ |
| **Exhaustive attractor enumeration on the second branch** (the one check the skeptic could not close by hand) | ✅ exactly **3** attractors found — matching `GROWTH_ARREST_STATE_2`, `SECOND_GA_STATE_2`, and `PROLIFERATION_STATE_2` precisely |
| Mechanism comparison: branch-1 vs branch-2 `Proliferation` states differ at exactly one bit (`EGFR_stimulus`) | ✅ same escape-route nodes (`CyclinE1`, `CyclinA`, etc.) active in both |

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The `p21CIP`/`RBL2` sufficiency pattern generalizes across the ONLY 2 branches of this model
  that offer the structural precondition to test it at all.
- [x] The escape mechanism is structurally identical between branches (same downstream nodes active),
  not a coincidental match.

### What Was NOT Confirmed
- [x] Generalization to the other 5 multistable branches, which lack a `Proliferation` attractor
  entirely and cannot be tested this way — the finding is confirmed on 2 of 2 TESTABLE branches, not
  2 of 7 multistable branches.
- [x] Whether the transient (not permanent) version of this clamp also generalizes to this second
  branch — untested here.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Permanent clamp only | Transient version of `do(p21CIP=0, RBL2=0)` on this second branch, mirroring `H-B7-9`'s test on the first — check whether the same duration threshold (or a different one) applies | Directly tests whether `H-B7-10`'s `k*=5` finding is branch-specific or a general property of this escape mechanism |

## What This Does NOT Mean

1. Does NOT mean the pattern generalizes to EVERY branch of this model — only the 2 branches that
   have a `Proliferation` attractor to escape to at all; the other 5 multistable branches are
   `Growth_arrest`-only and this question does not apply to them.
2. Does NOT establish real-world generality for bladder cancer biology — this is a within-model
   generalization across two synthetic input conditions of one published Boolean abstraction.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified, `pyboolnet`-cross-checked mechanism.

## CORRECTION ADDENDUM (2026-09-07, H-B7-12 scoping — Hindsight Distortion Gap discipline, not a
silent rewrite)

`H-B7-12`'s own FL Step 8a skeptic pass found, and this session independently verified against the
`.bnet` source, that `EGFR`'s rule (`SPRY&!GRB2&!FGFR3 | !GRB2&!FGFR3&EGFR_stimulus`) requires
`!FGFR3` in BOTH disjuncts — and since `FGFR3_stimulus=1` is fixed identically in BOTH this
experiment's branch and `H-B7-4`'s original branch, `EGFR` is forced to `0` regardless of
`EGFR_stimulus`'s value. **The two branches tested here are dynamically equivalent** — the one input
bit that differs between them (`EGFR_stimulus`) never actually propagates to anything. This does NOT
change the CONFIRMED verdict above (the clamp genuinely reaches `Proliferation` on this second
branch, independently `pyboolnet`-verified) — but it corrects the "first confirmed cross-branch
generalization" framing: this experiment demonstrates robustness to one specific INERT input
difference, not a test against a genuinely different dynamical regime. `H-B7-12` additionally found
that this network offers NO OTHER branch with a `Proliferation` attractor to test against — the
cross-branch generalization question for this specific escape target is now EXHAUSTED, not merely
answered once. See `experiments/20260906-remy-tumorigenesis-crossbranch-transient-h12/decision.md`
for the full analysis.

## Pearl Card Update

**New information:** the first confirmed cross-branch generalization in this bridge — and one that
came with a bonus finding along the way (the `H-B7-4` branch-count correction). The mechanism traced
across `H-B7-6`–`H-B7-10` (an explicit `Growth_arrest` OR gate plus a `CyclinE1`-driven positive
feedback escape) turns out to be a property of the network's internal `Cyclin`/`E2F`/`RB1` core, not
tied to the specific `EGFR_stimulus`/`FGFR3_stimulus` input configuration that happened to be tested
first — consistent with the mechanism's own traced logic never directly referencing those input
nodes.
