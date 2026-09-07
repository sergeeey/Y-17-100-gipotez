# claim.md — 20260907-chernoff-neuralode-nd-numerical-abscissa-fixedgrid

**Graph node:** `H-B2-1q` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (reuses existing,
already-verified pipeline pieces byte-identically; fixed grid + fresh seed range are the only
new elements)
**Parent:** `H-B2-1p` (MIXED at N∈{64,80}; N=64 individually significant, p=0.021, but a
same-session skeptic pass found this could NOT be trusted as independent evidence — N=64 and
N=80 were chosen ADAPTIVELY, specifically because N=40/50 were null, to test for "reappearance."
`H-B2-1p`'s own decision.md named the exact fix, verbatim, in its Relaxation Map: a genuinely
pre-registered fixed grid, decided before running, not in response to any prior null.)

## Why This Experiment, Specifically — and Why the Grid Is Not Newly Chosen Today

This is the direct, named next step from `H-B2-1p`'s Relaxation Map: *"pre-register a FIXED grid
(e.g. N in {56, 64, 72}, chosen before running anything, not because 40/50 were null) in ONE new
experiment. If N=64 replicates at p<0.05 there, reappearance is real, not drawer-selection."*

**Critically, this grid was NOT chosen today, after seeing more results — it was named and
committed to `main` in `H-B2-1p`'s own decision.md BEFORE this experiment's code existed.** This
is what distinguishes this experiment from `H-B2-1p`'s own adaptive-selection problem: the grid
`{56, 64, 72}` is fixed by a prior, already-merged commit, not decided in light of any data this
session has seen since. N=56 and N=72 flank N=64 on both sides (one below, one above) — chosen
for coverage, not because either individually was hoped to show anything.

**The specific question this resolves:** does N=64's apparent significance in `H-B2-1p`
(rho=0.298, p=0.021, on seeds 0-59) replicate on a FRESH, non-overlapping seed range, under a
pre-registration that was locked in before this session started building this experiment? If
yes, the earlier finding was real, just improperly evidenced at the time. If no, `H-B2-1p`'s
N=64 result was drawer-selection, and the honest reading of the whole arc becomes "signal at
small-mid N (16,32), vanishes by N~40 and does not measurably return."

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE** (same as the whole H-B2-1* arc).

## FL Step 0a — Mechanism Claim Gate

No new mechanism-behavior sentence introduced; `omega(A)`'s theoretical status was already
established as not triggering Step 0a in `H-B2-1n`, reused unchanged here.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(omega(A), M1)` pairs at `N_DIM` in {56, 64, 72} — a grid named in `H-B2-1p`'s decision.md before this experiment's code existed. Seeds 100-159 (60 fresh seeds per slice, 180 total pairs) — ZERO overlap with any prior seed range used at ANY N_DIM in this arc (H-B2-1m/n/o used 0-39 or 40-99; H-B2-1p used 0-59 at N=64,80) |
| **Falsifiable predicate** | N=64 individually significant (alpha=0.05, positive sign) on this fresh, pre-registered-grid data — the SAME specific claim `H-B2-1p` could not trust |
| **Measurable outcome** | Per-slice Spearman rho/p at N=56, 64, 72; N=64's result is the PRIMARY pre-registered criterion, N=56/72 reported as context (do they show the same pattern as their neighbors 50 and 80?) |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md`: this exact grid and exact question ("does N=64 replicate on
fresh, non-adaptively-selected data") is named verbatim in the `H-B2-1p` Pearl Registry entry
about the self-caught methodological error. Confirmed novel in the sense of being the first
actual execution of that named next step — not previously run.

## Kill Criterion (set BEFORE running — unchanged from what H-B2-1p already committed to)

- **REPLICATED:** N=64 individually significant at alpha=0.05, positive sign, on fresh seeds
  100-159. `H-B2-1p`'s N=64 finding was real; the drawer-selection concern does not invalidate
  the underlying relationship, only how confidently it could be stated at the time.
- **NOT_REPLICATED:** N=64 not significant (p>=0.05) on fresh seeds. `H-B2-1p`'s N=64 result was
  drawer-selection — a false positive produced by testing exactly the dimension most likely to
  look interesting after two nulls. The honest arc-wide reading becomes "solid at N in {16,32},
  vanishes by N~40, does not measurably return."

No tier for N=56/N=72 in the primary verdict — they are reported for context (continuity with
the already-known N=50/N=80 nulls flanking them) but the specific, pre-committed question is
about N=64, and only N=64's result determines REPLICATED vs NOT_REPLICATED.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1p`'s own MIXED verdict — that stands on its own,
   correctly-labeled, imperfect evidence. This experiment supplies the INDEPENDENT confirmation
   (or disconfirmation) `H-B2-1p` explicitly said it could not supply itself.
2. A REPLICATED verdict does NOT establish `omega(A)` as periodic/oscillating in N — it
   establishes that the specific N=64 relationship is real, nothing about the functional form
   between tested points.
3. A NOT_REPLICATED verdict does NOT prove no relationship could ever exist at N=64 under any
   circumstance — only that this specific, adequately-powered (n=60), pre-registered test did
   not find one.
4. Does NOT establish causality.

## MCID

N=64's Spearman p-value crossing 0.05 on seeds 100-159, positive sign, reported alongside N=56
and N=72 for full transparency about the surrounding pattern.
