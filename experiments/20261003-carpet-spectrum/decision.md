# decision.md — 20261003-carpet-spectrum

Date: 2026-10-03. Tier: FL Standard. L0: DESCRIPTIVE (spectra of finite graphs). Verdict: **REJECT of the narrow claim H** (no polynomial decimation map, degree <= 6, in the pre-registered family, on the tested carpet graphs). Nothing here says anything about analytic non-existence of spectral decimation.

## Provenance of the numbers (resume round)
Earlier attempts were interrupted (session limit, then a power-off). This round treated all earlier output as UNVERIFIED and used `rerun/` (a second full run of the same code) as the basis:
- `rerun/` outputs are byte-identical to the originals except timings: controls, carpet spectra levels 1..4 (both operators, with the 4-sector reduction checked against the full dense spectrum: max diff <= 4.5e-14), pair searches 2->3 and 3->4, dimension analysis, cell-graph variants. [VERIFIED, diff of the .txt files]
- Level-5 spectra (`carpet_spectra_L{1,2}_n5.npz`, 41584 vertices) were NOT recomputed (a recompute is ~11 min/operator at 10k-dim dense sectors, over the 10-minute single-job cap). Instead they were verified independently: trace(L) and trace(L^2) equal the sums of eigenvalues and squares exactly (L1: 158064 / 765512; L2: 41584 / 52579.5556), ARPACK shift-invert lowest 12 and top 6 eigenvalues match the stored ones to <= 3e-13. `rerun/check_n5_out.txt`. [VERIFIED]
- Carpet graph definition cross-check: Euler characteristic V - E + F = 1 - (8^n - 1)/7 holds for n = 1..5 (e.g. n=5: V=41584, E=79032, F=32768, chi=-4680). `rerun/euler_check.py`. [VERIFIED]
- 4->5 search re-run this round: `rerun/analysis_4_rerun.txt`. Relaxed (R(0)!=0) search re-run: `rerun/relaxed_rerun2.txt`.

## Objects (as pre-registered in claim.md)
Carpet vertex graph G^C_n = lattice points of the retained closed cells, edges = cell sides (V = 16, 96, 688, 5280, 41584). Operators L1 = D-A and L2 = I - D^-1 A (symmetrised). Gasket control operator: 4(I - D^-1 A), see claim.md amendments 1-2.

## Controls (positive controls run through the same code path)
- POS1 gasket levels 3->4, 5->6, 6->7: blind search recovers R(z)=z(5-z), matched fraction 1.000 (93/95 at 5->6, 189/191 at 6->7; the single unmatched value is the exceptional eigenvalue 6), coverage 1.000, at every degree 2..6 (extra coefficients ~1e-14). PASS. [VERIFIED, rerun/controls_rerun.txt]
- POS2 path graph 32->64, 128->256, 256->512: recovers z(4-z), fraction 1.000. PASS.
- POS-B (relaxed family) gasket with shifted R(0)=1 and with decreasing R: recovered at fraction 0.990. PASS (`rerun/relaxed_rerun2.txt`).
- NEG2 jittered gasket (1e-4 relative noise): best fraction 0.000 (5->6) / 0.001 (6->7). PASS. NEG-B jittered gasket in relaxed family: 0.000. PASS.
- NEG1 2D grid: pre-registered threshold (< 0.1) NOT met at the letter: best 0.26 (R=identity, nested spectra) and 0.12 (R=z(4-z), the 1D-mode subfamily). Recorded in Amendment 2 of claim.md; both are structural, both < 0.5, and the positive controls give 1.00, so the control still separates full decimation from partial structure. The carpet result below is far from this regime (0.000), so this deviation does not affect the verdict.

## Result on the carpet (kill criterion evaluated)
Kill criterion (pre-registered): REJECT if after the controls pass, for pairs 2->3, 3->4 (and 4->5) and BOTH operators, the best polynomial of every degree 2..6 matches < 50% of the finer distinct eigenvalues.

| pair | operator | distinct fine/coarse | best matched fraction, d=2..6 | identity (nesting) fraction |
|---|---|---|---|---|
| 2->3 | L1 | 510/67 | 0.000 (all d) | 0.002 |
| 3->4 | L1 | 3948/510 | 0.000 | 0.000 |
| 4->5 | L1 | 31092/3948 | 0.000 | 0.000 |
| 2->3 | L2 | 509/69 | 0.000 | 0.008 |
| 3->4 | L2 | 3933/509 | 0.000 | 0.001 |
| 4->5 | L2 | 31121/3933 | 0.000 | 0.000 |

[VERIFIED] best fraction is 0.000 everywhere (not merely < 0.5): not a single fine eigenvalue is mapped onto a coarse eigenvalue by any candidate within 1e-8. Claim H is REJECTED. The chance level at tolerance 1e-8 is also ~0 (jittered-gasket negative control), so 0.000 is a clean null, not a noise-floor artefact.

Robustness (post-hoc, declared non-pre-registered, same verdict):
- Wider family B: free constant term R(0)!=0, non-monotone assignment, nodes/targets from both ends of the coarse spectrum, d <= 3, pairs 2->3 and 3->4, L1 and L2: 0 candidates, fraction 0.000 (positive controls in the same family: 0.990).
- Cell-adjacency graphs (vertices = retained cells, 4-neighbour and 8-neighbour variants, L1 and L2), pairs 2->3, 3->4, d=2..6: fraction 0.000 in all 8 cases (`cellgraph_out.txt`). This is the graph type used by arXiv:1902.03408 [WEAK: inferred from the sentence about "eight cells in MC_m", not from a definition I checked].
- Pair-sum (Test S): the only prominent peaks are at sum = 2.0 for L2 (254 of 509 distinct values at 2->3, 1966 of 3933 at 3->4). That is the bipartite symmetry lambda <-> 2-lambda of a lattice subgraph, not a degree-2 decimation (the gasket control has its peak at 5 with 47 of 48 coarse values; the carpet graph is bipartite, the gasket is not). [INFERRED from the sums and the lattice structure; bipartiteness not separately tested numerically]
- Structural reason (Test T): the Schur complement of the fine operator onto the coarse vertex set (3i,3j) is exactly proportional to the coarse operator for the gasket (residual 1e-16, coefficients stable in nu), but for the carpet the residual is 0.12 (span{A,D,I}) and 0.046 (adding in-cell diagonal edges) at nu=0, and ~0.3 / 0.12 at nu=0.05, i.e. the reduced operator is not a multiple of the coarse graph Laplacian. A gasket-style exact closure under restriction does not hold on carpet graphs; consistent with the numerics. [VERIFIED numerically, analysis_more_rerun.txt; scope: these graphs, nu in {0, 0.05, 0.15}, not a proof.]

## Spectral and walk dimension
- Gasket control: ratio of lowest nonzero eigenvalues at consecutive levels -> 4.9998 at 6->7, i.e. d_w = ln 5/ln 2 = 2.3219, d_s = 2 ln3/ln5 = 1.365 [exact values, DOCS/known]; Weyl counting slope at level 7 gave 1.344 (-1.5%), level 6 gave 1.325, level 5 gave 1.972 (window-sensitive: the Weyl estimate is a weak tool, quote with this spread). [VERIFIED]
- Carpet: ratio of the lowest nonzero eigenvalue between consecutive levels (k=1) 4->5: L1 9.948, L2 10.032; L2 3->4: 10.036. This gives d_w = ln(r)/ln 3 = 2.091 (L1), 2.099 (L2) and d_s = 2 ln 8/ln r = 1.810 / 1.804. [VERIFIED numerically]
- Literature value: Barlow-Bass (1990) prove existence of rho > 1 with (1/4) rho^n <= R_n <= 4 rho^n (ADS abstract, opened); the numerical value rho ~ 1.251487 is quoted ("Computations give") in a talk slide deck on resistance scaling (Gallaudet IDA PDF, a secondary source, opened via search excerpt only) [WEAK: secondary]. With d_w = ln(8 rho)/ln 3 [INFERRED standard relation, formula not re-derived here]: 8 rho = 10.0119, d_w = 2.0970, d_s = 1.8052. My L2 ratio is within +0.2% of 8 rho, L1 within -0.6%, and both move toward it with level. That d_w > 2 is stated in the primary BBKT paper (Barlow-Bass-Kumagai-Teplyaev, arXiv:0812.1802: "d_w ... satisfies d_w > 2") [DOCS, opened]; that paper contains no numeric value of d_w (checked by regex on the full text).
- Carpet Weyl-window slope: 1.87 (L1), 1.856 (L2) at level 5 vs 1.805 from the ratio route: +3.6% off. I treat the Weyl window estimate as unreliable here (same window gave a 1.972 outlier on the gasket at level 5) and do not use it as a dimension claim.

## Literature statement actually verified
arXiv:1902.03408 (Goodman-Siu-Strichartz, "Geometry and Laplacian on discrete magic carpets"), full text opened: after comparing eigenfunctions of consecutive levels by an averaging procedure it says "We do not see evidence of the spectral decimation property as established on the Sierpinski gasket." That is an experimental observation for MAGIC carpets (torus-type identified cell graphs), not a theorem and not about the plain vertex graph. My result is an independent numerical statement for a different graph (carpet vertex graph) and for cell graphs, with an exact-inclusion test rather than an approximate-eigenfunction test. The audit-file claim "survey states no evidence" should be quoted with those qualifiers.

## Kill Analysis (REJECT of the narrow claim H)
What died: "there is a real polynomial R, deg <= 6, R(0)=0 (and in the relaxed family R(0) free, d <= 3), valid for all level pairs, with 90% inclusion R(spec G_{n+1}) subset spec G_n at 1e-8" for the carpet vertex graphs (L1, L2) and cell graphs. Why it died: best matched fraction is 0.000 on 6 of 6 pre-registered pairs, not only below the 0.5 kill line. Why we believe the test could have said yes: the same code returns 1.000 on the gasket (3 level pairs) and path (3 pairs) and 0.990 in the relaxed family, and returns ~0 on noise. What survives: nothing of the narrow claim. What does NOT follow: no statement about rational maps, level-dependent maps, maps of degree > 6, maps outside the search families, other carpet graph models or boundary conditions, or about the continuum carpet. Interesting residue (not a lead): inclusion fails because carpet spectra are not "nested through a function" at all (nesting fraction ~0), while multiplicity per distinct eigenvalue stays small (max 8..128, vs 366 for gasket level 6): consistent with the absence of gasket-type localized high-multiplicity eigenfunctions, but this was not tested further.

## Surgery / forbidden claims
Forbidden after this round: "the carpet has spectral decimation" (any degree <= 6 polynomial form), "the Weyl exponent was measured as the literature value" (window unreliable), "survey proves no decimation" (it is an observation on magic carpets).

## Next round (only if the owner wants it)
(1) a structure-free rational-map test (R = P/Q, deg <= 3) on level 3->4; (2) Dirichlet boundary / carpet with the outer square removed; (3) if a continuum-relevant statement is the goal, a Dirichlet-form (resistance) renormalisation check instead of a spectrum map. No big-run investment is justified by this result.

## Files
claim.md (pre-registration + 2 amendments), rerun/ (verified re-run, throttled), rerun/check_n5_out.txt, rerun/euler_check.py, rerun/analysis_4_rerun.txt, rerun/relaxed_rerun2.txt, rerun/controls_rerun.txt, rerun/analysis_*_rerun.txt, rerun/cellgraph_out.txt. Originals in the folder root are kept (not deleted).
