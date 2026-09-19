# H-CAT31-4 — claim.md (PRE-REGISTERED before any solve)

Pre-registration timestamp: 2026-09-19, written before `run.py` was executed. Nothing in this
file was edited after the first LP solve of this experiment; later additions go into
`decision.md` under a "post-registration" label.

## Origin

`H-CAT31-3` measured `Var(log(theta(G)/sqrt(n)))` for random dense circulant graphs (p = 0.5) on
`n in {32, 64, 128, 256, 512, 1024, 1536, 2048, 3000}` and got a weighted log-log slope of
`-0.9126`, 95% CI `[-0.9751, -0.8501]` (`experiments/20260910-lovasz-theta-variance-scaling-cat31-3/
metrics/run.json`). **Every `n` in that sweep is composite** (powers of two, `1536 = 2^9*3`,
`3000 = 2^3*3*5^3`). The proof programme for this law (Points 77-101) was parked; a portfolio audit
on 2026-09-19 named this law the only candidate for novelty, and named the missing prime-`n`
sweep as its cheapest test. The prime-`n` ensemble is the one the later proof work actually
concerns (prime `n` gives orbit transitivity), so the composite-only sweep may not describe it.

## EstimandOps L0

**DESCRIPTIVE.** Population variance of `X_n = log(theta(G_n)/sqrt(n))` over the random
circulant-graph ensemble at `p = 1/2`, as a function of prime `n`. No causal claim, no claim about
any single graph. Estimand sentence: *we estimate the log-log slope `b_P` of
`V_n = Var(X_n)` against `n` for prime `n` in `[67, 4093]`, comparing it with `-1` and with the
composite-`n` slope `-0.9126`, no intercurrent events.*

## Zero-Signal Gate

| Field | Value |
|---|---|
| Entity | `V_n = Var(log(theta(G)/sqrt(n)))`, `G` = random dense circulant graph on prime `n` vertices, `p = 0.5` |
| Falsifiable predicate | the weighted OLS slope `b_P` of `log V_n` on `log n` over the 8 prime `n` below has a 95% CI that (a) excludes `-1`, and (b) overlaps the composite band `[-0.9751, -0.8501]` |
| Measurable outcome | slope and 95% CI from `analyze.py`, same weighting rule as `H-CAT31-3/run.py::fit_exponent` |

## Design (locked)

Primes and replicates: `n = 67, 127, 251, 509, 1021, 2053, 3001, 4093` with
`reps = 300, 300, 300, 250, 200, 200, 200, 100`. Sampler and LP are reused unchanged from
`H-CAT31-1/run.py` (`sample_circulant_neighbors`, `theta_via_lp`). Seeds:
`330000 + n*1000 + i`.

Power statement (computed before the run, from the composite-sweep SE 0.031): if the true prime
slope equals the composite slope `-0.913`, the chance that the CI excludes `-1` is about 0.8; if
the true slope is exactly `-1`, the false-rejection rate is 0.05. An empirical version is a
control in `controls.md`.

## Outcome categories (locked before the run)

| Code | Condition on the prime slope CI `[lo, hi]` | Meaning |
|---|---|---|
| **P-CONSISTENT** | `lo > -1` (CI excludes `-1` from above) AND CI overlaps `[-0.9751, -0.8501]` | the sub-`n^-1` decay is not an artifact of composite `n`; `n^-1` is rejected on primes too |
| **P-MINUS-ONE** | `lo <= -1 <= hi` | `n^-1` cannot be rejected on primes. Sub-case **P-DISCREPANT** if additionally `-0.9126` lies outside the CI: prime and composite ensembles differ |
| **P-OTHER** | `hi < -1`, or `lo > -1` with no overlap with the composite band | a different exponent from both hypotheses |
| **UNDERPOWERED** | CI half-width > 0.10 | no verdict; report only |

Secondary (descriptive, no verdict): split slope on `n <= 509` versus `n >= 1021`; Spearman
correlation of `n*V_n` with `n`; the mean of `X_n` (expected exactly 0, see controls).

## What this result does NOT mean

1. It does **not** prove or disprove `Var(X_n) = O(1/n)` as `n -> infinity`: it covers
   `n <= 4093`, and a slowly varying factor `L(n)` (for example logarithmic) is compatible with any
   finite-range slope.
2. It says nothing about `p != 1/2`, non-circulant graphs, or composite `n` beyond the existing
   composite sweep.
3. Even a P-CONSISTENT verdict gives no explanation of the exponent, and no new theorem. It
   would be a numerical observation about one ensemble, with external novelty still unchecked
   beyond the companion paper's silence on variance.
4. A P-MINUS-ONE verdict would not show the composite sweep was wrong; it would show the two `n`
   classes behave differently in the tested range.

## Kill criterion

The pre-registered claim ("prime-`n` slope CI excludes `-1` and overlaps the composite band") is
**killed** if the outcome is P-MINUS-ONE or P-OTHER, and **UNDERPOWERED** is not a kill.
