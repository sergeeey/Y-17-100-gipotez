# claim.md -- 20261013-ybe-dim3-round2 (written BEFORE any round-2 computation)

Date: 2026-10-13. Problem #11, round 2. Follow-up of experiments/20261003-ybe-dim3-beyond-acc (read-only; its decision.md and
skeptic_verdict.md were read first). Parallel session artefacts (H-CYBE-001..003, experiments/20261003-c-ybe-001,
experiments/20261004-c3-obstruction-cas) are read-only inputs.

## L0 gate (EstimandOps)
Type: DESCRIPTIVE (existence / identification of exact solutions of an algebraic system; no causal or predictive content).
Estimand sentence: "We report, for the two weak-charge solutions cand88 and cand101 (d3_w001.npz idx 88, 101, braid form R1R2R1=R2R1R2 on C^3(x)C^3),
whether they are conjugate (g(x)g, transposition, scaling, P R P, R->R^-1) to a member of the monomial shift family of H-CYBE-002 (and of the
other monomial supports of its 73-permutation census), whether they lie in the published 3-state upper-triangular / weak-charge lists, and whether
they have an exact closed form over Q or a small number field."
Does NOT mean: a classification; novelty; that a failed random-start search proves absence of U(1)-free components.

## Precise questions and decision rules (fixed now)
Q-A (relation to H-CYBE-002). Convert the shift family to braid form  R_braid = P * R_vertex  (the other session's vertex form is R12 R13 R23 = R23 R13 R12,
verified by me on the family before use). Compare with the candidates by conjugation invariants that survive the whole symmetry group
(spectrum with multiplicities, diagonalisability, Hecke relation, ranks of R-lambda, dim L(R), tangent dimension).
 * DIFFERENT (kill of "same family / sub-case"): one such invariant, computed exactly for the whole 5-parameter invertible family, never equals the candidate value.
 * SUB-CASE / SAME: only if an explicit conjugating matrix (g(x)g) and a parameter point are exhibited with residual < 1e-12 and checked exactly.
 * If neither: UNDECIDED, reported as such.
Q-B (sampler power in the region without a U(1) charge). The round-1 sampler had 0/25 recovery of the published Gaussian solutions at noise >= 0.4 and 0/713 from Gaussian starts.
 A new sampler is "validated for the U(1)-free region" ONLY if, from generic (non-informed) starts, it returns the known U(1)-free solutions (G1,G2 = Weyl-Heisenberg
 Gaussian solutions, dimL=1; and in dim 2 the known Hietarinta families incl. the three Jordan-type ones missed in round 1) at a nonzero rate with a stated n.
 If the positive control fails (rate 0 at n >= 100 starts), the sampler is declared NOT validated and no negative statement about the U(1)-free region is made.
 Negative control: a non-solution perturbation of a known solution (noise 1e-2) must NOT be reported as converged.
Q-C (rationalisation). Success = a closed-form (parameters k,p,q and any additional ones as exact algebraic numbers or symbols) 9x9 matrix whose braid residual
 is IDENTICALLY zero in sympy over Q(params) (or Q with explicit rational points), and which reproduces the numerical candidate after an explicit basis change.
 Failure = no such form found within the iteration budget (reported as unexplained, not as "irrational").
Q-D (literature). Hietarinta, J. Phys. A 26 (1993) 7077 (3-state upper triangular), the Lovitz thesis, and 2310.03816's own table are opened and read by me.
 ALREADY_KNOWN requires the candidate's family to be identified with a listed solution by an explicit map; resemblance is not enough.

## KILL CRITERION for the round (fixed before running)
The round REJECTS "cand88/cand101 are a lead (new, unexplained, outside known families)" if EITHER
 (i) an exact 9x9 closed form is found AND it is identified (explicit map) with a published solution or a trivially-derived extension of a published dim-2 solution, OR
 (ii) the candidates are shown to be members of a family obtainable by a standard construction (direct-sum / 2+1 extension of a dim-2 solution with a charge grading) with an exact verification.
Outcome LEAD requires: exact closed form, not identified with anything in the literature actually read, plus a documented novelty search. Without all of these the maximum
honest verdict is REPEAT / ALREADY_KNOWN / SUB-CASE (as shown by the evidence). No classification claim will be made.

## Controls (must pass before results are trusted)
 P1: shift family (random rational weights) satisfies vertex YBE (exact) and its P-converted braid form satisfies braid YBE (residual < 1e-14) -- validates the form conversion.
 P2: the invariant routine applied to a random (g(x)g)-conjugate of a candidate returns the same invariants (conjugation invariance); applied to Id and flip returns known values.
 P3: sampler recovers G1/G2 (see Q-B) and the dim-2 Hietarinta families (see Q-B).
 N1: invariant routine applied to the shift witness (2,3,5,7,11) must give an invariant DIFFERENT from the candidate -- and applied to a deliberately constructed sub-case
     (candidate-like matrix with two eigenvalues) must give equal -- so that the comparison can return both answers.
 N2: sampler residual for perturbed solutions stays O(1e-2).
Evidence markers: [VERIFIED]=executed by me this round, [DOCS]=read in a primary source, [INFERRED], [WEAK], [UNKNOWN].
Hardware: one heavy process at a time, scripts/lowprio.py, jobs <= 10 min, 45 s pause between heavy jobs.
