# claim.md — 20260906-may1972-tda-ews-obrienlakes

**Graph node:** `H-B3-1` (re-scoped) · **Bridge:** `B3-MAY-TDA` · **Tier:** Full

> **Re-scoping note (read first):** the original Phase 1 plan (`experiments/20260906-may1972-tda-ews-peterlake/`)
> targeted Carpenter et al. 2011's Peter/Paul Lake dataset via EDI. That is `BLOCKED-INFRASTRUCTURE`
> (`substrate_gate.md` there: EDI's REST API returns 403 for all public methods, the web portal requires a
> Cloudflare Turnstile challenge — not bypassed). The Peter Lake experiment directory is left as-is, not
> deleted; its blocker stands. This is a **new, separate** experiment using a genuinely reachable data
> source: O'Brien et al. 2023 (*Nature Communications*, the same paper cited in `pearl_registry/INDEX.md`
> for the "classical EWS often fails on real data" finding) published their processed multi-lake plankton
> data and transition-date estimates on GitHub (`duncanobrien/ews-assessments`), reachable via
> `raw.githubusercontent.com` with no auth, no CAPTCHA. Downloaded and sha256-recorded in `manifest.md`.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Monthly community-state time series (`pca1`, first principal component of genus-level plankton abundance) for three lakes: Lower Zurich, Windermere, Loch Leven (O'Brien et al. 2023 public data) |
| **Falsifiable predicate** | A TDA-based signal (Betti-1 count / persistence entropy from Takens-embedded `pca1`) crosses a pre-registered threshold earlier than classical EWS (rising lag-1 autocorrelation / rising variance) on Lower Zurich's approach to its documented ~2002 community transition — and neither method crosses its threshold on Windermere or Loch Leven, which have no documented transition |
| **Measurable outcome** | lead time in months (TDA threshold date − classical EWS threshold date) on Lower Zurich; PASS/FAIL flag for false-positive on each of the two negative-control lakes |

Gate: entity/predicate/outcome all fillable from the downloaded, hash-verified data. **PROCEED.**

## L0: Question Type

- [ ] Descriptive
- [x] Predictive — does the TDA signal's timing precede the classical EWS signal's timing?
- [ ] Causal

## FL Step -4: Source Trace

| Claim | Source | Status |
|---|---|---|
| O'Brien et al. 2023 found classical EWS near-chance on most empirical lake data | Nature Communications, DOI in `s41467-023-43744-8` (already source-traced in `H-B3-1`'s original scoping, ADR-006) | `[VERIFIED]` |
| Processed data + transition-date estimates publicly hosted on GitHub, CC-BY-4.0 (per Zenodo record 10.5281/zenodo.10062493) | `github.com/duncanobrien/ews-assessments`, files fetched directly, sha256 recorded | `[VERIFIED]` |
| Lower Zurich "community" transition ≈2002 | `transition_dates.csv` row 4: `state_date=2002, temporal_date=2002, date_match=TRUE, threshold_date=2002` — three independent dating methods in the SAME row agree | `[VERIFIED]` — internal consistency checked, not just presence of a number |
| Windermere / Loch Leven "community": no transition | Same CSV, `state_date=NA` for both | `[VERIFIED]` |

**Consistency check that changed the plan (Gate 1 discipline — do not use a number without checking it fits
the artifact you actually have):** Mendota's transition (2012) and Washington's (1975) both fall **outside**
the date range of the corresponding series in the downloaded `wrangled_genus_plank_data_public.Rdata`
(Mendota data ends 2009.25; Washington data ends 1970.00). Using either as a positive case would test a
transition the downloaded population cannot see. **Excluded from this experiment for that reason** — not
because they were inconvenient, but because they fail the artifact/population match check.

## FL Step -3: Novelty Check

Same conclusion as the original H-B3-1 scoping (ADR-006): the general method (TDA-as-EWS with a lead-time
race) is established elsewhere; no prior application to O'Brien et al.'s specific lake series was found.
Not re-run in full — the population changed, the method and its novelty status did not.

## Natural Language Statement

> "We estimate the lead time (months) of a TDA-based regime-shift signal relative to classical EWS for
> Lower Zurich's community-state trajectory (pca1, 1977–2005) around its documented ~2002 transition,
> using Windermere and Loch Leven (both confirmed transition-free over their observed windows) as negative
> controls, handling missing months (ICE) by exclusion beyond a 2-sample gap (same convention as the
> blocked Peter Lake design, kept for consistency)."

## HD-MAVP Decomposition (abbreviated — full version in `estimand.md`)

| # | Assumption | Status |
|---|---|---|
| A1 | pca1 alone (not pca1+pca2 jointly) is an adequate scalar summary of community state | weak_alive — O'Brien's own transition dating used a single-axis bimodality test (mode1/mode2 columns in transition_dates.csv), so this matches their methodology, not an arbitrary simplification |
| A2 | Takens embedding parameters (dimension, delay) chosen on the WHOLE series via standard heuristics (autocorrelation-based delay, false-nearest-neighbours-free default dimension=3 given short series), not tuned near the transition | alive — pre-registered in `run.py` before inspecting the transition window |
| A3 | Monthly resolution (up to 332 points for LZ) is sufficient for a Vietoris–Rips construction in sliding windows | unknown → tested by whether the pipeline produces stable Betti numbers at all (harness check) |
| A4 | Lower Zurich's transition is a genuine regime shift, not an artifact of the threshold-GAM method that produced `transition_dates.csv` | accepted from O'Brien et al.'s own publication — not re-derived here |

## What This Does NOT Mean

1. Does NOT complete Phase 1 as originally scoped (Peter Lake) — that remains `BLOCKED-INFRASTRUCTURE`, unresolved, tracked separately.
2. Does NOT generalize beyond these 3 lakes / 1 transition — this is still an N=1-positive-case design, just with 2 negative controls instead of 1.
3. Does NOT validate or challenge O'Brien et al.'s own conclusion about classical EWS in general — this experiment uses their transition dates as ground truth, it does not re-litigate them.
4. Does NOT establish causality.

## MCID

MCID = 1 month (loose; existence-of-lead test, not effect-size test — same rationale as `H-B1-1c`).
