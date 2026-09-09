# claim.md — 20260910-remy-tumorigenesis-exact-large-deviation-h30

**Graph node:** `H-B7-30` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Full
**Parent:** `H-B7-26` (exact escape probabilities), `H-B7-28` (full-domain exact probabilities,
k=1..40). Directly executes the user's own explicit priority item 4 from the original H-B7-26
redirect ("Только затем повторно оценить large-deviation/Kramers claim"), deferred through
H-B7-27/28/29 while the branch-isomorphism mechanism was held per the user's own explicit
instruction. Now that the mechanism thread (H-B7-27/28/29) reached a natural stopping point
(confirmed, generalized, and contrasted), this experiment returns to the deferred item.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Re-fitting a log-linear relationship using exact (not sampled)
values from a fully specified deterministic system. Not causal, not inferring a population
parameter from a sample — but the FIT ITSELF is a statistical/descriptive summary whose strength
depends on sample size and x-axis distinctness regardless of y-axis precision.

## Origin and design rationale

The user's own original critique (which triggered the entire H-B7-26 arc) was precise: the
informal cross-domain report's `H9-A` result (`log(escape_prob) ~ -0.508*PNR_step, r²=0.8913`)
rested on only **3 distinct PNR-step values `{2,4,5}`** across effectively fewer than 8 independent
points (branches highly correlated). The user's own verdict: "LEAD, не PROMOTE."

**The question this experiment actually tests:** does replacing Monte Carlo escape-probability
ESTIMATES with EXACT escape probabilities (H-B7-26/28's own committed values) change this
assessment? Two candidate answers, genuinely uncertain before computing:

- **Hypothesis A (exactness helps):** the original weak `r²` was partly a Monte Carlo sampling
  noise artifact; exact numbers should tighten the fit and/or reveal that more of H-B7-22's own 80
  original conditions carry non-trivial information than the informal report used.
- **Hypothesis B (exactness doesn't help — geometry problem persists):** the weak evidentiary
  status was NEVER about y-axis (probability) precision — it was about x-axis (PNR-step)
  distinctness and sample size. Exact y-values on the SAME 3-4 x-values changes nothing structural.

**Compute-First Check (scratchpad, BEFORE building the full artifact):** directly tested Hypothesis
A vs B using H-B7-28's own exact `k=1..4` probabilities (the only non-trivial region — `k>=5` gives
`exact_escape_probability=1.0` identically, `log(P)=0`, zero information, confirmed for 36/40 of
H-B7-22's own originally-tested conditions) against H-B7-24's own committed PNR-step values:

```
log(P) ~ -0.4924 * PNR_step + const,  r=-0.9449, r²=0.8929  (n=4, only 3 distinct x: {2,4,5})
```

**r²=0.8929 with exact numbers vs the original report's r²=0.8913 with Monte Carlo estimates —
essentially unchanged.** Two alternative candidate x-axes were also tested as a robustness check
(`n_transient`: r²=0.7251; `expected_steps_to_absorption`: r²=0.5240) — BOTH weaker than PNR-step,
not stronger, and both still `n=4`. **This directly supports Hypothesis B, not Hypothesis A.**

**Minimal Relaxation Rule compliance:** this experiment changes ONE thing relative to the original
informal report — Monte Carlo `escape_prob` values replaced with exact ones, on the SAME underlying
domain and SAME candidate x-axis. No new state space, no new mechanism claim.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "The weakness the user identified in the original `H9-A` result was a
data-geometry limitation (few distinct x-values, small effective sample size), not a Monte Carlo
measurement-noise problem — exact probabilities computed from the SAME underlying release-state
family cannot add new distinct x-values, because 36 of H-B7-22's own 40 originally-tested `k`
values fall in the trivial `SCHEDULE_ROBUST` region where `P=1.0` identically, carrying zero
information regardless of measurement precision."

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The `log(exact_escape_probability)` vs `PNR_step` (and 2 alternative candidate x-axes) linear fit, computed on H-B7-26/28's own committed exact values across H-B7-22's full originally-tested domain (`k=1..40`) |
| **Falsifiable predicate** | Does replacing Monte Carlo estimates with exact probabilities materially change the fit's `r²`, its effective sample size, or the number of distinct x-values available, relative to the original informal report's own numbers? |
| **Measurable outcome** | `r²`, `n`, count of distinct x-values, for the primary axis (PNR-step) and each alternative axis, compared explicitly against the original report's own `r²=0.8913` |

## Kill Criterion (set BEFORE running the full formal artifact — Compute-First already ran)

- **Hypothesis A (exactness materially helps) is CONFIRMED if:** `r²` on exact numbers exceeds the
  original Monte Carlo `r²=0.8913` by a large margin (e.g. `>0.95`), OR the number of genuinely
  non-trivial, distinct x-value conditions across H-B7-22's own 40-`k` domain exceeds the original
  4-point/3-distinct-x sample materially (e.g. `>=8` distinct non-trivial x-values).
- **Hypothesis B (geometry problem persists, exactness doesn't rescue it) is CONFIRMED if:** `r²`
  stays within a small margin of the original `0.8913` (already found: `0.8929`, essentially
  identical), AND the informative-condition count stays capped near the original 3-4
  (already found: exactly 4 non-trivial conditions, 3 distinct x-values, out of 40 tested).
- **RESULT (from Compute-First, to be formally re-verified and locked in the full artifact):
  Hypothesis B CONFIRMED.** Exact numbers do not rescue the data-geometry limitation. The
  large-deviation/Kramers framing remains, honestly, "LEAD, не PROMOTE" — exactly the user's own
  original verdict — and this experiment formally closes that reassessment rather than leaving it
  open.

## What This Does NOT Mean

1. Does NOT mean the large-deviation/Kramers hypothesis is FALSE — only that THIS specific
   experimental family (2 branches, this clamp scheme, `k=1..40`) cannot supply enough distinct,
   non-trivial data points to test it rigorously. A genuinely different release-state family
   (different clamp targets, not just different `k` under the same clamp) would be needed to add
   real new x-values — named as a possible future direction, not attempted here (expensive, out of
   this cheap-cycle's scope).
2. Does NOT claim the `n_transient`/`expected_steps_to_absorption` alternative axes are inherently
   worse candidates in general — only that, on THIS specific 4-point sample, they fit worse than
   PNR-step, not better; a genuinely richer dataset might favor a different axis.
3. Does NOT retroactively invalidate H-B7-26/27/28/29's own confirmed exact-probability or
   isomorphism findings — this experiment is purely about the SEPARATE large-deviation regression
   question, which those experiments explicitly deferred rather than resolved.
4. Does NOT re-open or re-litigate the branch-isomorphism mechanism thread — this experiment closes
   the OTHER item (4) the user's original priority list named, independently.

## MCID

Not formally applicable in the usual estimand sense (n=4 is too small for a meaningful minimum
practically important difference threshold on its own) — the relevant "MCID-equivalent" bar here is
the qualitative one the user themselves set: LEAD requires `r²` improvement large enough to change
the "LEAD, не PROMOTE" verdict. `Δr² = 0.0016` (0.8929 vs 0.8913) does not clear any reasonable bar.
