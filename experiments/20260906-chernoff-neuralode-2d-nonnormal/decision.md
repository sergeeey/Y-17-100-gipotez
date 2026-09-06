# decision.md — 20260906-chernoff-neuralode-2d-nonnormal

**Graph node:** `H-B2-1c` · **Date:** 2026-09-06

## Verdict

- [x] **PROMOTE** — the Theorem 3.1 / `K_j=0` mechanism survives non-normality, with honestly
  measured (not assumed) `M1`/`M2` constants
- [ ] REPEAT
- [ ] REJECT
- [ ] ARCHIVE

**Confirmed statement:** *The `K_j=0` mechanism (H-B2-1, generalized to matrices in H-B2-1b) still
gives a valid, order-matching bound for a non-normal `A` with measurable transient growth, when `M1`
and `M2` are measured directly (via `scipy.linalg.expm` and matrix powers) rather than assumed to be 1.*

## Evidence Summary

| Quantity | Symmetric case (`H-B2-1b`) | Non-normal case (this experiment) |
|---|---|---|
| `A` normal? | Yes (orthogonally diagonalizable) | **No** — confirmed via `A@Aᵀ ≠ Aᵀ@A` |
| `M1` (`sup‖e^{tA}‖₂`) | 1 (assumed, valid by symmetry) | **2.563** (measured — genuine transient growth, ~2.56x the eigenvalue-only prediction) |
| `M2` (`sup‖F(h)^k‖₂`) | 1 (assumed, valid by symmetry) | **~2.56–2.60** (measured, stable across `n`) |
| Empirical order, order-1 block | 1.0014 | **1.0004** |
| Empirical order, order-2 block | 2.0032 | **2.0068** |
| Bound holds (16 tested cases) | 16/16 | **16/16** |
| Efficiency (order-1, constant across `n`) | 0.305–0.308 | **0.0076** (constant, ~40x looser) |
| Efficiency (order-2, constant across `n`) | 0.233–0.237 | **0.0151** (constant, ~16x looser) |

Both empirical orders match `m` exactly (not `m-1`), exactly as in the symmetric case. The bound holds
in every single tested case. The efficiency is **substantially lower** (bound is looser) than the
symmetric case, but crucially **still constant across `n`** — the signature of an exact order match
surviving even though the constant grew.

## Why the Looser Constant Is the Expected, Honest Result — Not a Weakness

Two independent effects both push the bound up here, and both are genuine, not analysis artifacts:

1. **Transient growth** (`M1, M2 ≈ 2.56` instead of 1) — exactly what Kreiss matrix theorem territory
   predicts for a non-normal matrix: `‖e^{tA}‖` can exceed what the eigenvalues alone would suggest, for
   intermediate `t`. Measured directly, not derived from an unverified quantitative Kreiss-theorem
   formula (per `claim.md`'s explicit scope limit).
2. **Larger `‖Aᵐ⁺¹x0‖`** (29.3 for order-1's `m+1=2`, 69.5 for order-2's `m+1=3`, vs 1.74/2.51 in the
   symmetric case) — the large off-diagonal coupling (`C=10`) directly inflates matrix powers,
   independent of the transient-growth question.

**Neither effect broke the mechanism** — the bound remained valid (never violated) and order-matching
(constant efficiency) throughout. A looser bound with correct order is exactly what should happen when
the mechanism is applied honestly to a harder case; a bound that either failed to hold, or held with a
DRIFTING (not constant) efficiency, would have been the informative negative result. Neither occurred.

## Kill Analysis (OSA) — for the PROMOTE verdict

### What Was Confirmed

- [x] The `K_j=0` algebraic argument (blocks match `e^{tA}`'s Taylor series exactly) is unaffected by
  normality — it's a purely algebraic fact about the block construction, not a spectral property.
- [x] `M1`/`M2` CAN be measured honestly (not assumed) for a non-normal matrix without the bound
  becoming vacuous or invalid — the mechanism degrades gracefully (looser constant), not catastrophically.

### What Remains Open

| Assumption | Modification | Cheapest test |
|---|---|---|
| Coupling magnitude (`C=10` tested here) | Much larger `C` (e.g. 100), pushing `M1/M2` further from 1 | Same code, change `C`; check if bound still holds or if numerical/theoretical limits are hit |
| Dimension (2D tested) | Higher-dimensional non-normal case (e.g. a larger Jordan-block-like structure) | New experiment, moderate scope |
| Realistic NN Jacobian structure | Random non-normal matrices matching typical trained-network Jacobian statistics | Requires literature/empirical grounding of what such Jacobians actually look like — a materially larger undertaking, not a cheap next step |

## What This Does NOT Mean

1. Does NOT use or validate a quantitative Kreiss matrix theorem formula — `M1`/`M2` were measured
   directly by brute-force numerical search over a grid, per `claim.md`'s stated scope.
2. Does NOT test a realistic neural-network-scale non-normal Jacobian — a single, deliberately simple
   2x2 toy with one tunable coupling parameter.
3. Does NOT mean the bound is "tight" in this case (efficiency 0.008–0.015 means the true error is only
   ~1% of the bound) — it means the bound is VALID and ORDER-CORRECT, not that its constant is optimal.
   A tighter non-normal-aware theorem (accounting for the actual pseudospectrum) might exist and do
   better; not sought here.

## Pearl Card Update

**New information:** across three consecutive generalizations of the SAME `K_j=0` mechanism (1D scalar
→ 2D symmetric matrix → 2D non-normal matrix), the mechanism has held every time, with the ONLY casualty
being the tightness of the constant (not the validity or the order). This is a genuinely reassuring
robustness pattern for `B2-CHERNOFF-UDE` — worth noting as a bridge status update, not just a per-experiment
pearl: the underlying idea (Chernoff's product-formula apparatus, applied via its strongest available
theorem, gives real, order-correct, if not always tight, bounds on ResNet/Neural-ODE-style discretization
error) has now survived three independent stress tests in one session.
