# H-CAT31-2 — claim.md

## Origin

Continuation of `reports/2026-09-09-breakthrough-routes.md` — Route 2 ("Ловас: хвосты
распределения и арифметика размера"), the report's own first bounded (<=4h) test, run now
because the report's two higher-priority routes (Route 3 = `H-B3-2`, Route 4 = `H-B2-3`) are
both already REJECTED (ADR-093, ADR-094), and Route 1 (Forsythe minimal-counterexample
construction) is blocked on reproducing the authors' own certificate (ADR-091: confirmed a
multi-session task, not a cheap first test). Route 2 is the cheapest remaining option with a
concrete, already-specified first test — reused verbatim from the report, not re-derived here,
per pre-registration discipline (a test chosen AFTER seeing this experiment's own results would
not count).

**Novelty Check (FL Step -3):** grep of `null_results/INDEX.md`, `parked/INDEX.md`,
`pearl_registry/INDEX.md`, `registry/graph.yaml` for "tail"/"arithmetic"/"divisor" combined with
"theta"/"circulant"/"CAT31" returns zero prior matches — `H-CAT31-1` tested only the MEAN of
`theta(G)/sqrt(n)` on a fixed geometric grid `n=10*2^k`; this experiment tests the TAIL/extreme-
value structure on near-prime-vs-composite `n` pairs, a genuinely different question the report
itself distinguishes explicitly (mean concentration vs rare-event contribution to the mean).

## EstimandOps L0

**Question type:** Descriptive. "Does the arithmetic class of `n` (near-prime vs
highly-composite) leave a detectable trace in the extreme-value structure of
`theta(G)/sqrt(n)` for random dense circulant graphs, at matched `n`?" No causal claim — `n`'s
primality is not manipulated, only compared across naturally-occurring pairs.

## The formal reformulation (from the report, reused verbatim)

At `p=1/2`, let `X_n = log(theta(G)/sqrt(n))`. From the exact identity
`theta(G)*theta(Gbar) = n` (Lovász 1979, tight for vertex-transitive graphs — already
independently verified in `H-CAT31-1`'s own cross-validation) and the ensemble's symmetry in
distribution under complementation at `p=1/2` (complementing a `p=1/2` circulant graph yields
another `p=1/2` circulant graph, same distribution), `X_n =_d -X_n`. Therefore:

    E[theta(G)] / sqrt(n) - 1 = E[cosh(X_n) - 1]

This is an elementary consequence of the symmetry, not a new theorem — but it reframes
`H-CAT31-1`'s own "ratio stays near 1" finding as a statement about `E[cosh(X_n) - 1]` being
small, which convexity of `cosh` means could hold EITHER because `X_n` concentrates tightly near
0, OR because rare large `|X_n|` values are individually rare enough that their (large) `cosh`
contribution still averages out small. `H-CAT31-1` cannot distinguish these — it only reports
the mean. This experiment looks at the DISTRIBUTION, specifically at whether the arithmetic
structure of `n` (divisor richness) changes that distribution's tail.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "the paper's own time-domain primal LP (`theta_via_lp`, already
independently verified in `H-CAT31-1`'s own cross-validation against known closed forms) is
exact enough at `n` up to ~511 to resolve the differences this experiment looks for."

**Check:** reused unchanged from `H-CAT31-1` (`sample_circulant_neighbors`, `theta_via_lp`), no
new formula introduced — this experiment adds no new Mechanism Claim of its own beyond what
`H-CAT31-1` already checked. A timing/sanity diagnostic (scratchpad, not committed) confirmed
`theta_via_lp` runs in well under 0.2s per solve even at `n=511`, so the full experiment (6 `n`
values x several hundred repetitions) completes in minutes, not hours.

## The claim (falsifiable)

For the three near-prime/composite `n` pairs specified by the report — `(127, 129)`,
`(251, 255)`, `(509, 511)` (first of each pair prime, second composite; chosen by the report
BEFORE any of this experiment's data existed, not cherry-picked here) — at matched `n` within
each pair, several hundred independent random dense circulant graphs (`p=1/2`) are sampled and
`theta(G)` computed via `theta_via_lp`. For each `n`, compute `X = log(theta(G)/sqrt(n))`, its
variance, range, and the top-decile contribution to `E[cosh(X)-1]` (fraction of the mean
`cosh(X)-1` coming from the top 10% of `|X|` values — the tail-concentration signal the report's
own reformulation motivates).

- **LEAD (arithmetic signal present, worth a held-out confirmatory test):** within EVERY one of
  the 3 pairs, the composite-n member shows a materially different tail statistic (e.g. >=50%
  higher top-decile contribution, or >=50% higher variance of X) than its prime-n partner, in
  the SAME direction across all 3 pairs (consistent sign, not 2-1 mixed).
- **CRITERION_INVALID (no signal to interpret):** the positive control fails (see below), or the
  per-n sample size is too small to distinguish tail statistics from sampling noise (checked via
  a bootstrap CI on the top-decile contribution, not just eyeballing the point estimate).
- **REJECTED (no arithmetic effect at this scale):** the 3 pairs show no consistent
  prime-vs-composite direction (mixed signs, or differences within bootstrap noise).

**Positive control (per the report's own specification):** `|theta(G)*theta(Gbar)/n - 1| <= 1e-6`
for every sampled graph — a violation is treated FIRST as a numerical/implementation problem,
not as evidence about the arithmetic hypothesis.

## What this does NOT mean

1. Does NOT establish the "continuation filter" bar the report itself names as the SECOND,
   separate test (an arithmetic feature predicting extremes on a held-out `n` group, with a
   pre-registered effect size) — this experiment is explicitly only the report's own FIRST,
   4-hour-budgeted reconnaissance test. A LEAD verdict here does not promote to CONFIRMED without
   that second, harder test, which is not run here.
2. n=3 pairs is far too few to support ANY statistical claim about "primality in general" — this
   experiment reports whether a SPECIFIC, pre-chosen set of 3 pairs shows a consistent pattern,
   not a general law about arithmetic structure and Lovász theta.
2b. In particular: a LEAD verdict is not evidence that divisor count/structure is the CAUSAL
    mechanism — many other differences between a prime and its composite neighbor exist (parity
    of `(n-1)/2`, distance to the nearest smaller prime, etc.) and are not disentangled here.
3. Does NOT investigate the dual LP certificate structure the report also mentions ("шаблон
   сертификата") — out of scope for this first test, named as a possible follow-up only.
4. Does NOT combine with `H-CAT31-1`'s own geometric-grid sweep — a separate, non-overlapping set
   of `n` values, deliberately chosen for a different purpose (near-prime/composite pairing vs
   wide dynamic range).
