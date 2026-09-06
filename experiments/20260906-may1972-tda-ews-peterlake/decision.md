# decision.md — 20260906-may1972-tda-ews-peterlake

**Graph node:** `H-B3-1` (unblocked 2026-09-06 by a user-provided CSV) · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [x] **CRITERION_INVALID** (FL Step 4a stop-verdict — NOT evidence against the claim, hard rule)
- [ ] ARCHIVE

**Why:** same failure mode as the sibling experiment `H-B3-1b` (O'Brien lakes), now independently
reproduced on a COMPLETELY different real dataset (high-frequency sonde data, not monthly plankton
counts; a controlled manipulation experiment, not observational field data). AR(1) red-noise floor check
(20 surrogates per lake×variable, mechanism removed by construction): **max false-positive rate = 85%**
across all 6 series. A threshold a no-mechanism null passes 85% of the time cannot discriminate anything.

## Data unblocking (Substrate Gate resolved)

`substrate_gate.md`'s `BLOCKED-INFRASTRUCTURE` verdict is resolved: the user provided
`squealSondesMet_08to11_forOPUS.csv` directly (path (a) in that file's "What would resolve this" list —
"a human passing EDI's Turnstile challenge is not a bypass"). sha256-recorded, internally consistency-checked
against the paper's own description before use (`manifest.md`).

## Escape Point — a second correction made mid-analysis (documented, not hidden)

The FIRST run of this experiment (before this decision.md was written) applied the sibling experiment's
ICE gap-exclusion rule ("keep only the longest contiguous run") unmodified to this dataset. Because Peter
and Paul Lakes are monitored only during summer stratification (per Carpenter et al. 2011 p.2), that rule
silently kept ONLY the 2009 field season (114 of ~450 available days) and discarded 2008 and 2010 —
including the actual transition-completion date (day 230, 2010), which fell in the DISCARDED part of the
record. **Caught by inspecting the raw output before writing this file**, not by a hook. Fixed by
concatenating the three relevant seasons (2008–2010) on a season-time axis that compresses winter gaps
(a sampling-design feature, not missing data) instead of treating them as ICE. 2011 excluded on the
paper's own authority (food web already re-converged with the reference lake by then — post-transition,
not lead-up). Locked in by `tests/test_peterlake_tda_ews.py` (5 tests, all pass).

## Ground Truth (Gate 1, primary source read directly)

| Fact | Source |
|---|---|
| Bass additions: day 193/2008, day 169 & 203/2009 | Carpenter et al. 2011 preprint p.3, PDF read directly |
| Food-web transition COMPLETE: day 230, 2010 | Same, p.3: "similar to the reference lake by about day 230 of 2010" |
| Classical EWS were evident ">1 year before" transition complete | Same, Abstract |
| Their own EWS analysis used DAILY chlorophyll | Same, p.3 — daily aggregation here matches, not arbitrary |

## Floor-Ceiling Interval

### Population
Peter Lake (positive) and Paul Lake (negative control), chl/pH/doSat, daily means, 2008–2010 field
seasons concatenated on season-time (334 points each, transition at season-time day 314).

### Floor
- Construction: AR(1) red-noise surrogate matched in length/mean/variance/lag-1-autocorrelation, no
  mechanism by construction (same method as `H-B3-1b`, 20 surrogates per series here vs 30 there —
  reduced rep count for runtime on the larger series; result is decisive at either rep count)
- Value: 45–85% false-positive rate across the 6 series (Peter: 45%, 65%, 45%; Paul: 60%, 85%, 65%)
- Result: [x] MEASURED

### Ceiling
- Result: [ ] NOT MEASURED — same reasoning as `H-B3-1b`: the floor alone already invalidates the criterion

### Efficiency
- Result: [x] DEGENERATE — floor (0.45–0.85) overlaps the success region; efficiency against an
  unmeasured ceiling on top of an invalid floor would be meaningless

## Decision (Step 4a)

- [x] `CRITERION_INVALID` — not evidence against the claim.

## Evidence Summary

| Series | Classical crossing (day) | TDA crossing (day) | Lead (TDA − classical) | Before transition (day 314)? | False positive? |
|---|---|---|---|---|---|
| Peter chl | 172 | — (never) | n/a | classical: 142 days before | no |
| Peter pH | 172 | — (never) | n/a | classical: 142 days before | no |
| Peter doSat | 173/175 | 172 | **+1 day** | both ~141–142 days before | no |
| Paul chl (control) | 180 | 180 | 0 | 134 days before | **yes** |
| Paul pH (control) | 173 | — (never) | n/a | classical: 141 days before | **yes** |
| Paul doSat (control) | 194/230 | 177 | **+17 days** | both >120 days before | **yes** |

## Criterion Diagnosis (not a Kill Analysis — see `H-B3-1b`'s decision.md for the same framing rationale)

### What the (now doubled) floor evidence shows

- Two independent real ecological datasets (monthly multi-lake plankton counts; daily whole-lake
  manipulation sonde data), different sampling designs, different ecosystems, SAME failure: a fixed
  tau≥0.5 threshold on an expanding-window Kendall trend statistic is passed by a mechanism-free AR(1)
  null 45–90% of the time. This is now a **cross-dataset confirmed** methodology finding, not a fluke of
  one series (pearl impact upgraded — see `pearl_registry/INDEX.md`).
- On Peter Lake specifically: 2 of 3 variables (chl, pH) never even reached a TDA crossing at all within
  the analyzed window — the TDA statistic's expanding tau simply never got that coherent. Only doSat
  crossed, and only 1 day before classical EWS — not a meaningful "TDA leads" result even setting the
  floor problem aside.
- On Paul Lake (should show nothing): 3 of 3 variables false-positived, one (doSat) with TDA "leading" by
  17 days on a lake that never underwent any manipulation.

### What remains untouched

- [x] Whether a BETTER-CALIBRATED detection rule would show TDA leading on Peter Lake — genuinely
  untested; the one series (doSat) that did cross showed a trivial +1 day lead, not strongly suggestive
  either way.
- [x] The underlying data quality and provenance — solid (see `manifest.md` consistency checks).

### Relaxation Map — SAME three candidates as `H-B3-1b`, now with cross-dataset motivation

| Assumption | Modification | Known kill-evidence? |
|---|---|---|
| Detection rule (tau≥0.5) | Surrogate-based per-series null (V1) | No — now motivated by 2 independent floor measurements, not 1 |
| Detection rule | Trend AND change-point co-requirement (V2) | No |
| Detection rule | Report peak tau, no threshold (V3) | No |

Not run here — new experiment ID required per Minimal Relaxation Rule. Given the SAME fix would need to
be validated on BOTH `H-B3-1` and `H-B3-1b` data, the natural next experiment is a single new ID that
re-runs whichever fix (V1 preferred — least circular) against both datasets together.

## Rescue Review (OSA)

| Branch | What was invalidated | Whole branch dead? | Revival Condition | Final Status |
|---|---|---|---|---|
| H-B3-1 / H-B3-1b (TDA leads EWS, tau≥0.5 rule) | The tau≥0.5 detection rule, now on 2 independent datasets | No | Re-run V1 (surrogate null) on both Peter Lake and O'Brien lakes; if false-positive rate on all negative controls drops near 0 while a real lead survives on at least one positive case | `weak_alive` (unchanged from `H-B3-1b`; this result reinforces, does not downgrade or upgrade, that verdict) |

## What This Does NOT Mean

1. Does NOT mean TDA cannot lead classical EWS on Peter Lake — untested with a valid criterion.
2. Does NOT mean the sonde data is unreliable — internal consistency checks (`manifest.md`) passed cleanly; the invalidity is in the DETECTION RULE, not the data.
3. Does NOT close `H-B3-1` or `H-B3-1b` — both `weak_alive`, same concrete next step, now doubly motivated.
4. Does NOT retroactively excuse the season-truncation bug in the first draft run — recorded above as an Escape Point, not smoothed over.

## Pearl Card Update

**Was the Prediction correct?** The floor-invalidity prediction from `H-B3-1b`'s pearl (impact 8: "the
SAME tau≥0.5 threshold on ANY other real ecological series of comparable length will show a comparable
floor") is now **confirmed on a second, independent dataset** — see `pearl_registry/INDEX.md` update.
