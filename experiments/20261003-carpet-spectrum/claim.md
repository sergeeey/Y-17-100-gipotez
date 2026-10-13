# claim.md — 20261003-carpet-spectrum (written BEFORE any carpet spectrum was computed)

Date: 2026-10-03. Tier: FL Standard (narrow computational claim). Evidence markers per CLAUDE.md.

## L0 (EstimandOps) classification
DESCRIPTIVE. We describe the spectra of finite graphs (exact linear algebra). No causal and no predictive claim.
Nothing here is an analytic statement about the continuum Sierpinski carpet or about non-existence of any method.

## Objects (pre-registered definitions)
- Gasket graph G^S_n: standard Sierpinski gasket graph level n (G_0 = triangle; G_{n+1} = 3 copies of G_n glued at corners), (3^(n+1)+3)/2 vertices.
- Carpet graph G^C_n: lattice points (x,y) in {0..3^n}^2 lying in at least one retained closed unit cell of the level-n carpet
  (retained cells = 8^n cells of the 3^n x 3^n grid obtained by removing the middle ninth recursively); edges = unit lattice
  segments that are sides of a retained cell. G^C_0 = 4-cycle, G^C_1 = 16 vertices / 24 edges. G^C_{n+1} = 8 copies of G^C_n glued along shared sides.
- Operators (pre-registered, both reported): (L1) combinatorial Laplacian L = D - A (primary);
  (L2) random-walk generator I - D^{-1}A (secondary; carpet degrees vary 2..4).
  For the gasket the standard Neumann Laplacian D - A is used (corner degree 2, others 4).

## Claim H (the narrow falsifiable claim)
"There is a real polynomial R of degree d <= 6 with R(0)=0, the same for all level pairs, and a small exceptional set E
(<= 5 distinct values), such that for each level pair (n, n+1) with n >= 2, at least 90% of the distinct eigenvalues of
spec(G_{n+1}) \ E satisfy |R(mu) - lambda| <= 1e-8 for some lambda in spec(G_n), and the images cover >= 50% of the distinct
values of spec(G_n)" (the coverage condition rules out trivial R, e.g. R = 0 or R mapping everything onto few values).
"Distinct" = eigenvalues clustered at tolerance 1e-9 (eigvalsh error is ~1e-13).

## Search family (pre-registered; limitation stated in advance)
Polynomials with R(0)=0, nodes taken from the lowest distinct eigenvalues of the finer level, monotone assignment to the
lowest distinct eigenvalues of the coarser level, then iterative least-squares extension. This misses decimation maps with
R(0) != 0, rational maps, and maps whose low-end ordering is not monotone. Rational maps are therefore NOT covered by the
kill criterion (only a separate structure-free test, see Test S below, is sensitive to them for degree-2 type relations).

## Controls (must pass BEFORE the carpet result is trusted)
- POSITIVE 1: gasket levels 1..7: every eigenvalue of level n+1 outside the exceptional set {2,5,6} must be a preimage of a level-n eigenvalue
  under z(5-z) to 1e-8 (this is a code-path check of the inclusion test), and the SEARCH code (blind to the answer) must recover
  R(z) = z(5-z) (coefficients within 1e-6) with matched fraction >= 0.99.
- POSITIVE 2: path graph P_{2^n} Laplacian: the blind search must recover R(z) = z(4-z).
- NEGATIVE 1: 2D grid graphs (side 2^n vs 2^(n+1)): blind search must return matched fraction < 0.1 for all d <= 6.
- NEGATIVE 2: gasket level n+1 spectrum jittered by 1e-4 relative noise: the same search must fail (fraction < 0.1).
  This also calibrates chance matches at 1e-8 tolerance.
- A search that cannot return a positive answer on the positive controls is not validated and the carpet verdict is then BLOCKED.

## KILL CRITERION (pre-registered)
Claim H is REJECTED (narrow claim only) if, after the controls pass, on the carpet level pairs (2->3) and (3->4) [and (4->5) if computed]
for operator L1 AND operator L2, the best polynomial of every degree 2..6 in the search family has a matched fraction < 0.5
(i.e. no candidate comes within a factor of 2 of the 0.9 requirement). Intermediate outcome 0.5 <= best < 0.9 => REPEAT with a wider family.
Claim H survives (LEAD) only if matched fraction >= 0.9 with the same R at two consecutive level pairs and R passes the negative-control calibration.
A single carpet level pair (1->2) is not informative (only ~16 distinct values) and is NOT used for the verdict.

## Additional pre-registered diagnostics (supporting, not part of the kill criterion)
- Test S (structure-free, no R(0)=0 assumption): histogram of pairwise sums mu_i + mu_j of the finer spectrum; a degree-2 decimation
  produces a peak with ~|spec(G_n)| pairs at a constant s = -a_1/a_2. Positive control: gasket peak at s=5.
- Test M (multiplicities): compare multiplicity patterns of spec(G_{n+1}) vs spec(G_n); gasket control: multiplicity of mu equals that of R(mu).
- Test T (structural reason): Schur complement of L_{n+1} onto the coarse vertex set (3i,3j) compared with c*L_n (gasket control: exact,
  carpet: expected to contain diagonal conductances). Residual min_c ||S - cL_n||_F / ||S||_F.
- Spectral dimension: Weyl counting slope on levels as large as computed, plus the level-to-level scaling ratio of the lowest nonzero
  eigenvalue -> walk dimension d_w = ln(ratio)/ln 3 (carpet) / ln(ratio)/ln 2 (gasket). Compared with literature values only after I
  open the source (not before; any number quoted from memory is [WEAK]).

## What this result will NOT mean
1. Not a proof that spectral decimation of any type is impossible for the carpet (analytic non-existence is NOT claimed).
2. Not a statement about maps outside the search family (R(0)!=0, rational R, level-dependent R).
3. Not a statement about the continuum carpet operator, only about the specific finite graphs and operators above at levels <= 4 (5).

---
## AMENDMENT 1 (2026-10-03, made after running ONLY the gasket code-path check, before any carpet spectrum was computed)
[VERIFIED, ctrl_gasket.py + ctrl_gasket_variants.py output] The pre-registered gasket operator D-A (corner degree 2) does NOT satisfy
the inclusion under z(5-z) (level 6->7: 188 of 284 distinct eigenvalues fail). The standard probabilistic Neumann Laplacian 4(I - D^{-1}A)
DOES: for levels 2->3 .. 5->6 all distinct eigenvalues of level n+1 map into level n under z(5-z) at 1e-8 except the single value 6.
(The Dirichlet matrix 4I-A on non-corner vertices also works, exceptional {5,6}.) So:
- Gasket positive control uses 4(I-D^{-1}A), exceptional set {6}; "{2,5,6}" in the text above is superseded.
- This is a finding in itself: whether a decimation map exists depends on the operator (D-A vs random-walk normalised). It is the reason both
  carpet operators L1 and L2 are reported. The search family is invariant under rescaling of the operator, so the factor 4 is immaterial.
- Kill criterion text unchanged: it requires failure on BOTH L1 and L2 for the carpet. No other pre-registered item was altered.

---
## AMENDMENT 2 (2026-10-03, after the controls ran, BEFORE any carpet spectrum was searched)
[VERIFIED, controls_output.txt] Controls outcome vs the pre-registered text:
- POS1 gasket (4*L2): blind search recovered a = [5, -1, ~1e-14, ...] i.e. R = z(5-z) at every degree 2..6, frac 1.000, cov 1.000 (levels 3->4, 5->6, 6->7 checked; see controls_output.txt). PASS.
- POS2 path graph: blind search recovered z(4-z). PASS.
- NEG2 jittered gasket: best frac 0.000 / 0.001. PASS.
- NEG1 2D grid: LETTER OF THE PRE-REGISTRATION NOT MET. Pre-registered "< 0.1 for all d"; observed best frac 0.26 at d=2 (R = identity, a=[1,0]) and 0.12 at d=3
  (R = z(4-z), the 1D map). Both are explained structurally: grid spectra are nested (1D eigenvalues of N-path are a subset of those of 2N-path => identity matches
  a quarter), and the 1D-mode subfamily (one quantum number 0) is exactly decimated. Neither exceeds 0.5, and positive controls give 1.00, so the control still
  separates "full decimation" from "partial/trivial structure" -- but I record that the control as written was too strict and that partial structure IS detected.
- Consequence for the carpet verdict: results are reported (i) as raw best fraction, (ii) with R(z)=z excluded, and (iii) the identity/nesting fraction
  (share of fine distinct eigenvalues that already belong to the coarse spectrum) is reported separately. Kill threshold 0.5 and the 0.9 survival threshold are unchanged.
  Any best fraction in [0.1, 0.5) is flagged "partial structure" and the responsible R is inspected, not silently counted as support or as noise.
