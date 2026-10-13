# claim.md -- 20261013-coxeter-round2 (written 2026-10-13 BEFORE the new computations)

Tier: Standard. Follow-up to experiments/20261003-coxeter-n3-completeness (round 1; READ-ONLY).

## L0 gate (EstimandOps)
Question type: DESCRIPTIVE / combinatorial-geometric existence (no causal/predictive content).
Statement: "We decide, with an exact-arithmetic validator written independently of cox.py/cox2.py, whether the two
4-dimensional Coxeter diagrams (7 nodes, no dotted edges, exactly one non-simple vertex) that round 1 reported as
finite-volume polytopes are finite-volume polytopes, and whether they appear in Roberts' list (arXiv:1511.08451, dim 4
appendix); we also record which Tumarkin-2004 table row corresponds to which dimension, and state exactly what part of
the k=2 non-pyramidal family is enumerated."

## Tasks (from the dispatcher)  (a) Q-ROBERTS-D4-DISCREPANCY  (b) Tumarkin 2004 table vs survey dims  (c) k=2 family d>=5
(d) Tumarkin dim-16 polytope as positive control.

## Pre-registered kill criteria
K-A1 (validator trust): the new exact validator must (i) accept a published control (Tumarkin-type pyramid in dim 11,
     E8~+A1~+A1~ glued; and one hyperbolic simplex per dim) and (ii) reject a perturbed negative control (one label of
     the dim-11 control changed to give signature (d,2) or spacelike rays). If either fails, no verdict on (a).
K-A2 (discrepancy resolution): the two round-1 diagrams are "valid finite-volume polytopes" only if the exact validator
     gives: Gram signature (4,1,nullity 2), all cone extreme rays timelike/lightlike on ONE sheet, every facet has
     rank-4 vertex set, ridge structure = Gram, Euler = 1. If any fails -> round 1 was wrong (the two diagrams are NOT
     polytopes).
K-A3 (consistency with Roberts): if valid, determine from the face lattice whether any pair of facets is combinatorially
     disjoint (forcing a dashed edge in the Coxeter diagram). If NO disjoint pair exists, then Roberts' "full classification"
     in dim 4 (every figure has a dashed edge) is either incomplete or defined for a narrower class; this is stated as a
     DISCREPANCY WITH A PUBLISHED LIST, not as a discovery, and is a LEAD only after (1) exact validation, (2) a second
     independent validator, (3) check of Roberts' definitions (e.g. "non-pyramidal", "one non-simple vertex").
K-D (positive control, high dim): the dim-16 Tumarkin polytope must be reproduced from its diagram by the exact/float
     validator within the hardware budget, else reported as NOT reproduced (not claimed).

## What this result does NOT mean (pre-registered)
1. Does NOT classify all finite-volume polytopes with n=d+3 facets.
2. A discrepancy with Roberts' list is not a theorem about Roberts' correctness: his appendix is a TikZ rendering of a
   thesis result and is stated by him as a classification; mismatches may be definitional.
3. Agreement of my validators does not prove the polytopes are new: the 2 diagrams may be in lists I cannot read
   (images in PDFs), so 'absent from lists I could read' is the only supportable statement.
