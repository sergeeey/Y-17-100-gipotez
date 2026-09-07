# decision.md — H-B2-1h (coupling-magnitude sweep of M1)

## CORRECTION ADDENDUM (2026-09-07, FL Step 8a skeptic pass — fifth in a row, strongest/most rigorous of the five)

**Verdict flipped CONFIRMED (exponential) → REJECTED (per claim.md's own kill criterion),** on
mathematical proof, not just statistical re-interpretation. Original text kept unedited below
(Hindsight Distortion Gap discipline). This is the fifth `Agent(skeptic)` invocation in the same
`/loop` continuation (after `H-B2-1l`, `H-B2-1j`, `H-B2-1k`, `H-B2-1i`) — the most conclusive of
the five, because the core claim was independently verified by direct computation, not just
argued statistically.

**What the skeptic found, given only `claim.md` + `run.py`:**

**Structural (the load-bearing catch):** `build_matrix(coupling_magnitude)` calls
`np.random.default_rng(SEED)` FRESH with the SAME constant seed on every invocation, so the 10
sweep points do NOT sample 10 different random matrices — they evaluate the SAME underlying
`[0,1)` draw stream, linearly rescaled by `coupling_magnitude`. Algebraically:
`A(c) = D + c·N` for a SINGLE FIXED matrix `N` (strictly upper triangular, hence nilpotent,
`N^8 = 0` for this 8-dimensional construction), independent of `c`.

**Independently verified before trusting this** (not accepted on the skeptic's say-so): a direct
computation comparing `build_matrix(3.0)`, `build_matrix(6.0)`, and `build_matrix(15.0)` confirmed
`off_diagonal(6.0) = 2 × off_diagonal(3.0)` and `off_diagonal(15.0) = 5 × off_diagonal(3.0)` to
machine precision (`atol < 4e-15`) — the scalar-dilation structure is exact, not approximate.

**Consequence — a mathematical fact, not an empirical pattern:** for `A(c) = D + c·N` with `N`
nilpotent of index ≤8, `exp(t·A(c))`'s off-diagonal entries are polynomials in `c` of degree ≤7
for every fixed `t`. Taking the sup over `t` preserves this bound. **`M1(c)` is PROVABLY bounded
by a degree-≤7 polynomial in `c` on this sweep — true single-rate exponential growth is
algebraically impossible for this specific construction, regardless of what any R² comparison
says.**

**The empirical signature was already visible and already reported** — this file's own
pre-correction "Caveat — consecutive-ratio diagnostic shows decelerating growth rate" section
(below) documents the monotonically decreasing ratio (3.76→1.80) and correctly declined to let it
override the pre-registered R²-based verdict, citing Anti-Overfitting Gate discipline (no new
post-hoc criterion after seeing data). **That discipline was correctly applied to the WRONG
question.** Refusing to invent a new statistical test after seeing the data is right; recognizing
that the construction is algebraically INCAPABLE of the claimed functional form is not a new
statistical test — it is a structural fact about the pre-registered construction itself, and
would have been true before any data was collected. The skeptic's own table of implied
polynomial degree at each step (climbing 1.91 → 5.60 as `c` grows, approaching the ceiling of 7)
matches the observed decelerating-ratio pattern exactly, with a mechanism, not just a description.

**Why the raw-NLS R²=0.9994 didn't catch this:** across >3 orders of magnitude (2.66 to 4522),
raw sum-of-squared-error is dominated by the largest values; an exponential and a bounded-degree
polynomial can both match the top 2-3 points closely, making R² a weak discriminator exactly in
the regime this experiment tested. The `_fit_models` docstring already flagged the log-vs-raw R²
pitfall (H-B2-1h's own earlier self-catch) but did not anticipate this second, independent
failure mode of R² as a discriminator.

**What survives:** the raw M1 measurements themselves (real, provenance-verified against
H-B2-1f/g) and the qualitative fact that `M1` grows very fast with coupling magnitude. **What
does NOT survive:** "exponential growth," the CONFIRMED verdict, and the fitted form
`M1 ≈ 9.08 × exp(0.207·coupling_magnitude)` as a description of the underlying mechanism — the
correct characterization is "bounded-degree polynomial in coupling_magnitude along this one fixed
random direction, with the fitted exponential curve serving only as a numerically convenient
LOCAL approximation over the tested range, not a mechanistic law."

**A second, previously-uncharacterized limitation this reveals:** the "single seed" caveat
already in claim.md (§3, "does NOT test multiple seeds... this sweep uses seed=0 throughout")
UNDERSTATED what actually varies. It is not "one random draw, tested at 10 coupling levels" — it
is "one FIXED random direction, uniformly dilated by a scalar." This sweep never tested whether
`M1` scales this way for a genuinely different random coupling matrix at each magnitude; it
tested how ONE fixed perturbation direction responds to amplitude scaling, which has a known,
provable algebraic answer independent of any curve-fitting.

**Response Matrix disposition:** Confirmed (structural, HIGH confidence, independently verified
by direct computation), Confirmed (the empirical ratio pattern was real and is now explained, not
just observed), Confirmed (R² weak-discriminator mechanism, argued rigorously on the actual
numbers). No concern is dismissible; this experiment's actual falsifiable predicate as pre-
registered ("log(M1) is approximately linear in coupling_magnitude") is mathematically false for
this construction.

**Corrected honest statement:** *On this specific sweep — one fixed random coupling direction,
dilated by scalar `coupling_magnitude ∈ {3,...,30}` — `M1` is provably bounded by a degree-≤7
polynomial (`N_DIM−1`), not exponential. The apparent "exponential" fit (R²=0.9994) is a
curve-fitting artifact of comparing functional forms on data spanning three orders of magnitude,
where a high-degree polynomial and an exponential are hard to distinguish empirically even though
they are mathematically distinct and only one is actually possible here. The genuinely open
question the pearl-registry entry asked for — "how does M1 scale with coupling strength across
DIFFERENT random matrices?" — remains untested; this experiment answered a different, narrower
question (how M1 scales under uniform dilation of ONE fixed direction) without realizing that was
the question being asked.*

**Corrected next step (supersedes the original Relaxation Map's "widen the sweep range" item,
which would not resolve this — dilating the SAME fixed direction further only extends the same
polynomial, it can't test genuine coupling-magnitude dependence):** re-run with a FRESH,
independently-seeded random matrix at EACH coupling magnitude (not `default_rng(SEED)` reset to
the same constant every call) — ideally combined with multiple seeds per level, reusing
`H-B2-1i`'s own seed-ensemble machinery, to get a real answer to the original pearl-registry
question with actual statistical power.

---

## Result (ORIGINAL TEXT, superseded by the correction above — kept for the audit trail)

**Verdict: CONFIRMED** (exponential growth), per the kill criterion in `claim.md`, evaluated
via a fair raw-space model comparison.

| Model | Fit method | R² on raw M1 |
|---|---|---|
| Linear | `np.polyfit` deg 1 (raw RSS) | 0.680 |
| Quadratic | `np.polyfit` deg 2 (raw RSS) | 0.951 |
| Exponential | `scipy.optimize.curve_fit` (raw RSS, nonlinear) | **0.9994** |

Exponential clearly dominates both alternatives (R² > 0.9, and > max(linear, quadratic)) — the
pre-registered kill criterion for CONFIRMED. Fitted form: `M1 ≈ 9.08 × exp(0.207 × coupling_magnitude)`.

`M1` at the 10 swept points (`coupling_magnitude = 3..30`, step 3):
`2.665, 10.013, 29.227, 71.605, 158.931, 334.672, 680.084, 1332.764, 2507.630, 4522.038`.

## Methodological catch — R² comparison must be same-loss, not just same-metric-name

The FIRST version of this experiment compared the exponential model's **log-space** R²
(0.985, from `log(M1) = a·coupling + b` fit by log-space least squares) directly against the
linear/quadratic models' **raw-space** R² — different target variables, different loss
functions, not a fair comparison despite both being called "R²". Caught before writing this
file (not after a wrong claim shipped) by asking whether the two numbers actually answered the
same question. Fixed by additionally fitting the exponential model via `scipy.optimize.curve_fit`
directly on raw M1 (nonlinear least squares, same loss as `polyfit` uses for linear/quadratic),
and gating the verdict on THAT comparison. Both R² values are kept in `metrics/run.json`
(`r_squared_logspace` vs `r_squared_raw_nls`) for the audit trail.

## Caveat — consecutive-ratio diagnostic shows decelerating growth rate

`M1[i+1]/M1[i]` at the fixed coupling step (Δ=3) should be **constant** for pure single-rate
exponential growth. Observed ratios instead **decrease monotonically**: 3.76, 2.92, 2.45, 2.22,
2.11, 2.03, 1.96, 1.88, 1.80 (`ratio_monotone_decreasing: true` in `metrics/run.json`). This is
a genuine, literal signal that the local growth rate is itself decreasing with coupling
magnitude — the process is not perfectly single-rate exponential, even though the raw-NLS
exponential fit still dominates both alternatives in aggregate R².

**Why this does NOT override the verdict:** the kill criterion was pre-registered in `claim.md`
as an R²-based comparison, before this run. Adding a NEW override rule (e.g. "reject if ratios
aren't constant") after seeing the data would be exactly the post-hoc goalpost-move the
project's Minimal Relaxation Rule / Anti-Overfitting Gate forbid. The ratio finding is reported
as a separate, explicit caveat instead — consistent with Perelman-audit discipline (report the
true residual pattern, don't suppress an inconvenient one).

**Why R² alone under-detects this:** with only 10 points spanning a ~1700× dynamic range
(2.66 → 4522), aggregate sum-of-squares is dominated by the largest values — a model that is
qualitatively "close to exponential but decelerating" can still score R² ≈ 0.999 in raw space,
because the deviations are small relative to the huge overall variance. The consecutive-ratio
check is a more literal, more sensitive diagnostic for this specific question (constant-ratio
growth) than R² is, on this kind of heavy-tailed data. **Tooling lesson for LEDGER:** R²
comparison between candidate functional forms should always be paired with a literal-structure
diagnostic (ratio test, residual plot) when the response variable spans orders of magnitude —
R² alone can rubber-stamp a "close enough" fit that has a real, systematic, and informative
deviation baked in.

## What Was Confirmed

- `M1` grows genuinely fast with `coupling_magnitude` — over the tested range, an exponential
  model (fit fairly, by raw nonlinear least squares) captures the shape far better than linear
  or quadratic alternatives (R²: 0.9994 vs 0.951 vs 0.680).
- The sweep's own matrix-construction (`build_matrix`) and measurement (`measure_m1`) logic is
  a faithful, verified reproduction of H-B2-1f/g's own module-level construction —
  `coupling_magnitude=3.0` reproduces H-B2-1f's `M1=2.665` to 3 decimal places, and
  `coupling_magnitude=15.0` reproduces H-B2-1g's `M1=158.93` to 2 decimal places (both via
  `provenance_check` in `metrics/run.json`), confirming no drift in RNG call order or eigenvalue
  set between this sweep and the two experiments that motivated it.

## What Remains Open

- The growth-rate deceleration itself (the consecutive-ratio finding) is not explained by this
  experiment — it could be a finite-range artifact of the specific 8-dim eigenvalue/seed
  construction, or a more general property of `||expm(t·A)||` growth under increasing random
  perturbation. A follow-up would need either a wider sweep (beyond `coupling_magnitude=30`) or
  a different seed/eigenvalue set to distinguish these.
- Per `claim.md`'s own scope limitation (§3): multiple seeds at each coupling level were NOT
  tested — this sweep uses seed=0 throughout, matching H-B2-1f/g for direct comparability. `M1`'s
  seed-to-seed variance at a fixed coupling magnitude remains a separate, untested question
  (already named in H-B2-1g's own Relaxation Map).

## Relaxation Map

- **Widen the sweep range** (e.g. `coupling_magnitude` up to 60-100) — would test whether the
  ratio-deceleration continues, plateaus, or reverses; a stronger test of whether growth is
  truly sub-exponential asymptotically or just in this finite window.
- **Multiple seeds per coupling level** — resolves H-B2-1g's own still-open question (is
  `M1=158.93` typical or an unlucky draw) and would let deceleration be checked against
  seed-to-seed noise rather than a single deterministic trajectory.
- **Different eigenvalue spectrum** — tests whether the deceleration is a property of THIS
  8-dim spectrum or more general.

## Note on Floor–Ceiling (FL Step 4a)

Not applicable in the arm/null-model sense — this is a descriptive numerical measurement of a
fully specified deterministic construction (matrix exponential norm ratio), not a detection rule
being run against a null-model floor or an oracle ceiling. There is no "mechanism-removed"
baseline to measure `M1` against; `M1` is the quantity itself, not a detector's score.

## FL Step 8a — Skeptic Pass

**Not run as a separate agent invocation this pass** — the Evaluator-Optimizer cap
(3 consecutive non-LGTM reviewer verdicts, session-wide) was still in effect from the prior B3
work when this experiment was built. In its place, the same discipline was applied manually and
is documented above: (1) the log-space-vs-raw-space R² comparison was caught and fixed BEFORE
this file was written, not after: a session self-catch matching the exact kind of thing a
context-asymmetric skeptic pass looks for; (2) the ratio-deceleration finding was surfaced and
reported rather than smoothed over; (3) provenance was independently cross-checked against both
parent experiments' own committed numbers, not asserted from memory.

**FALSIFIED-equivalent concern anticipated and pre-addressed:** "the exponential fit's high R²
is an artifact of comparing wrong-loss metrics" — this is exactly the mistake this file's own
first section documents catching and fixing. **Response: Mitigated** (raw-NLS refit).

## EstimandOps — What This Does NOT Mean (restated per claim.md)

1. Does NOT generalize beyond this specific 8-dimensional eigenvalue/seed construction.
2. Does NOT imply anything about real Neural-ODE/ResNet layers' actual coupling strengths in
   practice — a controlled numerical experiment on a toy stiff system.
3. Does NOT test multiple seeds at each coupling level — `M1=158.93`'s typicality remains open.
4. Does NOT establish that growth is *purely* single-rate exponential — the consecutive-ratio
   caveat above shows measurable deceleration; "exponential" here means "best of the three
   tested functional forms," not "exactly matches a single exponential rate."
