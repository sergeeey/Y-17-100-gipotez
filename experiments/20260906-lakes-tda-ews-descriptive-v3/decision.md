# decision.md — 20260906-lakes-tda-ews-descriptive-v3

**Graph node:** `H-B3-1f` · **Date:** 2026-09-06

## Verdict

Not applicable in the PROMOTE/REJECT sense — this is a **descriptive** experiment (L0 reclassified,
see `claim.md`). The finding below is reported as-is, not gated behind a pass/fail threshold.

## The Consolidated Table (all 4 methods × 9 series, `metrics/run.json`)

| Series | Role | # methods (of 4) with a TDA crossing | # methods with a POSITIVE lead (TDA before classical) |
|---|---|---|---|
| Lower Zurich | positive | 4 | 2 |
| Windermere | negative | 3 | 0 |
| Loch Leven | negative | 4 | 1 |
| Peter chl | positive | 2 | 0 |
| Peter pH | positive | 0 | 0 |
| Peter doSat | positive | 3 | 3 |
| Paul chl | negative | 4 | 0 |
| Paul pH | negative | 0 | 0 |
| **Paul doSat** | **negative** | **4** | **4** |

## The Central Finding

**Ranked by robustness of the "TDA leads classical EWS" signal across the 4 independent methods
tested (raw, V1/AR(1), V1'/IAAFT, V2'/detrend+IAAFT):**

```
Paul doSat (negative) ... 4/4 methods agree  <- MOST robust signal in the entire dataset
Peter doSat (positive) .. 3/4 methods agree
Lower Zurich (positive) . 2/4 methods agree
Loch Leven (negative) ... 1/4 methods agree
(5 series, 2 positive + 3 negative) 0/4 methods agree
```

**The single most method-independent, robust "TDA-leads-classical" signal in this entire study belongs
to a documented NON-transitioning reference lake (Paul doSat) — appearing in every one of the 4
detection methods (leads of +30, +35, +29 days under V1/V1'/V2', and even the raw fixed-threshold
method), more consistently than 2 of the 3 genuine positive cases (Peter chl: 0/4, Peter pH: 0/4).**
Only Peter doSat (3/4) comes close to Paul doSat's consistency, and no method achieves what Lower
Zurich's raw result alone suggested (a full, unambiguous, cross-method-replicated early warning).

This is NOT visible from any single parent experiment's binary REJECT/CRITERION_INVALID verdict — those
report only "5/5 negative controls false-positive" as an aggregate count. The per-series,
per-method-count breakdown reveals something more specific and more useful: **the false-positive signal
is not spread thin and weak across the 5 negative controls — it is concentrated, and in its most
concentrated instance (Paul doSat), it is QUANTITATIVELY MORE ROBUST than most of the true-positive
signal.** A detector whose most confident false alarm out-competes 2 of its 3 true alarms is not
usefully discriminating, regardless of which specific null model generated the alarm.

## Secondary Observations

- **Peter pH and Paul pH both show ZERO TDA crossings across all 4 methods** — the pH variable appears
  structurally quiet for TDA-Betti-1 regardless of role (positive or negative). This is a specificity
  observation orthogonal to the main finding: it's not that TDA fires indiscriminately on every series;
  it is silent on 2/9, mixed on the rest.
- **Peter chl and Paul chl are near-mirror images**: Peter chl (positive) gets 2/4 crossings with 0
  positive leads; Paul chl (negative) gets 4/4 crossings with 0 positive leads. Neither variable's TDA
  signal, when present, ever LEADS classical EWS in either lake — a further specificity-neutral
  observation (chl's TDA signal, when it fires, is uninformative about lead-time regardless of role).
- **Lower Zurich's signal degrades under naive surrogate-nulling** (2/4 methods, not 4/4) because two of
  the four methods (V1, V1') found NO classical crossing at all for Lower Zurich (making "lead" formally
  undefined, not merely negative) — a reminder that a missing comparison point is different from a
  negative one, and aggregate counts can obscure which.

## What This Does NOT Mean

1. Does NOT retroactively change the verdicts of `H-B3-1`/`H-B3-1b` (CRITERION_INVALID) or
   `H-B3-1c`/`H-B3-1d`/`H-B3-1e` (REJECT) — this is a re-presentation of their own already-committed
   numbers, not a new test.
2. Does NOT prove TDA carries no information — Peter doSat's persistence across 3/4 independent null
   models is a real, if uninterpretable-in-isolation, pattern.
3. Does NOT establish that Paul doSat's signal is "wrong" in some absolute sense — Paul Lake IS the
   documented reference (non-manipulated) lake per Carpenter et al. 2011, so by design it should show
   no regime-shift signal; its persistent TDA-lead is exactly what "false positive" means operationally
   here, now shown to be the STRONGEST such instance in the study, not a marginal one.
4. Does NOT constitute a PROMOTE of bridge `B3-MAY-TDA` — if anything, this descriptive synthesis
   sharpens the case that the CURRENT operationalization (Betti-1 persistence entropy + expanding-Kendall-tau
   crossing, under any of the 4 null models tried) does not reliably separate true from false alarms:
   its most convincing false alarm outranks 2 of 3 true alarms.

## Recommendation for `B3-MAY-TDA` Going Forward

Given: (a) three consecutive REJECTs with an identical false-positive series set across structurally
different null models, and (b) this descriptive synthesis showing the false-positive set's STRONGEST
member (Paul doSat) is more robust than most true positives — the honest position is that the specific
detector construction tested in this project (Betti-1 persistence entropy, expanding-window Kendall tau,
any of AR(1)/IAAFT/detrend+IAAFT nulling) has been given a fair, well-instrumented, four-variant test and
does not show the specificity needed to be useful as an early-warning detector on this population. This
does not kill the underlying cross-domain IDEA (persistent homology could in principle carry information
about phase-space restructuring) — it kills THIS SPECIFIC PIPELINE's ability to exploit that idea
reliably on THIS SPECIFIC population (small, noisy, short real ecological time series). A genuinely new
approach (different topological invariant, different embedding, or abandoning the crossing-detection
framing altogether in favor of a continuous score comparison) would be a NEW hypothesis, not a further
variant of the current one — Minimal Relaxation Rule would call this a "hard" branch requiring new
theoretical input, not another parameter tweak.

## Pearl Card Update

**New, general methodological finding (impact worth recording):** an aggregate false-positive COUNT
(e.g. "5/5") can hide a sharper and more damning pattern — ranking series by ROBUSTNESS (how many
independent methods agree) can reveal that the single most convincing false alarm outranks most true
alarms, a materially stronger statement than the aggregate count alone conveys. This cost zero new
compute to discover (pure re-analysis of already-committed data) and was only visible once the four
separate REJECT verdicts were joined into one comparative view — a concrete argument for running this
kind of "V3-style" descriptive synthesis EARLIER (e.g. after the 2nd REJECT, not the 3rd) in any future
multi-variant Relaxation Map chain.
