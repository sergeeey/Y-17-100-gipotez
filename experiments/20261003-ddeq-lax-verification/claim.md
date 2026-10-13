# claim.md -- 20261003-ddeq-lax-verification (written 2026-10-03 BEFORE any check was run)

## L0 / Zero-Signal gate
- Question type: DESCRIPTIVE / formal verification (no causal or predictive content).
  "Does a published symbolic claim hold when recomputed independently?"
- Entity: arXiv:2604.26870 (S. Igonin, v1, Apr 2026), HTML full text read by me
  (saved here: paper_2604.26870.md / paper_clean.md).
- Falsifiable predicate: each explicit identity printed in the paper (MLR zero-curvature,
  Miura-type transformation (MT), gauge-transformed Lax matrices, Theorems 1-3 applied to the
  paper's examples) holds identically in the stated variables.
- Measurable outcome: residual of the identity, as a rational function (exact symbolic
  cancel) and/or at random rational points (mp.dps=60 numerics where sqrt occurs).
  PASS = residual 0 ; FAIL = nonzero residual that survives an independent re-derivation.

## Source trace (Step -4) [VERIFIED by me, read in the full text]
- Def.1 MLR: D_t(M)=S(U)M-MU ; gauge (12): M^=S(G)MG^-1, U^=D_t(G)G^-1+GUG^-1 ;
  Def.2 trivial / fake MLR (fake = gauge equivalent to a trivial one, M independent of u_l);
  Def.3 nabla_M(Q)=S(M^-1 Q M), Delta^{u^j}(M)=sum_l nabla_M^{-l}(d_{u^j_l}(M) M^-1);
  Def.5 MT via (20); Thm 1 (cond (27) <=> u_p removable from the S-part by a gauge),
  Thm 2 (Delta covariance), Thm 3 (MLR fake <=> Delta^{u^j}(M)=0 for all j); Lemma 4.
- Examples to verify: (67)+MLR(68); (72)+(71); (85)+MLR(90,91) -> gauge (95)-(97) -> (100);
  MT (89) from (85) to (67); (113) with MT (110) and sqrt formulas (108)-(109);
  (114)+(118,119); MT (115) to Toda (116) with MLR (117); gauge -> (120); (128) with MT (126).
- Novelty: NOT claimed. Verification of a published result only.

## Claims under test
- C1  each printed MLR satisfies (10) identically for its stated equation.
- C2  each printed MT satisfies (20) identically (both sqrt branches for (110)).
- C3  printed gauge transformations map the printed MLR to the printed MLR.
- C4  Thm 3 criterion: Delta != 0 for the Toda-type MLRs (non-fake); Delta = 0 for a deliberately
      fake MLR; Thm 2 covariance for random gauges; Thm 1 condition (27) holds for (90) and (118).
- C5  (symmetry approach, independent of Lax) eq (67) with constant alpha (Kaup-Newell type) and
      Toda (116) have a higher symmetry in a polynomial ansatz; perturbed versions do not.

## KILL CRITERION (fixed before running)
- A paper claim is a DISCREPANCY only if the residual is nonzero in exact/high-precision
  arithmetic AND survives (i) re-reading the source for a transcription error and
  (ii) re-derivation of the intermediate object by an independent route.
- The CHECKER is INVALID (verdict BLOCKED; nothing is said about the paper) if the positive control
  (Toda/Volterra with textbook Lax pair) returns a nonzero residual, or any negative control
  (perturbed Lax matrix / perturbed U / perturbed equation) returns zero residual.
- C5 "higher symmetry exists" is falsified for an equation if the nullspace of the linear system
  on the stated ansatz contains only {F, scaling symmetry} while the positive control finds its
  known extra symmetry. If the positive control fails, the solver/ansatz is inadequate, not the equation.

## What this result does NOT mean
1. Passing does not prove the paper's general theorems; only instances of them.
2. Passing is not an independent derivation of Lax pairs: it checks identities, not discovery.
3. A symmetry found in a bounded ansatz is necessary, not sufficient, evidence of integrability.
4. Nothing here classifies new integrable equations; the open problem itself is untouched.
