# Result Summary (Full-Ladder Step 8)

**Experiment ID:** `20260906-riemann-rstat-gue` · **Date run:** 2026-09-06 · seed 0

## Raw Results (`metrics/run.json`, `metrics/controls.json`) — all `[VERIFIED]` from files

| Metric | Reference | Result | Delta | Reading |
|---|---|---|---|---|
| ⟨r⟩, all 100k zeros | surmise 0.602658 | **0.61092 ± 0.00072** | **+0.00826** | inside pre-registered band (±0.01); margin to kill = 0.0017 |
| ⟨r⟩, all 100k zeros | empirical GUE ceiling 0.60060 ± 0.00073 | 0.61092 | **+0.0103 ≈ 10 σ** | **above** the large-N GUE value |
| efficiency (Step 4a) | 1.0 = ceiling | **1.038** | | > 1 → ceiling mis-specified for this population (see below) |
| ⟨r⟩ first 50k | | 0.61188 | +0.0092 | |
| ⟨r⟩ last 50k | | 0.60995 | +0.0073 | monotone toward GUE with height |
| ⟨r⟩ first 1,000 (stress) | | 0.61704 | +0.0144 | outside band — low-height regime, no threshold was claimed |
| ⟨r⟩ synthetic GUE | 0.602658 | 0.60060 | −0.0021 | positive control PASS |
| ⟨r⟩ synthetic GOE | 0.535898 | 0.53102 | | separated from GUE by 0.070 |
| ⟨r⟩ Poisson | 0.386294 | 0.38666 | | kill fired — criterion can fail |

## Classification

**[x] PROMOTE — as a *replication* of the GUE regime and as the lab's positive control, with a `[WEAKENED]` scope note.**
**[ ] REPEAT** **[ ] REJECT** **[ ] ARCHIVE**

Rationale for PROMOTE rather than REPEAT: the pre-registered falsifiable claim (`|⟨r⟩ − 0.602658| < 0.01`)
holds; every control behaved; the pipeline is validated. Rationale for the `[WEAKENED]` note: the margin
is 17 % of the tolerance, and relative to the *empirical* GUE value the excess is 10 σ — the zeros at
heights ≲ 7.5·10⁴ are **not yet in the asymptotic GUE regime at the 0.01 level**. The claim survives as
worded; it would NOT survive with tolerance 0.005 or with the empirical ceiling as target.

## Evidence Quality

- Data source: **real** (Odlyzko table, sha256 in manifest) — `[VERIFIED-REAL]`; controls synthetic — `[VERIFIED-SYNTHETIC]`
- Sample size: N = 99,998 ratios (data); ≈ 10⁵ per synthetic ensemble
- Test command: `python run.py controls --seed 0 && python run.py run --seed 0 && python run.py stress`
- Log files: `metrics/controls.json`, `metrics/run.json`, `metrics/stress.json`

## Confidence Level

**[x] MEDIUM** — 1 run on real data, controls passed, single seed for synthetic controls.
HIGH would require a second independent implementation of the *loader* (the pure-Python check covers only
the statistic) and a second seed — cheap, but not done in this run and not claimed.

## Unexpected Observations (→ Pearl Gate)

1. **Low-height excess of ⟨r⟩ over GUE, monotone in height:** 0.617 (first 10³) → 0.6119 (first 5·10⁴) →
   0.6100 (last 5·10⁴) → 0.6006 (GUE, N→∞). Direction and rough size are consistent with known
   finite-height (arithmetic) corrections to nearest-neighbour statistics of low zeros
   (Bogomolny–Bohigas–Leboeuf–Monastra 2006, for P(s)); whether the *r-statistic* version has been
   published is **unknown → novelty check required before this becomes a hypothesis**. Falsifiable
   prediction: on `zeros6` (height ~10²²) the excess vanishes below 0.002.
2. **Shuffled-spacing gap:** ζ-shuffled 0.6432 vs GUE-shuffled 0.6346. Shuffling removes correlations
   and leaves P(s); the gap therefore says the *marginal* spacing distribution of low zeros is already
   more repulsive than GUE's — same physics as (1), seen through a different lens.
3. **Methodology:** efficiency > 1 is not "beating the ceiling"; it means the ceiling (asymptotic GUE)
   was specified for the wrong population (finite height). Step 4a needs the ceiling to be the
   *privileged answer for the population actually measured* — here, a finite-height-corrected value.

---

*Proceed to: `caveats.md` (pre-written; append post-run notes) → skeptic (Step 8a) → `decision.md`*
