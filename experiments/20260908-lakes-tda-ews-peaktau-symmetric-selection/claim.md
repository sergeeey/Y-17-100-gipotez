# H-B3-1p — claim.md

## Origin

H-B3-1l's sixth skeptic pass (2026-09-07) found: the code selects
`classical_peak_date_used` with TWO DIFFERENT RULES depending on the series' role. For
Lower Zurich (the positive case, `transition=2002.0` known), it picks whichever of
AC1/var peaks CLOSEST to the documented transition (oracle-informed -- uses the answer
being tested). For Windermere/Loch Leven (negative controls, `transition=None`), it falls
through to "earliest of the two" (a symmetric, honest rule with no oracle knowledge). The
skeptic independently verified `classical_ac1_peak_date=1999.25` predates
`tda_betti_peak_date=2000.5` on Lower Zurich -- i.e. AC1 ALONE already beats TDA; the
CONFIRMED verdict survives only because the code compares TDA against variance (2004.67,
selected BECAUSE it is closer to 2002.0), not against AC1.

pearl_registry (2026-09-07, impact 7) recorded the exact falsifiable prediction never
run: *"if recomputed with the SAME rule used for negative controls, classical_peak_date_
used becomes 1999.25 (AC1) -- then TDA (2000.5) would be LATER than classical, verdict
should invert to REJECTED under an honest, symmetric selection rule."*

## EstimandOps L0

**Question type:** Descriptive. "Does H-B3-1l's CONFIRMED verdict on Lower Zurich survive
when the classical-statistic-selection rule is made symmetric (the same 'earliest of the
two' rule already used for negative controls), instead of the current oracle-informed
'closest to the known transition' rule used only for the positive case?" No causal claim.

## The claim (falsifiable)

Reuses UNCHANGED via dynamic import: H-B3-1l's own `peak_index()`, and the same
`obrien.load_series`/`rolling_stat`/`betti1_entropy_series`/`expanding_kendall_tau`
pipeline (via H-B3-1l's own `run.py`, re-executed with ONE assumption changed per the
Minimal Relaxation Rule: the classical-peak selection rule).

**The one changed assumption:** `classical_peak_date_used = min(peak_ac1, peak_var)`
(earliest of the two) for ALL THREE lakes, including Lower Zurich -- removing the
`transition`-based oracle selection entirely, not just for negative controls.

1. **Primary:** recompute Lower Zurich's `classical_peak_date_used`,
   `peak_lead_months_tda_minus_classical`, and the resulting verdict under the symmetric
   rule.
2. **Consistency check:** confirm Windermere and Loch Leven's own results are UNCHANGED
   under the symmetric rule (they already used it) -- a sanity check that the rule change
   is correctly scoped to only affect the positive case, not silently altering the
   negative controls too.

## Kill criterion (pre-registered)

- **Pearl's prediction CONFIRMED if:** under the symmetric rule,
  `classical_peak_date_used == peak_ac1 (1999.25)` and `tda_betti_peak_date (2000.5) >
  classical_peak_date_used` -- i.e. TDA is now LATER, not earlier/equal, than classical.
  Per H-B3-1l's own verdict logic (`elif tda_dist < classical_dist and tda_peak <=
  classical_peak: CONFIRMED else: REJECTED`), `tda_peak <= classical_peak` becomes FALSE,
  so the verdict inverts to REJECTED regardless of the distance comparison.
- **Pearl's prediction FALSIFIED if:** the symmetric rule still selects var (2004.67) or
  some other value such that `tda_peak <= classical_peak` remains true -- CONFIRMED
  survives even under the fairer rule (not the expected outcome, but must be checked, not
  assumed from the pearl's own text).

## What this does NOT mean

1. Does NOT retest H-B3-1l's underlying TDA/classical computation -- reuses the pipeline
   unchanged, only the peak-SELECTION rule changes.
2. Does NOT change H-B3-1n's own separate finding (the +50-month peak-lead's
   AR(1)-surrogate floor check, INCONCLUSIVE_AT_THIS_SAMPLE_SIZE) -- that experiment used
   the ORIGINAL oracle-informed rule's own +50.0 lead value as its target; this experiment
   is about whether that +50.0 value itself was fairly derived, a different, earlier
   question in the causal chain.
3. Does NOT prove oracle-informed selection is always wrong in general -- this is a
   specific, targeted correction of ONE named asymmetry in ONE experiment's own code, not
   a new general detection methodology.
4. If REJECTED is confirmed here, this does NOT mean Peter doSat's own separately-robust
   signal (4x replicated across V1/V1'/V1g/conjunction) is affected -- that finding is
   entirely independent of Lower Zurich's peak-tau result.
