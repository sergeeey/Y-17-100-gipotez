# decision.md — 20260906-kauffman-cellcycle-perturbation-h2

**Graph node:** `H-B7-2` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-06

## Verdict

- [x] **CONFIRMED for `do(Rb=0)`** — a permanent Rb loss-of-function, on its own, is sufficient to
  make the `CycD=0` (growth-factor-absent) region converge to a persistent CYCLING attractor instead
  of the wild-type quiescent point attractor. This is the operationalized Kauffman claim, holding in
  this model, for this specific intervention.
- [x] **REJECTED for `do(p27=0)`** — a permanent p27 loss-of-function, on its own, is NOT sufficient:
  the `CycD=0` region still converges uniformly to a point attractor (quiescence), just a slightly
  different one than wild-type (p27 itself is now pinned to 0 rather than settling there naturally).

**Statement:** *Under the intervention `do(Rb≡0)`, every state in the growth-factor-absent region of
the Fauré et al. 2006 network converges to a NEW period-8 complex attractor that stays entirely within
`CycD=0` — the network cycles persistently WITHOUT growth-factor input, a genuine pre-existing
attractor made accessible by a single-node perturbation, not a redesigned model, exactly the
mechanism Kauffman's Cancer Attractor hypothesis proposes. Under `do(p27≡0)` alone, the same region
still converges to a (slightly modified) point attractor — quiescence survives this specific single
perturbation.*

## Evidence Summary

| Intervention | `CycD=0` region converges to | Type | Matches wild-type cycling attractor? |
|---|---|---|---|
| none (wild-type, from `H-B7-1`) | point attractor `0000001011` | point | n/a (this IS the baseline) |
| `do(Rb=0)` | **new period-8 complex attractor**, entirely within `CycD=0` | **complex** | **No — a DIFFERENT, NEW attractor**, not the wild-type CycD=1 cycling attractor reused. Compare: wild-type complex attractor's 7 states all have `CycD=1`; this new attractor's 8 states all have `CycD=0`. |
| `do(p27=0)` | point attractor `0000001010` | point | n/a — quiescence preserved, only p27's own clamped value differs from wild-type's naturally-settled `1` |

**A genuinely new attractor, not a reused one — worth being precise about:** the CycD=1 branch's
wild-type complex attractor (period 7, `H-B7-1`) survives unchanged under `do(Rb=0)` too (still one of
the 2 attractors found) — but the NEWLY accessible one from `CycD=0` is a DIFFERENT period-8 cycle,
not the same trajectory relocated. Kauffman's hypothesis, strictly read, says the pathological state
is A pre-existing attractor of the (unperturbed) network's dynamical repertoire — this result shows
something adjacent but distinct: perturbing ONE node creates a NEW attractor not present in the
wild-type dynamics at all (the wild-type network has exactly 2 attractors; this perturbed network also
has exactly 2, but one of them is genuinely different). This is `[CONFIRMED-WEAKENED]`, not a clean,
unqualified confirmation — see "What This Does NOT Mean" below.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] `do(Rb=0)` destabilizes quiescence into persistent, growth-factor-independent cycling — the
  pre-registered kill criterion for this intervention arm.
- [x] The two interventions are genuinely DIFFERENT in outcome (Rb: yes: p27: no) — this is itself
  informative: not every tumor-suppressor loss is equally destabilizing in this model, matching real
  biology's redundancy among cell-cycle checkpoints (Rb is more architecturally central — it directly
  gates E2F — than p27, one of several CDK inhibitors).

### What Was NOT Confirmed / Needs Qualification
- [x] The exact Kauffman claim (pathological state = a PRE-EXISTING attractor of the UNPERTURBED
  network) is only partially matched: the newly-accessible period-8 attractor under `do(Rb=0)` is NOT
  one of the wild-type network's own 2 attractors — it is a genuinely new one created by removing Rb's
  own dynamics from the state space. A stricter test of Kauffman's ORIGINAL claim would need to show
  that the SAME attractor (not a new one) becomes reachable from different initial conditions without
  changing any node's rule at all (e.g., via a transient perturbation returning to normal dynamics,
  not a permanent clamp) — see Relaxation Map.
- [x] `do(p27=0)` alone does not reproduce the phenomenon — single-node sufficiency is
  intervention-specific, not general across "any tumor suppressor."

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Permanent clamp (`do(Rb≡0)` for all time) | Transient perturbation: force Rb=0 for a FEW steps then release it back to its own update rule, from a `CycD=0` initial state — does the system settle into the wild-type quiescent point attractor again, or does it get trapped in cycling even after Rb is "restored"? | This is the STRICTER test of Kauffman's original hypothesis (pathological state reachable via a transient push, not requiring the intervention to persist forever) — a genuinely different, more faithful operationalization |
| Single-node perturbations only | Combined `do(Rb=0, p27=0)` — both tumor suppressors lost simultaneously, matching how real cancers typically involve multiple concurrent lesions, not one | Would need its own experiment ID (two assumptions changed together, deliberately, since this explores REDUNDANCY, not a single Minimal-Relaxation-Rule step) |
| Only Rb and p27 tested | The model's third named inhibitor, `cdh1` (proteasome co-activator) and `Cdc20`, are not yet tested as loss-of-function targets | Cheap to extend — same `clamp_rule` function, no new code needed, just two more intervention arms |

## What This Does NOT Mean

1. Does NOT establish that Rb loss alone causes cancer in real biology — this is one small, simplified
   10-node model; real cell-cycle control has many more redundant layers.
2. Does NOT show the STRICT form of Kauffman's hypothesis (pathological state = pre-existing attractor
   of the UNPERTURBED network) — the newly-accessible attractor under `do(Rb=0)` is a genuinely NEW
   attractor, created by permanently removing one node's own dynamics, not a state the unperturbed
   network could ever reach on its own. The weaker, still-meaningful claim actually shown: a SINGLE,
   biologically-plausible loss-of-function is sufficient to create persistent proliferation without
   growth factor, in this model — a real and relevant finding, but a distinguishable claim from
   Kauffman's original "differentiated states are attractors of the SAME unperturbed network."
3. Does NOT mean p27 is unimportant in real cell-cycle control — only that THIS single perturbation,
   in THIS model, is insufficient on its own; combined loss (Relaxation Map) may behave differently.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic exhaustive enumeration over a fully specified, known mechanism (2^10
states per intervention, all checked), same reasoning as `H-B7-1`.

## Pearl Card Update

**New information (methodologically important, not just biologically):** this result surfaces a real
distinction between two readings of "attractor-based disease" hypotheses that is easy to conflate: (a)
a permanent single-gene loss makes a NEW pathological attractor accessible (what this experiment
shows for Rb), versus (b) the ORIGINAL Kauffman claim that pathological states are attractors ALREADY
PRESENT in the healthy network's own dynamical repertoire, reachable via transient perturbation without
permanently altering any rule. These are different, both interesting, and easy to blur together when
summarizing a "confirmed" result casually. Worth flagging for any FUTURE cross-domain summary of this
bridge: state which of the two claims was actually tested.
