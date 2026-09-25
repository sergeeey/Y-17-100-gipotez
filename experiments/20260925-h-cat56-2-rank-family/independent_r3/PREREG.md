# Independent-code check of the r = 3 certificate (d = 23, s = 12), pre-registered 2026-09-25 before the implementer starts

Question type (EstimandOps L0): descriptive / existence check of an implementation, no causal layer.

## Purpose
`experiments/20260919-pcc-generic-quasipure-cat56-2/fp_certify.py` (my code, same author as the claim) reports for d=23, r=3, s=12:
PCC, SLD equation and nonsingular QFIM hold mod p and dim V-perp = 22 < 23 on two primes. This check asks whether a **from-scratch
implementation by a party that never saw that code or its outputs** reproduces the same object. It raises implementation independence
for r = 3; it does NOT raise author independence beyond "a different model instance briefed by me", and it produces no Q(i) instance.

## Blindness (Builder Blindness Rule)
The implementer gets the DEFINITIONS and the acceptance criteria below. It does NOT get: the expected value 22, the r = 2 numbers, any file
of `20260919-pcc-generic-quasipure-cat56-2/` (`fp_certify.py`, `exact_certify.py`, `h2_core.py`, `h2_ext.py`, `pcc_core.py`, `metrics/`),
`20260920-*`, or the outreach bundle. A blind positive control (d=8, r=2, s=5, whose saved answer only I know) is added for calibration.

## Pass / fail (fixed now)
- **PASS**: for d=23, r=3, s=12, on two primes NOT in {67108837, 67108777} and two seeds each, every exact identity holds (SLD equation, PCC on the full
  23x23 commutators, QFIM by the full-matrix formula nonsingular) and the reported `dim V-perp` is the same integer in all four runs; and the float
  (complex128, SVD with a reported singular-value gap) run gives the same integer; and the three negative controls are detected; and the blind
  positive control (8,2,5) equals my saved value.
- **DISCREPANCY**: the implementer's integer differs from mine (22). Then neither number is trusted until the difference is explained; no status change,
  no claim about which side is wrong.
- **FAIL / INCONCLUSIVE**: any exact identity fails, negative controls not detected, the four runs disagree with each other, or no rank gap in float.
  Not evidence against or for the claim; fix the implementation or report the obstacle.
- Evidence label of a PASS: `[VERIFIED-independent-implementation, same-briefing-author]`, at most Medium on the independence ladder
  (different model instance, different code, same briefing). Not `U3`.

## What this does NOT show
Not an explicit Q(i) point (existence still goes through the lifting lemma, unreviewed); not novelty; not independence of the definitions themselves
(both sides use the definitions I wrote down from arXiv:2601.21801); nothing about r = 4, 5.
