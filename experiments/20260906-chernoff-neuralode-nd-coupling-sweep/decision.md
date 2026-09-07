# decision.md — H-B2-1h (coupling-magnitude sweep of M1)

## Result

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
