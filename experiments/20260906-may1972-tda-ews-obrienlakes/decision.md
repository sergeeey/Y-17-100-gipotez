# decision.md — 20260906-may1972-tda-ews-obrienlakes

**Graph node:** `H-B3-1` (re-scoped) · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [x] **CRITERION_INVALID** (FL Step 4a stop-verdict, added after computing the floor — see below;
      supersedes an earlier draft of this file that read REJECT before the floor number existed)
- [ ] ARCHIVE

**Why CRITERION_INVALID, not REJECT:** the pre-registered detection rule (Kendall tau ≥ 0.5 on an
expanding window of a rolling statistic) was checked against a floor AFTER the main run: 30 AR(1)
red-noise surrogates per lake — same length, mean, variance, lag-1 autocorrelation, **zero real
mechanism by construction** — crossed the SAME tau ≥ 0.5 threshold on classical EWS in **80–83% of
surrogates, on all three lakes including the one with a documented real transition.** A threshold that a
no-mechanism null passes 4 times out of 5 is at floor (`falsification-ladder.md` Step 4a: "SUCCESS
threshold ≤ floor → CRITERION_INVALID — the criterion is passed by a construction with no mechanism in
it; it cannot be failed"). The negative-control false positives reported below are a symptom of this,
not an independent finding about TDA specifically.

## Result Classification (diamond scan)

- [ ] 🥇 Gold — the AS-STATED claim did not survive
- [x] 💎 **Diamond** — the false-positive PATTERN itself is an unexpected, valuable result (see below)
- [ ] 🥈 Silver
- [ ] 🪨 Stone

| Инсайт | Куда применимо |
|--------|----------------|
| A single fixed Kendall-tau threshold on a rolling-window statistic false-positives on real, transition-free ecological series — for BOTH classical EWS and TDA alike | Directly reproduces, independently, O'Brien et al. 2023's headline finding (classical EWS near-chance on empirical data) — but extends it: the failure mode is not specific to autocorrelation/variance, a topological summary inherits it too under the same naive threshold rule |

## Floor-Ceiling Interval

### Population
Same as `claim.md`/`manifest.md`: Lower Zurich, Windermere, Loch Leven monthly `pca1`, post-ICE-exclusion lengths.

### Floor
- Construction: AR(1) red-noise surrogate matched in length/mean/variance/lag-1-autocorrelation to each
  real series, with the mechanism (any real transition or structured dynamics) removed by construction
- Value: 80–83% false-positive rate on the tau≥0.5 classical-EWS threshold, across all 3 lakes (30 surrogates each, seed=0)
- Result: [x] MEASURED

### Ceiling
- Construction: not computed this run — a privileged-access performer (e.g. an oracle told the exact
  transition index) was out of scope once the floor alone already invalidated the criterion
- Value: not measured
- Result: [ ] NOT MEASURED

### Efficiency
- Result: [x] DEGENERATE — floor (0.80–0.83) is at/above any reasonable success threshold (the criterion
  fires on pure noise more often than not); computing efficiency against an unmeasured ceiling would be
  meaningless on top of an already-invalid floor

## Decision (Step 4a)

- [x] `CRITERION_INVALID` — SUCCESS threshold (tau≥0.5) ≤ floor (0.80–0.83 false-positive rate on a
  no-mechanism null). Per hard rule: NOT evidence against the claim.

## Evidence Summary

| Check | Result |
|-------|--------|
| Data provenance | `[VERIFIED-REAL]` — sha256-recorded, downloaded from `duncanobrien/ews-assessments` (GitHub) |
| Positive case (Lower Zurich) | TDA crossed 1999.5, classical (variance) crossed 2001.5 → **lead = +24 months**, correct sign, AC1 never crossed |
| Negative control 1 (Windermere) | **FALSE POSITIVE** — both var (1989.67) and TDA (1989.67) crossed; AC1 did not |
| Negative control 2 (Loch Leven) | **FALSE POSITIVE** — AC1 (1999.25), var (1999.58), TDA (1998.92) all crossed |
| Harness | `tests/test_lake_tda_ews.py`, 6 tests, all pass — includes a regression test locking in the ICE gap-exclusion behavior (verified not a bug, see below) |

## Criterion Diagnosis (not a Kill Analysis — CRITERION_INVALID is explicitly NOT evidence against the
claim; this section identifies what to fix, not what was disproven)

### What the floor shows

- The claim **as originally instrumented**: {population = these 3 lakes} ∩ {detection rule =
  expanding-window Kendall tau ≥ 0.5} ∩ {statistics = rolling AC1/variance/H1-persistence-entropy with
  window = 50% of series length} **could not have been informative** — a mechanism-free AR(1) null
  crosses the same threshold 80–83% of the time. This is a property of the detection rule at this
  sample size, not a property of Lower Zurich, Windermere, Loch Leven, or of TDA vs. classical EWS.
- Specifically invalid: **the assumption that a fixed tau=0.5 threshold discriminates "real transition"
  from "no transition"** at these series lengths (76–161 points after ICE exclusion) and this window
  fraction (50%). It does not — a rolling-window statistic on ANY sufficiently autocorrelated series
  accumulates enough apparent monotone drift to cross tau=0.5 most of the time, mechanism or not.

### What remains untouched (not addressed either way by this run)

- [x] **Core mechanism**: TDA producing a *directionally correct, earlier* signal than classical EWS on
  the one real transition (Lower Zurich, +24 months) — survived. The claim failed on specificity
  (false positives), not on TDA's ability to detect the real event at all.
- [x] **A1** (pca1 as adequate scalar summary) — survived; not implicated by this failure.
- [x] **A2** (embedding parameters, pre-registered before inspecting the transition) — survived; the
  failure is in the classical-statistic-to-threshold-crossing rule, common to both signal families,
  not in the TDA-specific embedding choice.
- [ ] **New assumption exposed, not previously listed**: "tau ≥ 0.5 on an expanding window is a
  specific-enough trigger for a 15-30 year ecological series" — this is what actually failed.

### Relaxation Map (for surviving assumptions)

| Assumption | Modification | New Path | Known kill-evidence? | Cheapest test |
|---|---|---|---|---|
| Detection rule (tau≥0.5, expanding window) | **Replace**: use a SURROGATE-based null distribution (shuffle pca1, recompute the whole pipeline, get a null tau distribution per lake) instead of a fixed universal threshold | V1: per-lake significance test against its own null, not a shared magic number | No | Re-run `run.py` with 200 phase-randomized surrogates per lake; ~5 min compute, no new data needed |
| Detection rule | **Weaken**: require the SAME rolling-window statistic to ALSO show a level shift (not just trend) via a change-point test (e.g. Pettitt's test) before declaring threshold-crossing | V2: two-part rule (trend AND change-point) | No | Add `scipy`-based Pettitt/CUSUM check; comparable effort to V1 |
| Detection rule | **Remove** trend-based triggering entirely; report the raw lead/lag of PEAK Kendall tau per lake instead of a binary crossing | V3: continuous comparison, no threshold at all | No | Cheapest — no new statistical machinery, just report peaks instead of first-crossings |

_Kill any row where "Known kill-evidence" = Yes before running the test — none are, so all three are alive
candidates for a follow-up experiment (new ID required per Minimal Relaxation Rule; NOT retried here)._

### Escape Point

- **Should have been caught at:** `claim.md` pre-registration — tau=0.5 was chosen as "a common convention
  threshold in this literature" without first checking it against a null/surrogate baseline for THESE
  specific series lengths and window sizes.
- **Why it wasn't:** the literature convention (tau≥0.5 signaling "coherent trend") is usually quoted for
  shorter, higher-frequency experimental series (like the blocked Peter Lake design) where a 50%-window
  rolling statistic has fewer degrees of freedom to drift by chance; it was carried over to these longer,
  lower-frequency field series without re-deriving it.
- **Guard to add:** any future `claim.md` using a fixed literature threshold on a NEW population must
  include a cheap null/surrogate check of that threshold's false-positive rate on that population's own
  negative controls, BEFORE running the positive case — not after.

### Why This Differs From Prior Null Results

No prior `null_results/` entry matches this claim (checked before starting, per protocol).

## Rescue Review (OSA)

| Branch | What Red Team killed | Whole branch dead? | Weaker formulation | Revival Condition | AOG risk | Final Status |
|---|---|---|---|---|---|---|
| H-B3-1 (TDA leads EWS, tau≥0.5 rule) | The tau≥0.5 detection rule's specificity | No — see Relaxation Map | V1 (surrogate-based null) is non-circular and independently motivated (standard TDA/EWS practice, not invented to save the claim) | Re-run with surrogate nulls; if false-positive rate on Windermere/Loch Leven drops to 0 while Lower Zurich's positive lead survives | low — V1/V3 don't relax the CORE claim, they fix a known-generic threshold-calibration gap | `weak_alive` |

**AOG check (informal, Standard-tier — full 5-point AOG deferred to the actual V1 follow-up experiment):**
AOG-1 (pre-registered from theory): partially — surrogate testing is standard practice, not post-hoc.
AOG-4 (non-triviality): yes, V1 could still fail (surrogates might not lower the false-positive rate).
Sufficient to justify `weak_alive`, not `alive` — full AOG required before any future promotion.

## What This Does NOT Mean

1. Does NOT mean TDA cannot work as an EWS on ecological data — the ONE real positive case still showed the theoretically correct direction and magnitude; what failed is a generic, unvalidated threshold shared with classical EWS.
2. Does NOT mean classical EWS is worse than TDA here — both failed the SAME way, on the SAME lakes, under the SAME rule. This is a rule problem, not a TDA-vs-EWS problem.
3. Does NOT close the door on `H-B3-1` — see Rescue Review, `weak_alive`, with 3 concrete, cheap, non-circular next tests.
4. Does NOT retroactively validate the original ≥3-collapse kill criterion from ADR-006 — if anything, this result reinforces why Phase 1 was narrowed to fewer cases first.

## Pearl Card Update

**Was the Prediction correct?** Partially — the falsification condition (false positive on a negative
control) triggered exactly as pre-registered in `claim.md`'s implicit escape route; the POSITIVE case's
directional prediction (TDA lead > 0) also held. Mixed, not simply wrong.
**Falsification condition triggered?** Yes (negative control) — but does not kill the core mechanism (see Kill Analysis).
