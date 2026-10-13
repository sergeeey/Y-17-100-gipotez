# decision.md -- 20261003-lum-chua-continuation (round 2, Problem #30: Filippov 2-zone PWL, straight line)

## Verdict

- [x] REPEAT -- no system with >= 4 crossing limit cycles found; NOT evidence that L* = 3.
  Round-2 deliverables (a), (b), (c) are done and validated; (d) was run to a bounded budget and found nothing.
  No LEAD is claimed. Nothing here is new mathematics: the reproduced 3-cycle system is the published
  Huan-Yang / Llibre-Ponce / Freire-Ponce-Torres example.

## What was done (all numbers re-run serially in this session; see controls.md)

| Item | Result | Marker |
|---|---|---|
| (a) fast half-return (closed form per focus zone, sign-scan + vectorised bisection), `pwl.py` | worst rel. error 8.0e-11 vs scipy DOP853 rtol 1e-12 on 10 parameter sets; 118x faster (0.044 s vs 5.2 s per 250 starts); no grid-edge artefact in the HY / continuous controls | [VERIFIED] |
| (c) positive control, discontinuous class: Llibre-Ponce / Huan-Yang system | exactly 3 crossing cycles; Y1,Y2,Y3 agree with the 30-digit published values to 8e-15 / 1e-14 / 4e-16; stable under grid refinement (3000 -> 8000 pts, y-range to 2000) | [VERIFIED] vs published numbers read in full text (UAB preprint LliPon2011.pdf) |
| negative controls | same-sign traces: 0 cycles in 100/100; continuous a_L=a_R: max 1 cycle in 200 draws (Freire et al. 1998 theorem not contradicted) | [VERIFIED] |
| (b) continuation from the known 1-cycle continuous example (Lienard form T_L=-2,D_L=5,T_R=0.5,D_R=1,a=0.5) | moving a_L, a_R or the x'-jump beta alone (121 points each, range +-6 / +-4): the cycle count is 0 or 1 only; one birth event each (a_L=-0.4, a_R=-0.1, beta=-0.4 on the grid). 2D (a_L,beta) 25x25: max 2 (one point, (a_L,beta)=(-3.5,4)); earlier 33x33 run: 2 points (-2.625,3.0), (-2.25,2.5), re-verified independently (expm+fsolve and DOP853 simulation: closure <= 5e-13, transversal, first-return) | [VERIFIED]; counts are sign changes on a grid |
| (d) structured search near HY, 12 parameters (A_R,A_L,e_R,e_L) | perturbations of HY: sigma=0.003 -> 133/150 have 3 cycles; 0.03 -> [144,191,11,54] cycles 0/1/2/3 of 400; 0.3 -> [207,59,3,1] (130 invalid, not focus-focus); three (1+1)-ES runs (16 candidates x 100 iterations each, count then near-event score) all stalled at 3; uniform random general focus-focus draws: 1500 valid, hist [1367,131,2], max 2. **No count >= 4 anywhere** (found4.jsonl never created). | [VERIFIED] (counts), search coverage is small |

Replication check vs. the earlier (Pool-based, unverified) run: sigma=0.003 gave 88.9% vs 87.8% 3-cycle
fraction; sigma=0.03 gave 13.5% vs 9.8%; same maximum (3). The 1D continuation sweeps reproduce exactly.

## Findings that are real but small

1. [VERIFIED] Round-1 used a STRICT subfamily (Lienard form: x-component continuous across x=0 -> no sliding
   region). The published 3-cycle mechanism lives in the family with a sliding segment (Huan-Yang example has
   sliding on {x=1, 1/5<=y<=19/50}). Round-1's "never more than 1" was therefore uninformative about the
   discontinuous 3-cycle mechanism. Within the Lienard+x'-jump (beta) family the maximum seen is 2.
2. [VERIFIED] 3 cycles are not an exotic isolated point in 12-D: in a relative neighbourhood sigma=0.003 of HY
   about 89% of random perturbations still have 3; but uniform random focus-focus draws gave 0 of 1500 with 3
   (2 of 1500 with 2). The multi-cycle region is reachable only through the mechanism, as the paper title says.
3. [VERIFIED, methodological] The lexicographic ES objective (count, near-event score) is partly gamed: all three
   ES runs ended at near-event scores 3e-5..4e-4 with step size collapsed to 1e-4. Analysis of the first run
   (`analyze_near.py 0`) shows the "event" is a root sitting 3e-3 from the END of the finite domain of the
   half-return maps (a weak-focus R zone, w=0.098), not a tangency; a one-parameter line search over all 12
   parameters (12 shifts from -3e-2 to +3e-2 each) never produced 4. Near-event scoring should exclude domain-end
   artefacts or use tangency (dG=0) detection separately before it is trusted as a guide.

## Skeptic Concerns (self-listed; no PROMOTE so no formal Step 8a)

- Search was bounded (roughly 7.5k G-count evaluations in this session (950 phase-1 + 1500 random + ~5100 ES + continuation grid), plus ~4k from an unverified parallel run):
  absence of 4 says nothing about L*. [Accepted limitation]
- Only focus-focus, only cycles with exactly 2 crossings (argued, not re-derived, that other crossing cycles
  reduce to fixed points of a monotone map). Node/saddle zones, sliding cycles, and the full canonical 5-parameter
  Freire-Ponce-Torres space were not scanned. [Accepted limitation]
- Counting sign changes on a log grid (2500-8000 pts) can miss two roots closer than the grid spacing (a
  tangency pair just born). No such miss was observed in controls (HY: 3 at all three resolutions) but a pair
  born near a root cannot be excluded. [Accepted limitation]
- Freire-Ponce-Torres 2014 (Publ. Mat. 58 S1, 221-253) full text NOT obtained: the Project Euclid page lists it as
  subscriber-only (only the abstract was read this session: 5-parameter canonical form, regions with 0,1,2,3
  crossing cycles). The canonical-form search space was therefore not used. [UNKNOWN: whether it contains hints
  toward 4]
- No novelty search for "4 crossing cycles, straight line, two foci" beyond: the Braga-Mello 4-7 cycle results
  concern non-straight separation lines (EJDE 2015/228 full text; IJBC 2014 full text not opened); a 2026 web search
  returned only center-type / three-zone papers. Absence of a hit is not proof (rule 3).

## If REPEAT: what would change the next attempt

- Change the search class, not the volume: (i) get the Freire-Ponce-Torres canonical form (library / author preprint /
  ResearchGate) and search that 5-parameter space with sliding-region unfolding, where the 3-cycle region is
  an open set and its boundary strata (grazing, tangency) are explicit; (ii) detect tangency (G=G'=0) directly
  by solving, instead of scoring on a grid; (iii) include node/saddle-focus pairs.
- Only if a count >= 4 ever appears: exact parameters + (1) expm+fsolve Newton on (tR,tL,y0), (2) DOP853 full piecewise
  simulation, (3) transversality at both crossings, (4) interval enclosure -- the machinery exists in `verify.py`.

## Pearl Registry candidates

| Insight | Falsifiable prediction | next_check |
|---|---|---|
| Lienard-form (x'-continuous) sub-family of 2-zone Filippov PWL cannot reach the HY mechanism: needs the x'-jump / sliding segment | in the Lienard+beta family the max crossing-cycle count stays <= 2 under a finer search (not 3) | next Problem #30 round |
| ES lexicographic near-event objective is gamed by domain-end roots | replacing it with an explicit tangency detector changes the ES end point away from a domain-end root | same |

## Files

`pwl.py` (fast maps), `validate_fast.py/.json`, `c2_hy_control.py/.json`, `c3_controls_serial.py/.json/.log`,
`continuation3.py/.json/.log`, `verify.py`, `verify2.py`, `search3.py`, `search3_runs.jsonl`, `queue.log`,
`analyze_near.py`, `run_serial_queue.sh`, `claim.md`, `controls.md`. Pool-based earlier scripts
(`continuation.py`, `continuation2.py`, `controls.py`, `search.py` main, `search2.py`) and their outputs, plus
`*_precision_bug.*`, are kept only as history and are NOT relied upon.
