# H-B7-17 — decision.md

## Result

**Substrate check passed:** the clamp-phase orbit is identical (12 states: 2 branches × k=1..6)
across all 5 conditions (baseline + 4 perturbations), exactly as the Compute-First Check
predicted (`RBL2` is forced to a constant during the clamp regardless of its own rule) —
`substrate_check_orbit_unchanged_across_all_conditions: true`.

**Baseline reproduces H-B7-15 exactly:** M1 sufficient at `j=1` (0 collisions), 1 collision at
`j=0` — the same numbers already committed in H-B7-15's own `metrics/run.json`.

**A real finding, not a bug, changed the analysis mid-experiment.** The first pass classified
perturbations only by whether M1 reached 0 collisions at `j=1`, giving a naive "3 of 4 robust, 1
of 4 fragile." An independently-invoked reviewer, checking the headline baseline-vs-fragile
numbers, flagged a discrepancy in a number quoted in the review PROMPT (my own transcription
error, not a code bug — the committed `metrics/run.json` already agreed with the reviewer). But
investigating that discrepancy surfaced something real: **`flip_TF_drop_CyclinE1`'s `floor`
marker (the branch-constant `DNA_damage` alone) ALSO showed 0 collisions — meaning no `k`-
dependent fate transition exists AT ALL under this perturbation.** Direct verification
(`diag_h17_flip_tf_investigate.py`, scratchpad): under `RBL2 := !CyclinD1` (dropping the
`CyclinE1` dependency), EVERY `k=1..6` on BOTH branches relapses to `GROWTH_ARREST` — the
transient escape mechanism itself is abolished, not merely made unobservable-vs-observable.

**Corrected classification (FL Step 4a Floor-Ceiling discipline, applied per perturbation):** a
perturbation whose own floor marker shows 0 collisions has NO underlying transition — M1 looking
"sufficient" there is vacuous (nothing to fail at distinguishing), not evidence of robustness.
`cmd_run()` was fixed to classify using floor's own transition-exists signal:

| Perturbation | Transition exists? (floor) | M1 sufficient at j=1? | Classification |
|---|---|---|---|
| `flip_FF_constant_false` (RBL2 permanently False) | Yes | No | **FRAGILE** |
| `flip_FT_drop_CyclinD1` (RBL2 := `!CyclinE1`) | Yes | Yes | **ROBUST** |
| `flip_TF_drop_CyclinE1` (RBL2 := `!CyclinD1`) | **No** | (vacuously Yes) | **CRITERION_INVALID** — not evidence either way |
| `flip_TT_xnor` (RBL2 := XNOR) | Yes | Yes | **ROBUST** |

**The one genuinely fragile case is mechanistically exactly the sensible one.**
`flip_FF_constant_false` is the perturbation that makes `RBL2` permanently `False` — i.e. it
removes the ONE truth-table row (`CyclinE1=False, CyclinD1=False → RBL2=True`) that let `RBL2`
ever re-establish itself post-release. This is precisely the signal H-B7-13's own original
diagnosis pointed to as the "CyclinE1/RBL2 feedback loop" providing the one-step-delayed
legibility. Removing `RBL2`'s ability to ever turn back on removes exactly that signal — the
mechanism breaks in the one way the arc's own prior mechanistic story would predict, not
arbitrarily.

## Verdict

**PARTIALLY-ROBUST**, using the CORRECTED (floor-validated) classification: 2 of 3 meaningfully-
testable perturbations (`flip_FT_drop_CyclinD1`, `flip_TT_xnor`) preserve `j*=1` sufficiency; 1 of
3 (`flip_FF_constant_false`) breaks it, mechanistically exactly where the arc's own prior
diagnosis would predict; 1 of 4 total perturbations (`flip_TF_drop_CyclinE1`) is uninformative —
it abolishes the phenomenon under study rather than testing observability of it, and is excluded
from the robust/fragile count rather than being miscounted as "robust."

**Sharpest defensible statement:**

> Within this Boolean model, `j*=1` sufficiency of `{Growth_arrest, Proliferation}` is robust to
> 2 of 3 meaningfully-testable single-bit truth-table perturbations of `RBL2`'s own rule — it
> breaks specifically when the perturbation removes `RBL2`'s ability to re-establish itself
> (`True`) post-release, consistent with this arc's own mechanistic account of WHY `j=1`
> resolves what `j=0` cannot. A fourth perturbation abolishes the underlying transient-escape
> phenomenon entirely and is not informative about observability robustness either way.

## FL Step 8a — Independent Reviewer

Narrowly-scoped, context-asymmetric reviewer pass on the core baseline-vs-`flip_FF` asymmetry
(the load-bearing numeric claim): **`[CONFIRMED-REAL]`** — independently reconstructed
`wild_type_rules` for both conditions from scratch, re-ran the k=1..6/2-branch domain, and
reproduced the exact numbers (baseline: 1→0 collisions `j0→j1`; `flip_FF`: 1→1, still failing at
`j1`), including the specific colliding `(branch, k)` group.

**The reviewer's spot-check of `flip_TF_drop_CyclinE1` surfaced the real finding above** — its
independently-computed `j0` collision count (0) did not match a number in my review prompt (which
claimed 1). Checking the committed data showed the reviewer was right and my prompt had a
transcription error — but chasing down WHY floor also showed 0 collisions (not expected for a
"1 collision" claim) is what led directly to discovering the abolished-transition finding.
**A skeptic-invoked discrepancy check caught a real, more important error than the one it was
sent to check** — worth recording as its own small methodology lesson (LEDGER).

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the naive "M1 sufficiency at j=1" criterion applied uniformly across all 4
perturbations without checking whether each perturbation still has a real transition to detect —
this would have silently misclassified `flip_TF_drop_CyclinE1` as "robust" when it is actually
uninformative.

**What was NOT killed:** the corrected finding — 2/3 meaningfully-tested perturbations ARE
genuinely robust, 1/3 IS genuinely fragile in a mechanistically sensible way. The underlying
`j*=1` mechanism from H-B7-13/14/15 is real and does show real (if partial) structural robustness
to rule-level perturbation, distinct from — and now more carefully characterized than — a naive
count would have shown.

**Relaxation Map:**
- **Remove** the single-node (`RBL2`-only) restriction: test perturbations of `CyclinE1`'s own
  rule (the OTHER half of the named feedback loop, a larger 32-row truth table — not exhaustively
  testable this cheaply, would need sampling) or `p21CIP`'s rule (the other clamped node).
- **Weaken** "exhaustive single-bit flips only": a small random sample of MULTI-bit perturbations
  (flipping 2+ rows at once) was not attempted — the exhaustive scope here was deliberately
  limited to `RBL2`'s small 4-row table.
- **Replace:** combine rule perturbation with asynchronous update (H-B7-16) — the two robustness
  axes tested separately so far, never together — a genuinely new, more expensive follow-up.

## Revival Condition

Not applicable (not a REJECT). Forward-looking: the `CRITERION_INVALID` perturbation
(`flip_TF_drop_CyclinE1`) is itself worth a SEPARATE follow-up question in its own right — WHY
does dropping `CyclinE1`'s input from `RBL2`'s rule abolish the escape entirely, rather than just
shift the threshold? A real, mechanistically interesting question this experiment surfaced but
did not answer (out of scope for this cheap first test).

## Skeptic Concerns (self-review + independent reviewer, combined)

- "4 perturbations of ONE small rule is a narrow robustness test" → **Accepted limitation,
  explicitly named in claim.md** — this tests only whether `j*=1` is fragile to THIS rule's exact
  form, not general structural robustness of the whole network.
- "Could the floor-based CRITERION_INVALID check itself be wrong (e.g. floor's own collision
  logic buggy)?" → **Checked**: the floor result was independently corroborated by a direct,
  separate diagnostic script printing every `(branch, k)` fate under `flip_TF_drop_CyclinE1` —
  all 12 entries show `GROWTH_ARREST`, confirmed by inspection, not inferred from the collision
  count alone.
- "Was the reviewer's flagged discrepancy actually resolved, or just reframed?" → **Resolved**:
  the specific NUMBER discrepancy (my prompt said 1, both the code and the reviewer agree on 0)
  was a prompt-writing error on my part, now corrected in this document; the SUBSTANTIVE finding
  it led to (abolished transition) is independently verified via the diagnostic script, not
  merely asserted.

## Scope note

Second half of the user's named "option 2" (2026-09-10) — H-B7-16 tested update-schedule
robustness (asynchronous), this tests update-rule robustness (structural perturbation). Both are
now closed for this arc's cheap-first-test budget; combining them, or extending to other rules,
are named but unattempted follow-ups.
