# decision.md — 20260906-remy-tumorigenesis-crossbranch-transient-h12

**Graph node:** `H-B7-12` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-07

## Verdict

- [x] **CONFIRMED-GENERALIZES-SAME-THRESHOLD (kill criterion met literally), WEAKENED in
  interpretation (per FL Step 8a Response Matrix)** — `k=1,3,4` relapse to this branch's own second
  `Growth_arrest` fixed point; `k=5,6,9,10,30` all reach the exact `Proliferation` attractor for this
  branch. Threshold is exactly `k*=5`, matching `H-B7-10`'s first-branch result precisely.

**Correction to the interpretive framing (not the technical result — Response Matrix: WEAKENED,
Accepted):** the FL Step 8a skeptic pass found, and this session independently verified, that
`EGFR`'s rule (`SPRY&!GRB2&!FGFR3 | !GRB2&!FGFR3&EGFR_stimulus`) requires `!FGFR3` in BOTH disjuncts.
Since `FGFR3_stimulus=1` is fixed identically in both `H-B7-11`'s and this experiment's branch, and
this forces `FGFR3=1` along the relevant trajectory, `EGFR` is forced to `0` REGARDLESS of
`EGFR_stimulus`'s value. **The two "branches" tested across `H-B7-11`/`H-B7-12` are dynamically
equivalent** — the one differing input bit never actually propagates to anything. The identical
`k*=5` threshold is therefore an ARITHMETIC NECESSITY of that equivalence, not independent evidence
that the escape mechanism's timing is branch-invariant in a stronger sense.

**Statement (corrected):** *The transient escape and its exact `k*=5` threshold reproduce identically
on the only other branch with a `Proliferation` attractor to escape to — but this branch differs from
the first only in an input (`EGFR_stimulus`) that is provably inert given `FGFR3_stimulus=1`. This
experiment demonstrates the mechanism is robust to that one specific inert perturbation, not that it
generalizes across a genuinely different dynamical regime.*

## A Further, Conclusive Finding: the Generalization Space Is Exhausted

Re-checked the full branch scoping from `H-B7-11`'s `data/branch_scoping.md`: of the 7 multistable
branches in this network, only **2** have a `Proliferation` attractor at all — and both require the
IDENTICAL combination `(DNA_damage=0, FGFR3_stimulus=1, Growth_inhibitors=1)`, differing only in the
now-shown-to-be-inert `EGFR_stimulus`. **There is no remaining branch in this model that could test
the escape mechanism against a genuinely different dynamical input configuration** — the other 5
multistable branches lack a `Proliferation` attractor entirely (a different, unrelated question).
This closes the cross-branch generalization line of inquiry for this specific network, not because
the answer is negative, but because the question has been fully answered by exhaustion of the
available test space.

## Evidence Summary

| `k` | Outcome (this branch) | State |
|---|---|---|
| 1, 3, 4 | `Growth_arrest` (second fixed point, this branch's own) | `00000000000000010111011000010110011` |
| **5** | **`Proliferation`** | **`00000100101001010111001000110010110`** |
| 6, 9, 10, 30 | `Proliferation` (identical to `k=5`) | `00000100101001010111001000110010110` |

`k_star: 5`, `threshold_matches_first_branch: true`.

## FL Step 8a — Skeptic Verdict (context-asymmetric: claim.md + code + data only, no session history)

**Verdict: `CONFIRMED-REAL`, with the WEAKENED interpretive caveat above (Response Matrix: Accepted,
not dismissed).** Skeptic agent flagged the "suspiciously convenient" exact threshold match as a
reason for MORE scrutiny, not less — and found the real explanation (`EGFR` gated by `FGFR3`,
verified directly against the `.bnet` source: `grep` confirms both `EGFR` disjuncts require `!FGFR3`,
and `FGFR3_stimulus=1` is fixed identically across both branches). It also independently hand-traced
the full `k=4`/`k=5` boundary on this branch and confirmed the SAME one-step `CyclinE1` race
mechanism `H-B7-10` found on the first branch — genuinely the same mechanism, correctly generalizing,
just not across as different a setting as the "cross-branch" framing implied.

| Check | Result |
|---|---|
| `GROWTH_ARREST_STATE_2`/`PROLIFERATION_STATE_2` are genuine fixed points (hand-verified against all 35 rules for this branch's specific inputs) | ✅ |
| `p21CIP`/`RBL2` at `PROLIFERATION_STATE_2` honestly derived, not residual clamp | ✅ |
| Full per-step trace of `k=4` vs `k=5` reproduces the exact one-step `CyclinE1` race condition from `H-B7-10` | ✅ same mechanism |
| `PYBOOLNET_NODE_ORDER`/`TESTED_DURATIONS` reuse from prior experiments is correct (node set is branch-independent), not stale | ✅ |
| **`EGFR_stimulus` is dynamically inert given `FGFR3_stimulus=1`** (the key WEAKENING finding) | ✅ confirmed directly against the `.bnet` source |

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The transient escape mechanism and its exact `k*=5` threshold are robust to the one dimension
  of variation actually available among this model's `Proliferation`-capable branches.
- [x] The escape mechanism itself (traced in `H-B7-6`, `H-B7-10`) is confirmed identical, not merely
  coincidentally matching, between the two tested configurations.

### What Was NOT Confirmed
- [x] Genuine cross-branch generalization across a dynamically DIFFERENT input regime — no such
  branch exists in this model to test against, for this specific escape target.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Branch generalization within THIS model | Test the SAME `p21CIP`/`RBL2` escape mechanism on a DIFFERENT published Boolean cancer model with its own `Growth_arrest`/`Proliferation`-style OR-gate structure | The only way to genuinely test cross-context generalization further, given this model's own branch space is exhausted for this question |

## What This Does NOT Mean

1. Does NOT mean the `p21CIP`/`RBL2` mechanism is fragile or branch-specific — it means this
   PARTICULAR model offers no further branch to test it against for this specific escape target.
2. Does NOT retroactively invalidate `H-B7-11`'s own CONFIRMED verdict — the technical result (clamp
   reaches `Proliferation` on the second branch) stands; only the "generalization" framing is
   corrected, in both this file and a matching addendum added to `H-B7-11`'s own `decision.md`.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified, `pyboolnet`-cross-checked mechanism.

## Pearl Card Update

**New information (a genuinely useful negative-space finding, not merely a positive result):**
"generalizes across branches" claims for THIS network should always first check whether the two
compared branches are dynamically distinguishable at all — a branch differing only in an input gated
out by another fixed input (here, `EGFR_stimulus` behind `FGFR3=1`) produces a guaranteed match, not
evidence. The Compute-First branch scoping in `H-B7-11` should have checked THIS before framing the
experiment as a generalization test — a cheap addition (trace which inputs the target mechanism's
own dependency chain actually reads) that would have caught this before running, not after.
