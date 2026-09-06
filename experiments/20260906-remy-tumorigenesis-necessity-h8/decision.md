# decision.md — 20260906-remy-tumorigenesis-necessity-h8

**Graph node:** `H-B7-8` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-06/07

## Verdict

- [x] **CONFIRMED** — the double clamp `do(p21CIP=0, RBL2=0)`, with `RAS` and `TP53` left completely
  UNCLAMPED (evolving under their own wild-type rules), starting from `GROWTH_ARREST_STATE`, reaches
  the EXACT `Proliferation` attractor `H-B7-7` reached with all four nodes clamped. The unclamped
  `RAS` ends at `1` and unclamped `TP53` ends at `0` — the same values `H-B7-7` held them at by force.
- **This confirms the necessity claim from `H-B7-7`'s own FL Step 8a skeptic pass**: `RAS=1`/`TP53=0`
  were not load-bearing in that four-hit clamp — the minimal sufficient perturbation, relative to this
  starting fixed point, is the two-hit `do(p21CIP=0, RBL2=0)`.

**Statement:** *Removing only the two directly-clampable branches of the `Growth_arrest` OR gate
(`p21CIP`, `RBL2`) — without touching `RAS` or `TP53` at all — is SUFFICIENT to reach `Proliferation`
from `GROWTH_ARREST_STATE`, because `RAS` and `TP53` independently settle to the values `H-B7-7`
clamped them to, via the branch's own unbroken signaling loops, not because they were forced.*

## Evidence Summary

| Field | Value |
|---|---|
| `final_state_pyboolnet_order` | `00000100101001010011001000110010110` |
| `proliferation_state` (from `H-B7-4`, `pyboolnet`-verified) | `00000100101001010011001000110010110` |
| Match | **Byte-identical** |
| `growth_arrest_phenotype_node` / `proliferation_phenotype_node` | `False` / `True` |
| `final_ras_unclamped` | `True` (matches `H-B7-7`'s clamped value) |
| `final_tp53_unclamped` | `False` (matches `H-B7-7`'s clamped value) |
| `branch_inputs_preserved` | `True` |

## FL Step 8a — Skeptic Verdict (context-asymmetric: claim.md + code + data only, no session history)

**Verdict: `CONFIRMED-REAL`, with one documented interpretive caveat (not a falsification).** Skeptic
agent (isolated context, no `decision.md`/reasoning history) reviewed the claim, code, `.bnet` source,
and tests; lacking Bash access itself, it hand-decoded both state strings against the rule set and
wrote an executable verification script rather than a hand-wave. That script was then actually RUN
(by the main session, which has Bash), producing:

| Check | Result |
|---|---|
| `RAS=1`/`TP53=0` genuinely present in `GROWTH_ARREST_STATE` (decoded directly, not trusted from prose) | ✅ verified at indices 27/31 |
| `apply_combined_clamp({p21CIP:0, RBL2:0})` leaves `RAS`/`TP53`'s rule objects **identical by reference**, only `p21CIP`/`RBL2` replaced with constants | ✅ `RAS identical object: True`, `TP53 identical object: True` |
| Bit-identical reproducibility (fresh `cmd_run()` called twice, deleted cache first) | ✅ `run1 == run2: True` |
| **Independent reproduction via `pyboolnet.compute_attractors()`** on a from-scratch `.bnet` with ONLY `p21CIP`/`RBL2` forced and the 4 branch inputs frozen — `RAS`/`TP53` left with their ORIGINAL rules, zero reuse of this project's own simulation code | ✅ exactly **1** attractor, `RAS=1`, `TP53=0`, `Growth_arrest=0`, `Proliferation=1`, byte-identical to `PROLIFERATION_STATE` |
| Neither `RAS` nor `TP53`'s rule is a syntactic tautology of the 4 branch inputs alone | ✅ confirmed — both depend on other dynamic nodes (`GRB2`/`FGFR3`/`EGFR` for `RAS`; `MDM2`/`E2F1_*`/`CHEK1_2_*`/`ATM_medium` for `TP53`) |

**Documented caveat (Response Matrix: Accepted, not dismissed):** the skeptic traced WHY `RAS=1`/
`TP53=0` reliably hold on this branch, beyond "it happens to work": the branch's fixed inputs set up
**self-reinforcing signaling loops** —
`FGFR3_stimulus=1 → FGFR3=1 → RAS=1 → SPRY=1 ⊣ GRB2=0`, and `FGFR3=1 ⊣ EGFR=0` (both `EGFR`
disjuncts carry `!FGFR3`) — which keep `RAS=1` self-sustaining once established, and similarly
`DNA_damage=0` propagates to keep `TP53`'s first disjunct at 0. **This means the necessity finding is
closer to a structural corollary of the branch's own input configuration than a coincidental
dynamical fact** — real and correctly verified, but less surprising than "genuinely could have gone
either way." This does not change the verdict (the pre-registered kill criterion is met exactly), but
it corrects `claim.md`'s framing that a REJECTED outcome was equally plausible a priori — the skeptic's
trace shows the branch topology favored this outcome from the start.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The two-hit `do(p21CIP=0, RBL2=0)` is sufficient, relative to `GROWTH_ARREST_STATE`, to reach
  `Proliferation` — `H-B7-7`'s four-hit clamp was not minimal.
- [x] `RAS`/`TP53` do not merely "start" at the needed values — they DYNAMICALLY STAY there across the
  full trajectory without being forced, verified two independent ways (this project's own pipeline,
  run twice for determinism, AND a from-scratch `pyboolnet` reconstruction).

### What Was NOT Confirmed
- [x] That this necessity result was a priori uncertain — the skeptic's structural trace shows the
  branch's own signaling loops make `RAS=1`/`TP53=0` the expected outcome given the fixed branch
  inputs, softening (not eliminating) the experiment's novelty.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Permanent double clamp only | Transient `do(p21CIP=0, RBL2=0)` for a few steps, then released — tests whether the escape survives release, the sharper reading of Kauffman's strict claim (a real attractor of the UNPERTURBED-once-past-the-push network), echoing `H-B7-2`/`H-B7-3`'s permanent-vs-transient distinction | Highest-value remaining test in this bridge — has not been run for ANY confirmed escape yet |
| This one branch only | Check whether other multistable branches (7 more found in `H-B7-4`'s scoping) show the same `p21CIP`/`RBL2`-suffices-alone pattern | Cheap — reuses cached branch data, no new simulation infrastructure |

## What This Does NOT Mean

1. Does NOT mean `RAS`/`TP53` are irrelevant to this network's biology in general — only that, on
   THIS branch, starting from THIS fixed point, they were already at the needed values and stayed
   there without intervention; a different starting state or branch could behave differently.
2. Does NOT mean the result was a foregone conclusion with zero informational content — the skeptic
   explicitly confirmed neither node's rule is a tautology of the branch inputs; the self-reinforcing
   loop still had to be traced and independently verified, not merely assumed.
3. Does NOT test the TRANSIENT version of this same double clamp — named as the clear next step above.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified, `pyboolnet`-cross-checked mechanism.

## Pearl Card Update

**New information:** a necessity test, motivated directly by a prior skeptic pass's own WEAKENING
finding (not a fresh guess), confirmed cleanly at the highest verification tier used in this bridge —
and the SAME skeptic pass that confirmed it also traced WHY the result holds (self-reinforcing
signaling loops from the branch's fixed inputs), turning "the clamps were redundant" from an
observation into an explained mechanism. This is a second example (after `H-B7-6`) of a skeptic pass
adding explanatory depth rather than only a pass/fail stamp.
