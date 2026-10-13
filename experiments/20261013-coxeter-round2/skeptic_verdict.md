# skeptic_verdict.md -- 20261013-coxeter-round2 (independent falsification pass, 2026-10-13)

Scope: five claims from the dispatcher. All checks below were re-derived with NEW code written in the verifier's scratchpad
(not exact3.py / cox.py / cox2.py / gale_enum.py); scripts are in
`C:/Users/serge/AppData/Local/Temp/claude/E-------------------------------------------------Y-17-100-gipotez/9e146a80-48ac-4700-aadb-0cf8d72b4b4e/scratchpad/skv_cox2/`
(myval.py, ridge.py, klein.py, mygale.py, iso.py, tabs.py, fastval.py, fvec.py, robd4c.py). No git, no installs; heavy jobs ran through lowprio.py (max 16 s).

## Summary table
| # | claim | verdict |
|---|---|---|
| 1 | PA, PB are finite-volume polytopes, f=(12,25,20,7,1), 7 facets, one degree-5 vertex, no disjoint facet pair | CONFIRMED |
| 2 | PA/PB absent from Ma-Zheng tables (so Ma-Zheng incomplete too) | REFUTED: PA = P_{7,1}, PB = P_{7,2} |
| 3 | exactly 5 one-pair Gale types in d=4; Roberts' appendix covers only k=5 and k=4 | CONFIRMED |
| 4 | survey list "4..9,13" unresolved; hypothesis list = {d+2} | hypothesis REFUTED; dims 8,9,13 NOT supported (evidence strong but Tumarkin Tables 4/5 themselves unread) |
| 5 | dim-11 control f-vector (37,216,669,1365,1968,2058,1572,870,340,89,14,1) | CONFIRMED |

## 1. PA / PB (independent method)
Method: mpmath 40 digits, Lorentz realisation of the Gram matrix (eigendecomposition, signature (4,1), nullity 2), every 4-subset of the 7 facets -> null vector -> keep rays with
all (x,e_j) <= 0 -> classify by norm -> incidence -> face lattice as closure of facet vertex-sets under intersection, face dimension by rank.
* PA: 12 rays, 0 spacelike, one sheet, 1 ideal; all 7 facets have rank-4 ray sets; f=(12,25,20,7,1); boundary chi=0; vertex facet-counts = eleven 4s and one 5; disjoint facet pairs: none.
* PB: same f-vector and degree pattern, 3 ideal vertices, no disjoint pair.
* Dihedral check (ridge.py): for every pair, "shares a 2-face" <=> G_ij > -1, and every ridge angle is pi/integer to 1e-20: no violations in either.
* Third method (klein.py, scipy HalfspaceIntersection in the Klein model, float): 12 vertices each, 1 resp. 3 on the sphere |y|=1 (ideal), rest inside; Chebyshev radius 0.25/0.31 (nonempty interior).
* Negative control (PA with 2-6 label 6 -> 5): rejected (signature). Not exhaustive, but it can return negative.
Not re-run: the "exact principal minors" Vinberg test of exact3.py (not needed once rays are enumerated).

## 2. Ma-Zheng arXiv:2401.13698v3 -- PA and PB ARE there
Primary source opened myself (arXiv LaTeX cache, v3). Facts:
* Table "disjoint pairs d_k": P_7 has d_k = {} (no disjoint pair); P_7 is the only zero-disjoint-pair type among P7..P11 (P8:1 pair, P9:2, P10:1, P11:2) -- agrees with my Gale count in claim 3 (types by #disjoint pairs 0,1,1,2,2).
* Table "Results for Theorem 1.1" lists P_{7,1}, P_{7,2} with Coxeter vectors (rows i=0..5, entries j>i; 2 = no edge, 0 = parabolic/inf):
  P_{7,1} = 222264|46222|2220|422|42|2, 1 cusp, volume 5/216 pi^2;  P_{7,2} = 222364|46322|2220|422|42|2, 3 cusps, volume 31/432 pi^2.
* Decoding: P_{7,1} edges 0-5:6, 0-6:4, 1-2:4, 1-3:6, 2-6:inf, 3-4:4, 4-5:4, a 7-cycle with labels inf,4,6,4,4,6,4. networkx edge-labelled isomorphism (iso.py):
  PA ~ P_{7,1} True, PB ~ P_{7,2} True, cross pairs False. Cusp counts (1 and 3) match the ideal-vertex counts of claim 1.
* Therefore the alternative "Ma-Zheng's list is incomplete too" is FALSE. The folder's [INFERRED] "PA/PB are among the 140" was right but was not row-matched; now matched.
* Cross-check of the quoted sentence: "we include the 140 polytopes that were missing from Roberts's census ... 164 non-pyramidal ... P7..P11 ... P9 and P10 are involved in Roberts's original list" -- present verbatim in the intro; 164 = 2+11+134+4+13 (P7,P8,P9,P10,P11 counts in the figure captions); Roberts' 24 = P_{9,7..16, 119..128} (20) + P_{10,1..4} (4) per Sec. "Validation". 164-24 = 140.
* Note: Ma-Zheng's own caveat that Roberts' 24 sit inside P9 (134 polytopes) and P10 means Roberts is also incomplete WITHIN the two types he covers (114 + 0 missing in P9/P10). The folder does not mention this.

## 3. Gale types (independent enumeration)
mygale.py: configurations of 7 (resp. 6) vectors in R^2 on the 2L-gon, L=2..n; multiplicity compositions; polytope condition (every open half-plane >= 2); cofaces by an exact half-plane test;
vertices = complements of minimal cofaces; keep configurations with exactly one minimal coface of size 2 and all others of size 3; deduplicate by facet-relabelling canonical form of the vertex-facet incidence (7! perms, no networkx).
Result d=4: 5 types, vertices 10,11,10,11,12, disjoint pairs 2,1,2,1,0, with Gale words (4,(0,1,1,0,1,1,0,3)), (4,(0,1,1,0,2,0,1,2)), (5,(0,1,0,1,0,1,0,1,1,2)), (5,(0,1,0,1,0,1,1,1,0,2)), (6,(0,1,0,1,0,1,1,0,1,0,1,1)) -- identical to results/roberts_gale_types_d4.txt. d=3 gives 2 types, both with 2 disjoint pairs (agrees with the folder's "2/0").
Roberts 1511.08451 (LaTeX cache): Definition 4.1 gives the same four rules as Tumarkin's, so there is no definitional reason for the omission. The dim-4 appendix has 24 diagrams; parsing the TikZ labels (robd4c.py): 4 diagrams on the 10-gon word (1,1,0,2,0,1,0,1,0,1) (1 dashed edge each) and 20 on the 8-gon word (1,1,0,1,1,0,3,0) (2 dashed edges each). Exactly two of the five types; the zero-disjoint type (PA/PB) is not used. Consistent with Ma-Zheng's P9 (2 disjoint pairs) and P10 (1 pair). CONFIRMED. (The folder's d>=5 type counts 14/6, 29/17, ... were not re-derived.)

## 4. Tumarkin tables / survey dimension list
What I did read: (i) the survey page polytopes.html (curl): "Pyramids over a product of three simplices [Tum3], dim=4,...,9,13." and "over two simplices ... dim=3,...,13, 17" -- exact quotes verified; (ii) Ma-Zheng intro repeats "4,5,...,9 and 13" (verified); (iii) Tumarkin short note math/0311272v2 text: Lemma 4 "Their dimension does not exceed 11" (verified); (iv) poly/pyram3.pdf rendered with PyMuPDF (the tables ARE readable: the PDF has one page, the text layer holds only the rule, the tables are vector/image) and viewed.
What I could NOT read: Tumarkin, Trans. Moscow Math. Soc. 65 (2004) Tables 4/5 -- the AMS URL returns a Cloudflare challenge (403); I did not try to bypass it. So "Tables 4/5" row-by-row = UNREAD; the survey's pyram3.pdf Tables 1/2 are what I read.
Structural fact (derived, not cited): for a pyramid over a product of three simplices n=d+3, the apex lies on the d+2 non-base facets, which must form a parabolic diagram of three connected components, so d = (number of white nodes in Sigma_1+Sigma_2+Sigma_3) - 2.
Test (tabs.py, fastval.py): I glued diagrams as drawn in pyram3.pdf (labels decoded by eye: single=3, double rail=4, bold=inf), under two readings of "left/right column", 234 candidates with d in {4..9,11,12,13}, and tested each with a float geometric validator (rays, spacelike test, ridge/Gram consistency; validator accepts PA, PB, rejects a perturbed PA).
Result: finite-volume candidates occur ONLY at d = 4,5,6,7,11 (9,9,6,9,3 found); every candidate at d = 8 (57), 9 (18), 12 (15), 13 (6) has spacelike rays (infinite volume). E8~ + two 2-white diagrams reproduces the 37-ray dim-11 polytope. Limits: Table 2 (triple-bond diagram) not encoded; my counts at d=6,7 (6 and 9, plus Table 2) fall short of round 1's 12 and 13, so my decoding is incomplete (about 3+3 classes unmatched) -- this is corroboration of the dimension SET, not an independent classification.
Hypothesis "survey list = {d+2}": the 56 round-1 classes have d in {4,5,6,7,11}, d+2 in {6,7,8,9,13}. The survey list is {4,5,6,7,8,9,13}: equality FAILS (the list contains 4,5 and omits the existing d=11). It matches only the upper part. Possible readings (not decidable here): list mixes d and d+2, or is simply a transcription slip; 11 (E8~ + A1~ + A1~) certainly exists (claim 5), so the survey/Ma-Zheng statement "exist only in 4..9 and 13" is false as literally written. So: pyramids over three simplices in dimensions 8, 9, 13: NOT supported by any computation here (candidates at those dimensions are all infinite-volume), and contradicted by Tumarkin's Lemma 4 (<= 11). Verdict on the folder's open point: lean strongly toward "survey/Ma-Zheng list is wrong", but a row-by-row read of Tumarkin 2004 Tables 4/5 remains undone.

## 5. dim-11 control
fvec.py (numpy SVD ray enumeration + float rank closed-set lattice, 0.3 s): n=14, d=11, 37 rays, f=(37,216,669,1365,1968,2058,1572,870,340,89,14,1), boundary chi=2 (=1-(-1)^11). Identical to results/controls_exact_dim11.txt. Same diagram arises from the survey table as E8~ + A1~ + A1~ glued at the base node (tabs.py, 37 rays).
CONFIRMED. (Caveat: the f-vector agreement between two implementations proves the validators agree, and Euler holds; "this is a published Tumarkin polytope" is supported by Tumarkin Lemma 4 + the survey table shape, not by a numeric check against a published f-vector.)

## Process issues
1. decision.md (b) says the tables "are images; no way to look at them in this environment". False: PyMuPDF (installed in ape311) renders the PDF and the image can be read. The open point was closable in minutes.
2. decision.md (a) kept "[INFERRED] I did NOT locate PA/PB row-by-row in Ma-Zheng" -- honest, but the task was cheaply decidable: the Ma-Zheng source is in the local arxiv cache and the P7 rows are 2 lines. Not a falsehood, an unfinished check.
3. No positive control from the exact class (n=d+3=7, one non-simple vertex, d=4) was run before declaring the validator trustworthy for it: all positives (E10, small simplices, dim-11 pyramid) have no non-simple-vertex d=4 7-facet member. The class-specific control (any of Ma-Zheng's P9/P10 or Roberts' diagrams, which carry dashed-edge lengths) was not exercised. My own check is also not class-specific for Roberts' diagrams; PA/PB validity is nonetheless established by three methods and by the Ma-Zheng match.
4. Round-1 vs round-2 label "ALREADY_KNOWN, no LEAD" is right, but the stated reason ("Roberts incomplete from three directions") overstates: the three directions share one fact (the number of Gale types); only the Ma-Zheng statement is independent of the Gale count. Roberts' omission of 3 of 5 types is nevertheless confirmed.
5. Missed finding: Ma-Zheng places Roberts' 24 inside P9 (134 polytopes) and P10 (4), so Roberts' list is incomplete also inside the two types he covers; the folder says only "3 of 5 types missing".
6. Hardware rules respected; no marker misuse found: the [VERIFIED] tags in decision.md that I re-ran (claims 1, 3, 5) hold.
7. Not verified by me: d>=5 Gale type counts (14/6, 29/17, 64/46, 127/103); the exact-arithmetic "Vinberg exact" claim; round 1's "full AMS text read" (AMS blocked for me).
