# H-B3-1p — decision.md

## FL Step 8a — mandatory reviewer

Scoped narrowly per the now-established pattern (4th consecutive success this session):
verify (1) the selection-rule change genuinely ignores `transition` for ALL lakes when
computing `classical_peak` (not just for negative controls), and (2) the consistency
check compares the correct stored field (`classical_peak_date_used`) from H-B3-1l's own
`metrics/run.json`. Completed successfully on the first attempt with a full, clean
verdict (no P0/P1/P2 findings, no blocking issues) — confirmed both: `transition` never
feeds into `classical_peak` selection (only into the separate diagnostic
distance-to-transition columns, guarded independently), and the consistency check reads
the correct field, verified by reading the actual stored JSON directly rather than
trusting the code's own comment. Ran `pytest` (6 passed, 3.47s) and `ruff` (clean) itself.

## Result

Recomputed Lower Zurich's classical-peak selection using the SAME "earliest of the two"
rule H-B3-1l already used for negative controls (Windermere, Loch Leven), removing the
transition-based oracle selection that was previously applied only to the positive case.

| | original (oracle-informed) | symmetric (this experiment) |
|---|---:|---:|
| classical_peak_date_used | 2004.667 (var, closest to 2002.0) | **1999.25 (AC1, earliest)** |
| tda_betti_peak_date | 2000.5 | 2000.5 (unchanged) |
| lead (TDA − classical, months) | +50.0 | **−15.0** |
| Verdict | `CONFIRMED` | **`REJECTED`** |

**Consistency check passed:** Windermere and Loch Leven's `classical_peak_date_used`
values under the symmetric rule match H-B3-1l's own stored values EXACTLY (they already
used this rule) — confirming the rule change is correctly scoped to the positive case
only, not silently altering anything else.

**Pearl's falsifiable prediction: CONFIRMED.** Exactly as pearl_registry (2026-09-07,
impact 7) predicted: under the honest, symmetric rule, `classical_peak_date_used` becomes
AC1's date (1999.25), TDA (2000.5) is now LATER than classical (not earlier/equal), and
the verdict inverts from `CONFIRMED` to `REJECTED`.

## Why this matters

H-B3-1l's own CONFIRMED verdict rested entirely on comparing TDA against variance
(2004.67) — a classical statistic that was selected SPECIFICALLY BECAUSE it happened to
sit closer to the documented transition (2002.0), i.e. using knowledge of the answer being
tested to pick which comparator to use. The SAME selection logic, applied honestly (no
oracle knowledge, same rule for positive and negative cases alike), picks AC1 instead —
and AC1 already precedes TDA by 15 months in the real data. There was never a version of
"classical vs TDA, compared fairly" where TDA led on Lower Zurich; the +50-month "TDA
leads" finding was an artifact of asymmetric statistic selection from the start.

## Kill Analysis

**What was killed:** H-B3-1l's specific CONFIRMED verdict on Lower Zurich ("TDA's peak
lands closer to the documented transition than classical's") -- under a fair, symmetric
selection rule (the SAME rule H-B3-1l itself already used for negative controls), the
claim inverts to REJECTED. The +50.0-month "TDA leads" number was never real under honest
methodology; it existed only because the classical comparator was picked with knowledge of
the answer being tested.

**What was NOT killed:**
- Peter doSat's own +13-month lead (V1/V1'/V1g/conjunction, 4x replicated) -- entirely
  independent of Lower Zurich's selection-rule problem, untouched by this correction.
- H-B3-1n's own AR(1)-surrogate floor-check machinery and its INCONCLUSIVE finding on the
  original (now-superseded) +50.0 lead value -- that experiment's own methodology and
  test suite remain valid records of what they tested, even though the target number they
  tested is now known to have been unfairly derived in the first place.
- The broader peak-tau (argmax) REPORTING approach as a method -- only ITS APPLICATION
  with an asymmetric selection rule on Lower Zurich specifically.

**Relaxation Map:** if peak-tau reporting is revisited for Lower Zurich in the future, the
symmetric "earliest of two" rule used in THIS experiment should be the default, not the
oracle-informed one -- no further variant of the selection rule is worth testing, since
the asymmetry itself (not a parameter within it) was the identified problem.

## What This Does NOT Mean

1. Does NOT retroactively invalidate H-B3-1n's own AR(1)-surrogate floor check — that
   experiment tested whether the ORIGINAL +50.0-month lead (as reported by H-B3-1l) could
   arise from noise, and found it genuinely ambiguous (90.4th percentile). This experiment
   answers an earlier, more basic question: was the +50.0 value itself fairly derived in
   the first place? It was not.
2. Does NOT affect Peter doSat's own separately-robust finding (the +13-month lead,
   replicated identically across V1/V1'/V1g/conjunction, unrelated to Lower Zurich's
   selection-rule asymmetry).
3. Does NOT mean peak-tau reporting as a METHOD is invalid in general — only that Lower
   Zurich's specific application of it, with its specific (asymmetric) selection rule, does
   not survive an honest recomputation.
4. Does NOT change any OTHER experiment's own verdict in this arc (H-B3-1c through 1o) —
   this is a targeted correction of H-B3-1l specifically.

## Go/No-Go

**REJECTED** (of H-B3-1l's original CONFIRMED claim, under a fair recomputation). This is
a decisive, not ambiguous, result — the pearl's own prediction was confirmed exactly, down
to the specific date (1999.25) and the sign of the lead (negative).

## Retroscan — H-B3-1l status correction required

Per this lab's own retroscan discipline (a new result bearing on a `grounds`-linked prior
node must revise that node in the same session): H-B3-1l's graph status, already downgraded
`confirmed` -> `lead` by H-B3-1n (AR(1)-surrogate floor, INCONCLUSIVE), should be further
downgraded to `killed` — the peak-tau claim's own selection methodology, when made honest,
directly REJECTS what H-B3-1l originally reported, independent of the floor question.

## Pearl Registry Update

Resolves the 2026-09-07 H-B3-1l "asymmetric classical_peak selection" pearl row (impact 7)
— done, prediction CONFIRMED exactly as specified. General methodological lesson recorded:
"pick whichever of several candidate statistics is closest to the known answer" is a form
of information leakage, applicable to any future multi-statistic comparison in this
project — this instance is now a concrete, worked example of that lesson causing an actual
verdict inversion when corrected, not just an abstract warning.
