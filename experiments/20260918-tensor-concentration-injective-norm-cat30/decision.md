# H-CAT30-1 — decision.md

## Result

**Pilot design is DEGENERATE and cannot test the claimed open regime — REJECTED, not INFORMATIVE-NEGATIVE.**

The original pilot (fixed `n=20` rank-1 tensors `T_i=a_i^⊗3`, scanning `d∈{5,10,20,40,80,160}`)
measured a quantity that, by construction, only depends on `d` through the `n×n` Gram matrix
`G=AA^T` of the FIXED family of `n` vectors — never through a genuinely `d`-dimensional search.
This was caught by a context-asymmetric skeptic review (FL Step 8a) dispatched with ONLY
`claim.md` and the core code, no session reasoning, and then independently re-derived and
re-verified before writing this record (per this project's own standing discipline).

## The degeneracy, proven and independently re-verified

**Skeptic's argument (real math, not a statistical quibble):** `f(x)=Σ_i g_i⟨a_i,x⟩^3` depends
on `x` only through `u=Ax∈R^n`. The supremum over `||x||_2≤1` is therefore attained inside
`span{a_i}` (an at-most-`n`-dimensional subspace of `R^d`), for ANY `d`. As `d→∞` with `n` fixed
and `a_i` random unit vectors, `G=AA^T→I_n`, and the true value converges to a closed form:

```
Σ g_i u_i^3 ≤ max_i|g_i| · Σ|u_i|^3 ≤ max_i|g_i| · (Σu_i^2)^{3/2} ≤ max_i|g_i|
```
with equality at `u=±e_{i*}`, `i*=argmax|g_i|` — i.e. **the asymptotic plateau IS `E[max_i|g_i|]`**,
an order statistic of `n` gaussians, carrying zero information about the tensor's dimension `d`.

**Independently re-verified (this session, fresh code, not accepted from the skeptic's own
arithmetic):**
1. `E[max_{i≤20}|Z_i|]` computed two independent ways — direct Monte Carlo (4,000,000 samples:
   `2.16701 ± 0.00024`) and numerical integration of the exact survival-function formula
   (`2.16657`, quadrature error `~3.6e-10`) — agree to 4 decimal places.
2. This closed-form value matches the pilot's own observed plateau (weighted constant across
   `d=40,80,160`: `2.1565`) to **0.48% relative gap**, well within the pilot's own reported
   standard errors (`~0.05-0.06`).
3. **Direct structural confirmation**: the optimizer's found `x*` lies EXACTLY in `span{a_i}` at
   every tested `d`, including `d=400` — orthogonal-complement residual norm `~1e-16` (machine
   precision), not merely small. This is not a numerical coincidence; it follows mechanically
   from the update rule (`x ← normalize(A^T(...))` always produces a vector in `span(A^T)`).

**Conclusion: the pilot's "flat plateau at large `d`" was NOT evidence about Conjecture 16's
dimension-free claim in the open `p<2r` regime — it was a theorem about `n=20` fixed gaussians,
true regardless of whether Conjecture 16 is true or false.** A kill criterion whose outcome is
derivable in three lines before running any code is not a test (skeptic's own phrase, matches
this project's own Cheapest Differentiating Test Protocol's ban on circular tests).

## Skeptic's additional findings (all independently assessed, not accepted wholesale)

| Skeptic finding | This session's independent assessment |
|---|---|
| Full-range power-law fit's CI, properly scaled by `sqrt(chi2/dof)` for the rejected model, widens to `[-0.130,-0.026]` — crosses the pre-registered LEAD threshold | **Accepted.** The pilot's own reported CI used the model's raw (unscaled) SE despite `chi2=29.05,p=7.6e-6` rejecting that model — a real statistical error, independent of the degeneracy argument. |
| Tail-only fit (`d≥40`) was an unregistered post-hoc exclusion — AOG-1/AOG-2/AOG-5 violation | **Accepted.** `d≤n=20` vs `d>n=20` is a real, nameable regime boundary (rank-deficient `G` vs not) that was NOT stated as a pre-registration criterion before seeing the chi2 failure — this is exactly the kind of after-the-fact rescue `falsification-ladder.md`'s Anti-Overfitting Gate exists to catch. |
| Random rank-1 construction samples a "typical" (non-tight) point, not a worst-case one — `LHS/√(Σ‖T_i‖²)→0` is the wrong regime for a conjecture about the worst case | **Accepted as a separate, independent problem** even setting the degeneracy issue aside — matches the catalog's own suggested "First Research Experiment" wanting ADVERSARIAL search, not random sampling, which this pilot never attempted. |
| Missing family-level variance (only ONE random draw of `A` per `d`; reported SEs are conditional-on-`A`, not accounting for variance across draws of `A` itself) | **Accepted as a real gap**, independent of the degeneracy finding — the chi2 rejection of the full-range fit likely reflects this missing variance component in part, though the degeneracy argument alone is sufficient to reject the pilot's conclusion regardless. |

## Kill Analysis (FL Anti-Overfitting Gate)

**What is killed:** this specific pilot design — `n` FIXED, scanning only `d`, using random
(non-adversarial) rank-1 tensors — as informative about Conjecture 16's claimed dimension-free
rate in the open `p<2r` regime. This is a **hard, provable kill of the method**, not a statistical
"probably wrong" — the degeneracy is a theorem, confirmed independently twice (closed-form
asymptotic match to 0.5%, and exact `x*∈span{a_i}` to machine precision).

**What is NOT killed:**
- Conjecture 16 itself — completely untouched; this pilot never actually probed the genuinely
  open regime (a d-dimensional search requires `n` to scale with `d`, which this design never had).
- The numerical pipeline — verified correct via 4 independent checks (analytic-vs-finite-difference
  gradient match, power-iteration-vs-Nelder-Mead cross-check, exact single-tensor norm
  verification to 10 decimals, restart-count robustness) — all now locked in as regression tests
  (`tests/test_tensor_injective_norm.py`, 4/4 passing).
- The `d≫n` regime as a genuine, useful **positive-control canary** for any future optimizer on
  this problem class: it has an exact closed-form answer (`E[max_i|g_i|]`) that any correct
  implementation MUST reproduce — valuable as a substrate/oracle-adequacy check, not as evidence
  about the conjecture.

**Relaxation Map (one assumption changed at a time, per Minimal Relaxation Rule):**
- **Scale `n` with `d`** (e.g. `n=d` or `n=d^{3/2}`) so the effective search space is genuinely
  `d`-dimensional and the paper's own "volumetric barrier" (an entropy argument over a `d`-dimensional
  ball) can actually bite — this is the ONE necessary change; everything else below is secondary.
- Measure the RATIO `R(d)=LHS/√(Σ‖T_i‖²)` against `polylog(d)`, not the raw LHS — the raw value
  conflates the conjecture's own scaling with whatever baseline growth `√(Σ‖T_i‖²)` itself has
  under the new `n=n(d)` scaling.
- ≥10 independent draws of the tensor family `A` per `d`, with between-family variance folded into
  the error bars (addresses the missing-variance gap above).
- A certified upper bound (e.g. an SOS/SDP relaxation, cheap here since the reduction to `G`'s
  `n`-dimensional structure applies to any fixed-`n` sub-check) paired with the power-iteration
  lower bound, sandwiching the true value instead of a one-sided heuristic.
- Adversarial (not random) tensor family search, matching the catalog's own suggested first
  experiment and this project's own established H-CAT37-1→H-CAT37-2 convention (random baseline
  first, adversarial follow-up second — this pilot only completed the random half, and even that
  half was degenerate).

**Pre-registered kill criterion for any redesign attempt (stated now, before any such attempt is
made — per skeptic's own proposal, adopted verbatim):** LEAD if `R(d)~d^c` with `c>0.05` at 3σ,
computed AFTER including between-family variance, on BOTH tested `n(d)` scalings; INFORMATIVE-NEGATIVE
if `R(d)/polylog(d)` is flat on both scalings with a certified upper bound present. Points with
`d≤n` excluded from any fit, stated in advance (not post-hoc).

## Verdict

**REJECTED.** Not a null result about Conjecture 16 (which remains genuinely open, untouched) —
a rejection of this specific pilot's ability to say anything about it. The construction was
provably confined to an at-most-`n=20`-dimensional subspace regardless of the ambient dimension
`d`, so scanning `d` alone, with `n` fixed, could never have been informative about the open
`p<2r` regime, independent of whether the numerical execution was correct (it was).

## What this does NOT mean

1. Does NOT mean Conjecture 16 is true, false, or that this project has any evidence either way.
2. Does NOT mean the general approach (Monte-Carlo probing of tensor concentration inequalities)
   is unsound — only that THIS specific fixed-`n` construction cannot reach the open regime.
3. Does NOT invalidate the numerical pipeline itself (`tensor_injective_norm.py`) — it is correct
   and reusable for a redesigned experiment per the Relaxation Map above.
4. The `E[max_i|g_i|]` closed-form match is not claimed as a novel finding — it is a basic order-
   statistic fact used here purely diagnostically, to confirm the degeneracy.

## Revival Condition

A redesign implementing the Relaxation Map above (primarily: `n=n(d)` scaling so the search is
genuinely `d`-dimensional) — not a hard theorem-level contradiction, so this stays available for
revival, not permanently closed. Given the significant redesign cost (certified upper bound,
adversarial search, multi-family variance) relative to this project's other currently-open leads,
no immediate follow-up is planned; this is a deliberate stop, matching the same discipline just
applied to H-CAT31-3's own PARK decision after Point 95.

## FL Step 8a

Run as specified: context-asymmetric skeptic (`claim.md` + core code only, no session reasoning),
verdict `FALSIFIED` on the central claim, with specific per-concern verdicts in the table above.
All specific numerical/mathematical claims in the skeptic's report independently re-derived with
fresh code before acceptance (`verify_skeptic_degeneracy_claim.py`) — not accepted on the
skeptic's own arithmetic alone, per this project's own standing rule.

## Methodology lesson, `[REPEAT]`-worthy — this window's dominant pattern extends to a new project session

The N-th consecutive instance (across the whole session containing this experiment) where a
positive-leaning finding sent to a real, context-asymmetric skeptic before being written to a
permanent record was found to contain at least one genuine, load-bearing error. This one is
unusual in KIND, not just degree: the flaw was not a statistical miscalculation but a structural
degeneracy in the experimental DESIGN that made the "kill criterion" derivable in three lines
before running any code at all — worth naming explicitly for future experiments in this project:
**before scanning a parameter (here, `d`) as if it controls the difficulty of a search, verify
that the parameter actually enters the optimization's effective degrees of freedom** — a cheap,
generalizable pre-check (e.g. "does the objective depend on `x` only through a lower-dimensional
projection?") that would have caught this before any computation was run.
