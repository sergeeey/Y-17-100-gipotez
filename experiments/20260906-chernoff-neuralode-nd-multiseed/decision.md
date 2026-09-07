# decision.md — H-B2-1i (seed-ensemble test of M1 at coupling_magnitude=15)

## Result

**Verdict: MODERATE** — `M1(seed=0)=158.93` (H-B2-1g's own reported value) is above the ensemble's
third quartile but well within the standard Tukey non-outlier fence. Not typical (not in the
central 50%), but not an "unlucky/lucky draw" outlier either.

| Statistic | Value |
|---|---|
| n seeds | 30 |
| mean | 109.14 |
| std | 97.57 |
| min | 15.00 (seed 26) |
| Q1 | 32.48 |
| median | 68.97 |
| Q3 | 143.97 |
| max | 371.36 (seed 28) |
| Tukey fence | [−134.75, 311.21] |
| **H-B2-1g's value (158.93)** | above Q3, inside Tukey fence → **MODERATE** |

## What Was Confirmed

- `M1=158.93` is **not** a representative/median draw for this construction — the ensemble
  median is 68.97, less than half of H-B2-1g's reported value. Citing 158.93 as "the" M1 for
  `coupling_magnitude=15` somewhat overstates the typical case.
- `M1=158.93` is **not** a wild statistical outlier either — it sits comfortably inside the
  Tukey non-outlier fence (max observed in the ensemble, 371.36 at seed 28, is more extreme).
- The distribution is **strongly right-skewed**: mean (109.14) noticeably exceeds median
  (68.97), min (15.00) and max (371.36) span a 25× range at fixed coupling magnitude and
  eigenvalue spectrum — only the random coupling-perturbation draw differs.
- Provenance check passed: `build_matrix_with_seed(0)` at coupling=15 reproduces H-B2-1g's own
  module-level `A` exactly, and the reference-seed `M1` computed via this ensemble's own
  machinery matches H-B2-1g's committed 158.93 to full precision.

## What Remains Open

- **Why right-skewed specifically?** Not investigated here — plausibly related to occasional
  near-degenerate eigenvalue configurations of the perturbed matrix producing large transient
  growth, but this is a hypothesis, not tested.
- This experiment is scoped to `coupling_magnitude=15` only (Minimal Relaxation Rule — one
  assumption changed, seed not coupling). Whether the SAME degree of seed-sensitivity holds at
  other coupling magnitudes (e.g. the ones swept in `H-B2-1h`) is untested — a natural next
  relaxation, but a SEPARATE experiment per the Minimal Relaxation Rule.
- 30 seeds is a modest ensemble size; the true right tail (does the distribution have a heavier
  tail than seed 28's 371.36 suggests, e.g. from rare near-resonant perturbations) is not
  well-characterized with n=30.

## Relaxation Map

- **Seed ensemble at other coupling magnitudes** (e.g. repeat at coupling=3, 30) — tests
  whether right-skew and this magnitude of seed-sensitivity are properties of strong coupling
  specifically, or general to this construction at any coupling level.
- **Larger ensemble** (e.g. n=200) — would better characterize tail behavior and give a more
  stable Q1/Q3/Tukey-fence estimate.
- **Diagnose the skew mechanism** — check whether the largest-M1 seeds correspond to
  near-degenerate or clustered eigenvalue configurations of the perturbed (non-symmetric) part.

## Note on Floor–Ceiling (FL Step 4a)

Not applicable in the arm/null-model sense — descriptive characterization of a distribution over
a fully specified stochastic construction (varying RNG seed), not a detection rule run against a
null-model floor or an oracle ceiling.

## FL Step 8a — Skeptic Pass

Not run as a separate agent invocation (Evaluator-Optimizer cap still in effect session-wide).
Manual discipline applied instead: (1) provenance independently cross-checked against H-B2-1g's
own committed value before trusting the ensemble machinery, not assumed correct because it reuses
H-B2-1h's already-verified formulas; (2) the Tukey-fence kill criterion was pre-registered in
`claim.md` BEFORE this run, avoiding a post-hoc percentile pick that could have been tuned to
whatever answer looked more interesting; (3) the finding (MODERATE, not TYPICAL, not OUTLIER) is
reported as-is rather than rounded to a more clean-sounding TYPICAL or OUTLIER verdict.

**Anticipated FALSIFIED-equivalent concern:** "30 seeds is too few to trust Q1/Q3 estimates
precisely, so MODERATE vs TYPICAL is a close call that could flip with more data." **Response:
Accepted limitation** — documented explicitly above (Relaxation Map: larger ensemble) rather than
overclaiming precision the n=30 sample doesn't support. The qualitative finding (158.93 is
above-median, right-skew is real, is not an extreme outlier) is robust to this concern even if
the exact TYPICAL/MODERATE boundary is not.

## EstimandOps — What This Does NOT Mean (restated per claim.md)

1. Does NOT generalize beyond this specific 8-dimensional eigenvalue/seed-space construction and
   this specific coupling magnitude (15).
2. Does NOT retroactively invalidate H-B2-1g's own verdict (bound holds, order matches) — that
   concerned mechanism validity, untouched by this experiment.
3. Does NOT test seed-ensembles at other coupling magnitudes — scoped to coupling=15 only.

## Pearl Card Update

**Closes H-B2-1g's own named open question** ("is M1=158.93 typical or an unlucky draw") with a
nuanced answer: neither cleanly — it's an above-median but non-outlier draw from a strongly
right-skewed distribution. The right-skew itself is a new, unexplained observation worth a future
mechanistic look (added to Relaxation Map above, not yet pearled — no falsifiable_prediction
concrete enough yet to warrant a registry row on its own).
