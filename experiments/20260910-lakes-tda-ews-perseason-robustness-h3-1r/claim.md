# claim.md — 20260910-lakes-tda-ews-perseason-robustness-h3-1r

**Graph node:** `H-B3-1r` (bridge `B3-LAKES-TDA-EWS`) · **Tier:** Standard
**Parent:** `H-B3-1q` (cross-variable tau-trajectory coherence, `LEAD`). Direct robustness check under
consolidation-phase priority item 2 ("B3-1q external-data search"): while searching for additional
independent manipulation-vs-reference systems to move beyond `n=1` lake-pair, found that the
EXISTING local data (`squealSondesMet_08to11_forOPUS.csv`, already used by H-B3-1g/1o/1q) spans 4
field seasons (2008-2011) with a `year` column, but `peter.load_daily_series` POOLS 2008-2010 onto
one continuous `season_time` axis before H-B3-1q's own tau-trajectory computation runs. This
experiment asks the natural, cheap robustness question the pooling choice raises: **does H-B3-1q's
own cross-variable coherence pattern hold when computed SEPARATELY per season, instead of pooled?**

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Comparing a statistical pattern (cross-variable correlation sign
consistency) across sub-periods of already-used real data. Not causal, not a new estimate of the
underlying ecological effect.

## Origin and design rationale

**Compute-First Check (BEFORE any formal artifact):** computed the SAME cross-variable
tau-trajectory correlations H-B3-1q reports, but SEPARATELY for each of the 3 seasons Carpenter et
al. 2011's own bass-manipulation experiment spans (2008, 2009, 2010), instead of pooling them onto
one `season_time` axis:

```
2008: Peter 1/3 positive (chl-pH=-0.24, chl-doSat=-0.15, pH-doSat=+0.23)
      Paul  1/3 positive (chl-pH=+0.83, chl-doSat=-0.82, pH-doSat=-0.98) -- ties Peter on
      the sign-count metric, though its two negative pairs have much larger magnitude
2009: Peter 3/3 positive (chl-pH=+0.84, chl-doSat=+0.59, pH-doSat=+0.75) -- matches H-B3-1q's pooled pattern
      Paul  1/3 positive, mixed (chl-pH=-0.73, chl-doSat=-0.38, pH-doSat=+0.72)
2010: Peter 2/3 positive (chl-pH=-0.40, chl-doSat=+0.52, pH-doSat=+0.21) -- the food-web transition
      COMPLETES this year (day 230/2010, Carpenter et al. 2011 p.3) -- yet Peter's own count is
      LOWER here than in 2009 (2 vs 3), not higher
      Paul  0/3 positive, all weak (chl-pH=-0.17, chl-doSat=-0.19, pH-doSat=-0.03)
```

**Only 2009 and 2010 show Peter strictly more consistent than Paul (by sign-count); 2008 TIES
(1 positive pair each, failing the strict "Peter more consistent" bar), and Peter's own count
DROPS from 2009 to 2010 (3→2) rather than strengthening toward the documented transition-completion
year — the opposite of what a signal that intensifies as the transition completes would predict.**

**Minimal Relaxation Rule compliance:** ONE change relative to H-B3-1q — computing the tau
trajectory per-season instead of pooled across seasons. Same underlying data, same statistic
(`betti1_total_persistence_series` + `expanding_kendall_tau`), same correlation test.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "If H-B3-1q's own pooled cross-variable coherence pattern reflects a
genuine, season-independent tracking of the real ecological transition (rather than an artifact of
concatenating 3 field seasons onto one smooth expanding-window timeline), the SAME
positive-at-Peter/inconsistent-at-Paul pattern should hold, or strengthen, when each season is
analyzed independently — especially in 2010, when the transition is documented as completing.
Finding only a TIE (not a Peter-favoring result) in 2008 and a WEAKER (not stronger) Peter count in
2010 than in 2009 argues that pooling itself — not a genuine within-season ecological coherence
that intensifies as the transition completes — may be substantially responsible for H-B3-1q's own
reported pooled pattern."

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 3 pairwise cross-variable tau-trajectory correlations H-B3-1q reports, computed separately per field season (2008, 2009, 2010) instead of pooled |
| **Falsifiable predicate** | Does the Peter-positive/Paul-inconsistent pattern replicate in EVERY season, or at minimum strengthen toward the transition-completion year (2010)? |
| **Measurable outcome** | Per-season, per-lake: 3 pairwise correlations, count positive, sign consistency |

## Kill Criterion (set BEFORE the formal artifact — Compute-First already ran)

- **H-B3-1q's own pattern REPLICATES (per-season robustness CONFIRMED) if:** ALL 3 seasons show
  Peter more consistently positive than Paul, with the pattern strengthening or at least stable
  toward 2010.
- **H-B3-1q's own pattern does NOT replicate (REJECTED for season-robustness) if:** any season
  shows the OPPOSITE pattern (Paul more consistent than Peter), or the pattern weakens rather than
  strengthens toward the transition-completion year.
- **RESULT (from Compute-First, to be formally locked in): REJECTED for season-robustness.** 2008
  ties rather than favoring Peter; 2010's Peter count (2/3) is lower than 2009's (3/3), not higher,
  despite 2010 being the documented transition-completion year. This does NOT retroactively invalidate
  H-B3-1q's own pooled numbers (those are real, correctly computed, and remain in
  `metrics/run.json`) — it substantially weakens confidence that the pooled pattern reflects a
  genuine, season-independent ecological coherence signal rather than being partly (or largely) an
  artifact of pooling multiple seasons onto one continuous timeline before computing an
  expanding-window statistic (a known general confound: expanding-window/cumulative statistics
  computed across concatenated periods can pick up shared multi-period drift structure that has
  nothing to do with any single period's own dynamics).

## What This Does NOT Mean

1. Does NOT invalidate H-B3-1q's own pooled correlation NUMBERS — those remain real, computed
   correctly, independently reviewer-verified. This experiment weakens the INTERPRETATION (does
   pooled coherence track a genuine transition-related signal), not the arithmetic.
2. Does NOT prove pooling is definitely the sole cause of H-B3-1q's own pattern — with only 3
   seasons (small n itself), the per-season results could also reflect genuine but
   season-to-season-variable ecological dynamics, not purely a pooling artifact. Both explanations
   remain plausible; this experiment cannot fully distinguish them with only 3 data points.
3. Does NOT resolve H-B3-1o's own original delay-vs-artifact question — unrelated, stays `parked`.
4. Does NOT claim this dataset is exhausted — a genuinely different, independent lake-pair system
   remains the real fix for the small-sample limitation, not attempted here.

## MCID

Not formally applicable (`n=3` seasons) — qualitative bar: does the pattern replicate across all 3
seasons and strengthen toward transition completion? It does not.
