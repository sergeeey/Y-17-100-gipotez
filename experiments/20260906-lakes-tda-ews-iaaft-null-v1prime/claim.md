# claim.md — 20260906-lakes-tda-ews-iaaft-null-v1prime

**Graph node:** `H-B3-1d` (new, per Minimal Relaxation Rule) · **Bridge:** `B3-MAY-TDA` · **Tier:** Full
**Parent:** `H-B3-1c` (V1, AR(1)-surrogate-null, REJECT — 5/5 negative controls still false-positived)

> **Role of this experiment:** V1' from `H-B3-1c`'s Relaxation Map. Exactly ONE assumption changed from
> V1 (Minimal Relaxation Rule): the null-generating model. Everything else — per-series/per-timepoint
> calibration mechanism, population (all 9 series), window fraction, embedding, statistics — is
> unchanged. Reuses `surrogate_null_curve`/`surrogate_crossing` (the V1 detection-rule machinery,
> already validated) via its new `surrogate_fn` parameter, passing `iaaft_surrogate` instead of
> `ar1_surrogate`.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 9 series analyzed in `H-B3-1c` (Peter chl/pH/doSat, Paul chl/pH/doSat, Lower Zurich, Windermere, Loch Leven) |
| **Falsifiable predicate** | An IAAFT-surrogate null (preserves the full power spectrum and exact amplitude distribution, not just lag-1 autocorrelation) reduces the false-positive rate on the 5 negative-control series below V1's 5/5, per `H-B3-1c`'s diagnosed cause (AR(1) too simple a null) |
| **Measurable outcome** | False-positive rate on the 5 negative controls under V1'; whether ≥1 positive case retains a TDA lead |

## FL Step -4: Source Trace / Novelty Check

- IAAFT: Schreiber & Schmitz 1996 ("Improved Surrogate Data for Nonlinearity Tests", Phys. Rev. Lett.
  77, 635) — standard, widely-cited surrogate-testing method, not a novel invention. `[VERIFIED]` by
  implementation-level cross-check: `tests/test_iaaft_v1prime.py` confirms the implemented algorithm
  reproduces its two defining properties (exact amplitude-distribution match; spectrum error ~1.5%
  vs AR(1)'s ~50% on a series with AR(2)+trend structure AR(1) cannot represent).
- Population/detection-rule-mechanism source tracing unchanged from `H-B3-1c`.

## Natural Language Statement

> "We estimate whether replacing the AR(1) surrogate (V1) with an IAAFT phase-randomized surrogate
> (V1') — preserving the full power spectrum and exact amplitude distribution of each real series
> instead of only its lag-1 autocorrelation — reduces the false-positive rate on the 5 negative-control
> series (Windermere, Loch Leven, Paul chl/pH/doSat) below V1's 5/5, while preserving a detectable TDA
> lead on at least one positive case (Lower Zurich, Peter chl/pH/doSat)."

## HD-MAVP — single assumption changed (from H-B3-1c)

| # | Assumption | Status before (H-B3-1c) | Status now (V1') |
|---|---|---|---|
| A_null | Null-generating model: AR(1) (matches lag-1 autocorrelation only) | `killed` (5/5 negative controls still false-positive; real series have structure beyond lag-1) | **replaced**: IAAFT (matches full spectrum + exact amplitude distribution) |
| A_rule (per-series calibration mechanism) | `alive` (validated by self-consistency test) | unchanged, `alive` |
| A1–A4 (embedding, window, statistic choice) | unchanged | unchanged |

**Rule respected:** only A_null changed. If V1' also fails, the next candidates (V2: detrend-then-null,
V3: descriptive-only reporting) require ANOTHER new experiment ID.

## Compute budget

IAAFT is FFT-based (`O(n log n)` per iteration × 20 iterations), comparable cost to `ar1_surrogate`'s
O(n) generation — the bottleneck remains the TDA (Betti-1/ripser) computation, unchanged from V1. Same
rep counts as V1: 100 for classical statistics, 20 for TDA.

## What This Does NOT Mean

1. Does NOT mean IAAFT is guaranteed correct if it passes — it is the specific fix diagnosed from V1's failure mode, not validated as uniquely sufficient.
2. A PASS here does NOT retroactively make V1's REJECT wrong — AR(1) genuinely was too simple for these series, independent of whether IAAFT succeeds.
3. Does NOT test V2 (detrend-then-AR(1)) or V3 (descriptive-only) — untested, separate candidates if V1' also fails.

## MCID

Same bar as V1: false-positive rate ≤ 1/5 negative controls with ≥1 surviving positive lead is the
target for PROMOTE. A false-positive rate strictly less than 5/5 (even if not ≤1/5) is the minimum to
call V1' "informative, not identical to V1."
