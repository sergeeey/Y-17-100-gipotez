# Artifact Manifest — 20260906-may1972-tda-ews-obrienlakes

## Data provenance (Gate 1 — artifact identity)

| field | value |
|---|---|
| artifact_id | ART-OBRIEN2023-LAKE-PLANKTON |
| source | https://github.com/duncanobrien/ews-assessments (branch: master), files under `Data/` |
| companion publication | O'Brien et al. 2023, *Nature Communications* 14:7942, DOI in `s41467-023-43744-8` |
| companion Zenodo record | https://zenodo.org/records/10062493 (code archive, CC-BY-4.0) |
| date_received | 2026-09-06 |
| publication_status | published, public repository |

| file | bytes | sha256 |
|---|---|---|
| `wrangled_genus_plank_data_public.Rdata` | 280,135 | `a836d6b8e76659dc1749df0937ace9f5a8aec40fe45ab682a128c971ad4b4e8a` |
| `transition_dates.csv` | 3,734 | `149a4443678da99c900a9297f8ea8abf2651f9528fa05efcb24f1234f7f969bd` |
| `Data_README.md` | 625 | `1a67826365d8eed1d3fed70e07b6225b1fe212fec46d7646f64a8197fff7dc27` |

## Environment (exact, 2026-09-06)

Python 3.13.2 · numpy 2.3.4 · scipy 1.16.3 · scikit-learn 1.7.2 · ripser 0.6.14 · pyreadr 0.5.6 (newly
installed this session) · requests 2.32.5 · Windows 11

## What Was Built

**Type:** data-pipeline + code

**Files:**
```
experiments/20260906-may1972-tda-ews-obrienlakes/run.py    — load, embed, classical EWS, TDA, compare
tests/test_lake_tda_ews.py                                  — harness sanity (pairing/embedding correctness)
```

## Objects used from `wrangled_genus_plank_data_public.Rdata`

| R object | Lake | n (monthly) | Date range | Role |
|---|---|---|---|---|
| `LZ_mth_dat` | Lower Zurich | 332 | 1977.00–2005.00 | Positive case (transition ≈2002) |
| `wind_mth_dat` | Windermere | 244 | 1979.00–1999.25 | Negative control (no transition) |
| `leve_mth_dat` | Loch Leven | 152 | 1992.08–2004.67 | Negative control (no transition) |

Column used from each: `pca1`.

## What Was NOT Built

- Mendota and Washington excluded (transition date falls outside the downloaded series' range — see `claim.md` § Step -4).
- No re-implementation of O'Brien et al.'s own threshold-GAM transition dating — their dates are used as ground truth, not re-derived.
- No use of `pca2` as a second axis (see assumption A1) — single-axis, matching their own dating methodology.

## Reproduce

```bash
pip install pyreadr
python fetch_obrien_data.py   # or re-download the 3 files listed above by URL
python run.py
```
