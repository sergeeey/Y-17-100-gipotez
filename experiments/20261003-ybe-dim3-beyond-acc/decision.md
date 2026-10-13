# decision.md -- 20261003-ybe-dim3-beyond-acc

Date: 2026-10-04 (resumed run; earlier attempts were killed by infrastructure failures, not by a scientific outcome).
Problem #11: constant YBE (braid form, 9x9) in dim 3, solutions beyond strict (SCC) / additive (ACC, arXiv:2310.03816) charge conservation.

## VERDICT: REPEAT (no lead, no classification claim, nothing shown to be new)

Substrate note (FL step 2a): the previous session's dim-3 random-start run (dim3_search1.log, ~28% "ok") was LOST (multiprocessing pool crash, nothing
saved) and the old S-variable solver drifted to singular R (det ~ 1e-16 while |R| ~ 0.4, residual decaying like 1/iter). Those earlier numbers are
UNVERIFIED and are not used. Everything below was re-run serially through scripts/lowprio.py (BELOW_NORMAL, 2 BLAS threads, no Pool; longest job 540 s;
45 s cooling pause in batch_masks.py).

## What was done / evidence ([VERIFIED] = executed by me this session)

1. [DOCS] Read arXiv:2310.03816 full text (lit_2310.03816.md): ACC is R^{kl}_{ij}=0 if i+j != k+l; "a complete solution is known only for dimension two [Hietarinta 1992]";
   dim-3 upper-triangular case solved in Hietarinta, J. Phys. A 26 (1993); no classification without an ansatz. [DOCS] abstract of arXiv:2609.38290 (opened):
   in dim 2, 10 of 11 local families are "close to charge conserving", the remaining one a singleton -- so U(1)-free dim-2 families exist and are known.
2. [VERIFIED] Positive control (a): 22 Table-1 families of 2310.03816 + P + Id satisfy braid YBE to <= 8e-17 (controls_output.txt, produced by an earlier session's run_controls.py; I did not re-run it, only
   pos3.py/pos3b.py rebuild the same families and use them as solver starting points; treat the C-section numbers as [UNVERIFIED-this-session] but consistent: pos3 starts converge back to them); 200 random 9x9: min relative residual 0.24; perturbed families: 2e-3..6e-3 (controls_output.txt C3).
3. [VERIFIED] Positive control (b), dim 2 (dim2_validate.py on dim2_search2.npz, 1943 converged solutions from the earlier S-solver): rediscovers the signatures of
   H3,1, H2,1, H2,2, H1,1/H1,2 (identical signature), H1,4, H0,2 and Id; DOES NOT rediscover H2,3, H1,3, H0,1 (non-diagonalisable / degenerate) nor flip P.
   => the random-start solver is only validated for 7 of 11 dim-2 families; 3 Jordan-type families are missed. (Signature = coarse conjugation invariants, not an
   explicit conjugacy.)
4. [VERIFIED] New dim-3 solver lm_det (solver_mask.py): unknown R only, equations F(R)=0 and det R = 1 (excludes singular R), serial. Positive control pos3_output.txt
   (noise 0.05, 4 trials per family): same-signature recovery 88/96, plus 2 same-L-class, 1 "other", 5 non-converged; Id and flip recovered 4/4.
   U(1)-free positive control pos3b.py (the two Gaussian/Weyl-Heisenberg solutions G1,G2, residual 1e-16, dimL=1): recovered 25/25 at noise <= 0.2, **0/25 at noise >= 0.4**.
5. [VERIFIED] Main search, full 81-parameter space (d3full_a.log): 2140 starts (near_flip / near_id / gauss, 713 each), 237 converged to residual < 1e-10
   (all 237 from near_flip or near_id; **0/713 from Gaussian random starts**). All 237 are L-class "distinct" (a 3-distinct-eigenvalue element in L(R)),
   i.e. conjugate to ACC (6) or SCC-or-more (231: 83 monomial/permutation-type with dimL=9 = identity-type, 125+ flip-type spectrum {6,3}, etc.). Zero U(1)-free and zero "degenerate" solutions.
   Kill criterion (i)-(iii) of claim.md is literally met by this sample.
6. [VERIFIED] Relaxed-symmetry searches (batch_masks.py, 700 starts each): Z3-graded (q=(0,1,2) mod 3): 172 solutions, all ACC/SCC+; Z2-graded: 138, all ACC/SCC+;
   weak charge q=(0,0,1) (33 free entries): 148 solutions, 146 ACC/SCC+ and **2 "beyond-ACC candidates"** (L(R) = scalars + diag(0,0,1); degenerate charge).
7. [VERIFIED] The 2 candidates (analyze_cand.py; seeds 300447 near_flip and 300508 near_id, file d3_w001.npz idx 88 and 101; mask w001): rel. residual 2.7e-17 and 3.3e-17; off-block entries exactly 0;
   the charge-0 block B0 (basis |00>,|01>,|10>,|11>) is itself a dim-2 braid solution (residual 4e-16 / 4e-17) with dim-2 signature equal to Hietarinta's **H1,4** (U(1)-free) for idx 88,
   and **H2,1** for idx 101. I.e. they are 2+1 extensions of known dim-2 solutions to a third state with a degenerate U(1) charge. [INFERRED] from the signature match (not an explicit conjugacy).
   Across all 148 w001 solutions B0 matches Id (48), H3,1 (20), H2,1 (3), H1,4 (1) or dim-2 non-generic strata (75).

## Honest reading

* Nothing found is outside "ACC/SCC, permutation-type, or extension of a known dim-2 Hietarinta solution". No lead.
* The "no U(1)-free solution in dim 3" outcome of item 5 is NOT evidence: the sampler converges only near identity/flip (gauss 0/713), and the solver's basin of attraction around a
  known U(1)-free dim-3 solution is noise <= 0.2 while the start scale used was larger (item 4). The search has no demonstrated power for the U(1)-free region; the negative-control/positive-control
  requirement ("a code path that cannot return a positive on the control is not validated") is NOT met for U(1)-free components in dim 3. Likewise dim-2 Jordan families were missed (item 3).
* The kill criterion's "(>= 2000 random starts)" was met numerically (2140) but the starts are not an unbiased sample of the variety; a REJECT of the beyond-ACC direction is therefore NOT justified.
* Novelty of the 2 weak-charge candidates is UNDETERMINED: only abstracts / search snippets of Hietarinta 1993 (3-state upper triangular), 0704.3334 (singular solutions from Lie algebras) and Lovitz' thesis
  were seen, not read. Not rationalised / not checked at high precision (double precision only, residual ~1e-17). Maximum honest status is REPEAT/ALREADY_KNOWN-type, per claim.md.
* No classification is claimed.

## What would change the verdict (next round, if anyone continues)
1. Give the sampler power in the U(1)-free region: seeds built from Weyl-Heisenberg / Gaussian solutions, from dim-2 U(1)-free Hietarinta families extended 2+1 (frozen-block search), from conjugating by random g(x)g, plus homotopy/continuation
   from known points; calibrate each start-scale against a positive control with noise >= the start scale.
2. Check whether the two weak-charge solutions form a NEW 2+1 extension component (compare with Hietarinta 1993 upper-triangular list and Martin-Rowell) by explicit conjugacy, and rationalise (mpmath / sympy) one point.
3. Handle Jordan-type solutions (H2,3 / H1,3 / H0,1 analogues), which the random-start solver demonstrably misses in dim 2.

## Skeptic Concerns (pre-answered, FL step 8a shortcut -- no PROMOTE, so no skeptic run needed)
- "L(R)-test = ACC-equivalence": valid only for Lie-algebraic (continuous) charge; discrete-symmetry-only solutions are labelled U1-free and are not claimed to be unrelated to ACC (2609.38290's notion of closeness is finer). Accepted limitation.
- "Signature match != conjugacy": accepted; stated as [INFERRED].
