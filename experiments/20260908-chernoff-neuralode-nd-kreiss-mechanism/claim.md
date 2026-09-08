# claim.md — 20260908-chernoff-neuralode-nd-kreiss-mechanism

**Graph node:** `H-B2-1u` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard (reuses existing,
already-verified pipeline pieces; adds one new quantity — a multi-`eps` Kreiss constant
estimate — and one new, closely-related transient-growth measurement)
**Parent:** `H-B2-1t` (pseudospectral abscissa CONFIRMED at N=40,50 on THREE independent data
sources: own seeds, independent implementation, fully fresh seeds. User's own Priority 3, gated
on Priority 2 passing: move from correlation to mechanistic explanation.)

## Why This Experiment, Specifically — User's Own Priority 3 Framing, Verbatim

> Не очередной sweep, а попытка понять почему:
> pseudospectrum → resolvent amplification → transient growth → Chernoff bound constant M1
> То есть перейти от корреляции к механистическому объяснению.

**What "mechanistic" means here, made concrete and falsifiable (not hand-waving):** the chain
the user names is not a metaphor — it is the **Kreiss Matrix Theorem**, a PROVEN result (not an
empirical hypothesis) already cited as the theoretical grounding for pseudospectral abscissa
since `H-B2-1r`'s own claim.md. The theorem states, for the Kreiss constant
`K(A) = sup_{eps>0} (alpha_eps(A) - alpha(A)) / eps`:

```
K(A)  <=  sup_{t>=0} ||exp(tA)||  <=  e * n * K(A)
```

Every prior experiment in this arc tested pseudospectral abscissa **at a single fixed
`eps=1`** and correlated it with M1 — real, valuable evidence, but indirect: a correlation, not
a direct test of the theorem's own inequality. This experiment computes the actual quantities
the theorem is ABOUT (`K(A)`, estimated via a genuine supremum over multiple `eps` values, and
the raw transient-growth quantity `sup_t ||exp(tA)||`, not M1's `w`-normalized variant) and
checks the inequality directly on real matrices from this arc's own population. **Per Gate 4
(Scientism Detection) of this project's own artifact-provenance-gates.md: citing "the Kreiss
Matrix Theorem" without ever computing the actual numbers for THIS case is exactly the failure
mode that gate exists to catch — this experiment is the fix.**

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Does a proven mathematical inequality hold on real computed
data, and how tight is it (an efficiency ratio, informative about how much of the observed
transient growth the Kreiss mechanism alone explains vs. residual slack)? No causal framing.

## FL Step 0a — Mechanism Claim Gate

**This is the unusual case where the "mechanism claim" IS a proven theorem, not an empirical
behavioral sentence about a specific test/statistic — same status as every prior theoretical
grounding in this arc (Trefethen-Embree for `kappa(V)`, Bendixson for `omega(A)`).** No Step 0a
synthetic-counter-example check is required for the theorem itself. What DOES need verification
(and is the actual content of this experiment): whether THIS PROJECT'S OWN COMPUTATIONS of the
two quantities the theorem relates (`alpha_eps(A)` via the already-verified grid search;
`sup_t||exp(tA)||` via a new, closely-related variant of `measure_m1`) are internally consistent
with each other — i.e., a correctness check on the arc's own code, using the theorem as the
verification oracle, in the same spirit as `H-B2-1r`'s own positive-control tests.

**Honest scope-limiting caveat, stated BEFORE running (not discovered after):** the theorem's
`sup_{t>=0}` is over ALL non-negative `t`; this arc's own `T_MAX=1.0` convention (used
throughout, unchanged here) only searches `t` in `(0, 1]`. The UPPER bound
(`observed <= e*n*K(A)`) is still mathematically guaranteed to hold even restricted to this
sub-interval (restricting the domain of a max can only decrease or preserve it, never violate an
upper bound valid for the full domain). The LOWER bound (`K(A) <= observed`) is NOT guaranteed
to hold on the restricted interval if the true growth peak occurs after `t=1` — a violation of
the lower bound specifically would be informative about `T_MAX=1.0`'s adequacy as a time window,
not necessarily a bug. This distinction is checked and reported separately, not conflated.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `(K_estimate(A), raw_transient_growth(A))` pairs at `N_DIM` in {40, 50} (matching the arc's established "primary large-N regime"), on 10 seeds per slice reusing `H-B2-1t`'s own fresh seed range (300-309, the first 10 of the 40 already used there — same deterministic matrices, no new randomness) |
| **Falsifiable predicate** | The proven upper bound `raw_transient_growth(A) <= e * n * K_estimate(A)` holds for EVERY sampled matrix. A violation would be a genuine, serious finding: either a bug in `pseudospectral_abscissa` (reused unchanged from `H-B2-1r`, already twice independently verified) or in the new `raw_transient_growth` routine — informative regardless of which |
| **Measurable outcome** | Per-matrix: `K_estimate(A)`, `raw_transient_growth(A)`, `e*n*K_estimate(A)` (the ceiling), whether the upper bound holds, whether the lower bound holds (diagnostic only, not part of the kill criterion per the honest caveat above), and the "efficiency" ratio `raw_transient_growth / (e*n*K_estimate)` — the actual mechanistic insight: how much of the ceiling the observed growth reaches |

## FL Step -3: Novelty Check

`grep` of `pearl_registry/INDEX.md`: no prior computation of a multi-`eps` Kreiss constant
estimate or the raw (non-`w`-normalized) transient growth quantity anywhere in this arc — every
prior experiment used a single fixed `eps=1` and the `w`-normalized `measure_m1`. Confirmed
novel.

## Kill Criterion (set BEFORE running)

- **Upper bound holds for all matrices (expected, mathematically required if code is correct):**
  no verdict in the usual CONFIRMED/REJECTED sense — a proven theorem cannot be "confirmed" by
  data, only have its COMPUTATION verified. If it holds for all sampled matrices, this is
  evidence the arc's own `alpha_eps`/transient-growth computations are mutually consistent
  (a correctness cross-check), and the efficiency ratios are reported as the substantive
  mechanistic finding.
- **Upper bound VIOLATED for any matrix:** this is the actual falsifiable, serious outcome — it
  would mean a real bug exists in this arc's core computations (not a "the hypothesis was
  wrong" result, since the theorem is proven). Requires immediate investigation, not a normal
  REJECT/`hard_killed` classification.

## What This Does NOT Mean

1. Does NOT retroactively change any prior verdict in this arc.
2. A clean upper-bound-holds result does NOT "prove" pseudospectral abscissa is the SOLE
   mechanism — the efficiency ratio (how tight the bound is) is the actual informative content;
   a very loose bound (efficiency near 0) would mean the Kreiss mechanism, while mathematically
   valid, leaves most of the observed variance unexplained by this specific inequality, pointing
   to residual structure not captured by `K(A)` alone.
3. Does NOT establish causality — this is a mathematical inequality check, not an intervention.
4. A lower-bound violation (if it occurs) does NOT indicate a bug — see the honest T_MAX caveat
   above, checked and reported as a separate, non-alarming diagnostic.

## MCID

Per-matrix efficiency ratio (`raw_transient_growth / (e*n*K_estimate)`), reported as a
distribution across the 20 sampled matrices (10 seeds x 2 N_DIM values), alongside a binary
pass/fail on the upper-bound check (which must be 20/20 if the arc's own code is correct).
