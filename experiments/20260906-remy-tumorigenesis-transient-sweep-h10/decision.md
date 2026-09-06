# decision.md — 20260906-remy-tumorigenesis-transient-sweep-h10

**Graph node:** `H-B7-10` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-07

## Verdict

- [x] **CONFIRMED** — a single clean monotone threshold exists at `k*=5`: `k=4` relapses to the
  "second" `Growth_arrest` fixed point `H-B7-9` identified; `k=5,6,7,8,9` all reach the exact
  `Proliferation` attractor. Fully consistent with `H-B7-9`'s own boundary cases (`k=3` relapse,
  `k=10` escape).

**Statement:** *The transient `do(p21CIP=0, RBL2=0)` escape has an EXACT minimum duration of 5
synchronous steps on this branch, starting from `GROWTH_ARREST_STATE` — not merely "somewhere between
4 and 9."*

## Evidence Summary

| `k` | Outcome | State |
|---|---|---|
| 4 | `Growth_arrest` (second fixed point) | `00000000000000010011011000010110011` |
| **5** | **`Proliferation`** | **`00000100101001010011001000110010110`** |
| 6–9 | `Proliferation` (identical to `k=5`) | `00000100101001010011001000110010110` |

`k_star: 5`, `is_clean_monotone_threshold: true` (computed directly by `run.py`, independently
verified by re-running twice bit-for-bit identically).

## The Exact Mechanism — a Race Condition in Synchronous Update

A full per-step trace (run during the FL Step 8a skeptic pass) of `k=4` vs. `k=5` under the clamp,
watching `CyclinE1`, `CDC25A`, `E2F3_medium`, `E2F1_medium`, `p21CIP`, `RBL2`, `RB1`, reveals EXACTLY
why the threshold is 5, not merely "somewhere in the gap":

**Both trajectories are IDENTICAL through clamped step 4**: `RB1` drops at step 2, `E2F3_medium`/
`E2F1_medium` activate at step 3, `CDC25A` activates at step 4. `CyclinE1` is still `False` at the end
of clamped step 4 in BOTH cases (it requires `CDC25A` to already be `True`, which only just happened).

- **`k=4` (release after step 4):** at the moment of release, `CyclinE1` is still `False`. The
  RELEASE step computes `p21CIP`/`RBL2` from the PRE-release state (`CyclinE1=False`) — their rules
  (`...&!CyclinE1&...`) both evaluate to `True` again, SIMULTANEOUSLY with `CyclinE1` finally turning
  `True` in that same synchronous update. `p21CIP`/`RBL2` being back on immediately blocks
  `CyclinE1`'s self-sustaining condition (`!p21CIP&!RBL2&...`), so `CyclinE1` drops back to `False`
  the very next step. The system settles into an oscillation that resolves to the second
  `Growth_arrest` fixed point.
- **`k=5` (release after step 5):** the clamp is held ONE STEP LONGER. `CyclinE1` turns `True` DURING
  clamped step 5, WHILE `p21CIP`/`RBL2` are still forced `False` by the clamp. At release, `p21CIP`/
  `RBL2`'s rules now evaluate against a state where `CyclinE1=True` ALREADY — `!CyclinE1=False` keeps
  them off. The positive feedback (`CyclinE1` keeps `p21CIP`/`RBL2` off, which keeps `CDC25A`/
  `CyclinE1` on) is now self-sustaining from the first released step onward.

**The entire threshold is a single synchronous step's difference in whether `CyclinE1`'s activation
lands ONE STEP BEFORE or SIMULTANEOUSLY WITH the clamp's release** — a razor-thin race condition
between the clamp's own release timing and the feedback loop's own completion time, not a fuzzy or
approximate boundary.

## FL Step 8a — Skeptic Verdict (context-asymmetric: claim.md + code + data only, no session history)

**Verdict: `CONFIRMED-REAL`.** Skeptic agent (isolated context) reviewed the claim, code, `.bnet`
source, and tests. Lacking Bash access, it hand-verified both boundary states (`k=4` and `k=5`)
against all 35 `.bnet` rules — confirming both are genuine fixed points of the fully unclamped
wild-type rules, not residual-clamp artifacts — and adversarially tested the monotonicity-detection
logic in `run.py` against 5 different non-monotone shapes (flapping patterns, late relapse), all
correctly rejected. It recommended (without being able to run it) a cheap bit-for-bit re-execution
check and a full per-step trace of the k=4/k=5 boundary to identify the actual mechanism. Both were
then run by the main session:

| Check | Result |
|---|---|
| `k=4`/`k=5` boundary states are genuine fixed points of the fully unclamped rules (hand-verified against all 35 rules) | ✅ both confirmed |
| Monotonicity-detection logic correctly rejects 5 adversarial non-monotone patterns | ✅ all 5 correctly rejected |
| Bit-for-bit determinism (fresh `cmd_run()` called twice) | ✅ `r1 == r2: True` |
| **Full per-step trace of `k=4` vs `k=5`** (the mechanistic check the skeptic could not execute) | ✅ run — reveals the exact one-step race condition described above |

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The relapse/escape pattern is a clean, single monotone threshold, not a fuzzy or non-monotone
  region — the pre-registered CONFIRMED condition is met exactly.
- [x] The threshold has a complete mechanistic explanation, not just an empirical correlation: it is
  a one-synchronous-step race between the clamp's release and `CyclinE1`'s self-sustaining activation.

### What Was NOT Confirmed
- [x] Whether this exact threshold (`k*=5`) or its race-condition mechanism generalizes to other
  clamp pairs, branches, or starting states remains untested.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| This one branch, this one clamp pair, this one starting state | Test the same duration sweep starting from the "second" `Growth_arrest` fixed point `H-B7-9`/`H-B7-10` identified, to check whether `k*=5` is specific to `GROWTH_ARREST_STATE` or a property of the mechanism generally | Cheap — reuses `simulate_transient_clamp_multi` unchanged with a different starting state |
| This one branch | Test the same clamp pair's transient threshold on one of the other 7 multistable branches | Tests generality beyond this one branch |

## What This Does NOT Mean

1. Does NOT mean `k*=5` is a universal constant of this network — it is specific to this exact clamp
   pair, branch, and starting state (`GROWTH_ARREST_STATE`).
2. Does NOT establish a real-time duration — "5 synchronous steps" has no direct physical time unit
   in this discrete Boolean abstraction.
3. Does NOT test robustness to noise or asynchronous update — this is a synchronous, noiseless,
   fully deterministic result; a stochastic or asynchronous version of this network could show a
   probabilistic rather than sharp threshold.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified, `pyboolnet`-cross-checked mechanism
(inherited from `H-B7-4`/`H-B7-9`).

## Pearl Card Update

**New information:** the exact threshold (`k*=5`) has a complete, traced mechanistic explanation — a
one-synchronous-step race condition between the clamp's release timing and the `CyclinE1` positive
feedback loop's own completion time. This is a rare case in this bridge where an empirical duration
threshold is not just measured but FULLY EXPLAINED down to the exact synchronous-update step at which
the outcome is decided — a template for how to investigate any future duration-threshold finding in
this or related Boolean-network experiments (trace the watched nodes step-by-step across the boundary,
don't stop at reporting the number).
