# decision.md — 20260906-lakes-tda-ews-surrogate-null-v1

**Graph node:** `H-B3-1c` · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [x] **REJECT** — this IS a genuine REJECT, not a CRITERION_INVALID stop-verdict (see rationale)
- [ ] ARCHIVE

**Falsified statement:** *Replacing the fixed tau≥0.5 threshold with a per-series, per-timepoint
AR(1)-surrogate-null significance test (α=0.05) reduces the false-positive rate on the 4 known
negative-control lakes.* It does not: **5 of 5 negative-control series still false-positived**
(Windermere, Loch Leven, Paul chl/pH/doSat) — identical to the fixed-threshold outcome in kind, though
via a different mechanism (see Kill Analysis).

**Why REJECT and not CRITERION_INVALID this time:** `CRITERION_INVALID` applies when the criterion
itself cannot discriminate anything (a no-mechanism null passes it too easily). Here the criterion DOES
discriminate — `tests/test_surrogate_null_v1.py::test_self_consistency_ar1_surrogate_fires_near_nominal_alpha_not_near_certainty`
confirms a genuinely AR(1) series crosses its own null at a low rate, well below the 45–90% floor the
fixed threshold gave. The rule works AS DESIGNED. It fails here because its **input assumption is wrong**:
the real negative-control lakes are not adequately described by an AR(1) process. That is a substantive,
falsifiable finding about the data, not a defect in the test construction — hence REJECT with a proper
Kill Analysis, filed in `null_results/`.

## Evidence Summary

| Series | Role | Classical crossing | TDA crossing | False positive? |
|---|---|---|---|---|
| Lower Zurich | positive | none | 2000.08 | — |
| Windermere | negative | 1993.5 (var) | none | **yes** |
| Loch Leven | negative | 1999.67 (ac1) | 2002.33 | **yes** |
| Peter chl | positive | none | 270.0 | — |
| Peter pH | positive | 218.0 (var) | none | — |
| Peter doSat | positive | 185.0 (ac1) | 172.0 | — (+13 day TDA lead) |
| Paul chl | negative | none | 185.0 | **yes** |
| Paul pH | negative | 205.0 (ac1) | none | **yes** |
| Paul doSat | negative | 212.0 (ac1) | 182.0 | **yes** |

5/5 negative controls false-positive. 1/3 positive Peter Lake series (doSat) shows a TDA lead
(+13 days) that is at least directionally consistent — but with all negative controls also firing,
this cannot be distinguished from noise. `n_positive_cases_with_tda_lead = 1`, `n_false_positives = 5`.

## Kill Analysis (OSA, required for REJECT)

### What Was Killed

- **The AR(1) null-generation model as an adequate representation of "no real transition" for these
  specific real ecological negative-control series.** Confirmed self-consistent and well-calibrated on
  data that IS genuinely AR(1) (unit test); fails on data that only LOOKS AR(1) at the lag-1-autocorrelation
  level but has additional structure the fit does not capture.
- Specifically implicated structure NOT captured by AR(1): within-season trends unrelated to any
  regime shift (e.g. seasonal warming/cooling trajectories, nutrient depletion curves), possible
  heteroskedasticity (variance itself changing over the season), or higher-order autocorrelation
  (AR(2)+ or seasonal ARMA structure) — any of these would make a real series' own rolling-statistic
  trend exceed what a lag-1-only AR(1) surrogate would predict as "typical for noise."

### What Was NOT Killed

- [x] **The detection-rule MECHANISM itself** (per-series, per-timepoint percentile-of-surrogates
  significance testing) — validated as sound in principle by the self-consistency unit test. Only the
  specific null-generating model (AR(1)) was killed, not the surrogate-testing approach as a category.
- [x] **A1–A4** (embedding, window, statistic choices) — untouched by this experiment, unchanged from
  both parents.
- [x] **Peter Lake doSat's directional TDA lead (+13 days)** — not itself falsified; simply
  uninterpretable while every negative control also fires under the same rule.

### Relaxation Map (for surviving assumptions)

| Assumption | Modification | New Path | Known kill-evidence? | Cheapest test |
|---|---|---|---|---|
| Null-generating model (AR(1)) | **Replace**: phase-randomized (IAAFT) surrogate — preserves the FULL power spectrum and amplitude distribution of the real series, not just its lag-1 autocorrelation | V1': richer, assumption-light null | No | `statsmodels` or a hand-rolled IAAFT (FFT-shuffle-phase-inverse-FFT, iterate to match amplitude distribution); moderate new code, no new data needed |
| Null-generating model | **Weaken**: detrend each series (remove a low-order polynomial or seasonal fit) BEFORE AR(1) surrogate generation, so the surrogate targets residual noise, not raw structure | V2': detrend-then-AR(1) | No | Cheaper than V1' — a few lines added to `ar1_surrogate`'s caller |
| Detection target | **Remove** false-positive-rate-across-6-series as the pass bar; instead report each series' result independently with its own confidence, no aggregate PASS/FAIL | V3': descriptive reporting only, no binary verdict | No | Cheapest, but sacrifices the falsifiable claim entirely — least preferred |

_None have known kill-evidence; V1' (IAAFT) is the least circular — directly addresses the diagnosed gap
(AR(1) captures lag-1 correlation only) without assuming what "detrending" should remove._

### Escape Point

- **Should have been caught at:** `claim.md` pre-registration for V1 — the choice to reuse `ar1_surrogate`
  (already implemented for the floor check) was made for code-reuse convenience, not because AR(1) was
  independently justified as an adequate null model for THESE specific real series.
- **Why it wasn't:** the self-consistency test validated the RULE's mechanism, not whether AR(1) is a
  good MODEL for real lake/lake-manipulation data specifically — those are different questions, and only
  the first was checked before running.
- **Guard to add:** before adopting any parametric surrogate null (AR(1), ARMA, etc.) as adequate for a
  REAL dataset, run a goodness-of-fit check first (e.g., does the AR(1) residual still show significant
  autocorrelation at lag ≥2, or a trend the fit doesn't capture?) — this would have flagged the problem
  before spending the compute on the full 9-series run.

### Why This Differs From Prior Null Results

No prior entry in `null_results/INDEX.md` (this is the first genuine REJECT this repo has filed —
`H-B3-1`/`H-B3-1b` were `CRITERION_INVALID`, a different, non-REJECT outcome).

## Rescue Review (OSA)

| Branch | What Red Team killed | Whole branch dead? | Weaker formulation | Revival Condition | AOG risk | Final Status |
|---|---|---|---|---|---|---|
| H-B3-1c (surrogate-null detection, AR(1) specifically) | AR(1) as the null-generating model | No | V1' (IAAFT phase-randomized surrogate) | Re-run with IAAFT nulls; false-positive rate on all negative controls should drop meaningfully below 5/5 if AR(1) was truly the bottleneck | low — IAAFT is a strictly richer, better-justified null, not a rule invented post hoc to force a pass | `weak_alive` |

**AOG check (informal):** AOG-1 (pre-registered from theory): yes — IAAFT is standard surrogate-testing
practice (Theiler et al. 1992), not invented to save this claim. AOG-4 (non-triviality): yes — IAAFT
could still fail if the real structure is genuinely non-stationary in a way even a full-spectrum surrogate
can't capture (e.g. a real slow trend). Sufficient for `weak_alive`.

## What This Does NOT Mean

1. Does NOT mean surrogate-based significance testing is the wrong general approach — only that AR(1) specifically is too simple a null for these series.
2. Does NOT mean TDA fails to detect anything — Peter Lake doSat's +13-day lead is still on the table, just uninterpretable under a rule with 5/5 false positives elsewhere.
3. Does NOT mean H-B3-1/H-B3-1b's CRITERION_INVALID verdicts should be revisited — those remain correct characterizations of the fixed-threshold rule specifically.
4. Does NOT retroactively justify skipping the goodness-of-fit check named in the Escape Point for any future surrogate-based experiment.

## Pearl Card Update

**Was the Prediction correct?** No — V1 predicted a meaningful false-positive reduction; none was observed.
**Falsification condition triggered?** Yes, as pre-registered (`claim.md` MCID: "≤1/4 negative controls" was the bar; 5/5 negative firings is worse than even the no-improvement threshold).
