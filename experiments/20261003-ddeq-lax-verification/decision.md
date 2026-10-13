# decision.md -- 20261003-ddeq-lax-verification (2026-10-03)

## Verdict: ARCHIVE (verification complete; ALREADY_KNOWN; no discrepancy found, no new lead)
Kill criterion from claim.md was NOT triggered for any paper claim (no residual survived).
The checker passed its validity gate (positive controls zero, all negative controls nonzero).

## Evidence (all [VERIFIED] by running code in this folder; logs next to the scripts)
Substrate: sympy + mpmath in ape311; scripts src/ddlax.py (checker), controls.py, verify_paper.py,
theorems.py, symmetry.py, run_sym.py; logs controls_result.json, verify_paper_log.txt,
theorems_log.txt, sym_*.log, symmetry_*.json.

### Controls (controls_result.json, "CONTROLS VALID")
- POS: Toda (116)+MLR (117): residual 0 (symbolic) / 2.5e-60 (numeric). POS: random gauge (12) of it: 0.
- NEG (all nonzero, O(1..15)): M12 w1_0->w1_1; M11 w2_1->w2_0; U22 w2_0->w2_1; U21 1->2; F2 += w1_0 w2_0.
- Weakness (honest): the Volterra control with M=[[lam,u0],[-1,0]] found NO U in my ansatz, so that
  second independent positive control was NOT obtained; Toda (117) is the textbook-literature pair
  that the paper itself only quotes from [10].
- Symmetry solver controls: Toda: base flow F recovered (nullity 1), and the known second Toda flow
  w1_t = -w1_0 w1_1 + w1_0 w1_{-1} + w1_0 (w2_0^2 - w2_1^2),
  w2_t = -w1_0 w2_0 - w1_0 w2_1 + w1_{-1} w2_0 + w1_{-1} w2_{-1} recovered and exactly verified;
  perturbed Toda (F1 += w2_0^3): higher-flow nullity 0.

### (c) Paper examples -- 31/31 PASS (verify_paper_log.txt; first run had 2 FAIL = my own reporting bug,
dict iterated by keys; fixed, not a paper discrepancy; the debug script src/debug89.py confirmed 0)
- MLR (68) for (67); MLR (71) for (72); MLR (90),(91) for (85); MLR (96),(97) and (100) for (85);
  MLR (118),(119) for (114); Toda (117); MLR (120) for (114); MLR from Remark 7 for (128).
- MT (89) from (85) to (67) (exact symbolic 0); MT (115) (114)->Toda; MT (126) (128)->(114) (exact 0).
- MT (110) from (113) to (85) with the sqrt formulas (108)-(109): BOTH sqrt branches, residual ~1e-59
  at 4 random rational points, dps=60 (numeric, not a symbolic proof); (107) solved by (108) both branches;
  Remark 6 MLR for (113) at lam=q, residual ~1e-57.
- Gauge computations recomputed from the definition (not copied): S(G)MG^-1 and DtG G^-1+GUG^-1 with G (95),
  diag(lam+al(n-1),1), and G of Sect. 3.2 reproduce the printed (96),(97),(100),(120) exactly (symbolic 0).
- Lemma 4 route: substituting (89) into (71) reproduces the printed (90),(91) exactly.

### Theorems 1-3 on instances (theorems_log.txt, 15/15 PASS)
- Thm 3: Delta^{u^j}(M) != 0 for Toda (117), (118), (90), (100), (68), (120) => all non-fake;
  Delta = 0 for two deliberately fake MLRs S(G)M0G^-1 (constant M0 gauged by nontrivial G).
- Thm 2 covariance holds for random G on (118),(100); NEG control (wrong formula with G instead of S(G)) fails as it should.
- Thm 1: condition (27), p=1 holds for (90),(118); explicit gauge (28) removes u_1 from (118); NEG: (27) fails for an entangled matrix.
  (Numeric-exact-point zero tests, dps=60, after the first symbolic attempt hung on sympy.cancel; log kept as theorems_log_attempt1_symbolic_hung.txt.)

### (d) Symmetry approach (sym_kn.log, symmetry_kn.json)
Eq (72)=(67) relabelled, alpha=3/2 const (Kaup-Newell-type lattice), ansatz: charge-preserving
(u1:+1,u2:-1) polynomials of degree<=5 in u^i_{-2..2} (1210 unknown coefficients, 5914 equations).
Nullity = 3 = {scaling (u1,-u2)} + {F (up to scaling)} + ONE genuine higher symmetry, 5-point stencil [-2,2], exactly verified by sympy expand:
  u1_tau = u1_0^3 u2_0^2 - u1_0^2 u2_{-1} - 2 u1_0 u1_1 u2_0 - u1_1^2 u2_1 + u1_2
  u2_tau = -u1_0^2 u2_0^3 + 2 u1_0 u2_0 u2_{-1} + u1_1 u2_0^2 + u1_{-1} u2_{-1}^2 - u2_{-2}
Negative control (F1 += u1_0^3 u2_0^2): nullity 2 = {F, scaling}, no higher symmetry (caveat: perturbation degree 5 would
need a degree>=7 ansatz, so this control is weaker than the Toda one).
Consistent with the paper's integrability claim for (67) (necessary condition only).

## Skeptic Concerns (self-answered, Step 8a not run as a separate agent: nothing was PROMOTEd)
- "Transcription error": paper HTML alt-text is LaTeX-derived; every printed identity reproduced, so none suspected.
- "Verification circular, my code encodes the paper's definitions": mitigated by controls and by recomputing gauges and
  Delta/Thm covariance from definitions; residual risk: Def.1 sign convention shared with the paper -> checked by
  Toda positive control with an externally known pair.
- "Numeric zero != proof" for sqrt cases: Accepted limitation (documented).

## Kill Analysis (n/a: no REJECT). Not killed: all C1-C5 within tested instances.
## What this does NOT mean: see claim.md (instances only, not proofs; no new integrable equation found; not a classification).
## Pearl: none (no unexpected testable insight beyond the paper).
## Next (optional): symmetry test of the paper's NEW equation (128)/(85) with a Laurent/rational ansatz; free-lambda MLR check for sqrt system (113).

## Re-run addendum (2026-10-03, "Try again" round) -- all [VERIFIED] by re-execution, outputs in rerun/
- controls.py: "CONTROLS VALID" reproduced (POS Toda+gauge zero; all 5 NEG nonzero). rerun/controls.out
- verify_paper.py: 31 PASS, "any FAIL: []" reproduced. rerun/verify_paper.out
- theorems.py: "DONE; FAIL: []" reproduced (17 PASS lines incl. NEG controls that are expected to fail and are marked PASS). rerun/theorems.out
- run_sym.py kn: nullity 3 reproduced, 3rd solution stencil [-2,2], exact_verified=True. rerun/sym_kn.out
- NEW independent check src/indep_check_symmetry.py (no shared code with symmetry.py/ddlax.py): the printed 5-point flow G
  commutes with F of (72) at alpha=3/2 -- both commutator components expand to exactly 0; NEG (G1 perturbed) nonzero;
  G not proportional to F (the printed label "proportional? True" in rerun/indep_sym.out means G1*F2-G2*F1 != 0, i.e. NOT proportional -- label wording bug only).
  rerun/indep_sym.out
