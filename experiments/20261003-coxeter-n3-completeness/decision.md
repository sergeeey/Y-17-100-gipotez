# decision.md -- 20261003-coxeter-n3-completeness (resume round, 2026-10-04)

**Verdict: ARCHIVE the validated reproduction (status ALREADY_KNOWN, no LEAD). REPEAT only for the two families
that were not completed (k=2 "Roberts-type" search for d>=5; k=3 / simple-vertex search needed for Tumarkin's
dim-16 polytope).**

## What was done (all re-run in this round, hardware rules respected: one process at a time, lowprio.py, 45 s cooldowns)
| item | result | evidence |
|---|---|---|
| CoxIter available locally? | not looked for beyond the earlier session (no install attempted); own toolkit used | cox.py, cox2.py |
| Library transcription (spherical/affine diagrams) | 0 failures | results/controls1_rerun.txt |
| Simplex positive control (all hyperbolic Coxeter simplices, labels 3..6/inf, d=3..9) | compact 9, 5 (d=3,4); non-compact 23, 9, 12, 3, 4, 4, 3 (d=3..9); 0 disagreements, 0 Euler failures | results/controls1_rerun.txt (counts agree with the published Lanner / quasi-Lanner tables, from memory of Vinberg/Chein: [INFERRED], not re-read from a primary source this round) |
| Negative controls | chain [3,5,4], E11 (sig (10,2)), chain [5,3,3,3,5] rejected by BOTH implementations. NOTE: the old "negative" Lanner [3,5,3] label 5->6 is actually [3,6,3], a genuine non-compact simplex; both implementations correctly accept it (mis-labelled control, not a failure) | results/controls1_rerun.txt |
| Differential test, 99 verified positives (n = d+1, d+2, d+3) | Vinberg finite 99/99, strict geometry 99/99, Euler/facet-count OK | results/controls2_out_v2.txt |
| Differential test, 900 mutants | 205 both-positive, 695 both-negative, 0 disagreements (note: mutations of rank-deficient Gram matrices mostly give nondegenerate ones, so this mainly probes the n=d+1 regime) | results/controls2_out_v2.txt |
| First-run disagreements: 1796 of 1803 stored candidate matrices (c2k2) were "finite" for Vinberg but rejected by the strict geometry | ALL 1796 have NO timelike ray at all (cone lies outside the light cone => no hyperbolic polytope with that Gram matrix exists) and the true signature dimension differs from the dimension the search assumed. Vinberg's theorem presupposes the polytope exists. | results/ (tally_vng.py output: total 1803, V_not_Gv 1796, no_timelike_ray 1796, other 0) |
| Independent enumeration of pyramids over a product of 2 simplices (n=d+2), labels {3..12,inf} | 200 iso classes, dimension set {3,...,13,17}; counts d=6..17: 27,26,16,10,5,5,2,3,0,0,0,1. Identical (dimension by dimension) to the rooted search c2k1 (a different algorithm). Matches the published dimension set (survey: "dim=3,...,13, 17"). | results/pyr2_p2_lab12.txt, results/c2k1_d*.txt |
| Same for 3 simplices (n=d+3), labels {3..12,inf} | 56 iso classes, dimensions {4,5,6,7,11}, counts 13,15,12,13,3. Identical to rooted search c3k1 (labels {3,4,5,6,inf}; d=3..18, all with found counts: d=8,9,10,12..18 = 0). Labels 7..12 add no compatible option at all (pair table identical to the 6-label run: 665 compatible pairs) | results/pyr2_p3_lab12.txt, results/c3k1_d*.txt |

Every one of the 56 + 200 enumerated diagrams: accepted by `vinberg_check` AND `geom_validate`, Euler sum of the f-vector = 1, #facets = n.

## Comparison with the literature
* n=d+2 pyramids: dimension set reproduced exactly (3..13, 17). [VERIFIED computationally vs survey page].
* n=d+3 pyramids over three simplices: Tumarkin, Trans. Moscow Math. Soc. 65 (2004), section 4 (full text read):
  "The corresponding polytopes have dimensions at most 11." Tumarkin's short note (arXiv math/0311272) says the
  same. My enumeration gives {4,5,6,7,11}: consistent, with the maximal case 11 realised (E8~ + A1~ + A1~ glued
  at the base node; 3 diagrams).
* DISCREPANCY (documentary, not mathematical): the Felikson-Tumarkin survey page lists this class as
  "dim=4,...,9,13". The primary source says <= 11, so "13" cannot be right, and my exhaustive enumeration finds
  nothing in dim 8, 9 (nor 10, 12, 13, ...) for labels <= 12. The tables of Tumarkin (Tables 4, 5) and the survey
  PDF pyram3.pdf are images that I could not read, so I cannot say which published dimensions in 8..9 the survey
  intends. Most likely a transcription slip in the survey (the n+2 list is "3,...,13,17"); [UNKNOWN] until the
  tables are read by eye. This is NOT a new theorem and NOT a LEAD.

## Kill criteria (claim.md)
K1 (toolkit): soundness leg (geometry-accepted => Vinberg-accepted) holds on every control, mutant and enumerated
   set: 0 violations. Completeness leg: the only disagreements (1796) are fully explained (empty P in H^d).
   NOT triggered, but the first-run arbiter (vinberg_check + geo_check) is withdrawn as insufficient; arbiter is
   geom_validate (claim.md amendment).
K2 positive controls can return positive: yes (99 + 256 positives, 0 false negatives).
K3 LEAD gate: no enumerated polytope outside a published class => NOT a LEAD.
K4 negative controls rejected by both: yes.
K-PYR: no diagram in dim >= 12 => not triggered.

## What this does NOT mean (pre-registered + added)
1. NOT a classification of finite-volume polytopes with n=d+3 facets: dotted edges and the non-pyramidal
   one-non-simple-vertex case (Roberts, arXiv 1511.08451, dims 4..10) were NOT enumerated this round. The earlier
   k=2 run only completed d=3,4,5 (7 strict-geometry polytopes found, 6 of them d=4, 0 at d=5); d>=6 were killed
   by the machine shutdown/timeouts and not re-run. Roberts' diagrams are images in the PDF; no diagram-level
   comparison was possible.
2. Tumarkin's unique dim-16 polytope was NOT reproduced as a positive control: its diagram is an image
   (survey 16.pdf); it has no one-non-simple vertex in my k<=2 family (Roberts finds none in dim >= 11), so it
   needs a k=3 / simple-vertex search, which was not implemented.
3. The "prune is exact" claim for rooted2.py (k=2) is not independently validated (bf_check.py was neutered to run
   serially and not run). For k=1 (c=2,3) the pruned DFS agrees with the independent McLeod-lemma enumeration
   dimension by dimension, which is strong evidence for k=1 only.
4. Labels > 12 were not enumerated. Evidence they do not matter for p=3: labels 7..12 produced zero compatible
   options; a proof for arbitrary labels was not written.
5. Counts of simplices quoted from memory of Vinberg/Chein are [INFERRED], not re-read.

## Next (if continued)
* Read Tables 4/5 of Tumarkin 2004 by eye to settle the dim-8,9 question (the one open documentary point).
* Serial, chunked (per-root, checkpointed, <= 10 min per job) re-run of rooted2 k=2 for d=5..10 with geom_validate
  as arbiter, compared against the counts of Roberts' appendix read by eye.
* k=3 rooted search at d=16 for the Tumarkin polytope as a positive control.
