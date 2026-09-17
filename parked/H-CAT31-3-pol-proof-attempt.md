# PARKED — H-CAT31-3 `(POL)` proof-attempt line (Points 77–92)

**Date parked:** 2026-09-18
**Scope note:** this entry parks ONLY the `(POL)` proof-attempt sub-line (Points 77–92) within
the broader `H-CAT31-3` experiment, not the whole experiment (which has separate, still-open
questions: `F4rel`, `R_n`, composite `n`, and the project's own original target
`Var(log(θ(G)/√n))=O(1/n)`). The graph node `H-CAT31-3` already records `RESULT: REJECTED` for a
narrower, earlier claim (the direct `-1` log-log slope exponent, killed ~Point 54) — that verdict
is untouched here.

**Deviation from `parked/INDEX.md`'s own template, stated explicitly:** the template instructs
copying the filled-in `decision.md` into this file. `decision.md` for this experiment is over
10,000 lines (Points 1–92). Copying it here would not aid a future reader — it would just
duplicate the primary record. This file instead SUMMARIZES the arc and points at the primary
source (`experiments/20260910-lovasz-theta-variance-scaling-cat31-3/decision.md`, Points 77–92)
for full detail, evidence, and the extensive skeptic-review trail behind each claim below.

## What `(POL)` is

`(POL): sup_n E‖x*(G)‖² < ∞` — equivalently (Point 85), `E[CV²(y*)] = O(1)`, where `y*` is the
LP-optimal certificate for `θ(G)` on a random dense circulant graph, `CV²(y) :=
Var(y|supp)/Mean(y|supp)²`. Reduces, via the project's own exact KKT identity `s=2Q+1` (Point 85)
and support-saturation fact `s=Θ(n)` (Points 64/85), to whether the LP-optimal certificate's
nonzero weights stay roughly uniform (bounded coefficient of variation) as `n→∞`.

## Why parked — summary of the kill/correction sequence

Four independent proof-attempt ROUTES were killed with precise, quantified reasons, each genuinely
attempted (not just cited):
1. Direct Talagrand transfer from Arora-Bhaskara's i.i.d.-edge technique — killed Point 81,
   circulant graphs lack the `Θ(n²)`-independent-bits structure the technique needs.
2. Uncertainty-principle-on-supports — killed Point 85, saturated with zero slack at every
   non-degenerate LP vertex (Tao's inequality holds as equality, no room to extract new info).
3. Young's/sup-norm convolution bounds on `F4rel` — killed Point 86, gap widens with `n`.
4. KKT/argmin-stability via LP non-degeneracy margins — killed Point 88, zero correlation between
   vertex margins and `CV²`, survived an adversarial skeptic pass testing 3 alternative
   explanations.

An extensive measurement program (Point 87, `n=127→8009`, up to 300 reps) found `mean(CV²)` is
**significantly, genuinely increasing with `n`** (`0.987→1.050`, `9σ+` from 1 at the largest `n`) —
real, not noise, but whether it converges to a constant or grows without bound is **unresolved and
likely unresolvable within this `n`-range**: a 5-model functional-form comparison (Point 87§4I) and
two genuine out-of-sample tests (Point 87§4K) both, independently, found the candidate models
statistically indistinguishable over `n∈[127,8009]` — this line was formally, robustly CLOSED via
3 converging lines of evidence, not merely inconclusive.

A separate heuristic (the "D2" Dirichlet pair-weight model, Point 89) does not explain the drift
either, and turned out to be algebraically CIRCULAR with the same open `mean(CV²)` question — not
independent evidence.

A detailed proof-structure audit of the closest published result (Bandeira et al. 2025,
arXiv:2502.16227, Points 90 and 92, each independently corrected twice by a real skeptic before
reaching final form) established: `(POL)`, even if proven exactly as stated, would close the
`log log n` ORDER gap in that paper's own Theorem 1 (`Θ(√n)`) but would NOT give the paper's own
sharp constant Conjecture 1 (`(1+o(1))√n`) — and `CV²(y*)` is already, trivially, bounded by the
SAME `O(log³n)` ceiling the paper's Lemma 5 already gives (Point 92) — genuine but modest
clarifications, not progress toward a proof.

Two final, cheap ("no computation") next steps named by Point 90 were then attempted and both
KILLED/corrected by real skeptic passes (Points 91, 92):
- **Point 91**: whether `s=2Q+1` (established only for the `θ`-optimal vertex) holds at EVERY
  non-degenerate vertex of the polytope, as pilot evidence toward the paper's own `(SP)` sparsity
  conjecture — KILLED. Contained a composite-modulus test-design error (`n=63` is not prime, and
  the skeptic constructed an explicit feasible counterexample with support well below the claimed
  floor) AND a numerical threshold bug (a claimed "sub-floor" vertex at `n=251` was a pure
  threshold artifact — at a tighter, verified-clean threshold, support matched the already-known
  Tao floor exactly, no violation). Both independently re-confirmed with fresh code before
  recording as killed.
- **Point 92**: whether `mean(CV²)`'s drift is already implied by the paper's own `O(log³n)` bound
  — the claimed "novel Parseval connection" was FALSIFIED as novel (already explicit, verbatim, in
  this project's own prior derivation file); what survives is a simpler, corrected, but ALREADY
  mostly-known bound, not new leverage.

## Kill Analysis (FL Anti-Overfitting Gate)

**What is killed:** every attempted PROOF ROUTE for `(POL)` this arc tried (4 routes, Points
81/85/86/88) — no remaining untried route identified as promising after Points 90–92's own
"cheapest next step" search came up empty twice.

**What is NOT killed:** `(POL)` itself remains an open mathematical question, not disproven — only
every attempted approach to proving it has failed. The extensive `CV²` measurement program (Point
87) remains valid, reusable data. The Bandeira et al. proof-structure understanding (Points 90, 92)
is a genuine, durable contribution to this project's own map of the literature, independent of
`(POL)`'s own fate.

**Revival condition (measurable, per Adaptive Iteration discipline):** any of —
(a) a genuinely new proof technique for `(POL)` not among the 4 already-killed routes, with a
concrete argument sketch, not just a name; (b) new literature (a follow-up to arXiv:2502.16227, or
an unrelated paper) that bounds `CV²`-type quantities for LP/SDP optimizer coordinates specifically
(Point 79's own Gate 0 novelty search found nothing in this class as of 2026-09-16 — re-run that
search if reviving); (c) a low-density (small `c`), prime-`n`, structured (non-generic-objective)
follow-up to Point 91's killed investigation that avoids all three of its named bugs and finds a
genuine sub-Tao-floor sparse vertex — Point 91's own "what survives" section names the concrete
setup needed.

**What this project's own original target still has going for it:** the project's OWN stated
original target, `Var(log(θ(G)/√n))=O(1/n)`, is a DIFFERENT (and per an external analysis relayed
mid-session, potentially stronger-implying) claim than `(POL)` — proving it would give the paper's
own sharp Conjecture 1 directly (per a "mean-gap" connection referenced but not independently
re-derived in this arc, flagged `[WEAK]` in Point 90). This target is NOT parked by this entry —
it was the project's target before the `(POL)` detour began at Point 77, and remains open,
untouched by this specific proof-attempt line's failure.
