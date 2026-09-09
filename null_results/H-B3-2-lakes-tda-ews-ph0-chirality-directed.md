# H-B3-2 — decision.md

## Result

### Mechanism Claim Gate — confirmed exactly, not merely asserted (unaffected by the bug below)

5/5 independent trials (`diag_time_reversal_h1.py`, random windows with trend, matching real-
series character): the arc's own H1-VR-on-Takens-embedding diagram is **byte-identical**
between a window and its time-reversal, both in shape and in sorted values. The user's
claimed mechanism (a Vietoris-Rips complex on an embedded point cloud depends only on the
pairwise-distance multiset, which time-reversal permutes but does not change) holds exactly
on the actual code Bridge 3 used, not just in the abstract. **HOLDS.** This part of the
experiment is independent of `merge_tree_bars` and is not affected by the bug documented below.

### A real implementation bug was found by an independently-invoked reviewer, fixed, and the
### experiment re-run — the primary finding did NOT survive

**What happened, in order:**

1. The first implementation of `merge_tree_bars` (0-dim persistence via recursive stem-pruning,
   Baryshnikov 2022 Section 2.2.1) used an ad hoc iterative heuristic — repeatedly pair the two
   INDEX-ADJACENT extrema with the smallest value-difference, working inward from small
   persistence, deferring the largest/global pair to last. This passed 6/6 hand-verified tests
   (monotone increasing/decreasing, a 4-point W-shape) and produced a clean CONFIRMED result
   (below, § "Superseded result").

2. Per this session's stated methodology (apply the same rigor to every task, run an
   independently-invoked reviewer on high-stakes findings before trusting them — FL Step 8a), a
   narrowly-scoped `Agent(reviewer)` was invoked with exactly two checkable claims: (a) is
   `merge_tree_bars` correct, and (b) is the 2.25-year lead-time/calendar-date claim correct.
   Check (b) **passed** — independently reproduced exactly. Check (a) **failed**: the reviewer
   hand-constructed a 7-point counter-example, `w = [2, 8, 0, 9, 1, 7, 3]` (all 7 points are
   extrema — odd count), hand-traced the buggy algorithm, and confirmed by running the live code
   that it silently DROPS the window's global minimum (value 0.0 at index 2) whenever the total
   extrema count is odd. Measured directly on the real Lower Zurich data: **45 of 82 rolling
   windows (~55%)** have an odd extrema count and are affected.

3. `merge_tree_bars` was re-implemented directly per the paper's own definition (Section 2.2.1):
   find the GLOBAL min and GLOBAL max of the current point set, pair them first as the outermost
   "stem" bar, remove both, recurse independently on each remaining contiguous run. Hand-traced
   against the reviewer's counter-example: the global minimum (index 2) is now correctly paired
   as the very FIRST bar (`(2, 3, 0.0, 9.0)`) — confirmed both by hand-tracing and by running the
   fixed code (`run.py::_recursive_pairing`). The odd-extrema-count case still leaves one point
   per affected recursive branch explicitly unmatched (`merge_tree_bars_full` returns it), rather
   than silently dropping it — this is an honest, visible handling of the boundary case the
   paper's own Section 2.4.1 flags (its clean procedure assumes global min at the left end / max
   at the right end; other conventions need an explicit "stitching" transformation "at the cost
   of at most one (long) bar").

4. The masking test (`test_merge_tree_bars_count_matches_extrema_pairing_invariant`, which
   compared `len(bars)` to `total_points // 2` — floor division that silently absorbs a dropped
   point) was replaced with an exact-accounting test
   (`test_merge_tree_bars_full_accounts_for_every_point_exactly`) plus a dedicated regression
   test using the reviewer's exact counter-example
   (`test_reviewer_counter_example_odd_extrema_includes_global_min`). All 7 tests pass, including
   the original 4 hand-verified cases (one, the W-shape case, had its EXPECTED BAR ORDER
   corrected — the true recursive algorithm extracts the global min/max pair FIRST, not last, so
   the two bars in `[0,3,1,4]` come out in the opposite order from the old buggy implementation,
   though `chirality_excess` itself is unchanged at 0.0 for that specific case).

5. **The full experiment (`cmd_run()`) was re-run under the corrected statistic.** The result
   changed materially — see below.

### Primary finding under the CORRECTED statistic — the clean pattern collapses

| lake | role | chirality V1-crossing (buggy, superseded) | chirality V1-crossing (corrected) |
|---|---|---|---|
| lower_zurich | positive (transition 2002.0) | index 18 | index **13** (fires earlier) |
| windermere | negative | never | index **7** (**new false alarm**) |
| loch_leven | negative | never | never |

Floor false-positive rate for chirality-excess also **inverted**: 26.7–36.7% under the buggy
statistic (the LOWEST of the three, cited as a secondary finding) → **53.3–63.3%** under the
corrected statistic (now the **HIGHEST** of the three, worse than trend_slope on 2 of 3 lakes).

**The corrected chirality-excess statistic fires a false alarm on Windermere, the same failure
mode both baselines already showed on their own negative controls.** The property that made
this result CONFIRMED — "chirality-excess is the ONLY one of the three statistics correctly
silent on BOTH negative controls while firing on the real transition" — is false under the
corrected, verified-correct implementation. It was true only of the buggy version.

### What the bug was actually doing, mechanistically (why the buggy version looked clean)

Not fully characterized (would require a dedicated follow-up, not done here), but the direction
is clear from the data: the buggy algorithm systematically dropped points working from the
*smallest*-persistence pairs inward, which means whichever point survived unmatched tended to be
whatever was left after all the "noisy," small-persistence local wiggles had already been
consumed — i.e. the bug had an incidental smoothing/conservatism effect that suppressed exactly
the kind of small, high-frequency chirality flips that (correctly) drive false alarms in a
genuinely noisy negative-control series like Windermere. The corrected algorithm has no such
incidental damping, and the resulting statistic is noisier — and, on this dataset, noisier in a
way that erases the discriminating signal the buggy version appeared to show.

## Verdict

**REJECT.** The pre-registered CONFIRMED criterion in `claim.md` — chirality-excess V1-crossing
fires on the positive control while staying silent on both negative controls, with a lower floor
false-positive rate than both baselines — does **not** hold under the corrected, verified-correct
`merge_tree_bars` implementation. It held only under a buggy implementation that silently dropped
the global minimum on ~55% of real windows, an artifact discovered and fixed by an independently-
invoked reviewer per this session's own FL Step 8a discipline.

This is a direct, mechanical falsification via bug-fix-and-rerun, not a skeptic-argued weakening —
stronger grounds for REJECT than most entries in this repo's `null_results/`, which typically rest
on an argued concern rather than a demonstrated code defect with a controlled before/after
comparison on identical data.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the specific claim that PH₀ chirality-excess (Baryshnikov 2022, correctly
implemented) shows a clean, uniquely-discriminating early-warning pattern on the Lower
Zurich / Windermere / Loch Leven three-lake dataset, with a verified 2.25-year lead and correct
silence on both negative controls. This is now falsified — the corrected statistic fires a false
alarm on Windermere and has the worst floor false-positive rate of the three tested statistics.

**What was NOT killed:**
- The Mechanism Claim Gate result: Bridge 3's existing H1-VR-on-Takens-embedding statistic is
  genuinely, exactly blind to window time-reversal (5/5 trials, byte-identical diagrams). This is
  independent of `merge_tree_bars` and stands regardless of this experiment's outcome.
- `merge_tree_bars` itself, now correctly implemented per Baryshnikov 2022 Section 2.2.1 and
  covered by a regression test built from an adversarial counter-example, is a validated,
  reusable building block — the FAILURE is about this specific dataset/comparison, not about
  whether the statistic can be computed correctly.
- The general idea that a time-reversal-SENSITIVE statistic (of which chirality-excess is one
  example, correctly implemented) *could* add value over H1-VR is not disproven — only this
  specific test, on this specific 3-lake dataset, with this specific detection rule, failed to
  show it. A structurally different order-sensitive statistic, or a dataset with more than one
  positive-control transition, remains untested.

**Relaxation Map for surviving assumptions:**
- Remove: the specific claim that THIS statistic on THIS dataset shows the pattern — REJECTED,
  do not retry without a materially different statistic or dataset.
- Weaken: "chirality-excess adds value" → "chirality-excess, as one specific order-sensitive
  construction, does not add value on the one available positive-control lake dataset; other
  order-sensitive constructions or larger datasets are untested."
- Replace: a different 0-dim/order-sensitive TDA statistic (not stem-pruning chirality
  specifically) could still be tried against the same H1-VR-blindness gap this experiment's
  Mechanism Claim Gate established is real and unaddressed by the existing arc.

## Revival Condition

**Contingent, not theorem-level** — the kill rests on: (a) one specific statistic construction
(Baryshnikov chirality-excess via stem-pruning) (b) tested on one specific 3-lake dataset with
only one positive-control transition (c) using one specific detection rule (V1 AR(1)-surrogate
calibration). Revival requires relaxing at least one of these three, not a theorem-level
contradiction:

- **A genuinely different positive-control dataset** — e.g. the Peter/Paul lake dataset used in
  earlier H-B3-1 sub-experiments (doSat's independently-reported +13-month lead) — would let the
  n=1-positive-control limitation (already flagged as the single biggest caveat on the superseded
  CONFIRMED result) be addressed directly, and might show a different pattern for the corrected
  statistic than this one dataset did.
- **A different order-sensitive TDA construction** (not stem-pruning chirality specifically) that
  is less sensitive to the small, high-frequency wiggles this experiment's data suggests the
  corrected chirality-excess picks up as noise (see "What the bug was actually doing" above) —
  e.g. a chirality statistic computed on a smoothed/coarsened version of the series, or restricted
  to bars above a minimum persistence threshold, might recover discriminating power without
  reintroducing the original bug's ad hoc (and uncontrolled) smoothing effect.
- **No revival** on the exact claim as tested (this specific statistic, this specific dataset,
  this specific detection rule) — that combination is REJECTED and should not be retried
  unmodified.

## Skeptic Concerns (retained from the superseded CONFIRMED verdict, for the record — largely
mooted by the REJECT above, but kept so the audit trail is honest about what was already
flagged BEFORE the bug was found)

- "n=1 positive control -- could be a coincidence, not a real mechanism" → this concern is now
  moot in a different way: the result did not survive a controlled bug-fix comparison on the SAME
  n=1 data, which is strictly stronger evidence against the claim than "n=1 is a weak sample."
- "30 surrogate reps for a 95th-percentile null curve is a small sample" → unresolved, but no
  longer the operative concern given the REJECT above.
- Cross-lake RNG-seed-sharing concern (previously checked, dismissed) → reasoning still holds,
  irrelevant to the REJECT.
- "Baseline choices might not be the strongest possible baselines" → still an accepted
  limitation, orthogonal to why this REJECT occurred (the bug affected chirality-excess only, not
  the baselines).

## Process note — why this REJECT is evidence FOR this session's methodology, not against it

The original CONFIRMED verdict was explicitly marked WEAKENED (n=1) and, per FL Step 8a, sent to
an independently-invoked, narrowly-scoped `Agent(reviewer)` BEFORE being trusted further — not
after a complaint, not because something looked wrong, but as a matter of this session's standing
practice (applied identically to every other high-stakes finding this session: H-B2-3, H-CAT37-1,
H-CAT37-2). That reviewer pass is what caught the bug. Without it, this REJECT would not exist and
a false CONFIRMED verdict — resting on a statistic that silently dropped data on the majority of
real windows — would have been registered in `graph.yaml` as a positive result for Bridge 3's
15-hypothesis history. The reviewer's Check 2 (lead-time claim) passing independently, while Check
1 (statistic correctness) failed, is itself a demonstration of why narrow, checkable, two-claim
reviewer scoping works better than broad "review everything" prompts (an established pattern
this session, see prior LEDGER entries): a broad prompt might have accepted the passing lead-time
arithmetic as reassurance and never constructed the specific adversarial input needed to find the
real defect.

## Scope note

Route 3 of the user's 2026-09-09 direction-scoping report, executed after B2 (`начни B3`). Does
not reopen Bridge 3's own closed H1-VR arc (H-B3-1 through H-B3-1p) — chirality-excess is a
structurally different statistic family, tested here for the first time, and this experiment's
Mechanism Claim Gate result (H1-VR is exactly time-reversal-blind) stands independent of this
REJECT. This is Bridge 3's second REJECT-with-full-Kill-Analysis in its history (the first eight
sub-experiments of H-B3-1 through H-B3-1p were informative negatives of a different, earlier
kind) — and the first case in this session where a bug fix, not an argued skeptic concern, was
the direct falsifying mechanism.
