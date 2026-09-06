# case_study_notes.md — Loch Leven / Paul doSat focused read (H-B3-1h Relaxation Map, item 2)

**Date:** 2026-09-06
**Trigger:** `decision.md` § Relaxation Map — "A focused single-series case study on just these
two [Loch Leven, Paul doSat] (what does their raw data actually look like around the
false-crossing date?) — Cheapest possible next step — no new compute, just closer reading of
already-collected data."
**Script:** `case_study_loch_leven_paul_dosat.py` (read-only diagnostic, no new detection compute,
no new surrogate runs — reuses `tda_betti_crossing` values already committed in V1's
`metrics/run.json`).

## What was done

For each of Loch Leven and Paul doSat, loaded the raw scalar series (`pca1` for Loch Leven,
`doSat` for Paul) and inspected the ±10-point window around the series' own already-recorded
`tda_betti_crossing` time: local mean/std vs. whole-series mean/std, expressed as a z-shift and a
variance ratio (`local_var_ratio = local_std² / full_std²`).

## Finding 1 — both false positives cross during a local variance MINIMUM, not maximum

| Series | crossing time | local_var_ratio | local_mean_zshift |
|---|---|---|---|
| Loch Leven | 2002.33 | **0.259** | -0.258 |
| Paul doSat | 182.00 | **0.151** | -0.785 |

This is the opposite of the textbook critical-slowing-down signature (rising variance/AC1 before a
regime shift) — `[VERIFIED]` from the raw data, not a re-interpretation of an existing metric.
**Candidate hypothesis formed:** the TDA crossing detector is triggered by an artificially
"clean" (low-noise) Takens embedding during quiet periods, producing a spurious topological signal
unrelated to the approaching-transition mechanism the detector is meant to find.

## Finding 2 — the SAME signature appears in the one interpretable TRUE positive (falsifies Finding 1's mechanism as discriminating)

Added a contrast case not in the original Relaxation Map item: Peter doSat, the one series whose
TDA crossing has a real paired classical crossing (interpretable +13-day lead) and which has
survived every variant tried in this arc (V1/V1'/V2'/V1g/conjunction) — i.e. the strongest
positive evidence in the whole bridge.

| Series | role | crossing time | local_var_ratio | local_mean_zshift |
|---|---|---|---|---|
| Peter doSat (contrast) | **positive**, trusted lead | 172.00 | **0.297** | -0.863 |

Peter doSat's crossing sits in a local variance minimum of essentially the same magnitude (0.297
vs. 0.259/0.151) as the two false positives, with an even larger negative mean shift. **This
falsifies "local variance minimum at the crossing" as a mechanism that discriminates false
positives from the genuine signal** — per the Positive-Control Digitization discipline
(`artifact-provenance-gates.md` Gate 3: "a test that cannot distinguish your control from your
target is not a test"), a diagnostic that fires identically on the trusted positive is not
evidence about what makes Loch Leven/Paul doSat wrong.

## Verdict on this specific candidate mechanism

**KILLED** (not a claim revision to H-B3-1h itself — H-B3-1h's LEAD verdict and 2/5 conjunction
result stand unchanged; this only closes one specific explanatory hypothesis for *why* those 2/5
are false positives).

**What this narrows:** the local-variance-dip pattern at a `tau≥0.5` crossing is most likely a
generic property of the expanding-Kendall-tau threshold-crossing RULE itself (any series with a
locally quiet, low-scatter stretch will tend to produce a locally "cleaner" rolling statistic and
a coherent tau trend there, regardless of whether that stretch precedes a real transition) — not a
property specific to Loch Leven/Paul doSat's data. This is now `[HYPOTHESIS]`, not tested here.

**What remains unexplained:** why Loch Leven and Paul doSat, specifically, produce a TDA crossing
under every invariant/null-model combination tried, while Windermere/Peter pH/Paul pH never cross
under ANY method (`tda_betti_crossing=None` in V1 itself — not merely filtered out by the
conjunction), and Paul chl crosses under entropy alone (V1) but not under total persistence
(V1g), which is why the conjunction (`H-B3-1h`) correctly filters it out.
**Correction (2026-09-06, same session):** an earlier draft of this note incorrectly grouped Paul
chl with the never-crossing series (Windermere/Peter pH/Paul pH) — checked directly against V1's
committed `metrics/run.json`: `peterlake_Paul_chl.tda_betti_crossing = 185.0027...`, i.e. it DOES
cross under entropy. Fixed here per Hindsight Distortion Gap discipline (not silently rewritten —
this correction sentence stays). The local variance-dip pattern is necessary-looking (present at
every crossing checked, confirmed 6/6 in the population-wide follow-up below) but evidently not
sufficient to explain which negative-role series cross under which invariant.

## Follow-up (2026-09-06, same session) — pearl's own falsifiable_prediction tested

The pearl registry entry above named a specific, checkable prediction: does the local-variance-dip
pattern hold across ALL series that have a crossing, not just the 3 checked here? Ran
`all_series_variance_ratio_check.py` against all 6 series in the B3 population with a recorded
`tda_betti_crossing` (Windermere/Peter pH/Paul pH excluded — no crossing, no window to check).

**Result: 6/6 (100%) show var_ratio < 0.5** — positive role mean 0.375 (Lower Zurich, Peter chl,
Peter doSat), negative role mean 0.199 (Loch Leven, Paul chl, Paul doSat). **Prediction CONFIRMED**:
this is a structural property of the expanding-Kendall-tau crossing rule itself — it fires when a
series locally quiets down, independent of role or statistic family. Pearl registry entry status
updated to CONFIRMED; see `decision.md` Addendum 2 for the full writeup.

## Relaxation Map status update

The Relaxation Map row "A focused single-series case study on just these two ... Cheapest possible
next step" is now **addressed** — with a negative result (candidate mechanism killed by its own
positive control), not a resolution of the open question. The sharpest remaining open question
from `decision.md` is unchanged: what distinguishes Loch Leven/Paul doSat from the other 3
negative-role series that do NOT cross under any method tried.
