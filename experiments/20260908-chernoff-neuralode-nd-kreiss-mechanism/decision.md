# decision.md — 20260908-chernoff-neuralode-nd-kreiss-mechanism (H-B2-1u)

## Result

**MECHANISM_VERIFIED.** The proven Kreiss upper bound `sup_t||exp(tA)|| <= e*n*K(A)` holds for
all 20/20 sampled matrices (10 seeds x N_DIM in {40, 50}), after fixing a real sampling gap in
this experiment's own first-draft `EPS_VALUES` (see Bug/Fix below). This is not a "confirmed
hypothesis" in the FL sense — a proven theorem cannot be confirmed by data, only have its
computation checked — the substantive finding is the **efficiency ratio** distribution: how
much of the theoretical ceiling the observed transient growth actually reaches.

| N_DIM | efficiency median | efficiency min | efficiency max | upper bound violations |
|---|---|---|---|---|
| 40 | 0.0368 | 0.0227 | 0.0698 | 0/10 |
| 50 | 0.0632 | 0.0305 | 0.3099 | 0/10 |

**Interpretation (per claim.md's own pre-registered "What This Does NOT Mean" #2):** efficiency
is low across the board (median 3.7-6.3%, one outlier at 31%) — the Kreiss upper bound holds
comfortably but is LOOSE for this matrix family. This is informative, not disappointing: it means
`e*n*K(A)` is a mathematically valid but far-from-tight ceiling here, consistent with the known
general looseness of the Kreiss Matrix Theorem's `e*n` factor (a classical, acknowledged
limitation of the theorem itself, not of this arc's computation) — the theorem gives existence
and an order-of-magnitude bound, not a sharp estimate.

## Bug/Fix History — Found By This Experiment's Own Kill Criterion

**First draft** used `EPS_VALUES=(0.5,1.0,1.5,2.0,3.0)` reusing `pseudospectral_abscissa`'s
arc-wide default grid (`RE_MIN..RE_MAX=-5..60`, `N_RE=100` -> step 0.65). Result: **1/20
apparent violations** of the proven upper bound — seed=301, N_DIM=50: `growth=11025.75 >
ceiling=3104.06` (from `k_estimate=22.84`). Per `claim.md`'s own pre-registered Kill Criterion,
a violation of a PROVEN theorem cannot be a real result — it meant "investigate before reporting
a verdict," not "report `CODE_BUG_SUSPECTED` and stop."

**Investigation (Causal Debugging Protocol, `integrity.md`):**
1. *What changed?* New code (`kreiss_constant_estimate`, `raw_transient_growth`) — the reused
   `pseudospectral_abscissa` (twice independently verified, `H-B2-1r`/`H-B2-1s`) was not touched.
2. *What does the error say?* One matrix's ceiling was ~3.5x below its observed growth.
3. *What assumptions was I making?* That `EPS_VALUES` in `[0.5, 3.0]` would find the region
   where `(alpha_eps(A)-alpha(A))/eps` is maximized. Untested assumption.
4. *Simplest reproduction?* Recompute `alpha_eps` for the SAME matrix (seed=301, N=50) at
   smaller `eps` with a locally-refined grid (script kept at
   `tooling-eval/diagnostics/h_b2_1u_seed301_n50_kreiss_eps_scan.py`).

**Finding:** `build_matrix_with_seed_and_n` constructs a genuinely upper-triangular matrix
(diagonal + strictly-upper-triangular random coupling, `H-B2-1m`) — a near-nilpotent, strongly
non-normal structure. For this matrix family the TRUE Kreiss-constant supremum lives in the
SMALL-eps regime, not `eps>=0.5`:

| eps | ratio (K-candidate) |
|---|---|
| 3.000 | 6.59 |
| 1.000 | 14.08 |
| 0.500 | 23.46 (≈ the original k_estimate=22.84 at the coarser global grid) |
| 0.100 | 78.77 |
| 0.050 | 130.73 |
| 0.020 | **259.78** |

An 11x jump between the original sample's max (`eps=0.5`) and `eps=0.02`. Corrected ceiling with
`K≈260`: `e*50*260 ≈ 35313`, comfortably above the observed `growth=11025.75`.

**Verdict on this finding:** a SAMPLING gap in this experiment's own new code — `EPS_VALUES`
never probed the eps region where this specific matrix family's supremum actually lives — not a
bug in the already-twice-independently-verified `pseudospectral_abscissa`, and not evidence
against the theorem. Consistent with `H-B2-1r`'s own precedent (that experiment's real bug was
also caught by checking against a proven bound, not by "it looks plausible").

**Fix:** widened `EPS_VALUES` to `(0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0)` and switched
`kreiss_constant_estimate` to a dedicated, LOCAL grid centered on `alpha(A)`
(`KREISS_GRID_KWARGS`: window `[alpha(A)-1, alpha(A)+30]`, `150x80` resolution) instead of
`pseudospectral_abscissa`'s eps~1-tuned arc-wide default, which cannot resolve small eps (step
0.65 vs eps as small as 0.02). Re-run: **0/20 violations**, confirmed by a dedicated regression
test (`test_regression_seed301_n50_that_previously_hit_the_eps_sampling_gap_bug`) that locks in
both the specific matrix and a `k_estimate` floor (`> 2x` the old undersampled value).

## FL Step 0a — Mechanism Claim Gate

As stated in `claim.md`: this is the case where the mechanism claim IS a proven theorem, not an
empirical behavioral sentence — no synthetic counter-example check was needed for the theorem
itself. What DID need (and received) verification: this arc's own computation of the two related
quantities. The bug/fix above is exactly that verification doing its job — it caught a real gap
in the NEW code (Kreiss estimate sampling), not in the already-verified reused code.

## Honest T_MAX Diagnostic (pre-registered, not discovered after)

`t_at_max == T_MAX (1.0)` for **all 20/20 matrices** — the raw transient growth is still
increasing at the edge of the arc's `T_MAX=1.0` window for every sampled matrix. Per `claim.md`'s
pre-registered caveat: this does NOT threaten the upper-bound check (a restricted time domain can
only make the upper bound easier to satisfy, never violate a bound valid on the full domain — and
indeed all 20 held). It DOES mean the raw `growth` values reported here are themselves LOWER
bounds on the true `sup_{t>=0}||exp(tA)||` — the true transient growth over a longer window would
likely be even larger, which would only make the upper-bound check MORE conservative (harder to
violate), consistent with what was observed. Diagnostic only, not a kill signal.

## Kill Analysis

**What this experiment killed:** nothing in the falsifiable-claim sense (a proven theorem was
not "at risk" of being falsified by real data) — but it DID kill this experiment's own first-draft
`EPS_VALUES` design as adequate for this matrix family.

**What this experiment confirmed:** the arc's own `alpha_eps`/transient-growth computations are
mutually consistent with the Kreiss Matrix Theorem across 20 real matrices spanning both primary
N_DIM values, once the Kreiss constant is estimated with an eps-sampling range that actually
covers where the supremum lives for this matrix family.

## What This Does NOT Mean

1. Does NOT retroactively change any prior verdict in this arc.
2. Does NOT "prove" pseudospectral abscissa is the SOLE mechanism behind `H-B2-1r/1s/1t`'s M1
   correlation — the low efficiency ratios (median 3.7-6.3%) mean the Kreiss upper bound, while
   mathematically valid, leaves most of the observed growth magnitude unexplained by this
   specific inequality alone. The theorem's `e*n` factor is a known-loose classical bound;
   this does not diminish the earlier correlational evidence (`H-B2-1r/1s/1t`), it contextualizes
   what "mechanistic" can mean here: pseudospectral abscissa correlates with M1 because both are
   downstream of the same underlying non-normality, not because the Kreiss inequality itself is a
   tight quantitative predictor of M1's magnitude.
3. Does NOT establish causality — this is a mathematical inequality check, not an intervention.
4. The `t_at_max == T_MAX` finding for all 20 matrices does NOT indicate a bug — see the honest
   T_MAX diagnostic above.

## Relaxation Map / Next Steps (not auto-launched)

- User's own roadmap named Priority 3 as the last currently-scoped step (Priorities 1-2 already
  closed: `H-B2-1s` cross-implementation, `H-B2-1t` fresh-seed confirmatory). No further
  experiment in this specific sub-arc is pre-authorized — report back and await direction, per
  this session's established discipline against auto-chaining past what was explicitly requested.
- Possible (not launched) follow-up if the user wants a tighter mechanistic bound: replace the
  classical `e*n*K(A)` ceiling with a matrix-specific numerical-range or resolvent-norm bound,
  which are known to be tighter than the universal Kreiss constant for many non-normal families —
  would require new theory, not just new code.

## Pearl Registry Update

New finding, general beyond this one experiment: for `build_matrix_with_seed_and_n`'s matrix
family (diagonal + strictly-upper-triangular random coupling), the Kreiss-constant supremum is
dominated by SMALL eps (observed order-of-magnitude jump: eps=0.02 gives ~11x the ratio found at
eps=0.5-3.0 for the worst-case sampled matrix). Any FUTURE experiment in this arc computing a
Kreiss/pseudospectral-based quantity on this same matrix family should default to an eps range
that includes values well below 0.5, not assume the eps~1 regime (tuned for this arc's earlier
M1-correlation use case) is representative of where pseudospectral quantities peak.
