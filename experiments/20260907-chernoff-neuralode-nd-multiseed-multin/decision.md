# decision.md — H-B2-1m (genuinely independent multi-seed x multi-N_DIM test of kappa(V)->M1)

## Result

**Verdict: WEAKENED** — kappa(V) has a strong, individually-significant relationship with M1 at
small-to-moderate dimension (`N_DIM` in {3,4,8,12}: all rho >= 0.88, all p < 1.4e-4), but the
relationship is not detectable — inconsistent in sign, no individual significance — at larger
dimension (`N_DIM` in {16,24,32,40,50}) with the sample size tested here (15 seeds/`N_DIM`).

| N_DIM | Spearman rho | p-value | Individually significant (a=0.05)? |
|---|---|---|---|
| 3 | 0.996 | 2.4e-15 | Yes |
| 4 | 0.982 | 8.2e-11 | Yes |
| 8 | 0.882 | 1.4e-5 | Yes |
| 12 | 0.946 | 9.4e-8 | Yes |
| 16 | **-0.225** | 0.420 | No |
| 24 | **-0.225** | 0.420 | No |
| 32 | 0.264 | 0.341 | No |
| 40 | 0.300 | 0.277 | No |
| 50 | 0.504 | 0.056 | No (borderline) |

Fisher-combined p-value across all 9 slices: 1.1e-26 — overwhelmingly significant, but per the
kill criterion's own refinement (below), this does NOT satisfy CONFIRMED because it is driven
entirely by the `N_DIM` in {3,4,8,12} slices — zero slices at `N_DIM >= 24` reach individual
significance. Naive pooled Spearman (all 135 points, `[CONFOUNDED — reference only]`): rho=0.930,
p=1.5e-59 — not the claim under test, per this experiment's own FL Step 0a check.

## FL Step 8a Skeptic Pass — full context-asymmetric run, findings and dispositions

Ran `Agent(skeptic)` with claim.md + run.py + the real per-slice numbers, no session history.
Verdict: **WEAKENED** (agreeing with the corrected verdict above — the agent's own read of the
raw numbers independently arrived at the same conclusion this decision.md reports). Findings,
Response Matrix:

1. **[HIGH, CONFIRMED and FIXED] RNG independence claim was false as first implemented.**
   `build_matrix_with_seed_and_n` seeded only on `seed`, sharing the raw uniform stream across
   `N_DIM` for a matching seed index. **Independently verified by direct computation** (not
   accepted on the skeptic's derivation alone): `default_rng(0).uniform(size=(3,3)).ravel() ==
   default_rng(0).uniform(size=(4,4)).ravel()[:9]` — confirmed `True`. This is the **third**
   instance of this exact failure class in this project's `H-B2-1*` arc (after H-B2-1l's and
   H-B2-1h's hard-coded-seed incidents), this time a subtler variant (genuinely different curves
   per `N_DIM`, but statistically dependent across `N_DIM` for matching seed indices). **Fixed**:
   `default_rng(np.random.SeedSequence([n_dim, seed]))`. Re-running with the fix materially
   changed the results — 2 of 9 slices flipped from positive to negative rho (`N_DIM=16,24`),
   confirming the dependency was doing real (confounding) work, not just a theoretical concern.

2. **[HIGH, ACCEPTED] The Fisher-combined "CONFIRMED" would have been a Recomposition Gate
   failure.** Before the fix, ~93% of the Fisher statistic came from the single `N_DIM=3` slice.
   The pre-registered kill criterion ("majority positive AND combined p<0.05") does not itself
   distinguish "the mechanism holds across dimension" from "the mechanism holds at small
   dimension and the combined statistic is dominated by that." **Response: criterion refined**
   (see claim.md's Kill Criterion refinement note) to require at least one large-`N_DIM`
   individually-significant slice for CONFIRMED — this changed the actual verdict on the
   (already-fixed) data from CONFIRMED to WEAKENED.

3. **[HIGH, ADDRESSED — reassuring result] `N_DIM=3`'s near-perfect correlation could be a
   low-degrees-of-freedom construction artifact.** At `N_DIM=3` there are only 3 random coupling
   entries and fixed eigenvalues (upper-triangular matrix -> eigenvalues = diagonal). Tested
   directly: do two ARBITRARY monotone functions of the same 3 coupling values (`f1` = sum of
   absolute values, `f2` = max of absolute values) also correlate near-perfectly with kappa(V)
   and M1? **Result: no** — `f1_vs_kappa` rho=0.489 (p=0.064), `f1_vs_m1` rho=0.464 (p=0.081),
   `f2_vs_kappa` rho=0.232 (p=0.405), `f2_vs_m1` rho=0.225 (p=0.420) — none reach significance,
   all well below the kappa(V)-vs-M1 slice's own 0.996. This is evidence AGAINST the low-DOF
   artifact concern: kappa(V) specifically (not just any smooth function of the same inputs) has
   an unusually tight relationship with M1 at `N_DIM=3` — the small-N result appears to reflect
   something real about kappa(V), not a generic property of low-dimensional constructions.

4. **[MEDIUM, ACCEPTED and FIXED] `np.finfo(float).tiny` as a p-value floor inflates the Fisher
   statistic beyond what the data supports.** A perfect-rank slice (`N_DIM=3` before the fix, still
   near-perfect after) makes scipy's asymptotic-t approximation report an exact `p=0.0`, which is a
   real limiting value but not a meaningful probability at n=15. **Fixed**: floored to the
   exact-permutation minimum achievable at this sample size, `2/15! ≈ 1.5e-12`, the principled cap
   for this specific artifact rather than an arbitrarily tiny float.

5. **[LOW, FIXED] `classify_verdict`'s WEAKENED-branch fallback didn't match claim.md's own
   pre-registered text** (counted any slice `>=0.2` regardless of sign, not just positive ones).
   Did not change the verdict on this run's data (all counted slices were already positive) but
   was a real latent inconsistency between code and spec — fixed.

## Kill Analysis (WEAKENED, not a full REJECT — partial per this project's own status vocabulary)

**What is KILLED:** the claim that kappa(V) "explains M1's variation" **across the full tested
dimension range** — the relationship is undetectable at `N_DIM >= 16` with this sample size, and
2 of those 5 large-`N_DIM` slices show a (non-significant) NEGATIVE rho, not just a weaker
positive one.

**What is NOT killed:**
- kappa(V)'s explanatory power at `N_DIM` in {3,4,8,12} — strong, individually significant on
  genuinely independent seeds, and the `N_DIM=3` result specifically survives a direct check
  against the low-degrees-of-freedom-artifact concern.
- `H-B2-1i`'s own original `N_DIM=8` finding (rho=0.453, n=30, a DIFFERENT eigenvalue
  construction — `H-B2-1h`'s own eigenvalues, not this experiment's fixed-spectral-range
  construction) is untouched by this experiment; this experiment's own `N_DIM=8` slice
  (rho=0.882, a structurally different population) does not replace or contradict it, they are
  not the same measurement (see claim.md's own non-transfer note).
- The general Trefethen-Embree inequality this mechanism is built on remains a proven
  mathematical fact, not something this experiment could have falsified.

**Relaxation Map (untested directions, if resumed):**
- Increase seeds/`N_DIM` at the large-`N_DIM` end specifically (e.g. 30-50 seeds at `N_DIM` in
  {24,32,40,50}) — the current WEAKENED verdict at large N could reflect genuine absence of the
  effect, or simply inadequate power at n=15/slice; `N_DIM=50`'s p=0.056 is close enough to
  alpha=0.05 that more seeds could plausibly flip it.
- Investigate numerical stability of `cond(V)` at large `N_DIM` directly (skeptic finding, not
  independently checked here) — `np.linalg.cond` on a near-defective eigenvector matrix can be
  unstable, and this was flagged but not resolved; the negative slices at `N_DIM=16,24` could in
  principle reflect measurement noise in kappa(V) itself rather than a genuine absence of
  mechanism, not distinguished here.
- A mechanistic explanation for WHY the relationship concentrates at small `N_DIM` (more degrees
  of freedom at large N for other transient-growth contributors to dilute kappa(V)'s specific
  contribution is a plausible hypothesis, not tested here).

## What This Does NOT Mean (restated per claim.md)

1. Does NOT retroactively re-validate the discredited `H-B2-1l` N-sweep leg (still WEAKENED, a
   separate, structurally different measurement).
2. Does NOT establish causality between kappa(V) and M1.
3. Does NOT contradict `H-B2-1i`'s own surviving `N_DIM=8` finding — different population.
4. Does NOT establish that the large-`N_DIM` absence of signal is permanent — it may simply
   reflect insufficient power at 15 seeds/slice, an open question named in the Relaxation Map.

## Pearl Registry Update

New falsifiable, testable side-finding worth its own row: kappa(V)'s explanatory power for M1
appears concentrated at small-to-moderate dimension and is undetectable (not just weaker) at
larger dimension with matched sample size — filed separately with a concrete falsifiable
prediction (more seeds at large N should either restore or rule out the effect).
