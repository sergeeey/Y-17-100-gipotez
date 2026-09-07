# decision.md — H-B2-1m (genuinely independent multi-seed x multi-N_DIM test of kappa(V)->M1)

## FOLLOW-UP (2026-09-07, same session, user request: increase seeds at N_DIM>=16 and re-run,
resolves the Relaxation Map's open H1-vs-H2 question below) — **VERDICT UNCHANGED (WEAKENED),
but the evidence is now much stronger and points toward H1 (genuine mechanism breakdown), not H2
(inadequate power)**

The original run's Relaxation Map (below) left open whether the large-`N_DIM` null (no
individually-significant slice at `N_DIM` in {16,24,32,40,50}, `N_DIM=50`'s p=0.056 close to
alpha) reflected a genuine breakdown of the kappa(V) mechanism at large dimension (H1), or simply
inadequate statistical power at 15 seeds/slice (H2). Re-ran with seeds increased to 40 at
`N_DIM>=16` (the boundary is drawn where THIS experiment's own data actually broke — `N_DIM=12`
was individually significant, `N_DIM=16` was the first slice that was not), leaving `N_DIM<16`
unchanged at 15 seeds (already strongly significant, no need for more power there). 40 seeds
detects `rho~=0.43` at 80% power — comparable to this experiment's own original point estimates
at `N_DIM=24` (0.446) and `N_DIM=50` (0.504), so a real effect of that size should have become
individually significant if H2 were correct.

**Result: it did not. If anything, the opposite happened.**

| N_DIM | rho (n=15, original) | rho (n=40, follow-up) | p (n=40) | Individually significant? |
|---|---|---|---|---|
| 16 | -0.225 | **-0.012** | 0.943 | No |
| 24 | -0.225 | **-0.091** | 0.575 | No |
| 32 | 0.264 | **0.157** | 0.334 | No |
| 40 | 0.300 | **0.057** | 0.728 | No |
| 50 | 0.504 | **0.298** | 0.062 | No (still borderline, but weaker) |

With 2.67x more seeds, every large-`N_DIM` point estimate moved TOWARD zero (three of five moved
substantially closer to zero; none moved further from it), not toward significance. This is the
classic signature of the original small-sample point estimates being noise regressing toward a
true null, not evidence of an under-detected real effect — the opposite of what H2 (power
explains the null) would predict, which is that more data should sharpen a real signal, not
dissolve it. `n_large_n_slices_significant` remains 0. The decay trend (`Spearman(N_DIM,
per-slice rho)`) itself is now individually significant: rho=-0.683, p=0.042 (was p=0.053,
borderline, at the original sample sizes) — the decay is no longer merely suggestive.

**Reading:** this evidence favors H1 (kappa(V) genuinely stops being a sufficient descriptor of
transient growth at larger dimension — other structure, e.g. pseudospectral geometry, eigenvector
interaction patterns, or block/orientation effects, likely dominates) over H2 (the large-N null
was just underpowered). It does not prove H1 outright — `N_DIM=50` remains borderline (p=0.062,
weaker point estimate than before but not yet cleanly zero) and a mechanistic account of WHY the
relationship breaks down at `N_DIM>=16` specifically has not been tested. But the specific,
falsifiable prediction H2 implied (more seeds restores significance) did not hold, while the
prediction naturally following from H1 (more seeds should not manufacture a significant effect
out of noise) is exactly what was observed.

**graph.yaml / kill_criterion:** verdict stays WEAKENED (no large-N slice individually
significant, same criterion as the original run) — the follow-up strengthens the CONFIDENCE in
that verdict and narrows the open question, it does not change the verdict category itself.

**Practical implication for any future experiment on this bridge:** per the user's own framing,
the honest next boundary question is not "does kappa(V) explain M1" (answered: only at small-to-
moderate N) but "what starts to dominate transient growth once kappa(V) stops being sufficient" —
a mechanistic question, not a power question, and NOT recommended to pursue via another broad
N-sweep (this one already answered the power question cleanly).

## Result (ORIGINAL, before the follow-up above)

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
- ~~Increase seeds/`N_DIM` at the large-`N_DIM` end specifically~~ **DONE, same session (see
  FOLLOW-UP at top of this file):** 40 seeds at `N_DIM>=16` — every large-N point estimate moved
  TOWARD zero, not toward significance; `n_large_n_slices_significant` stayed 0. Evidence now
  favors genuine absence of the effect (H1) over inadequate power (H2), though not proven outright
  (`N_DIM=50` still borderline at p=0.062).
- Investigate numerical stability of `cond(V)` at large `N_DIM` directly (skeptic finding, not
  independently checked here) — `np.linalg.cond` on a near-defective eigenvector matrix can be
  unstable, and this was flagged but not resolved; still open after the power follow-up — the
  negative slices at `N_DIM=16,24` could in principle reflect measurement noise in kappa(V)
  itself rather than a genuine absence of mechanism.
- A mechanistic explanation for WHY the relationship concentrates at small `N_DIM` (more degrees
  of freedom at large N for other transient-growth contributors to dilute kappa(V)'s specific
  contribution is a plausible hypothesis, not tested here) — now the PRIMARY open question on
  this bridge, per the follow-up's own practical-implication note. NOT recommended to pursue via
  another broad N-sweep (the power question is now answered); the natural next step is a targeted
  test of a specific alternative descriptor (e.g. pseudospectral abscissa, eigenvector clustering
  metrics beyond kappa(V), or `x0`-orientation dependence) at one or two large `N_DIM` values.

## What This Does NOT Mean (restated per claim.md)

1. Does NOT retroactively re-validate the discredited `H-B2-1l` N-sweep leg (still WEAKENED, a
   separate, structurally different measurement).
2. Does NOT establish causality between kappa(V) and M1.
3. Does NOT contradict `H-B2-1i`'s own surviving `N_DIM=8` finding — different population.
4. Does NOT establish that the large-`N_DIM` absence of signal is a PROVEN mechanism breakdown —
   the power follow-up (see top of this file) makes H1 (genuine breakdown) more likely than H2
   (inadequate power), but does not rule out H2 entirely, and does not identify WHAT replaces
   kappa(V) as the dominant descriptor at large N, if anything does.

## Pearl Registry Update

**Original entry (resolved by the FOLLOW-UP above, not superseded):** kappa(V)'s explanatory
power for M1 appears concentrated at small-to-moderate dimension and is undetectable (not just
weaker) at larger dimension with matched sample size — falsifiable prediction was "more seeds at
large N should either restore or rule out the effect." Result: seeds increased 2.67x at
`N_DIM>=16`, effect did NOT restore (point estimates moved toward zero) — prediction resolved in
favor of "ruled out" over "restored," strengthening but not proving genuine mechanism breakdown.

**New entry from the follow-up itself:** the primary open question on this bridge is now
mechanistic (what replaces kappa(V) as a sufficient descriptor of transient growth at large
`N_DIM`), not statistical (is there enough power) — filed separately with the concrete next step
named in the Relaxation Map above.
