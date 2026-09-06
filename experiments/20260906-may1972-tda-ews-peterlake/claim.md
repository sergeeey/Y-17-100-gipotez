# claim.md — 20260906-may1972-tda-ews-peterlake

**Graph node:** `H-B3-1` · **Bridge:** `B3-MAY-TDA` · **Tier:** Full · **Phase:** 1 of 2 (see kill_criterion)

> **Scoping note (read first):** the bridge's original grounding (Mangal, GloBI databases) was found
> WRONG for this task during scoping (2026-09-06) — neither gives repeated time-series snapshots of one
> system approaching collapse. Corrected source: Carpenter et al. 2011 (*Science*) whole-ecosystem
> experiment. See `01-cross-domain-bridges/Cross-Domain Bridge Lab — Project.md § Bridge 3` for the full
> correction record. This file is the DESIGN artifact from that scoping session — data has not yet been
> downloaded or analyzed. Status in `registry/graph.yaml`: `ready` (scoped, not run).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Multivariate limnological time series (chlorophyll-a, pH, dissolved oxygen, zooplankton biomass) from Peter Lake (manipulated) and Paul Lake (reference), NTL-LTER Cascade Project, 2008–2011 manipulation window |
| **Falsifiable predicate** | A topological signal (Betti-1 count or persistence entropy, computed via Takens time-delay embedding + Vietoris–Rips filtration) crosses a pre-registered threshold earlier than classical EWS (rising lag-1 autocorrelation / rising variance) on the SAME series, in Peter Lake only — not in Paul Lake |
| **Measurable outcome** | Lead time (days) of TDA signal vs classical EWS signal, per series, computed against the known manipulation/shift timeline published in Carpenter et al. 2011; PASS iff TDA lead time > 0 on ≥1 of ≥2 tested series in Peter Lake AND neither method false-positives on Paul Lake |

Gate: entity, predicate, outcome all fillable from verified sources. **PROCEED.**

## L0: Question Type

- [ ] Descriptive
- [x] Predictive — "does the TDA signal's timing predict/precede the classical EWS signal's timing on THIS system?"
- [ ] Causal

No intervention BY us (the lake manipulation is Carpenter's, already in the historical record); we are
comparing two detection methods retrospectively on the same recorded intervention. `estimand.md` filled
without a causal DAG.

## Natural Language Statement (written before data download)

> "We estimate the **lead time (in days) of a TDA-based regime-shift signal relative to classical EWS**
> for the **Peter Lake manipulation (2008–2011, NTL-LTER Cascade Project)**, comparing **Betti-1 /
> persistence entropy from Takens-embedded limnological series** against **rising lag-1 autocorrelation
> and variance on the same series**, using **Paul Lake (unmanipulated reference, same period)** as the
> negative control, and handling **missing/irregular sampling gaps** (ICE) by **linear interpolation
> capped at 2 missing samples, else exclude the window** (composite: a longer gap changes what the
> embedding measures, so it is not silently imputed past that cap)."

## FL Pre-Gates (AI-generated claim — mandatory before estimand)

### Step -4: Source Trace

| Claim | Source | Status |
|---|---|---|
| Peter Lake manipulated 2008–2011, Paul Lake reference, EWS detected >1 yr before shift | Carpenter et al. 2011, *Science* 332(6033):1079–1082, DOI 10.1126/science.1203672 | `[VERIFIED]` (WebSearch, title/journal/date/finding cross-confirmed across ResearchGate, Science.org, Cary Institute preprint, USDA mirror) |
| High-frequency chlorophyll/temperature/DO data publicly archived | Environmental Data Initiative, `portal.edirepository.org`, `knb-lter-ntl` package series | `[VERIFIED]` general accessibility; `[WEAK]` exact package IDs — not pinned yet, to be recorded in `manifest.md` at download time |
| Classical EWS indicators perform near chance on most empirical (non-experimental) lake data; clean critical transitions are rare | Wang et al. 2023, *Nature Communications*, DOI in article page `s41467-023-43744-8` | `[VERIFIED]` (WebSearch, title/journal/finding cross-confirmed across Nature.com, PMC, NSF PAR, PubMed) |
| Persistent homology applied generically to ecological time series (BioTIME, 500 series) | Bailey 2026 review, arXiv:2603.25760 | `[VERIFIED]` (arXiv abstract fetched directly) — this is a REVIEW citing the application, not itself the primary BioTIME study; the primary study was not independently located and is NOT cited as a standalone source |
| Mangal database: 187 static cross-sectional predation networks, not repeated snapshots of one system | mangal project pages (Wiley Ecography, bioRxiv preprint) | `[VERIFIED]` |
| GloBI: interaction-record aggregator; "snapshots" = database versions every 6 months | globalbioticinteractions.org, Zenodo versioning | `[VERIFIED]` |

### Step -3: Novelty Check

- Searched: `null_results/INDEX.md`, `parked/INDEX.md` (no prior entry — new hypothesis) `[VERIFIED]`
- Searched: "TDA/persistent homology + Carpenter Peter Paul Lake" — **no hit found** connecting persistent
  homology methods specifically to this dataset `[VERIFIED, absence — WebSearch, 2026-09-06]`
- The GENERAL method (TDA as EWS, with a quantified lead-time race against classical CSD indicators) IS
  established in finance (~34-day lead time reported, Frontiers 2022) and applied descriptively to ecology
  (BioTIME, Bailey 2026 review) — so this is **transfer of an established method to a new, specific,
  well-characterized case**, not invention of a new method and not a re-run of an already-published
  head-to-head comparison. `[VERIFIED via absence + presence, see table above]`
- **Verdict: proceeds.** Not pseudo-novelty (the specific comparison on this dataset is not found
  published); not overclaiming invention (the method itself is borrowed, cited, not presented as new).

## Claim Entropy

| Component | Before scoping (2026-09-06, start of session) | After scoping (now) |
|---|---|---|
| Unsupported HIGH claims | 2 (Mangal/GloBI as valid sources; ≥3 collapses assumed cheaply available) | 0 (both corrected with cited evidence) |
| Hidden assumptions | 3 (network-snapshot data exists in Mangal; classical EWS ground truth is reliable enough to race against; TDA method transfers to ecology without modification) | 1 (embedding parameters (dimension, delay) are not yet chosen — deferred to Substrate Gate at run time) |
| Missing negative controls | 1 (no reference system specified) | 0 (Paul Lake specified as built-in negative control) |
| Ambiguous definitions | 1 ("known historical collapses" — vague) | 0 (Peter Lake manipulation window is dated to the day in Carpenter 2011) |
| Unresolved blockers | 1 (no dataset identified) | 0 (EDI/NTL-LTER identified and generally accessible; exact package pinning deferred to manifest.md, not a blocker) |
| **Total** | **8** | **1** |

## Counterfactual Frame

| Question | Answer |
|---|---|
| What must change for H to be true? | Nothing structural — H asks whether an established method (TDA-EWS) transfers to a specific, well-characterized dataset with a known answer key (Carpenter 2011's own classical-EWS lead time) |
| How many independent changes required? | 0 for the transfer test itself; if H fails, the interesting question becomes whether embedding parameters or the specific topological summary (Betti-1 vs persistence entropy) matter — that's Minimal Relaxation territory, not a new theory |
| Known system where these conditions already hold? | Yes — financial-crisis TDA-EWS studies already race the same two families of indicators; ecology has not yet had this specific race published for this dataset |

**Verdict:** `within-framework`.

## Falsifiable Claim

**Claim:** On Peter Lake, the TDA lead time (days between topological threshold crossing and classical-EWS
threshold crossing) is positive on ≥1 of ≥2 tested series, while Paul Lake shows no threshold crossing by
either method.

**Check:** `python experiments/20260906-may1972-tda-ews-peterlake/run.py run` (not yet written) →
`metrics/run.json["lead_time_days"]` per series, `metrics/controls.json["paul_lake_false_positive"]`.

## HD-MAVP Decomposition

| # | Assumption | Type | Role | Depends On | Evidence | Status |
|---|---|---|---|---|---|---|
| A1 | Carpenter 2011's classical-EWS timeline (>1 yr lead) is itself correct/reproducible from the raw series | empirical | core | — | Carpenter et al. 2011, published finding | alive |
| A2 | Takens embedding parameters (dimension, delay) chosen a priori do not need per-series tuning that would make the comparison circular | tooling | core | — | standard TDA-on-time-series practice (Bailey 2026 review cites this as a named limitation: "representation dependence") | weak_alive — flagged, not yet tested |
| A3 | Peter/Paul Lake data at the needed temporal resolution (daily or better, 2008–2011) is actually downloadable, not just "archived in principle" | measurement | protective_belt | — | EDI portal exists and is public; exact package pinning not yet done | unknown → tested at Substrate Gate |
| A4 | Betti-1 / persistence entropy is a meaningful summary for THIS kind of multivariate limnological series (not just for the 1D scalar series used in finance) | mathematical/empirical | core | A2 | Bailey 2026 review — ecology application exists (BioTIME) but for population time series, not manipulated-lake physicochemical series specifically | weak_alive |
| A5 | Wang et al. 2023's finding (EWS near-chance on empirical data) does not itself disqualify Carpenter 2011 as ground truth | empirical | protective_belt | — | Carpenter 2011 is a controlled MANIPULATION experiment, explicitly the kind of case Wang et al. 2023 contrasts with uncontrolled observational data | alive |

**Principal Assumption (cut vertex):** A2 (embedding parameters) — feeds A4; if embedding choice is
under-specified or tuned post hoc, both the TDA signal and the "no circularity" claim collapse together.
**Rule: pre-register embedding dimension/delay in `estimand.md` sensitivity plan BEFORE looking at Peter Lake data**, using only Paul Lake or a held-out window to choose them if tuning is unavoidable.

### Constraints

- Applies only to physicochemical/biological time series from a controlled whole-ecosystem manipulation
  with a paired reference — NOT to uncontrolled observational lake surveys (per Wang et al. 2023, those
  are a harder, separate case).
- Says nothing about ecological *interaction networks* (the original Mangal/GloBI framing) — this is a
  time-series-embedding method, not a network-topology method. The bridge's title (May 1972
  stability-complexity, which is about network structure) connects to this test only via the shared
  "topology detects reorganization" mechanism, not via literal network snapshots. This is a scope
  narrowing the scoping session itself produced — flagged explicitly, not smoothed over.

### Unknowns

- [U] Exact EDI package IDs and whether daily-resolution data covers the full 2008–2011 window without
  large gaps — to be resolved at Substrate Gate.
- [W] Whether Betti-1/persistence entropy on THIS series type will show a clean pre-shift trend at all
  (weakly supported by the BioTIME analogy, not this specific data type).

### Dependencies

- EDI/NTL-LTER portal reachable at run time; Ripser (or `giotto-tda`/`ripser.py`) installable.

## Pearl Card

**Prediction:** if H holds, TDA lead time > 0 days on ≥1 series in Peter Lake; Paul Lake shows no
threshold crossing on either method within the same window.
**Falsification:** TDA lags or ties classical EWS on every series, OR TDA false-positives on Paul Lake
(disqualifying it regardless of Peter Lake's result).

## What This Does NOT Mean

1. Does NOT prove TDA is generally superior to classical EWS — N=1 controlled system, one manipulation type (trophic cascade via predator addition).
2. Does NOT generalize to uncontrolled/observational ecological time series — Wang et al. 2023 shows those are a materially harder case, explicitly out of scope for Phase 1.
3. Does NOT test the original network-topology framing (Mangal/GloBI, interaction-network snapshots) — that framing was found infeasible during scoping and is not resolved by this experiment.
4. Does NOT establish causality — both methods are applied retrospectively to an already-recorded, already-published intervention.
5. A PASS here does NOT license claiming "≥3 collapses confirmed" — Phase 2 (multiple independent cases) is a separate, harder undertaking gated on Phase 1 not being killed.

## MCID

MCID = **1 day** of lead time (any positive, reproducible lead time is informative given N=1; this is
deliberately loose because the point of Phase 1 is existence, not effect size — a large MCID would let a
near-tie pass as a win, which is not being risked here).
