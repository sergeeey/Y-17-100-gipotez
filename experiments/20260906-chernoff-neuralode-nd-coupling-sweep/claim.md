# claim.md — 20260906-chernoff-neuralode-nd-coupling-sweep

**Graph node:** `H-B2-1h` (bridge `B2-CHERNOFF-UDE`) · **Tier:** Standard
**Parent:** `H-B2-1g` (Relaxation Map: "A systematic sweep of coupling magnitude (e.g. 3, 6, 9, 12,
15...) — would characterize HOW M1 scales with coupling strength (linear? exponential?)"; pearl
registry impact 9: "arguably the most practically important finding of the whole H-B2-1* arc" — this
sweep is the direct, named follow-up).

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** This experiment characterizes a functional relationship
(`M1` as a function of `coupling_magnitude`) within a fully specified, deterministic numerical
construction — not an intervention on a system with uncertainty, and not a causal claim about
real Neural-ODE/ResNet training. It measures a mathematical quantity's scaling behavior, matching
every prior `H-B2-1*` experiment's own descriptive framing.

## Why This Sweep, Specifically

`H-B2-1f` (coupling `[-3,3]`) found `M1=2.665`. `H-B2-1g` (coupling `[-15,15]`, 5x) found
`M1=158.93` (~60x larger) — establishing that `M1` is HIGHLY coupling-sensitive, but with only 2
data points, the functional FORM of that sensitivity (linear? polynomial? exponential?) is
unknown, and unknowable from 2 points. This sweep fills that gap directly.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | `M1` (the transient-growth constant in `H-B2-1*`'s own Theorem 3.1 bound construction), measured across a systematic sweep of `coupling_magnitude` on the SAME eigenvalue set and seed as `H-B2-1f`/`H-B2-1g` |
| **Falsifiable predicate** | `log(M1)` is approximately LINEAR in `coupling_magnitude` over the tested range (i.e. `M1` grows exponentially with coupling) — the natural alternative hypotheses (linear or polynomial growth) predict a poor fit to `log(M1)` vs `coupling_magnitude` on a semi-log plot |
| **Measurable outcome** | `M1` measured at `coupling_magnitude ∈ {3, 6, 9, 12, 15, 18, 21, 24, 27, 30}` (10 points, covering and extending both prior data points at 3 and 15), fitted against linear, power-law, and exponential models; report which fits best (highest R², lowest residual) |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md`/`pearl_registry/INDEX.md`: no prior systematic coupling sweep in
this project — `H-B2-1f`/`H-B2-1g` each tested exactly ONE coupling magnitude. This is the first
sweep, directly named as the next step in the existing pearl registry entry.

## Kill Criterion (set BEFORE running)

- **CONFIRMED (exponential growth):** `log(M1)` vs `coupling_magnitude` is well-fit by a straight
  line (R² > 0.9) AND this fit is clearly better than a linear or quadratic fit of `M1` itself vs
  `coupling_magnitude` (lower residual sum of squares after accounting for parameter count) — `M1`
  grows exponentially with coupling strength.
- **REJECTED (not exponential):** a linear or polynomial model fits `M1` vs `coupling_magnitude`
  at least as well as the log-linear model — the practically important implication would be
  different (e.g. a polynomial bound on how bad the constant gets, rather than an unbounded
  exponential blowup).
- **AMBIGUOUS:** neither functional form clearly dominates over this range — would require a wider
  sweep or more seeds to resolve.

## What This Does NOT Mean

1. Does NOT generalize beyond this SPECIFIC 8-dimensional eigenvalue/seed construction — a
   different spectrum could show a different scaling law.
2. Does NOT imply anything about real Neural-ODE/ResNet layers' actual coupling strengths in
   practice — this is a controlled numerical experiment on a toy stiff system, per every prior
   `H-B2-1*` experiment's own explicit scope limitation.
3. Does NOT test multiple seeds at each coupling level (per `H-B2-1g`'s own Relaxation Map, "is
   `M1=158.93` typical or a particularly unlucky draw" remains a SEPARATE, untested question) — this
   sweep uses the same single seed (`0`) throughout, for direct comparability with `H-B2-1f`/`g`.

## MCID

The specific functional form (exponential vs. polynomial vs. linear) that best fits `M1` vs.
`coupling_magnitude` — reported via R² and residual comparison, not a binary pass/fail threshold.
