# claim.md -- 20261003-lum-chua-continuation (round 2 of Problem #30)

Written BEFORE the main search was run (kill criterion fixed first). Stage: idea scouting,
Standard-Ladder. L0 / EstimandOps: N/A (existence question about a deterministic ODE class,
not a population estimand; same reasoning as round 1 claim.md).

## Zero-Signal Gate

| Field | Value |
|---|---|
| Entity | planar 2-zone piecewise-linear system, straight switching line x=0, DISCONTINUOUS (Filippov), general data (A_L,b_L,A_R,b_R), both zones linear FOCI |
| Predicate | number of CROSSING limit cycles (isolated periodic orbits that only cross x=0 transversally) |
| Measurable | number of simple sign changes of G(y0)=P_L(P_R(y0))-y0 over its whole domain, exact half-return maps P_R, P_L (closed form), roots refined to 1e-12, verified by a 2nd method |

## Natural-language statement

We count crossing limit cycles of a focus-focus discontinuous 2-zone PWL system and ask
whether any member of this class has >= 4, i.e. whether the known lower bound 3 can be raised
(known upper bound 8, Carmona-Fernandez-Sanchez-Novaes arXiv:2210.12125).

## Findings from the literature read this round (primary sources opened)

1. [VERIFIED, full text] Llibre-Ponce (UAB preprint, ddd.uab.cat LliPon2011.pdf): explicit
   Huan-Yang system with THREE crossing limit cycles. Line x=1, A+ = [[19/500,-1/10],[1/10,19/500]]
   for x>=1, A- = [[1,-5],[377/1000,-13/10]] for x<1, common equilibrium at origin
   (virtual unstable focus of A+, real stable focus of A-). Cycle data (x=1, point (1,Y)):
   Y1=1.68119451051893996990946394580, Y2=0.96579985584668225513544927484,
   Y3=0.61885416518252501376067323768, with return times t+_k, t-_k also listed.
   This is the REAL positive control for the discontinuous class (30 digits to compare against).
2. [VERIFIED] The Round-1 model (Lienard form x'=Tx-y, y'=Dx-a, a_L != a_R) is a STRICT
   SUBFAMILY: x-component of the field is continuous across x=0 there (both equal -y), so
   NO sliding region exists. The Huan-Yang example has a sliding segment {(1,y): 1/5<=y<=19/50}
   (x'-components of the two fields have opposite sign there). So Round 1 never touched the
   family in which the 3-cycle mechanism lives. This round therefore uses the GENERAL
   12-parameter data (A_L,b_L,A_R,b_R).
3. [VERIFIED, full text EJDE 2015/228 Braga-Mello] "4,5,6,7 limit cycles" (Braga-Mello IJBC 2014)
   and "arbitrary n" are for NON-straight (polygonal / curved) separation line; for a straight
   line with one equilibrium off L the same paper states 3 is the numerical max. Abstract of
   the IJBC 2014 paper alone (WorldSci page) does not say "polygonal" -- the polygonal statement
   is taken from the EJDE 2015 introduction [DOCS, secondary]. Full text of IJBC 2014 NOT opened.
4. Freire-Ponce-Torres 2014 (Publ. Mat. 58 S1) full text is paywalled/not obtained; only the
   abstract opened [DOCS]: canonical form with five parameters; regions with 0,1,2,3 crossing
   limit cycles found. Not used as a numeric source.

## Falsifiable claims and KILL CRITERIA (fixed now)

- C1 (tool validity). Closed-form half-return agrees with scipy solve_ivp (rtol 1e-11) to
  < 1e-7 abs on >= 8 parameter sets incl. Huan-Yang and Round-1 control, and is >= 20x faster.
  KILL: any disagreement > 1e-6 not explained by an identified domain/branch artifact -> fix or
  abandon the fast path.
- C2 (positive control, discontinuous). The fast counter returns EXACTLY 3 cycles for the
  Huan-Yang system and their Y_k agree with the published Y_k to <= 1e-8 (after the shift x->x-1).
  KILL: not 3, or Y_k off by >1e-6 -> the code does not model the class; NO search result may
  be trusted or reported. (A search that cannot return 3 on the known 3-cycle system is not
  validated.)
- C3 (negative controls). (i) T_L*T_R>0 -> 0 cycles; (ii) continuous (a_L=a_R, Lienard) ->
  never >1 cycle in a scan, Freire et al. theorem. KILL: any >=2 in a continuous case = bug.
- C4 (continuation). Moving a_L away from a_R from the known 1-cycle continuous example (and
  continuing the x'-jump parameter), track #sign changes of G. Pure observation; no kill.
- C5 (main claim). There is a parameter set (A_L,b_L,A_R,b_R), both zones foci, with >= 4
  crossing limit cycles. PASS only if: exact parameters recorded; count robust under grid
  refinement; each of the 4 roots re-confirmed by an INDEPENDENT method (scipy solve_ivp
  integration with a different tolerance, plus Newton on the 3-unknown system as in
  Llibre-Ponce); closed orbits verified to be CROSSING (no sliding contact).
  Otherwise verdict = REPEAT (not found), never "L*=3".

## What this does NOT mean

1. Not finding >=4 does not show L*=3; the search space (12-dim, plus focus-node / saddle
   combinations not scanned) is only sampled near the known mechanism.
2. A numerical 4 would still be only a LEAD until a validated enclosure (Newton-Kantorovich /
   interval arithmetic) exists, plus a check against the literature for prior 4-cycle examples.
3. Reproducing 3 cycles reproduces known work, it is not new.

## Constraints

- Only focus-focus is modelled (closed form needs w>0 in both zones). Node/saddle zones skipped.
- Cycles considered: those that cross x=0 exactly twice per period (one R arc + one L arc).
  A cycle with 4+ crossings would be a periodic point of period >=2 of the first-return map on
  the "up-crossing" half-line; that map is monotone increasing (planarity / Jordan curve), and a
  monotone increasing 1D map has only fixed points as periodic points [INFERRED, standard
  argument; not re-derived here], so 2-crossing cycles are the only crossing cycles.
