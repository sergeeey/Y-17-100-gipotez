# claim.md — 20260910-lakes-tda-ews-crossvar-coherence-h3-1q

**Graph node:** `H-B3-1q` (bridge `B3-LAKES-TDA-EWS`) · **Tier:** Standard
**Parent:** `H-B3-1o` (parked, not killed — named revival condition: "compare the expanding-tau
TRAJECTORY itself, not raw value, between pH and doSat," never attempted). Revives that condition
under the mission's own "find the next fresh, cheap candidate" cycle (Explore-agent-driven scan of
`graph.yaml`/`null_results`/`parked`, matching the established H-B2-4/H-CAT31-2 selection pattern).

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Comparing statistical trajectories (Kendall tau vs time, expanding
window) between real time series from a documented whole-lake manipulation experiment. Not causal
(the underlying causal claim — Peter Lake's manipulation caused a regime shift — is already
established by the original O'Brien field experiment, not tested here), not a new causal estimate.

## Origin and design rationale

**H-B3-1o's own revival condition, attempted directly first:** computed `expanding_kendall_tau`
trajectories (reusing `obrien.expanding_kendall_tau`/`betti1_total_persistence_series` UNCHANGED)
for Peter Lake's `pH` and `doSat` series. Two comparisons:
- **Unaligned** Spearman correlation (no time shift): `rho=0.8407` (p<0.0001, n=161).
- **Aligned** (pH shifted so its own stored crossing date lines up with doSat's): `rho=0.6176`
  (p=0.0186, n=14 — most of the series is consumed by the 147-day shift, leaving very few
  overlapping points).

**The aligned correlation is LOWER than the unaligned one, and rests on too few points (n=14) to
trust.** This does NOT support H-B3-1o's own "genuine delay, same shape shifted" hypothesis (which
would predict aligned > unaligned) — if anything it mildly favors the artifact hypothesis, but the
tiny n makes this inconclusive rather than a clean answer. **H-B3-1o's own original question
(delay vs artifact for Peter pH specifically) remains genuinely OPEN after this attempt** — this
experiment does NOT claim to have resolved it.

**What the attempt surfaced instead (Compute-First Check, floor check per this arc's own
established discipline):** before trusting the `rho=0.84` unaligned correlation as evidence of
anything, checked whether it's simply an artifact of two expanding-window statistics trending
together by CONSTRUCTION (exactly the class of floor problem that killed H-B3-1c/1d's own
threshold-crossing approach on 5/5 negative controls earlier in this arc). Computed the SAME
unaligned tau-trajectory correlation for ALL 3 pairwise combinations of Peter Lake's own 3
variables (`chl`, `pH`, `doSat`) AND, as the floor check, the same 3 pairs on **Paul Lake**
(`role: "negative"` in `peter.LAKES` — the reference lake with NO documented manipulation/transition):

```
Peter (positive, real manipulation):  pH-doSat=+0.841  chl-doSat=+0.818  chl-pH=+0.713  (3/3 strong positive)
Paul  (negative, no manipulation):    pH-doSat=-0.906  chl-doSat=+0.375  chl-pH=-0.337  (0/3 consistent; signs mixed)
```

**A clean, unprompted, floor-tested discrimination**, on a different axis than any prior B3
experiment tried: not "does ONE series' tau cross a fixed/self-calibrated threshold" (the approach
that repeatedly floor-failed in this arc, H-B3-1c/1d/1i/1j/1l/1m), but "do MULTIPLE co-measured
variables' tau-trajectories become mutually, consistently, positively correlated." At Peter
(known real transition), all 3 pairs strongly positive; at Paul (known no transition), the pairs
are weak and sign-inconsistent — exactly the opposite pattern a spurious construction-only artifact
would produce (a construction artifact would show up equally at BOTH lakes).

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "If a lake undergoes a genuine whole-ecosystem regime shift, the
co-measured state variables should become mutually correlated in their RATE of structural change
(their expanding-window tau trajectories track each other), because a true regime shift is a
shared, ecosystem-wide event, not an independent per-variable process — whereas in a stable lake
with no shared driving event, different variables' tau trajectories have no reason to move
together."

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Peter Lake (positive, documented manipulation) and Paul Lake (negative, no manipulation) — each with 3 co-measured variables (`chl`, `pH`, `doSat`), their `expanding_kendall_tau(betti1_total_persistence_series(...))` trajectories |
| **Falsifiable predicate** | Are ALL 3 pairwise unaligned Spearman correlations positive AND substantially stronger at Peter than at Paul? |
| **Measurable outcome** | 3 pairwise correlation coefficients per lake (6 total), sign consistency, magnitude comparison |

## Kill Criterion (set BEFORE formalizing — Compute-First already ran)

- **Positive control / floor check (mandatory):** ALL 3 Peter pairs must be positive; Paul pairs
  must NOT show the same consistent-positive-and-strong pattern (either mixed sign, or
  substantially weaker magnitude). RESULT (Compute-First): Peter 3/3 positive (0.71-0.84); Paul 0/3
  consistent (signs: -0.91, +0.38, -0.34) — **PASSES**.
- **Sample-size honesty (mandatory, not a pass/fail bar but a required caveat):** this is `n=1`
  lake-pair (Peter vs Paul) with 3 non-independent within-lake pairwise comparisons (all 3 derived
  from only 3 underlying series — `chl-doSat` and `chl-pH` share the `chl` series, so these are NOT
  3 independent replicates). This is real, floor-checked signal but a SMALL effective sample —
  explicitly `LEAD`, not `PROMOTE`, regardless of how clean the pattern looks (per this session's
  own established discipline from the H9-A overclaim correction earlier).
- **Does NOT resolve H-B3-1o's own original question:** the pH-specific delay-vs-artifact question
  stays genuinely open (aligned correlation inconclusive on n=14).

## What This Does NOT Mean

1. Does NOT resolve H-B3-1o's own original delay-vs-artifact question for Peter pH specifically —
   that stays `parked`, unresolved by this attempt.
2. Does NOT claim statistical significance in the usual multi-replicate sense — `n=1` lake-pair,
   3 non-independent comparisons. A genuine test would need multiple independent
   manipulation-vs-reference lake PAIRS, which this dataset does not provide (O'Brien lakes has
   only 1 variable per lake, so cross-variable coherence cannot be tested there).
3. Does NOT claim this generalizes to any other ecological regime-shift dataset.
4. Does NOT re-open or contradict any of the B3 arc's own prior REJECT verdicts (H-B3-1c/1d/1i/
   1j/1l/1m) — those tested a DIFFERENT statistic (single-series threshold-crossing), not
   cross-variable coherence.

## MCID

Not formally applicable (`n=1` lake-pair) — the qualitative bar is the floor-check itself: does the
pattern separate positive from negative control cleanly? It does, on this one pair.
