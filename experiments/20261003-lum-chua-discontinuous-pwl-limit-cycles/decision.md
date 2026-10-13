# decision.md — 20261003-lum-chua-discontinuous-pwl-limit-cycles

## Verdict

- [x] REPEAT — inconclusive; need more data or different approach; document what to change

## Evidence Summary

| Check | Result |
|-------|--------|
| Positive control (continuous, a_L=a_R=0.5, TL=-2.0,DL=5.0,TR=0.5,DR=1.0) | PASS — found exactly 1 cycle (y*=2.887683), matches Freire et al. 1998 / Carmona et al. 2019 theorem |
| Positive control, 35-config calibration scan | PASS — never found >1 cycle across any continuous config tried, 0 counterexamples to the theorem |
| Negative control (T_L*T_R>0) | PASS — found 0 cycles, matches Green's theorem argument |
| Stress tests | SKIPPED — idea-scouting stage, Standard-Ladder, stress_tests.md not required (Step 7 is a Full-Ladder item; no ≥90% success here to trigger skeptic-triggers.md Rule 3 override) |
| Skeptic verdict | SKIPPED — no PROMOTE claim made, nothing to defend adversarially |

## Rationale

40 uniformly-random draws of `(T_L,D_L,a_L,T_R,D_R,a_R)` (focus condition + `T_L*T_R<0`
enforced, `a_L,a_R ∈ [-5,5]` independent) found **at most 1** sign change of the composed
half-return map in every single trial — never 2, never 3+. This is not evidence that the
discontinuous case is actually bounded at 1 (that would contradict the already-cited
literature construction of 3 nested cycles) — it is evidence that **blind random search in
this parameter range essentially never lands near the structured configuration multi-cycle
examples require**. The paper that first produced 3 cycles is explicitly titled "a general
MECHANISM to generate three limit cycles" (Freire-Ponce-Torres 2014) — mechanism, not luck.

## If REPEAT: What Changes Next Attempt

- Change: stop searching blindly. Start from a KNOWN single-cycle continuous configuration
  (`T_L=-2.0, D_L=5.0, a=0.5, T_R=0.5, D_R=1.0`, cycle at y*≈2.887683) and **perturb `a_L`
  away from `a_R` continuously** (parameter continuation / numerical bifurcation tracking),
  watching whether additional sign changes of `G(y0)` are BORN as the asymmetry `a_L-a_R`
  grows from 0. This is the standard way multi-cycle examples are actually found in this
  literature (perturbation off a known degenerate/boundary case), not uniform random sampling
  of a 6D box. Continuous (`a_L=a_R`) is exactly the boundary between "proven ≤1" and "open,
  possibly more" -- the natural place to look for a bifurcation into extra cycles.
- Also worth trying independently: widen `y_max`/`t_max` (some trials showed roots near the
  grid edge, e.g. trial 5 at y=14.386 with y_max=15 -- possible additional root just outside
  the scanned window; this is a search-budget artifact, not evidence either way).
- Budget estimate for continuation approach: a 1D parameter sweep in `a_L-a_R` (say 50-100
  steps) at fixed other params, tracking how many sign changes appear -- same per-case cost
  (~1-14s) but far more likely to be informative than another 40 random draws, since it
  directly targets the boundary where the known theorem's guarantee (≤1) stops applying.

## Pearl Registry

| Insight | Where applicable |
|---|---|
| Weak-focus parameter regions (T^2 close to 4D) make `scipy.solve_ivp`'s adaptive step cost 5-20x more per half-return than a typical case (observed 0.5s-14s range on an otherwise uniform grid) | Any future numerical ODE search over focus/center-type linear systems in this project -- budget estimates must account for this, not assume uniform per-case cost |

## Pearl Card Update

**Was the Prediction correct?** Not testable yet — the claim was about EXISTENCE of a >3-cycle
configuration; 40 random draws finding none neither confirms nor falsifies existence (absence
of evidence, not evidence of absence — see claim.md "What This Does NOT Mean" #2).

**Falsification condition triggered?** No — claim not falsified, not confirmed, genuinely open
after this round. REPEAT, not REJECT.
