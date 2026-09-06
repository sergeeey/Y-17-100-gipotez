# Artifact Manifest (Full-Ladder Step 2)

**Experiment ID:** `20260906-riemann-rstat-gue` · **Graph node:** `H-B1-1a`

## What Was Built (Minimal Artifact)

**Type:** code + data-pipeline

**Files:**
```
experiments/20260906-riemann-rstat-gue/run.py      — PIPELINE (r_stat, synthetic ensembles, unfold, shuffle)
                                                    + EXPERIMENT (controls / run / stress → metrics/*.json)
tests/test_rstat.py                                — harness sanity (A5 pairing), 5 tests
experiments/20260906-riemann-rstat-gue/data/zeros1.txt  — cached download, gitignored (1,900,000 bytes)
experiments/20260906-riemann-rstat-gue/metrics/{controls,run,stress}.json — all outputs
```

**Environment (exact, 2026-09-06):** Python 3.13.2 · numpy 2.3.4 · requests 2.32.5 · PyYAML 6.0.3 · Windows 11 Pro 10.0.26200

## Data provenance (Gate 1 — artifact identity)

| field | value |
|---|---|
| artifact_id | ART-ODLYZKO-ZEROS1 |
| source | https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1 |
| description (publisher) | first 100,000 zeros, accurate to within 3·10⁻⁹ |
| date_received | 2026-09-06 |
| sha256 (as downloaded, UTF-8 text) | `3436c916a7878261ac183fd7b9448c9a4736b8bbccf1356874a6ce1788541632` |
| identity checks at load | count = 100,000 ✓ · γ₁ = 14.134725142 ✓ · strictly increasing ✓ |
| publication_status | published (public table) |

## What Was NOT Built

- No unfolding-based statistics (P(s), Σ², Δ₃) — only ⟨r⟩.
- No higher tables (`zeros2`…`zeros6`) — the finite-height trend seen here would need them; deferred to a
  possible follow-up experiment, not bolted on post hoc.
- No plotting.

## Reversibility

- **Can this be reverted?** Yes — `git revert <commit>`; the data file is re-downloadable and gitignored.

## Reproduce

```bash
cd experiments/20260906-riemann-rstat-gue
python run.py controls --seed 0 && python run.py run --seed 0 && python run.py stress
```
