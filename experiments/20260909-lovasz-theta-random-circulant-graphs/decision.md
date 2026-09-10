# H-CAT31-1 — decision.md

## Result

### Mechanism Claim Gate catch (before trusting any number)

The claim.md's own triggering sentence -- "theta(G) = n*(-lambda_min)/(d-lambda_min)
exactly, for any vertex-transitive G" -- was checked against the paper's own independently
sourced LP (Table 1, arXiv:2603.29571) rather than trusted from memory. **FAILS**: the two
implementations match EXACTLY on sparse cycles (`theta_via_eigenvalues(C_5) = theta_via_lp(C_5)
= sqrt(5)`, matching the well-known textbook value) but diverge substantially (differences
up to 3.72, not numerical noise) on denser random circulant graphs at n>=9.

**Third independent check, not just "the two disagree so pick one":** for the n=9,
seed=31090 disagreement (theta_eigenvalue=2.671, theta_lp=2.064), the graph's complement
collapses to a connection set {4,5} which -- since 5 = -4 mod 9 -- is a single circulant
offset, isomorphic to C_9. The closed-form odd-cycle formula
`theta(C_{2k+1}) = (2k+1)cos(pi/(2k+1))/(1+cos(pi/(2k+1)))` gives `theta(C_9) ~= 4.360`.
Via the theta(G)*theta(Gbar)=n identity (exact for vertex-transitive graphs, Lovász 1979):
`9/theta_lp = 9/2.064 = 4.36` -- matches. `9/theta_eigenvalue = 9/2.671 = 3.37` -- does not
match. **`theta_via_lp` is confirmed correct; `theta_via_eigenvalues` is confirmed wrong**
(the recalled ratio-bound formula either applies under a stronger condition than plain
vertex-transitivity, or was simply mis-remembered -- not re-derived further, since the
directly-sourced LP is sufficient).

The eigenvalue formula was never used for the reported result. It is kept in `run.py`
purely as a documented, regression-tested example of "I recalled a formula from memory and
it was wrong" -- exactly the failure mode `integrity.md` warns [MEMORY]-tier claims about,
caught here before it corrupted the headline finding, not after.

### Performance fix (needed before the LP-based sweep was even feasible)

The first LP implementation built its n x n DFT-cosine matrix via a Python-level double
loop -- O(n^2) *interpreted* operations, making n=2560 impractically slow (a `TaskStop`ped
background run exceeded 3 minutes with no output). Vectorized via `numpy` outer product
(`np.cos(-2*pi*j*k/n)` on broadcast index arrays) -- same O(n^2) FLOP count, done in C.
Confirmed identical numerical output to the loop version on all tested cases before/after
(same theta values to full precision). Full sweep then completed in ~2.5 minutes.

### Primary finding

theta(G)/sqrt(n), random dense circulant graphs (p=0.5), n from 10 to 2560:

| n | mean theta | theta/sqrt(n) | reps |
|---:|---:|---:|---:|
| 10 | 3.966 | 1.254 | 25 |
| 20 | 5.300 | 1.185 | 25 |
| 40 | 6.301 | 0.996 | 25 |
| 80 | 8.812 | 0.985 | 25 |
| 160 | 12.624 | 0.998 | 25 |
| 320 | 18.046 | 1.009 | 25 |
| 640 | 25.132 | 0.993 | 15 |
| 1280 | 36.417 | 1.018 | 10 |
| 2560 | 49.331 | 0.975 | 6 |

**The ratio stays within a tight band around 1.0 across nearly 3 orders of magnitude in
n** (excluding the smallest n=10,20 where finite-size effects are expected and visible --
1.25 and 1.19 respectively, converging toward ~1.0 by n=40 and staying there).

**CORRECTION ADDENDUM (2026-09-10, decisive check from the deep external novelty audit,
`reports/2026-09-10-deep-external-novelty-audit.md`):** the originally-reported log-log
slope **-0.035** was computed over the FULL range including n=10,20 -- the two points this
same section already excludes as finite-size effects. Recomputed on n>=40 only (the 7
points actually used to support the "tight band" claim): **slope = -0.0002**, i.e.
indistinguishable from exactly flat. -0.035 must not be cited going forward; it mixed the
excluded finite-size points back into the regression.

**A stronger, exact result was found that the original write-up missed:** for
vertex-transitive G, theta(G)*theta(Gbar) = n exactly (Lovasz 1979). At p=0.5 the ensemble
is self-complementary in distribution (each offset independently included with probability
0.5, so the excluded-offset complement graph has the identical distribution as G itself),
so E[theta(G)] = E[theta(Gbar)]. By AM-GM, (theta(G)+theta(Gbar))/2 >= sqrt(theta(G)*theta(Gbar))
= sqrt(n) pointwise for every realization, hence **E[theta(G)] >= sqrt(n) EXACTLY, for every
n, with no o(1) term** -- not an asymptotic claim, not something this experiment needed to
measure. This has two consequences for how this result should be read: (1) the "ratio stays
near 1" headline is HALF forced by this exact inequality (only deviations ABOVE 1 are
informative; the 5/9 sample means below 1.0, including 0.975 at n=2560, are finite-sample
noise around a population mean that is provably >=1 -- verified: SE at n=2560 is 0.0143, so
0.975 is only 1.74 SE below 1.0, well within noise); (2) a negative log-log slope of the
ratio is impossible in expectation given this inequality, which independently confirms the
corrected ~0 slope above and further undermines the original -0.035 reading. Kill-criterion
and CONFIRMED verdict below are UNCHANGED by this correction (the numeric evidence still
supports the tight conjecture over the weak fallback bound) -- what changes is that part of
what looked like an open numerical question is actually a proven fact, and should not be
re-presented as if the numerics alone established it.

## Verdict

**CONFIRMED** — numerical evidence over the tested range (n up to 2560) is directly
consistent with the tight Conjecture 18 (E[theta(G)] = (1+o(1))sqrt(n)), and distinctly
more consistent with it than with the paper's own weaker fallback upper bound. This is a
substantive result, not the low-probability-as-expected outcome that H-CAT37-1's Forsythe
conjecture check turned out to be — the ratio converging cleanly to ~1 across 3 orders of
magnitude in n is a real, informative numerical data point for the specific gap the source
paper's own authors identify as open (closing the O(sqrt(log log n)) vs (1+o(1))sqrt(n) gap).

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the recalled eigenvalue-ratio formula for theta(G) on non-sparse
vertex-transitive graphs (confirmed wrong, not just "disagreed with an alternative").

**What was NOT killed:** Conjecture 18 itself (never provable by finite numerical sweep);
the paper's own weaker published upper bound (not contradicted, only not what the data
best matches at these n).

**Revival condition for going further:** push n substantially higher (the current sweep is
limited by O(n^2) LP cost — n=2560 already took ~40s per solve; n=10^5 would need either a
faster/structured solver exploiting the LP's own symmetry further, or a cluster) to see
whether the flat ratio persists or eventually shows the log-log-slow growth the weaker
bound would predict at astronomically larger n. Not planned as a next step in this project
— the current range already gives a genuinely informative data point for a live, partially
open 2026 conjecture, which is the experiment's own pre-registered bar (claim.md).

## Skeptic Concerns (self-review, FL Step 8a — low-stakes descriptive numerical claim, not
architectural; the Mechanism Claim Gate catch above substitutes for an external adversarial
pass on the correctness of the core computation)

- "n up to 2560 says nothing about the true asymptotic (n -> infinity) behavior" →
  **Accepted, explicitly stated in claim.md before running.** log(log(n)) moves so slowly
  that no computationally reachable n could fully discriminate the two hypotheses -- the
  finding is "the data is more consistent with the tight conjecture over this range," not
  "the conjecture is proven."
- "Only one edge density (p=0.5) tested" → **Accepted limitation**, matches catalog item
  #31's own scope ("dense circulant graphs"), not investigated across other densities here.
- "The eigenvalue-formula bug could mean there's a similar bug in theta_via_lp that just
  happens to pass the C_5/C_9 checks" → **Mitigated, not eliminated**: two independent
  checks (C_5 known value, C_9-isomorphic-complement + product identity) both pass;
  cannot rule out a third, more subtle bug with certainty, same epistemic status as
  H-CAT37-1's own equivalent concern.

## Scope note

Second experiment under the 2026-09-09 scope expansion (ADR-087), after H-CAT37-1. Real
Source Trace (`mcp__arxiv__download_paper`, full text read, not a snippet) done BEFORE any
implementation, matching the discipline established after Bridge 8's mistake.
