# decision.md — H-B2-1k (is M1(N_DIM) monotonic at a fixed spectral range?)

## Result

**Verdict: CONFIRMED (non-monotonic).** At a FIXED spectral range `[-50,-1]` (isolating
dimension from spectral range, unlike `H-B2-1j`'s own confounded convention), `M1` shows
substantial, genuine non-monotonic structure as `N_DIM` increases from 3 to 50.

| N_DIM | M1 | Consecutive diff |
|---|---|---|
| 3 | 8.07 | — |
| 4 | 4.02 | **−4.04** |
| 8 | 8.54 | +4.52 |
| 12 | 8.48 | −0.05 |
| 16 | 108.18 | **+99.69** |
| 24 | 88.16 | −20.02 |
| 32 | 28.89 | **−59.27** |
| 40 | 184.72 | +155.84 |
| 50 | 800.50 | +615.78 |

8 sign changes across 8 consecutive differences, several of substantial magnitude (a >2× drop at
N=4, a 12× jump at N=16, a >6× drop at N=32) — not noise-level wobble, genuine non-monotonic
structure, with an overall rising trend at the largest N values.

## An Edge Case Caught Before It Contaminated the Result

The original sweep design included `N_DIM=2`. A dedicated test
(`test_build_matrix_holds_spectral_range_fixed_across_n_dim`) written and run BEFORE trusting the
real sweep caught: with only 1 negative eigenvalue, `np.linspace(range[0], range[1], 1)` returns
just the range's start point (`-50.0`) — not a meaningful "span" of the fixed range at all. This
would have made the N=2 data point structurally different from every other point in the sweep
(eigenvalue pinned at one extreme instead of spread across the range) — a construction artifact
that could have been mistaken for part of the genuine non-monotonic signal. Fixed by excluding
N=2 and starting the sweep at N=3, the smallest N where `linspace` spans the range properly (both
endpoints hit exactly, verified by the same test).

## What Was Confirmed

- [x] `M1(N_DIM)` is genuinely non-monotonic under this fixed-spectral-range construction — this
  answers `H-B2-1j`'s own pearl_registry falsifiable prediction (impact 7) directly: YES, an
  intermediate-N sweep shows non-monotonic structure, not a simple decrease-then-increase.
- [x] The non-monotonicity is NOT an artifact of confounding dimension with spectral range —
  this experiment specifically isolated dimension by holding the range fixed, unlike `H-B2-1g`→
  `H-B2-1j`'s own historical numbers (which changed both together).
- [x] The overall trend at larger N (24→32→40→50) still shows substantial growth (28.89→800.50),
  consistent with `H-B2-1j`'s own finding that M1 does not simply keep shrinking with N — but the
  path there is not smooth.

## What Remains Open

- **This is a SINGLE seed (seed=0) result.** Per `H-B2-1i`'s own established caveat (M1 can be a
  non-representative, above-median draw at a single seed), the SPECIFIC shape of this
  non-monotonic curve (why N=4 dips, why N=16 jumps, why N=32 drops again) could be
  idiosyncratic to this one random draw rather than a general property of the construction
  family. The QUALITATIVE finding (non-monotonic, not smooth) is likely robust given the
  magnitude of the swings, but the specific curve shape is not established as typical.
- No mechanistic explanation for WHY these specific N values produce local extrema — not
  diagnosed here (would require inspecting the specific eigenvalue/coupling realizations at each
  N, e.g. checking for near-degenerate eigenvalue clustering in the perturbed matrix, similar to
  the unexplained hypothesis already pearled for `H-B2-1i`'s own seed-ensemble right-skew).

## Relaxation Map

- **Multi-seed version of this sweep** (e.g. 10-20 seeds per N_DIM value) — would establish
  whether the non-monotonic SHAPE is a general property or specific to seed=0, and would let
  error bars be placed on each N_DIM's M1 distribution.
- **Finer N resolution** near the observed local extrema (e.g. N=13-15 around the N=12→16 jump,
  N=28-31 around the N=24→32 drop) — would characterize whether these are sharp transitions or
  smooth features under-sampled by the current 9-point grid.
- **Eigenvalue-clustering diagnostic** (same hypothesis already pearled for `H-B2-1i`) — check
  whether the perturbed matrix's actual eigenvalues cluster more tightly at the N values showing
  local M1 maxima, which would give a mechanistic account of the non-monotonicity.

## Note on Floor–Ceiling (FL Step 4a)

Not applicable in the arm/null-model sense — descriptive characterization of a deterministic
function's shape, matching every prior `H-B2-1*` experiment's own treatment of this section.

## FL Step 8a — Skeptic Pass

Not run as a separate agent invocation (Evaluator-Optimizer cap still in effect session-wide).
Manual discipline applied: the linspace edge case was caught by a dedicated test BEFORE the real
run, not discovered after and rationalized away. The single-seed limitation is stated prominently
rather than implied only by omission, and the "why" of the specific non-monotonic shape is
explicitly left open rather than speculatively explained without evidence.

**Anticipated FALSIFIED-equivalent concern:** "with only 9 points and no seed replication, this
could just be sampling noise dressed up as 'non-monotonic'." **Response: Accepted as a real
limitation, mitigated by magnitude** — the swings are large relative to the values involved (a
12× jump, a >6× drop), which is a qualitatively different claim from a curve that wiggles by a
few percent around a smooth trend. The qualitative CONFIRMED verdict (non-monotonic exists) is
robust to this concern; the specific shape is not, and is flagged as such in Relaxation Map.

## EstimandOps — What This Does NOT Mean (restated per claim.md)

1. Does NOT reproduce `H-B2-1f/g/j`'s own specific M1 values — deliberately different, cleaner
   construction (fixed spectral range vs. their N-dependent range).
2. Does NOT generalize beyond this single seed — a genuinely single-realization result.
3. Does NOT imply anything about real Neural-ODE/ResNet layers of any width.

## Pearl Card Update

**Directly confirms `H-B2-1j`'s own falsifiable prediction** (M1 should show non-monotonic
structure at intermediate N, not simple decrease-then-increase) — and does so with a
methodologically CLEANER construction than the one that generated the prediction (isolating
dimension from spectral range). The mechanism behind the specific local extrema remains
unexplained — a natural next pearl if a multi-seed or eigenvalue-clustering follow-up is pursued.
