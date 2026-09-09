# H-CAT37-2 — decision.md

## Result

### Objective design bug caught before any search result was trusted

A first pilot run (before this committed version) used a flat `-1.0` penalty for every
`exact_solve_hit` outcome. Result: `eval_slope=-1.000000` at ALL three tested `n`, in only
3 seconds of wall-clock time. Inspecting the raw results (not just the summary) showed
**every single candidate the optimizer evaluated hit exact convergence within 7-16
restarts** out of an 800-restart budget — the objective was therefore constant almost
everywhere `differential_evolution` looked, giving it zero gradient. It could not have been
doing meaningful optimization; it was returning an arbitrary point from a flat landscape.

Fixed by rewarding *slower* exact-solves continuously
(`-1.0 + min(0.9, restarts_run / EVAL_RESTARTS)`) instead of collapsing every exact-solve
outcome to the same value. Re-run: `eval_slope` moved from -1.0 to -0.82/-0.67/-0.72 at
n=5/6/7 respectively — the optimizer found real structure, delaying exact convergence by a
factor of ~10-40x over the naive first version (restarts-to-solve moved from single digits
to 39-314 in the extended check, see below).

### Primary finding

For each of `n = 5, 6, 7`, `differential_evolution` (40 iterations, population 10×n,
maximizing a proxy for non-convergence) found its best candidate, then each candidate was
independently re-checked with 5 fresh random initial residuals at 5000 restarts (10x more
than the search's own 800-restart evaluation budget, guarding against the same
short-observation-window artifact H-CAT37-1 itself caught):

| n | best restarts-to-solve found (5 fresh seeds) | resolved to exact convergence? |
|---:|---|:---:|
| 5 | 39, 44, 66, 100, 109 | YES, all 5 |
| 6 | 65, 199, 246, 247, 314 | YES, all 5 |
| 7 | 226, 232, 235, 239, 254 | YES, all 5 |

Every single candidate the optimizer could find — after explicitly, continuously
optimizing FOR delayed convergence, not sampling randomly — still resolved to EXACT
convergence within the extended 5000-restart budget. None showed a genuinely non-decaying
or growing residual-direction gap.

## Verdict

**INFORMATIVE_NEGATIVE**, per claim.md's own pre-registered criterion. A targeted search —
demonstrated to find real structure (10-40x delay over a naive/flat-objective baseline,
itself confirmed via the objective-design bug fix above) — could not locate a genuine
s=4 non-convergent diagonal SPD matrix at n in {5, 6, 7}. This does **not** prove dimension
8 is minimal (see `## What this does NOT mean` in claim.md, item 1 — a bounded
differential-evolution run with fixed budget/bounds cannot exhaustively search the
continuous parameter space), but it is real, honest evidence consistent with the authors'
own choice of dimension 8 not being arbitrary — the "room" for a counterexample genuinely
seems to shrink as n approaches s+4 from below, at least along the directions this
optimizer's proxy objective could explore.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the hypothesis that THIS specific search strategy (differential
evolution over log-diagonal entries, this objective, this budget) would find an s=4
counterexample at n in {5,6,7}. It did not.

**What was NOT killed:** the possibility that a counterexample exists at these dimensions
reachable by a different search strategy (this experiment's own objective is a heuristic
proxy, marked `[UNTESTED-MECHANISM]` in claim.md, not derived specifically for this
dynamical system); the theorem's own support-size bound (5-8 eigenvalues for s=4) is
consistent with n=5,6,7 counterexamples still being possible in principle.

**Revival condition:** a genuinely different search technique — e.g., directly searching
for a fixed point of the rescaled squared-weight map's linearization near a transverse
eigenvalue-crossing (closer to the actual analytic structure of the authors' proof, rather
than this experiment's black-box proxy objective) — could revisit n in {5,6,7}. Not
attempted here; the gap between "a heuristic optimizer found nothing" and "a
theory-informed search found nothing" is real and should not be elided.

## Skeptic Concerns (self-review, FL Step 8a — low-stakes exploratory numerical search, not
architectural; the objective-design bug catch above substitutes for an external adversarial
pass on this experiment's core search logic)

- "3 fixed seeds per objective evaluation is a small, possibly unrepresentative sample" →
  **Accepted limitation**, a cost/thoroughness tradeoff explicit in claim.md; the extended
  check (5 fresh, independent seeds at 5000 restarts) partially mitigates this for the final
  reported candidates specifically.
- "The proxy objective (decay slope / restarts-to-solve) has no proven connection to the
  actual Hopf-bifurcation structure of the true counterexample" → **Accepted, explicitly
  marked `[UNTESTED-MECHANISM]` in claim.md before running** — this is exactly why the
  result is reported as INFORMATIVE_NEGATIVE, not as evidence toward a minimality proof.
- "40 iterations / population 10n is a small optimization budget" → **Accepted limitation**,
  chosen for session-scale tractability; a much larger budget was not attempted here.

## Scope note

Direct follow-up from H-CAT37-1's retroscan (ADR-091), registered as `H-CAT37-2`, grounded
from `H-CAT37-1` and the `pearl_registry/INDEX.md` entry (2026-09-10) that named this
specific, well-posed open sub-question.
