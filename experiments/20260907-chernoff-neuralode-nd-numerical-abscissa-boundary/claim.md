# claim.md — 20260907-chernoff-neuralode-nd-numerical-abscissa-boundary

**Graph node:** `H-B2-1p` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (reuses existing,
already-verified pipeline pieces byte-identically; only two new `N_DIM` values tested)
**Parent:** `H-B2-1o` (CONFIRMED per pre-registered Fisher criterion, p=0.0019, on fresh seeds —
but FL Step 8a skeptic pass + post-hoc partial-conjunction test [p=0.151, walled off] scoped this
down: signal real at `N_DIM` in {16,24,32}, genuinely absent — rho=0.007 twice, not degenerate —
at `N_DIM` in {40,50})

## Why This Experiment, Specifically

`H-B2-1o`'s own decision.md and Pearl Registry named the concrete next step: a NEW test at
`N_DIM` in {64, 80} (the skeptic's own suggestion, recorded verbatim) to discriminate two
readings of the N=40/N=50 null:

1. **"Unlucky pair"** — N=40 and N=50 happened to land in a low-signal patch; a genuine
   `omega(A)`-M1 relationship would reappear (individually significant, positive sign) further out.
2. **"Genuine ceiling"** — `omega(A)` stops explaining transient growth somewhere around N~35-40
   and stays null indefinitely beyond that point.

This is a discriminating test in the Cheapest Differentiating Test Protocol sense: both readings
predict the SAME thing at N in {16,24,32,40,50} (already observed) but DIFFERENT things at N in
{64,80} — reading 1 predicts recovery, reading 2 predicts continued nullity. Genuinely new data
required (unlike `H-B2-1o`'s own partial-conjunction check, which was a re-analysis of existing
data) — this experiment builds NEW matrices at NEW dimensions never tested in this arc.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE** (same as the whole H-B2-1* arc).

## FL Step 0a — Mechanism Claim Gate

No new mechanism-behavior sentence introduced. `omega(A)`'s theoretical status (Bendixson/
Lumer-Phillips) was already established as not triggering Step 0a in `H-B2-1n`; reused unchanged.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(omega(A), M1)` pairs at `N_DIM` in {64, 80} — dimensions NEVER before tested in the H-B2-1* arc — 60 seeds each (0-59; seed reuse across different `N_DIM` is fine since `SeedSequence([n_dim, seed])` makes each `(N_DIM, seed)` pair unique regardless of `N_DIM`'s novelty), via `build_matrix_with_seed_and_n` UNCHANGED |
| **Falsifiable predicate** | Two competing, mutually exclusive predictions: (a) "unlucky pair" — at least one of N=64/N=80 shows individually significant positive correlation; (b) "genuine ceiling" — neither does, extending the null pattern already seen at N=40,50 |
| **Measurable outcome** | Per-`N_DIM`-slice Spearman rho/p at N=64 and N=80, plus Fisher combination of the two (informative but low-powered with only 2 slices — reported, not over-interpreted) |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md`: `N_DIM` in {64, 80} for `omega(A)` vs M1 named as the
concrete next discriminating test in `H-B2-1o`'s own Pearl Registry entry (2026-09-07, "H-B2-1o
(различающий тест N∈{64,80})"), not yet run. Confirmed novel — this IS that named test.

## Kill Criterion (set BEFORE running)

- **REAPPEARS** ("unlucky pair" supported): BOTH N=64 and N=80 individually significant at
  alpha=0.05, positive sign — a genuine recovery of the signal, consistent with N=40/50 having
  been an unlucky patch rather than a real boundary.
- **CEILING_CONFIRMED** ("genuine ceiling" supported): NEITHER N=64 nor N=80 individually
  significant — extends the null pattern from N=40,50 to N=64,80, strengthening the reading that
  `omega(A)` has a real explanatory ceiling somewhere around N~35-40.
- **MIXED** (genuinely ambiguous, neither reading cleanly supported): exactly one of the two
  slices significant — reported honestly as inconclusive, not forced into either bucket.

No Fisher-combination-as-primary here (unlike `H-B2-1o`): with only 2 slices, a combined test has
even less power to discriminate heterogeneity than the 5-slice case already showed problems with,
and the whole point of this experiment is the per-slice pattern, not a combined scalar.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1o`'s own CONFIRMED-but-scoped verdict — that stands
   regardless of this result (different `N_DIM` values, genuinely new data).
2. A REAPPEARS verdict would NOT prove the N=40/50 null was purely statistical bad luck with high
   confidence — 2 more data points narrow but do not eliminate the "ceiling with occasional
   recovery" possibility; would motivate, not conclusively establish, further testing.
3. A CEILING_CONFIRMED verdict would NOT prove `omega(A)` is uninformative at ALL N>=40 for all
   possible matrix families — only for this project's specific coupling-matrix construction.
4. Does NOT establish causality.

## MCID

Individual significance (alpha=0.05, consistent positive sign) at N=64 and N=80, reported
per-slice and compared directly against the already-known N=40/50 null pattern.
