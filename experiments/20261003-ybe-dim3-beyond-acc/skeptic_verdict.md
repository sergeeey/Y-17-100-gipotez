# skeptic_verdict.md -- 20261003-ybe-dim3-beyond-acc

Date: 2026-10-04. Independent falsification pass (context-asymmetric: claim.md + code + data only).
All scripts were written fresh in the session scratchpad (not in this folder); only `np.load` of the saved npz files was shared with the audited code,
except where stated ("audited solver re-run"). Hardware rules followed: one process at a time, scripts/lowprio.py, no Pool, no git, no installs.
Evidence markers: [VERIFIED] = executed by me this pass; [DOCS] = read in a primary source.

## Overall verdict

Numerical claims 1, 2, 3 and 6 are CONFIRMED by independent re-computation. Claim 4 is CONFIRMED on its numbers but its interpretation
("extension of H2,1, not a new component") is not established (UNVERIFIABLE with what is in the folder). Claim 5 is WEAKENED: the counts reproduce,
but the headline "all 237 have a 3-distinct-eigenvalue element in L(R)" holds only because the L-tolerance is loose (1e-7 relative), 213/237 solutions are
trivial (c*Id or c*flip), and the 0/713 Gaussian failure is a solver-formulation artefact (collapse to R = 0), not information about the variety.
The decision verdict REPEAT (no lead, no classification) is consistent with everything I found; nothing here supports PROMOTE.

## Claim 1 -- idx 88 (seed 300447, near_flip, w001) satisfies braid YBE and is block-diagonal  -> CONFIRMED
- [VERIFIED] My own kron/matmul residual: ||R1R2R1-R2R1R2||/||R||^3 = 2.66e-17 (also 1.3e-16 relative to max|R1R2R1|), with and without det-normalisation.
  Non-braided form R12R13R23 = R23R13R12 with R_YBE = P*checkR (R13 built by index placement, not by the audited code): 2.66e-17.
- [VERIFIED] det R = 1 + 9e-16; off-block entries (charge [i==2]+[j==2]) are exactly 0 (count of nonzero off-block entries = 0).
- Caveat: "exactly 0" is true by construction -- the w001 mask search never varies entries outside the grading, so block-diagonality is an input of the search,
  not a finding. The informative statement is claim 2.

## Claim 2 -- L(R) is 2-dimensional = span{I, diag(0,0,1)}, no element with 3 distinct eigenvalues  -> CONFIRMED
- [VERIFIED] Independent null space: explicit 81x9 matrix of h -> [R, h(x)1+1(x)h] over the matrix units, SVD. Singular values:
  4.09 4.09 4.06 4.06 1.57 1.47 0.85 | 1.2e-16 0 (gap of 15 orders; dim of null space is 2 for every threshold 1e-6..1e-14).
- [VERIFIED] Null basis = {diag(1,1,0)/sqrt2 (up to sign), diag(0,0,1)}: distance of I and of diag(0,0,1) from the null span is 5e-16 and 0.
  2000 random elements of L: largest normalised eigenvalue gap = 1.3e-15 (always two equal eigenvalues).
- [VERIFIED] Method controls on the same routine: R = Id and R = flip give dim L = 9; random (0,1,2)-graded and random (0,0,1)-graded matrices give dim L = 2.
- Logical note: L(R) is covariant under R -> (g(x)g) R (g(x)g)^-1, transpose, P R P and R^-1, so "no 3-distinct element" really excludes conjugacy to any ACC/SCC matrix.
  It does NOT exclude the finer notions of "close to charge conserving" of arXiv:2609.38290 (accepted limitation already in decision.md).
- The same check for idx 101 gives the same L (2-dimensional, singular values 2.03 2.03 2.01 2.00 0.30 0.27 0.17 | 1e-16 0).

## Claim 3 -- 4x4 charge-0 block of idx 88 is dim-2 braid and has the signature of H1,4  -> CONFIRMED (and upgraded from signature to explicit conjugacy)
- [VERIFIED] Block on basis |00>,|01>,|10>,|11> (indices 0,1,3,4): dim-2 braid residual 4.25e-16.
- [DOCS] Forms of H1,4 and H2,1 checked against arXiv:2409.05375v2 eq. (2.17): H1,4 = [[0,0,0,p],[0,k,0,0],[0,0,k,0],[q,0,0,0]]; the code's hiet_families matches.
  The same paper's Definition 2.1 allows gauge R -> kappa (Q(x)Q) R (Q(x)Q)^-1 plus three discrete symmetries.
- [VERIFIED] Explicit construction (not an optimiser): the block has eigenvalue k = -0.5100-0.0031i with a 2-dimensional eigenspace E; E contains the singlet
  (0,1,-1,0) (distance 4.5e-16); the symmetric element S of E is a nondegenerate 2x2 matrix; its inverse form has two isotropic lines a, b; put g = [a b].
  Then (g(x)g)^-1 B0 (g(x)g) = H1,4 with p = 0.0090-0.0240i, q = 3.502-3.391i, k = -0.5100-0.0031i; max entry outside the H1,4 pattern 2.6e-15,
  H11-H22 = 1e-17, ||H - H1,4(p,q,k)|| = 3.5e-15. Eigenvalues +-sqrt(pq), k, k check out (0.19376-0.29548i).
  H1,4(p,q,k) is a braid solution for random complex k,p,q (residual <= 5e-18), so it is a 3-parameter family and B0 is a member.
- Negative control: a 1e-2 perturbation of B0 breaks the braid residual (0.039) and the repeated eigenvalue.
- So B0 is gauge-equivalent to H1,4 (a U(1)-free dim-2 solution, dimL=1 in the audit's own control C4).

## Claim 4 -- idx 101 (seed 300508, near_id): YBE 3e-17, L = span{I, diag(0,0,1)}, charge-0 block matches H2,1; is it a new component?  -> CONFIRMED on numbers, interpretation UNVERIFIABLE
- [VERIFIED] YBE residual 3.3e-17; L as above; B0 diagonalises to H2,1 (k^2, k^2-pq, kp, kq pattern) after conjugating by the eigenbasis of its dim-2 charge element:
  ||g^-1 B0 g - H2,1(k,p,q)|| = 2e-14 with (kp)(kq)-k^2 pq = 1e-14.
- [VERIFIED] Not conjugate to any Table-1 (ACC) family: every Table-1 matrix has an L-element with spectrum (0,1,2)-type, this one has none (claim 2 argument).
  So "an equivalent already in Table 1 under a non-diagonal basis change" is refuted.
- [VERIFIED] NEW structural facts the decision does not state: the full 9x9 R101 is diagonalisable with exactly TWO eigenvalues, 7 x lambda (lambda = k^2) and 2 x mu (mu = -pq);
  B0 and B1 (charge-1 block) have the same spectrum, R[8,8] = lambda. I.e. R101 is a Hecke-type (R-lambda)(R-mu)=0 solution with rank-2 mu-eigenspace, the same spectral signature (7,2)
  as the ACC family V.2.1 (L = span{I,diag(0,1,2)}). Zariski tangent dimension at R101 = 11 (7 orbit + 1 scale + 3 moduli) vs 10 at a random V.2.1 member.
  So R101 is not in the V.2.1 orbit family and lives on a strictly larger-dimensional piece of the variety, but I did not decide whether it is a known (Hietarinta 1993 upper-triangular / weak-charge /
  Hecke-type) solution. "2+1 extension of H2,1" is a description of the charge-0 block only; novelty and extension status remain UNDETERMINED. The decision's own wording ([INFERRED], REPEAT) is the right strength.
- Same facts for idx 88: spectrum multiplicities (1,1,2,2,2,1), tangent dim 12.

## Claim 5 -- full 81-parameter search: 237 solutions, all with a 3-distinct L element; gauss never converges; no U(1)-free component outside the Gaussian basin  -> WEAKENED
Reproduction:
- [VERIFIED] audited solver re-run (lm_det, maxit 200, abort on) on seeds 100000..100599: 66 converged, identical seed set to d3full_a.npz (symmetric difference 0).
  Log d3full_a.log: (gauss, stall) 713, near_flip ok 148, near_id ok 89 -- consistent with 237 = 148 + 89. In the stored file every converged seed has (seed-100000)%3 in {0,1}; none is a gauss seed.
- [VERIFIED] My independent classification of the 237 stored matrices: worst relative residual 3.6e-15, max condition number 601 (no near-singular spurious "solutions").
  83 are c*Id to 1e-14; 130 are c*flip to within 1.1e-6 (relative distance, not 1e-14); only 24 are "other" (dimL 2 or 3, all with a 3-distinct element at L-tolerance 1e-8 except one, all at 1e-6).
  => 213 of 237 (90 %) are the trivial Id/flip points; the sample says very little about positive-dimensional components.
What is weakened:
- The label "distinct" for the 130 flip-type matrices depends on the L-tolerance. The audited L_algebra uses tol 1e-7 relative to max(s0, ||R||*sqrt(2N)) ~ 7e-7; the commutators of these
  matrices with delta(h) are ~3e-7 (they are approximations of c*flip at distance 1e-7..1e-6 because the residual is quadratic near that singular point and LM stops at 1e-13).
  With tolerance 1e-8 my routine returns dim L = 1 for 128 of the 237 and "no 3-distinct element" for 129. They ARE flip-type (distance to c*P up to 1e-6), so the physical conclusion survives,
  but "all 237 have a 3-distinct element" is a tolerance statement, not a clean separation; the same fragility affects the w001 sample (76/148 fail at 1e-8, 2/148 at 1e-6; the two real candidates
  88 and 101 are robust: singular value gap 1e-16 vs 0.85 / 0.17).
- "gauss 0/713": [VERIFIED] the audited solver on 200 gauss seeds ends with f = 1.000 (min = median = max = 1) after a median of 19 iterations, i.e. it converges to R = 0, where F = 0 and the only
  residual is |det-1| = 1. The Gaussian failure is a collapse to a trivial attractor of the det-penalty formulation, not evidence about the geometry of the solution variety. My scipy LM on the same
  formulation also fails 30/30 (scale 1.0) and 30/30 (scale 0.3).
- Different formulation, as requested: R = expm(X), tr X = 0 (so det R = 1 exactly, no collapse), scipy trf on ||F||. From 24 Gaussian starts (X0 scale 0.5): 16 converge (rel. residual < 1e-9),
  8 nearly converge (1e-8); of the 16: 11 are the generic Hecke-(1,8) type with dim L = 2 (3-distinct L element, ACC-type), 5 are c*Id. No U(1)-free solution appeared. So the audited conclusion
  "no U(1)-free solution found" is reproduced by a method that DOES start from generic points -- but 16 samples with a basin dominated by the generic ACC component is weak evidence for absence.
  Starting from random g(x)g conjugates of G1/G2 plus relative noise 0.4: 0/10 return to a U(1)-free solution (7 land on ACC-type, 3 stall).
- Dead end noted: with plain-minimisation near-identity starts my own solver converged only to c*Id / c*flip (6/80), which is why the audited sampler's "all 237 distinct" is partly a statement about the start distribution.

## Claim 6 -- lm_det has no power in the U(1)-free region (25/25 for noise 0.02-0.2, 0/25 for 0.4 and 0.8)  -> CONFIRMED
- [VERIFIED] G1 = (I + w(P+P^2))/sqrt3, P = X(x)Z, w = exp(2 pi i/3): braid residual 1.2e-16, dim L = 1, spectrum (3,6) (G2 likewise). Independent implementation:
  scipy MINPACK LM on real/imag split, own analytic Jacobian (finite-difference check 8e-7 on entries ~1.6e3), residuals F and det R - 1, my own seeds (noise*(N+iN)/sqrt2 added to normalised G1):
  noise 0.02, 0.05, 0.10, 0.20: 25/25 converge, all to dim L = 1, spectrum (3,6) (the U(1)-free class of G1);
  noise 0.40, 0.80: 0/25, final relative residual ~1e-1 (stall).
- Interpretation caveat: ||G1||_F = 3, so noise 0.2 is already a ~60 % relative Frobenius perturbation and the basin edge lies between 0.2 and 0.4. The statement "no demonstrated power for the U(1)-free
  region at the start scale of the search" is correct; but, per claim 5, a good part of the failure at large noise is the same R -> 0 / ACC-attractor problem, not a property of U(1)-free points.

## Literature checks (opened myself)
- [DOCS] 2310.03816 text in lit_2310.03816.md lines 125-126: "a complete solution is known only for dimension two [9]... three dimensional upper triangular case was solved in [10]"; refs [9] Hietarinta 1992 Phys. Lett. A 165, [10] Hietarinta J. Phys. A 26 (1993) 7077. Matches decision item 1.
- [DOCS] arXiv:2409.05375v2 (opened in full around eq. 2.17): H1,4 and H2,1 forms, 10 classes + permutation singleton: matches the code.
- [DOCS] arXiv:2609.38290 abstract (opened): "in dimension 2, 10 out of 11 local families ... close to charge conserving, and the one that misses is a singleton" -- matches.
  But decision item 1 draws "so U(1)-free dim-2 families exist and are known" from it; that does not follow from this abstract (close-to-charge-conserving is a different notion). The conclusion itself is true
  and supported instead by the audit's own control C4 and by claim 3 here (H1,4 has dim L = 1).
- Not opened by me and not opened by the audit (paywalled / only abstracts): Hietarinta 1993 upper-triangular list, arXiv 0704.3334, Lovitz thesis. Novelty of idx 88/101 is therefore genuinely undetermined (the decision says so).

## Process issues
1. No controls.md exists (the controls live only in controls_output.txt and pos3*_output.txt); run_controls.py / controls_output.txt were produced by an earlier session and are labelled [UNVERIFIED-this-session] in decision.md -- honest, but the claim.md controls "must pass BEFORE any search result is trusted" were not re-run before the search; I re-ran their relevant L-routine controls (Id, flip -> dim L 9; ACC-graded -> 2).
2. A positive control that can return the target answer ("U(1)-free dim-3 solution") exists (pos3b: G1, G2) and was exercised -- good -- but it exposed 0/25 power at the search scale; the decision draws the right conclusion from it. The control did NOT detect that the failure is a collapse to R=0 (f=1), which is a cheap diagnostic (print final f for gauss starts).
3. Tolerance fragility in L-class labelling (1e-7 vs 1e-8) is undocumented; 130/237 and 76/148 labels flip with the tolerance. Recommend labelling flip-type points by distance to c*P/c*Id and reserving L-class for matrices whose commutator is at machine precision.
4. [VERIFIED] markers in decision.md items 5-7 are fine: counts reproduce (66/66 seeds in a re-run, 237 and 148 from stored files, 2 candidates at tol 1e-6). Items 2 (C-section numbers) are correctly marked as not re-run.
5. decision.md item 3 "88/96 same-signature" is arithmetically consistent with pos3_output.txt (88+2+1+5 = 96). "Signature = coarse invariant, not conjugacy" was a fair caveat; claim 3/4 here turns the signature matches into explicit conjugacies of the charge-0 blocks only.
6. Sample bias: the search starts only near identity/flip (or from Gaussian, which collapses); 90 % of returned "solutions" are the trivial points. The kill criterion "(>= 2000 random starts)" is met numerically but is not a random sample of the variety (decision.md already says so).
7. The two weak-charge candidates are structurally (0,0,1)-graded by the mask. A search without the mask for "weak-charge" solutions (dim L = 2, diag(0,0,1)-type) was not done; whether they are interior points of larger families is unknown (tangent dim 11 for idx 101, 12 for idx 88).

## What would change my verdict
- A single point with L-commutator at machine precision, dim L = 1 or non-diagonalisable-only, from the unmasked search that is not c*flip/c*Id and not in a known orbit (e.g. new component near G1/G2 under expm-parametrisation with many more starts).
- Explicit identification of idx 101 (Hecke-type (7,2), 3 moduli) with a solution in Hietarinta 1993 / Martin-Rowell / U_q(gl(2|1))-type constructions -- would close the novelty question as REPEAT.
