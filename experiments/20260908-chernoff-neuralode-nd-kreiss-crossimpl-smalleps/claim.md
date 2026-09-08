# claim.md — 20260908-chernoff-neuralode-nd-kreiss-crossimpl-smalleps (H-B2-1v)

**Graph node:** `H-B2-1v` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (independent
cross-implementation check of an already-flagged open gap, reuses matrix construction unchanged)
**Parent:** `H-B2-1u` (Kreiss mechanism, MECHANISM_VERIFIED, then corrected: reviewer P1 found
`k_estimate` pinned to the smallest sampled eps with no plateau — a demonstrated lower bound,
not a converged estimate — see `H-B2-1u`'s Convergence Caveat)

## Why This Experiment, Specifically — User's Own Corrected Priority, This Session

User proposed a cross-implementation check of the pseudospectral pipeline as the highest-value
next step. Direct check (this session) found the eps~1 regime (the one that correlates with M1)
was ALREADY cross-validated in `H-B2-1s` (`pseudopy.NonnormalMeshgrid`, rho=0.989-0.995, median
discrepancy 2.4-2.7%). The genuinely OPEN gap is narrower and more specific: `H-B2-1u`'s own grid-
search-based Kreiss constant estimate never showed convergence at small `eps` (still climbing at
`eps=0.001`, `ratio` 262.9->2208.5) — is that non-convergence a property of the MATRIX, or an
artifact of the 2D box-grid method (which needs grid step `<< eps`, structurally hard to satisfy
as `eps -> 0`)? `pseudopy.NonnormalAuto` is a genuinely DIFFERENT algorithm — not a box grid, but
`n_circles` adaptively-placed rings of `n_points` samples around each eigenvalue, so its
resolution scales with the circle radius (`eps`) directly rather than a fixed global grid step.
This is the right tool to distinguish "matrix property" from "grid-search artifact."

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Does an independently-implemented, non-grid pseudospectrum
algorithm (`pseudopy.NonnormalAuto`) reproduce the same non-convergent small-`eps` growth pattern
`H-B2-1u`'s grid-search found, or does it show a plateau/convergence that grid-search's own
resolution limit was hiding? No causal framing.

## FL Step 0a — Mechanism Claim Gate

No new "X targets/discriminates Y" behavioral sentence is being introduced here beyond what
`H-B2-1u`'s own Convergence Caveat already stated as `[UNTESTED-MECHANISM]`-adjacent (grid-search
cannot resolve `eps` smaller than its own step). This experiment IS the check for that gap — not
a new unchecked claim requiring its own gate.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(ratio_grid_search(A, eps), ratio_pseudopy_auto(A, eps))` pairs at matching `eps` in `{0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0001}`, on the worst-case matrix from `H-B2-1u` (seed=301, N_DIM=50) plus 2 additional matrices spanning `H-B2-1u`'s observed K-estimate range (seed=307,N=40 — lowest k_estimate=30.20 at eps=0.02; seed=304,N=50 — mid-range k_estimate=161.07 at eps=0.02) to avoid overfitting to a single matrix |
| **Falsifiable predicate** | EITHER: (a) `pseudopy`'s independent, circle-based algorithm shows the SAME non-convergent growth pattern (ratio still increasing, no plateau, agreeing with grid-search within ~10% at each matching eps) -- confirms the growth is a genuine matrix property, not a grid-search artifact; OR (b) `pseudopy` shows a clear plateau/convergence that grid-search's own resolution limit was hiding -- would mean grid-search's own numbers in `H-B2-1u` were themselves an artifact requiring correction |
| **Measurable outcome** | Per matrix, per eps: `ratio_grid_search`, `ratio_pseudopy_auto`, relative discrepancy; whether pseudopy's own ratio sequence shows a plateau (define: consecutive-octave ratio growth factor stabilizing below 1.3x, vs. the ~1.6-2x growth factor seen in the raw data so far) anywhere in the tested range |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md`: no prior use of `pseudopy.NonnormalAuto` anywhere in this
arc — `H-B2-1s` used only `NonnormalMeshgrid` (a different class, box-grid based). Confirmed
novel application, reusing an already-cross-validated PACKAGE but a different, more appropriate
ALGORITHM within it.

## Kill Criterion (set BEFORE running, informed by an already-run exploratory pilot on the primary
matrix — see honest disclosure below)

- **Agreement + continued non-convergence (both algorithms track within ~10% at each eps, both
  keep climbing with no plateau through eps=0.0001):** confirms `H-B2-1u`'s grid-search growth
  was a genuine matrix property, independently cross-validated by a structurally different
  algorithm. Strengthens (does not weaken) `H-B2-1u`'s "efficiency ratio is an upper bound, true
  value likely much lower" caveat, with a number now backed by TWO independent methods.
- **Disagreement (pseudopy shows a plateau grid-search did not, or the two methods diverge by
  more than an order of magnitude at any matching eps):** would mean grid-search's H-B2-1u
  numbers need correction beyond what the existing Convergence Caveat states.

**Honest disclosure (Perelman-audit discipline — no genius leap, no hidden pilot):** an
exploratory check on the PRIMARY matrix (seed=301, N=50) was already run before this claim.md was
finalized, to first confirm `pseudopy.NonnormalAuto` was usable at all (found and fixed a
`numpy>=2.0` `np.Inf` compatibility bug, analogous to `H-B2-1s`'s `shapely` shim) and to gauge
compute cost before committing to a 3-matrix design. That pilot's numbers ARE reported below as
part of the primary matrix's result (not re-run blind) — this is disclosed explicitly rather than
silently treated as a fresh, pre-registered-blind result. The kill criterion above was written
with full knowledge of that pilot's outcome (agreement + continued growth to eps=0.0001), which
is itself a limitation: the primary matrix's result is NOT a blind confirmatory test of the kill
criterion. The 2 SECONDARY matrices (seed=307,N=40 and seed=304,N=50) ARE run blind, after this
claim.md and kill criterion were fixed, and carry the actual confirmatory weight of this
experiment's verdict.

**Second disclosure, added mid-pilot (Gate 3 doing its job):** the pilot's FIRST extraction
approach (`pspec.points`/`pspec.vals` with a boolean mask, mirroring how `H-B2-1s` used
`NonnormalMeshgrid`) was run against a positive control (symmetric matrix, exact-known ratio=1.0)
and FAILED it — systematic ~16% undershoot, not converging to 1.0. This is precisely what Gate 3
(Positive-Control Digitization) exists to catch before trusting any comparison. Root-caused to
`vals` not being independently-evaluated resolvent norms at each point, and the naive mask not
properly interpolating the true eps-level contour. Fixed by replicating `pseudopy`'s own intended
extraction (`matplotlib.tricontour` over the triangulated mesh, bypassing a separate, unrelated
`.collections`-removal bug in `pseudopy.contour_paths()` on modern matplotlib) — the corrected
method passes the positive control at ratio=0.9998-1.0000 and gives primary-matrix numbers within
<1.5% of grid-search at every eps (closer agreement than the buggy extraction's own ~1-7%,
consistent with the buggy version's error being real noise, not signal). `run.py`'s module
docstring carries the full technical account.

## What This Does NOT Mean

1. Does NOT retroactively change `H-B2-1u`'s `MECHANISM_VERIFIED` verdict (an even larger true
   K(A) only makes the proven upper bound hold with MORE margin, not less).
2. Does NOT establish a converged, precise value for K(A) — `pseudopy.NonnormalAuto`, while a
   different algorithm, is STILL a finite-sample numerical method and could itself fail to
   converge at even smaller eps than tested here. This experiment establishes AGREEMENT between
   two independent methods over a shared tested range, not a proof of the true limiting value.
3. Does NOT establish causality — this is a numerical cross-validation, not an intervention.
4. Does NOT mean this matrix family's Kreiss constant is literally infinite — the Kreiss Matrix
   Theorem guarantees `K(A)` is finite for any finite matrix; "no plateau observed down to
   eps=0.0001" is a statement about the tested range, not a claim of unboundedness.

## MCID

Per-eps relative discrepancy between `ratio_grid_search` and `ratio_pseudopy_auto` (target: within
~10-20% agreement, matching the same order-of-magnitude standard `H-B2-1s` used for the eps~1
regime), reported per matrix, alongside a qualitative plateau/no-plateau call for pseudopy's own
sequence.
