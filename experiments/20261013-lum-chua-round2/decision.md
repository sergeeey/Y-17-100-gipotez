# decision.md -- 20261013-lum-chua-round2 (Problem #30, round 2: planar discontinuous PWL, two focus zones, one straight line)

## Verdict
- [x] REPEAT -- counter fixed and validated; literature bound clarified; NO system with >= 4 crossing limit cycles found in
  3119 counted canonical-form systems (2045 of them with the paper's necessary condition k>=2 for >=4 satisfied). Not evidence that L*=3. No LEAD.
  Nothing here is new mathematics; the 3-cycle systems are the published HY / FPTT21 / GRS examples.

## (a) What arXiv:2508.02321 (Carmona, Fernandez-Sanchez, Novaes; HTML v1 read in full this session) proves [VERIFIED by reading]
* Object: system (1), two zones separated by x_1=0, DISCONTINUOUS in general, Filippov convention. "Limit cycle" = isolated CROSSING periodic solution
  (Sec 2.3: crossing periodic solutions / limit cycles / hyperbolic limit cycles <-> zeros / isolated zeros / simple zeros of the displacement function delta_b on int(I_b)).
  Sliding cycles (orbits using the sliding set) are not covered by this count. [INFERRED from the construction; the theorems do not discuss sliding]
* Thm 1: the Huan-Yang (2), Freire-Ponce-Torres-Tonnelier (3) and Gasull-Rondon-da Silva (4) systems have EXACTLY three limit cycles (existence from earlier papers, upper bound from the new method).
* Thm 4 (+ Prop 1): under (S_L) or (S_R), if the conic {F~_b=0} has <= N noncompact components in phi(U_b) and the polynomial system (12) (F~=G~=0) has <= k isolated real solutions, then <= N+k+1 crossing limit cycles. Tool: Khovanskii-type Thm 2 ([7, Thm 4]).
* Thm 5 (focus-focus: T^2-4D<0 in both zones): <= 8-l limit cycles, l = number of roots of R(Y1)=Res_{Y0}(F~,G~) in C minus (-inf,0]. **Cor 1: focus-focus systems have <= 7 limit cycles** (l >= 1 always, by the root Y1 = a_L^2/D_L > 0 of Remark 8). So 7 is a proved bound for focus-focus discontinuous systems, for crossing cycles. The general (not focus-focus) bound in [7] is 8 (Cor 1 "improves by one" the result of [7]).
* Thm 6: if the degree-6 coefficient of R is nonzero: <= k+2, k = number of NONPOSITIVE roots of R. Remark 9: HY, FPTT21, GRS satisfy it with k=1.
* Thm 7: if condition P holds (Delta_b* < 0, or Delta_b*=0 with b* = (a_L D_R T_L - a_R D_L T_R)/(2 D_L D_R) and a_L a_R < 0) then <= 1 limit cycle. Remark 10: when not-P the method cannot give a better estimate.
* Reduction to the canonical form (Sec 2.1, from [12, Prop 3.1]): every system with a12^L a12^R > 0 is conjugated by a homeomorphism preserving the line to x'=T x-y(+b), y'=D x-a with 7 parameters (T_L,D_L,a_L,T_R,D_R,a_R,b*). The 3-vs-7 gap is NOT closed by this paper: it proves no 4th cycle only for the three listed systems and for classes with k<=1 / P.
  Journal reference (JDE 2025 per round 1) not checked by me. [UNKNOWN]

## (b) Counter fix [VERIFIED, controls.md]
* Round-1 failure mode reproduced and explained: blanket noise filter 1e-11*(1+|y|) vs measured float64 noise 1.3e-15..2.0e-15 (relative) -> FPTT21 cycles (|G| ~ 1e-9..1e-12 because kappa = 1-3e-8) were discarded; plus the d<200 cap.
* New counter `lc2_core.count_cycles2`: float scan on a log grid d in [1e-8,1e6], noise floor measured, every sub-threshold sign change confirmed in 40-digit mpmath, dense tangency/hidden-pair detector, root classification against both fields (crossing vs sliding), degenerate (G==0 on a large share) -> not counted.
* Validation: HY = 3 in three coordinate systems with identical Floquet multipliers (canonical form conjugate to the original: multipliers equal to 4e-9); FPTT21 = 3 (round 1: 0..1); GRS = 3; 1-cycle example = 1; global stable focus = 0; exact center flagged degenerate (round-1 counter: 951 spurious sign changes). Independent exact-rational mp + fsolve + DOP853 confirmation of all 6 FPTT21/GRS cycles.
* The hidden-pair (tangency) detector and the mp-rejection branch fired 0 times in all 3119 search counts: no information about pairs born inside a grid cell beyond what the detector can see. [Accepted limitation]
* Round-1 correction: "Lienard form is a strict subfamily lacking the HY mechanism" is only true at b=0. With the x'-jump b the Lienard form IS the canonical form of the whole focus-focus class (HY maps into it with b*=9/10). Round-1's Lienard+beta search was therefore already inside the full class (only its sampling was small); the HY mechanism is inside it.

## (c) Structured search [VERIFIED counts; coverage small]
Canonical 7-parameter family (scaling D_L=1 used in sampling); the paper's per-system quantities k and Delta_b computed cheaply for every sample.
| Stage | What | N counted | Result |
|---|---|---|---|
| 1 (seed 2) | 60000 random draws screened: k-hist {0:37902, 1:19764, 2:2281, 3:51, 4:2}; not-P share 97%. Counted 1000 with k>=2 and Delta>0, 400 with k<=1 | 1400 | k=2: counts {0:830, 1:153, 2:2}; k=3: {0:14, 1:1}; k<=1: max 2 (9 systems at k=1). **max = 2, no 3, no 4** |
| 2 (seed 3) | 36 random directions from each of HY, FPTT21, GRS (p0*(1+t d), t in [1e-4,0.5], both signs) | 675 | HY/GRS neighbourhoods: 3 cycles in 189/228 and 179/222 counted steps, always with k=1 (so <=3 is PROVEN there by Thm 6); only 1 of 13409 line points had k=2 (GRS, count 0); FPTT21 window (~1e-8 wide) not re-found by log-spaced t>=1e-4 (max 2). max = 3 (the published systems' own neighbourhoods) |
| 3 (seed 4) | random walk INSIDE {k>=3, Delta>0} (52411 draws to find 40 seeds, pool 3000, k hist {3:2998, 4:2}); 637 counted; then 407 count-guided accept-if-not-worse evaluations | 1044 | counts {0: 591, 1: 453}; **max 1** |
Total 3119 counted, 2045 with k>=2; Thm-6 violations 0; sign(F)=sign(mult-1) in 311/311 roots (stage 1).
Reading: the paper's necessary condition for >=4 (k>=2) is NOT sufficient, and in the sampled k>=2 region cycles are rarer and fewer (max 2) than in the k=1 region where HY/GRS live (3); the bound k+2 is far from attained for k>=2. [VERIFIED as a statement about these samples, not about the whole space]
Kill criterion (>=2000 counted, >=500 with k>=2, no >=4) is met -> REPEAT.

## Findings that are real but small
1. [VERIFIED] The counter is now reliable on the three published 3-cycle systems in all coordinate forms, including the near-Hopf-at-infinity FPTT21 mechanism that round 1 could not see.
2. [VERIFIED] Per-system theory cross-check works: the paper's R(Y1) criterion gives k=1 for HY/FPTT21/GRS (exact sympy) and is never contradicted by 3119 counted systems.
3. [VERIFIED + theorem] For any system with k<=1 and deg R=6, <=3 crossing cycles is a theorem (Thm 6), so searches near HY/GRS in the k=1 region cannot produce a 4th; the only theoretically open region for a 4th cycle is k>=2 (about 4% of random canonical draws), and there random and k-conditioned search found max 2 (k=2) and max 1 (k>=3).
4. [VERIFIED] The x'-jump b is essential: b=0 gives <=1 (Carmona et al., no sliding set); 2-cycle systems are common enough (9/400 random k<=1 draws, 2/1000 at k=2).

## Skeptic Concerns (self-listed; no PROMOTE so no formal Step 8a)
* Coverage: 3119 systems of a 5-effective-dimensional space with huge dynamic range; random sampling cannot find sets of relative measure ~1e-8 (FPTT21 window). Absence of 4 says nothing about L*. [Accepted limitation]
* Search counts used n=2500, d<=1e4 (fast mode); cycles at larger amplitude (kappa ~ 1 mechanism as in FPTT21) are visible only if their roots are <=1e4. kappa is recorded per system but not used as a target. [Accepted limitation]
* The k-pruning rests on the paper's Thm 6 (not re-proved here) and on my transcription of m_i,n_i; checked by (i) exact HY resultant structure incl. the factor (200Y1-117), (ii) sympy identity G~=<grad F,X_L>, (iii) sign(F)=sign(mult-1) on 311 roots, (iv) 0 contradictions in 3119 systems. m_i were not re-derived from the half-map integral characterisation. [Accepted limitation]
* Sliding cycles, node/saddle zones and a12=0 degenerate cases are outside the counter, as in the paper's focus-focus bound. [Accepted limitation]
* count_cycles2 grid + bisection can lose two roots closer than the grid spacing unless the tangency detector triggers; the detector had no positive control (never exercised on a true hidden pair). [Accepted limitation; a synthetic hidden-pair control is the next hardening step]
* No novelty search was run (nothing claimed new).

## Overlap with the parallel session
experiments/20261003-c-ybe-001 and experiments/20261004-c3-obstruction-cas (Yang-Baxter / CAS) and graph nodes H-CYBE-*, SUB-QYBE-DIM3: only listed by directory (graph.yaml not opened); topic unrelated to planar PWL limit cycles, no overlap or contradiction found at topic level. [UNKNOWN beyond topic level]

## If REPEAT: what would change the next attempt
* Change the object, not the volume: (i) a synthetic hidden-pair control for the detector; (ii) the kappa->1 stratum (Hopf at infinity) with extra interior cycles (the FPTT21 mechanism plus an interior pair); (iii) track the boundary R(0)=0 of the k=1 -> k=2 transition adjacent to HY/GRS by continuation (the only place where the theorem allows a 4th next to a 3-cycle system; I only sampled lines); (iv) interval-arithmetic enclosure of any candidate.
* A count >= 4 would first need: exact rational parameters, stability under grid refinement, mp + fsolve + DOP853 confirmation (machinery in verify_fptt.py / verify_r1.py), crossing check (classify_root), and a literature check (round 1 found no published 4-cycle straight-line example; Braga-Mello 4-7 cycles are for non-straight lines).

## Pearl Registry candidates
| Insight | Falsifiable prediction | next_check |
|---|---|---|
| In the canonical focus-focus family the paper's bound k+2 is far from sharp for k>=2: counts anticorrelate with k (k=1: up to 3; k=2: max 2; k>=3: max 1 in 1044 systems) | a larger k>=2-conditioned search (>=10000 counted, incl. boundary tracking of R(0)=0 next to HY) still shows max <=2 for k>=2 | next Problem #30 round |
| A guessed tolerance beat the physics: a 1e-11 noise filter was ~5000x the measured float noise and removed a whole mechanism | any other fixed tolerance in the lab's counters (NOISE_TOL / tol=) is >=100x the measured float noise on a published control | next audit of lab numerics |

## Files (all in this folder)
claim.md, controls.md, decision.md, lc2_core.py (counter), lc2_theory.py (m_i, n_i, F~, G~, R, k, Delta), controls_def.py, validate_counter.py/.json/.log, check_theory.py/.json, search_stage1.py + search_stage1_seed2.json/.log (seed1 = 12-system smoke test), search_stage2.py + search_stage2_seed3.json/.log, search_stage3.py + search_stage3_seed4.json/.log, verify_fptt.py/.json, analyze_stage1.py, pwl_r1.py + verify_r1.py (round-1 code copied unchanged).
