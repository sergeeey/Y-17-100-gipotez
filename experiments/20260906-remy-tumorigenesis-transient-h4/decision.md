# decision.md — 20260906-remy-tumorigenesis-transient-h4

**Graph node:** `H-B7-4` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Date:** 2026-09-06

## Verdict

- [x] **REJECTED (for `do(RAS=1)` specifically)** — all 4 tested transient-clamp durations (1, 3, 10,
  30 steps) return to the original `Growth_arrest` fixed point once released. None reach
  `Proliferation` or any other attractor.
- **This is a genuine, informative negative result, NOT a `TASK_INFEASIBLE` finding like `H-B7-3`.**
  Unlike the Fauré network, this branch DOES have the required multi-attractor structure (verified via
  `pyboolnet` before designing this experiment) — the test COULD have succeeded. It didn't, for this
  specific single-node perturbation.

**Statement:** *In the Remy et al. 2015 bladder tumorigenesis network's `(DNA_damage=0,
EGFR_stimulus=0, FGFR3_stimulus=1, Growth_inhibitors=1)` branch — which genuinely contains both a
`Growth_arrest` and a `Proliferation` attractor under identical external signaling — a transient
activation of `RAS` alone (1 to 30 synchronous steps, then released) is NOT sufficient to move the
system from the `Growth_arrest` basin into the `Proliferation` basin. The system returns to
`Growth_arrest` every time.*

## Evidence Summary

| Case | k (steps) | Final attractor | Branch inputs preserved? |
|---|---|---|---|
| clamp RAS=1 | 1 | `Growth_arrest` (original) | ✅ |
| clamp RAS=1 | 3 | `Growth_arrest` (original) | ✅ |
| clamp RAS=1 | 10 | `Growth_arrest` (original) | ✅ |
| clamp RAS=1 | 30 | `Growth_arrest` (original) | ✅ |

`any_case_flipped_to_proliferation: false`. The sanity check (`branch_inputs_preserved`) confirms the
4 branch-defining input nodes never drifted during any simulation — a real risk given the more complex
35-node network, checked explicitly rather than assumed.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The pipeline correctly executes a transient clamp-then-release simulation on a real 35-node
  network, cross-checked against `pyboolnet`'s independently-computed ground truth (both the
  `Growth_arrest` and `Proliferation` states verified as genuine fixed points under this project's own
  `synchronous_step`, in `tests/test_remy_tumorigenesis_transient.py`, BEFORE trusting this result).
- [x] A single-node transient perturbation of `RAS` alone, however long sustained (up to 30 steps,
  well beyond the network's own settling time), is insufficient to cross this particular basin
  boundary in this model.

### What Was NOT Confirmed
- [x] Kauffman's strict hypothesis was NOT confirmed by this specific test — but critically, this
  time the negative result is INFORMATIVE (the structural precondition for a positive result existed),
  unlike `H-B7-3` where a negative result was logically guaranteed regardless of the hypothesis's truth.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Perturbation target = `RAS` alone | Try `TP53` (transient inactivation, `do(TP53=0)`) or `RB1` (transient inactivation) — both plausible single-hit tumor-suppressor losses named in the model's own inhibitor set | Named explicitly in `claim.md`'s "What This Does NOT Mean" #2; each needs its own experiment ID per Minimal Relaxation Rule |
| Single-node perturbation only | Combined `do(RAS=1, TP53=0)` — a genuine two-hit perturbation, matching multi-hit carcinogenesis theory (a real, well-established idea in cancer biology: single oncogene activation is typically insufficient, cooperating lesions are usually required) | Two assumptions changed together deliberately (exploring cooperativity, not incrementally) — would need its own experiment, framed explicitly as a 2-hit test, not a Minimal-Relaxation-Rule single step |
| Starting point = the `Growth_arrest` fixed point only | Try starting from intermediate/transient states already partway through a natural trajectory, not only the settled attractor | Lower priority — the settled attractor is the most natural, best-motivated starting point for a "kick a stable cell" thought experiment |

## What This Does NOT Mean

1. Does NOT mean Kauffman's Cancer Attractor hypothesis is false in this model — only that this ONE
   perturbation target, tested alone, is insufficient. The bistable structure itself (verified via
   `pyboolnet`) remains real and available for other perturbations to test.
2. Does NOT mean `RAS` activation is biologically irrelevant to bladder cancer — only that, IN THIS
   SIMPLIFIED MODEL, activating it alone (without also disabling a countervailing tumor suppressor)
   does not overcome the network's own restoring dynamics back to `Growth_arrest`. This is actually
   CONSISTENT with, not contradictory to, the well-established multi-hit model of carcinogenesis:
   single oncogene activation is textbook-insufficient for transformation in most contexts.
3. Does NOT test whether a LONGER clamp (beyond 30 steps) would eventually flip the outcome — 30 steps
   is well beyond this network's natural settling time in every other experiment in this bridge, making
   an even longer clamp implausible as the missing ingredient, but not formally ruled out here.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable — deterministic simulation on a fully specified, `pyboolnet`-cross-checked mechanism.

## Pearl Card Update

**New information:** the FIRST genuinely capable test of Kauffman's strict hypothesis in this bridge
(structural precondition verified present, unlike `H-B7-3`) gives a clean, biologically-coherent
negative result for a single-hit perturbation — consistent with multi-hit carcinogenesis theory rather
than contradicting it. This reframes the bridge's open question productively: not "can ANY transient
perturbation reveal a pre-existing pathological attractor" (too broad, unfalsifiable in practice) but
"does a biologically-realistic COMBINATION of perturbations do so, matching how real tumorigenesis is
understood to require multiple cooperating lesions." The next experiment (combined `RAS`+`TP53` or
similar) is the natural, well-motivated test of that sharper question.
