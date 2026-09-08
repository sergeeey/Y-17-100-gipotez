# H-B3-1o — claim.md

## Origin

H-B3-1g (total persistence, "hard branch" invariant) found: Peter pH's TDA signal, under
the self-calibrated expanding-tau/surrogate-crossing detection rule, crosses its own null
threshold at day 318 (season-time), **100 days AFTER** the classical statistics' earliest
crossing (day 218). H-B3-1g's own Relaxation Map named this explicitly: *"Investigate
directly why total persistence fires LATE here — could reveal a real, if delayed,
structural signal, or an artifact of the total-persistence statistic's own dynamics...
Cheapest immediate follow-up if this branch is pursued."* Never run. This is the last
unexecuted item from H-B3-1g's own Relaxation Map (the other two rows -- combine with
IAAFT/detrend null, and conjunction with entropy -- were completed by H-B3-1i and H-B3-1h
respectively).

## EstimandOps L0

**Question type:** Descriptive. "Does Peter pH's RAW total-persistence signal show a
structural rise timed similarly to a clean positive control (Peter doSat), even though its
statistical (tau/surrogate-crossing) detection is delayed by 100 days?" No causal claim
about lake dynamics.

## The claim (falsifiable)

Reuses UNCHANGED via dynamic import: `peter.load_daily_series`, `obrien.WINDOW_FRAC`,
`obrien.EMBED_DIM`, `obrien.EMBED_DELAY`, `obrien.betti1_total_persistence_series`
(H-B3-1g's own tda_stat_fn). H-B3-1g's own stored `metrics/run.json` values (crossings)
are reused unchanged, not recomputed, per Minimal Relaxation Rule.

**Half-rise date metric:** for a given raw total-persistence series (window-end dates,
values), the first date at which the series reaches >=50% of its own [min, max] range
within the observed window. This is a simple, scale-robust indicator of "when does the raw
topological signal show its main structural change" -- independent of the expanding-tau
accumulation and self-calibrated-null machinery that produces the crossing date.

1. **Positive control (sanity check on the metric itself):** compute the half-rise date
   for Peter doSat (a clean positive with NO lag problem, tda_crossing=172,
   classical_crossing=185). If the half-rise date is NOT reasonably close to doSat's own
   tda_crossing, the half-rise metric itself is not tracking what "crossing" tracks, and
   the primary check below cannot be trusted.
2. **Primary:** compute the half-rise date for Peter pH. Compare its distance to
   `classical_crossing=218` (the "artifact" hypothesis anchor -- raw signal timed near
   the classical detection, lag purely from the tau/null-crossing statistic) versus its
   distance to `tda_crossing=318` (the "genuine delay" hypothesis anchor -- raw signal
   itself changes late). Whichever anchor is closer is the better-supported explanation.

## Kill criterion (pre-registered)

- **ARTIFACT_HYPOTHESIS_SUPPORTED if:** pH's half-rise date is closer to
  `classical_crossing` (218) than to `tda_crossing` (318) -- the raw signal changes near
  where classical statistics already detect something, and the 100-day lag is a property
  of the tau-accumulation/self-calibrated-null detection method, not the underlying
  topology.
- **GENUINE_DELAY_HYPOTHESIS_SUPPORTED if:** pH's half-rise date is closer to
  `tda_crossing` (318) -- the raw signal itself does not change meaningfully until close
  to when the statistical test finally detects it.
- **Positive-control gate:** if doSat's own half-rise date is NOT within 20 days of its
  `tda_crossing` (172), the metric itself is deemed unreliable and NEITHER primary verdict
  is reported -- `METRIC_UNRELIABLE` instead.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "the half-rise date (>=50% of own [min,max] range) is a
meaningful proxy for 'when the raw signal structurally changes', independent of the
tau/crossing machinery." **Check:** the positive-control gate above IS this check --
before trusting the metric on pH (the case with an unresolved question), it must first
correctly track a KNOWN case (doSat, whose crossing is already established and undisputed)
Not run as a separate abstract check; the experiment's own Kill Criterion structure already
requires this validation to pass before the primary claim is even reported.

## What this does NOT mean

1. Does NOT establish a NEW detection rule or propose using half-rise dates for future
   PROMOTE-tier detection -- this is a diagnostic on ONE already-flagged anomaly, not a
   new methodology.
2. Does NOT retroactively change H-B3-1g's own REJECT-adjacent verdict (4/5 false
   positives, far from PROMOTE) -- that verdict does not depend on resolving pH's lag
   mechanism.
3. Does NOT test any OTHER series with a similar lag pattern -- Peter pH is the only
   series in this arc's history flagged with this specific "crosses late" behavior.
4. A half-rise date close to one anchor is suggestive, not proof of causation -- this
   experiment cannot distinguish "the tau-accumulation method is slow for this series" from
   "the self-calibrated null happens to be elevated for this series" as the SPECIFIC
   mechanism, even if it does distinguish "raw signal early" from "raw signal late."
