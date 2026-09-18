# PARKED — H-CAT31-3 active search (Points 77–95), scope extended 2026-09-18

**Date parked:** 2026-09-18 (originally scoped to Points 77–92; extended same day after Point 95)
**Scope note:** this entry parks the ENTIRE active-search effort on `H-CAT31-3` as of Point 95 —
not just the `(POL)` proof-attempt sub-line (Points 77–92), but also the two follow-ups attempted
after it: `F4rel` (found gated on the already-parked `(POL)` — its clean route to the main theorem
needs `J_n=O(1)`, but `F4rel`+the current second-moment bound only gives `J_n=O(log⁶n)`, not new
leverage) and `R_n` (Point 95: a pre-registered tightened-reps follow-up, found by a real skeptic
review to leave the scaling question as open as before — the weighted 95% CI on `R_n`'s own scaling
exponent contains BOTH `b=0`, the target hypothesis's own plateau, and `b=1`, a scenario where
`Var(X_n)` does not decay as `1/n` at all). This is a deliberate research PAUSE, not a KILL — none
of `(POL)`, `F4rel`, or `R_n`'s scaling is disproven, only every attempted cheap next step has
stopped yielding new information. This does NOT park the broader `H-CAT31-3` experiment's
`composite n` question in a different sense than before (H-CAT31-2's own divisor-feature test of
it was separately `REJECTED`, not merely parked — see that experiment's own decision.md) or, most
importantly, the project's own original target `Var(log(θ(G)/√n))=O(1/n)` as a claim in its own
right, independent of any specific proof route to it. The graph node `H-CAT31-3` already records
`RESULT: REJECTED` for a narrower, earlier claim (the direct `-1` log-log slope exponent, killed
~Point 54) — that verdict is untouched here.

**Why extended (not just the original `(POL)` scope):** `F4rel`'s only clean path to the main
theorem needs the already-parked `(POL)`'s own tighter second-moment bound, so it offers no
independent route (Point 92's own algebra, independently re-checked). `R_n`'s own pre-registered
follow-up (Point 95) was the ONE concrete, ready-to-run next step available at the time of the
original PARK — it has now been run, and a real skeptic review found it does not discriminate
between the target hypothesis and its negation. No further ready, non-tautological cheap next step
remains for this experiment as of 2026-09-18.

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
setup needed; **(d) for `R_n` specifically (Point 95's own named fallback, cheapest first):**
combine the old (200/150/80-rep) and new (800/600/160-rep) draws via inverse-variance weighting at
each `n`; equalize rep counts across all tested `n` (removes both the estimator-bias/`n` confound
and the "how many power-law comparisons 'fail' depends on rep count" artifact); reformulate the
target explicitly as a `95%` CI on the scaling exponent `b` in `n·R_n∝n^b`, with a PRE-REGISTERED
stopping rule for how many points/reps would be needed to exclude `b=1`; use a BCa or studentized
bootstrap for `n·R_n` specifically (its CI is visibly skewed and sits near the `b=0` boundary,
exactly where percentile-bootstrap coverage is weakest).

**(d) EXECUTED 2026-09-18 (decision.md Point 98) — still inconclusive for `R_n` itself, but a real,
precise positive side-finding for the project's own original target.** Pooled old+new draws,
equalized to `800-1000` reps at `n=509/1021/2039` (`~159min` LP-solve time at `n=2039` alone), BCa
bootstrap + nested-bootstrap exponent CI, exactly as specified above. A first-draft result looked
like a genuinely new, concerning finding (CI excluding both `0` and `1`) but a context-asymmetric
skeptic found a real methodological bug (delta-method log-SE instead of the already-equivariant
BCa interval) — corrected, `R_n`'s own exponent CI is `[-0.04,1.01]`, landing back in the SAME
`STILL INCONCLUSIVE` bucket as Point 95, even at `5×` the effective sample size (more data bought
precision, `SE` narrowed `0.479→0.268`, matching pure `√5` scaling, not resolution). **The genuinely
valuable result of this revival effort was a byproduct, not the target**: the SAME pooled data,
fit DIRECTLY on `n·Var(X_n)` (bypassing the `R_n` decomposition entirely), gives `b_Var=
-0.042±0.046`, `95%` CI `[-0.13,0.05]` — `5×` more precise than the `R_n`-only fit and consistent
with (mildly supporting) `Var(X_n)=O(1/n)` directly, the single most informative confirmatory
number for the project's headline claim `C0` produced by any experiment to date at these 3 `n`.
**Updated revival condition for `R_n`'s own scaling question specifically**, named by the same
skeptic review: a single additional point at `n≈8191` (next convenient prime, doubling the tested
log-`n` range from `1.39` to `2.78` natural-log units) would be more informative than any further
rep-count increase at the existing 3 points — pre-registered kill criterion: predicted `n·R_n`
under the pure power-law scenario vs. the log-saturating/flat alternative diverge by `~3.5σ` at
`n=8191` at comparable rep counts. Not pursued in this point (uncosted fresh LP-solve budget at a
new `n`, matching this project's own discipline against manufactured compute expansion).

**What this project's own original target still has going for it, corrected (Point 94):** the
project's OWN stated original target, `Var(log(θ(G)/√n))=O(1/n)`, is a DIFFERENT claim than
`(POL)` — but the "mean-gap" connection to Bandeira et al.'s sharp Conjecture 1 that was originally
relayed and flagged `[WEAK]` was found, on independent derivation, to run in the OPPOSITE direction
(`decision.md:215-230`'s own real result shows mean-gap-closing forces variance to vanish, not the
converse) — and a rare-value counterexample (Point 94 addendum, `sympy`-verified) shows
`Var(X_n)=O(1/n)` alone is compatible with the mean gap DIVERGING, not merely missing the sharp
constant. This target is NOT parked by this entry — it was the project's target before the `(POL)`
detour began at Point 77, and remains genuinely open — just without the shortcut to Conjecture 1
the original relayed claim suggested.
