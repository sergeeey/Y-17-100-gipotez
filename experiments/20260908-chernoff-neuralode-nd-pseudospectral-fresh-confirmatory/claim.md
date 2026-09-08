# claim.md — 20260908-chernoff-neuralode-nd-pseudospectral-fresh-confirmatory

**Graph node:** `H-B2-1t` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (reuses existing,
already-verified pipeline pieces byte-identically; fresh seed range is the only new element)
**Parent:** `H-B2-1s` (CONFIRMED: independent `pseudopy` implementation reproduces `H-B2-1r`'s
pseudospectral abscissa result at N=40,50 within ~2.5% median value difference, rank correlation
~0.99. Closed the skeptic's named remaining gap. User's own explicit Priority 2, gated on
Priority 1 passing: a fresh confirmatory experiment on NEW seeds, with `kappa(V)`/`omega(A)` as
pre-registered comparators, not new hypotheses evaluated after seeing results.)

## Why This Experiment, Specifically — User's Own Priority 2 Framing, Verbatim

> Тогда уже делать fresh confirmatory experiment на новых матрицах/сидах, не на тех же данных.
> И заранее фиксировать: N=40,50 как primary large-N regime; pseudospectral abscissa как primary
> descriptor; один предрегистрированный критерий эффекта; κ(V) и ω(A) как comparators, а не как
> новые гипотезы после просмотра результата.
>
> Тогда можно проверить уже более сильный claim: При large N pseudospectral abscissa устойчиво
> предсказывает M1 лучше, чем κ(V) и ω(A).

**Why this specific design, not a variation:** every prior confirmation of pseudospectral
abscissa at N=40,50 (`H-B2-1r`, `H-B2-1s`) used the SAME 15-seed population (seeds 0-14). Even
`H-B2-1s`'s independent cross-implementation check reused those exact matrices — a genuinely
independent implementation, but not genuinely independent DATA. This experiment is the first
test of pseudospectral abscissa at N=40,50 on data that has never been seen by this arc before,
in any form.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE** (same as the whole H-B2-1* arc — a correlational claim, no
causal framing).

## FL Step 0a — Mechanism Claim Gate

No new mechanism-behavior sentence introduced. All three descriptors' theoretical status was
already established earlier in the arc (Trefethen-Embree for `kappa(V)`, Bendixson for
`omega(A)`, Kreiss Matrix Theorem for pseudospectral abscissa) — none trigger Step 0a. The
pseudospectral abscissa COMPUTATION was already correctness-verified twice (`H-B2-1r`'s own
positive controls + bug fix, `H-B2-1s`'s independent cross-implementation) — reused unchanged
here, no new verification needed for the routine itself.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(kappa(V), omega(A), alpha_eps(A), M1)` quadruples at `N_DIM` in {40, 50} — the user's own specified "primary large-N regime" — on FRESH seeds 300-339 (40 seeds per slice, 80 total pairs). Seed range chosen to have ZERO overlap with EVERY prior seed range used anywhere in this arc at ANY N_DIM (0-39, 40-99, 0-59, 100-159) — not just at N=40,50 specifically, for maximum defensibility |
| **Falsifiable predicate** | Pseudospectral abscissa individually significant (alpha=0.05, positive sign) at BOTH N=40 and N=50 on this fresh data — direct replication of `H-B2-1r`'s own criterion. `kappa(V)` and `omega(A)` are computed as PRE-REGISTERED COMPARATORS on the identical fresh matrices (same population, not a separate hypothesis test) — their expected behavior (null at N>=40, per `H-B2-1q`'s `hard_killed` verdict) is stated BEFORE running, not evaluated after |
| **Measurable outcome** | Per-N_DIM-slice Spearman rho/p for all three descriptors against M1, reported side by side on the SAME fresh matrices — the "stronger claim" the user named (pseudospectral abscissa predicts M1 reliably where the other two don't) is directly visible in one table, not inferred across different experiments' different data |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md`: this exact experiment (fresh-seed confirmatory replication,
`kappa(V)`/`omega(A)` as comparators) is named verbatim as Priority 2 in the user's own plan,
recorded in this session. Confirmed novel — first actual execution, gated on `H-B2-1s` (Priority
1) having passed, per the user's own explicit ordering.

## Kill Criterion (set BEFORE running)

- **CONFIRMED (replicates on independent data):** pseudospectral abscissa individually
  significant (alpha=0.05, positive) at BOTH N=40 and N=50 on the fresh seeds. This is the
  primary, sole pre-registered criterion — matching `H-B2-1r`'s own bar exactly, now tested on
  data that arc has never touched.
- **REJECTED/weakened (does not replicate):** pseudospectral abscissa loses significance at
  EITHER N=40 or N=50 on fresh data — would mean the `H-B2-1r`/`H-B2-1s` result was specific to
  that one 15-seed sample in a way three separate verification passes (positive controls, local-
  vs-global, cross-implementation) all failed to catch. Would be a serious, surprising finding
  requiring its own investigation, not just a downgrade.

**`kappa(V)` and `omega(A)` comparator predictions, stated BEFORE running (not a kill criterion
for THIS experiment — their arc-wide verdicts are already `hard_killed`/settled — but a
pre-registered expectation that would itself be noteworthy if violated):** both expected to
remain individually non-significant at N=40 and N=50 on this fresh data, consistent with
`H-B2-1q`'s six-point null pattern across two independent seed ranges. If either comparator
UNEXPECTEDLY shows significance here, that is itself a finding worth flagging (a third seed
range breaking an already twice-independently-confirmed null would be surprising), not silently
absorbed into "well, comparators are just for context."

## What This Does NOT Mean

1. Does NOT retroactively change any prior verdict in this arc — this is a NEW, independent
   confirmatory test, not a re-analysis.
2. A CONFIRMED verdict here does NOT constitute publication-grade evidence by itself — it is one
   more independent replication, strengthening but not concluding the overall claim.
3. Does NOT establish causality.
4. `kappa(V)`/`omega(A)` results here are COMPARATORS on the same fresh population, not a new
   test of their own arc-wide status — their `hard_killed` verdicts from `H-B2-1q` stand
   regardless of what happens on this specific 40-seed sample (a single sample not replicating a
   null at alpha=0.05 by chance ~5% of the time is expected, not a revival).

## MCID

Individual significance (alpha=0.05, positive sign) of pseudospectral abscissa at N=40 AND N=50
on fresh seeds 300-339, reported alongside `kappa(V)`/`omega(A)` comparator results on the
identical matrices for direct, same-data, same-table comparison.
