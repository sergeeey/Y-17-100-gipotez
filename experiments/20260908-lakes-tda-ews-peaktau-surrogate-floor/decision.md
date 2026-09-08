# H-B3-1n — decision.md

## Result

500 AR(1) surrogates of Lower Zurich's real PC1 series (matched length/mean/variance/lag-1
autocorrelation, no real transition or mechanism by construction), scored with the exact
same window/embedding/peak-selection pipeline H-B3-1l used, transition date held fixed at
2002.0 across all surrogates.

| | value |
|---|---:|
| Real lead (TDA vs oracle-selected classical) | **+50.0 months** |
| Surrogate null: median | 6.5 |
| Surrogate null: mean | 5.07 |
| Surrogate null: std | 33.4 |
| Surrogate null: p05 | -54.0 |
| Surrogate null: p80 | 33.0 |
| Surrogate null: p95 | 61.0 |
| Surrogate null: max | 74.0 |
| **Percentile of real lead within null** | **90.4** |
| Fraction of surrogates matching/exceeding real lead | **9.6%** |

**Verdict: `INCONCLUSIVE_AT_THIS_SAMPLE_SIZE`**, exactly as the pre-registered thresholds
say it should be (80th < 90.4 <= 95th). Not the clean floor-artifact result the pearl's own
motivating hypothesis leaned toward, and not a clean survival either — genuinely
ambiguous, and reported as such rather than rounded to whichever side looks more
interesting.

### Bonus check — AC1-alone lead

`real_ac1_lead_months = -15.0` (AC1 peaks before TDA in the real data) sits comfortably
inside its own null distribution (median 1.0, p05=-64.0, p95=67.0) — **entirely
unremarkable relative to noise.** This confirms the skeptic's own qualitative read (AC1
beating TDA is not surprising) with a number: -15 is well within one AR(1)-surrogate
standard deviation of the null median, nowhere near either tail.

## What this changes about H-B3-1l

**H-B3-1l's `CONFIRMED` status needs a caveat it did not carry before.** The +50-month
lead is NOT solidly outside what mechanism-free noise, run through the exact same
peak-selection algorithm, produces on its own — 9.6% of surrogates equal or exceed it.
That is meaningfully weaker than "confirmed": a criterion that a null model clears roughly
1 time in 10 is closer to "plausible under noise" than "clearly discriminates signal." At
the same time, 90.4th percentile is not nothing either — it is above the noise median by a
wide margin (50 vs a median of 6.5), and the pre-registered 80th-percentile
floor-invalidity bar is NOT met, so this is not a repeat of H-B3-1m's clean
CRITERION_INVALID outcome.

**Correct characterization going forward:** the Lower Zurich TDA-vs-classical peak lead is
`[WEAK]` evidence, not `CONFIRMED` — present, moderately unusual relative to a proper
mechanism-free null, but not statistically decisive at n=500 surrogates. `graph.yaml`'s
H-B3-1l node should be updated to reflect this (see below) rather than left citing the
original CONFIRMED-without-caveat status, per the lab's own retroscan discipline (a new
result bearing on a `grounds`-linked prior node must revise that node in the same session).

## FL Step 0a / Mechanism Claim Gate

The skeptic's proposed mechanism ("argmax of expanding-window statistics is structurally
biased toward an earlier index for jumpier series like TDA") is NOT directly verified by
this experiment — this experiment tests the mechanism's PREDICTED CONSEQUENCE (large leads
from noise) without independently confirming the mechanism's own logic. Recorded as
`[UNTESTED-MECHANISM]`, consistent with claim.md's own scope limitation #3 — this
experiment settles the numeric question, not the causal explanation for why the algorithm
behaves this way.

## Kill Analysis

**What was killed:** the strong form of H-B3-1l's CONFIRMED verdict (implicitly, "the lead
is a real, discriminating signal") — it is not, at the 95th-percentile bar this experiment
pre-registered. **What was NOT killed:** the possibility that SOME real signal is present
alongside a large noise contribution — 90.4th percentile is above the noise median by a
substantial margin, not indistinguishable from typical noise the way H-B3-1m's 41-44%
floor-crossing rates were indistinguishable from a coin flip near a 50% threshold.

**Relaxation Map:**
- Run the same check on Windermere and Loch Leven (H-B3-1l's own negative controls) — if
  their real leads ALSO sit near the 90th percentile of their own surrogate nulls, that
  would suggest the ~90th-percentile-but-not-95th pattern is a generic property of this
  algorithm+data combination, not specific to Lower Zurich's claimed signal.
- Increase N_REPS (e.g. to 2000) to narrow the percentile estimate's own uncertainty —
  at 500 reps, the 90.4th percentile itself has sampling noise; a materially different
  percentile at higher N would change which side of the 80/95 bar this result should be
  read as leaning toward.

## What This Does NOT Mean

1. Does NOT prove the TDA peak-lead finding is a floor artifact — the pre-registered
   80th-percentile bar for CRITERION_INVALID was not met.
2. Does NOT prove the lead is genuine signal either — the pre-registered 95th-percentile
   bar for informative survival was not met.
3. Does NOT test Windermere or Loch Leven — Lower Zurich only, per claim.md's own scope.
4. Does NOT independently verify the skeptic's proposed early-index-bias mechanism — tests
   its numeric consequence only.

## Go/No-Go

**LEAD** (not REJECT, not CONFIRMED) — a genuine, informative, but not decisive result.
Reported honestly as inconclusive rather than forced toward either a REJECT or a
confirmation the data does not clearly support.

## Pearl Registry Update

Resolves the 2026-09-07 H-B3-1l pearl row's stated next step ("~5 minutes, machinery
ready") — done, result was genuinely uncertain (not the clean floor-artifact the pearl's
own framing anticipated), itself worth a note: a "cheap check" motivated by a plausible
mechanism does not always resolve cleanly, and reporting an honest INCONCLUSIVE is the
correct outcome, not a reason to keep pushing toward one side.
