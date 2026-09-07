# decision.md — 20260907-chernoff-neuralode-nd-pseudospectral-crossimpl (H-B2-1s)

## Result

Pre-registered criterion: **CONFIRMED**. Both large-N slices individually significant under the
INDEPENDENT (`pseudopy`) implementation, with close value agreement well inside the 15% tolerance.

| N_DIM | rho(mine, pseudopy) | median rel. diff | max rel. diff | mine: rho, p | pseudopy: rho, p |
|---|---|---|---|---|---|
| 40 | 0.995 | 2.4% | 4.7% | 0.821, 0.00018 | 0.785, 0.00053 |
| 50 | 0.989 | 2.7% | 5.6% | 0.824, 0.00016 | 0.804, 0.00030 |

Both slices: `verdict_agrees = true` (both implementations independently classify the M1
correlation as significant and positive). Rank agreement between the two implementations
(0.995, 0.989) is about as strong as two independent numerical routines measuring the same
continuous quantity typically get.

## This Closes Skeptic Concern #5 From H-B2-1r (Response Matrix Update)

`H-B2-1r`'s FL Step 8a skeptic pass named "no cross-implementation check against an established
tool (pseudopy, EigTool)" as the one remaining, undone limitation — "the load-bearing gap." This
experiment closes it:

| Concern (from H-B2-1r) | Status before | Status now |
|---|---|---|
| #5 — no cross-implementation check | Named, not done | **Done.** `pseudopy==1.2.5`, an independently-written package, reproduces both the ranking (rho>=0.99) and the statistical conclusion (both slices significant, positive) of `H-B2-1r`'s own routine at exactly the two large-N slices the main conclusion rests on |

## A Minor Bug Was Found and Fixed Before This Result Was Trusted

First run of the full test suite crashed at the JSON-serialization step (`TypeError: Object of
type bool is not JSON serializable`) — `numpy.bool_` results from boolean comparisons on numpy
floats (`p_pseudopy_m1 < ALPHA and rho_pseudopy_m1 > 0`) are not plain Python `bool` and
`json.dumps` rejects them. **The expensive computation itself (all 30 matrices through
`pseudopy`, ~6.7 minutes) completed successfully both times** — this was purely a
result-serialization bug, not a computational one, confirmed by the fact the fixed version
(`bool(...)` wrapping) reproduced numerically identical `rho`/`p` values on re-run. Fixed by
explicit `bool()` casts; no other logic changed.

## Reviewer Finding, Fixed Before Merge (P2, not statistical — code-level)

The mandatory CLAUDE.md reviewer pass (3+ files changed) caught a real, if minor, logic gap:
the original `any_slice_lost_significance` check only tested `pseudopy_vs_m1`'s significance in
isolation, never actually comparing it against `mine_significant_positive` (computed but left
unused) — the `verdict_note`'s own wording ("loses significance") implied a before/after
comparison the code didn't perform. Fixed: the verdict now consults the already-computed
`verdict_agrees` field per slice directly. A companion test gap (asserting only that the SOURCE
json had 15 seeds, never that `cmd_run()`'s own output keys matched it) was fixed with a direct
key-equality + value-equality test. **The verdict itself is unchanged (CONFIRMED, unaffected by
the fix)** — re-run after the fix reproduced numerically identical results; this was a
robustness/clarity fix for a case that didn't actually occur in this run's data, not a
correction of the reported numbers.

## Honest Scope of This Verification (per claim.md's own caveat)

This is cross-**implementation** (two independently written codebases), not cross-**algorithm**
— both `H-B2-1r`'s own routine and `pseudopy.NonnormalMeshgrid` use grid search + per-point SVD
of `zI-A`. Per the Independent Verification Strength Ladder
(`falsification-ladder.md`), this sits at "independently-written code" — real and useful, but it
would not catch a bug shared by the grid-search approach itself. Given `H-B2-1r`'s own
local-vs-global convergence check (a different verification, using a different grid geometry) had
already shown convergence, and now a THIRD, fully independent codebase agrees within ~5%, the
combined weight of evidence is strong for this specific claim, even though a genuinely different
algorithm (e.g. the Guglielmi-Overton continuation method) was not tried.

## Kill Analysis

**What this experiment killed:** the specific possibility that `H-B2-1r`'s grid-search
implementation had an implementation-specific bug (beyond the one already found and fixed)
producing a spurious correlation at N=40/N=50 — an independently written codebase reproduces both
the values and the statistical conclusion closely.

**What this experiment did NOT kill / test:** whether a fundamentally different algorithm for
computing pseudospectra (not grid+SVD) would agree — named as a residual, smaller limitation.

## What This Does NOT Mean

1. Does NOT constitute a cross-ALGORITHM check — see honest scope above.
2. Does NOT change any verdict outside the `alpha_eps(A)` vs M1 claim at N=40,50 specifically.
3. Does NOT establish causality.
4. Per the user's own stated roadmap, this experiment's CONFIRMED verdict is what gates moving to
   Priority 2 (a fresh confirmatory experiment on new seeds/matrices, with `kappa(V)`/`omega(A)`
   as pre-registered comparators, not new hypotheses) — that next step is named here, NOT
   launched automatically.

## Relaxation Map / Next Steps (not auto-launched)

- **Priority 2 (user's own plan, now unblocked):** a fresh confirmatory experiment on NEW
  seeds/matrices (not the ones already used across `H-B2-1r`/`H-B2-1s`), with pseudospectral
  abscissa as the primary descriptor, `kappa(V)` and `omega(A)` as pre-registered comparators
  (not new hypotheses evaluated after seeing results), one pre-registered effect criterion, N=40
  and N=50 as the primary large-N regime. This is a genuinely new experiment requiring its own
  claim.md — named, not launched automatically per this session's standing discipline.
- **Priority 3 (deferred further, per user's own explicit ordering):** mechanistic analysis of
  WHY pseudospectral abscissa succeeds where the other two fail (resolvent amplification -> Kreiss
  constant -> transient growth -> Chernoff bound constant M1) — only after Priority 2.

## Pearl Registry Update

Closes the `H-B2-1r` entry about the missing cross-implementation check — resolved CONFIRMED,
with numbers (rank correlation ~0.99, value agreement within ~5%), not left open. New process
note: `pseudopy` required a one-line shapely compatibility shim to run on a modern environment —
worth remembering as a reusable pattern if this or another unmaintained pseudospectral package is
needed again.
