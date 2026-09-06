# decision.md — 20260906-lakes-tda-ews-iaaft-null-v1prime

**Graph node:** `H-B3-1d` · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [x] **REJECT** — same outcome in kind as V1 (`H-B3-1c`), but a materially more informative diagnosis
- [ ] ARCHIVE

**Falsified statement:** *Replacing AR(1) with an IAAFT phase-randomized surrogate (preserving the full
power spectrum and exact amplitude distribution) reduces the false-positive rate on the 5 negative-control
series below V1's 5/5.* It does not: **5 of 5 negative-control series still false-positived**, essentially
reproducing V1's pattern series-for-series (same false-positive set, same directionally-consistent Peter
doSat lead of +13 days, near-identical crossing dates on most series).

## Evidence Summary

| Series | Role | V1 (AR(1)) false positive? | V1' (IAAFT) false positive? | Comment |
|---|---|---|---|---|
| Lower Zurich | positive | — | — | both silent on classical; TDA crossed both times (~2000) |
| Windermere | negative | **yes** | **yes** | |
| Loch Leven | negative | **yes** | **yes** | |
| Peter chl | positive | — | — | |
| Peter pH | positive | — | — | |
| Peter doSat | positive | — | — | **+13 day TDA lead, identical under both null models** |
| Paul chl | negative | **yes** | **yes** | |
| Paul pH | negative | **yes** | **yes** | |
| Paul doSat | negative | **yes** | **yes** | lead widened 30→35 days, same sign |

5/5 negative controls false-positive, identical set to V1. `n_positive_cases_with_tda_lead = 1` (Peter
doSat), same as V1.

## Why This Result Is Informative Despite Being "The Same Outcome"

A naive reading is "nothing changed, IAAFT was a wasted experiment." That is wrong. **IAAFT and AR(1) are
qualitatively different null models** — IAAFT is verified (unit tests, `tests/test_iaaft_v1prime.py`) to
match the FULL power spectrum (all lags) and the EXACT amplitude distribution of each real series; AR(1)
matches only lag-1 autocorrelation. If AR(1)'s failure (`H-B3-1c`) were caused by missing higher-lag
linear structure, IAAFT — which captures that structure by construction — should have shown a
meaningfully different (lower) false-positive rate. **It produced essentially the same result.** This
rules out "insufficient linear/spectral richness" as the explanation and narrows the diagnosis
considerably (see Kill Analysis).

## Kill Analysis (OSA, required for REJECT)

### What Was Killed

- **The hypothesis that AR(1)'s failure in `H-B3-1c` was caused by insufficient spectral/linear
  richness.** IAAFT is a strictly richer linear null (full spectrum + exact amplitude distribution) and
  performs no better. Linear-structure richness, as a category of fix, is now killed for this specific
  false-positive problem.

### What Was NOT Killed — and a sharper diagnosis

- [x] **The per-series calibration mechanism** — still validated sound (unit tests unchanged).
- [x] **A1–A4** — untouched.
- [x] **Peter doSat's directional TDA lead** — reproduced near-identically under a completely different
  null model, which is itself a small positive signal for that one series' robustness (though still
  uninterpretable given the false positives elsewhere).
- **New, sharper hypothesis exposed by this specific REJECT:** the real negative-control series most
  likely contain a **within-season deterministic/non-stationary trend** (e.g. a repeatable seasonal
  bloom-decline trajectory, warming curve, or nutrient-depletion arc) that is NOT adequately modeled as
  "a realization of a stationary linear stochastic process" — which is the shared assumption underlying
  BOTH AR(1) and IAAFT. Phase-randomization (IAAFT's mechanism) assumes (weak) stationarity; a genuinely
  non-stationary deterministic component survives phase randomization in neither the real series' own
  rolling-statistic trend nor is it destroyed in the surrogate's power spectrum matching — both the real
  series AND its surrogates end up producing coherent low-frequency rolling-statistic trends for the same
  underlying reason (strong low-frequency spectral power), so the null band widens right along with the
  real signal instead of narrowing around "typical noise." This is why a RICHER stationary-process
  surrogate did not help: the missing ingredient is not spectral richness, it is stationarity itself.

### Relaxation Map (for surviving assumptions)

| Assumption | Modification | New Path | Known kill-evidence? | Cheapest test |
|---|---|---|---|---|
| Null-generating model class (stationary linear process, AR(1) or IAAFT) | **Replace category**: detrend each series (e.g. subtract a smooth seasonal fit — LOESS or low-order polynomial per season) BEFORE generating a surrogate (AR(1) or IAAFT) of the RESIDUAL, then add the trend back | V2': detrend-then-surrogate | No — this is exactly V2 from `H-B3-1c`'s own Relaxation Map, now independently motivated by IAAFT's failure, not just AR(1)'s | Add a per-season LOESS/polynomial detrend step before `ar1_surrogate`/`iaaft_surrogate`; moderate new code (one detrend function + residual/recompose logic), no new data |
| Detection target | Same V3 candidate as before: descriptive-only reporting, no binary verdict | V3: least preferred, sacrifices falsifiability | No | Cheapest, last resort |

_V2' is now the clear next candidate — it was ALREADY named in `H-B3-1c`'s Relaxation Map before this
experiment ran, and this experiment's result (richer null, same failure) is independent evidence
pointing at the SAME fix from a different angle (ruling out spectral richness strengthens the case for
non-stationarity/trend as the real driver, rather than just being "the other untried option")._

### Escape Point

- **Should have been caught at:** `H-B3-1c`'s own Escape Point already flagged "run a goodness-of-fit
  check before trusting a parametric surrogate" — a quick check of whether the real series' rolling
  statistics show a trend visually consistent with a smooth SEASONAL ARC (not noise-like fluctuation)
  would have suggested testing V2' (detrend) before V1' (richer spectral null), potentially saving one
  full 25-minute compute cycle.
- **Guard to add:** before choosing between "richer stationary null" (V1') and "detrend first" (V2') as
  the next fix, plot or numerically characterize whether the real series' rolling-statistic trend looks
  smooth/monotonic (suggesting a real trend to remove) vs. noisy-but-persistent (suggesting genuine
  richer-noise structure) — this diagnostic is cheap and would have ordered these two experiments
  correctly instead of by "which is more standard in the literature."

### Why This Differs From Prior Null Results

`null_results/H-B3-1c-lakes-tda-ews-surrogate-null-v1.md` — same false-positive series, same magnitude
of Peter doSat lead. This experiment differs in DIAGNOSIS (rules out spectral richness as the fix,
narrows toward non-stationarity/trend) even though the observed outcome is nearly identical.

## Rescue Review (OSA)

| Branch | What Red Team killed | Whole branch dead? | Weaker formulation | Revival Condition | AOG risk | Final Status |
|---|---|---|---|---|---|---|
| H-B3-1d / H-B3-1c (surrogate-null detection, stationary-process class) | Stationary-linear-process null models (AR(1) AND IAAFT) as adequate for these real series | No | V2' (detrend-then-surrogate) | Re-run with detrended residual nulls; false-positive rate should drop meaningfully if a within-season trend was truly the driver | low — V2' is independently motivated by TWO failed stationary nulls, not invented ad hoc | `weak_alive` |

## What This Does NOT Mean

1. Does NOT mean IAAFT was a wasted experiment — ruling out "spectral richness" as the fix is real, useful information that sharpens the next hypothesis (V2').
2. Does NOT mean surrogate-testing in general is inappropriate for this problem — it means the surrogate must model the RIGHT kind of null (non-stationary-aware), not just a richer stationary one.
3. Does NOT change the standing of `H-B3-1`/`H-B3-1b` (CRITERION_INVALID) or `H-B3-1c` (REJECT) — both remain correct characterizations of what was tested there.
4. Does NOT establish that V2' will succeed — it is the best-motivated remaining candidate, not a guaranteed fix.

## Pearl Card Update

**Was the Prediction correct?** No — V1' predicted a meaningful false-positive reduction; the outcome was
statistically indistinguishable from V1's. **Falsification condition triggered?** Yes, identically to V1.
**New information:** the NEAR-IDENTITY of the two failures (not just "both failed" but "failed the same
way, on the same series, by similar magnitudes") is itself evidence favoring the non-stationarity
diagnosis over a residual "maybe a slightly richer null would still help" reading.
