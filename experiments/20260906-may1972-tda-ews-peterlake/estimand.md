# estimand.md — 20260906-may1972-tda-ews-peterlake
# question_type = predictive (not causal) -> causal layer below is N/A, kept struck-through for the record
# Protocol: rules/estimand-ops.md

## L1 Attributes

**Population:** Daily/high-frequency limnological time series (chlorophyll-a, pH, dissolved oxygen,
zooplankton biomass) from Peter Lake (manipulated, NTL-LTER Cascade Project) and Paul Lake (unmanipulated
reference), 2008–2011. Inclusion: windows with ≤2 consecutive missing samples. Exclusion: larger gaps (ICE).

**Intervention:** None by us — retrospective comparison of two detection methods on an already-recorded
historical manipulation (Carpenter et al. 2011: gradual largemouth bass addition to Peter Lake).

**Comparator:** Classical EWS (rising lag-1 autocorrelation, rising variance) on the same series, benchmarked
against Carpenter et al. 2011's own published lead time (>1 year before the food-web shift).

**Endpoint:** Lead time in days between TDA threshold crossing and classical-EWS threshold crossing, per series.

**Summary measure:** Lead time (days), reported per series (not pooled — N=1 system, pooling would hide
which series actually carries the signal).

**MCID:** 1 day (deliberately loose — Phase 1 tests existence of a lead, not its magnitude).

---

## Intercurrent Events (ICE)

_Post-baseline events that change endpoint meaning or measurability. ICE is NOT missing data._

| Event | Strategy | Rationale |
|-------|----------|-----------|
| Gap of >2 consecutive missing samples | composite → exclude window | A long gap changes what the embedding measures; imputing past 2 samples would fabricate the topology being tested |

---

## Natural Language Statement
_Write BEFORE collecting results._

> "We estimate the lead time (days) of a TDA-based regime-shift signal relative to classical EWS for the
> Peter Lake manipulation (2008–2011), comparing Betti-1/persistence entropy against rising
> autocorrelation/variance on the same series, using Paul Lake as negative control, handling sampling
> gaps by exclusion beyond a 2-sample cap."

---

## Causal Layer — N/A (question_type = predictive, not causal)

Per `rules/estimand-ops.md`, the causal layer (DAG, 4 identifiability checks, identification strategy) is
required only for `question_type: causal`. This estimand is `predictive` (comparing which of two detection
methods signals earlier) — no causal claim is made about WHY the regime shift occurred. Section omitted
by design, not by oversight.

---

## What This Result Does NOT Mean
_Write at least 3 explicit non-interpretations BEFORE collecting results._

1. Does NOT prove generalization to uncontrolled/observational lake time series (Wang et al. 2023 shows those are materially harder — clean transitions are rare, classical EWS itself often fails there).
2. Does NOT establish causality — retrospective comparison of two detection methods on an already-recorded intervention.
3. Does NOT apply to the original network-topology framing (Mangal/GloBI interaction-network snapshots) — found infeasible during scoping; this experiment tests a different (time-series-embedding) mechanism under the same bridge title.
4. A PASS does NOT license "TDA beats EWS on ≥3 collapses" — Phase 2 is separate and gated on this not being killed.

---

## Sensitivity Analyses
_Minimum 2 for Full-Ladder. Minimum 1 for Standard-Ladder._

1. Embedding parameters (Takens dimension, delay) pre-registered on Paul Lake / pre-manipulation window ONLY — never tuned on the Peter Lake shift window (guards the principal assumption A2 in claim.md from circularity).
2. Alternative topological summary: persistence entropy vs Betti-1 — both computed, neither picked post hoc.
3. Alternative classical estimator: autocorrelation vs variance, both required to fail before declaring a TDA lead.
