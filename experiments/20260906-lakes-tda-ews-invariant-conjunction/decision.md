# decision.md — 20260906-lakes-tda-ews-invariant-conjunction

**Graph node:** `H-B3-1h` · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [ ] REJECT
- [x] **LEAD** — best specificity result in the entire B3 investigation so far; still short of the
  PROMOTE bar, but a genuine, well-motivated improvement, not a repeat

**Statement:** *Requiring agreement between two independently-computed TDA invariants (persistence
entropy from V1, total persistence from V1g), both using the same AR(1)-surrogate null, reduces the
TDA-crossing false-positive count on the 5 negative controls to 2/5 — lower than either invariant alone
(entropy: 3/5, total persistence: 4/5) — while Peter doSat's robust +13-day lead survives the
conjunction unchanged, and Peter pH's problematic 100-day-lag signal (introduced in `H-B3-1g`) is
naturally filtered out.*

## Evidence Summary (no new compute — pure re-join of V1 and V1g's committed results)

| Series | Role | Entropy crosses? | Total persistence crosses? | Conjunction (both)? | Lead (if any) |
|---|---|---|---|---|---|
| Lower Zurich | positive | yes | yes | **yes** | uninterpretable (no classical crossing) |
| Windermere | negative | no | yes | no | — |
| Loch Leven | negative | yes | yes | **yes → FP** | -2.7d (entropy) / 0d (total persistence) |
| Peter chl | positive | yes | yes | **yes** | uninterpretable (no classical crossing) |
| Peter pH | positive | **no** | yes | no | — (the 100-day-lag signal is filtered out) |
| Peter doSat | positive | yes | yes | **yes** | **+13d, identical under both invariants** |
| Paul chl | negative | yes | no | no | — |
| Paul pH | negative | no | yes | no | — |
| Paul doSat | negative | yes | yes | **yes → FP** | +30d (entropy) / +3d (total persistence) |

**Conjunction false positives: 2/5** (Loch Leven, Paul doSat) — down from 3/5 (entropy TDA-crossings
alone) and 4/5 (total persistence alone). **Conjunction positive signals: 3/3** positive cases show
conjunction agreement, though only Peter doSat's is interpretable (has a paired classical crossing to
compute a lead against).

## Why This Is the Best Result Yet, and Why It's Still Not PROMOTE

This is the lowest false-positive count found anywhere in the `B3-MAY-TDA` investigation across every
method tried (raw threshold, V1, V1', V2', V1g, now this conjunction) — genuinely earned by combining
two independently-motivated invariants, not by loosening the detection criterion. It also naturally
solves `H-B3-1g`'s own new problem (Peter pH's misleading late signal) as a side effect, since entropy
never agreed with it. **But 2/5 is still well above the pre-registered `H-B3-1c`-era MCID of ≤1/5** —
Loch Leven and Paul doSat remain false-positive under BOTH invariants, meaning whatever drives their
false signal is not specific to either invariant's particular sensitivity, and a conjunction cannot fix
a problem that both methods share.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] Conjunction of independently-motivated TDA invariants is a real, working technique here — reduces
  false positives below either alone, not merely averaging them.
- [x] Peter doSat's signal is now supported at the highest level of scrutiny available in this session
  (4 individual variants + this conjunction, all agreeing).

### What Remains Unfixed
- [x] Loch Leven and Paul doSat false-positive under BOTH invariants — this is now the sharpest
  remaining open question in the bridge: what property do these two specific series share that NEITHER
  entropy NOR total persistence (nor 3 different null models tested earlier on entropy) can filter out?

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Conjunction built only from AR(1)-null variants (V1, V1g) | Extend conjunction to include IAAFT-null and/or detrend-null total-persistence variants (not yet computed) | Would need 1-2 new real compute runs (~25 min each), not free like this join |
| Loch Leven / Paul doSat as the last 2 unexplained false positives | A focused single-series case study on just these two (what does their raw data actually look like around the false-crossing date?) | Cheapest possible next step — no new compute, just closer reading of already-collected data |
| Binary conjunction (both invariants must cross) | A weighted/scored combination instead of strict AND | Untested; strict AND is the simplest, most interpretable rule, chosen first per Occam's razor |

## What This Does NOT Mean

1. Does NOT constitute a validated, pre-registered predictive rule — the conjunction was formed by
   looking at both invariants' AR(1) results after they were already computed; a genuine test would
   need to pre-register the conjunction rule and test it on new data, which this fixed 9-series
   population cannot provide (same in-sample caveat as the whole `H-B3-1*` arc).
2. Does NOT mean the bridge is close to being usable in practice — 2/5 false positive is still far
   worse than a real early-warning system would need.
3. Does NOT explain why Loch Leven and Paul doSat resist every method tried — that remains the single
   most important open question for anyone continuing this bridge.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable here, same reasoning as `H-B3-1f` (V3) and `H-B3-1g`: this is a descriptive re-join of
already-collected, already-floor-checked data (both V1 and V1g inherit V1's own validated per-series
AR(1) self-calibration) — no new compute, no new null model, nothing to re-float a floor/ceiling against.

## Addendum (2026-09-06, same session) — Relaxation Map item 2 addressed

Ran the cheapest-named Relaxation Map item: a focused single-series case study on Loch Leven and
Paul doSat's raw data around their own already-recorded `tda_betti_crossing` times. Full writeup
in `case_study_notes.md`; raw diagnostic output in
`metrics/case_study_loch_leven_paul_dosat.json`.

**Result:** both false positives cross during a local variance MINIMUM (var_ratio 0.259 / 0.151),
opposite the textbook critical-slowing-down signature. But a contrast check against Peter doSat
(the one interpretable true positive) shows the SAME signature (var_ratio 0.297) — per Gate 3
(Positive-Control Digitization, `artifact-provenance-gates.md`: "a test that cannot distinguish
your control from your target is not a test"), this **falsifies the local-variance-minimum
mechanism as an explanation specific to the false positives**. Likely a generic property of the
expanding-Kendall-tau crossing rule itself, not of these two series' data. The core open question
(what distinguishes Loch Leven/Paul doSat from the 3 other negative-role series that never cross)
is unchanged and remains open.

This does not change the LEAD verdict above.

## Addendum 2 (2026-09-06, same session) — pearl's falsifiable_prediction tested and CONFIRMED

Followed the pearl registry entry's own `falsifiable_prediction` (filed in the addendum above):
checked `local_var_ratio` at the crossing window for ALL series in the B3 population that actually
have a `tda_betti_crossing` (6 of 9 — Windermere, Peter pH, Paul pH never cross at all, so there is
no window to check). Script: `all_series_variance_ratio_check.py`; output:
`metrics/all_series_variance_ratio_check.json`.

**Result: 6/6 (100%) of crossing series show var_ratio < 0.5**, across both positive role (mean
0.375: Lower Zurich, Peter chl, Peter doSat) and negative role (mean 0.199: Loch Leven, Paul chl,
Paul doSat). The prediction is fully confirmed — this is a **generic property of the
expanding-Kendall-tau threshold-crossing rule itself**: the detector systematically fires when a
series locally quiets down, not when it becomes more unstable, regardless of whether that quiet
stretch precedes a real transition. It is not specific to Loch Leven/Paul doSat and does not
discriminate false positives from true positives — closing this line of inquiry as far as it can
go with existing data. The pearl registry entry's status is updated to CONFIRMED (see
`pearl_registry/INDEX.md`).

**What this means for the bridge as a whole:** the detection RULE (Kendall-tau ≥ 0.5 on an
expanding window) itself has a structural bias toward firing during local quiescence, independent
of the statistic family (classical or TDA) it is applied to. This is a methodological finding about
the shared detection apparatus across the entire `H-B3-1*` arc, not about any one invariant or
series — worth flagging in any future revision of the detection rule, separate from the
still-unresolved question of why Loch Leven/Paul doSat specifically cross under every
invariant/null-model tried while the other 3 negative-role series do not.

## CORRECTION ADDENDUM (2026-09-07, resuming B3 work — Hindsight Distortion Gap discipline, not a
silent rewrite)

Re-examining this file's own claim ("Windermere/Peter pH never cross under ANY method") before
starting a new investigation, cross-tabulated `tda_betti_crossing` for all 9 series across ALL 7
method variants actually run in this arc (V1, V1', V2', V1g, V1g', diagram-distance+AR1,
diagram-distance+IAAFT), read directly from each experiment's own `metrics/run.json` — not
reconstructed from memory:

```
                     V1  V1' V2' V1g V1g' diag-AR1 diag-IAAFT   rate
Paul_doSat           X   X   X   X   X    X        X            7/7
Loch_Leven           X   X   X   X   .    X        X            6/7
Lower_Zurich         X   X   X   X   .    X        X            6/7
Windermere           .   X   X   X   X    X        X            6/7
Peter_chl            X   X   .   X   X    X        X            6/7
Peter_doSat          X   X   .   X   X    X        X            6/7
Peter_pH             .   .   .   X   X    X        X            4/7
Paul_chl             X   X   X   .   .    .        .            3/7
Paul_pH              .   .   .   X   .    X        X            3/7
```

**The claim above was WRONG, not just imprecisely worded:** `Windermere` crosses in 6 of 7 method
variants — the SAME rate as three of the four positive-role series (`Lower Zurich`, `Peter_chl`,
`Peter_doSat`). Crossing rate does NOT correlate with true/false-positive role at all. The actual
distinctive outliers are `Paul_doSat` (the ONLY series crossing under literally every method tested)
and `Paul_chl`/`Paul_pH` (tied for the LOWEST rate, 3/7) — not "Loch Leven and Paul doSat vs. the
other 3." `Loch_Leven` itself sits at 6/7, indistinguishable from the role-mismatched `Windermere`
and three positives.

**This reframes the sharpest open question more precisely and more tractably than before:** the
most informative comparison is not "2 stubborn negatives vs 3 clean negatives" (that framing doesn't
survive the actual data) — it is **`Paul_doSat` (7/7) vs. its own siblings `Paul_chl`/`Paul_pH`
(3/7 each)**: three variables measured on the SAME lake, SAME period, SAME (absence of)
manipulation, differing only in which physical quantity is recorded. This is a cleaner natural
experiment than any cross-lake comparison, since lake-level confounds (basin morphology, sampling
protocol, observer, instrumentation) are held constant by construction. See the new investigation in
`paul_lake_variable_comparison.py`/`paul_lake_variable_comparison_notes.md` for the follow-up.

## Addendum 3 (2026-09-07) — Paul lake within-lake variable comparison: trend hypothesis REJECTED,
inverted, new candidate found

Ran `paul_lake_variable_comparison.py` on Paul lake's 3 variables (same lake, same period, same
absence of manipulation — the cleanest natural comparison available, per the corrected framing
above). Pre-registered falsifiable predicate: `Paul_doSat` (crosses 7/7 methods) shows a STRONGER
raw monotonic trend than `Paul_chl`/`Paul_pH` (3/7 each), since expanding-Kendall-tau detectors are
known to respond to genuine secular drift.

**Result: REJECTED, and inverted.**

| Variable | Spearman trend ρ | trend p-value | ACF lag-1 | TDA crossing rate |
|---|---|---|---|---|
| `pH` | **-0.579** (strong) | 2.7×10⁻³¹ | 0.940 | 3/7 (lowest) |
| `chl` | -0.187 (weak) | 0.0006 | 0.922 | 3/7 (lowest) |
| **`doSat`** | **-0.044 (essentially none)** | **0.418 (n.s.)** | **0.874 (lowest of the 3)** | **7/7 (highest)** |

`pH` has by far the STRONGEST, most statistically overwhelming secular trend of the three
variables, yet the LOWEST crossing rate. `doSat` has a trend statistically indistinguishable from
zero, yet the HIGHEST possible crossing rate. This is the opposite of the pre-registered
prediction — a clean, informative falsification, not a null (no-signal) result.

**New candidate surfaced, not yet tested:** `doSat` has the lowest lag-1 autocorrelation of the
three (0.874 vs. 0.922/0.940) — faster decorrelation, i.e. noisier / less persistent than `chl`/
`pH`. A candidate mechanism: an AR(1) surrogate null is calibrated to the SAME empirical AC1 as the
real series; a series with genuinely lower AC1 (like `doSat`) sits closer to white noise, and any
higher-order structure in the real data (e.g. short storm/wind-mixing bursts well documented in
limnological dissolved-oxygen records, not captured by a simple AR(1) model) would be relatively
MORE anomalous against that null than the same structure would be against a higher-AC1 null — a
different, autocorrelation-mediated route to more frequent crossings, not a trend-mediated one.
**Not tested here** — this is a Pearl Registry candidate for a follow-up, not a claim.

## Kill Analysis (OSA) — Addendum 3

### What Was Confirmed
- [x] The naive "raw monotonic trend explains crossing rate" hypothesis is REJECTED for this
  specific, cleanest-available natural comparison (same lake, same period).

### What Was NOT Confirmed
- [x] No replacement mechanism confirmed — the autocorrelation-difference candidate is named but
  untested.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Trend (Spearman ρ vs. time) as the candidate mechanism | Test lag-1 autocorrelation itself (not trend) as the predictor, across all 9 series (not just Paul lake's 3) — does crossing rate correlate with empirical AC1 across the full population? | Directly follows from this addendum's own surfaced candidate; cheap, reuses already-loaded series |
| Within-lake (Paul) comparison only | Repeat the SAME within-lake comparison on Peter lake's 3 variables (chl, pH, doSat) as a second natural-experiment replicate | Peter is the positive-role lake; if the same AC1-crossing-rate pattern holds there too, it strengthens the candidate considerably |

## Note on Floor-Ceiling (FL Step 4a) — Addendum 3

Not applicable — this is a descriptive statistical comparison (trend, autocorrelation) of already-
collected raw series, not a detection-rule run being tested against a threshold. There is no
floor/ceiling construction here: the finding is a REJECT of a candidate mechanism via direct
statistical comparison, not a pass/fail against a null-model floor.

## Addendum 4 (2026-09-07) — AC1-vs-crossing-rate candidate tested population-wide: WEAK, not
statistically confirmed

Followed up Addendum 3's own surfaced candidate (lower lag-1 autocorrelation → higher TDA-crossing
rate) across the full 9-series population (`ac1_vs_crossing_rate_check.py`).

**Result: `rho=-0.523, p=0.149`** — direction matches the prediction, but NOT statistically
significant at `n=9`. **Important confound caught before over-interpreting:** the 3 `obrienlakes`
series (`Lower Zurich`, `Windermere`, `Loch Leven`) are MONTHLY-sampled PCA1 scores, while all 6
`peterlake` series are DAILY-aggregated — adjacent daily values are mechanically more similar than
adjacent monthly values, so AC1 differs by sampling interval alone, confounding any cross-population
comparison. Re-ran restricted to the 6 sampling-frequency-matched `peterlake` series only
(`ac1_vs_crossing_rate_peterlake_only.py`): **`rho=-0.441, p=0.381`** (`n=6`) — same direction,
still not significant.

**Verdict: WEAK, not CONFIRMED.** Both tests point the same direction the candidate predicted, but
neither reaches significance, and `n=6-9` is honestly underpowered to detect anything short of a
very strong effect. Per FL discipline, this stays `[WEAK]` — a hint worth naming, not a finding to
promote or act on.

## Note on Floor-Ceiling (FL Step 4a) — Addendum 4

Not applicable — a correlation test between two already-computed descriptive statistics (AC1,
crossing rate), not a detection-rule run against a null-model floor.

**Post-commit reviewer catch (2026-09-07, same session):** the `reviewer` agent, run per the
project's own 3+-file-Python-change checklist, found a real P1 bug in `paul_lake_variable_
comparison.py`'s `approx_n_seasons` field — it diffed `season_time`, whose own gap-bridging logic
deliberately compresses every season boundary to a single nominal step (indistinguishable from a
normal daily increment, by the design of `peterlake/run.py`'s own `median_gap_bridge_days`), so the
heuristic silently returned `1` for every series regardless of the real season count. Confirmed
NOT load-bearing (never referenced in this file's own trend/ACF conclusions above). Fixed by
independently re-deriving season boundaries from the raw decimal-year axis (`count_seasons`,
mirroring `load_daily_series`'s own gap logic exactly) rather than the season-time-diff heuristic.
Corrected field now reads `n_seasons: 3` for all three Paul lake variables, matching
`peterlake/run.py`'s own `INCLUDED_SEASONS = (2008, 2009, 2010)` exactly. Regression test added.

## Session Summary — B3 case-study thread (2026-09-07)

Three genuinely distinct candidate mechanisms for "why do some series resist correction under every
method more than others" have now been tested against real data in this thread:
1. **Local variance minimum at the crossing** — KILLED by its own positive control (same session,
   2026-09-06).
2. **Raw monotonic trend strength** — REJECTED, inverted (Addendum 3): the variable with by far the
   strongest trend (`pH`) has the LOWEST crossing rate; the variable with no trend (`doSat`) has the
   HIGHEST.
3. **Lag-1 autocorrelation** — WEAK (Addendum 4): direction matches prediction twice (full
   population and sampling-frequency-controlled subset) but neither reaches significance at the
   available sample sizes.

**Also corrected along the way:** the original framing ("2 series always cross, 3 never cross") was
factually wrong, not merely imprecise — the real pattern is a spectrum with `Paul_doSat` as the sole
7/7 outlier and `Paul_chl`/`Paul_pH` as the sole 3/7 low-crossers, uncorrelated with
positive/negative role.

**Honest state of the open question:** no single raw-series statistic tested so far cleanly explains
the crossing-rate spectrum. The `AC1` candidate remains the most promising untested-to-significance
lead (consistent direction, twice), but would need either a larger population or a differently-
powered test (e.g., a designed comparison rather than the 9 series this bridge happens to have) to
move past `[WEAK]`.

## Pearl Card Update

**New information:** two specific series (Loch Leven, Paul doSat) have now resisted false-positive
correction under: 3 different null models (AR(1), IAAFT, detrend+IAAFT) AND 2 different TDA invariants
(entropy, total persistence) AND their conjunction. This is the most concentrated, most
method-independent false-positive evidence in the whole investigation — stronger than the earlier
"Paul doSat 4/4" finding (`H-B3-1f`) because it now also survives a genuinely different topological
invariant, not just different null models on the same invariant. Whatever produces this signal in these
two specific series is very likely a genuine, real, reproducible STRUCTURAL feature of their data — just
not the regime-shift signal the detector was built to find. Worth a dedicated look at what these two
series' raw dynamics actually look like, independent of any further detector-variant engineering.
