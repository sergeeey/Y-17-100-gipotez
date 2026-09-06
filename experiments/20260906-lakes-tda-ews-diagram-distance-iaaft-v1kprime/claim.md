# claim.md — 20260906-lakes-tda-ews-diagram-distance-iaaft-v1kprime

**Graph node:** `H-B3-1k` (new) · **Bridge:** `B3-MAY-TDA` · **Tier:** Standard
**Parent:** `H-B3-1j` (diagram-distance + AR(1)) and `H-B3-1i` (total-persistence + IAAFT). This
experiment fills the FOURTH and last cell of the enlarged 2×2 design:
`{total persistence, diagram-distance} × {AR(1), IAAFT}` — the first two cells (total-persistence
axis) were filled by `H-B3-1g`/`H-B3-1i`; the third (diagram-distance + AR(1)) by `H-B3-1j`; this is
the fourth.

> **Role of this experiment:** directly tests the pearl registry's own pre-registered prediction
> (`pearl_registry/INDEX.md`, 2026-09-06, H-B3-1j entry): *"Если запустить IAAFT+diagram-distance ...
> лид Peter doSat развернётся в отрицательный (как под IAAFT+total-persistence), подтверждая
> null-модель, а не статистику, как драйвер разворота"* — i.e. IF the sign-flip discovered in
> `H-B3-1i` is a NULL-MODEL effect (spiky IAAFT threshold curve, per `H-B3-1i`'s own mechanism
> diagnostic) rather than a statistic-family effect, THEN Peter doSat's lead should flip negative
> here too, mirroring `H-B3-1i` rather than `H-B3-1j`/`H-B3-1g`. ONE assumption changed from
> `H-B3-1j`: null model AR(1) → IAAFT (already validated as a mechanism against entropy in `H-B3-1d`
> and against total persistence in `H-B3-1i`).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 9 series as `H-B3-1c`–`j` |
| **Falsifiable predicate** | Peter doSat's TDA lead under IAAFT+diagram-distance is NEGATIVE (matching `H-B3-1i`'s -74d sign, not `H-B3-1g`/`H-B3-1j`'s positive +11–13d) |
| **Measurable outcome** | Sign of Peter doSat's `tda_lead` in `metrics/run.json`; false-positive rate and series set for completeness |

## FL Step -3: Novelty / Prior-Art Check

`grep` of `null_results/INDEX.md` and `pearl_registry/INDEX.md`: no prior attempt combined IAAFT
with diagram-distance — this is the one untested cell of the 2×2 design explicitly named as the
next step in both `H-B3-1i`'s and `H-B3-1j`'s own decision.md files.

## Natural Language Statement

> "We test whether Peter doSat's TDA-lead sign, positive under both statistic families tested
> against AR(1) (total persistence +13d, diagram-distance +11d) and negative under the one IAAFT
> variant tested so far (total persistence, -74d), is determined by the NULL MODEL (predicting
> negative here) or by some interaction specific to total persistence (predicting positive here)."

## L0 Classification

**Predictive** — a genuine, sharply falsifiable prediction is pre-registered above (sign, not just
direction of trend).

## Kill Criterion (set BEFORE running — a genuine two-sided test, not a one-sided PROMOTE/REJECT bar)

- **NULL-MODEL HYPOTHESIS CONFIRMED:** Peter doSat's lead is negative (matches `H-B3-1i`'s sign,
  regardless of magnitude).
- **NULL-MODEL HYPOTHESIS FALSIFIED:** Peter doSat's lead is positive (matches `H-B3-1g`/`H-B3-1j`'s
  sign) — would mean the sign-flip is specific to the total-persistence+IAAFT combination alone, not
  a general null-model effect, and the "spiky IAAFT threshold" mechanism from `H-B3-1i` would need to
  be re-examined for why it did NOT reproduce here.
- **Separately, standard FP-rate bar still applies for the bridge's own PROMOTE bar:** FP ≤ 1/5 with
  ≥1 surviving lead for PROMOTE (not expected to be met, based on every prior variant's 4/5, but
  checked for completeness).

## What This Does NOT Mean

1. A negative result (hypothesis confirmed) does not explain WHY IAAFT's null-threshold curve is
   spikier — that mechanism (from `H-B3-1i`) is assumed, not re-derived here.
2. A positive result (hypothesis falsified) would not automatically mean the statistic family drives
   the sign either — with only 2×2=4 data points total, either outcome updates a hypothesis formed
   from 3 points, not proves a law. Either way this is the last cell of THIS specific 2×2 design;
   further generalization would need a different population or a fifth statistic/null-model pairing.

## MCID

Not a PROMOTE/REJECT experiment in the usual sense — the MCID here is simply: does Peter doSat's
lead sign match H-B3-1i (confirming the null-model hypothesis) or H-B3-1g/H-B3-1j (falsifying it)?
Any result answers the question; there is no ambiguous middle ground for the sign itself.
