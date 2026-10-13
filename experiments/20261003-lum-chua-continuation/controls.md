# controls.md -- 20261003-lum-chua-continuation (round 2, Problem #30)

All numbers below were RE-RUN in this session (serial, via scripts/lowprio.py) unless marked otherwise.
Outputs of earlier attempts that used multiprocessing.Pool (continuation2.json, search2.json, controls.json,
search_interrupted.log) are treated as UNVERIFIED context only; `*_precision_bug.*` files are known-bad.

## C1 tool validity (closed-form half-return vs scipy DOP853, rtol 1e-12)  -- PASS
`validate_fast.py` -> `validate_fast.json`: 10 parameter sets (HY R/L zone, round-1 Lienard R/L zones, 6 random
foci with general b), 25 start points each. worst relative error in y1 = 8.04e-11 (kill threshold 1e-6),
worst time error 2.9e-10; 0 NaN-mismatches; speedup 118x (0.044 s vs 5.23 s). [VERIFIED]
Weak spot noted: rand4 had only 2/25 mutually valid points (most starts never return) so that set is
thin evidence; HY_L 13/25.

## C2 positive control, DISCONTINUOUS class (Huan-Yang / Llibre-Ponce system)  -- PASS
`c2_hy_control.py` -> `c2_hy_control.json`.  System: line x=1, A+=[[19/500,-1/10],[1/10,19/500]], A-=[[1,-5],[377/1000,-13/10]],
equilibrium at origin (virtual in R, real stable focus in L). The fast counter returns EXACTLY 3 crossing cycles
for (n=3000, dmax=200), (8000, 200), (8000, 2000).  Cycle points on the switching line vs the 30-digit values of
Llibre-Ponce (UAB preprint, read in full in this round):
  Y1 = 1.681194510518948  (published 1.68119451051893997)   |diff| 8.2e-15
  Y2 = 0.9657998558466(7) (published 0.96579985584668226)   |diff| 1e-14..1e-15 (grid-dependent)
  Y3 = 0.6188541651825255 (published 0.61885416518252501)   |diff| 4.4e-16
(kill threshold 1e-8). Residuals G(y0) <= 6e-16. dG/dy0 = +1.18, -0.104, +0.118 (alternating stability).
This is the first time this lab's code reproduces a published multi-cycle discontinuous example. [VERIFIED]

## C3 negative controls  -- PASS
`c3_controls_serial.py` -> `c3_controls_serial.json`:
 (i) T_L*T_R>0, 100 random Lienard-form draws: histogram [100] -> 0 cycles in all (Green's theorem).
 (ii) continuous class a_L=a_R, T_L*T_R<0, 200 random draws: histogram [97,103] -> never more than 1 cycle
      (Freire-Ponce-Rodrigo-Torres 1998; no counterexample to the theorem, 0 ambiguous grid gaps).
Round-1 positive control (TL=-2,DL=5,aL=aR=0.5,TR=0.5,DR=1): 1 cycle, y1=2.8877 (reconfirmed in controls.log header
of the earlier run and the continuation sweeps; base point of continuation3).

## Independent verification of the only >=2 events found outside the HY neighbourhood
`verify2.py` (method A: scipy.linalg.expm + fsolve on (tR,tL,y0); method B: DOP853 full piecewise simulation
rtol 1e-13, event detection) on two 2-cycle systems of the Lienard+beta family, (aL,beta)=(-2.625,3.0) and (-2.25,2.5):
all four cycles close to <=5e-13, are transversal at both crossings and satisfy the first-return property.
[VERIFIED, 2 independent methods]. (Two cycles is not a record; 3 is known.)
