# claim.md — 20260906-lakes-tda-ews-surrogate-null-v1

**Graph node:** `H-B3-1c` (new, per Minimal Relaxation Rule) · **Bridge:** `B3-MAY-TDA` · **Tier:** Full
**Parents:** `H-B3-1` (Peter/Paul Lake, CRITERION_INVALID) and `H-B3-1b` (O'Brien lakes, CRITERION_INVALID)

> **Role of this experiment:** V1 from both parents' Relaxation Maps. Exactly ONE assumption changed
> from H-B3-1/H-B3-1b (Minimal Relaxation Rule): the detection rule. Everything else — population (all
> 9 series from both prior experiments), window fraction, embedding dimension/delay, statistics
> (AC1, variance, Betti-1 persistence entropy) — is unchanged. Re-uses the tested `ar1_surrogate`,
> `rolling_stat`, `betti1_entropy_series`, `expanding_kendall_tau` functions from
> `20260906-may1972-tda-ews-obrienlakes/run.py` (the shared module both parents already import from).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 9 series analyzed in `H-B3-1` (Peter chl/pH/doSat, Paul chl/pH/doSat) and `H-B3-1b` (Lower Zurich, Windermere, Loch Leven pca1) |
| **Falsifiable predicate** | A PER-SERIES, PER-TIMEPOINT surrogate-null threshold (95th percentile of an AR(1)-surrogate expanding-tau curve) discriminates positive cases (Lower Zurich, Peter Lake) from negative controls (Windermere, Loch Leven, Paul Lake) — where the fixed tau≥0.5 threshold could not (floor 45–90%) |
| **Measurable outcome** | False-positive rate on the 4 negative-control series (Windermere, Loch Leven, Paul×3) under V1; whether ≥1 positive-case series (Lower Zurich, Peter×3) shows a TDA lead with NO false positive anywhere |

## FL Step -4: Source Trace / Novelty Check

Not re-run in full — the population and prior source-tracing are unchanged from `H-B3-1`/`H-B3-1b`; only
the detection rule is new. The surrogate-testing approach itself (Theiler et al. 1992-style AR(1)/phase
surrogates for significance testing of nonlinear statistics) is standard methodology, not a novel
invention — cited generically in the EWS literature (Dakos et al. 2012).

## Natural Language Statement

> "We estimate whether replacing the fixed tau≥0.5 detection rule with a per-series, per-timepoint
> AR(1)-surrogate-null significance test (alpha=0.05) reduces the false-positive rate on the 4 known
> negative-control series to near zero while preserving a detectable TDA lead on at least one of the 2
> positive-case systems (Lower Zurich, Peter Lake), for the classical (AC1, variance) and TDA
> (Betti-1 persistence entropy) statistics already computed in H-B3-1/H-B3-1b."

## HD-MAVP — single assumption changed

| # | Assumption | Status before (H-B3-1/1b) | Status now (V1) |
|---|---|---|---|
| A_rule | Detection rule: fixed tau≥0.5 for every series | `killed` (floor 45–90%, both parents) | **replaced**: per-series, per-timepoint 95th-percentile AR(1)-surrogate null |
| A1–A4 (embedding, window, statistic choice) | unchanged, `alive` (survived both parent decisions) | unchanged |

**Rule respected:** only A_rule changed. If V1 also fails, the next candidate (V2: change-point
co-requirement, or V3: report peak tau) requires ANOTHER new experiment ID, not a retry here.

## Compute budget (stated up front, not discovered mid-run)

Betti-1 (TDA) surrogates require a fresh `ripser` call per window per surrogate — the expensive path.
Classical (AC1, variance) surrogates are cheap (closed-form per window). Reps are asymmetric by design:
- Classical statistics: 100 surrogates per series (cheap, matches literature convention for a
  95th-percentile estimate — 1/0.05 = 20 minimum, 100 gives a stable estimate with margin)
- TDA (Betti-1): 20 surrogates per series (same rep count already used for the floor check in both
  parents — no new compute-budget precedent set, reuses the one already spent)

## What This Does NOT Mean

1. Does NOT mean V1 is THE correct detection rule if it passes — it is the FIRST of 3 candidates in the Relaxation Map, chosen as least circular, not validated as uniquely correct.
2. A PASS here does NOT retroactively make H-B3-1/H-B3-1b's original CRITERION_INVALID verdicts wrong — those verdicts were correct for the rule as originally specified.
3. Does NOT test V2 or V3 — those remain untested, separate candidate experiments if V1 also fails.

## MCID

False-positive rate ≤ 1/4 negative controls (i.e., strictly fewer false positives than the 4/4 seen
under the fixed threshold) is the minimum improvement to call this "informative, not identical." A
false-positive rate of 0/4 with ≥1 surviving positive lead is the target for PROMOTE.
