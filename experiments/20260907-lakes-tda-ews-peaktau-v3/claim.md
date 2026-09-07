# claim.md — 20260907-lakes-tda-ews-peaktau-v3

**Graph node:** `H-B3-1l` (bridge `B3-MAY-TDA`) · **Tier:** Standard
**Parent:** `H-B3-1b` (Relaxation Map Row 3, marked "cheapest — no new statistical machinery, just
report peaks instead of first-crossings" — the one remaining untested item after Row 1
(surrogate-based null: tested via `H-B3-1c/d/e`, REJECTED) and before Row 2 (change-point
co-requirement, still untested).

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Compares WHERE (in time) two signal families' expanding-tau
trajectories reach their maximum, against a documented external transition date. No fitted
threshold, no intervention, no causal claim about ecosystem dynamics.

## Why This Experiment, Specifically

`H-B3-1`/`H-B3-1b`'s original detection rule (first time Kendall tau ≥ 0.5) was found
`CRITERION_INVALID` (Step 4a): a mechanism-free AR(1) null crosses the SAME threshold 80-83% of
the time — the threshold itself, not TDA, was uninformative. Rows 1 (surrogate null) through
`H-B3-1c/d/e` and their descendants `H-B3-1g-k` all kept SOME form of threshold-crossing rule
(just varying the null model or statistic) and all REJECTED with an identical false-positive
pattern. Row 3 removes the threshold-crossing framing entirely, asking a different, non-circular
question: **does the peak (argmax) of TDA's tau trajectory fall closer to the documented real
transition date than classical EWS's peak does** — sidestepping the invalid-threshold problem by
never requiring ANY series (transition or not) to "cross" a fixed number.

## Scope Decision — Explicit, Not an Oversight

This experiment reuses `H-B3-1`/`H-B3-1b`'s ORIGINAL 3-lake population (Lower Zurich, Windermere,
Loch Leven) — NOT the later, expanded 5-series population used in `H-B3-1g` through `H-B3-1k`
(which added Peter/Paul lake series). Per the Minimal Relaxation Rule, this experiment changes
ONE assumption (the detection rule: threshold-crossing → peak-proximity-to-known-transition) on
the SAME population `H-B3-1b`'s own Relaxation Map was written against. Testing peak-tau on the
5-series population would be a SEPARATE, later experiment if this one is informative.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The time index (date) at which the expanding-window Kendall tau trajectory reaches its maximum, for TDA (Betti-1 persistence entropy) and for classical EWS (rolling AC1, rolling variance), on the SAME 3 lakes/series and rolling-window construction as `H-B3-1`/`H-B3-1b` (reused unchanged: `load_series`, `takens_embed`, `rolling_stat`, `betti1_entropy_series`, `expanding_kendall_tau`) |
| **Falsifiable predicate** | On Lower Zurich (documented transition ≈2002.0), TDA's peak-tau date is CLOSER to the documented transition than classical EWS's peak-tau date is, AND TDA's peak does not occur later than classical's peak (still "leads or ties", not "lags") |
| **Measurable outcome** | `|TDA_peak_date − 2002.0|` vs `|classical_peak_date − 2002.0|` on Lower Zurich; peak-lag (`classical_peak − TDA_peak`, in months) reported descriptively (no committed criterion — no real transition to compare against) for Windermere and Loch Leven |

## FL Step -3: Novelty Check

`grep` of `null_results/INDEX.md` / `pearl_registry/INDEX.md` / all `H-B3-1*` graph nodes:
peak-based (argmax) reporting has NEVER been tried in this project — every prior `H-B3-1*`
variant (`b` through `k`) kept a threshold-crossing or surrogate-crossing rule of some form.
Confirmed genuinely untested, as `H-B3-1b`'s own Relaxation Map already flagged.

## Kill Criterion (set BEFORE running)

- **CONFIRMED:** `|TDA_peak − 2002.0| < |classical_peak − 2002.0|` AND `TDA_peak ≤ classical_peak`
  on Lower Zurich — TDA's peak genuinely anticipates the real transition better than classical's
  peak does, under a threshold-free comparison.
- **REJECTED:** either condition fails — TDA's peak is not closer to the true transition, or it
  occurs no earlier than classical's.
- **Windermere/Loch Leven:** no committed criterion (they have no documented transition to
  compare proximity against) — peak-lag values reported descriptively, checked qualitatively
  for whether they show the SAME directional bias as Lower Zurich (which would suggest a
  structural artifact of the two statistics' smoothing properties rather than a real signal) or
  not (supporting that Lower Zurich's result, if CONFIRMED, reflects the real transition and not
  a generic property of the two statistic families).

## What This Does NOT Mean

1. Does NOT retroactively validate or invalidate `H-B3-1`/`H-B3-1b`'s own `CRITERION_INVALID`
   verdict on the threshold-crossing rule — that verdict concerns a DIFFERENT detection rule.
2. Does NOT generalize to the 5-series population used in `H-B3-1g-k` — explicit scope decision
   above; a separate experiment if warranted.
3. Does NOT establish causality or mechanism — a descriptive comparison of two signal families'
   peak timing against one documented historical date.
4. A CONFIRMED verdict here would NOT be statistically validated against a null model (no
   surrogate baseline is used in this design, by construction — Row 3's own wording removes
   statistical machinery entirely) — any CONFIRMED result should be read as suggestive, informing
   whether a FUTURE experiment combining peak-reporting WITH a surrogate null is worth the
   additional complexity, not as a standalone strong claim.

## MCID

Whether TDA's peak-tau date on Lower Zurich is closer to the documented transition than
classical's — reported as a fact (with exact date differences), not a threshold pass/fail on a
separate metric.
