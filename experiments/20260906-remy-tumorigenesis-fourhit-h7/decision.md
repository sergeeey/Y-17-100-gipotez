# decision.md — 20260906-remy-tumorigenesis-fourhit-h7

**Graph node:** `H-B7-7` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-06

## Verdict

- [x] **CONFIRMED** — the combined permanent `do(RAS=1, TP53=0, p21CIP=0, RBL2=0)` clamp, started from
  the `Growth_arrest` fixed point, settles into the EXACT `Proliferation` attractor
  (`final_state_pyboolnet_order` is byte-identical to `PROLIFERATION_STATE`). The model's own
  phenotype nodes confirm this unambiguously: `Growth_arrest=False`, `Proliferation=True`.
- **This is the FIRST confirmed permanent-clamp escape from `Growth_arrest` to `Proliferation` in the
  entire B7 bridge**, closing the chain `H-B7-4` (REJECTED, single-hit) → `H-B7-5` (REJECTED, two-hit)
  → `H-B7-6` (REJECTED, three-hit, mechanism named) → `H-B7-7` (CONFIRMED, four-hit).

**Statement:** *Removing all three named branches of the `Growth_arrest` redundant OR gate
(`p21CIP | RBL2 | RB1` — `p21CIP` directly clamped, `RBL2` directly clamped, `RB1` already proven
dead by `H-B7-6`'s own algebraic/`pyboolnet`-confirmed argument whenever `p16INK4a`'s coupling holds)
is SUFFICIENT, together with `RAS=1` and `TP53=0`, to move the system permanently into the
`Proliferation` phenotype — the exact attractor state independently verified by `pyboolnet` in
`H-B7-4`.*

## Evidence Summary

| Field | Value |
|---|---|
| `final_state_pyboolnet_order` | `00000100101001010011001000110010110` |
| `proliferation_state` (from `H-B7-4`, `pyboolnet`-verified) | `00000100101001010011001000110010110` |
| Match | **Byte-identical** |
| `growth_arrest_phenotype_node` | `False` |
| `proliferation_phenotype_node` | `True` |
| `final_attractor_type` | point (period 1) — a genuine fixed point, not a transient or cycling state |
| `branch_inputs_preserved` | `True` — the 4 branch-defining external inputs did not drift under the 4 simultaneous clamps |

Cross-checked against the pipeline's own composition test (`test_apply_combined_clamp_helper_handles_four_simultaneous_clamps`)
and a hand-traced synthetic "genuine four-hit" network (two independent redundant blockers `D`, `E`,
mirroring the real `p21CIP`/`RBL2` pair) BEFORE trusting the real result — the synthetic test confirmed
three hits alone (removing only one of two blockers) is insufficient, and all four hits together flip
the toy network, exactly matching the real network's qualitative behavior.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The chain of reasoning built across `H-B7-4`→`H-B7-6` was CORRECT and COMPLETE: `Growth_arrest`
  in this branch is sustained by exactly the three named redundant mechanisms
  (`p21CIP`, `RBL2`, and `RB1`'s structural dead-end via `CyclinD1`), and removing the two directly
  clampable ones (`p21CIP`, `RBL2`) — while `RB1`'s route was already proven unreachable — is
  SUFFICIENT to escape arrest.
- [x] The escape route is exactly the one `H-B7-6` predicted: through `CyclinE1`/`CyclinA` via the
  `E2F3_medium`/`E2F1_medium`/`CDC25A` axis, NOT through `CyclinD1` (which remains irrelevant — its
  value was not specifically re-examined here, but the reached state is byte-identical to the known
  `Proliferation` attractor where `CyclinD1=0`, per `H-B7-6`'s own table).
- [x] Kauffman's Cancer Attractor hypothesis, in its STRICT permanent-perturbation operationalization,
  receives its first clean confirmation in this bridge: a MULTI-HIT combination of clamps on a real,
  published cancer network moves the system from one biologically-labeled phenotype attractor
  (`Growth_arrest`) to another (`Proliferation`) that pre-existed in the unperturbed network (verified
  independently by `pyboolnet` in `H-B7-4`) — consistent with, and a direct confirmation of, multi-hit
  carcinogenesis theory as modeled here.

### What Was NOT Confirmed
- [x] This does NOT establish that all four hits are individually NECESSARY (only that they are
  jointly SUFFICIENT) — `H-B7-6`'s own finding suggests `RB1`'s contribution may already be structurally
  moot once `p21CIP`/`RBL2` are off, meaning a THREE-hit combination targeting `p21CIP`+`RBL2` alone
  (without `TP53`, or without `RAS`) might also succeed — untested here.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Four hits: `RAS`+`TP53`+`p21CIP`+`RBL2` | Necessity test: `do(p21CIP=0, RBL2=0)` alone (drop `RAS`/`TP53`) — checks whether the upstream oncogene/suppressor pair was ever load-bearing, or whether directly clamping the two OR-branches was always sufficient by itself | Directly tests the "What Was NOT Confirmed" gap above — cheap, no new pipeline code needed |
| Permanent clamp only | A TRANSIENT (released) version of this same four-node combination — does the system relapse back to `Growth_arrest` once released, or does it stay in `Proliferation` (implying `Proliferation` is a genuine independent attractor of the WILD-TYPE unperturbed rules once reached, not merely an artifact of the sustained clamp) | High-value: distinguishes "clamp holds the phenotype open" from "clamp pushes the system across a real basin boundary of the unperturbed network," the sharper reading of Kauffman's strict claim (echoing the permanent-vs-transient distinction from `H-B7-2`/`H-B7-3`) |

## What This Does NOT Mean

1. Does NOT establish that this four-hit combination, or any subset of it, causes bladder cancer
   progression in real patients — this is a confirmation within a specific Boolean abstraction of one
   published model, not a claim about real-world tumor biology.
2. Does NOT mean every perturbation combination targeting `Growth_arrest`'s OR-gate branches will
   succeed — this experiment tested exactly the combination motivated by `H-B7-6`'s own traced
   mechanism, not an exhaustive search.
3. Does NOT resolve whether the individual hits are all necessary (see Relaxation Map above) — a
   genuine open question, not yet tested.
4. Does NOT test whether this is reachable via a TRANSIENT rather than PERMANENT clamp — the strict
   original form of Kauffman's hypothesis (a pathological state pre-existing as an attractor of the
   UNPERTURBED network, revealed by a temporary push) remains to be tested for this specific branch
   and combination.

## FL Step 8a — Skeptic Verdict (context-asymmetric: claim.md + code + data only, no session history)

**Verdict: `CONFIRMED-REAL`.** Skeptic agent (isolated context) reviewed `claim.md`, `run.py`,
`metrics/run.json`, the test file, the `.bnet` source, and every imported helper module —
deliberately WITHOUT `decision.md` or any of this project's own reasoning, to avoid agreeableness
bias. It generated 5 concrete falsification attempts. It could not execute Python itself (tool
restriction), so it hand-verified both fixed points algebraically against the raw `.bnet` rules and
wrote an executable falsification script; that script was then actually RUN (by the main session,
which does have Bash) rather than left as an unexecuted recommendation:

| Check | Result |
|---|---|
| `PYBOOLNET_NODE_ORDER` genuinely alphabetical, matches the `.bnet`'s 35 node names exactly | ✅ `sorted(.bnet) == PYBOOLNET_NODE_ORDER` — True |
| `apply_combined_clamp` replaces EXACTLY the 4 target nodes with constants, 0 other nodes' rules touched | ✅ 0 diffs among the other 31 nodes |
| This project's own pipeline: WT rules from `Growth_arrest` stay at `Growth_arrest` (sanity); four-hit clamp reaches `Proliferation` exactly | ✅ both byte-identical matches |
| **Independent reproduction via `pyboolnet.compute_attractors()`** (branch-restricted + four-clamped `.bnet`, built fresh, zero reuse of this project's own simulation code) | ✅ exactly **1** attractor found, `is_steady=True`, `is_univocal=yes`, `is_faithful=yes`, state byte-identical to `PROLIFERATION_STATE` |
| `metrics/run.json` freshness (not a stale cached file) | ✅ fresh run matches the stored file exactly |
| Branch-defining inputs did not silently drift under the 4 clamps | ✅ all 4 preserved, and structurally guaranteed (identity rules in the `.bnet`) |

**This is the highest independent-verification tier used anywhere in this bridge** (Independent
Verification Strength Ladder: "different tool, same task") — `pyboolnet`'s own attractor computation,
built from a freshly-constructed `.bnet` file, with zero dependency on this project's hand-rolled
`synchronous_step`/`run_until_attractor` code.

**One real WEAKENING observation, not a falsification, incorporated into the record:** the skeptic
found that `RAS=1` and `TP53=0` are ALREADY the values present at the `GROWTH_ARREST_STATE` starting
point (`RAS=1` via `FGFR3` signaling already active in this branch; `TP53=0` already off) — so those
two clamps are no-ops relative to the actual starting state, and the entire empirical effect is
carried by the two genuinely novel perturbations, `p21CIP=0` and `RBL2=0`. This does not change the
verdict (the pre-registered predicate and the four literal clamps are exactly what was tested and
exactly what succeeded), but it sharpens the claim: **the minimal SUFFICIENT perturbation demonstrated
here, relative to this specific starting fixed point, is the two-hit `do(p21CIP=0, RBL2=0)`** — already
named as the top row of this experiment's own Relaxation Map below, now with independent motivation
from the skeptic pass rather than only from `H-B7-6`'s own reasoning.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified, `pyboolnet`-cross-checked mechanism.
The reached state's identity was verified against `pyboolnet`'s independently-computed
`PROLIFERATION_STATE` (inherited from `H-B7-4`), serving the same evidentiary role a positive control
would.

## Pearl Card Update

**New information:** the first CONFIRMED result in the B7 bridge for a permanent multi-hit
perturbation reaching the true `Proliferation` phenotype — completing a 4-experiment mechanistic
chain (`H-B7-4`→`H-B7-7`) where each step's REJECT motivated the next hit with increasing precision,
ending in a clean, byte-identical match to an independently-verified attractor. This is a strong,
concrete illustration of the Relaxation Map / Minimal-Relaxation-adjacent discipline actually working
as intended over multiple iterations: no step guessed blindly, each built directly on the prior
step's traced mechanism.
