# decision.md — 20260906-remy-tumorigenesis-transient-necessity-h9

**Graph node:** `H-B7-9` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-07

## Verdict

- [x] **CONFIRMED** — for `k=10` and `k=30` synchronous steps, the transient `do(p21CIP=0, RBL2=0)`
  clamp, RELEASED back to fully unperturbed wild-type dynamics, settles into the EXACT `Proliferation`
  attractor (byte-identical to `PROLIFERATION_STATE`). The escape PERSISTS after release — this is
  NOT an artifact of a sustained clamp.
- **This is the FIRST confirmation of Kauffman's STRICT original hypothesis anywhere in this
  bridge.** Every prior CONFIRMED result in the B7 series (`H-B7-2`'s `do(Rb=0)`, `H-B7-7`/`H-B7-8`'s
  multi-hit combinations) required the clamp to remain PERMANENT. This is the first case where a
  pathological state, already known to be a genuine attractor of the UNPERTURBED network (verified
  independently by `pyboolnet` in `H-B7-4`), is reached via a TEMPORARY push and then persists once
  the network is returned fully to its own rules — exactly Kauffman's original 1971 framing.

**Statement:** *A sufficiently long (≥10 steps, but not necessarily ≤30) transient push of
`p21CIP=0, RBL2=0`, released back to fully unperturbed dynamics, moves the system permanently from
`Growth_arrest` to `Proliferation` — the pathological attractor pre-exists in the unperturbed network
and is REVEALED, not created, by the perturbation.*

## Evidence Summary — A Clean Duration Threshold

| `k` (steps) | Final phenotype | Final state | Notes |
|---|---|---|---|
| 1 | `Growth_arrest` | `00000000000000010011011000010110011` | Relapses — but NOT to the original `GROWTH_ARREST_STATE`; this is the SECOND (previously found via `pyboolnet` in `H-B7-6`) `Growth_arrest` attractor of this branch |
| 3 | `Growth_arrest` | `00000000000000010011011000010110011` | Same relapse target as `k=1` |
| **10** | **`Proliferation`** | **`00000100101001010011001000110010110`** | **Byte-identical to `PROLIFERATION_STATE`** |
| **30** | **`Proliferation`** | **`00000100101001010011001000110010110`** | **Byte-identical to `PROLIFERATION_STATE`**, same as `k=10` |

**Ancillary data point (`k=0`, not part of the pre-registered duration set, run during the FL Step 8a
skeptic pass as a sanity check):** with zero clamped steps (the clamp is applied to the initial state
itself but immediately released with no dynamics under it), the system does NOT reach either named
fixed point — it settles into a period-2 COMPLEX attractor instead. This confirms the clamped step(s)
genuinely do dynamical work (letting `CyclinD1` transiently rise before `p21CIP`/`RBL2` reassert) —
the escape at `k≥10` is not an artifact of merely poking the initial state.

**A clean threshold between `k=3` and `k=10`**: short pushes relapse to a DIFFERENT `Growth_arrest`
fixed point (not the starting one — a genuine trajectory change, not simply "nothing happened"), while
sufficiently long pushes cross the basin boundary permanently. This is itself a novel, useful finding
beyond the pre-registered binary kill criterion: the escape is not immediate, but requires the network
enough time under the push to complete the `CyclinE1`/`CDC25A`/`E2F` positive-feedback loop
`H-B7-6`/`H-B7-8` identified as the actual escape route, before release is safe.

All 4 durations: `branch_inputs_preserved: true` (the 4 branch-defining external inputs never
drifted).

## FL Step 8a — Skeptic Verdict (context-asymmetric: claim.md + code + data only, no session history)

**Verdict: `CONFIRMED-REAL`.** Skeptic agent (isolated context, no `decision.md`/reasoning history)
reviewed `claim.md`, `run.py`, `metrics/run.json`, the test file, the `.bnet` source, and every
imported helper module. Lacking Bash access itself, it hand-verified both critical failure modes
algebraically against the raw `.bnet` rules and wrote follow-up checks it could not execute; those
were then actually RUN by the main session (which has Bash):

| Check | Result |
|---|---|
| Release genuinely switches from clamped to wild-type rules at exactly step `k` (code trace) | ✅ confirmed by direct reading — `range(k_steps)` under clamped rules, then `run_until_attractor` under `wild_type_rules` |
| `PROLIFERATION_STATE` (k=10/30 result) is NOT a residual-clamp artifact — `p21CIP=0`/`RBL2=0` in that state are HONESTLY derived from their own rules (`!CyclinE1` term), not leftover forcing | ✅ hand-verified against all 35 `.bnet` rules |
| The k=1/3 relapse state is a genuine fixed point, not a mid-trajectory state mistakenly reported as final | ✅ hand-verified against all 35 `.bnet` rules |
| Bit-identical determinism (fresh `cmd_run()` called twice) | ✅ `r1 == r2: True` |
| **k=0 sanity prediction** (skeptic predicted, without being able to run it, that `k=0` would NOT reach either named fixed point but instead a period-2 oscillation, since no clamped step ever lets `CyclinD1` transiently rise) | ✅ **exactly confirmed**: `k=0` → period **2**, complex attractor — neither `Growth_arrest` fixed point nor `Proliferation` |
| **Independent `pyboolnet.compute_attractors()` on the FULLY UNCLAMPED branch** (zero clamps at all — only the 4 branch inputs frozen, `p21CIP`/`RBL2` keep their own original rules) — do all THREE reported states (`GROWTH_ARREST_STATE`, the k=1/3 relapse state, and `PROLIFERATION_STATE`) independently exist as genuine unclamped attractors of this branch? | ✅ **exactly 3 attractors found, matching all three reported states one-to-one** — `GROWTH_ARREST_STATE` (original), the k=1/3 relapse state (second GA), and `PROLIFERATION_STATE` (k=10/30) |

**This is the strongest possible confirmation available**: not only are the reported final states
self-consistent under the rules (hand-verified), an INDEPENDENT tool, given ZERO information about
which clamp was tested, computing the FULLY UNCLAMPED branch's attractor set from scratch, finds
EXACTLY these three states and no others — this is precisely `H-B7-4`'s original branch-scoping
result (3 attractors: 2 `Growth_arrest` + 1 `Proliferation`), now with the two `Growth_arrest`
attractors individually identified as the specific relapse targets for short vs. long transient
pushes.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] Kauffman's STRICT hypothesis, previously untestable (`H-B7-3`, wrong model) or untested
  (`H-B7-4`–`8`, all permanent clamps), receives its first clean confirmation in this bridge.
- [x] The escape mechanism traced across `H-B7-6`/`H-B7-7`/`H-B7-8` (removing the `p21CIP`/`RBL2`
  branches of the `Growth_arrest` OR gate lets `CyclinE1`/`CDC25A`/`E2F` positive feedback take over)
  is confirmed to be SELF-SUSTAINING once established — it does not require the clamp to persist,
  only to persist LONG ENOUGH to complete.

### What Was NOT Confirmed
- [x] The exact minimum sufficient duration is not pinned down more precisely than "between 4 and 9
  steps" (only 1, 3, 10, 30 were tested) — a finer sweep would be needed to find it exactly.
- [x] Whether this generalizes to other multistable branches or clamp combinations in this model
  remains untested.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Duration set `{1,3,10,30}` | Finer sweep (e.g. `4,5,6,7,8,9`) to pin down the exact threshold | Cheap — no new pipeline code, reuses `simulate_transient_clamp_multi` with a denser `TESTED_DURATIONS` |
| This one branch, this one clamp pair | Test transient `p21CIP`/`RBL2` release on one of the other 7 multistable branches found in `H-B7-4`'s scoping | Tests generality of the duration-threshold pattern beyond this one branch |

## What This Does NOT Mean

1. Does NOT establish the exact minimum duration — only that it lies strictly between 3 and 10 steps
   for this specific branch and clamp pair.
2. Does NOT mean every transient perturbation in this model would show the same threshold structure —
   this is specific to the `p21CIP`/`RBL2` pair and this branch's own feedback-loop completion time.
3. Does NOT generalize to real bladder cancer timing/dosing — this is a discrete synchronous-update
   Boolean abstraction; "steps" have no direct real-time unit.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified, `pyboolnet`-cross-checked mechanism.

## Pearl Card Update

**New information (high impact — first strict-Kauffman confirmation in the bridge, plus a clean
duration threshold):** this closes the original methodological gap named all the way back in
`H-B7-2`'s decision.md (distinguishing the weak "new attractor from permanent clamp" reading from the
strict "pre-existing attractor revealed by temporary push" reading) — the strict reading is now
CONFIRMED for at least one clamp pair and branch, with an unexpected bonus: a sharp, previously-unseen
duration threshold between relapse and permanent escape, and the relapse target itself is not the
original starting state but a SECOND, distinct `Growth_arrest` fixed point already catalogued in
`H-B7-6`.
