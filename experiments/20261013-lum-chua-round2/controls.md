# controls.md -- 20261013-lum-chua-round2 (all numbers from validate_counter.json / .log, check_theory.json, verify_fptt.json, produced this session)

Evidence: [VERIFIED] = produced by a script in this folder in this session. VERIFIED-SYNTHETIC does not apply: all controls are PUBLISHED systems
(arXiv:2508.02321 eqs. (2),(3),(4),(15),(17),(18), rational data copied, opened by me) or analytic degenerate cases.

## Float64 noise calibration (the thing round 1 guessed)
max |G_float - G_mp40| / (1+|y|) over 38/60/32 starts (y from 1e-4 to 1e5 from the R fold): HY 2.0e-15, FPTT21 1.3e-15, GRS 1.7e-15 [VERIFIED].
Round-1 NOISE_TOL was 1e-11*(1+|y|) (about 5000x above the measured noise). Used here: 2.0e-14*(1+|y|); anything below is re-checked in mpmath.

## Positive controls (all must be hit) -- new counter count_cycles2, n=8000, d in [1e-8,1e6]
| System | Expected | New counter | Round-1 counter (d<200, noise filter) |
|---|---|---|---|
| HY, shifted original coordinates (round-1 hy_zones) | 3 | 3 (y0 = -0.48606, -0.08891, 0.16383; multipliers 1.11847, 0.89617, 2.18397) | 3 |
| HY, paper eq (2) as printed (line x=0) | 3 | 3 (same numbers) | 3 |
| HY, Lienard canonical form (15), b*=9/10 | 3 | 3 (y0 = -3.43031, -1.44457, -0.18087; multipliers 1.11847, 0.89617, 2.18397) -> conjugate to the original: same Floquet multipliers to 4e-9 | 3 |
| FPTT21 (Freire-Ponce-Torres-Tonnelier), eq (3) | 3 | 3 (y0 = -273.615, -201.164, -132.952; multiplier-1 = -3.7e-9, +3.4e-9, -1.6e-8; kappa = 0.99999997) | 1 sign change inside d<200; skeptic of round 1 saw 0 + 3 "noise_suspect" |
| FPTT21 canonical (17) | 3 | 3 | 1 |
| GRS (Gasull-Rondon-da Silva), eq (4) | 3 | 3 | 3 |
| GRS canonical (18) | 3 | 3 | 3 |
| round-1 continuous Lienard 1-cycle (T_L=-2,D_L=5,T_R=.5,D_R=1,a=.5,b=0) | 1 | 1 | 1 |

## Negative / degeneracy controls
| System | Expected | New counter |
|---|---|---|
| global stable focus (same matrix both sides, T=-0.4, D=1.5, a=0.5, b=0) | 0 | 0 [VERIFIED] |
| T_L=-0.5,D_L=1,a_L=.7,T_R=-.3,D_R=2,a_R=.4,b=0 (both stable, continuous) | 0 | 0 |
| exact center both sides (T=0,b=0,a_L=a_R): G identically 0 | flagged non-isolated, NOT a cycle count | count=None, degenerate=True, flat_share=1.0; round-1 counter returned 951 sign changes + 1584 "noise_suspect" on the same system [VERIFIED] |
| EXTRA (not a control): both traces negative WITH x'-jump b=0.3 (T_L=-.5,D_L=1,a_L=.7,T_R=-.3,D_R=2,a_R=-.4) | n/a | 1 crossing cycle, multiplier 0.40: a real discontinuity-driven stable cycle with two dissipative foci. My first draft used it as the "stable focus" negative control and it correctly returned 1, which exposed that the control was mis-specified (virtual equilibrium on one side). Replaced by the linear global-focus control above. |

## Independent second computation of the newly detected FPTT21 / GRS cycles (verify_fptt.py; exact rational parameters)
For all 3+3 roots: (1) mpmath 40-digit exact-rational G has opposite signs at y0(1-1e-6), y0(1+1e-6) (FPTT21: +-1e-12 on the two sides, same order as 2e-14*|y|=5e-12 float tolerance, so the float bracket was near the noise floor and the mp flip is the real evidence);
(2) round-1 verify.py: expm + fsolve Newton in (tR,tL,y0), residual <= 7e-14, same y0 within 5e-4 abs (float-rounded parameters; 1e-6 relative); (3) DOP853 piecewise simulation closure <= 1.8e-12; (4) all four x'-components at the two crossing points have the crossing signs (R,L at y0 > 0; R,L at y1 < 0) -> crossing, not sliding [VERIFIED].

## Theory-side controls (check_theory.py, exact sympy rationals)
* HY canonical: R(Y1)=Res_{Y0}(F~,G~) has degree 6, (200 Y1 - 117) divides it, exactly ONE nonpositive real root (-5.11022058908); Delta_b = 0.0280 > 0. FPTT21: one nonpositive root (-53151.7999184), GRS: one (-8.73536644012). k=1 for all three, as the paper states [VERIFIED].
* My transcription of m_i,n_i (eqs. (9), Remark 4) is self-consistent: sympy identity G~ = <grad F, X_L> (with X_L=-(y1 W_L(y0), y0 W_L(y1))) and F~ = F hold exactly for the three systems; numeric and exact k agree.
* Geometry check: in 311 of 311 roots found in the stage-1 draws, sign(F~(y0,y1)) = sign(multiplier-1) (paper: sign(delta')=sign(F)) [VERIFIED].
* Consistency: count <= k+2 on every counted system with deg R = 6 (3119 systems), 0 violations [VERIFIED].
