# decision.md — 20260906-chernoff-neuralode-nd-stiff

**Graph node:** `H-B2-1f` · **Date:** 2026-09-06

## Verdict

- [x] **PROMOTE** — the mechanism survives scaling from N=2 to N=8, with a non-obvious finding: M1
  did NOT grow with dimension in this construction
- [ ] REPEAT / REJECT / ARCHIVE

**Confirmed statement:** *The `K_j=0` mechanism, confirmed at N=2 through five stress tests
(`H-B2-1`-`H-B2-1e`), still gives a valid, order-matching bound at N=8, with a widely-separated
("stiff"), non-normal, mixed-sign 8x8 matrix.*

## Evidence Summary

| Quantity | N=2 combined (`H-B2-1e`) | N=8 (this experiment) |
|---|---|---|
| Eigenvalues | +0.5, -2 | **+0.5, -1, -2, -3, -4, -5, -6, -8** (widely separated, "stiff") |
| `A` normal? | No | **No** |
| `M1` | 3.806 | **2.665 — SMALLER, despite 4x the dimension** |
| Empirical order, order-1 | 1.0031 | **1.0022** |
| Empirical order, order-2 | 2.0040 | **2.0066** |
| Bound holds (16 cases) | 16/16 | **16/16** |
| Efficiency, order-1 (constant) | 0.000397–0.000404 | **0.00073** (constant; looser than N=2, but from `‖A³x0‖` growing with N, not from M1) |
| Efficiency, order-2 (constant) | 0.00180–0.00183 | **0.000212–0.000219** (constant) |

## The Non-Obvious Finding: M1 Did Not Grow With Dimension Here

A naive expectation (stated explicitly in `claim.md` as the thing being tested) was that higher
dimension might make transient growth WORSE — more room for non-normal interactions to compound. That
did NOT happen for this specific construction: `M1` at N=8 (`2.665`) is actually SMALLER than at N=2
(`3.806`). The efficiency numbers ARE looser at N=8, but this traces to `‖A^(m+1)x0‖` growing with
dimension (more terms contributing to the matrix-power norm), not to `M1`/`M2` themselves. This is a
genuinely informative, non-obvious result: **dimension alone does not straightforwardly worsen the
transient-growth constant** for this class of construction — the compounding seen in `H-B2-1e`
(combining non-normality with growth) was NOT further compounded by adding more (mostly fast-decaying)
dimensions in this specific random-coupling setup. This should not be over-generalized (see Kill
Analysis) — it depends on the specific coupling magnitude and eigenvalue distribution chosen.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] The mechanism holds at N=8, sixth consecutive confirmation.
- [x] Dimension scaling, AT LEAST for this specific construction (widely-separated eigenvalues,
  moderate random coupling), does not by itself worsen the `M1`/`M2` constants.

### What Remains Open
| Assumption | Modification | Why not attempted here |
|---|---|---|
| Coupling magnitude fixed at `[-3,3]` uniform | Larger coupling magnitude at N=8 (e.g. `[-10,10]`) | Would test whether the N=2 compounding pattern (`H-B2-1e`) reappears with stronger coupling at higher N — cheap, same code, next natural step |
| N=8 still far from realistic layer width | N=50-100+ | Would need to verify numerical stability of `expm`/`matrix_power` at that scale — a real, if modest, engineering concern, not just a parameter change |
| Random coupling seed=0 only | Multiple seeds | Single seed could be lucky; a distribution over seeds would characterize typical vs. worst-case M1 growth with N |

## What This Does NOT Mean

1. Does NOT establish that M1 NEVER grows with dimension — only that it didn't for this ONE
   construction (fixed eigenvalues, fixed coupling scale, one random seed).
2. Does NOT reach realistic neural-network scale (N=8 vs. typical hundreds-to-thousands).
3. Does NOT mean the mechanism is dimension-independent in general — a genuinely different coupling
   structure or eigenvalue distribution could behave differently; this is one data point, not a proof.

## Pearl Card Update

**New information:** sixth consecutive confirmation of the `K_j=0` mechanism, and the first to show a
COUNTERINTUITIVE result (M1 not increasing with dimension) rather than a confirmed expectation — a
reminder that "more complex/higher-dimensional = worse constant" is an intuition to verify, not assume,
consistent with this project's broader discipline of measuring rather than presuming.
