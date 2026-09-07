# Lesson: why self-review found 0/7 and an adversarial skeptic pass found 7/7

**Date:** 2026-09-07. **Trigger:** user, reviewing the session log, pointed out that the correct
reading of "skeptic caught 7/7" is not "the skeptic is great, run it more" but "the generation
process produced 7/7 false-confidence results before the skeptic ever ran" — and asked for the
common failure mechanism to be diagnosed before doing any more experiments.

**Status:** [VERIFIED] — every citation below is a direct grep/read of this session's own
`decision.md` files, not recollection. This analysis is itself subject to the same discipline it
describes: claims are grounded in file:line, not asserted from memory.

## The seven cases, what was missed, and why self-review didn't catch it

| # | Experiment | What the skeptic found | What self-review actually checked | What self-review never checked |
|---|---|---|---|---|
| 1 | H-B2-1l | `SEED=0` hard-coded in a 9-point "N-sweep" claimed as a second independent population — actually one deterministic curve | That the sweep ran, produced 9 numbers, and the correlation was computed correctly | Whether the 9 draws were *actually* statistically independent — never read the RNG seeding line itself |
| 2 | H-B2-1j | "Only `N_DIM` changes" was false — `[0.5] + linspace(-1,-50,49)` also changes the spectral range simultaneously | That the claimed changed variable (`N_DIM`) did change, and the pipeline ran end-to-end | Whether *other* variables also changed as a side effect of the one edit — no structural diff against the baseline was ever run |
| 3 | H-B2-1k | Kill criterion ("≥1 sign change in 9 points") is satisfied by pure noise with P≈0.999994 — the criterion has no discriminating power at all | That the criterion was met on the real data, and the number was computed correctly | Whether the criterion *could ever fail* — no floor/null check was run because the experiment's own claim.md called it "descriptive" and treated FL Step 4a as inapplicable |
| 4 | H-B2-1i | Tukey 1.5×IQR fence applied to a severely right-skewed (lognormal-like) distribution, mislabeling a typical value as "MODERATE" | That the 30 raw values were real, independent, and correctly measured | Whether the *labeling method's own assumptions* (near-symmetry) matched the actual shape of the data it was labeling |
| 5 | H-B2-1h | Same as #1: `np.random.default_rng(SEED)` re-seeded to the same constant on every call across a 10-point coupling sweep — all 10 points were one fixed random direction, scalar-dilated | That the sweep ran and R² for "exponential growth" was high | The RNG seeding, again — same blind spot as #1, five experiments apart, never connected until the skeptic pass |
| 6 | H-B3-1l | Classical-statistic selection used an oracle-informed rule ("closest to the known transition") for the positive case but "earliest of two" for negative controls — an asymmetric rule that manufactures part of the reported advantage | That the pipeline correctly computed crossing dates for AC1, variance, and Betti-1 on all 3 lakes | Whether the *same selection logic* was applied identically to the positive and negative branches of the code — the two branches were read separately, never diffed against each other |
| 7 | H-B3-1m | claim.md's central justification ("Pettitt targets step-change, not trend") is false — Pettitt has near-full power against monotone trend alone, independently verified twice (hand computation + third-party `pyhomogeneity`) | That the hand-rolled Pettitt implementation's positive/negative controls passed, and the floor rate was computed correctly | Whether the *English-language mechanism claim* used to justify the experiment's whole design was itself true — no direct test of "does Pettitt fire on trend alone" was ever run before relying on the opposite as a premise |

## The pattern, stated once

**Self-review in all 7 cases verified that the code ran and produced the number the narrative
expected. It did not verify that the STATISTICAL OR MECHANISTIC PREMISE the narrative rested on
was actually true.** Every miss is a variant of the same gap: a plausible-sounding claim about how
the data, the code, or a named statistical test *behaves* was accepted as a premise instead of
being treated as a claim requiring its own minimal, direct, computational check.

This is not "not enough review effort" — every one of these experiments had FL-compliant
`controls.md`/`claim.md` sections, positive and negative controls, and (per this session's own
discipline) 2-3 rounds of self-re-reading before being called done. The effort was real. It was
aimed at the wrong target: **end-to-end behavior of the pipeline**, not **the specific mechanistic
sentence used to justify why the pipeline should work**.

Concretely, the miss-pattern splits into three sub-shapes, not one:

- **RNG/independence claims** (#1, #5 — 2/7): "N points" or "an independent population" was never
  checked against the actual seeding code. Already captured as a cross-cutting lesson in this
  session's global memory (`skeptic-pass-caught-degenerate-sample.md`) before this analysis; this
  document folds it into the larger pattern rather than treating it as a separate lesson.
- **Hidden co-variation** (#2 — 1/7): a change was verified to include the intended variable, but
  not verified to EXCLUDE unintended ones. "One assumption changed" (Minimal Relaxation Rule) is a
  design intent that was never checked as a code-level invariant.
- **Unverified mechanistic sentences** (#3, #4, #6, #7 — 4/7, the majority): a natural-language
  claim about how a statistic, a criterion, or a selection rule *behaves* was used as load-bearing
  justification without ever being tested in isolation, on a minimal synthetic case built
  specifically to probe that one sentence. This is the largest and most general sub-pattern.

## Why existing FL machinery didn't catch this

The project's own Floor–Ceiling Interval (FL Step 4a) and positive/negative controls (FL Steps
3-4) are designed almost exactly for sub-pattern 3 — but they are scoped to the EXPERIMENT'S FINAL
OUTCOME (does the pipeline detect a known transition, does it fire on pure noise), not to the
INTERMEDIATE MECHANISTIC CLAIMS used to explain why the design should work. H-B3-1m had real,
passing positive/negative controls for the overall two-part rule — and still rested on a false
premise about what Pettitt's test specifically discriminates, because nothing in the control suite
tested that one sentence directly. The gap is structural, not a missed checklist item within the
existing gates.

## What this predicts, and how to check it

**Falsifiable prediction:** any FL `claim.md` containing a natural-language sentence of the shape
"X specifically detects/targets/requires Y, and therefore Z" (a mechanism claim used to justify a
design choice, as opposed to a description of what was measured) is at elevated risk of being
false as stated, UNLESS that sentence was itself the subject of a dedicated minimal test before
being relied on. This is checkable retroactively: grep past `claim.md` files in this project for
comparable justification sentences that were never independently tested, and see how many survive
a targeted check.

**Proposed practice going forward, this project only (not a global rule change — flagging for the
user to decide whether to promote it):** before writing the "Why This Experiment, Specifically"
section of any future `claim.md`, any sentence of the "X targets/discriminates/requires Y" shape
must be checked with a minimal synthetic counter-example (a 5-line script, not a new experiment)
BEFORE it is used as justification — the same discipline this session applied AFTER the fact to
H-B3-1m (`K=n²/4` on a pure monotone series, zero noise) should happen BEFORE the claim is written,
not after a skeptic catches it. This is cheap — the H-B3-1m check took under two minutes — and
would have caught #3, #4, #6, and #7 (4 of 7) at design time, before any compute was spent on the
full experiment.

## What this does NOT mean

1. Does NOT mean self-review is worthless — it correctly verified code-runs-and-computes-the-right-
   number in all 7 cases, which is itself necessary, just not sufficient.
2. Does NOT mean every future experiment needs a full skeptic pass at design time — the proposed
   fix (a 5-line synthetic check per mechanism sentence) is far cheaper than a skeptic pass and is
   scoped to exactly the failure mode found here.
3. Does NOT establish that 7/7 is the "true" miss rate of this project's self-review in general —
   this is a specific, flagged batch of 7 experiments the session already knew were unreviewed;
   it is not a random sample of all decisions.md in this project.
4. Does NOT mean the skeptic agent itself is now unnecessary — sub-pattern 1 and 2 (3/7) were NOT
   mechanism-sentence issues and would not have been caught by the proposed pre-write check; an
   adversarial second reader is still doing real, distinct work beyond what this fix would add.

## Pearl Registry cross-reference

Filed as a Caveat/Pearl Gate entry in `pearl_registry/INDEX.md` (this session, 2026-09-07) with
`impact_score=9` — this is a structural finding about the generation process itself, not about any
one experiment, and applies to every future `claim.md` in this project, not a narrow scope.
