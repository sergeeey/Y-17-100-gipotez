# decision.md — 20260910-lakes-tda-ews-perseason-robustness-h3-1r

## Verdict: **REJECTED-FOR-SEASON-ROBUSTNESS**

## Result Summary (`metrics/run.json`)

| Season | Peter n-positive/3 | Paul n-positive/3 | Peter more consistent? |
|---|---|---|---|
| 2008 | 1 | 1 | **No — tie** |
| 2009 | 3 | 1 | Yes |
| 2010 (transition completes) | 2 | 0 | Yes, but **lower than 2009** |

**H-B3-1q's own pooled pattern (Peter 3/3, Paul mixed/inconsistent) does NOT replicate cleanly
across the 3 individual field seasons it was computed from.** 2008 fails the "Peter more
consistent" bar outright (ties Paul). 2009 alone matches the pooled pattern exactly. 2010 — the
season in which Carpenter et al. 2011's own documented food-web transition actually COMPLETES
(day 230/2010) — shows a WEAKER Peter count than 2009, the opposite of what a signal genuinely
tracking transition intensity should show.

## Mandatory checks against claim.md's own Kill Criterion

- [x] Pattern replicates in ALL 3 seasons — **FAILS** (2008 ties)
- [x] Pattern strengthens toward 2010 — **FAILS** (2010 < 2009: 2 vs 3)
- Verdict: `REJECTED-FOR-SEASON-ROBUSTNESS`, exactly as the Compute-First Check predicted

## Kill Analysis (Anti-Overfitting Gate, mandatory for REJECT)

**What this KILLS:** the specific interpretation that H-B3-1q's own pooled cross-variable
coherence pattern reflects a genuine, season-independent signal that tracks (and should intensify
with) the real, documented ecological transition. That specific reading is REJECTED — the
per-season decomposition does not support it.

**What this does NOT kill:**
1. **H-B3-1q's own pooled correlation NUMBERS** — those remain correctly computed, independently
   reviewer-verified (two independent methods, exact match). This experiment does not recompute or
   challenge the arithmetic, only the INTERPRETATION of what that arithmetic means.
2. **The floor-check contrast itself** (Peter vs Paul, pooled) — Peter's pooled numbers ARE more
   internally consistent than Paul's pooled numbers, on the pooled data. What's now in question is
   WHY — genuine ecological coherence, vs. a pooling-induced artifact (concatenating 3 seasons onto
   one continuous expanding-window timeline can create shared multi-season drift structure across
   variables that has nothing to do with within-season ecological coupling).
3. **H-B3-1o's own original question** — unrelated, unaffected, stays `parked`.

**Relaxation Map (surviving directions):**
- Could the season-to-season VARIABILITY itself (not a monotonic trend) be informative — e.g., is
  2009's clean 3/3 pattern itself meaningful (the year EWS theory itself flags as when warning
  signals were "evident... more than a year before" transition completion, per Carpenter et al.
  2011's own abstract) even though 2008 and 2010 don't extend it monotonically? NOT tested here —
  would require a dedicated follow-up asking specifically about 2009's own role, not attempted in
  this cycle.
- Could a LONGER per-season window (more days per season, requiring a different
  `WINDOW_FRAC`/embedding choice tuned for the shorter ~107-114-day per-season series rather than
  the pooled ~340-day series) change the per-season results? Not tested — the SAME window-fraction
  parameter was deliberately kept unchanged (Minimal Relaxation Rule) to isolate exactly ONE
  variable (pooled vs per-season), not conflate it with a second change.

## Interpretation

This is the honest, disciplined outcome of running a robustness check the pooling design choice in
H-B3-1g/1o/1q itself invited, rather than treating H-B3-1q's own clean floor-check result as
sufficient on its own. Per this session's own Anti-Overfitting Gate and immediate-retroscan
principle, H-B3-1q's own `graph.yaml` status/evidence is updated in the SAME session to reflect
this finding (see registration below) — not deferred.

## FL Step 8a — Independent Reviewer

Standard-tier claim, but directly retroscans (weakens confidence in) an already-`lead` sibling
claim (H-B3-1q) in the same session — mandatory per FL Step 8a and the null-retroscan principle.
Context-asymmetric: reviewer given `claim.md` + `run.py` only, no reasoning chain. Scoped narrowly:
independently recompute the 2009 Peter pH-doSat correlation (the single number that most directly
matches H-B3-1q's own pooled headline number) AND the 2010 Peter chl-pH correlation (the number
whose sign flip vs 2009 is most load-bearing for the "does not strengthen toward 2010" conclusion).

**Verdict: CONFIRMED-REAL.** Reviewer wrote fully independent data-loading and correlation logic
(not calling this experiment's own `daily_series_for_season`/`tau_for_season`/
`unaligned_correlation` functions), reading the CSV directly and importing only the shared
primitives (`betti1_total_persistence_series`, `expanding_kendall_tau`, `WINDOW_FRAC`, `EMBED_DIM`,
`EMBED_DELAY`).

| Target | Committed | Independently recomputed |
|---|---|---|
| Peter, 2009, pH-doSat | ρ=0.746878 | ρ=0.746878, p=3.1e-10, n=51 |
| Peter, 2010, chl-pH | ρ=-0.395385 | ρ=-0.395385, p=4.1e-3, n=51 |

Both match to 6 decimal places, **including the negative sign on the 2010 chl-pH value** — the
single specific data point that drives this experiment's "does not strengthen toward 2010"
conclusion. Window computation, `n_daily` (114 for 2009, 113 for 2010), and τ-trajectory lengths
(n=51 aligned points both) all reproduce independently.

## Skeptic Concerns

No `[FALSIFIED]` concerns raised. Reviewer's independent recomputation matched exactly, including
the sign-critical 2010 value — no dismiss/accept/mitigate entries needed.

## Caveats / What This Does NOT Mean

Per claim.md's own "What This Does NOT Mean" section — unchanged and reaffirmed:

1. Does NOT invalidate H-B3-1q's own pooled correlation numbers.
2. Does NOT prove pooling is definitely the SOLE cause — n=3 seasons is itself too small to fully
   distinguish "pooling artifact" from "genuine but season-variable ecological dynamics."
3. Does NOT resolve H-B3-1o's own original question.
4. Does NOT claim this dataset is exhausted — a genuinely independent lake-pair system remains the
   real fix for the small-sample limitation.

## MCID

Not formally applicable (`n=3` seasons) — qualitative bar (replicate + strengthen toward 2010) not met.
