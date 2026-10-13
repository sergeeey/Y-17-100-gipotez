# skeptic_verdict.md -- 20261003-ddeq-lax-verification (independent falsification, 2026-10-03)

Given to the skeptic: claim.md C1-C5 + code/logs only. decision.md was not used as evidence.
Primary source: arXiv:2604.26870 **LaTeX source** (read via the arXiv tool, sections 1-3), NOT the HTML alt-text
the author transcribed from. KMX2015 = arXiv:1503.06406, MMBW2013 = arXiv:1212.5299 opened separately.
Independent code lives outside this folder (I may only write this file):
`C:/Users/serge/AppData/Local/Temp/claude/E-------------------------------------------------Y-17-100-gipotez/9e146a80-48ac-4700-aadb-0cf8d72b4b4e/scratchpad/sk/`
(dual.py, sk_lax.py, sk_thm.py, sk_thm1.py, sk_sym.py, sk_mono.py, sk_consts.py). All jobs ran through scripts/lowprio.py,
sequentially, no multiprocessing, each < 1 min, sleeps between the heavy SVD jobs.

## Method (different from the author on every axis)
- Author: sympy symbolic shift calculus + random-rational numerics (mpmath dps 60), exact coefficient extraction for symmetries.
- Skeptic: periodic lattice N=9..11 with an explicit n-dependent kappa(n), random real state, **forward-mode dual numbers over mpmath
  (dps 40)** so d/dt along the flow is exact (no sympy, no shared code, no finite-difference step). My own transcription from the LaTeX.
  Symmetries: numeric evaluation of D_F(G)-D_G(F)=0 at ~1.6x(#unknowns) random points + SVD nullspace (float64). Thm 1: plain sympy, local.

## C1 -- every printed MLR satisfies D_t M = S(U)M - MU  : CONFIRMED
(68)/(67), (71)/(72), (90)(91)=Mbce/Ubce and (96)(97), (100)=2hhm for (85), (118)(119) and (120) for (114), Toda (117): 44 checks x 3 seeds
+ 4 extra (c, alpha) constant pairs incl. c=0, alpha=c. Max positive residual 1.6e-30 (dps 40); every negative control >= 1.6
(perturbed equation, perturbed Lax entry, wrong shift, wrong radicand sign). Convention-independent control: tr of the periodic monodromy
is conserved for Toda+(117), (85)+(100), (67)+(68), (114)+(120) (|d/dt trT| <= 7.5e-37) and is NOT conserved for perturbed equations
(>= 2e3), while d trT/dx_site ~ 1e2..1e4 (the invariant is non-trivial).

## C2 -- every printed MT satisfies (20), both sqrt branches : CONFIRMED (with a scope reduction the author did not state)
MT (89)/(mtkmx) (85)->newkmx, mtpeqq (85)->(67), mtmbw MMBW->Toda, (126)=mtmtd (128)->MMBW, composed (128)->Toda: residual <= 3.6e-34.
Sqrt MT (110)=tmtkmx, branches +/-: the printed quadratic (mvv11) is solved by (108)-(109) (<= 3.8e-37) and the **first component**
of (113) satisfies (20) (<= 1.4e-34); wrong radicand sign gives O(50-150). Remark 6 MLR for (113) holds for FREE lambda and at lambda=q.
**Scope reduction:** the second component H of (113) is not printed in the paper (it is "obtained by substituting", LaTeX label tdtmv);
checking (20) for u2 is tautological (my D1b = exactly 0.000e+00; the author's two "(110) ... u2: numeric_max 0.0" lines are the same).
So 2 of the author's 31 "PASS" lines carry no information, and "(113) with MT (110) holds" is only testable for component 1.

## C3 -- printed gauge transformations map printed MLR to printed MLR : CONFIRMED
G=(guu0z) Mbce->(96),(97); diagonal G=diag(lam+kappa(n-1),1) ->(100); G of Sect.3.2 ->(120) (MMBW). Gauge recomputed from the definition
(S(G) M G^-1, D_t G G^-1 + G U G^-1 with duals): <= 7.5e-37; wrong sign / wrong shift negatives 3.4e1 / 4.8e1.

## C4 -- Thm 1-3 on instances : CONFIRMED (instances only)
- Thm 3: Delta^{u^j}(M) from the LaTeX definition (nabla(Q)_n=M_{n+1}^-1 Q_{n+1} M_{n+1}, nabla^-1(Q)_n=M_n Q_{n-1} M_n^-1, derivative by site
  seeding) is nonzero (norm 1..1e5) for Toda(117), (118), (90), (100), (68), (120), (96); zero (<= 1.7e-38) for two deliberately fake
  MLRs S(G)M0G^-1 (second G mixes u_0,u_1); perturbed-fake negative control 4e1.
- Thm 2: Delta(M~) = S(G) Delta(M) S(G)^-1 residual 3.7e-35; wrong formula (G instead of S(G)) 1.6e3-3.0e3.
- Thm 1: cond (27) true for (118) and (90); gauge (guum) with a0=(a1,a2), (0,0), (1/2,1/3) removes u_1 (checked by cancel + diff, not by
  free_symbols). Negative [[lam-q1*p0,1],[-1,p1]] violates (27) and the same gauge leaves u_1. Caution found: my first "entangled" matrix
  [[lam-q1,p0*p1],[-1,0]] actually SATISFIES (27) -- a negative control for (27) must be tested, not assumed (the author's
  [[lam,u0*u1],[1,u1]] does violate it; I verified by hand).

## C5 -- higher symmetries (Lax-independent) : CONFIRMED, bounded-ansatz evidence only
Own enumeration + numeric nullspace. Toda (116), weight-graded ansatz stencil [-2,2]: nullity 1 at shift-weight s=1,2,3 (base flow, the
known 2nd and 3rd Toda flows; the author's s=2 ansatz size 220 reproduced); F2+... perturbed (F1 += w2_0^3): nullity 0 at s=2.
(72)=(67) with constant alpha, charge-preserving deg<=5, stencil [-2,2] (1210 unknowns): nullity 3 for alpha = 3/2, 0, -2/3 (scaling, F, ONE
5-point flow; independent of alpha because [E,G]=0). Perturbations: F1 += u1_0 u1_1 u2_0 (degree 3, INSIDE the ansatz): nullity 2; F1 += u1_{-1}: 2;
F1 += u1_0^3 u2_0^2: 2. So the author's caveat ("deg-5 perturbation is a weak control") is real, but a degree-3 control discriminates cleanly.
This is a necessary condition only; it does not prove integrability.

## Literature facts (primary sources opened by me)
- KMX2015 (arXiv:1503.06406, sect. 3.1): symmetry d_x p = 2(p^2 q_10 + alpha(n) p - p_10), d_x q = 2(q_-10 - p_-10 q^2 - alpha(n-1) q) and
  Lax matrix lambda*diag(1,0)+[[f,p],[q_10,1]], f=alpha+p q_10: matches printed (67),(68). [VERIFIED]
- MMBW2013 (arXiv:1212.5299, sect. 5.1.1): (k1)_t = k1 k2, (k2)_t = k1_{s-1}/k1_s - k1_s/k1_{s+1}; Miura p=k1_s/k1_{s+1}, q=k2 to Toda
  p(q_s-q_{s+1}), p_{s-1}-p_s: matches printed (114),(115),(116). [VERIFIED]
- Toda (116) is exactly Newton's Toda with w2=p_n, w1=exp(q_n-q_{n+1}) (derived by hand), so (117) is a physically correct positive control.

## Process issues
1. The positive control used for the zero-curvature checker is the paper's own Toda pair (117); the planned independent control (Volterra,
   solver-found U) returned "none found" and was silently dropped from the validity gate (controls_valid = true). Disclosed in decision.md, not in controls_result.json.
2. No negative control exists for the MT checker (miura_residual) nor for the sqrt branch; all negative controls are MLR-only. (I added them: all pass.)
3. Two "PASS" lines (sqrt MT u2, both branches) are tautological by construction, counted in "31/31 PASS".
4. "Re-run addendum": re-executing the same scripts is reproducibility, not independent verification; only indep_check_symmetry.py is new, and it only
   re-checks the printed G. rerun/indep_sym.out prints "G1/F1 proportional? True" when the code computes NOT proportional (label bug, noted by the author).
5. theorems.py marks expected-to-fail negative controls as "PASS" (confusing counting: "17 PASS lines").
6. The paper was transcribed from the arXiv HTML alt-text (LaTeX-derived) and never diffed against the LaTeX source; my independent LaTeX transcription
   agrees on all examples (indirectly, since both pass the same identities), so no transcription error is indicated.
7. Hook "mcp-response-guard" flagged the arXiv LaTeX responses as "command_injection" -- false positive (TeX markup); no instruction in them was followed.

## Overall
No claim refuted. C1-C5 stand as stated, but only as identity checks on instances (not proofs of Thms 1-3, not discovery of Lax pairs); the sqrt
MT (113) is verified for component 1 only; the symmetry evidence is a bounded-ansatz necessary condition. Verdict: author's ARCHIVE/ALREADY_KNOWN is supported.
