# skeptic_verdict.md — independent adversarial audit of 20261003-carpet-spectrum

Date: 2026-10-03. Auditor: independent verifier. Hardware limits respected (one heavy job at a time, lowprio.py wrapper, no multiprocessing, 45 s sleeps, no git/installs, no repo-wide pytest).
All code was written by the auditor in the session scratchpad (`.../scratchpad/v3/`: graphs.py, a_basic.py, b_res.py, c_schur.py, d_search.py, e_ctrl2.py). It does NOT import the audited lib.py. Graph builders are new (digit-rule cell test, explicit edge sets, triangle recursion for the gasket). Audited search.py was imported only for claim 2, where that is the object under test.

## Verdicts

| # | claim | verdict |
|---|---|---|
| 1 | no polynomial R (deg 2..6, R(0)=0) matches >0% | WEAKENED. Substance confirmed, the literal "0%" is a reporting artifact |
| 2 | search returns z(5-z), 93/95, on gasket; control not hard-coded, null not a tolerance artifact | CONFIRMED |
| 3 | level-5 sums, sums of squares, lowest nonzero eigenvalues | CONFIRMED |
| 4 | ratios 9.9476 / 10.0321, d_w 2.091 / 2.099; rho~1.2515, d_w~2.097 | CONFIRMED numerically; primary-source literature value UNVERIFIABLE by me |
| 5 | Schur complement not in span{A,D,I}, residual ~0.12; gasket exactly proportional | CONFIRMED |
| 6 | Euler characteristic 1-(8^n-1)/7, E = 24,168,1272,9960,79032 | CONFIRMED |

## Claim 1 — details
Independent search (d_search.py), deliberately different from the audited family:
- R(0) FREE (d+1 coefficients), nodes = any (d+1)-subset of the lowest 24/20/14/11/10 fine values (d=2..6, zero included).
- Targets = ANY ordered selection from the lowest 12/10/9/9/8 coarse values (no monotonicity).
- Score = number of distinct fine eigenvalues over the whole spectrum within 1e-8 of a coarse eigenvalue. Interpolation alone gives d+1 hits by construction.

Results (best full-spectrum hits; baseline d+1 in brackets):

| case | d=2 | d=3 | d=4 | d=5 | d=6 |
|---|---|---|---|---|---|
| carpet L1 2->3 | 4 (3) | 5 (4) | 6 (5) | 7 (6) | 8 (7) |
| carpet L2 2->3 | 4 (3) | 5 (4) | 6 (5) | not run | not run |
| carpet L1 3->4 | 4 (3) | 5 (4) | 6 (5) | not run | not run |
| carpet L2 3->4 | 4 (3) | 6 (4) | 6 (5) | not run | not run |

- Chance floor from the same code: jittered gasket 8-9 hits (baseline 3-4, 366 fine values); random uniform "spectrum" 4-5 hits.
- Sensitivity of my search, synthetic only ([VERIFIED-SYNTHETIC], test-of-test): a fine spectrum built as the full cubic Chebyshev preimage of the carpet level-3 spectrum gives 504 hits at d=3 and 270 at d=4. My search has no least-squares refinement, so it under-recovers (504 of 1528), but the signal is far above chance. Positive control on a real gasket (my own spectra, level 4->5): 47 of 47 nonzero values matched at d=2 and d=3.
- Conclusion: no polynomial of degree <= 6 (R(0) free, non-monotone assignment, low windows) reaches more than about 1 hit above interpolation on the carpet pairs I ran. The "no decimation in this family" conclusion survives an independent attack. Not covered by my attack: rational maps, d=5,6 on the other pairs, windows beyond the low end, level-dependent maps.

Why the literal wording fails (this is the process defect):
1. "matched=0/509, a=None" is produced by the search code's stage-1 filter. A candidate is kept only if it hits >= d+5 of the 40 lowest fine values at 1e-6. Any polynomial through d chosen points matches >= d eigenvalues, so "0 matches" is impossible for an actual R. Re-running the audited search.py with min_hits=0 gives matched=2 (d=2) and 3 (d=3), i.e. exactly the interpolation nodes, for both L1 and L2 at 2->3. decision.md's sentence "not a single fine eigenvalue is mapped onto a coarse eigenvalue by any candidate within 1e-8" is therefore false as worded. The honest statement is "no candidate beat bare interpolation by 5 hits".
2. The survival bar is arithmetically unattainable. A degree-d polynomial has at most d preimages per value, so matched <= d*|coarse|. Max matched fraction at d=6: L1 0.788 / 0.775 / 0.762 and L2 0.813 / 0.776 / 0.758 for pairs 2->3 / 3->4 / 4->5. All below the pre-registered 0.9 survival threshold. Claim H could not have been "LEAD" at d<=6 for any operator on these graphs, whatever the physics. Only the 0.5 kill side was discriminating. The decision.md "why we believe the test could have said yes" is true for the gasket and not for the 0.9 criterion on the carpet.
3. The audited search is narrow: nodes from the lowest d+3 fine values, targets from the lowest 16 coarse values, strictly monotone, a_1>0, R(0)=0. My wider family is a partial answer to this, not a proof.

## Claim 2 — details
Own gasket spectra (operator 4(I-D^-1A)), levels 5 and 6, fed to the audited search():
- Cluster tolerance 1e-7 / 1e-9 / 1e-10 x match tolerance 1e-8 / 1e-10 (6 combinations): every one returns a=[5,-1], 93/95 matched, 96/48 distinct values.
- Operator scaled by 0.37: returns a=[5, -2.7027] = [5, -1/0.37], fraction 1.0. This shows the 5 is not hard-coded (reading search.py also shows no constants).
- Unseen synthetic map z(3.3 - z): returns a=[3.3,-1], 44/45.
- Jitter null (1e-4 relative noise), d=2,3,4: 0 matched. The carpet null is not obtained at a tolerance that kills genuine decimation; the control is 93/95 at the same TOL and clustering.
- Caveat (not a refutation): the gasket operator was changed from D-A to 4(I-D^-1A) after seeing the gasket control fail (Amendment 1, made before any carpet spectrum was searched). The positive control exercises only an exact degree-2 map; partial-decimation sensitivity is supported only by the grid control (which missed the pre-registered < 0.1 bar, 0.26 and 0.12).

## Claim 3 — details
Independent graph (V=41584, E=79032), traces computed from the graph, not from eigenvalues: tr L1 = 158064, tr L1^2 = 765512; tr L2 = 41584, tr L2^2 = 52579.5556. All equal the stored spectrum sums. I also checked higher moments: tr L^3 and tr L^4 from the sparse matrices equal the stored sums of cubes and fourth powers (L1: 4177728, 24656488; L2: 74570.667, 113948.307). Lowest eigenvalues by shift-invert eigsh (L1 x = lam x, and L1 x = lam D x for L2): L1 8.921856e-05 (x2), L2 2.348409e-05 (x2). Matches the claim and the stored values to 1e-12. Levels 1..4 dense spectra (my graph) equal the stored ones to <= 4.2e-14; distinct counts 9/67/510/3948 (L1) and 9/69/509/3933 (L2) agree. Caveat: moments 1-4 plus extremes constrain the level-5 spectrum but do not prove each of the 41584 values; the level-5 null (4->5) rests on a spectrum that was verified this way, not recomputed.

## Claim 4 — details
From my own eigenvalues: lam1(4)/lam1(5) = 9.94756 (L1), 10.03208 (L2); d_w = 2.0911 / 2.0988. Level 3->4: 9.80331 / 10.03562.
Independent estimate of rho (not copied from literature): effective resistance R_n between the left and right sides (each shorted), n=1..5 = 0.75, 1.008587, 1.303173, 1.654398, 2.083397. Successive ratios 1.34478, 1.29208, 1.26952, 1.25931. Aitken extrapolation of the last three ratios gives rho ~ 1.2509, so 8 rho ~ 10.007 and d_w = ln(8 rho)/ln 3 ~ 2.0967. This agrees with the quoted rho ~ 1.2515 and d_w ~ 2.097 to ~0.05%, and the L2 ratio (10.032) is within +0.2% of 8 rho. Literature: I could only reach a secondary source (a citing arXiv paper quoting the Barlow-Bass-Sherwood analytic bounds 1.6737 <= d_s <= 1.8620, via firecrawl excerpt of arXiv:1804.06549). d_s from the ratio, 1.805, lies inside. I did NOT open a primary source that states rho = 1.2515 or d_w = 2.097, so that specific literature number remains secondary-sourced. Also not verified by me: the quoted sentence from arXiv:1902.03408 ("We do not see evidence of the spectral decimation property...", scrape returned nothing usable).

## Claim 5 — details
Own Schur complement (splu, nu=0, onto (3i,3j)) of L1: carpet 2->3: residual 0.1262 in span{A,D,I} (0.1814 for proportionality to L alone), coefficients [-0.354, 0.579, -0.273]; carpet 3->4: 0.1234 (0.1819), coefficients [-0.353, 0.601, -0.344]. Gasket 2->3, 3->4, 4->5: residual 1e-16 / 3e-16 / 2e-15, constant 0.6 (= 3/5). Identical to the audited numbers (0.1262, 0.1234). Interpretation limit: non-closure of the Schur complement is a structural observation, not a proof that no spectral decimation exists. It is consistent with the in-cell diagonal conductances that a 12-point cell boundary produces.

## Claim 6 — details
Own cell/edge counts: n=1..5, V=16,96,688,5280,41584; E=24,168,1272,9960,79032; F counted from the digit rule = 8^n; V-E+F = 0,-8,-72,-584,-4680 = 1-(8^n-1)/7. The Euler check validates the graph builder, not the spectra, since the hole count is taken from the formula.

## Other process findings
- Reruns in rerun/ are "byte-identical" because they are the same code on the same input. That checks reproducibility and the interrupted-run damage, not correctness. Level-5 spectra were never recomputed.
- Test S (pair sums): L2 peak at 2.0 is the bipartite symmetry lambda <-> 2-lambda, and the audit file itself says bipartiteness was not tested numerically. Not re-run here.
- Everything the decision says about literature beyond the Barlow-Bass existence statement is secondary or [WEAK] by its own tags; I agree with the tags.
- Overall: REJECT of the narrow claim H (polynomial decimation, d<=6, in the stated families) stands after independent re-computation. The wording of the evidence ("0.000 everywhere", "not a single eigenvalue mapped", "survival possible") should be corrected to "no candidate exceeded interpolation by more than ~1 hit" and "0.9 unattainable for d<=6 by counting".
