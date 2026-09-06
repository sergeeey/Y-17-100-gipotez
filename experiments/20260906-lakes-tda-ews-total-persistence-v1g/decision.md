# decision.md — 20260906-lakes-tda-ews-total-persistence-v1g

**Graph node:** `H-B3-1g` · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [ ] REJECT
- [x] **LEAD** (project three-outcome convention) — genuine, partial improvement; not clean, not
  a repeat of the entropy finding, clear next step

**Statement:** *Replacing Betti-1 persistence entropy with Betti-1 total persistence (same AR(1)
surrogate-null detection rule as V1, same 9 series) changes the false-positive PROFILE — one negative
control (Paul chl) stops being a false positive — but does not reach the PASS bar (still 4/5 false
positive), and introduces a new failure mode on one positive case (Peter pH now shows a TDA signal that
LAGS classical EWS by 100 days, rather than showing no signal at all as under entropy).*

## Evidence Summary — First Non-"NO_IMPROVEMENT" Verdict in the Entire B3 Arc

| Series | Role | V1 (entropy, AR1) | V1' (entropy, IAAFT) | V2' (entropy, detrend+IAAFT) | **V1g (total persistence, AR1)** |
|---|---|---|---|---|---|
| Lower Zurich | positive | FP-role n/a, TDA crossed, no lead | same pattern | TDA+classical crossed, +23mo | TDA crossed alone (2001.67), no lead |
| Windermere | negative | **FP** | **FP** | **FP** | **FP** (unchanged) |
| Loch Leven | negative | **FP** | **FP** | **FP** | **FP** (unchanged) |
| Peter chl | positive | no crossing | no crossing | no crossing | no crossing (unchanged) |
| Peter pH | positive | no crossing | no crossing | no crossing | **TDA crosses, but LAGS classical by 100 days** (new) |
| Peter doSat | positive | **+13d lead** | **+13d lead** | lost (no TDA crossing) | **+13d lead — reproduced, 4th time** |
| Paul chl | negative | **FP** | **FP** | **FP** | **NOT a false positive** (flips!) |
| Paul pH | negative | **FP** | **FP** | **FP** | **FP** (unchanged) |
| Paul doSat | negative | **FP** | **FP** | **FP** | **FP** (unchanged) |

**`n_false_positives`: 4/5 (down from 5/5 in every prior variant) → `verdict: IMPROVED_NOT_PASS`** — the
first time any variant in this entire B3 investigation (raw threshold, V1, V1', V2') has produced
anything other than a clean 5/5 or the raw floor-invalidity result.

## The Standout Finding: Peter doSat's +13-Day Lead Is Now 4-for-4

Across FOUR structurally different detection variants — V1 (AR(1) null, entropy), V1' (IAAFT null,
entropy), and now V1g (AR(1) null, total persistence) — Peter doSat shows the IDENTICAL +13-day TDA
lead (only V2', which additionally detrended the series, lost it). This is now the single most
robust, method-independent positive signal found anywhere in the `B3-MAY-TDA` investigation — more
robust than Lower Zurich's signal (which has changed direction/magnitude across variants) and vastly
more robust than any of the negative controls' false positives (which are also persistent, but that is
the problem, not a virtue).

## Kill Analysis (OSA)

### What Was Confirmed / Improved
- [x] Total persistence IS a genuinely different invariant in practice, not just in definition — it
  changed the false-positive SET (Paul chl), not just magnitudes.
- [x] Peter doSat's lead is now the best-replicated single finding in the whole B3 arc (4/4 methods
  that didn't detrend the series).

### What Was NOT Fixed
- [x] 4/5 negative controls still false-positive — nowhere near the ≤1/5 PASS bar.
- [x] A NEW problem appeared: Peter pH's TDA signal under total persistence is not just noisy, it is
  actively MISLEADING (fires 100 days AFTER the classical signal, which would be worse than useless as
  an early-warning tool in practice — a false sense of a lagging confirmation, not a false alarm, but
  also not helpful).

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Null-generating model (still AR(1), unchanged from V1) | Combine total persistence WITH IAAFT or detrend+IAAFT nulls | Untested combination — total persistence has only been tried with the simplest (AR(1)) null so far |
| Single invariant per run | Report BOTH entropy and total persistence together, flag a series as "positive" only if BOTH invariants agree | A conjunction rule could reduce false positives further (Paul chl now clean under total persistence AND already had entropy issues) at the cost of also filtering out true positives that only show up under one invariant |
| Peter pH's new lag behavior | Investigate directly why total persistence fires LATE here — could reveal a real, if delayed, structural signal, or an artifact of the total-persistence statistic's own dynamics | Cheapest immediate follow-up if this branch is pursued |

## What This Does NOT Mean

1. Does NOT constitute a PROMOTE — 4/5 false positive is still far from usable.
2. Does NOT mean total persistence is "better" than entropy in general — it traded one specific false
   positive (Paul chl) for one specific new problem (Peter pH's lag) on this exact population.
3. Does NOT invalidate `H-B3-1c`/`d`/`e`'s REJECT verdicts (entropy-based) — those remain correct
   characterizations of what was tested there.
4. Does NOT mean the bridge `B3-MAY-TDA` should be promoted — it means the "genuinely new approach"
   experiment recommended in `H-B3-1f` produced a genuinely different (not identical) result, which is
   itself the informative outcome regardless of whether it clears the PASS bar.

## Note on Floor-Ceiling (FL Step 4a)

Not re-run here: this experiment reuses V1's per-series AR(1)-surrogate self-calibration UNCHANGED
(only `tda_stat_fn` differs) — the self-calibrating detection rule itself already replaced the
fixed-threshold floor problem (`H-B3-1c`'s own Step 4a finding) with a per-series null, and that
mechanism's self-consistency was already validated in `tests/test_surrogate_null_v1.py` and is not
re-tested per invariant swap, exactly as V1'/V2' also did not re-run it. The new
`tests/test_total_persistence_v1g.py` checks are the correct analogue here: they verify the NEW
invariant's own properties (non-negative, numerically distinct from entropy, threads correctly through
the existing calibration), not a fresh floor/ceiling for machinery that didn't change.

## Pearl Card Update

**New information:** unlike the null-model axis (3 variants, byte-identical 5/5 false-positive set
every time — `H-B3-1c/d/e`'s central finding), the TDA-INVARIANT axis (entropy vs. total persistence,
1 comparison so far) DOES change the false-positive profile. This suggests the earlier "the detector
lacks specificity no matter which null model" conclusion (`H-B3-1f`) was correctly scoped to the null
model, not to the whole detector design — the topological invariant choice is a live, not exhausted,
axis. Peter doSat's 4-for-4 replication across every non-detrended variant is itself worth flagging as
the most credible single candidate signal in this bridge, warranting a closer, single-series
case-study look if `B3-MAY-TDA` is pursued further.
