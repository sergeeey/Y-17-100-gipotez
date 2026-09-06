# claim.md — 20260906-lakes-tda-ews-descriptive-v3

**Graph node:** `H-B3-1f` (new, per Minimal Relaxation Rule) · **Bridge:** `B3-MAY-TDA` · **Tier:** Standard
**Parents:** `H-B3-1` / `H-B3-1b` (raw fixed-threshold), `H-B3-1c` (V1, AR(1)-null), `H-B3-1d` (V1',
IAAFT-null), `H-B3-1e` (V2', detrend+IAAFT-null) — all four already-computed real-data experiments

> **Role of this experiment:** V3 from `H-B3-1e`'s own Relaxation Map: abandon the binary PASS/REJECT
> threshold framing that has produced three consecutive REJECTs with an identical false-positive SET
> (Windermere, Loch Leven, Paul chl/pH/doSat), and instead report the 9-series × 4-method comparison
> DESCRIPTIVELY. **No new compute** — this experiment re-reads the already-committed `metrics/run.json`
> from all 4 parent experiments and joins them into one table. This is exactly the "cheapest
> differentiating test" available at this point (CDT Protocol): zero new risk of a 5th null-model
> failure, maximum reuse of existing evidence.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 9 series (Lower Zurich, Windermere, Loch Leven, Peter chl/pH/doSat, Paul chl/pH/doSat), across the 4 already-run detection methods (raw fixed-threshold, V1/AR(1), V1'/IAAFT, V2'/detrend+IAAFT) |
| **Descriptive predicate** | Which series, under WHICH methods, show a TDA lead over classical EWS — reported as a continuous comparison, not a binary verdict |
| **Measurable outcome** | A single joined table (`metrics/run.json` + a human-readable markdown table) with crossing dates/lead magnitudes for all 9 series × 4 methods, plus the floor false-positive rate from the two raw experiments |

## L0 Classification

**Descriptive** (explicit reclassification from `predictive` used in H-B3-1/1b/1c/1d/1e). This
experiment makes NO falsifiable predictive claim and has NO kill_criterion in the binary sense — per
EstimandOps, a descriptive question characterizes what IS observed, and is evaluated on accuracy of the
characterization, not on a pass/fail threshold. The four PARENT experiments remain predictive and keep
their own verdicts (CRITERION_INVALID ×2, REJECT ×3) unchanged — this experiment does not retroactively
alter them (Gate 1: a verdict for one artifact does not transfer to another just because they share data).

## Natural Language Statement

> "We describe, for each of the 9 series and each of the 4 already-tested detection methods, whether a
> TDA-betti crossing was found, whether a classical-EWS crossing was found, and the sign/magnitude of
> any lead — without applying a binary pass/fail threshold to summarize across series."

## What This Does NOT Mean

1. Does NOT establish that TDA "works" or "doesn't work" as an early-warning signal in general — it
   describes what was observed in THIS specific population under THESE specific methods.
2. Does NOT change or supersede the verdicts of `H-B3-1`, `H-B3-1b`, `H-B3-1c`, `H-B3-1d`, `H-B3-1e` —
   those experiments' own decision.md files remain the authoritative record of what was tested and found
   there.
3. Does NOT constitute a PROMOTE of the underlying bridge `B3-MAY-TDA` — a clean descriptive pattern
   (if one emerges) would be a LEAD at best, requiring a properly pre-registered follow-up experiment
   with its own kill criterion to become a predictive claim again.
