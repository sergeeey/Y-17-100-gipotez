# decision.md -- 20261013-coxeter-round2 (2026-10-13)

**Verdict: REPEAT-for-(c),(d); (a) RESOLVED -> ALREADY_KNOWN-class (Roberts' list is incomplete; the two round-1 diagrams are genuine polytopes;
no LEAD). (b) NOT resolved (tables are images; no way to look at them in this environment).**
Hardware: no heavy parallel jobs; one background job (dim-11 exact control, 235 s, lowprio.py); no multiprocessing.

## (a) Q-ROBERTS-D4-DISCREPANCY -- resolved: the discrepancy is on Roberts' side
The two diagrams (7 nodes, no dotted edge):
* PA = `0-1:inf 0-6:4 1-5:4 2-3:4 2-6:6 3-4:4 4-5:6`
* PB = PA + `3-5:3 3-6:3`
**Third validator (exact3.py, written from scratch, exact arithmetic in Q(sqrt2,sqrt3), does not import cox.py/cox2.py):**
Gram rank 5 / nullity 2 / signature (4,1,2) [VERIFIED]; exact enumeration of cone rays: 12 rays, all timelike/lightlike on ONE sheet, every facet has a
rank-4 ray set, ridge <=> G_ij>-1 exactly, f-vector (12,25,20,7,1), Euler sum 1, exactly one vertex of degree 5 (=d+1), others degree 4, ideal vertices 1 (PA) / 3 (PB),
NO pair of facets without a common face; code-independent exact Vinberg criterion (exact principal minors) also says finite volume [VERIFIED, results/PA_PB_exact_validation.txt].
Controls (results/controls_exact_small.txt, controls_exact_dim11.txt): 10/10 small cases PASS incl. positives E10=T(2,3,7) (d=9), [3,3,6],[6,3,6],[4,4,4],[3,6,3],[4,3,6]; negatives E11=T(2,3,8) (spacelike ray), E9~ affine, A4~ affine, decomposable pair;
dim-11 Tumarkin-type pyramid E8~+A1~+A1~ accepted (f-vector (37,216,669,1365,1968,2058,1572,870,340,89,14,1), Euler 1 -- identical to the round-1 verifier's Qhull f-vector), and two label-perturbed copies
rejected (15/37 and 17/37 spacelike rays). Agreement with cox2.geom_validate on all 13 cases. K-A1, K-A2 not triggered.
**Why Roberts' dim-4 appendix cannot contain them [VERIFIED by reading the TikZ source and by computation]:** I enumerated all standard Gale diagrams of 4-polytopes with 7 facets having exactly one
nonzero opposite pair (weights 1): 5 combinatorial types (gale_one_pair.py). PA and PB both have the combinatorial type Gale k=6 mu=(0,1,0,1,0,1,1,0,1,0,1,1) (incidence-graph isomorphism, results/PA_PB_gale_match.txt),
which has ZERO combinatorially disjoint facet pairs, hence no dashed edge is possible. Roberts' dim-4 figures use exactly two of the five types
(k=5 (0,1,0,1,0,1,1,1,0,2), 1 disjoint pair; k=4 (0,1,1,0,1,1,0,3), 2 disjoint pairs; results/roberts_gale_types_d4.txt) and every diagram there carries 1-2 dashed edges (read in 1511.08451 sec. 7.1).
Roberts himself writes that the thesis gave "a near classification" (sec. 1) while the abstract says "full".
**Independent third-party corroboration [DOCS]:** Ma-Zheng, arXiv:2401.13698v3 (Theorem 1.1: 331 finite-volume Coxeter 4-polytopes with 7 facets) state: "we include the 140 polytopes that were missing from Roberts's census in dimension 4,
thereby achieving a comprehensive coverage of 164 non-pyramidal Coxeter 4-polytopes with 7 facets and one non-simple vertex. These polytopes are realized over the five combinatorial types P7..P11 ... P9 and P10 are involved in Roberts's original list."
This matches my independent Gale count exactly (5 types; Roberts covers 2). Hence PA/PB are almost certainly among those 140 (not a new object). [INFERRED: I did NOT locate PA/PB row-by-row in Ma-Zheng's tables; their Table format
(angle-matrix rows over P7..P11) was not decoded.] CoxIter: looked (`where`, find under C:/Users/serge and E:/): not present; not installed.
=> Q-ROBERTS-D4-DISCREPANCY: Roberts incomplete (confirmed from three directions), round-1 toolkit correct. Not a LEAD (K3: the objects are in the published literature).

## (b) Tumarkin 2004 vs survey dimension discrepancy -- NOT resolved
* Primary text read (arXiv math/0311272v2, the short version of Tumarkin 2004): Lemma 4: a finite-volume pyramid with n+3 facets is a pyramid over a product of three simplices; "Their dimension does not exceed 11." [VERIFIED]
  Theorem 1: no polytope for n>=17, "a unique polytope with 19 facets" in H^16. Round 1 read the same bound in the full AMS text.
* Survey (polytopes.html, links are `poly/pyram3.pdf`, `poly/16.pdf`; relative-path trap: `./pyram3.pdf` 404s): "dim=4,...,9,13". The pyram3.pdf text layer (markitdown) contains only the structure rule
  (Sigma_1 from the left column of Table 1, Sigma_2, Sigma_3 from the right column, or all three from Table 2); Tables 1, 2 are graphics: the Browser pane receives a download dialog for the PDF, the pdf-viewer MCP would not mount. NOT read.
* NEW: the same list "4,5,...,9 and 13" is repeated in Ma-Zheng 2401.13698 (intro) as a statement about Tumarkin's pyramids -- so it is a propagated claim, not a one-off survey typo. My (and round 1's, and the verifier's) enumeration gives d in {4,5,6,7,11}.
* Numerical observation (INFERRED/WEAK, a hypothesis only): d+2 = (number of facets at the apex = number of nodes of Sigma_1+Sigma_2+Sigma_3) takes the values {6,7,8,9,13} on my 56 classes. That reproduces "..,9,13" of the survey list but not its lower end "4,5".
  If the survey's list were "d+2" it would read {6,...,9,13}; nothing verifies this. Row-by-row identification of Tumarkin's Tables 4/5 with dimensions: NOT done.
Status: [UNKNOWN]; the conflict between "<=11 (primary)" and "13 (survey, Ma-Zheng)" stands, with my enumeration supporting the primary.

## (c) k=2 non-pyramidal family, d>=5 -- NOT finished; precise statement of coverage
Terminology: "k=2" = n - (d+1) = 2 facets outside the single non-simple (ideal) vertex, whose d+1 facets form two connected parabolic diagrams A,B (Roberts' / Gale "one opposite nonzero pair" family).
* Enumerated by round 1 (rooted2.py, labels {3,4,5,6,inf}, NO dotted edges): d=3,4,5 completed (7 strict-geometry polytopes in total per round-1 decision.md/skeptic_verdict.md: 6 in d=4, 0 in d=5, the 7th in d=3); d>=6 never run. The prune is not independently validated (bf_check.py never run).
* NEW this round (gale_one_pair.py, results/gale_types_d3_8.txt): the no-dotted-edge condition is equivalent to "no pair of facets without a common face". Hence the family splits by Gale type; the number of one-pair types / types with zero disjoint pairs:
  d=3: 2/0, d=4: 5/1, d=5: 14/6, d=6: 29/17, d=7: 64/46, d=8: 127/103. So for d=4 the no-dotted family consists of ONE combinatorial type (the PA/PB type), for d=5 of six types, etc.
  Everything with a Gale-disjoint pair needs an ultraparallel (dotted) edge: NOT covered by any search of mine or of round 1 (Roberts covers part of it; his dim-4 list misses 3 of the 5 types).
* NOT covered: (i) all polytopes with a dotted edge; (ii) labels >6 (round 1 argued labels <=6 only for pyramids); (iii) d>=6 of the no-dotted family -- the labelling search per Gale type (vertex = spherical/connected affine; Vinberg extension condition for pairs x in A, y in B) was designed but NOT implemented
  within the iteration budget; (iv) polytopes with >=2 non-simple vertices or all vertices simple. No claim "no polytope exists" is made for any d>=5.

## (d) Tumarkin's dim-16 polytope -- NOT reproduced
Its diagram is an image (Roberts' Dim16CoxPoly.png, survey 16.pdf); I could not view it, and did not invent it from memory. A blind search at n=19 requires the Gale-guided CSP of (c) plus quasi-Lanner/Lanner machinery (Tumarkin's paper); not feasible in this round.
The high-dimension positive control that WAS achieved is the dim-11 Tumarkin-class pyramid (exact validator, n=14, 235 s).

## Overlap with the parallel session (YBE / Coxeter-adjacent)
grep of registry/graph.yaml: only SUB-COXETER-N3-FINITE-VOLUME, H-COXETER-1, Q-ROBERTS-D4-DISCREPANCY mention Coxeter polytopes; experiments/20261003-c-ybe-001 and 20261004-c3-obstruction-cas contain no "Coxeter polytope" text. No overlap, no contradiction.

## Kill criteria status
K-A1 passed; K-A2 passed (both diagrams valid polytopes); K-A3 triggered as designed: "Roberts incomplete" -- confirmed independently (Ma-Zheng 2024), so NOT a LEAD; K-D not met (not reproduced, stated).
Suggested graph.yaml update (NOT made by me, read-only rule): Q-ROBERTS-D4-DISCREPANCY -> resolved: Roberts' dim-4 census omits 3 of 5 one-nonsimple-vertex combinatorial types (Ma-Zheng 2401.13698: 140 missing polytopes).

## What this result does NOT mean
1. Does not show PA/PB appear (row by row) in Ma-Zheng's tables.
2. Does not resolve the 8,9,13 vs <=11 question; does not show the survey is wrong (images unread).
3. Does not classify anything for d>=5.
