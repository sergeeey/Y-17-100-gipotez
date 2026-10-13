# skeptic_verdict.md -- 20261003-lum-chua-continuation (independent falsification pass, 2026-10-03/04)

Auditor rule: default to REFUTED/UNVERIFIABLE when evidence thin. Everything below was recomputed with an
implementation that shares NO code with `pwl.py` (complex-eigendecomposition closed form, uniform time grid,
vectorised bisection; mpmath 40-60 digit `expm` Newton; scipy LSODA / DOP853 / Radau event integration).
Scripts live in the session scratchpad, not in this folder. All heavy runs were serial, via `scripts/lowprio.py`, <10 min each.
I did NOT rerun the lab's own scripts; I compared my outputs to their logged numbers.

## Verdict table

| # | Claim | Verdict |
|---|---|---|
| 1 | HY control: exactly 3 crossing cycles, Y values as published, no 4th in y in (-400,400) | CONFIRMED |
| 2 | Two Lienard+beta 2-cycle systems: those 4 cycles, only 2 each, transversal | CONFIRMED |
| 3 | No focus-focus system >=4 in HY neighbourhood / 1500 random draws | WEAKENED (finding reproduced; coverage and controls weaker than stated) |
| 4 | Cycles with >2 crossings need not be counted (monotone first-return map) | CONFIRMED (now derived, was only asserted) |
| 5 | Literature: no published >=4 straight-line two-zone example; Braga-Mello 4-7 is non-straight | CONFIRMED with limits; lab's literature scouting itself WEAKENED (missed 2025 paper) |

## Claim 1 -- HY control [CONFIRMED]

* Independent scan (own closed form), G(y0) on 14000 log-spaced points d in [1e-3, 400] from the R fold (y0 = 0.38 - d):
  exactly 3 sign changes, 0 ambiguous gaps. Second scan in the other variable (y1, L-entry side, d in [1e-3,400]): exactly 3.
  Third scan with scipy LSODA event integration (700 pts): exactly 3. Roots (my float): y0 = 0.163826227627, -0.088914080943, -0.486061649127.
* mpmath (dps 60) Newton on (tR,tL,y0): Y values `1.6811945105189341692`, `0.96579985584668225513544464841`, `0.61885416518252502958`.
  Published (Llibre-Ponce, opened myself at ddd.uab.cat LliPon2011.pdf): Y1=1.68119451051893996990946..., Y2=0.96579985584668225513544927..., Y3=0.61885416518252501376...
  Differences: 5.8e-15, 4.6e-24, 1.6e-17. The paper's own Newton-Kantorovich step reports f(z0)~1.6e-16 and alpha=6.5e-15, i.e. the printed "30 digits" are
  accurate to ~15 / 24 / 17 digits only. Lab agreement of 8e-15 / 1e-14 / 4e-16 is therefore real but "30-digit published values" in controls.md is an overstatement.
  Transversality at all 6 crossing points confirmed (x' signs R/L at y0 and y1 all consistent).
* **Correction to the task statement**: the cycle pairing is y0 -> y1: 0.16383 -> 0.61885, -0.08891 -> 0.96580, -0.48606 -> 1.68119 (paper: t1+ = 1.4866 pairs Y1=1.68119 with tR=14.866 in the unscaled time).
  "R arc from 0.16383 to 1.68119" is wrong. Lab files do not contain that error (verify.py pairs correctly).
* Extra independent support the lab did not have: Carmona-Fernandez-Sanchez-Novaes, arXiv 2508.02321 (JDE 2025) prove rigorously that the Huan-Yang system has EXACTLY three limit cycles
  (abstract opened myself). So "no 4th" is a theorem, not only a scan result.

## Claim 2 -- Lienard+beta 2-cycle systems [CONFIRMED]

Zone R: A=[[0.5,-1],[1,0]], b=(beta,-0.5); zone L: A=[[-2,-1],[5,0]], b=(0,-a_L). For each (a_L,beta):
* own scan in y0 (20000 pts, d in [1e-4,2000]) and in y1 (20000 pts): exactly 2 sign changes each, no more.
* mpmath 40-digit Newton + DOP853 full piecewise simulation (rtol 1e-13, event detection): all cycles close.
  (-2.625,3.0): y0=-0.0877655779058 (y1=10.8337563063501, dG=+2.7851), y0=-0.8599565806516 (y1=12.5573759820721, dG=-0.3240).
  (-2.25,2.5): y0=-0.1407712672006 (y1=9.3396943493192), y0=-0.6372403982140 (y1=10.4439853410221). All match the stated 12 digits.
* Transversal at both crossings (x'_R, x'_L signs +,+ at y0 and -,- at y1); the escaping segment y in (0,beta) of the line is never touched by the orbit.
* Bonus: the point (a_L,beta)=(-3.5,4.0), reported by the serial 25x25 run as the ONLY 2-cycle grid point, was never independently verified by the lab. I verified it:
  y0=-0.4282063605941 (y1=14.8288873366517) and y0=-0.7419973821747 (y1=15.5317670799077), closure by mp Newton and DOP853.
* Radau failed with a step-size error on the discontinuous RHS (stiff solver at a sliding-type switch); DOP853/LSODA are fine. Not a claim problem.
* Consistent with theory: Carmona et al. (arXiv 2207.14634) prove <=1 cycle when there is no sliding set, which is why a_L,a_R-only variation (no beta) stays at <=1.

## Claim 3 -- negative search result [WEAKENED]

What survived my attacks (the narrow finding is real):
* Near-event end points of the three ES runs (parameters from search3_runs.jsonl): 24000-pt log scans (d in [1e-5,400]) and 20000-pt linear zooms
  on d in [0.20,0.30] and [0.30,2.5]: exactly 3 roots each, and only two local extrema of G, each with |g| ~ 0.01-0.1 (relative size 1): no root pair near tangency, none closer than the old grid spacing.
* The "near event" is NOT a pair about to be born. G at the domain end is +0.0076 / +0.0068 / +0.0021 with root #1 only 0.4% beyond the end (d_end=0.24349, root 0.24446 for ES0).
  The domain ends because the L-arc return becomes tangent (y2 = L fold), not because the L arc starts tangent (checked: x'_L(y1) = -2.49 at the end). Pushing g_end through 0 makes root #1 EXIT through the end (count 3 -> 2), it cannot create a 4th.
  Parity: G(end)>0, G(far)<0 forces an odd count; a 4th root needs a sign flip at one end: either g_end<0 with a born pair, or kappa = exp(pi(tauR/wR + tauL/wL)) crossing 1 (cycle from infinity).
  ES count-then-score has no handle on either; the lab's own self-assessment ("domain-end artefact") is right.
* I tested the kappa route directly: shift A_L -> A_L + s*I from HY (common equilibrium kept), s in [-0.3,0.1], 41 points: count = 3 only at s=0, 1 at s=+-0.01, 0 on the far side,
  and a 1-cycle of large amplitude appears for kappa<~1.02 (s ~ -0.13, d ~ 40). The 3-cycle window is thin (|s| < ~0.005) and does not overlap the kappa=1 stratum on this line.
* Independent random sampling (my own seed/distribution, 340 valid draws, 170 general + 170 with kappa forced into [0.8,1.25]): hist 0/1/2/3/4 = [156,13,1,0,0] and [126,42,2,0,0]. Max 2. Consistent with the lab's [1367,131,2].
* 150 random perturbations around the three ES endpoints (sigma 3e-3 and 3e-2, own code): max 3 (e.g. ES0 sigma=3e-3: 18/25 have 3), never 4.

Why it is only WEAKENED:
1. **Detector blind spot, never controlled.** The only positive control for the discontinuous class is HY (O(1) amplitudes). I ran the lab's own `pwl.count_cycles` on the published 3-cycle
   systems of Freire-Ponce-Torres-Tonnelier 2021 ("FPTT21", three high-amplitude cycles from Hopf at infinity, kappa = 1 - 3e-8) and Gasull-Rondon-da Silva (GRS, piecewise holomorphic example), both listed in arXiv 2508.02321:
   - GRS: lab code returns 3 (correct).
   - FPTT21: lab code returns **0 sign changes, 3 "noise_suspect"** for dmax = 500, 1e3, 1e4, 1e6 (G at the grid points next to each root is ~1e-9 or less, below NOISE_TOL = 1e-11*(1+|y|) ~ 1.3e-9, so every real sign change is discarded as suspect).
     My independent code finds the 3 cycles at d = 132.6, 200.8, 273.2 (dmax >= 1000). With dmax = 200 (the cap used by `search.py::evaluate`, hence by search3 phase1/es/rand) only 1 of the 3 is inside the window.
   So a search built on this counter cannot see the infinity-Hopf 3-cycle mechanism at all, and any 4-cycle configuration that uses it would be invisible. The negative result is valid for "d < 200, |G| not tiny".
2. Perturbing FPTT21 itself (my own code, sigma 1e-4..1e-2 on 8 entries): count never exceeds 2, but the 3-cycle region there is so thin that sigma=1e-4 already destroys it, so this attack is inconclusive, not exculpatory.
3. Search coverage stays what the lab already says (small, near HY, focus-focus only). Not a proof about L*; the 2025 literature bound for focus-focus is 7, not 8 (see claim 5).

## Claim 4 -- >2 crossings need not be counted [CONFIRMED, derived by me]

Derivation (the lab only asserted it): in a linear zone, two half-arcs from the line are non-self-intersecting and non-crossing. Starts lie on one side of the zone's fold, ends on the other side,
so the endpoint intervals [y1,y0] and [y1',y0'] both contain the fold: interleaving is excluded (Jordan), hence they are nested, hence each half-return map P_R, P_L is strictly order-REVERSING on its domain.
The first return to the up-crossing half-line, P = P_L o P_R, is strictly increasing; an increasing map of a totally ordered set has no points of exact period 2, so a crossing cycle with 4 (or 2k, k>=2) crossings cannot exist.
Numerical attack (46 systems: HY, 3 ES endpoints, a Lienard+beta system, 41 random focus-focus): monotonicity violations 0 of 26615 consecutive pairs; sign(P2(y)-y) != sign(P(y)-y) on 0 of 21710 evaluable points; I could not construct a 4-crossing orbit.
Scope: crossing cycles only (no sliding, no tangent contacts), as in the lab's definition and in Carmona et al.'s ("isolated crossing periodic solution").

## Claim 5 -- literature [CONFIRMED with limits; lab scouting WEAKENED]

* Novaes-Ponce 2015 (IJBC 25, preprint opened in full at ddd.uab.cat): for a straight boundary Han-Zhang conjectured <=2, Huan-Yang gave 3; "when the boundary ... is not a straight line any longer, it is possible to obtain more than three";
  Braga-Mello used "some broken line as the boundary". This confirms the lab's reading of the 4-7 results from a source other than EJDE 2015/228.
* Carmona-Fernandez-Sanchez-Novaes arXiv 2210.12125 (intro opened): for the straight-line class "many other works provided examples with 3 limit cycles"; no example with 4 is cited; L* <= 8; limit cycle = isolated crossing periodic solution.
* **Missed by the lab**: arXiv 2508.02321 (JDE 2025, same authors): (i) HY, FPTT21 and GRS examples have EXACTLY three limit cycles; (ii) Corollary: focus-focus systems have <= 7 limit cycles; (iii) Theorem: <= k+2 via a resultant R(Y1), and <=1 if a discriminant condition P holds.
  decision.md says a "2026 web search returned only center-type / three-zone papers"; the main directly relevant 2025 paper was not found. The bound "8" in claim.md is the general-case bound; for focus-focus it is already 7.
* Limits of my check: the full text of Braga-Mello IJBC 2014 is paywalled ("No Access"); I did not open it either, so "4-7 cycles are for non-straight lines" rests on Novaes-Ponce's description (secondary) plus the lab's EJDE 2015 reading. Absence of a >=4 straight-line example is absence of evidence in 3-4 sources, not a literature census.

## Process issues

1. Positive control did not cover the claimed search space (see claim 3); published 3-cycle systems FPTT21/GRS (available in the 2025 paper) were never run. `count_cycles` (noise-filtered) and `search.evaluate` (unfiltered, dmax=200) are two different counters; only the first was validated.
2. controls.md calls the published values "30-digit"; they are accurate to 15-24 digits. Harmless for the 1e-8 kill threshold, misleading as a precision statement.
3. Literature scouting missed the single most relevant 2025 paper; decision.md "known upper bound 8" is stale for focus-focus.
4. The (a_L,beta)=(-3.5,4.0) 2-cycle point (the only one in the serial 25x25 run) had no independent verification; the two verified points came from the earlier Pool-based 33x33 run that controls.md itself labels UNVERIFIED context.
5. ES objective was gamed (self-reported); I add that its "near-event" is a root leaving, and that the count-parity makes 3->4 reachable only via a flip at an end -- the objective cannot see that.
6. Marker hygiene is otherwise good: counts re-run serially, Pool/precision-bug artefacts excluded, REPEAT (not "L*=3") correctly stated. No item is marked VERIFIED that I found false; the weakest is the implied coverage of the search.
7. Auditor's own caveats: did not rerun lab scripts; claim-3 perturbation sample sizes are small (25 per cell); one MCP response (arXiv LaTeX of 2508.02321) was flagged by a hook as a command-injection pattern; it contained only mathematical text, no instructions, and nothing in it was acted on.

## Bottom line

The reproducible core of the lab (HY control, the 2-cycle Lienard+beta systems, REPEAT verdict) is solid. The negative search is honest but under-controlled: it is blind to the large-amplitude / tiny-|G| 3-cycle mechanism and capped at d<200.
Nothing I tried produced a 4-cycle system; nothing here is a LEAD. Highest-value next step: read arXiv 2508.02321 Section 4 (resultant criterion) and use it to prune/target the 12-D search instead of grid sign-counting.
