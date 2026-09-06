# decision.md — 20260906-chernoff-neuralode-2d-combined-stress

**Graph node:** `H-B2-1e` · **Date:** 2026-09-06

## Verdict

- [x] **PROMOTE** — the mechanism survives non-normality AND mixed-sign spectrum combined, with a
  measurable but non-catastrophic compounding effect
- [ ] REPEAT
- [ ] REJECT
- [ ] ARCHIVE

**Confirmed statement:** *The `K_j=0` mechanism survives the combination of non-normality (`H-B2-1c`)
and a mixed-sign spectrum (`H-B2-1d`), with the two complications' effects on `M1` COMPOUNDING (not
merely adding, and not cancelling), while the bound remains valid and order-matching throughout.*

## Evidence Summary

| Quantity | Non-normal alone (`H-B2-1c`) | Mixed-sign alone (`H-B2-1d`) | Combined (this experiment) |
|---|---|---|---|
| `A` normal? | No | Yes | **No** |
| Eigenvalue signs | both negative | mixed (+0.5, -2) | **mixed (+0.5, -2)** |
| `M1` | 2.563 | 1.0 (exact) | **3.806** |
| Empirical order, order-1 | 1.0004 | 0.9988 | **1.0031** |
| Empirical order, order-2 | 2.0068 | 2.0020 | **2.0040** |
| Bound holds (16 cases) | 16/16 | 16/16 | **16/16** |
| Efficiency, order-1 (constant) | 0.00298 | 0.323–0.324 | **0.000397–0.000404** |
| Efficiency, order-2 (constant) | 0.0059–0.0061 | 0.117–0.118 | **0.00180–0.00183** |

## The Compounding Is Real But Not Catastrophic

`M1=3.806` for the combination is **larger than the non-normal-alone value (2.563)**, confirming the
two complications genuinely interact (not simply "whichever is worse dominates") — the transient growth
from non-normality and the genuine exponential growth from the positive eigenvalue compound. But the
compounding is **multiplicative-ish, not explosive**: `3.806` is well within an order of magnitude of
either individual effect, not orders of magnitude worse. The bound stays valid in all 16 cases, and the
order match is exact and stable, exactly as in every other `H-B2-1*` experiment this session. This is
the informative result the experiment was designed to check for (see `claim.md`'s explicit motivation)
— and the answer is: the mechanism's graceful-degradation property extends to the combined stress case,
not just each complication in isolation.

## Kill Analysis (OSA) — for the PROMOTE verdict

### What Was Confirmed

- [x] The `K_j=0` mechanism has now survived FIVE consecutive tests in one session: 1D scalar, 2D
  symmetric-decay, 2D non-normal, 2D mixed-sign, and 2D non-normal-mixed-sign combined.
- [x] Combining two independently-confirmed complications produces a MEASURABLE but BOUNDED
  compounding effect on the bound's constant, not a breakdown.

### What Remains Open (genuinely larger undertakings, not cheap next steps)

| Assumption | Modification | Why not attempted here |
|---|---|---|
| Dimension (2D throughout) | Higher-dimensional (10D+) case | Would need a principled way to generate a "realistic" higher-dimensional non-normal, mixed-sign matrix — not a simple parameter change |
| Realistic Jacobian statistics | Random matrices matching actual trained-network Jacobian distributions | Requires literature/empirical grounding beyond what `WebSearch` summaries can provide reliably — a genuinely separate research task |
| Nonlinear dynamics | A genuinely nonlinear Neural ODE, not a linear toy | Analytically intractable — would require numerical ODE integration as the "ground truth" instead of `expm`, a materially different experimental design |

These are correctly left as OPEN, not attempted-and-failed — they represent the natural boundary of what
a single-session, analytically-tractable toy-model stress-test arc can responsibly cover.

## What This Does NOT Mean

1. Does NOT test a higher-dimensional or nonlinear case — still a 2x2 linear toy.
2. Does NOT establish that the compounding effect is always modest — tested ONE specific combination
   (`C=10`, eigenvalues `+0.5/-2`); a more extreme combination could compound worse.
3. Does NOT mean this arc has "proven" the bridge `B2-CHERNOFF-UDE` for realistic Neural-ODE/ResNet
   layers — it has built a coherent, cross-checked, honest evidence base for the mechanism's robustness
   across the specific complications tested, which is a meaningfully stronger position than the single
   1D toy `H-B2-1` started from, but is not the same as a general theorem for practical networks.

## Pearl Card Update

**New information, closing out the `H-B2-1*` arc for this session:** the `K_j=0`/Theorem 3.1 mechanism
now has five independent confirmations forming a coherent stress-test progression (scalar → symmetric →
non-normal → mixed-sign → combined), each isolating one axis of "realism" motivated either by the
theorem's own generality (Theorem 3.1 explicitly covers `dim F=∞`) or by literature on real trained
network Jacobians. This is a substantially more thorough evidence base for a Standard-Ladder bridge than
this project has built for any other single hypothesis this session, and a natural, deliberate stopping
point before the remaining next steps become genuinely separate research undertakings (see table above).
