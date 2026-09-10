# decision.md — 20260910-lakes-tda-ews-crossvar-coherence-h3-1q

## Verdict: **CONFIRMED-CROSSVAR-COHERENCE-LEAD** (floor-checked; explicitly `LEAD`, not `PROMOTE`)

## Result Summary (`metrics/run.json`)

| Lake | var1-var2 | ρ (unaligned) | p | n |
|---|---|---|---|---|
| Peter (positive) | chl-pH | +0.713 | <1e-25 | 161 |
| Peter (positive) | chl-doSat | +0.818 | <1e-39 | 161 |
| Peter (positive) | pH-doSat | +0.841 | <1e-43 | 161 |
| Paul (negative) | chl-pH | -0.337 | <1e-4 | 161 |
| Paul (negative) | chl-doSat | +0.375 | <1e-6 | 161 |
| Paul (negative) | pH-doSat | -0.906 | <1e-60 | 161 |

**Peter: 3/3 pairs positive (0.71-0.84). Paul: 1/3 positive, signs mixed, including a STRONG
negative (-0.91) — the opposite of the pattern a construction-only artifact would produce (which
would show up equally at both lakes).** Floor check PASSES.

## H-B3-1o's own original revival condition — attempted, stays inconclusive

- Unaligned pH-vs-doSat (Peter): ρ=0.8407, n=161
- Aligned (shift=147 days to match stored crossing dates): ρ=0.6176, n=14 — **below the
  pre-registered minimum overlap (30 points)**, and LOWER than the unaligned value
- **`conclusive: false`** — this experiment does NOT resolve H-B3-1o's own delay-vs-artifact
  question. `H-B3-1o` stays `parked`. The aligned-lower-than-unaligned pattern mildly disfavors
  the "genuine delay, same shape shifted" reading, but n=14 is too small to trust as a verdict.

## Mandatory checks against claim.md's own Kill Criterion

- [x] Peter: all 3 pairs positive — **PASS**
- [x] Paul: NOT consistently positive (1/3, mixed signs) — **PASS**
- [x] Sample-size caveat stated explicitly, not glossed over — **PASS** (`n=1` lake-pair,
  3 non-independent within-lake comparisons — `sample_size_caveat` field in `metrics/run.json`)
- [x] Original H-B3-1o question honestly reported as unresolved, not silently answered — **PASS**

## Interpretation

This is real, floor-tested signal — the pattern discriminates cleanly on the ONE lake-pair this
dataset provides, and the direction (construction-artifact-proof, since Paul does NOT show the
same pattern) rules out the most obvious alternative explanation. But the effective sample size is
genuinely small: **one manipulated lake, one reference lake, three within-lake variable pairs that
are not independent replicates** (all three derive from only three underlying series). This is
exactly a `LEAD` situation per this session's own established discipline (the H9-A overclaim
correction earlier this session made the same distinction: a clean-looking pattern with a small
effective sample is a lead worth recording, not a result ready to promote). A genuine test would
need multiple independent manipulation-vs-reference lake pairs, which the available datasets in
this project do not currently provide (O'Brien lakes has only one variable per lake).

**What this contributes to the B3 arc, honestly:** every single-series threshold-crossing approach
this arc tried (H-B3-1c through 1m) floor-failed on real negative-control lakes. This is the FIRST
approach in the whole B3 arc whose floor check (Paul) actually passes cleanly, on a genuinely
different statistic (cross-variable coherence, not single-series threshold-crossing). That is worth
recording even at `LEAD` status — it names a class of statistic (multi-variable coherence, not
per-series thresholds) that this arc had not tried before, as a candidate for future work if this
bridge is ever revisited with more lake systems.

## FL Step 8a — Independent Reviewer

Standard-tier claim, but the pattern (clean floor-check pass after 9+ prior floor-check FAILURES in
the same arc) is surprising enough (skeptic-triggers.md Trigger 2: success rate far exceeds this
arc's own prior base rate) to warrant an independent check despite the tier. Context-asymmetric:
reviewer given `claim.md` + `run.py` only, no reasoning chain. Scoped narrowly: independently
recompute the 6 pairwise correlations (3 Peter, 3 Paul) from scratch, confirm the sign pattern
(Peter 3/3 positive, Paul not consistent) and the two headline numbers (Peter pH-doSat=+0.84, Paul
pH-doSat=-0.91).

**Verdict: CONFIRMED-REAL.** Reviewer computed all 6 tau-trajectories independently and correlated
them with TWO independent methods (scipy's `spearmanr` AND a hand-written rank-transform + Pearson
computation) — not calling this experiment's own `unaligned_correlation` function.

| Lake | Pair | manual ρ | scipy ρ | committed ρ |
|---|---|---|---|---|
| Peter | chl-pH | 0.712980 | 0.712980 | 0.712980 |
| Peter | chl-doSat | 0.817863 | 0.817863 | 0.817863 |
| Peter | pH-doSat | 0.840723 | 0.840723 | 0.840723 |
| Paul | chl-pH | -0.337445 | -0.337445 | -0.337445 |
| Paul | chl-doSat | 0.375086 | 0.375086 | 0.375086 |
| Paul | pH-doSat | -0.905705 | -0.905705 | -0.905705 |

All 6 values match to full float precision, both manual and scipy implementations agree with each
other (ruling out a scipy-specific artifact), and the sign pattern (Peter 3/3 positive, Paul not
consistent) is confirmed. Reviewer explicitly noted this is an artifact-verification check only —
it does not adjudicate the `n=1`/LEAD-not-PROMOTE caveat, which claim.md already states correctly.

## Skeptic Concerns

No `[FALSIFIED]` concerns raised. Reviewer's independent dual-method computation matched exactly —
no dismiss/accept/mitigate entries needed.

## Caveats / What This Does NOT Mean

Per claim.md's own "What This Does NOT Mean" section — unchanged and reaffirmed:

1. Does NOT resolve H-B3-1o's own original question — stays `parked`.
2. Does NOT claim usual multi-replicate statistical significance — `n=1` lake-pair.
3. Does NOT generalize beyond this dataset.
4. Does NOT re-open or contradict the B3 arc's own prior REJECT verdicts — different statistic.

## MCID

Not formally applicable (`n=1`) — the qualitative bar (clean floor-check separation) is met.
