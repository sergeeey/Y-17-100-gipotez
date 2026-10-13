# claim.md -- 20261013-lum-chua-round2 (Problem #30, round 2 of the sequential run; written BEFORE the main search)

Class: planar discontinuous piecewise-linear (Filippov) systems, two zones, ONE straight switching line x=0,
both zones linear FOCI. Object: number of CROSSING limit cycles (isolated crossing periodic orbits).
L0 / EstimandOps: N/A (existence/counting question about a deterministic ODE class, not a population estimand).
Stage: Standard-Ladder, idea scouting. Not AI-novelty-claimed: any ">=4" would first be a LEAD needing double confirmation.

## Zero-Signal Gate
| Field | Value |
|---|---|
| Entity | the 7-parameter Lienard canonical family (T_L,D_L,a_L,T_R,D_R,a_R,b) of focus-focus systems with a12^L a12^R > 0 (arXiv:2508.02321 sec.2.1), plus the original 12-parameter general form |
| Predicate | number of crossing limit cycles >= 4 for some member |
| Measurable | sign changes + tangencies of G(y0)=P_L(P_R(y0))-y0 (closed-form half-returns), every float64 sign change below the calibrated trust threshold re-checked in mpmath (40 digits); exact rational parameters; independent second computation |

## Round-1 facts used (read from decision.md / skeptic_verdict.md of 20261003-lum-chua-continuation, folder read-only)
1. [VERIFIED by round 1] Huan-Yang (HY) control: 3 crossing cycles reproduced to ~1e-14 vs Llibre-Ponce.
2. [round-1 skeptic, VERIFIED there] the round-1 counter returned 0 (3 "noise_suspect") on the published FPTT21 3-cycle system and
   was capped at d<200 in search; NOISE_TOL = 1e-11*(1+|y|) was set blindly, ~1e4x above float64 rounding noise.
3. Round-1 "Lienard form is a strict subfamily" is only true for b=0; with the x'-jump b the Lienard form IS the general canonical
   form (Carmona et al. 2508.02321 sec.2.1, citing [12] Prop.3.1). To be checked here by mapping HY into canonical form and
   comparing Floquet multipliers of the 3 cycles in both coordinate systems.

## Tasks and falsifiable claims, with KILL CRITERIA fixed now
- (a) Literature: state exactly what arXiv:2508.02321 proves (record theorem numbers).  [done by reading the HTML full text]
- (b) Counter fix. Claim C1: a rebuilt counter (a) calibrates float64 noise by comparison with mpmath, (b) re-checks every float
  sign change and every near-tangency in mpmath, (c) extends the amplitude range to d<=1e6 together with the analytic large-amplitude
  multiplier kappa=exp(pi(tauR/wR+tauL/wL)), (d) checks transversality of each root against BOTH fields (sliding set excluded).
  POSITIVE CONTROLS (must be hit): HY = exactly 3 (original AND canonical coordinates, same Floquet multipliers), FPTT21 = exactly 3,
  GRS = exactly 3, the round-1 continuous 1-cycle example = exactly 1. NEGATIVE CONTROLS: global stable focus (T_L,T_R<0) = 0;
  100 random same-sign-trace draws = 0; the exact-center system (T=0 both, b=0, G identically 0) must be flagged "non-isolated/degenerate",
  not counted as isolated cycles.
  KILL: any positive control missed or any negative control non-zero => the counter is NOT validated; no search result is reported.
- C2 (consistency with the paper's theory). By Thm 6 of 2508.02321, if the degree-6 coefficient of R(Y1)=Res_{Y0}(F~,G~) is nonzero
  the number of crossing limit cycles is <= k+2, k = # roots of R with Y1<=0. The exact resultant for HY must have one negative root (paper: Descartes).
  My numeric implementation of m_i,n_i (eqs. 9,13) must reproduce, for HY, R = -C3 (200Y1-117)(quintic) and k=1.
  KILL: formula transcription not reproducing the paper's HY resultant (=> do not use k for pruning); or any sampled system with
  counter value > k+2 (=> counter bug or paper-hypothesis violation; investigate before any further claim).
- (c) Structured search. Necessary condition from the paper: >=4 crossing cycles need (generic case) k>=2 negative roots of R and
  Delta_b>0 (not-P). Sampling the canonical family restricted to {k>=2}, plus perturbations of HY/FPTT21/GRS canonical data,
  plus the best-k boundary. Main claim C3: some focus-focus canonical member has >=4 crossing cycles.
  PASS (to LEAD): exact rational parameters; count robust to grid refinement; each cycle re-confirmed by an independent method
  (expm+fsolve Newton in (tR,tL,y0) and DOP853 full piecewise simulation); transversality at all crossings.
  KILL / verdict REPEAT: no count >= 4 after the bounded budget (>=2000 counted canonical systems incl. >=500 with k>=2); never "L*=3".

## What this does NOT mean
1. Not finding >=4 is not a proof that 3 is the sup for focus-focus; the paper's proven bound is 7 and nobody has closed 3 vs 7 (as far as I verified).
2. A numerical sampling cannot see cycles that are born in a pair inside one grid cell unless the tangency detector catches it.
3. Reproducing the 3-cycle examples reproduces published work; nothing here is new mathematics unless a >=4 system survives double confirmation.
4. Sliding / escaping cycles and node/saddle zones are outside this counter (the paper's focus-focus bound also counts crossing cycles only).

## Constraints (hardware)
One heavy process at a time, all heavy jobs via scripts/lowprio.py, <=10 min per job, 45 s sleep between jobs.
