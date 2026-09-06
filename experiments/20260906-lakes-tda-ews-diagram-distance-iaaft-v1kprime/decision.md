# decision.md — 20260906-lakes-tda-ews-diagram-distance-iaaft-v1kprime

**Graph node:** `H-B3-1k` · **Date:** 2026-09-06

## Verdict

- [x] **REJECT** (standard FP-rate bar) — false-positive rate 4/5, same series set as every prior
  variant (Windermere, Loch Leven, Paul pH, Paul doSat).
- **Primary result: the pre-registered NULL-MODEL HYPOTHESIS is FALSIFIED.**

**Statement:** *This experiment was pre-registered specifically to test a prediction: if the
sign-flip discovered in `H-B3-1i` (Peter doSat's lead reversing from +13d to -74d) is a NULL-MODEL
effect, then IAAFT+diagram-distance should ALSO give a negative lead. It does not — Peter doSat's
lead here is +4.0 days, positive, matching `H-B3-1g` and `H-B3-1j` (both AR(1)-based), not `H-B3-1i`
(the one other IAAFT-based variant). The null-model-effect hypothesis formed after two data points is
falsified by the third and fourth.*

## The Full 2×2 Design, Now Complete

| | AR(1) null | IAAFT null |
|---|---|---|
| **Total persistence** | H-B3-1g: **+13.0d** | H-B3-1i: **-74.0d** |
| **Diagram-distance** | H-B3-1j: **+11.0d** | H-B3-1k: **+4.0d** |

Peter doSat's lead is positive in 3 of 4 cells and negative in exactly one (IAAFT+total-persistence).
Neither the null-model axis (AR1 vs IAAFT) nor the statistic axis (total persistence vs
diagram-distance) cleanly separates positive from negative — the pattern that looked like "IAAFT
causes negative" after `H-B3-1i` alone does not hold across the full grid. The -74d result now looks
more like an idiosyncratic outlier specific to the IAAFT+total-persistence PAIRING than evidence of a
general null-model effect.

## A Second, Unplanned Mirror-Image Pattern: Peter pH

Not pre-registered, found while filling in this table, but too directly relevant to omit:

| | AR(1) null | IAAFT null |
|---|---|---|
| **Total persistence** | H-B3-1g: -100.0d | H-B3-1i: -133.0d |
| **Diagram-distance** | H-B3-1j: **+2.0d** | H-B3-1k: -45.0d |

Peter pH is negative in 3 of 4 cells — almost the MIRROR of Peter doSat's pattern (positive in 3 of
4). Neither series shows a null-model-driven or statistic-driven pattern; each shows its own
idiosyncratic mix. This is additional, independent evidence against any simple one-axis explanation
of lead sign, and against treating either series' lead sign as a stable property at all across this
2×2 space.

## Kill Analysis (OSA)

### What Was Killed
- [x] **The null-model-effect hypothesis** (pre-registered from `H-B3-1i`/`H-B3-1j`'s pearl entry:
  "the sign flip is driven by IAAFT's spikier null-threshold curve, not the choice of statistic") —
  directly falsified. If it were true, H-B3-1k (IAAFT+diagram-distance) should have given a negative
  lead for Peter doSat. It gave +4.0, positive.
- [x] **Any simple one-axis (null-model OR statistic-family) explanation for lead sign** — the
  2×2×2-series data (Peter doSat + Peter pH) shows no clean split along either axis for either
  series.

### What Was NOT Killed
- [x] Peter doSat's TENDENCY toward a positive lead (3 of 4 cells, small-to-moderate magnitude:
  +4 to +13 days) — weaker than the "identical across 4 variants" framing used before `H-B3-1i`, but
  not zero; the -74d result looks like the outlier now, not the new normal.
- [x] `H-B3-1i`'s own MECHANISM diagnostic (the IAAFT null-threshold curve for Peter doSat under
  total-persistence specifically was measurably spikier at t=172d) is not falsified by this
  experiment — that was a direct measurement on that one specific (series, null, statistic) triple,
  not a general claim about IAAFT nulls. What's falsified is the GENERALIZATION from that one
  measurement to "IAAFT nulls generally flip signs" — a scope error the original finding's own
  wording tried to guard against ("this is a hypothesis strengthened by two data points, not yet a
  conclusion" — `H-B3-1i` decision.md), and which this experiment correctly tested and closed.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Lead-sign explanation sought along a single axis (null model OR statistic) | Consider a genuine interaction/idiosyncrasy model: each (series, null, statistic) triple has its own near-threshold behavior with no simple additive structure | Matches the Peter pH mirror-image finding above; would need many more cells (different windows, different series) to characterize, likely low information-per-cost per CDT Protocol given the small, noisy effect sizes involved (4-13 days on ~330-point series) |
| 2×2 design considered exhausted after 4 cells | Extend to detrend+IAAFT (the fifth null-model variant, already used for entropy in `H-B3-1e`) against both statistics | Low priority — the null-model axis has now been shown NOT to be the driver, weakening the motivation for this extension |

## What This Does NOT Mean

1. Does NOT mean Peter doSat's positive-lead tendency is meaningless — 3 of 4 cells still show it,
   just not as an unconditional, method-independent property as originally (over-)stated.
2. Does NOT invalidate `H-B3-1i`'s own mechanism diagnostic (the specific numeric measurement of the
   IAAFT/total-persistence null threshold at t=172d) — only the GENERALIZATION drawn from it.
3. Does NOT provide a positive explanation for why lead sign varies as it does across this small grid
   — the honest state is "idiosyncratic, no simple axis explains it," not a new confirmed mechanism.

## Note on Floor-Ceiling (FL Step 4a)

Not re-run here, same reasoning as every prior V1-family variant: reuses the per-series
self-calibrating surrogate-null detection rule unchanged; both `surrogate_fn` and `tda_stat_fn` are
individually already-validated components (IAAFT: `H-B3-1d`; diagram-distance: `H-B3-1j`), and their
combination is unit-tested (`tests/test_diagram_distance_iaaft_v1kprime.py`) rather than requiring a
fresh floor/ceiling arm.

## Pearl Card Update

**Correction to the `H-B3-1j` pearl entry (2026-09-06, same session):** that entry's
`falsifiable_prediction` — "IAAFT+diagram-distance will flip Peter doSat's lead negative, confirming
the null-model-effect hypothesis" — is FALSIFIED. Status updated in `pearl_registry/INDEX.md`. This
is exactly the kind of prediction-then-test cycle the Falsification Ladder is meant to produce: a
hypothesis formed from 2 data points, made explicitly falsifiable, and cleanly falsified by the 3rd
and 4th. The bridge-level takeaway strengthens, not weakens: `B3-MAY-TDA`'s `evidence: CONFLICT`
status is reinforced — neither series' lead sign is a stable, well-understood property across this
small grid of reasonable methodological choices, which is itself informative about how much weight
the bridge's positive evidence can bear.
