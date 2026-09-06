# Artifact Manifest — 20260906-may1972-tda-ews-peterlake

## Data provenance (Gate 1 — artifact identity)

| field | value |
|---|---|
| artifact_id | ART-CASCADE-SONDES-08TO11 |
| source | User-provided file: `squealSondesMet_08to11_forOPUS.csv`, delivered 2026-09-06 |
| filename convention | "squeal" (likely internal Cascade-project shorthand) + "SondesMet" (sonde meteorological/limnological sensors) + "08to11" (2008–2011) + "forOPUS" (prepared for the project's OPUS analysis pipeline) — consistent with the NTL-LTER Cascade Project's own internal naming, not independently confirmed against a published package ID |
| companion publication | Carpenter et al. 2011, *Science* 332(6033):1079–1082, DOI 10.1126/science.1203672 |
| date_received | 2026-09-06 (manual delivery, unblocking the `BLOCKED-INFRASTRUCTURE` verdict in `substrate_gate.md`) |
| publication_status | Underlying study published; this specific CSV extract's exact EDI package/version is not independently re-verified — treated as `[VERIFIED-REAL]` on the strength of internal consistency checks below, not on a re-confirmed DOI/package ID |

| file | bytes | sha256 |
|---|---|---|
| `squealSondesMet_08to11_forOPUS.csv` | 34,216,860 | `1e03208bb5bf42fab5d4df848b072df8ccb70e02bd05e95e89ae611622c7d71e` |

## Internal consistency checks (Gate 1, run before analysis)

| Check | Result |
|---|---|
| Lakes present | `Peter`, `Paul` — matches the manipulated/reference pair in Carpenter et al. 2011 |
| Years present | 2008, 2009, 2010, 2011 — matches the paper's stated experiment window |
| Row balance | Peter and Paul have IDENTICAL row counts per year (e.g. 30,465 in 2008 for both) — consistent with a paired, simultaneously-sampled design |
| Sampling interval | Median 5.0 minutes for both lakes — matches "high-frequency" framing |
| Large gaps (>60 min) | 3 per lake across 3.5 years — excellent completeness |
| Missing chl/pH/doSat | 1,380 of 127,263 rows (~1.1%) — plausible instrument maintenance/calibration windows |
| Seasonal structure | 4 clean field seasons (2008: doy 133–239; 2009: doy 133–246; 2010: doy 134–246; 2011: doy 133–245), each ~107–114 days, separated by winter gaps of ~230 days — matches the paper's own description: "monitored daily ... for three years of summer stratification" (2008–2010) plus an apparent 4th confirmatory season (2011) |

**Verdict: internally consistent with the claimed identity.** Not independently re-confirmed against a
specific EDI package DOI (the original blocked package was `knb-lter-ntl.360.2`) — this file was not
downloaded by this session from that URL, it was provided directly by the user. Recorded honestly as
`[VERIFIED-REAL]` on the strength of the checks above, with this provenance caveat explicit rather than
silently assumed.

## Environment (exact, 2026-09-06)

Python 3.13.2 · numpy 2.3.4 · pandas 2.3.3 · scipy 1.16.3 · ripser 0.6.14 · Windows 11

## What Was Built

**Type:** data-pipeline + code (reuses tested functions from the sibling experiment via import)

```
experiments/20260906-may1972-tda-ews-peterlake/run.py   — loader (season-concatenated) + verdict
```

Imports `rolling_stat`, `betti1_entropy_series`, `expanding_kendall_tau`, `first_crossing`,
`floor_false_positive_rate`, `WINDOW_FRAC`, `EMBED_DIM`, `EMBED_DELAY`, `TAU_THRESHOLD` directly from
`../20260906-may1972-tda-ews-obrienlakes/run.py` — same tested code, not reimplemented.

## What Was NOT Built

- No re-verification of the exact EDI package/version this CSV traces to (see provenance caveat above).
- 2011 season excluded from the lead-time analysis (post-transition per the paper; used only as an
  implicit sanity reference, not analyzed in `run.py`).
- No re-implementation of Carpenter et al.'s own EWS statistics (their published lag-1 autocorrelation /
  variance results are not re-derived here as a direct numeric cross-check — only the SAME kind of
  statistic, computed independently on this data, is compared to the TDA signal).

## Reproduce

```bash
python run.py   # reads data/squealSondesMet_08to11_forOPUS.csv, writes metrics/run.json
```
