# H-B3-1n — claim.md

## Origin

H-B3-1l (peak-tau reporting) found: on Lower Zurich, the TDA (Betti-1 persistence entropy)
peak date (2000.5) precedes the classical peak date the paper's own selection rule uses
("whichever of AC1/var peaks closest to the documented transition", 2004.67 for var) by
**+50.0 months** — reported CONFIRMED per the pre-registered criterion. A sixth skeptic
pass (same day) found the mechanism cited to explain this ("argmax of an expanding-window
statistic is structurally biased toward an earlier index; TDA statistics can jump
discontinuously between windows while classical rolling statistics change smoothly")
plausible but unverified, and separately found that AC1 ALONE (1999.25) already precedes
TDA (2000.5) — the classical-peak "closest to transition" selection rule is what lets TDA
appear to win at all.

This experiment (pearl_registry, 2026-09-07, impact 8, "~5 minutes, machinery ready") runs
the cheap check the skeptic pass proposed but did not execute: reproduce the SAME
peak-lead computation on ~500 AR(1) surrogates of Lower Zurich's own real series (matched
length/mean/variance/lag-1 autocorrelation, no real transition or mechanism by
construction) and check whether a comparable lead arises from noise alone.

## EstimandOps L0

**Question type:** Descriptive. "Does the classical-vs-TDA peak-date lead H-B3-1l found on
Lower Zurich arise at comparable magnitude from mechanism-free AR(1) surrogates of the same
series?" No causal claim about what drives lake dynamics.

## The claim (falsifiable)

Reuses UNCHANGED via dynamic import: `obrien.ar1_surrogate`, `obrien.rolling_stat`,
`obrien.betti1_entropy_series`, `obrien.expanding_kendall_tau`, `obrien.load_series`
(H-B3-1/obrienlakes) and H-B3-1l's own `peak_index`/peak-date-selection logic (same file,
reused via dynamic import, NOT reimplemented). The documented transition date (2002.0) is
kept FIXED across all surrogates — it is an externally given design parameter of the
peak-selection algorithm (which classical statistic to prefer), not something derived from
the data being tested, so holding it fixed while randomizing the SERIES is the correct way
to isolate "does the algorithm produce large leads on structureless input" from "is there a
real transition."

1. **Primary:** compute `lead_months = (classical_peak_date_used - tda_betti_peak_date) *
   12` on 500 AR(1) surrogates of Lower Zurich's real PC1 series, using the exact same
   window (80), embedding (dim=3, delay=1), and classical-selection rule ("closest to
   2002.0") as H-B3-1l. Report the empirical percentile of the REAL lead (+50.0 months)
   within this null distribution.
2. **Secondary (bonus, same machinery, near-zero extra cost):** the same check for
   `ac1_lead_months = (ac1_peak_date - tda_betti_peak_date) * 12` — testing whether AC1
   alone preceding TDA (the skeptic's second finding, -15 months, i.e. AC1 leads) is itself
   inside or outside the mechanism-free null.

## Kill criterion (pre-registered)

- **CRITERION_INVALID (floor artifact) if:** the real +50.0-month lead falls at or below
  the **80th percentile** of the surrogate null distribution (i.e. **>=20% of
  mechanism-free surrogates produce a lead at least as large**) — same discipline H-B3-1m
  used for its own floor check (a criterion within ordinary noise range cannot discriminate
  signal from no-mechanism).
- **Lead survives as informative if:** the real lead falls **above the 95th percentile**
  (fewer than 5% of surrogates match or exceed it) — genuinely unusual relative to what
  pure AR(1) structure + this peak-selection algorithm produces on its own.
- **Between 80th-95th percentile:** inconclusive at this sample size, reported as such, not
  rounded to either side.

## What this does NOT mean

1. Does NOT retest H-B3-1l's underlying data or TDA computation — reuses it unchanged, per
   Minimal Relaxation Rule. Any bug in the shared `obrien` module would affect both.
2. Does NOT test the OTHER two lakes (Windermere, Loch Leven, negative controls) — Lower
   Zurich only, matching H-B3-1l's own primary (positive-control) claim; a full population
   check is a possible but not yet run follow-up.
3. Does NOT resolve the skeptic's proposed MECHANISM (early-index argmax bias) directly —
   this tests the mechanism's PREDICTED CONSEQUENCE (large leads arise from noise) without
   independently verifying the mechanism's own internal logic.
4. A CRITERION_INVALID verdict here would not retroactively change H-B3-1l's own recorded
   status without a separate, explicit correction step (this experiment's decision.md would
   propose one, not apply it automatically) — the graph node itself must be edited
   separately per this lab's retroscan discipline.
