# decision.md — 20260906-lakes-tda-ews-diagram-distance-v1j

**Graph node:** `H-B3-1j` · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [x] **REJECT** — per pre-registered kill criterion in `claim.md`: false-positive rate = 4/5, meeting
  the literal REJECT bar. Same discipline as `H-B3-1i`: kept the pre-registered verdict despite an
  interesting qualitative result (see below) rather than upgrading post-hoc.
- [ ] ARCHIVE

**Statement:** *A genuinely different detection FAMILY — Wasserstein-2 distance from each rolling
window's H1 diagram to a fixed baseline diagram, instead of any scalar diagram summary — reproduces
the same 4/5 false-positive rate and the same false-positive SERIES SET as the scalar-summary
variants (Windermere, Loch Leven, Paul pH, Paul doSat; Paul chl the sole exception, same as V1g/
H-B3-1i). But it restores Peter doSat's TDA-leads-classical lead to a positive value (+11 days,
close to the historical +13) and, for the first time in this entire investigation, gives Peter pH an
interpretable POSITIVE lead too (+2 days) — n_positive_cases_with_tda_lead=2, the best count achieved
by any variant so far (previous best: 1, in V1g).*

## Evidence Summary (real compute — a structurally new statistic family, not a parametric variant)

| Series | Role | V1g (AR1+total-persist.) lead | H-B3-1i (IAAFT+total-persist.) lead | H-B3-1j (AR1+Wasserstein-distance) lead |
|---|---|---|---|---|
| Lower Zurich | positive | null (no classical pair) | no TDA crossing | null (no classical pair) |
| Windermere | negative | +3.67 (FP) | null lead, FP via TDA-only | +2.25 (FP) |
| Loch Leven | negative | 0.0 (FP) | FP via classical only, no TDA cross | +0.08 (FP, essentially simultaneous) |
| Peter chl | positive | null (no classical pair) | null (no classical pair) | null (no classical pair) |
| Peter pH | positive | -100.0 (TDA lags) | -133.0 (TDA lags, larger) | **+2.0 (TDA LEADS — first time ever)** |
| **Peter doSat** | **positive** | **+13.0 (TDA leads)** | **-74.0 (TDA LAGS — sign flip)** | **+11.0 (TDA leads again, close to +13)** |
| Paul chl | negative | not FP | not FP | not FP |
| Paul pH | negative | +33.0 (FP) | FP via classical only, no TDA cross | +1.0 (FP) |
| Paul doSat | negative | +3.0 (FP) | +28.0 (FP) | +23.0 (FP) |

**False-positive count: 4/5, identical series set to V1g and H-B3-1i.** **Positive cases with a
genuine TDA lead: 2** (up from 0-1 in every prior variant) — both Peter pH and Peter doSat now show
TDA leading classical, though neither clears the ≤1/5 FP bar needed for PROMOTE.

## The Sharper Pattern This Result Reveals

Combined with `H-B3-1i`, this experiment lets the sign-flip finding be narrowed further. Peter doSat's
lead is **positive under BOTH AR(1)-null variants tested** (total persistence: +13; Wasserstein
diagram-distance: +11) and **negative under the one IAAFT-null variant tested** (total persistence:
-74). This is consistent with the sign flip being primarily a **null-model effect** (the spikier
IAAFT-derived threshold curve identified in `H-B3-1i`'s own mechanism diagnostic), not a
statistic-family effect — the diagram-distance family and the total-persistence family AGREE with
each other under the same (AR(1)) null, which they would not necessarily do if the statistic family
itself were driving the sign. This is a hypothesis strengthened by two data points, not yet a
conclusion: IAAFT + diagram-distance has not been tested, and would be the natural next check (see
Relaxation Map).

## Why REJECT, Not LEAD, Despite the Interesting Lead-Count Result

`claim.md`'s pre-registered LEAD condition required the false-positive rate to be strictly better
than 2/5 (the conjunction's best) or the false-positive SET to differ meaningfully. Neither holds: FP
rate is 4/5 (worse than 2/5), and the SET is identical to two prior variants. The improved
`n_positive_cases_with_tda_lead` count was not part of the pre-registered PROMOTE/LEAD/REJECT
criteria (the pre-registration only asked whether the false-positive rate improved and whether "the
lead" — implicitly Peter doSat's — reappeared with what sign). Per the Anti-Overfitting Gate's
verdict-shopping discipline, honoring the letter of the pre-registered criterion and documenting the
richer qualitative finding separately (here, and in the pearl registry) is the correct move, exactly
as done for `H-B3-1i`.

## Kill Analysis (OSA)

### What Was Killed
- [x] **"A diagram-distance statistic family reduces the false-positive rate below the scalar-summary
  family's best (2/5)"** — false. Same 4/5, same series.
- [x] **"The scalar-vs-diagram statistic-family axis explains the Peter doSat sign flip"** — false, or
  at least not supported: the sign is positive under BOTH statistic families tested with the AR(1)
  null (total persistence, diagram distance), suggesting the null-model axis (confirmed in `H-B3-1i`'s
  diagnostic) is the more likely driver, not the statistic family.

### What Was NOT Killed
- [x] Peter doSat's lead, when it appears with a positive sign, is now supported under THREE
  independently-motivated statistic/null combinations (V1/V1'/V1g's entropy-or-total-persistence +
  AR(1)-or-IAAFT[entropy only]; and now diagram-distance + AR(1)) — the AR(1)-null branch of this
  family tree is robust; the IAAFT-null branch (tested only against total persistence so far) is not.
- [x] Peter pH's TDA signal, previously either absent or badly lagging (-100 to -133 days) under every
  prior variant, is for the first time genuinely interpretable and LEADING under diagram-distance +
  AR(1) — a new, small but real positive data point for the bridge's core mechanism claim.
- [x] Paul doSat and, now also Loch Leven and Paul pH under this variant, remain false positives
  across every statistic family and null model combination tried in this session (7+ combinations for
  Paul doSat specifically) — still the single most concentrated unexplained false-positive evidence in
  the bridge.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Only AR(1) null tested against diagram-distance | Run IAAFT + diagram-distance (the natural test of "is the sign flip a null-model effect or a total-persistence-specific effect") | Directly tests the hypothesis raised in this decision.md's own "sharper pattern" section — highest-value next step |
| Fixed-baseline reference diagram | Try a previous-window (frame-to-frame) reference instead | Named in claim.md as the alternative if baseline-referenced is uninformative; FP rate here (4/5) is not below the scalar family's best, so this remains a live option |
| Wasserstein metric only | Try bottleneck distance (already implemented and tested, `metric="bottleneck"` parameter exists) | Cheap — no new pipeline code needed, already unit-tested in `test_diagram_distance_v1j.py` |

## What This Does NOT Mean

1. Does NOT establish that diagram-distance statistics are superior to scalar summaries for this
   bridge — false-positive rate is unchanged; the improvement is specifically in lead COUNT and sign
   consistency with the AR(1)-null branch, not in specificity.
2. Does NOT resolve why Loch Leven/Paul doSat/Paul pH/Windermere false-positive under this variant too
   — the open question from `H-B3-1h`'s case study remains open.
3. Does NOT test the IAAFT+diagram-distance combination named above as the highest-value next step —
   left for a future experiment if this line of inquiry continues.

## Note on Floor-Ceiling (FL Step 4a)

Not re-run here, same reasoning as `H-B3-1g`/`H-B3-1i`: reuses the per-series self-calibrating
surrogate-null detection rule UNCHANGED (only `tda_stat_fn` differs, null model unchanged from V1).
That rule's self-consistency was validated once in `tests/test_surrogate_null_v1.py`, not re-tested
per statistic-family swap. The new `tests/test_diagram_distance_v1j.py` checks verify the NEW
statistic's own properties (non-negative, zero at its own reference, numerically distinct from both
scalar summaries AND from the bottleneck-metric variant, threads correctly through the existing
calibration) — the correct analogue here, not a fresh floor/ceiling for unchanged machinery.

## Addendum (2026-09-06, same session) — reviewer-flagged P2 resolved: reference diagram non-degeneracy

Code review (`reviewer` agent) on this commit raised a real, checkable concern: `betti1_diagram_distance_series`
fixes the reference diagram to the first valid window's H1 diagram, but if that diagram happened to be
empty or near-empty, "distance from baseline" would collapse toward measuring the raw magnitude of
each subsequent window alone — numerically close to `betti1_total_persistence_series`, undermining
this experiment's "genuinely different detection FAMILY" framing (see claim.md's central argument).

Ran the cheap, fully-verifiable check the reviewer recommended: computed the reference diagram's
cardinality and total persistence for all 9 real series (one `ripser` call per series, no new
surrogate compute). Script: `check_reference_diagram_nondegeneracy.py`.

**Result: all 9 reference diagrams are non-degenerate** — 12 to 46 finite H1 bars each, total
persistence 0.17 to 10.06. Peter doSat specifically (the series whose lead is the headline finding of
this decision.md): 46 bars, total persistence 8.30 — clearly substantial real topological structure,
not a near-empty diagram. This confirms the diagram-distance statistic is genuinely comparing against
a meaningful baseline, not degenerating into a total-persistence proxy. The "Sharper Pattern" section's
claim of independent confirmation across two statistic families stands.

## Pearl Card Update

**New information:** the Peter doSat sign-flip finding from `H-B3-1i` is narrowed by a second data
point. The sign is positive under both statistic families tested against the AR(1) null (total
persistence: +13d; diagram-distance: +11d) and negative under the one IAAFT-null variant tested
(total persistence: -74d) — consistent with `H-B3-1i`'s own mechanism finding (IAAFT's null-threshold
curve is spikier, not just shifted) being the actual driver, rather than the choice of TDA statistic.
Also newly informative: Peter pH's TDA signal is interpretable and leading for the first time under
any method tried (+2d) — a small but genuine addition to the bridge's positive evidence, previously
this series only ever showed a badly-lagging or absent TDA signal.
