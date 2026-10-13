# claim.md -- 20261003-coxeter-n3-completeness (written BEFORE the main enumeration)

Date: 2026-10-03. Tier: Standard (computational verification / reproduction task).

## L0 gate (EstimandOps)
Question type: DESCRIPTIVE / combinatorial-existence ("which Coxeter diagrams on n = d+3 nodes
define finite-volume hyperbolic polytopes in a stated family"). No causal or predictive content.
Natural-language statement: "We enumerate all connected Coxeter diagrams with n = d+3 nodes in a
precisely stated family F and decide, with two independent implementations of the finite-volume
criterion, which of them are finite-volume hyperbolic Coxeter polytopes; we compare the resulting
list with the published classes (pyramids over products of three simplices, Tumarkin 2004; one
non-simple vertex, Roberts 2015; compact, Tumarkin 2007)."

## What this result does NOT mean (pre-registered)
1. It is NOT a classification of all finite-volume polytopes with n = d+3 facets: dotted edges
   (disjoint facets, p >= 1) are outside the enumerated family.
2. A match with published lists is a reproduction, not a new theorem; absence from a list that
   I could only partly read is NOT proof of novelty.
3. Label alphabet is bounded (stated per run); polytopes needing other labels are not covered.

## Claims
C1 (toolkit): my implementation of Vinberg's criterion (elliptic / parabolic subdiagrams, each
rank d-1 elliptic subdiagram extends in exactly 2 ways) and my independent geometric
implementation (extreme rays of the cone {x : <e_i,x> <= 0} in R^{d,1}, no diagram combinatorics)
agree on every control and on a mutation differential test, and reproduce known counts of
hyperbolic Coxeter simplices (Lanner / quasi-Lanner) per dimension.
C2 (enumeration): within family F the enumeration returns a finite list per dimension; every
member falls into a published class.

## Kill criteria (fixed before running)
K1: ANY disagreement between the two criterion implementations on a control or on the mutation
    test, or any failure to reproduce the known simplex counts => toolkit NOT trusted; no
    enumeration claim is made (verdict BLOCKED/REJECT on the toolkit).
K2: positive control must be able to return positive: a code path that cannot return a
    finite-volume polytope on known finite-volume diagrams is invalid.
K3 (LEAD gate): a LEAD requires a polytope returned by BOTH implementations, with Euler
    relation f-vector check passing, that is absent from all published lists I can actually read.
    If every enumerated polytope falls into a published class => verdict REPEAT / ALREADY_KNOWN
    (validated reproduction), NOT LEAD.
K4 (negative control): diagrams known NOT to be finite volume (e.g. Gram signature (d,2),
    or a Lanner simplex with one label raised) must be rejected by both implementations.

## Family F (precise, per run)
Connected Coxeter diagrams, n = d+3 nodes, edge codes {none(pi/2), 3,4,5,6, infinity(parallel)},
NO dotted edges (all facet pairs intersect or are parallel), containing a parabolic subdiagram
of rank d-1 with c components at an ideal vertex (rooted search; see run logs for the label
alphabet actually used).

---
## AMENDMENT 2026-10-04 (resume round; written BEFORE re-running the controls/enumerations, after reading
## the interrupted-run logs -- amendments are post-hoc w.r.t. the first attempt and are marked as such)
1. The first attempt's `vinberg_check` + `geo_check` (cox.py) both accepted 900+ Gram matrices from the rooted
   k=2 search that the strict validator `geom_validate` (cox2.py) rejects ("spacelike ray", i.e. the cone
   {x : <e_i,x> <= 0} is not inside the light cone => infinite volume). So the pair (vinberg_check, geo_check)
   is NOT an adequate arbiter on arbitrary candidate matrices. From now on the arbiter is `geom_validate`
   (cone built from scratch, ridge structure must reproduce the fed diagram, f-vector Euler sum == 1,
   #facets == n); `vinberg_check` is a second, independent implementation. A LEAD needs BOTH to say
   "finite volume" AND Euler OK.
2. K1 is refined, not weakened: (soundness) every matrix accepted by geom_validate MUST be accepted by
   vinberg_check; any violation = BLOCKED. (completeness) matrices accepted by vinberg_check but rejected by
   geom_validate must be explained (Vinberg's theorem presupposes G is the Gram matrix of an actual polytope);
   the explanation is tested in controls2.py via the Euler sum of the face counts Vinberg's own
   combinatorics would assert.
3. Interpretation of "pyramid" dimension lists is checked against the PRIMARY source (Tumarkin, Trans. Moscow
   Math. Soc. 65 (2004), section 4: pyramids over a product of three simplices "have dimensions at most 11")
   because the Felikson-Tumarkin survey page says "dim=4,...,9,13" for the same class.
4. Pre-registered expectation for pyramids over THREE simplices (n=d+3) with labels in {3,4,5,6,inf}:
   dimension set contained in {4..11}; K-PYR kill: any diagram in dim >= 12 => toolkit/enumeration suspect.
   For TWO simplices (n=d+2) the control is the published dimension set {3..13, 17} (survey, Tumarkin 2004).
