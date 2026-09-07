# claim.md — 20260907-lakes-tda-ews-changepoint-v2

**Graph node:** `H-B3-1m` (bridge `B3-MAY-TDA`) · **Tier:** Standard
**Parent:** `H-B3-1b` (Relaxation Map Row 2: "Weaken: require the SAME rolling-window statistic
to ALSO show a level shift (not just trend) via a change-point test (e.g. Pettitt's test) before
declaring threshold-crossing." Last untested item of the original 3-row Relaxation Map — Row 1
[surrogate null] was run three times via `H-B3-1c/d/e`, REJECTED; Row 3 [peak-tau] was run via
`H-B3-1l`, CONFIRMED-with-confound.)

## EstimandOps L0 Gate

**Classification: PREDICTIVE** (same as `H-B3-1`/`H-B3-1b` — a detection rule tested against a
documented real transition and two no-transition negative controls; predicts whether a signal
"fires" at a given series, not a causal claim about ecosystem mechanism).

## Why This Experiment, Specifically

`H-B3-1`/`H-B3-1b`'s original rule (tau≥0.5 on an expanding-window Kendall tau) was
`CRITERION_INVALID`: an AR(1) null with NO real mechanism crosses the SAME threshold 80-83% of
the time. The rule detects *smooth monotone trend*, and red noise accumulates enough apparent
trend by chance at these series lengths to fire almost always. Pettitt's test targets a
DIFFERENT signal — a genuine *level shift* (step change in the mean) — which pure AR(1) red noise
should NOT reliably produce, even though it CAN produce spurious monotone trend. Requiring BOTH
conditions (trend AND level shift) is a natural, literature-standard way to sharpen a
trend-only detector's specificity, and it is the last of `H-B3-1b`'s three originally-named,
non-circular fixes.

## New Statistical Machinery — Built and Validated BEFORE Use (per project precedent)

Pettitt's test is NOT provided by any already-installed package in this repo (checked: no
`pymannkendall`, `ruptures`, or similar dependency present). Implemented from scratch in
`run.py` (`pettitt_test`), following the standard 1979 formulation and its widely-used
approximate p-value. Per this project's own established precedent — `H-B3-1c`'s `ar1_surrogate`
and `H-B3-1d`'s `iaaft_surrogate` were both independently correctness-tested BEFORE being trusted
in a real pipeline (see those experiments' own evidence markers) — this implementation is
validated the same way, in `tests/test_lakes_tda_ews_changepoint_v2.py`, BEFORE this claim.md's
own real run:
- **Positive control:** a series with an obvious single step change (constant + noise, mean
  jumps at the midpoint) — the test must locate the change-point near the true midpoint and
  report a very small p-value.
- **Negative control / calibration check:** many independent white-noise trials at a fixed
  nominal alpha — the observed false-positive rate must be in a sane range around the nominal
  level (loose bound, since the p-value formula is an approximation), not wildly miscalibrated.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The two-part "crossing" status (tau≥0.5 AND Pettitt p<0.05 on the raw statistic, evaluated causally — using only data up to the tau-crossing index) of each rolling statistic (AC1, variance, Betti-1 persistence entropy), on the SAME 3 lakes and pipeline as `H-B3-1`/`H-B3-1b` |
| **Falsifiable predicate** | The AR(1) floor false-positive rate under the two-part rule is meaningfully LOWER than the original rule's 80-83% (the specific mechanism this fix targets: red noise can fake a trend but not reliably a level shift) |
| **Measurable outcome** | New floor false-positive rate (30 AR(1) surrogates/lake, same construction as `H-B3-1`/`H-B3-1b`); IF the floor is no longer invalid, whether Lower Zurich two-part-crosses (TDA lead>0) while Windermere/Loch Leven do not |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md` / `pearl_registry/INDEX.md` / all `H-B3-1*` graph nodes: no
prior change-point / level-shift test in this project. `H-B3-1b`'s own Relaxation Map names this
exact idea as untested (Row 2). Confirmed genuinely novel, as the annotation-fix ADR-044 found.

## Kill Criterion (set BEFORE running) — Floor checked FIRST, per FL Step 4a discipline

**Step 1 — Floor (checked before interpreting anything else):**
- **STILL CRITERION_INVALID:** new floor false-positive rate ≥ 50% (still clearly at-floor,
  same failure mode as the original rule) — report as `CRITERION_INVALID`, NOT evidence against
  the underlying claim, per FL Step 4a's hard rule. Do not interpret real-lake results as
  confirmatory in this case.
- **FLOOR IMPROVED:** new floor false-positive rate < 50% — proceed to Step 2.

**Step 2 — Real-lake pattern (only interpreted if Step 1 passes):**
- **PROMOTE-worthy:** Lower Zurich two-part-crosses with TDA lead > 0, AND neither Windermere nor
  Loch Leven two-part-crosses on any statistic (0 false positives).
- **REJECT:** any negative control still two-part-crosses, or Lower Zurich does not show a
  positive TDA lead.

## What This Does NOT Mean

1. Does NOT retroactively validate or invalidate `H-B3-1`/`H-B3-1b`'s own `CRITERION_INVALID`
   verdict on the ORIGINAL rule — that verdict concerns a different (single-condition) rule.
2. Does NOT generalize to the 5-series population used in `H-B3-1g-k` — this experiment reuses
   the ORIGINAL 3-lake population, per the same explicit scope decision `H-B3-1l` made (Minimal
   Relaxation Rule).
3. A hand-implemented statistical test carries implementation risk regardless of unit tests —
   the positive/negative-control validation reduces but does not eliminate this risk. Any
   CONFIRMED-style result should be read alongside the validation tests' own pass/fail record.
4. Pettitt's test assumes a SINGLE change-point; if a series has multiple real shifts, the test's
   power and location estimate are not guaranteed reliable — not checked for these specific
   series.

## MCID

Whether the AR(1) floor false-positive rate drops below the original rule's 80-83% under the
two-part gate — reported as an exact number, not a threshold pass/fail on a separate metric.
