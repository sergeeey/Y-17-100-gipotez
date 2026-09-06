# claim.md — 20260906-lakes-tda-ews-total-persistence-iaaft-v1gprime

**Graph node:** `H-B3-1i` (new, per Minimal Relaxation Rule) · **Bridge:** `B3-MAY-TDA` · **Tier:** Standard
**Parent:** `H-B3-1g` (V1g — total persistence + AR(1) null). Named in `H-B3-1h`'s own Relaxation Map:
"Extend conjunction to include IAAFT-null and/or detrend-null total-persistence variants (not yet
computed) — Would need 1-2 new real compute runs (~25 min each), not free like this join."

> **Role of this experiment:** ONE assumption changed from `H-B3-1g` (V1g): the null-generation
> procedure — AR(1) surrogate (only lag-1 linear structure preserved) → IAAFT surrogate (full power
> spectrum + exact amplitude distribution preserved). Everything else (total persistence as the TDA
> statistic, same 9 series, same window, same embedding) unchanged — reuses `v1.cmd_run()` via
> `surrogate_fn=iaaft_surrogate` + `tda_stat_fn=betti1_total_persistence_series` together, exactly the
> same reuse pattern as every prior V1-family variant. This is the SAME null-model change already
> validated on the entropy invariant (`H-B3-1d`/V1'), now applied to the total-persistence invariant for
> the first time — a single-cell fill-in of the 2×2 (invariant × null-model) design this arc has been
> implicitly building: {entropy, total persistence} × {AR(1), IAAFT}. Three of four cells are already
> filled (V1=entropy/AR1, V1'=entropy/IAAFT, V1g=total-persistence/AR1); this is the fourth.

## Why This Cell Specifically (Not detrend-null, the other item in the Relaxation Map)

IAAFT is the cheaper, more directly comparable next step: `H-B3-1d` already validated IAAFT works
correctly in this pipeline (unit-tested, ran cleanly) and gave a clean, interpretable result (identical
5/5 to AR(1) on entropy) — a known-good null generator, only the invariant changes. detrend+IAAFT
(`H-B3-1e`/V2') requires an additional smoothing-parameter choice (`DETREND_FRAC`) that adds a second
free assumption on top of the null-model change, which would violate the Minimal Relaxation Rule if
done in the same step as extending to total persistence. Filling the IAAFT/total-persistence cell first
keeps this a clean one-assumption change from `H-B3-1g`.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 9 series as `H-B3-1c`–`h` |
| **Falsifiable predicate** | Per-series IAAFT-surrogate-null detection using TOTAL PERSISTENCE reduces the false-positive rate below V1g's 4/5 (AR(1)+total-persistence), OR reproduces the identical false-positive set (informative either way — see below) |
| **Measurable outcome** | False-positive rate on the 5 negative controls; whether the false-positive SET matches V1g's (Windermere, Loch Leven, Peter pH, Paul doSat) or V1's/V1''s entropy set, or is different again; whether Peter doSat's lead survives |

## FL Step -3: Novelty / Prior-Art Check

`grep` of `null_results/INDEX.md` and `pearl_registry/INDEX.md`: no prior attempt in this project
combined IAAFT null with total persistence — IAAFT was tested only against entropy (`H-B3-1d`), and
total persistence was tested only against AR(1) (`H-B3-1g`). This is a genuinely new combination in
this pipeline, not a repeat.

## Natural Language Statement

> "We test whether replacing the AR(1)-surrogate null with the IAAFT surrogate null (already validated
> on the entropy invariant in `H-B3-1d`), while keeping total persistence as the TDA statistic
> (unchanged from `H-B3-1g`), changes the false-positive rate or the specific false-positive series."

## L0 Classification

**Predictive** — same as every V1-family variant with a real kill_criterion (unlike the descriptive
`H-B3-1f`/`H-B3-1h` re-joins).

## Kill Criterion (set BEFORE running, per project discipline)

- **PROMOTE:** false-positive rate ≤ 1/5 with ≥1 surviving positive lead.
- **REJECT (repeat of the pattern):** false-positive rate = 4/5 or 5/5, same core series as V1g/V1'.
- **LEAD:** false-positive rate strictly better than V1g's 4/5 but worse than PROMOTE's ≤1/5, OR the
  false-positive SET differs meaningfully from every prior variant (informative regardless of count).

## What This Does NOT Mean

1. Does NOT test detrend+IAAFT on total persistence — a further, more involved next step (two
   assumptions changed from `H-B3-1g`, not one) if this one is also uninformative.
2. Does NOT, by itself, resolve why Loch Leven/Paul doSat specifically resist every method — even a
   clean result here narrows the space further without necessarily explaining the mechanism (same
   caveat as `H-B3-1h`'s own case study).
3. If this cell reproduces the SAME false-positive set as V1g (Windermere, Loch Leven, Peter pH, Paul
   doSat) despite a structurally richer null, that is strong evidence the null-model axis is fully
   exhausted for total persistence too (mirroring what `H-B3-1d`/`H-B3-1e` already showed for entropy) —
   would complete the null-model-exhaustion finding across BOTH invariants, not just one.

## MCID

Same bar as every V1-family variant: false-positive rate ≤ 1/5 with ≥1 surviving positive lead for
PROMOTE.
