# claim.md — 20260907-chernoff-neuralode-nd-dimension-sweep

**Graph node:** `H-B2-1k` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard
**Parent:** `H-B2-1j` (pearl_registry impact 7: "M1 does NOT continue the N=2→N=8 shrinkage found
in `H-B2-1f`" — M1 grew from 158.93 (N=8) to 675.40 (N=50). Falsifiable prediction: "if
intermediate N values are tested, M1 should show a NON-monotonic profile (possibly a local
minimum somewhere between N=2 and N=50), not simple decrease-then-increase.")

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Characterizes a functional relationship (`M1` as a function of
`N_DIM`) within a fully specified deterministic construction — same framing as every prior
`H-B2-1*` experiment.

## A Methodological Refinement, Stated Explicitly

`H-B2-1f`, `H-B2-1g`, and `H-B2-1j` each used a DIFFERENT, hand-picked eigenvalue set per
experiment, and critically, `H-B2-1j`'s own convention (`most negative eigenvalue = -N_DIM`)
CONFOUNDS dimension with total spectral range — going from N=8 to N=50 changed BOTH the number of
eigenvalues AND the range they span. That confound means `H-B2-1j`'s own M1 growth finding
cannot cleanly attribute the change to "dimension" alone.

This experiment fixes that: the eigenvalue spectrum's TOTAL RANGE is held FIXED at `[-50, -1]`
for every tested `N_DIM` — only the NUMBER of eigenvalues packed into that fixed range changes.
This isolates dimension as the single varied assumption (Minimal Relaxation Rule), at the cost of
NOT being a literal reproduction of `H-B2-1f/g/j`'s own specific numbers (a deliberate,
documented scope choice, not an oversight — those experiments remain valid for what they tested).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `M1`, measured across `N_DIM ∈ {3, 4, 8, 12, 16, 24, 32, 40, 50}` (N=2 excluded — see below), with eigenvalues `[0.5] + linspace(-1, -50, N_DIM-1)` (fixed range, only count varies), `coupling_magnitude=15.0` and `seed=0` fixed (matching `H-B2-1g`/`H-B2-1j`'s own values) |
| **Falsifiable predicate** | `M1(N_DIM)` is NOT monotonic across the tested sweep — there exists a local decrease-then-increase (or increase-then-decrease) pattern, not a single monotonic trend |
| **Measurable outcome** | The full `M1(N_DIM)` sequence; whether it is monotonic (via a simple sign-change-count on consecutive differences) |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md`: no prior `H-B2-1*` experiment holds spectral range fixed
while varying `N_DIM` — every prior experiment changed both simultaneously or tested only two
widely-separated points (N=8, N=50). Confirmed genuinely novel.

## Kill Criterion (set BEFORE running)

- **CONFIRMED (non-monotonic):** the sequence of consecutive differences `M1(N_i+1) - M1(N_i)`
  changes sign at least once across the sweep — genuine non-monotonic structure.
- **REJECTED (monotonic):** all consecutive differences have the same sign — `M1` increases (or
  decreases) monotonically with `N_DIM` under this fixed-range construction.

## Edge Case Found and Fixed BEFORE Running

`N_DIM=2` was in the original sweep design but caught by a dedicated test before the real run:
with only 1 negative eigenvalue, `np.linspace(range[0], range[1], 1)` returns just the range's
start point (documented numpy behavior for `num=1`), not a placement that meaningfully spans
`SPECTRAL_RANGE` — this would have introduced a construction artifact specific to N=2 (eigenvalue
pinned at one end instead of "spanning" anything), not a genuine dimensional effect. `N_DIM=2` is
excluded; the sweep starts at `N=3`, the smallest N where `linspace` spans the range properly.

## What This Does NOT Mean

1. Does NOT reproduce `H-B2-1f/g/j`'s own specific M1 values — those used a different,
   N-dependent spectral range; this is a deliberately different, cleaner construction.
2. Does NOT generalize beyond this single seed (seed=0) — a genuinely single-realization result,
   per `H-B2-1i`'s own established caveat about seed-to-seed variability; non-monotonicity found
   here could be an artifact of this one random draw, not a general property of the construction
   family. A multi-seed version of this sweep would be the natural follow-up if this result is
   informative.
3. Does NOT imply anything about real Neural-ODE/ResNet layers of any width.

## MCID

Whether `M1(N_DIM)` is monotonic or not across the tested sweep — a binary structural fact about
the sequence, not a continuous threshold.
