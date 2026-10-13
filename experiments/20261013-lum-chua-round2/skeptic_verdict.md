# skeptic_verdict.md -- 20261013-lum-chua-round2 (independent falsification pass, 2026-10-13)

Method: new code written from scratch (no import of lc2_core's counter for the verdict numbers): a 40-50 digit mpmath implementation of the
half-return maps on EXACT rational data (scratchpad hp.py), DOP853 closure (rtol 1e-13), the paper's m_i/n_i parsed AUTOMATICALLY from the
arXiv:2508.02321 LaTeX source (not hand-transcribed), exact rational Sylvester resultants + Sturm counts, and reruns of the audit target's own
counter only where the claim is about that counter. All heavy jobs ran through scripts/lowprio.py, one at a time. Scripts live in the session
scratchpad (C:/Users/serge/AppData/Local/Temp/claude/.../scratchpad), not in this folder.

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | HY: exactly 3 crossing cycles, y0 and multipliers, canonical vs original | CONFIRMED |
| 2 | FPTT21: exactly 3 cycles, round-1 counter sees 1, no 4th beyond d=1e6 | WEAKENED (count/positions/kappa true; quoted multipliers off by up to 9%) |
| 3 | R(Y1): deg 6, factor (200Y1-117), one nonpositive root, values for HY/FPTT21/GRS, matches paper | CONFIRMED |
| 4 | exact-center control: count=None/degenerate vs 951 + 1584 | CONFIRMED |
| 5 | no >=4 in 3119 systems; max 2 at k>=2, max 1 at k>=3 | WEAKENED (headline survives; k stratification is wrong) |
| 6 | Thm-6 consistency (0 violations), 311/311 sign(F)=sign(mult-1) | CONFIRMED (with a process flaw: the k column was numerically wrong) |

## Claim 1 -- CONFIRMED
Independent mp code (dps 50, exact rationals, 3000-point log grid d in [1e-8,1e14], 1000+ grid points have no valid return = outside I_b, as in the paper's
I_L=[lambda_L,inf)) finds exactly 3 sign changes of G in each coordinate system. Polished roots / multipliers (central difference at two step sizes, 1e-12 and 1e-18, agree to 13 digits):
* HY paper eq (2): y0 = -0.4860616491266, -0.08891408094288, 0.1638262276271; multipliers 1.118470773915, 0.8961707398351, 2.183970502602.
* HY Lienard canonical (b=9/10): y0 = -3.430308245633, -1.444570404714, -0.1808688618646; the SAME 13-digit multipliers. (Their float values agreed only to 4e-9; the true
  conjugacy is exact.) DOP853 closure of all 3 canonical cycles: 6e-15..7e-13.
* G has constant sign for d up to 1e14 (kappa-1 = +0.7603 > 0 in the original coordinate sign convention), so no further cycle at large amplitude.
No discrepancy.

## Claim 2 -- WEAKENED
Confirmed independently (mp, dps 50, exact rationals from arXiv eq (3), dense log scan d in [1,3e4] with 4000 points, plus 600 points to 1e16):
* exactly 3 sign changes, y0 = -273.614899218947, -201.163862982957, -132.952306394267 (claim: -273.6149, -201.1639, -132.9523);
  no local |G| minimum without sign change anywhere; DOP853 closure 1.3e-12..2.2e-12; G(+-1 offset) changes sign.
* kappa = 0.99999997003862 (claim 0.99999997).
* round-1 counter pwl_r1.count_cycles(dmax=200, n=6000) returns exactly 1 sign change, noise_suspect 0 (rerun by me). [controls.md says "skeptic of round 1 saw 0 + 3 noise_suspect"; the default-parameter rerun here gives 1 + 0 -- minor inconsistency, same qualitative failure.]
* 4th cycle beyond d=1e6 is excluded: G(d) = (1-kappa) d + c + O(1/d) with 1-kappa=2.9961e-8 and c = -1.8208559e-5 (stable to 10 digits for d from 1e10 to 1e20),
  G(1e4)=2.8e-4, G(1e6)=0.0299, G>0 and increasing for all d>274.
WEAKENED because the quoted multipliers are float noise: true multiplier-1 = -4.078e-9 (y0=-273.6), +3.659e-9 (-201.2), -1.626e-8 (-132.95)
versus the claimed -3.7e-9, +3.4e-9, -1.6e-8 (errors 9%, 7%, 2%). The finite-difference step 1e-6|y| with a float64 noise of ~1e-14|y| gives dG noise ~1e-8, comparable to the quantity measured; the canonical-form run in validate_counter.json gives yet another set (-3.96e-9, +3.67e-9, -1.60e-8), which is the visible symptom. Signs and orders of magnitude are right; the digits are not.

## Claim 3 -- CONFIRMED
* The 15 coefficients m_0..m_5, n_1..n_9 were parsed by code from the LaTeX of arXiv:2508.02321 (conic-coef and the n_i display) and compared symbolically with lc2_theory.mn_coeffs: identical (expand(diff)==0 for all 15).
* Exact resultants (sympy resultant AND an independent Fraction-arithmetic Sylvester/interpolation pipeline, which agree): deg 6 for HY/FPTT21/GRS; Sturm count of roots in (-inf,0] = 1; nonpositive roots -5.11022058908, -53151.7999184, -8.73536644012 (all three match the claim to the stated digits); (200Y1-117) divides R for HY, and Y1=a_L^2/D_L (Remark 8) is a root in all three.
* Paper print check: R_HY / [(200Y1-117) * printed quintic] is a single constant (-1.1216e-23, negative, i.e. -C3 with C3>0 as printed); same for GRS with (31250Y1-31213) and the printed quintic (constant -1.3954e-29). The paper prints no FPTT21 resultant ("too large"), so for FPTT21 only the exact computation exists.
* The paper's printed F_b and G_b for HY equal my F~,G~ up to the constants C1=334737/1e12, C2=39164229/2e15 that the paper itself records in comments. Delta_b for HY = 0.0280 > 0 (quad-part discriminant).
Caveat (not a defect of the claim): this verifies the audit's transcription against the paper, not the paper's formulas against first principles; the first-principles test is claim 6's sign check.

## Claim 4 -- CONFIRMED
Rerun: pwl_r1.count_cycles(n=6000,dmax=200) on T=0,D_L=1,D_R=2,a=0.5,b=0 returns 951 sign changes and 1584 noise_suspect; count_cycles2 (both with n=8000,dmax=1e6,noise_rel=2e-14 and with defaults) returns count=None, degenerate=True, flat_share=1.0. Independent reason: both zones are exact centers with the reversibility (x,y,t)->(x,-y,-t), so each half-map is y -> -y and G == 0; max |G|/(1+|y|) over a 2000-point grid = 8.7e-16 (noise).
Weakness found while attacking it: the degeneracy test is a hard threshold (flat_share>0.2 at 2e-14*(1+|y|)); a genuinely weakly dissipative system is also flagged: TL=-1e-9 (otherwise the same center) returns count=None, degenerate=True; TL=-1e-6 returns 0. The searches DROP all count==None systems silently (`if r["count"] is None: continue`), and the number dropped is not recorded. The control is a single exact case; it cannot show that the threshold does not hide real near-Hopf systems.

## Claim 5 -- WEAKENED
What holds (recomputed from the three JSON files): 1400+675+1044 = 3119 counted, 3119 distinct parameter vectors; with the stored k, max count at k>=2 is 2 (2 systems), at k>=3 is 1; no count>=4. My reruns of the audit target's own count_cycles2 with n=20000, dmax=1e6: the 40 highest-count stored-k>=2 vectors (2x count 2, 38x count 1): ALL counts unchanged (0 changes), no degenerate flags. The detector was also checked independently (below).
What does not hold:
1. **The stored k is numerically wrong for 1186 of 3119 systems (38%).** `k_negative_roots` rebuilds R(Y1) by np.polyfit of 13 Sylvester determinants and np.roots with a 1e-9 imag tolerance; the parameter dynamic range (a_R, D_R, b spanning 4 decades) makes this unreliable. I recomputed deg and k exactly (parameters converted from the stored doubles to rationals, exact Sylvester via interpolation, exact Sturm counts with multiplicity; the pipeline matches sympy.resultant on 3 systems, and reproduces k=1 for HY/FPTT21/GRS). Stored-vs-exact k over the 3119: (0,0):467, (1,0):10, (1,1):597, (2,0):38, (2,1):79, (2,2):869, (3,0):1, (3,1):22, (3,2):1036. The error is always an over-count.
2. **There are NO k>=3 systems in the data at all.** The systems with stored k=3 (stage 3 and stage 1) are in fact exact k=2 (1036), k=1 (22), k=0 (1). The sentence "highest count in k>=3 samples is 1" is therefore about an empty set; the walk was inside k=2. Across the full 60000-draw seed-2 screen (regenerated by me with the same RNG; khist reproduced exactly {0:37902,1:19764,2:2281,3:51,4:2}) I computed exact k for all 2334 stored-k>=2 draws: exact k = 2 for 2072, 1 for 173, 0 for 89, **none >= 3**.
3. **The "2 systems with k=4" are not in the counted set** (stored khist only; stage 3 counted only k=3). Regenerated: both have exact k=1 and count 0 at n=20000, dmax=1e6 (hp scan also 0 sign changes).
4. With exact k, "highest count at k>=2" is 1, not 2: the two count-2 systems have exact k=1 (my mp scan confirms both are real 2-cycle systems, sign changes at the same places). The paper's necessary condition (k>=2 for >=4) was therefore tested on 1905 counted systems, ~1025 of them (stage 3) diffusions from only 40 seeds, i.e. strongly clustered; 880 independent stage-1 draws.
5. The search window is part of the answer: all counts used dmax=1e4. Of the 246 counted systems with |kappa-1|<0.05, rerun with n=8000, dmax=1e9: 2 gained a cycle (index 2637: y0=-63482.87, index 3080: y0=-15257.19; both verified in 40-digit mp: G changes sign, |G|~3e-10, 7e-11), none exceeded 2 cycles. So the stored counts are lower bounds, and the Hopf-at-infinity stratum (the very FPTT21 mechanism the audit says it fixed) was not searched at the amplitude where its cycles live.
Headline "no >=4 found" is true of the counter's output; the supporting stratification and the "k>=3" statement are not.

## Claim 6 -- CONFIRMED (process flaw)
* With exact k and exact deg (=6 for all 3119; the numeric deg was 4/5 for 11 systems and was excluded from the audit's test), count <= k+2 holds for all 3119: 0 violations. The bound is tight in two strata, so the test has teeth: exact k=0 with count 2 (13 systems), exact k=1 with count 3 (368 systems); exact k=2: max count 1.
* sign(F~(y0,y1)) = sign(multiplier-1): the 311 stage-1 roots all have +1 (verified from the JSON: 311 values, all 1.0, equal to the total root count of stage 1). Independently on the 6 HY/GRS cycles with 13-digit multipliers and the exact rational F~: F=+2.686,-0.198,+0.0839 (HY) and +4117.6,-97.34,+48.14 (GRS) vs multiplier-1 = +,-,+ : all agree.
* Counter-example hunt (my own): 150 random directions x two signs x 22 points from GRS and from HY canonical (t up to 4), exact k computed at each point, bisection to the k: 1->2 boundary R(0)=0, then counting 3 points inside k=2 (n=6000, dmax=1e5): 5 boundaries near GRS (15 points) and 4 near HY (12 points); counts 0 or 1 (0: 21 points, 1: 6 points). No violation, no 3. The row the task points at (stage 2, GRS, t=0.433, stored k=2) actually has exact k=1.
Process flaw: the audit's own k column over-counts in 38% of systems, so its "consistency" statistic was weaker than reported; with exact k the statement is true and tighter.

## Process issues (a positive control that can say yes; markings)
1. Hidden-pair (tangency) detector had no positive control (acknowledged). I built one: system 265 (count 2) continued in T_L to the cycle fold s*=0.39274219767; for delta=1e-3..1e-10 below the fold the roots are 0.0004..0.06 apart in y0; count_cycles2 with the SEARCH settings (n=2500, dmax=1e4) returns 2 at every delta, and the detector reports hidden_pairs=1 for delta<=1e-7. The detector works on a real fold; this removes that listed limitation (to ~0.1% root separation).
2. Counter positive controls are legitimate (published HY/FPTT21/GRS, 3 coordinate forms) and I reproduced all of them; the round-2 2-cycle and 1-cycle outputs were also confirmed by mp. The one positive control that matters for the claim (a system with >=4 cycles) does not exist, as stated; nothing was marked [VERIFIED] that I found false.
3. Mislabelled "k>=3" search (claim 5) and silently dropped count==None systems (claim 4) are the main design defects; neither changes the "no >=4 seen" outcome but both overstate what the search covered.
4. float64 multiplier digits for FPTT21 are quoted as if resolved (claim 2).
5. dmax=1e4 in all 3119 counts; 2/246 near-Hopf systems miss a cycle (claim 5).
6. Literature facts opened and checked against the arXiv LaTeX myself: Thm 1 (HY/FPTT21/GRS exactly three), focuscasegeneral (<= 8-l), Cor (<=7), focuscase (<= k+2 with non-vanishing degree-6 coefficient, k = number of non-positive roots counting multiplicity), canonical data for HY/FPTT21/GRS (eqs coefHY/coefGRS and the FPTT block), printed R for HY and GRS: all as in decision.md; theorem numbers 5/6/7 are consistent with a shared theorem/lemma counter (not independently checked in a PDF).

## Overall
No contradiction of the central outcome (REPEAT, no >=4 found, no new mathematics): the counter is reliable on all published controls, the resultant criterion is reproduced exactly, and independent mp scans, a 40+53 system fine-grid rerun and a boundary-hugging hunt found no 4-cycle system. But the write-up overstates the coverage of the necessary-condition region (k>=2 is really k=2, no k>=3 exists in the sample), the search window missed real cycles in the near-Hopf stratum, and the FPTT21 multiplier digits are noise. Recommended edits to decision.md: replace stored k by exact k, delete the "k>=3: max 1" statement, report counts as lower bounds with dmax=1e4, record the number of dropped count==None systems.
