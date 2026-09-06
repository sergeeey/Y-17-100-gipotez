# decision.md — 20260906-chernoff-neuralode-nd-strong-coupling

**Graph node:** `H-B2-1g` · **Date:** 2026-09-06

## Verdict

- [x] **PROMOTE** — the mechanism remains formally valid and order-matching even under severe
  compounding, but the bound becomes practically vacuous (a distinct, important finding)
- [ ] REPEAT / REJECT / ARCHIVE

**Confirmed statement:** *H-B2-1f's counterintuitive finding (M1 smaller at N=8 than at N=2) was
coupling-strength-dependent, not a general property: at 5x the coupling magnitude, M1 grows
dramatically (from 2.665 to 158.93, ~60x) — confirming compounding CAN be severe. The bound remains
VALID (holds in all 16 cases) and ORDER-MATCHING throughout, but becomes practically useless as a
predictive tool (efficiency ~1.5e-7 — the bound is ~7 million times larger than the true error).*

## Evidence Summary

| Quantity | H-B2-1f (weak coupling, `[-3,3]`) | This experiment (strong coupling, `[-15,15]`) |
|---|---|---|
| `M1` | 2.665 | **158.93 — ~60x larger** |
| Empirical order, order-1 | 1.0022 | **1.0026** |
| Empirical order, order-2 | 2.0066 | **2.0007** |
| Bound holds (16 cases) | 16/16 | **16/16** |
| Efficiency, order-1 (constant) | 0.00073 | **~1.5e-7** (constant, but bound now ~7,000,000x looser than the true error) |

## The Key Distinction This Experiment Establishes: Valid ≠ Useful

Every `H-B2-1*` experiment this session asked "does the bound hold, and does its order match?" This is
the first to show these two questions can BOTH answer "yes" while the bound is **practically useless**
as an error estimate — off by 7 orders of magnitude from the truth. This is not a failure of the
mechanism (the algebraic argument, `K_j=0`, remains exactly as valid as ever) — it is a demonstration
that **a mathematically valid, order-correct bound can still be operationally meaningless** if the
constant (`M1²`, driven by transient growth under strong coupling) is large enough. For a real
Neural-ODE/ResNet application, this would matter enormously: knowing the bound "holds" would offer no
practical guidance if `M1` is this large — a user would need the ACTUAL constant, not just the
asymptotic order, to decide whether the guarantee is useful for their step-size choice.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] `H-B2-1f`'s finding was coupling-dependent, not universal — resolved cleanly, not contradicted.
- [x] The mechanism's validity (bound holds, order matches) is UNCONDITIONAL on coupling strength in
  this construction — even at extreme compounding, it never breaks.
- [x] **New, important distinction:** validity and practical usefulness are separate axes; this session's
  earlier "efficiency" numbers (all reasonably informative, 0.0002–0.37) should not be read as implying
  the bound is ALWAYS reasonably tight — it can become arbitrarily loose while remaining valid.

### What Remains Open
| Assumption | Modification | Note |
|---|---|---|
| Single coupling magnitude tested at each of two levels | A systematic sweep of coupling magnitude (e.g. 3, 6, 9, 12, 15...) | Would characterize HOW M1 scales with coupling strength (linear? exponential?) — informative for understanding when the bound becomes impractical |
| Single seed | Multiple seeds at strong coupling | Would show whether `M1=158.93` is typical or a particularly unlucky draw |

## What This Does NOT Mean

1. Does NOT mean the `K_j=0` mechanism is "broken" at strong coupling — it is exactly as valid as at
   weak coupling; only the CONSTANT is enormous.
2. Does NOT mean Theorem 3.1 is impractical for real Neural-ODE/ResNet layers in general — it means
   that FOR THIS SPECIFIC toy construction with this specific (large) coupling, the guarantee, while
   true, would not usefully inform a practitioner's step-size choice.
3. Does NOT invalidate any earlier `H-B2-1*` result — each was scoped to its own tested parameters and
   remains correct as stated.

## Pearl Card Update

**New information, arguably the most practically important finding of the whole `H-B2-1*` arc:** a
formally valid, order-matching Chernoff-type bound can still be practically useless if its constant is
large — "the theorem applies" and "the theorem is useful" are different claims, and this session's
earlier experiments (which all happened to land in a "reasonably tight" regime, efficiency 0.0002–0.37)
could have created a false impression that Theorem 3.1's bounds are generally tight. This experiment
shows that impression was an artifact of the specific parameters tested, not a general property —
worth flagging explicitly for anyone using this `H-B2-1*` arc as evidence for `B2-CHERNOFF-UDE`'s
practical value: the mechanism's mathematical validity is robust; its PRACTICAL USEFULNESS is not,
and depends sharply on the specific matrix's transient-growth properties.
