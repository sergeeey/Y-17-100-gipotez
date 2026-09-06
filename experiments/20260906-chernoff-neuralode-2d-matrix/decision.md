# decision.md — 20260906-chernoff-neuralode-2d-matrix

**Graph node:** `H-B2-1b` · **Date:** 2026-09-06

## Verdict

- [x] **PROMOTE** — the Theorem 3.1 / `K_j=0` mechanism verified in `H-B2-1`'s 1D correction
  generalizes cleanly to a genuine 2D matrix case with two distinct eigenvalues
- [ ] REPEAT
- [ ] REJECT
- [ ] ARCHIVE

**Confirmed statement:** *The same mechanism that gave a tight, order-matching bound for the 1D case
(Theorem 3.1 applied with the legitimate `K_j=0` choice, valid because the polynomial block matches
`e^{tA}`'s Taylor series exactly to order `m`) also gives a tight, order-matching bound for a 2D
symmetric matrix `A` with two distinct eigenvalues, at the SAME step sizes used in the 1D test.*

## Evidence Summary

| Block | `m` | Empirical order | Bound holds (8/8 `n`) | Efficiency (constant across `n`) | M2 condition holds for BOTH eigenvalues (8/8 `n`) |
|---|---|---|---|---|---|
| order-1 | 1 | **1.0014** | ✅ | 0.305–0.308 | ✅ |
| order-2 | 2 | **2.0032** | ✅ | 0.233–0.237 | ✅ |

Both empirical orders match `m` exactly (not `m-1`), matching `H-B2-1`'s 1D finding. The efficiency
ratio is **constant as `n` grows** for both blocks (drifting by <2% across an 128x range of `n`,
50→6400) — the same signature of an exact order match found in the 1D case, now confirmed in 2D.

## Why the M2-Condition Check Mattered (Not a Foregone Conclusion)

`claim.md` explicitly flagged the risk: the faster eigenvalue (`λ₂=-2`) requires the step size condition
`|1+λh|≤1` (order-1) or `|1+λh+(λh)²/2|≤1` (order-2) to hold at HALF the step size the slower eigenvalue
(`λ₁=-1`) would need, since its "natural" scale is `1/|λ|`. **The check confirmed the condition holds
at every tested `n` (even the coarsest, `n=50`, giving `h=1/50=0.02`)** — the fastest eigenvalue's
stricter requirement was NOT violated in this test range. This was not guaranteed in advance; a faster
eigenvalue or a smaller `n` range could plausibly have broken the `M2` condition at small `n`, which
would have shown the mechanism is step-size-sensitive to the WORST (fastest) eigenvalue in a way the 1D
test could never reveal. That this risk didn't materialize here is itself part of the result, not a
foregone conclusion baked into the design — the same test with, say, `λ₂=-20` or `n=10` could show a
different picture (a natural, well-motivated next step if this bridge is pursued further).

## Kill Analysis (OSA) — for the PROMOTE verdict, what remains open

### What Was Confirmed

- [x] The `K_j=0` legitimate-choice mechanism (exact polynomial Taylor-truncation blocks) generalizes
  from 1D to a genuine 2D matrix case without modification to the core argument.
- [x] The bound's ORDER (not just its validity) matches the true empirical order exactly, with a
  reasonable, stable constant — not merely "holds trivially by being enormous."

### What Remains Open (Relaxation Map for further generalization)

| Assumption | Modification | New Path | Cheapest test |
|---|---|---|---|
| Symmetric `A` (orthogonally diagonalizable) | Non-normal `A` (e.g. a Jordan-block-like matrix with transient growth) | Test whether the mechanism survives when `‖e^{tA}‖` is NOT simply `e^{λ_max t}` (non-normal matrices can have `‖e^{tA}‖ ≫ e^{λ_max t}` transiently — the Kreiss matrix theorem territory) | Pick a simple 2x2 non-normal matrix with known transient growth; recompute `M1` via the actual sup norm, not the eigenvalue shortcut |
| Eigenvalue ratio (2:1 tested here) | Wider ratio (e.g. 1:10 or 1:100, closer to realistic ill-conditioned neural network Jacobians) | Test whether the M2 condition survives at practical step sizes when eigenvalues are far apart | Same code, just change `EIGENVALUES` |
| Dimension (2D tested here) | Higher dimension (e.g. 10D or 50D, closer to realistic layer widths) | Test whether the mechanism's bound and M2 condition scale reasonably, not exponentially worse, with dimension | Same code, generalize `P` to a random orthogonal matrix via QR decomposition |

None of these is required to accept THIS experiment's own conclusion (the mechanism generalizes to a
basic 2D case) — they are natural next steps if the bridge `B2-CHERNOFF-UDE` is pursued toward a
genuinely publishable multi-dimensional result, closer to what real Neural-ODE/ResNet layers look like
(non-normal, wide-eigenvalue-spread, high-dimensional).

## What This Does NOT Mean

1. Does NOT test a non-normal matrix — deliberately restricted to symmetric `A` to keep the norm
   analysis exact; non-normality is a materially different regime (transient growth) not covered.
2. Does NOT test a realistic neural-network-scale dimension or eigenvalue spread.
3. Does NOT prove the mechanism generalizes to ALL multi-dimensional cases — confirms it survives the
   simplest genuine (non-1D-reducible-in-spirit) generalization tested.
4. Does NOT change `H-B2-1`'s own verdict (`confirmed`) — this is an independent, additional data point
   supporting the same underlying mechanism, not a re-test of the 1D case.

## Pearl Card Update

**New information:** the `K_j=0` / Theorem 3.1 mechanism is not a 1D-only curiosity — it generalizes
cleanly to a basic multi-dimensional case, with the multi-dimensional M2 condition (checked
per-eigenvalue, not just for the dominant one) surviving at the SAME step sizes that worked in 1D. This
strengthens the case that `H-B2-1`'s correction reflects something real about Theorem 3.1's mechanism,
not an artifact of the 1D toy's simplicity.
