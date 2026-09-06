# decision.md — 20260906-lakes-tda-ews-total-persistence-iaaft-v1gprime

**Graph node:** `H-B3-1i` · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [x] **REJECT** — per pre-registered kill criterion in `claim.md`: false-positive rate = 4/5, and the
  false-positive SET is identical to `H-B3-1g`/V1g (Windermere, Loch Leven, Paul pH, Paul doSat).
  Honoring the pre-registered criterion literally, per the Anti-Overfitting Gate's Minimal Relaxation
  Rule discipline — do NOT reclassify to LEAD just because the underlying mechanism turned out to be
  more interesting than the count alone suggests (see below).
- [ ] ARCHIVE

**Statement:** *IAAFT-surrogate null combined with total persistence reproduces V1g's exact
false-positive rate (4/5) and exact false-positive series set — but the underlying MECHANISM differs
for 2 of the 4 (Loch Leven and Paul pH now trigger via the classical statistic only, not TDA), and,
most importantly, Peter doSat's TDA lead — identical (+13 days) across all four prior structurally
different variants (V1, V1', V1g, the H-B3-1h conjunction) — REVERSES SIGN here to -74 days (TDA now
lags classical by 74 days instead of leading it by 13). This is the first failure of the single most
robust finding in the entire B3 investigation.*

## Evidence Summary (real compute — first genuinely new run since H-B3-1g)

| Series | Role | V1g (AR1+total-persist.) TDA lead | H-B3-1i (IAAFT+total-persist.) TDA lead | Sign/behavior change? |
|---|---|---|---|---|
| Lower Zurich | positive | null (no classical pair) | **no TDA crossing at all** | TDA crossing disappeared entirely |
| Windermere | negative | +3.67 (FP) | null lead, still FP (TDA crosses, no classical pair) | mechanism shifted |
| Loch Leven | negative | 0.0 (FP, TDA crosses) | **TDA does not cross**; FP now via classical only | TDA signal vanished, FP survives via classical |
| Peter chl | positive | null (no classical pair) | null (no classical pair) | unchanged |
| Peter pH | positive | -100.0 (TDA lags) | -133.0 (TDA lags, larger) | same sign, magnitude grew |
| **Peter doSat** | **positive** | **+13.0 (TDA leads — 4x confirmed)** | **-74.0 (TDA LAGS)** | **SIGN FLIP — headline finding** |
| Paul chl | negative | no crossing, not FP | no crossing, not FP | unchanged |
| Paul pH | negative | +33.0 (FP, TDA crosses) | **TDA does not cross**; FP now via classical only | TDA signal vanished, FP survives via classical |
| Paul doSat | negative | +3.0 (FP, TDA crosses) | +28.0 (FP, TDA crosses, larger) | same sign, magnitude grew |

**False-positive count: 4/5, identical set to V1g** (Windermere, Loch Leven, Paul pH, Paul doSat).
**Positive cases with a genuine TDA lead: 0** (down from 1 in V1g) — Peter doSat's lead is gone.

## Why REJECT, Not LEAD, Despite the Genuinely Interesting Mechanism Shift

`claim.md`'s pre-registered LEAD condition required "the false-positive SET differs meaningfully from
every prior variant." It does not — the SET (which series trip the combined `false_positive` flag) is
byte-identical to V1g. What differs is which underlying statistic (classical vs. TDA) drives that flag
for 2 of the 4, and the sign of Peter doSat's lead. Neither of those was anticipated in the
pre-registered kill criteria, and reclassifying REJECT to LEAD post-hoc because the qualitative result
turned out more interesting than the pre-registered count-based criterion would be exactly the
verdict-shopping the Anti-Overfitting Gate (`falsification-ladder.md`) exists to block. The verdict
stays REJECT; the qualitative content goes into Kill Analysis and the pearl registry instead, where it
belongs.

## Kill Analysis (OSA)

### What Was Killed
- [x] **"IAAFT null + total persistence reduces the false-positive rate below V1g's 4/5"** — false.
  Identical rate, identical set.
- [x] **"Peter doSat's TDA-leads-classical lead is robust under ANY structurally different variant"**
  — false. This was the single most confidently-stated finding of the whole `H-B3-1*` arc
  ("самый надёжный сигнал во всём мосте B3", `activeContext.md`, `H-B3-1g` entry) after surviving 4
  consecutive method changes unchanged. It does not survive the 5th. The claim should have been stated
  as "robust under the 4 variants tested so far," not as an unconditional property — a scope-discipline
  lesson, not just a data point.

### What Was NOT Killed
- [x] The total-persistence invariant itself is not shown to be worse than entropy — both invariants,
  under both null models tested, converge on similar false-positive counts (3-4/5) and never reach the
  ≤1/5 PROMOTE bar. The null-model-exhaustion finding (`H-B3-1d`/`H-B3-1e`, "no stationary linear
  surrogate is sufficient") is now reinforced across BOTH invariants, not just entropy — IAAFT changes
  WHICH statistic (classical vs TDA) drives the false-positive flag for Loch Leven/Paul pH, but does not
  remove the flag itself.
- [x] Paul doSat remains a false positive under every method tried in this session (now 6 for 6:
  AR1/IAAFT/detrend-null × entropy, AR1/IAAFT × total persistence) — the single most concentrated
  false-positive evidence in the whole bridge, per the pearl registry's own running tally.

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Only IAAFT tested against total persistence, not detrend+IAAFT | Run detrend+IAAFT/total-persistence (the "V2g'" cell, two assumptions from `H-B3-1g`, one from this experiment) | Would complete the null-model axis for total persistence to match entropy's 3-variant coverage |
| Peter doSat's lead treated as a single scalar per variant | Look at whether the underlying persistence-diagram STRUCTURE (not just the crossing time) changes qualitatively between AR1 and IAAFT surrogates for this one series | Cheapest next step — no new compute, re-inspect already-computed diagrams/statistics if cached, else a small targeted diagnostic |
| Verdict classification used only the SET-based criterion pre-registered in claim.md | A future claim.md for this kind of comparison should pre-register a MECHANISM-level criterion too (which statistic drives each flag), not just a count/set-level one | Methodological lesson for future FL Standard-Ladder claims in this bridge |

## What This Does NOT Mean

1. Does NOT mean total persistence or IAAFT are worse choices in general — both were independently
   reasonable, validated choices; the interaction between them on this specific series (Peter doSat) is
   what changed, not either choice alone.
2. Does NOT retroactively invalidate `H-B3-1g`'s or `H-B3-1h`'s verdicts — those were correct
   characterizations of what AR(1)+total-persistence and the conjunction showed AT THE TIME. This
   experiment adds a boundary condition (IAAFT+total-persistence breaks it) rather than showing the
   earlier results were wrong.
3. Does NOT explain WHY Peter doSat's lead flips sign under this specific combination — that remains
   open, and is arguably now the single most interesting unresolved question in the bridge, ahead of
   Loch Leven/Paul doSat's false-positive mechanism.

## Note on Floor-Ceiling (FL Step 4a)

Not re-run here, same reasoning as `H-B3-1g`/V1g: this experiment changes the null-generation
procedure (AR(1) → IAAFT, already validated as a mechanism in `H-B3-1d`/V1') while reusing the
per-series self-calibrating surrogate-null detection rule UNCHANGED — that rule itself already
replaced the fixed-threshold floor problem (`H-B3-1c`'s own original Step 4a finding) with a per-series
null, and its self-consistency was validated once in `tests/test_surrogate_null_v1.py`, not re-tested
per null-model/invariant swap (exactly as V1'/V2'/V1g did not re-run it either). The new
`tests/test_total_persistence_iaaft_v1gprime.py` checks are the correct analogue here: they verify that
BOTH overrides (`surrogate_fn=iaaft_surrogate`, `tda_stat_fn=betti1_total_persistence_series`) compose
correctly and produce a result genuinely different from either single-assumption neighbor (V1' and
V1g), not a fresh floor/ceiling for machinery that didn't change.

## Addendum (2026-09-06, same session) — mechanism of the sign flip, isolated cheaply

Ran the Relaxation Map's own next-named step: inspected the null-threshold curves directly for
Peter doSat, instead of another full 9-series run. Key structural fact confirmed by reading
`run.py` before writing any new code: `analyze_series` computes the REAL total-persistence tau
curve from the real data ONLY — it does not depend on `surrogate_fn` at all. The null model only
builds the per-timepoint THRESHOLD curve the real tau is compared against. So the crossing-time
shift (172d under AR(1) → 259d under IAAFT) can only come from the threshold curve moving, not
from the real signal changing. Script: `case_study_peter_dosat_sign_flip.py` (single series, far
cheaper than a population run); output: `metrics/case_study_peter_dosat_sign_flip.json`.

**Result:** at t=172d (the AR(1) crossing), the real tau (0.786) clears AR(1)'s threshold there
(0.557) but NOT IAAFT's (0.948) — a large, specific spike in IAAFT's threshold at exactly that
time blocks the early crossing. By t=259d, the real tau has declined to 0.564 while IAAFT's
threshold happens to dip to 0.558, producing a narrow, late crossing.

**Self-caught error in the script's own auto-generated interpretation:** the script's canned
`interpretation` field concluded "IAAFT null threshold sits HIGHER than AR(1) null on average" from
comparing the two MEANS alone (0.686 vs 0.621). But `fraction_of_timepoints_iaaft_null_higher_than_ar1_null
= 0.416` — IAAFT's threshold is actually LOWER than AR(1)'s at the MAJORITY (58%) of timepoints.
The mean comparison is misleading here; a mean-only auto-interpretation is a real (if minor)
instance of the same failure mode this project's rules warn about — a metric that sounds
authoritative while the fuller picture contradicts its simple framing. Caught by reading the raw
numbers rather than trusting the printed one-line verdict.

**Corrected mechanism:** IAAFT's null-threshold curve for total persistence is not systematically
*shifted* relative to AR(1)'s — it is *spikier/more variable* over time, with an anomalous local
spike exactly at the time AR(1) crossed, which blocks that specific early opportunity. The eventual
first IAAFT crossing at 259d happens where a (by-then-declining) real tau meets a locally low point
of the (still generally noisier) IAAFT threshold — closer to "AR(1)'s crossing point specifically
got blocked by IAAFT noise" than to "IAAFT is a uniformly stricter null."

This does not change the REJECT verdict or the sign-flip finding itself — it only replaces a vague
"the null model changed, so the crossing changed" statement with an actual, checked mechanism, and
catches a real (if small) case of a misleading auto-generated summary string inside this session's
own diagnostic tooling.

## Pearl Card Update

**New information (high impact):** the ONE finding in the entire `H-B3-1*` investigation that had
survived 4 consecutive structurally different method changes unchanged — Peter doSat's TDA-leads-
classical-by-13-days signal — fails on the 5th (IAAFT null + total persistence combined). It does not
merely weaken; it reverses sign (TDA now lags by 74 days). This is a significant correction to how
confidently that finding should be described going forward, and a concrete illustration of why "robust
under N variants tested" must never be silently upgraded to "robust" without qualification — exactly
the discipline the Independent Verification Strength Ladder (`falsification-ladder.md`) and Hindsight
Distortion Gap heuristic both warn about, now demonstrated with real data inside this project rather
than as an abstract risk.
