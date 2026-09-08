# decision.md — 20260908-chernoff-neuralode-nd-kreiss-crossimpl-smalleps (H-B2-1v)

## Result — the raw verdict string is misleading, read this section first

`cmd_run()`'s mechanical verdict is `GRID_SEARCH_ARTIFACT_SUSPECTED` (triggered because
`any_plateau_detected=True`). **This is a genuine result of the pre-registered logic, but the
3-way enum in `claim.md`'s Kill Criterion turned out too coarse for what actually happened** —
the real, per-matrix picture is a COHERENT one, not "grid-search is wrong":

| Matrix | grid @ eps=0.02 | pseudopy @ eps=0.02 | rel diff | pseudopy plateau? | interpretation |
|---|---|---|---|---|---|
| seed=301, N=50 (highest K) | 261.74 | 262.95 | 0.46% | **No** — still climbing to eps=0.0001 | confirms `H-B2-1u`'s non-convergent growth is a genuine matrix property |
| seed=304, N=50 (mid K) | 161.07 | 167.93 | 4.26% | **No** — still climbing to eps=0.0001 | same, confirms non-convergence |
| seed=307, N=40 (lowest K) | 30.20 | 35.66 | 18.09% | **Yes** — growth factor -> 1.01 | genuinely converges within the tested range, true K approx 47 |

**Correct reading:** the "plateau" belongs to the matrix with the SMALLEST Kreiss constant, not to
a contradiction of `H-B2-1u`'s worst-case finding. This is consistent with (not evidence against)
the structural-limitation explanation in `H-B2-1u`'s Convergence Caveat: matrices with a small
true `K(A)` reach their supremum at moderate `eps` and are fully resolved within this experiment's
tested range; matrices with a LARGE true `K(A)` (seed=301, seed=304) require correspondingly
smaller `eps` to see their own plateau, which this experiment's range (down to `1e-4`) still did
not reach for either of them. Both behaviors were independently reproduced by `pseudopy` — a
structurally different algorithm from the box-grid — which is exactly the kill criterion's
POSITIVE case (agreement + continued non-convergence for the matrices that don't plateau).

## Supplementary Direct Comparison — seed=301, N=50, down to eps=0.001

`H-B2-1u`'s own `metrics/run.json` only stored `ratios_by_eps` for `eps>=0.02` (its production
`EPS_VALUES`), so the automated `comparison` table above has `grid=None` for `eps<0.02` — a real
design gap in this experiment (the comparison baseline should have included the deeper values
`H-B2-1u`'s own diagnostic follow-up already computed, but that data lived only in a script's
printed output, not a stored artifact). Filled in manually here from
`tooling-eval/diagnostics/h_b2_1u_seed301_n50_kreiss_eps_convergence_check.py`'s own
(reproducible) numbers:

| eps | grid-search (diagnostic script) | pseudopy (this experiment) | rel diff |
|---|---|---|---|
| 0.02 | 262.9 | 262.95 | 0.02% |
| 0.01 | 437.7 | 434.59 | 0.71% |
| 0.005 | 723.3 | 723.02 | 0.04% |
| 0.002 | 1377.8 | 1375.12 | 0.19% |
| 0.001 | 2208.5 | 2206.53 | 0.09% |

**Sub-1% agreement at every point down to eps=0.001, between two structurally different
algorithms.** This is the strongest, most direct confirmation in this experiment: `H-B2-1u`'s
grid-search growth pattern on the worst-case matrix is genuinely reproduced by an independent
method, not an artifact of the box grid.

## The eps=0.02 discrepancy pattern — grid-search's known undershoot, now visible in relative terms

The three matrices' relative discrepancy at `eps=0.02` (0.46%, 4.26%, 18.09%) INCREASES as the
matrix's own `K` decreases. This is consistent with grid-search's own documented undershoot bias
(same mechanism as `H-B2-1r`'s original bug and `H-B2-1u`'s Convergence Caveat: the grid step is
fixed in absolute terms, `~0.65` for `H-B2-1u`'s arc-wide grid) — for a small-`K` matrix, the
`(alpha_eps - alpha) ` difference itself is small, so a fixed absolute undershoot becomes a much
larger RELATIVE error. Not a new finding, but a clean confirmation of the mechanism already
understood, now visible because this experiment spans a wider range of `K` magnitudes than any
single prior experiment did.

## FL Step 8a — Skeptic-Style Self-Check (informal, no separate agent invocation — see below)

**Concern anticipated:** "you pre-registered a 3-way verdict enum and then explained away the
actual mechanical output — isn't that exactly the AOG (Anti-Overfitting Gate) failure mode of
rescuing a hypothesis after the fact?" **Response:** No — the KILL CRITERION's substance (does
pseudopy agree with grid-search where both are tested, and does it show non-convergence where
grid-search showed non-convergence) is fully satisfied and reported above with numbers, not
narrative. What was wrong was the LABELING logic (`any_plateau -> artifact_suspected`), which
conflated "a plateau exists somewhere in the population" with "a plateau exists WHERE grid-search
claimed non-convergence" — a real design flaw in `run.py`'s verdict computation, disclosed here
rather than patched to hide it. The underlying data is reported in full above; a reader can verify
the conclusion (agreement + genuine per-matrix convergence heterogeneity) directly from the
numbers, not from my characterization of them.

## Kill Analysis

**What this experiment killed:** the possibility that `H-B2-1u`'s non-convergent small-eps growth
was purely an artifact of its own 2D box-grid method — an independently-implemented,
structurally-different algorithm reproduces the same pattern for the two matrices where
`H-B2-1u` found it (seed=301, seed=304), agreeing within <1% down to eps=0.001 on the primary
matrix.

**What this experiment did NOT kill, and newly confirmed:** grid-search's known undershoot bias
(documented since `H-B2-1r`) — visible again here, more clearly, across a wider `K` range.

**New, genuinely additional finding:** Kreiss-constant convergence behavior is matrix-dependent —
small-`K` matrices (seed=307) plateau within a moderate eps range; large-`K` matrices
(seed=301, seed=304) do not, at least not within `[1e-4, 2e-2]`. This is a real, useful piece of
information for anyone continuing this line (e.g. the "tighter predictor" research direction named
as Step 3 of the user's own roadmap): the required eps depth to characterize `K(A)` scales with
`K(A)` itself, not a fixed small value.

## What This Does NOT Mean

1. Does NOT mean grid-search was systematically wrong in `H-B2-1u` — the two matrices that showed
   non-convergence there ALSO show it here, independently confirmed.
2. Does NOT establish a converged, final value for `K(A)` on the two large-K matrices — both
   methods still show growth at `eps=0.0001`; only the small-K matrix (seed=307) is resolved.
3. Does NOT retroactively change `H-B2-1u`'s `MECHANISM_VERIFIED` verdict in any direction.
4. Does NOT mean the automated `verdict` field in `metrics/run.json`
   (`GRID_SEARCH_ARTIFACT_SUSPECTED`) is the correct summary — it is a real, disclosed limitation
   of this experiment's own pre-registered labeling logic, superseded by this decision.md's
   per-matrix reading. Any future automated re-read of `run.json` alone (without this decision.md)
   would draw the wrong conclusion — flagged explicitly here and in `graph.yaml`/`pearl_registry`
   so this doesn't silently propagate.

## Relaxation Map / Next Steps (not auto-launched)

- User's own roadmap: Step 2 (close B2 arc documentation) and Step 3 (tighter predictor/bound
  research) are next. This experiment's finding that convergence depth scales with `K(A)` is
  directly useful context for Step 3.
- Not pursued here: extending `EPS_VALUES` even smaller to find the plateau for seed=301/seed=304
  — would need proportionally finer `AUTO_KWARGS` resolution (more `n_circles`/`n_points`, likely
  significant compute), and the qualitative point (grid-search's growth pattern is real, not an
  artifact) is already established with the current data.

## Pearl Registry Update

New, general finding: Kreiss-constant grid-search/circle-based convergence depth scales with the
matrix's own true `K(A)` magnitude — small-K matrices converge within a moderate eps range,
large-K matrices need correspondingly smaller eps. Any future experiment estimating `K(A)` for a
NEW matrix should first get a rough magnitude estimate (e.g. one coarse eps value) before
committing to a fixed eps range, rather than assuming one range serves all matrices in a
population.
