# claim.md — 20260906-chernoff-neuralode-nd-multiseed

**Graph node:** `H-B2-1i` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard
**Parent:** `H-B2-1g` (Relaxation Map: "Multiple seeds at strong coupling — would show whether
`M1=158.93` is typical or a particularly unlucky draw." Still open after `H-B2-1h`'s coupling
sweep, which used seed=0 throughout for direct comparability, per its own explicit scope limit.)

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** This experiment characterizes the DISTRIBUTION of `M1` over an
ensemble of random matrix draws (RNG seed varied, everything else fixed) at one fixed coupling
magnitude — not an intervention, not a causal claim. It asks where H-B2-1g's single reported
value sits within that distribution.

## Why This Experiment, Specifically

`H-B2-1g` reported `M1=158.93` at `coupling_magnitude=15` from a SINGLE seed (0). Every
downstream citation of this number (including this session's own `H-B2-1h` provenance checks)
implicitly treats it as representative. Whether it is typical or an unlucky/lucky single draw
has never been tested — named explicitly in `H-B2-1g`'s own Relaxation Map and left untested by
`H-B2-1h` on purpose (that experiment varied `coupling_magnitude`, not seed, to stay comparable).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `M1`, measured at FIXED `coupling_magnitude=15` (H-B2-1g's own tested value) and FIXED eigenvalue set (`H-B2-1f/g`'s own 8-dim spectrum), across an ensemble of `N_SEEDS=30` different RNG seeds (`0..29`) — only the random coupling-perturbation matrix draw varies |
| **Falsifiable predicate** | `H-B2-1g`'s own seed=0 draw (`M1=158.93`) is a TYPICAL draw from this ensemble (falls within the ensemble's interquartile range), not a statistical outlier |
| **Measurable outcome** | Distribution of `M1` over 30 seeds: median, IQR (Q1, Q3), and Tukey outlier fences (`Q1 - 1.5×IQR`, `Q3 + 1.5×IQR`); report where `M1(seed=0)` falls relative to these |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md` / `null_results/INDEX.md`: no prior seed-ensemble test in
this project. `H-B2-1g`'s own decision.md names this exact question ("is `M1=158.93` typical or
a particularly unlucky draw") as untested. First test of it.

## Kill Criterion (set BEFORE running) — standard Tukey fences, not an ad hoc percentile pick

- **TYPICAL:** `M1(seed=0)` falls within `[Q1, Q3]` (the ensemble's own interquartile range).
- **MODERATE (not typical, not an outlier):** falls outside `[Q1, Q3]` but within the standard
  Tukey non-outlier fence `[Q1 - 1.5×IQR, Q3 + 1.5×IQR]`.
- **OUTLIER (unlucky/lucky draw):** falls outside the Tukey fence — a standard, pre-defined
  threshold, not chosen after seeing the data.

## What This Does NOT Mean

1. Does NOT generalize beyond this SPECIFIC 8-dimensional eigenvalue/seed-space construction and
   this SPECIFIC coupling magnitude (15) — a different spectrum or coupling level could show a
   different typicality picture.
2. Does NOT retroactively invalidate `H-B2-1g`'s own verdict (bound holds, order matches) even
   if `M1=158.93` turns out to be an outlier — that verdict concerned mechanism VALIDITY, which
   this experiment does not re-test; it only characterizes how representative the CONSTANT was.
3. Does NOT test seed-ensembles at OTHER coupling magnitudes (e.g. the ones swept in `H-B2-1h`)
   — this experiment is scoped to `coupling_magnitude=15` only, matching `H-B2-1g` exactly, per
   the Minimal Relaxation Rule (one assumption changed: seed, not coupling).

## MCID

Whether `M1(seed=0)=158.93` sits inside or outside the ensemble's Tukey non-outlier fence —
reported as a fact, not a threshold pass/fail on a separate metric.
