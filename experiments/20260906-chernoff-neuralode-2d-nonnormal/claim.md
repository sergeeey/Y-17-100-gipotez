# claim.md — 20260906-chernoff-neuralode-2d-nonnormal

**Graph node:** `H-B2-1c` (new, per Minimal Relaxation Rule) · **Bridge:** `B2-CHERNOFF-UDE` · **Tier:** Standard
**Parent:** `H-B2-1b` (2D symmetric matrix case, CONFIRMED — mechanism generalizes cleanly when `A` is
orthogonally diagonalizable)

> **Role of this experiment:** Relaxation Map row 1 from `H-B2-1b`'s own decision.md: does the
> `K_j=0`/Theorem 3.1 mechanism survive when `A` is **non-normal** (not orthogonally diagonalizable),
> where `‖e^{tA}‖` can transiently exceed what the eigenvalues alone would suggest (Kreiss matrix
> theorem territory) — the regime real Neural-ODE/ResNet Jacobians are actually expected to be in, unlike
> the symmetric toy tested in `H-B2-1b`. ONE assumption changed: `A` normal → `A` non-normal (same
> eigenvalues, same block construction, same `K_j=0` argument).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `A = [[-1, c], [0, -2]]` (upper-triangular, non-normal for `c≠0`), eigenvalues `-1,-2` unchanged from `H-B2-1b`, but `A·Aᵀ ≠ Aᵀ·A` |
| **Falsifiable predicate** | The `K_j=0` mechanism (still exactly valid algebraically, since our blocks still match `e^{tA}`'s Taylor series exactly) gives a bound that (a) can still be constructed with FINITE, numerically-determined `M1, M2` despite transient growth, and (b) still matches the true empirical order, possibly with a much larger constant reflecting the transient hump |
| **Measurable outcome** | Numerically-determined `M1` (`sup‖e^{tA}‖₂` over the tested range), `M2` (`sup‖F_m(h)^k‖₂`), resulting bound vs. true empirical error, for order-1 and order-2 blocks |

## Why This Is a Real Test, Not a Formality

In `H-B2-1b`, symmetry let `M1=M2=1, w=0` work for free (`‖f(A)‖₂ = max|f(λᵢ)|` for symmetric `A`, and
both eigenvalues gave `|f_m(λh)|≤1` at the tested step sizes). For **non-normal** `A`, this shortcut is
INVALID — `‖e^{tA}‖₂` is not simply `max_i e^{λᵢt}`; it can be substantially larger at intermediate `t`
even though every eigenvalue decays (this is precisely what the Kreiss matrix theorem quantifies: the
transient growth is controlled by the *pseudospectrum*, not the spectrum alone). If `c` is large enough,
`M1` and `M2` could plausibly need to be very large, or worse, the natural `w=0` choice might fail
entirely (requiring `w>0`), which would change the ORDER of the bound's exponential prefactor even
before touching the polynomial-in-`n` part. This experiment finds out empirically whether that happens
for a moderately transient-growth-inducing `c`, rather than assuming it away.

## FL Step -4: Source Trace

- Kreiss matrix theorem: standard numerical-linear-algebra result (Kreiss 1962; see e.g. Trefethen &
  Embree, *Spectra and Pseudospectra*, 2005) characterizing transient growth of `e^{tA}` for non-normal
  `A` via the pseudospectrum, not directly quoted/re-derived here — used only as the CONCEPTUAL framing
  for why this test is non-trivial, not as a formula plugged into the computation. The computation itself
  uses only `scipy.linalg.expm` (exact numerical matrix exponential) and direct operator-norm
  measurement — no unverified quantitative Kreiss-theorem formula is used.
- Theorem 3.1 / `K_j=0` mechanism: unchanged from `H-B2-1`/`H-B2-1b`, already source-traced.

## Natural Language Statement

> "We test whether the K_j=0/Theorem 3.1 mechanism, confirmed for a symmetric 2D matrix in H-B2-1b,
> still yields a valid, order-matching bound (via numerically-determined, not assumed, M1/M2 constants)
> when A is non-normal and exhibits measurable transient growth."

## L0 Classification

**Descriptive**, unchanged from parent experiments.

## What This Does NOT Mean

1. Does NOT use or verify a quantitative Kreiss matrix theorem formula — that theorem is cited only as
   context for why non-normality matters; the actual M1/M2 constants here are measured directly, not
   derived from a Kreiss-theorem bound.
2. Does NOT test a realistic neural-network-scale Jacobian — a single 2x2 non-normal toy, chosen for
   tractability.
3. A finding that M1/M2 grow large (looser bound) does NOT kill the mechanism itself — the `K_j=0`
   algebraic argument remains valid regardless of normality; only the CONSTANT in the final bound is at
   stake, not its existence or order.

## MCID

The mechanism is "informative" here if a FINITE (M1, M2, w) triple can be found such that the resulting
bound (a) holds for all tested `n`, and (b) still shows the correct ORDER (constant efficiency across
`n`), even if the constant itself is substantially larger than in the symmetric case (`H-B2-1b`'s
0.23–0.37 range). A qualitatively different outcome — order mismatch, or no finite (M1,M2,w) findable at
reasonable magnitude — would be the informative negative result.
