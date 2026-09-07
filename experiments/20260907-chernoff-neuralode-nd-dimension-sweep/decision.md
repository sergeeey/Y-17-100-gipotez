# decision.md — H-B2-1k (is M1(N_DIM) monotonic at a fixed spectral range?)

## CORRECTION ADDENDUM (2026-09-07, FL Step 8a skeptic pass — third in a row, most severe finding)

**Verdict downgraded CONFIRMED → FALSIFIED.** Original text kept below unedited (Hindsight
Distortion Gap discipline). Third `Agent(skeptic)` invocation in the same `/loop` continuation
(after `H-B2-1l` and `H-B2-1j`, both WEAKENED) — this one found the most severe problem of the
three: the pre-registered kill criterion itself has essentially zero power to distinguish signal
from noise.

**What the skeptic found, given only `claim.md` + `run.py`:**

1. **[Confirmed — structural]** `build_matrix(n_dim)` calls `np.random.default_rng(SEED)`
   FRESH, inside the function, on every invocation. The 9 sweep points are therefore NOT "one
   coherent system probed at 9 dimensions" — they are 9 structurally independent random matrix
   draws that merely share a seed *number*, not a shared random *state*. Combined with `H-B2-1i`'s
   own already-committed finding (M1 varies ~25× across 30 independent seeds at FIXED N=8), the
   between-N swings observed here are not clearly distinguishable from ordinary seed-to-seed
   noise at a single N.
2. **[Confirmed — mathematically decisive]** The pre-registered kill criterion ("CONFIRMED if
   consecutive differences change sign at least once in the 9-point sequence") is passed by pure
   noise with probability ≈1. For 9 iid continuous draws, only 2 of `9! = 362,880` possible
   orderings are monotonic (fully increasing or fully decreasing), so `P(monotonic | pure noise)
   ≈ 5.5×10⁻⁶` and `P(≥1 sign change | pure noise) ≈ 0.999994`. **This criterion cannot fail on
   noise, and therefore cannot count as evidence of signal when it passes.** This is precisely
   the class of defect the project's own FL Step 4a exists to catch (a criterion passed by a
   construction with no real mechanism in it — normally checked via an explicit floor/null
   baseline) — this experiment's own "Note on Floor–Ceiling: not applicable" was WRONG. A
   pre-registered pass/fail criterion on a NEW quantity (here, "is a sequence monotonic") needed
   a null-model floor check even though the experiment is "descriptive," and didn't get one.
3. **[Confirmed — my own anticipated defense doesn't survive]** The original FL Step 8a section
   below explicitly anticipated "could just be sampling noise dressed up as non-monotonic" and
   responded "mitigated by magnitude" (the swings are large, not a few-percent wiggle). That
   defense is invalid: the criterion's near-certain pass under noise does not depend on the
   MAGNITUDE of the swings at all — any 9 iid draws of any scale produce a sign change with
   probability ≈1. Anticipating the right concern and answering it with the wrong argument is
   itself worth recording (this is different from `H-B2-1l`/`H-B2-1j`'s pattern of not
   anticipating the flaw at all).

**What survives:** the raw numbers themselves (the M1 sequence, provenance-verified,
byte-identical formula to every prior `H-B2-1*` experiment) are real measurements, not fabricated
or miscalculated. **What does NOT survive:** the interpretive claim that they demonstrate
"genuine non-monotonic structure" as opposed to noise — the pre-registered test could not have
told the difference either way, so CONFIRMED here is not evidence of anything beyond "9 numbers
were computed."

**Downstream consequence:** this compounds `H-B2-1l`'s own correction. `H-B2-1l`'s N-sweep leg
was already downgraded because its 9 points are one deterministic curve, not independent
samples (true, and now understood to be worse: even AS a single curve, whether it reflects a
real N-dependent trend or just 9 independent-ish noisy draws was never established by THIS
experiment's own criterion). `H-B2-1j`'s M1-growth claim (already corrected for the N/range/
coupling-size confound) was never solid ground to begin with, for the same underlying reason —
none of `H-B2-1g`, `H-B2-1j`, or `H-B2-1k` ever compared their single-draw M1 measurements
against a noise floor.

**Recommended fix (per skeptic's own suggestion), not yet built:** re-run as a genuine
multi-seed × multi-N grid (≥20-30 seeds per `N_DIM` value, reusing `H-B2-1i`'s own seed-ensemble
machinery), and replace the sign-change criterion with something that has real discriminating
power against a seed-shuffled null — e.g. a permutation test (shuffle which M1 value is assigned
to which N, count how often the shuffled data produces an equally or more "non-monotonic"
pattern than observed).

**New pearl (generalizes beyond this one experiment):** any pre-registered "≥1 sign change in a
short sequence" criterion is a Zero-Signal/Floor problem in disguise — worth auditing every prior
`H-B2-1*` verdict for the same shape before trusting it further.

**Response Matrix disposition:** Confirmed (1), Confirmed (2, the load-bearing one), Confirmed
(3). No concern is dismissible. Response: Mitigated only by a real re-design (multi-seed grid +
permutation test), not by anything already in this decision.md.

---

## Result (ORIGINAL TEXT, superseded by the correction above — kept for the audit trail)

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
