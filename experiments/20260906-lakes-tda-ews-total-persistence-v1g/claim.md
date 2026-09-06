# claim.md — 20260906-lakes-tda-ews-total-persistence-v1g

**Graph node:** `H-B3-1g` (new, per Minimal Relaxation Rule) · **Bridge:** `B3-MAY-TDA` · **Tier:** Standard
**Parent:** `H-B3-1f` (V3 descriptive join — recommended "a genuinely new approach (different
topological invariant...)" over another null-model variant, given three consecutive REJECTs with an
identical false-positive set on the ENTROPY statistic)

> **Role of this experiment:** the "hard branch" named in `H-B3-1f`'s decision.md, now attempted
> directly. ONE assumption changed from `H-B3-1c` (V1): the TDA statistic itself — Betti-1 persistence
> ENTROPY (captures the SHAPE of the persistence diagram's lifetime distribution, normalized) →
> Betti-1 TOTAL PERSISTENCE (captures the MAGNITUDE of topological structure, unnormalized: sum of H1
> bar lengths). Everything else (per-series AR(1)-surrogate null from V1, same 9 series, same window,
> same embedding) unchanged — reuses `v1.cmd_run()` via the new `tda_stat_fn` parameter, exactly the
> same reuse pattern as V1'/V2'.

## Why This Is a Genuinely Different Invariant, Not a Relabeling

Persistence entropy `-Σp_i·log(p_i)` (where `p_i = life_i / Σlife_j`) is invariant to uniformly scaling
all bar lengths — it only sees the SHAPE of the lifetime distribution (many short bars vs one dominant
long bar). Total persistence `Σlife_i` is exactly the opposite: it is sensitive ONLY to overall
magnitude, blind to shape (a diagram with 10 equal short bars and one with 1 long bar of the same total
length give the SAME total persistence but very different entropy). A series whose entropy trend was
uninformative (H-B3-1c/d/e's finding) could plausibly show a clean total-persistence trend if the real
signal is "more/bigger topological loops appear," not "the loop-length distribution becomes more/less
uniform" — a substantively different physical hypothesis about what a regime shift looks like
topologically.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 9 series as `H-B3-1c`/`d`/`e`/`f` |
| **Falsifiable predicate** | Per-series AR(1)-surrogate-null detection using TOTAL PERSISTENCE (instead of entropy) reduces the false-positive rate on the 5 negative controls below the persistent 5/5 seen across three entropy-based null variants |
| **Measurable outcome** | False-positive rate on the 5 negative controls; whether ≥1 positive case retains a lead; explicit comparison of WHICH series false-positive here vs. under entropy (same set = the problem is in the null/threshold machinery, not the invariant; different set = the invariant itself matters) |

## FL Step -3: Novelty / Prior-Art Check

`grep` of `null_results/INDEX.md` and `pearl_registry/INDEX.md`: no prior attempt in this project used
total persistence as the TDA statistic for this bridge — entropy was used throughout `H-B3-1`
(original scoping) onward. Total persistence itself is a standard TDA summary statistic (not a novel
invention), used here for the first time in this specific pipeline.

## Natural Language Statement

> "We test whether replacing Betti-1 persistence entropy with Betti-1 total persistence — a
> topologically different summary statistic of the same persistence diagrams already computed in this
> pipeline — changes the false-positive rate or the specific false-positive series, using the
> already-validated per-series AR(1)-surrogate-null detection rule (V1) unchanged."

## L0 Classification

**Predictive** (same as `H-B3-1c`/`d`/`e` — a genuine kill_criterion applies here, unlike the
descriptive `H-B3-1f`).

## What This Does NOT Mean

1. Does NOT change the null-generation procedure — reuses V1's AR(1) surrogate exactly, isolating the
   TDA-invariant question from the null-model question already explored three times (`H-B3-1c/d/e`).
2. Does NOT test a bottleneck/Wasserstein-distance-based change-point statistic (a genuinely different
   FAMILY of TDA change detection, comparing diagrams directly rather than summarizing each one) — a
   further, more involved next step if this one is also uninformative.
3. If the SAME 5 series false-positive here as under entropy, that would be strong evidence the
   specificity problem lives in the detection/null machinery, not in the choice of topological summary
   — informative either way this comes out.

## MCID

Same bar as `H-B3-1c`/`d`/`e`: false-positive rate ≤ 1/5 with ≥1 surviving positive lead for PROMOTE; a
false-positive rate or false-positive SET strictly different from entropy's 5/5-on-the-same-series is
the minimum bar for "informative, not a repeat of the same finding under a new name."
