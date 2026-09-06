# claim.md — 20260906-lakes-tda-ews-detrend-surrogate-v2prime

**Graph node:** `H-B3-1e` (new, per Minimal Relaxation Rule) · **Bridge:** `B3-MAY-TDA` · **Tier:** Full
**Parent:** `H-B3-1d` (V1', IAAFT-surrogate-null, REJECT — 5/5 negative controls still false-positived,
identical outcome to V1/AR(1))

> **Role of this experiment:** V2' from `H-B3-1d`'s Relaxation Map. Exactly ONE assumption changed from
> V1' (Minimal Relaxation Rule): the null-generating PROCEDURE now removes a smooth trend before
> generating the surrogate (on the residual), then adds the trend back. Everything else — per-series/
> per-timepoint calibration mechanism, population (all 9 series), window fraction, embedding, statistics,
> and the residual surrogate model itself (IAAFT) — is unchanged.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 9 series analyzed in `H-B3-1c`/`H-B3-1d` (Peter chl/pH/doSat, Paul chl/pH/doSat, Lower Zurich, Windermere, Loch Leven) |
| **Falsifiable predicate** | A null model that first removes a smooth trend (moving average, window = 25% of series length) and generates an IAAFT surrogate of the RESIDUAL, then adds the trend back, reduces the false-positive rate on the 5 negative-control series below V1'/V1's 5/5 |
| **Measurable outcome** | False-positive rate on the 5 negative controls under V2'; whether ≥1 positive case retains a TDA lead |

## FL Step -4: Source Trace / Novelty Check

- Detrend-then-surrogate is a standard construction in the surrogate-testing literature when a series
  is suspected non-stationary (Theiler et al. 1992's own framework explicitly separates "the null
  hypothesis under test" from nuisance non-stationarity; detrending before surrogate generation is a
  common variant, not a novel invention here).
- IAAFT itself: Schreiber & Schmitz 1996 (unchanged from `H-B3-1d`, already source-traced there).
- Population/detection-rule-mechanism source tracing unchanged from `H-B3-1c`/`H-B3-1d`.

## Escape-Point Gate Run BEFORE the Real 9-Series Compute (per H-B3-1d's own recommendation)

`H-B3-1d`'s decision.md flagged: "plot or numerically characterize whether the real series' rolling-
statistic trend looks smooth/monotonic... before choosing between richer-null and detrend-first" — this
check was run as `tests/test_detrend_surrogate_v2prime.py::test_mechanism_synthetic_negative_control_v2prime_reduces_false_positives`
BEFORE writing this claim.md's real-run section:

- Built a synthetic "negative control" (n=334, matching Peter/Paul Lake length): a smooth deterministic
  seasonal-like trend (sine + slow linear drift) + AR(1) noise (phi=0.6) — no real transition, exactly the
  mechanism `H-B3-1d` diagnosed.
- **Plain IAAFT false-positive rate on this synthetic series: 7/8 (87.5%)** — confirms the synthetic
  construction reproduces the diagnosed failure mode (a valid analogue, not an arbitrary toy).
- **Detrend-then-IAAFT false-positive rate on the SAME series: 3/8 (37.5%)** — confirms the fix
  meaningfully addresses the diagnosed mechanism BEFORE spending the real ~25-minute compute.
- `[VERIFIED-SYNTHETIC]` — this is a pipeline/mechanism sanity gate, not evidence for the real-world
  hypothesis itself (same status as `floor_false_positive_rate`'s AR(1) floor check elsewhere in this
  bridge). The real claim is tested only by the real 9-series run below.

## Natural Language Statement

> "We estimate whether replacing the plain IAAFT surrogate (V1') with a detrend-then-IAAFT surrogate
> (V2') — removing a smooth trend (moving-average window = 25% of series length) before generating the
> null on the residual, then adding the trend back — reduces the false-positive rate on the 5
> negative-control series (Windermere, Loch Leven, Paul chl/pH/doSat) below V1'/V1's 5/5, while
> preserving a detectable TDA lead on at least one positive case (Lower Zurich, Peter chl/pH/doSat)."

## HD-MAVP — single assumption changed (from H-B3-1d)

| # | Assumption | Status before (H-B3-1d) | Status now (V2') |
|---|---|---|---|
| A_null_procedure | Null-generating procedure: apply IAAFT directly to the raw series (assumes weak stationarity) | `killed` (5/5 negative controls still false-positive, identical to V1; rules out spectral richness as sufficient fix) | **replaced**: detrend (moving-average, frac=0.25) → IAAFT on residual → retrend |
| A_null_residual_model | Residual surrogate model | n/a (no detrend step existed) | IAAFT (unchanged, already validated in H-B3-1d) |
| A_rule (per-series calibration mechanism) | `alive` | unchanged, `alive` |
| A1–A4 (embedding, window, statistic choice) | unchanged | unchanged |
| A_detrend_frac | n/a | **new**: 0.25 (deliberately narrower than the 0.5 detection window, so the removed trend is slower than any potential regime-shift signal) — an explicit, stated design choice, not tuned to the real data |

**Rule respected:** only the null-generating procedure changed (one coherent new step: detrend/retrend),
the residual model itself (IAAFT) is carried forward unchanged. If V2' also fails, the next candidate is
V3 (descriptive-only reporting, abandoning binary verdicts for this population) — a new experiment ID
required.

## Compute budget

Detrending is `O(n)` (pandas rolling mean); IAAFT on the residual is the same `O(n log n) × 20 iterations`
cost as V1'. Same rep counts as V1/V1': 100 for classical statistics, 20 for TDA. Same bottleneck
(Betti-1/ripser), same expected wall-clock (~25 minutes).

## What This Does NOT Mean

1. Does NOT mean detrending is guaranteed correct if it passes — `DETREND_FRAC=0.25` is one specific,
   stated choice; a different window could give a different result, and this is not swept here.
2. A PASS here does NOT retroactively make V1/V1's REJECTs wrong — AR(1)/IAAFT alone genuinely failed on
   these series, independent of whether detrending fixes it.
3. Does NOT test V3 (descriptive-only) — untested, separate candidate if V2' also fails.
4. The synthetic escape-point check above is `[VERIFIED-SYNTHETIC]` — it validates the MECHANISM
   plausibly, not the real-world claim; only the real 9-series run below can confirm or reject that.

## MCID

Same bar as V1/V1': false-positive rate ≤ 1/5 negative controls with ≥1 surviving positive lead is the
target for PROMOTE. A false-positive rate strictly less than 5/5 is the minimum to call V2' "informative,
not identical to V1/V1'."
