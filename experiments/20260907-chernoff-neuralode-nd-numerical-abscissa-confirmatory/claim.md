# claim.md — 20260907-chernoff-neuralode-nd-numerical-abscissa-confirmatory

**Graph node:** `H-B2-1o` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (reuses existing,
already-verified pipeline pieces byte-identically; only the seed range and the pre-registered
primary statistic change)
**Parent:** `H-B2-1n` (omega(A) WEAKENED by its own majority-of-5-slices bar, but ALL 5 slices
positive-sign, and an EXPLORATORY post-hoc Fisher combination gave p=0.013 — explicitly walled
off from that verdict per the Anti-Overfitting Gate, not used to upgrade it)

## Why This Experiment, Specifically

`H-B2-1n`'s own decision.md named the concrete next step explicitly, not a vague "investigate
more": a NEW, separately pre-registered experiment with the Fisher combination (or an equivalent
multi-slice combined test) as the PRIMARY kill criterion FROM THE START — not a retroactive
re-analysis of the same data (double-dipping / optional stopping bias) — on a FRESH seed range
(seeds 40-99) to avoid reusing the same 200 data points for both the exploratory discovery and
the confirmatory test. This experiment is exactly that: same `N_DIM` set held fixed (per Minimal
Relaxation Rule — change ONE thing at a time; only the seed range moves), same descriptor
(`omega(A)`), same per-slice Spearman machinery, reused byte-identically via dynamic import.

**Why hold `N_DIM` fixed rather than also varying it:** `H-B2-1n`'s Relaxation Map explicitly
listed "whether to hold the N_DIM set fixed" as an open design choice for this follow-up.
Changing both the seed range AND the `N_DIM` set at once would violate the Minimal Relaxation
Rule (falsification-ladder.md) — this experiment isolates exactly the one question the parent's
exploratory finding raised: does the Fisher-combined signal replicate on independent data, holding
everything else constant.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE** (same as the whole H-B2-1* arc — a correlational claim about a
measured mathematical quantity, no causal intervention framing).

## FL Step 0a — Mechanism Claim Gate

No new mechanism-behavior sentence is introduced here. `omega(A)`'s theoretical status (Bendixson/
Lumer-Phillips, a proven bound) was already established as not triggering Step 0a in `H-B2-1n`;
this experiment reuses that descriptor unchanged. The one new methodological element — combining
5 independent slice p-values via Fisher's method as the PRIMARY statistic — is not a mechanism
claim about the world, it is a pre-registered analysis-plan choice; its legitimacy (as opposed to
pooling raw data across `N_DIM`, the confound Step 0a caught in `H-B2-1l`) was already argued in
`H-B2-1n`'s run.py: each slice is a genuinely independent test on a disjoint `(N_DIM, seed)`
population, so Fisher's method is the textbook-correct way to combine them. Re-verified here by
the same Step 8a skeptic pass this project runs before any PROMOTE (see decision.md).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(omega(A), M1)` pairs on FRESH matrices — same `N_DIM` in {16,24,32,40,50}, but seeds 40-99 (60 fresh seeds per slice, 300 total pairs, ZERO overlap with the 200 pairs `H-B2-1n` already used), via `build_matrix_with_seed_and_n` UNCHANGED (Minimal Relaxation Rule) |
| **Falsifiable predicate** | The Fisher combination of the 5 slices' independent Spearman p-values is itself significant at alpha=0.05 — i.e. `omega(A)` carries a real, replicable (if individually-weak) signal across the large-`N_DIM` population, not an artifact of the specific 200 data points `H-B2-1n` happened to draw |
| **Measurable outcome** | `scipy.stats.combine_pvalues(slice_ps, method="fisher")` on the 5 fresh-seed slice p-values, reported alongside per-slice rho/p and sign-consistency for full transparency |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md` / `null_results/INDEX.md`: no prior confirmatory (as opposed
to exploratory) test of the Fisher-combination criterion for any descriptor in this project. This
is the first experiment in the H-B2-1* arc where a multi-slice combined statistic is the
PRE-REGISTERED primary criterion rather than a post-hoc report. Confirmed novel in that specific
sense (the underlying descriptor and population-construction code are all reused unchanged).

## Kill Criterion (set BEFORE running)

- **CONFIRMED:** Fisher-combined p < 0.05 on the 5 fresh-seed slices. This would mean the
  exploratory signal `H-B2-1n` reported (p=0.013, walled off from its own verdict) replicates on
  independent data — a genuine, if individually-weak-per-slice, relationship between `omega(A)`
  and M1 across the large-`N_DIM` population.
- **REJECTED:** Fisher-combined p >= 0.05. This would mean the exploratory signal was noise (or
  an artifact of the specific 200-point sample), and `omega(A)` — like kappa(V) before it — does
  not explain transient growth at large `N_DIM` with statistical confidence, at least not via a
  simple monotone correlation with M1.

No WEAKENED tier for this experiment specifically: unlike `H-B2-1n` (which combined a majority-
of-slices bar with an unplanned exploratory add-on), this is a single pre-registered binary test
of one statistic, by design — the whole point of running a confirmatory follow-up is to remove
the ambiguity a three-way verdict would reintroduce.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1n`'s own verdict (WEAKENED stands regardless of this
   result — this is a NEW test on NEW data, not a re-analysis of the same 200 points).
2. A CONFIRMED verdict here would establish only that `omega(A)` carries a real combined-across-
   slices signal — NOT that it individually clears the per-slice significance bar `H-B2-1n` used,
   and NOT that it is superior to kappa(V) in any absolute sense (kappa(V) was strong at small
   `N_DIM`, `omega(A)` has never been tested there).
3. A REJECTED verdict does NOT mean transient growth at large `N_DIM` is inherently unexplainable
   — only that these two specific, cheap descriptors (kappa(V), omega(A)) do not capture it via a
   simple monotone correlation; pseudospectral abscissa and other options remain open, and this
   session's own discipline is to NOT auto-chain a third alternative-descriptor experiment without
   a checkpoint.
4. Does NOT establish causality — `omega(A)` and M1 are both functions of the same random coupling
   matrix; this tests explanatory/correlational power, not a causal mechanism.

## MCID

Fisher-combined p-value crossing 0.05, computed on 5 independent slices over a population with
zero seed-index overlap with the exploratory-discovery data — reported as the primary number,
alongside per-slice rho/p and sign-consistency for full transparency (so a reader can see exactly
how the combined result decomposes, not just the pass/fail bit).
