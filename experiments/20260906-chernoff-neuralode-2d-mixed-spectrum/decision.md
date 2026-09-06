# decision.md — 20260906-chernoff-neuralode-2d-mixed-spectrum

**Graph node:** `H-B2-1d` · **Date:** 2026-09-06

## Verdict

- [x] **PROMOTE** — the mechanism survives a mixed-sign (growing + decaying) spectrum, with an
  exact (not merely numerical) `M1=M2=1` derivation
- [ ] REPEAT
- [ ] REJECT
- [ ] ARCHIVE

**Confirmed statement:** *The `K_j=0` mechanism gives a valid, order-matching bound even when
`‖e^{tA}‖` genuinely GROWS with `t` (driven by a positive eigenvalue), requiring `w>0` for the first
time in the `H-B2-1*` family — and for a symmetric `A`, `M1` and `M2` can be shown EXACTLY equal to 1
(not merely bounded), via the fact that a positive-argument Taylor truncation of `e^x` always
underestimates it (all series terms positive for `x>0`).*

## Evidence Summary

| Quantity | Symmetric, both-decaying (`H-B2-1b`) | Mixed-sign (this experiment) |
|---|---|---|
| Eigenvalues | -1, -2 (both decay) | **+0.5, -2 (growth + decay)** |
| `w` needed | 0 | **0.5** (first non-zero `w` in this family) |
| `M1` | 1 (by symmetry) | **1.0000000000000004** (measured — matches the EXACT value 1 predicted analytically, to machine precision) |
| `M2` | 1 | **0.9999999999999... → 1** (same, machine-precision match to the exact prediction) |
| Empirical order, order-1 | 1.0014 | **0.9988** |
| Empirical order, order-2 | 2.0032 | **2.0020** |
| Bound holds (16 cases) | 16/16 | **16/16** |
| Efficiency, order-1 (constant) | 0.305–0.308 | **0.323–0.324** |
| Efficiency, order-2 (constant) | 0.233–0.237 | **0.117–0.118** |

## Why M1=M2=1 EXACTLY Here Is Itself Informative

Unlike `H-B2-1c` (non-normal case), where `M1`/`M2` had to be measured numerically because no closed
form was available, this experiment's `M1=M2=1` is **provable in closed form**: for `x>0`, `eˣ = Σ xᵏ/k!`
has every term positive, so ANY finite truncation `f_m(x) = Σ_{k=0}^m xᵏ/k!` satisfies `f_m(x) ≤ eˣ`
exactly. Choosing `w` equal to the growing eigenvalue makes this argument apply directly to both the
semigroup (`M1`) and the finite-step propagator (`M2`). The numerical measurement (`1.0000000000000004`,
`0.9999999999999...`) is a machine-precision CONFIRMATION of an exact algebraic fact, not an
approximate empirical finding — a stronger form of verification than the other `H-B2-1*` experiments
could offer (where the symmetric-decay and non-normal cases both required either an eigenvalue-argument
shortcut or brute-force numerical search, not an exact closed-form guarantee).

## Correction Filed Against `H-B2-1c` (Found While Writing This Experiment's Bound Formula)

While deriving this experiment's `theorem_3_1_bound` function, re-derived formula (13) from Theorem 3.1
carefully and found the correct form is `M1² · M2 · t^(m+1) · e^{wt} / ((m+1)! · n^m) · ‖A^(m+1)x0‖` —
**an M1² term, not M1**, because `C_{m+1}(t) = K_{m+1}(t)e^{-wt} + M1/(m+1)!` (from Lemma 3.3's bound on
the exponential's OWN Taylor remainder) is itself multiplied by the outer `M1·M2` prefactor. `H-B2-1`
and `H-B2-1b`'s own bound functions used only a single `M1` factor — invisible there because `M1=1`
exactly in both (so `M1²=M1`), but this WAS a real formula error, and it propagated into `H-B2-1c`
(non-normal case), where `M1≈2.563 ≠ 1`. See the separate correction note filed against `H-B2-1c`'s own
decision.md — the qualitative verdict there is unaffected (the bound only gets LOOSER, which was
already comfortably satisfied), but the quoted efficiency numbers there were too optimistic by a factor
of `M1≈2.563`.

## What This Does NOT Mean

1. Does NOT test a non-normal mixed-spectrum case — deliberately kept symmetric, isolating this ONE
   question (sign mixing) from normality (already tested in `H-B2-1c`), per Minimal Relaxation Rule.
2. Does NOT use the cited ResNet/stiff-Neural-ODE literature findings quantitatively — they motivated
   the DESIGN CHOICE (test a mixed-sign spectrum) only, per `claim.md`'s explicit scope note.
3. A future experiment combining non-normality AND mixed sign (closer still to a realistic Jacobian)
   would be a genuinely new, two-assumption-changed test — not run here, would need its own experiment ID.

## Pearl Card Update

**New information:** the `K_j=0` mechanism now has FOUR consecutive confirmations in one session (1D
scalar → 2D symmetric-decay → 2D non-normal → 2D mixed-sign), the last of which is provable in exact
closed form, not merely numerically verified. This is now a genuinely robust, multiply-cross-checked
finding for bridge `B2-CHERNOFF-UDE`, not a single lucky toy case.
