# claim.md -- 20261003-ybe-dim3-beyond-acc (written BEFORE the main search)

Date: 2026-10-03. Problem #11: constant Yang-Baxter equation (YBE) in dim 3, solutions beyond strict charge conservation (SCC) and additive charge conservation (ACC, Hietarinta-Martin-Rowell arXiv:2310.03816).

## L0 gate (EstimandOps)
Type: DESCRIPTIVE / existence-and-classification of solutions of an algebraic system (no causal or predictive content).
Estimand sentence: "We report which numerically found solution components of the braid-form YBE
R1 R2 R1 = R2 R1 R2 (R in GL(C^3 x C^3), 9x9) exist, characterised by GL3-conjugation invariants
(spectrum with multiplicities, Jordan data, dimension of the solution variety at the point, and the
Lie algebra L(R) = {h in gl3 : [R, h(x)1 + 1(x)h] = 0}), and which of them are not GL3-conjugate to an ACC/SCC solution."
Does NOT mean: (1) a classification (random-start search is not exhaustive; components of small basin, non-generic or
lower-dimensional strata can be missed); (2) novelty (any 'beyond ACC' solution is first compared with known
set-theoretic / quantum-group / twist constructions); (3) that a numerical residual of 1e-15 is an exact solution
(only a lead until rationalised/symbolically checked).

## Gate 2 (target provenance) for the positive-control targets
The Table-1 families of 2310.03816 are published exact algebraic solutions (human-derived, Proposition proved by
symbolic computation). Not fits. Used only as POSITIVE CONTROLS (their residual must be ~1e-15), not as targets.

## Plan / definitions
Braid form R := check-R = P R_YBE. Residual F(R) = R1R2R1 - R2R1R2 with R1 = R(x)1, R2 = 1(x)R.
Conjugation by g(x)g, transpose, scaling, and (check-R -> P check-R P) preserve the solution set.
ACC-equivalent  <=>  exists h in L(R) diagonalisable with spectrum an arithmetic progression of 3 distinct values.
SCC/generic-weight U(1)-charge-conserving  <=>  exists h in L(R) diagonalisable with 3 distinct eigenvalues, no AP condition.
Weaker charge conservation  <=>  L(R) contains a non-scalar h with repeated eigenvalue or non-diagonalisable h.
'Beyond ACC' (in the sense of this note)  <=>  no h in L(R) diagonalisable with 3-term-AP spectrum.

## Controls (must pass BEFORE any search result is trusted)
Positive 1: every Table-1 family of 2310.03816 (random admissible parameters) has residual < 1e-12; L(R) is non-trivial.
Positive 2 (solver, dim 2): solver started at random points converges to solutions; the invariants it finds
(spectrum classes / L(R) / variety dimension) must be consistent with Hietarinta's published dim-2 classification
(11 local families, 2609.38290; list in 2409.05375). A solver that cannot find e.g. the 2-parameter-richer families is not validated.
Positive 3 (solver, dim 3): solver must recover known dim-3 solutions (identity, flip P, SCC/ACC family members) from random starts at a rate > 0.
Negative 1: random 9x9 matrices and perturbed family members have residual O(1); the solver code path returns nonzero residual for them.
Negative 2 (equivalence test): L(R) test applied to a random GL3-conjugate of an ACC solution must still say 'ACC-equivalent'
(conjugation-invariance of the test), and applied to a generic (non-symmetric) solution must say 'no U(1)'.

## KILL CRITERION (fixed before running)
The 'beyond-ACC' search is REJECTED as a source of a lead if EVERY converged dim-3 solution (residual < 1e-10, full rank,
reached from >= 2000 random starts) falls in one of: (i) conjugate to ACC/SCC (via L(R)), or (ii) a set-theoretic /
permutation-type solution, or (iii) an obvious known construction (identity, flip, scalar multiples, twist by diagonal
conjugation, Jimbo/U_q(sl_3) constant R, or tensor/direct-sum/ 'diagonal-type' constructions recognisable by invariants).
Outcome 'LEAD' requires a solution component that (a) passes all controls, (b) has no h in L(R) with AP spectrum,
(c) is not a known construction after a documented literature check, (d) is rationalised/verified to residual < 1e-13 at
high precision. Without (c)/(d) the maximum honest verdict is REPEAT/ALREADY_KNOWN. No classification claim will be made.

## Evidence conventions
[VERIFIED] = executed by me here; [DOCS] = read in a primary source; [INFERRED]; [WEAK]; [UNKNOWN].
