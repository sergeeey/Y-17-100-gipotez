# decision.md — H-B2-1l (eigenvector conditioning κ(V) vs M1)

## CORRECTION ADDENDUM (2026-09-07, FL Step 8a skeptic pass — first one actually run all session)

**The verdict below is downgraded from CONFIRMED to WEAKENED.** The original text is kept
unedited below (Hindsight Distortion Gap discipline) with this dated correction on top, not a
silent rewrite. This is the first genuine, context-asymmetric skeptic invocation of the entire
session (Evaluator-Optimizer cap had blocked the `reviewer` agent since mid-`B3`; every CONFIRMED
verdict since then substituted manual self-review) — invoked specifically because the session's
own retrospective report flagged this as the highest-priority methodological gap.

**What the skeptic found, given only `claim.md` + `run.py` (no session history, no decision.md,
no reasoning chain):**

1. **[Dismissed]** `np.linalg.cond(V)` numerical trustworthiness — the construction is strictly
   upper-triangular, so eigenvalues are exactly the real, distinct diagonal entries; `eig`/`cond`
   behave sanely here. Not a flaw, but it clarifies WHY rho can't approach 1 even under the true
   mechanism (Trefethen–Embree is an inequality, not an equality — noted in the original text
   too, but the skeptic sharpened why this caps the seed-ensemble rho specifically).

2. **[Accepted — fatal for the "cross-population" framing]** The N-sweep population has
   `SEED=0` hard-coded (verified directly against `H-B2-1k`'s own source). Its 9 (κ(V), M1) pairs
   are **not 9 independent draws** — they are ONE deterministic curve evaluated at 9 designed
   grid points. `spearmanr`'s null hypothesis ("ranks are a random permutation of each other")
   does not apply: any quantity that is roughly monotone-in-N (`log N`, `‖A‖_F`, Henrici's
   departure-from-normality, pseudospectral abscissa) would likely post a similarly large rho
   against `M1` on this same curve, because both trend upward with `N` for structural reasons
   that have nothing specifically to do with `κ(V)`. Effective sample size for testing "does
   κ(V) explain M1" is closer to **1** (one curve), not 9. **The N-sweep leg does not corroborate
   the seed-ensemble leg** — the "consistent, cross-population support" argument that was this
   experiment's central rhetorical move does not hold as stated.

3. **[Accepted — narrows the surviving claim]** The seed-ensemble result (rho=0.453, n=30, real
   independent seeds) IS a genuine, valid finding — but rho²≈0.20 means κ(V) explains roughly
   20% of rank variance in M1, not "the mechanism." "CONFIRMED" over-read what a modest,
   partial correlation licenses. Also: `run.py`'s original verdict logic (`if seed_rho > 0 and
   n_rho > 0: CONFIRMED`) accepted ANY positive rho, looser than `claim.md`'s own pre-registered
   `|rho| < 0.2` rejection threshold — a genuine code/spec inconsistency, fixed (see below), even
   though it happened not to flip the numeric verdict on the committed data.

4. **[Documented limitation]** The two populations both anchor on `seed=0` (P1's seed=0 case and
   P2 at N=8 both use it as their reference point) — not fully statistically independent draws,
   a minor additional reason not to treat them as two separate confirmations.

**Fixed:** `run.py`'s verdict logic now implements `claim.md`'s own `|rho| >= 0.2` threshold
exactly (`classify_verdict`, regression-tested). The numeric verdict on the already-committed
data is unchanged (CONFIRMED under the code's own criterion) — the downgrade to WEAKENED is an
INTERPRETIVE correction (per the project's Skeptic Response Matrix), not a re-run with different
numbers.

**Corrected honest statement, replacing the original headline claim:** *At fixed N=8,
coupling=15, κ(V) is positively rank-correlated with M1 across 30 independent seeds (Spearman
ρ=0.453, p=0.012) — consistent with the Trefethen–Embree bound as ONE contributor to M1's
variability, explaining roughly 20% of rank variance, not the dominant driver. The N-sweep
result does NOT independently corroborate this — with seed fixed and 9 designed grid points, it
is one deterministic curve, and any monotone-in-N proxy would likely show similarly strong rank
correlation with M1 for purely structural reasons unrelated to κ(V) specifically.*

**What survives:** the seed-ensemble finding itself (κ(V) as a genuine, partial, independently-
sampled contributor to M1's seed-to-seed variability at fixed N and coupling). **What does not
survive:** the "unifies two independently-pearled findings under cross-population support"
framing — `H-B2-1k`'s own pearl entry (non-monotonicity by N) is NOT actually explained by this
experiment; that remains open, exactly as it was before this experiment ran.

**Response Matrix disposition:** Accepted (2), Accepted (3), Dismissed (1), Documented limitation
(4). No concern rises to a full kill of the surviving seed-ensemble finding.

---

## Result (ORIGINAL TEXT, superseded in interpretation by the correction above — kept for the audit trail)

**Verdict: CONFIRMED.** Eigenvector-matrix conditioning `κ(V)` is POSITIVELY correlated with `M1`
in BOTH independently-collected populations, unifying two previously-unexplained findings from
this session under one classically-motivated mechanism.

| Population | n | Spearman ρ | p-value |
|---|---|---|---|
| Seed ensemble (`H-B2-1i`'s own 30 seeds, fixed N=8, coupling=15) | 30 | **0.453** | 0.012 |
| N-sweep (`H-B2-1k`'s own 9 points, fixed coupling=15, seed=0) | 9 | **0.917** | 0.0005 |

Both statistically significant despite small samples (α=0.05), same direction as pre-registered.

## What Was Confirmed

- [x] The mechanism proposed informally in both `H-B2-1i`'s and `H-B2-1k`'s own pearl_registry
  entries ("eigenvalue clustering") has a specific, testable, classically-grounded form
  (`κ(V)`, the eigenvector matrix's condition number, per `‖exp(tA)‖ ≤ κ(V)·max_i exp(t·Re(λ_i))`
  — Trefethen & Embree's non-normal matrix theory), and it holds up under direct test on BOTH
  populations independently.
- [x] The N-sweep correlation (ρ=0.917) is remarkably strong — `κ(V)` explains the large majority
  of `H-B2-1k`'s own non-monotonic `M1(N)` curve. The specific local extrema found there (e.g.
  the 12× jump at N=16, the >6× drop at N=32) are very likely driven by `κ(V)` moving in the same
  pattern, not a separate, unexplained phenomenon.
- [x] The seed-ensemble correlation (ρ=0.453) is weaker but still significant — `κ(V)` explains
  PART of `H-B2-1i`'s own right-skewed `M1` distribution, but leaves substantial unexplained
  variance, consistent with the pre-registered expectation that `κ(V)` is "a mechanism, not
  necessarily the only one."
- [x] No new stochastic draws were needed — this experiment reused `H-B2-1i`'s and `H-B2-1k`'s
  own already-built matrices and already-committed `M1` values (provenance-verified: the
  reference seed=0 case reproduces `H-B2-1i`'s own committed `M1` exactly).

## What Remains Open

- **Why is the N-sweep correlation so much stronger than the seed-ensemble correlation?**
  (0.917 vs 0.453) Not diagnosed here. One plausible account: varying `N_DIM` at fixed spectral
  range changes how densely eigenvalues are packed into a fixed interval in a fairly systematic
  way, while varying `seed` at fixed `N_DIM=8` produces more genuinely random, less structured
  variation in eigenvalue spacing — but this is speculation, not tested.
- `κ(V)` does not fully explain either population's `M1` variation (ρ<1 in both cases) — the
  residual variance's source is unidentified.
- The classical bound this mechanism is based on is an INEQUALITY, not an equality — a strong
  correlation is expected under the mechanism but not mathematically guaranteed at any specific
  strength; this experiment establishes association, not a validated quantitative law.

## Relaxation Map

- **Regress `M1` on `κ(V)` directly** (not just rank correlation) to see whether a power-law or
  linear relationship fits either population, which would sharpen "correlated" into an actual
  quantitative account.
- **Decompose why the N-sweep and seed-ensemble correlations differ in strength** — could
  investigate by computing `κ(V)` under BOTH manipulations jointly (multi-seed AT each N_DIM),
  which would also address `H-B2-1k`'s own open single-seed-limitation caveat.
- **Test on a THIRD, independent population** — e.g. `H-B2-1h`'s own 10-point coupling-magnitude
  sweep — to see if `κ(V)` also explains the exponential-with-deceleration pattern found there.

## Note on Floor–Ceiling (FL Step 4a)

Not applicable in the arm/null-model sense — descriptive correlational analysis of two
already-computed quantities on already-collected data, not a detection rule tested against a
null-model floor.

## FL Step 8a — Skeptic Pass

Not run as a separate agent invocation (Evaluator-Optimizer cap still in effect session-wide).
Manual discipline applied: the mechanism was sharpened to a SPECIFIC, falsifiable, pre-existing
mathematical quantity (not an ad hoc post-hoc metric invented to fit the data) before running;
both populations were checked independently and reported separately (never pooled, since they
vary different things); the weaker seed-ensemble correlation is reported honestly alongside the
much stronger N-sweep one, not averaged into a single flattering number.

**Anticipated FALSIFIED-equivalent concern:** "a positive correlation between two quantities
both derived from the same matrix could be a mathematical near-tautology, not a real mechanistic
finding." **Response: Accepted as a valid framing concern, mitigated by literature grounding** —
`κ(V)` and `M1` are NOT trivially the same quantity by construction (one is a static algebraic
property of the eigendecomposition, the other is a measured dynamic transient-growth quantity
over a time integral); the relationship between them is a real, previously-established
inequality in the numerical-analysis literature (Trefethen & Embree), not invented for this
experiment — the correlation found here is empirical support for an existing theoretical
relationship holding on this specific construction family, not a novel unverified claim.

## EstimandOps — What This Does NOT Mean (restated per claim.md)

1. Does NOT establish causation — both `κ(V)` and `M1` are properties of the same matrix `A`;
   this is a mechanistic-association claim, not a causal claim.
2. Does NOT explain 100% of `M1`'s variation in either population.
3. Does NOT generalize beyond this specific construction family (one positive eigenvalue, many
   negative, random upper-triangular coupling) without further testing.
4. Statistical power is limited (n=9, n=30) — CONFIRMED here is suggestive and grounded in
   established theory, not a strong independent statistical discovery on its own.

## Pearl Card Update

**Unifies two independently-pearled, previously-unexplained observations** (`H-B2-1i`'s
right-skew, `H-B2-1k`'s non-monotonicity) under one classically-grounded mechanism, with
cross-population empirical support. This is the strongest, most theoretically-anchored
mechanistic finding of the `H-B2-1*` arc's "digging into mechanisms" phase — closes both
open pearl_registry falsifiable predictions that proposed this mechanism informally.
