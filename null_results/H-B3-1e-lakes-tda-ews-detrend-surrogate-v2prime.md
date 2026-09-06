# decision.md — 20260906-lakes-tda-ews-detrend-surrogate-v2prime

**Graph node:** `H-B3-1e` · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [x] **REJECT** — third consecutive REJECT on the same binary metric, but with a qualitatively new,
  more troubling finding than V1/V1'
- [ ] ARCHIVE

**Falsified statement:** *Removing a smooth trend (moving-average, window=25% of series length) before
generating an IAAFT surrogate on the residual, then adding the trend back, reduces the false-positive
rate on the 5 negative-control series below V1/V1's 5/5.* It does not: **5 of 5 negative-control series
still false-positived — the EXACT SAME SET of series as V1 and V1'** (Windermere, Loch Leven, Paul
chl/pH/doSat), byte-for-byte identical across three structurally different null-generation methods.

## Evidence Summary

| Series | Role | V1 (AR(1)) FP? | V1' (IAAFT) FP? | V2' (detrend+IAAFT) FP? | Comment |
|---|---|---|---|---|---|
| Lower Zurich | positive | — | — | — | **NEW: gained a classical (var) crossing at 2001.5 + TDA at 1999.58 → lead +1.92y (~23mo)**, close to the original H-B3-1b raw finding (+24mo) before any surrogate-null was applied |
| Windermere | negative | **yes** | **yes** | **yes** | unchanged |
| Loch Leven | negative | **yes** | **yes** | **yes** | unchanged |
| Peter chl | positive | — | — | — | TDA crossing that existed under V1' (261.0) disappeared under V2' |
| Peter pH | positive | — | — | — | classical crossing shifted 201→219 (var), ac1 crossing disappeared |
| Peter doSat | positive | — | — | — | **LOST its TDA crossing (was 172.0, lead +13d under V1/V1') — now null, no TDA signal at all** |
| Paul chl | negative | **yes** | **yes** | **yes** | unchanged |
| Paul pH | negative | **yes** | **yes** | **yes** | unchanged |
| Paul doSat | negative | **yes** | **yes** | **yes** | lead 30→35→29 days across V1→V1'→V2', same sign throughout |

5/5 negative controls false-positive — **identical set across all three null-generation methods tested
so far.** `n_positive_cases_with_tda_lead = 1`, same count as V1/V1', but the series carrying it CHANGED
(Peter doSat → Lower Zurich).

## Why the Cross-Method Identity of the False-Positive Set Matters

Three structurally different null models (AR(1): matches lag-1 only; IAAFT: matches the full spectrum +
exact amplitude distribution; detrend+IAAFT: additionally removes a smooth low-frequency trend before
nulling) have now each produced **the exact same 5/5 false-positive set, on the exact same 5 series**.
This is stronger evidence than any single REJECT: whatever property makes Windermere/Loch Leven/Paul
chl/pH/doSat "look like a trend is present" to this detection rule is **robust to changing the null
model's assumptions about temporal structure** (autocorrelation depth, amplitude distribution, and now
low-frequency smoothness). That rules out a large class of candidate explanations at once.

## Escape-Point Gate Result: Synthetic PASSED, Real FAILED

`claim.md`'s own pre-registered synthetic mechanism check (run BEFORE this real compute) showed
detrend+IAAFT cutting the false-positive rate from 87.5% to 37.5% on a synthetic series built from a
smooth sine+linear trend plus AR(1) noise. **On the real data, false-positive count did not move at
all (5/5 → 5/5).** This is not a contradiction — `claim.md` explicitly flagged the synthetic check as
`[VERIFIED-SYNTHETIC]`, validating only that the FIX addresses the MODELED mechanism, not that the model
captures the REAL mechanism. The real negative-control lakes' "extra structure" is evidently NOT well
described by a smooth, low-frequency deterministic trend of the kind the synthetic check assumed —
otherwise a moving-average detrend at a plausible window would have helped at least partially.

## Kill Analysis (OSA, required for REJECT)

### What Was Killed

- **The hypothesis that a smooth low-frequency trend (moving-average removable, frac=0.25) is the
  dominant source of false positives on these 5 real negative-control series.** The synthetic analogue
  of this exact mechanism was fixed by detrending; the real series were not. This is a materially
  different (and stronger) kill than V1'/H-B3-1d's: it doesn't just fail to help, it fails to help
  DESPITE a working synthetic proof-of-concept for the SPECIFIC mechanism being targeted.
- **The general strategy "keep trying richer/different null models"** as applied to this population, at
  least for the three variants tried (AR(1), IAAFT, detrend+IAAFT). Three attempts, three null
  hypotheses about "what makes these lakes noisy," three failures on THE SAME series.

### What Was NOT Killed

- [x] **The per-series calibration mechanism** — still validated sound.
- [x] **A1–A4** — untouched.
- [x] **Lower Zurich's directional signal** — actually strengthened this round (now a full
  classical+TDA lead pair, ~23 months, consistent with the original pre-surrogate H-B3-1b finding).
- **New, sharper open question:** what property do Windermere, Loch Leven, and Paul (chl/pH/doSat)
  share that NONE of the three null models tested captures? Candidates not yet tested: (a) genuine
  heteroscedasticity (variance itself changes with season, not mean level — none of AR(1)/IAAFT/
  detrend-IAAFT explicitly model changing variance), (b) an abrupt but undocumented within-series shift
  that isn't a "trend" in the smooth sense at all, (c) these specific series are simply shorter/noisier
  in a way that inflates any Kendall-tau-based expanding-window statistic regardless of null model
  (Windermere n=244, Loch Leven n=152, Paul series n=334 — no obvious length pattern distinguishing them
  from the positive cases, so (c) is weakly supported at best).

### Relaxation Map (for surviving assumptions)

| Assumption | Modification | New Path | Known kill-evidence? | Cheapest test |
|---|---|---|---|---|
| Binary pass/fail framing itself | **Change the L0 question type**: stop asking "does TDA lead classical EWS, yes/no" (predictive, binary) and instead report the raw tau trajectories, lead times, and floor rates DESCRIPTIVELY for all 9 series, without a promote/reject binary gate | V3: descriptive-only reporting | Explicitly named as the last remaining candidate in `H-B3-1c`/`H-B3-1d`'s own Relaxation Maps | Reformat existing `metrics/run.json` outputs from all 4 experiments (H-B3-1, H-B3-1b, H-B3-1c, H-B3-1d, H-B3-1e) into one descriptive comparison table; no new compute needed |
| Null model class (temporal-structure-only nulls: AR(1)/IAAFT/detrend+IAAFT) | Model changing VARIANCE explicitly (e.g., a null with time-varying variance envelope matched to the real series' own rolling variance, keeping mean/autocorrelation structure simpler) | V4' (heteroscedastic null) | No — untested candidate, would require new code (rolling-variance-matched surrogate) | Moderate: write a new surrogate function; same rep counts, same compute cost as V1'/V2' |

**Recommendation:** switch to V3 (descriptive-only) before attempting a 4th null-model variant. Three
consecutive REJECTs with an IDENTICAL false-positive set is diminishing-returns evidence that the
binary-threshold framing itself, not the specific null model, is poorly matched to this population size
and noise level (Wang et al. 2023's own finding, already in this project's `pearl_registry`, that
classical EWS performs "no better than chance" on most observational lake data — this may be the same
limit, now demonstrated three times over for a TDA-augmented detector too).

### Escape Point

- **Should have been caught at:** the synthetic mechanism check validated ONE specific hypothesis about
  the real failure mode (smooth deterministic trend); it should have also tested at least one
  ALTERNATIVE synthetic mechanism (e.g., heteroscedastic noise with no trend at all) to see whether that
  alternative reproduces the real failure pattern better — this would have told us BEFORE the real run
  whether detrending was likely to be sufced, rather than after.
- **Guard to add:** before spending compute on a null-model variant, run the same escape-point check
  against ≥2 distinct candidate synthetic mechanisms (not just the one the new variant targets), and
  proceed with the real run only for the variant whose synthetic check is not ALSO explained equally
  well by leaving the null model unchanged.

## Rescue Review (OSA)

| Branch | What Red Team killed | Whole branch dead? | Weaker formulation | Revival Condition | AOG risk | Final Status |
|---|---|---|---|---|---|---|
| H-B3-1e / H-B3-1d / H-B3-1c (surrogate-null detection, binary threshold framing) | Three temporal-structure null models (AR(1), IAAFT, detrend+IAAFT), all producing the identical false-positive set | No, but heavily weakened for the SURROGATE-NULL approach specifically | V3 (descriptive-only, abandon binary framing) or V4' (heteroscedastic null, untested) | V3 requires no new compute — pure re-analysis; if it produces a genuinely informative descriptive comparison (e.g., Lower Zurich/Peter consistently distinguishable from Windermere/Loch Leven/Paul on SOME continuous measure even without a binary threshold), that's a viable PROMOTE path without ever fixing the binary detector | Low for V3 (reformatting existing data, no new false-positive risk); Medium for V4' (a 4th null-model attempt after 3 failures needs strong independent motivation, which heteroscedasticity has some but not overwhelming support for) | `weak_alive`, leaning toward V3 next |

## What This Does NOT Mean

1. Does NOT mean detrending as a technique is wrong in general — it worked exactly as predicted on the
   synthetic analogue of the mechanism it targets; the real lakes simply don't have THAT specific
   mechanism as their dominant structure.
2. Does NOT mean Lower Zurich's improved signal this round is more "real" than Peter doSat's signal
   under V1/V1' — both are single-series directional results uninterpretable against a 5/5
   false-positive backdrop, regardless of which null model produced them.
3. Does NOT change the standing of `H-B3-1`/`H-B3-1b` (CRITERION_INVALID), `H-B3-1c`/`H-B3-1d` (REJECT)
   — all remain correct characterizations of what was tested there.
4. Does NOT establish that V3 (descriptive-only) or V4' (heteroscedastic null) will succeed — they are
   the best-motivated remaining candidates, not guaranteed fixes.
5. Does NOT mean the bridge (`B3-MAY-TDA`) itself is dead — three failed DETECTOR variants is a finding
   about the STATISTICAL METHOD, not about whether TDA carries information about ecological regime
   shifts at all (Lower Zurich's persistent, strengthening directional signal across all 4 real-data
   experiments is a small but real hint the underlying idea has merit even if this detector doesn't).

## Pearl Card Update

**Was the Prediction correct?** No — V2' predicted a meaningful false-positive reduction on real data,
based on a synthetic mechanism check that itself succeeded; the real result was unchanged (5/5 → 5/5).
**Falsification condition triggered?** Yes. **New information:** (a) the false-positive SET is byte-
identical across 3 structurally different null models — a strong, generalizable methodological finding
in its own right; (b) a synthetic escape-point check passing is necessary but NOT sufficient evidence
that a real run will succeed — it only confirms internal consistency of the fix for the MODELED
mechanism, not that the model matches reality. This second point deserves its own pearl entry, distinct
from the surrogate-null-specific one.
