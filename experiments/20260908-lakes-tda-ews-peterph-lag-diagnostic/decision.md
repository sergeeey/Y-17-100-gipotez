# H-B3-1o — decision.md

## Result

### Positive control gate: FAILED

| | value |
|---|---:|
| doSat half-rise date | 249.0 |
| doSat tda_crossing (stored, H-B3-1g) | 172.0 |
| Gate distance | **77.0 days** |
| Gate threshold | 20.0 days |
| **Gate passes** | **NO** |

The half-rise-date metric does **NOT** track the tau/surrogate-crossing date even on the
KNOWN-good case (Peter doSat, a clean positive with no lag anomaly) — it lands 77 days
later than the actual crossing, nearly 4x the pre-registered 20-day tolerance.

### Primary result (reported, but per the pre-registered gate, NOT trusted as an answer)

| | value |
|---|---:|
| pH half-rise date | 218.0027397260917 |
| pH classical_crossing (stored) | 218.0027397260917 |
| pH tda_crossing (stored) | 318.0054794521577 |
| Distance to classical anchor | **0.0** (exact match) |
| Distance to tda_crossing anchor | 100.0 |

**Verdict: `METRIC_UNRELIABLE`** — per the pre-registered Kill Criterion, since the
positive-control gate failed, NEITHER `ARTIFACT_HYPOTHESIS_SUPPORTED` nor
`GENUINE_DELAY_HYPOTHESIS_SUPPORTED` is reported, despite pH's half-rise date landing
EXACTLY on the classical crossing date (0.0 days apart) — a striking-looking number that
is explicitly NOT treated as evidence, because the same metric was just shown to be off by
77 days on a case where the right answer is already known.

**This is the discipline working as designed, not a failure of the experiment.** The
exact 0.0 match on pH is exactly the kind of number a less careful writeup would be
tempted to report as "the artifact hypothesis is confirmed" — the pre-registered gate
existed specifically to prevent that, and it did its job.

## Why the metric failed (diagnosed, not just reported)

The half-rise-date metric compares the RAW total-persistence value's own [min,max] range
midpoint-crossing against a date derived from a fundamentally different quantity: the
EXPANDING KENDALL TAU of that series (a cumulative rank-correlation-with-time statistic
computed over the full history up to each point), crossing a PER-TIMEPOINT self-calibrated
AR(1)-surrogate null. "When does the raw value cross halfway" and "when does the
cumulative trend statistic exceed a moving null threshold" are not the same question, and
there is no reason a priori to expect them to align closely even in a case with no
anomaly — confirmed directly by doSat's own 77-day gap.

## Kill Analysis

**What was killed:** the half-rise-date-of-the-raw-series diagnostic, as a valid cheap
proxy for "when does this specific tau-accumulation/self-calibrated-crossing detection
method register a change" — it does not track that quantity reliably, shown directly on a
known case, not assumed.

**What was NOT killed:** H-B3-1g's own original open question (is Peter pH's 100-day lag
a real delayed structural signal or a detection-method artifact?) — this experiment does
NOT answer it; the question remains genuinely open, now for a different reason (the first
cheap attempt to answer it used an inadequate diagnostic, not because the question itself
is unanswerable).

**Relaxation Map:**
- A more faithful diagnostic would compare the EXPANDING TAU trajectory itself (not the
  raw value) between pH and doSat — e.g., does pH's tau curve rise similarly to doSat's
  but simply take longer to clear an elevated or noisier null threshold, versus pH's tau
  curve itself not rising until late. This directly targets the quantity the crossing rule
  actually uses, unlike the raw-value half-rise metric this experiment tried.
- Alternatively, compare the per-timepoint NULL CURVE itself between pH and doSat — if
  pH's surrogate null happens to be unusually elevated/noisy near day 218-318 (a
  calibration-noise explanation) versus comparably calibrated to doSat's, that would
  separate "the real signal is late" from "the bar it must clear is unusually high late."

## What This Does NOT Mean

1. Does NOT resolve H-B3-1g's original open question about Peter pH's lag mechanism —
   genuinely still open.
2. Does NOT mean pH's exact 0.0-day half-rise/classical-crossing match is meaningless in
   some other sense — only that THIS metric, shown unreliable on a known case, cannot be
   used to interpret it. A different, better-validated diagnostic might legitimately
   revisit this number.
3. Does NOT change H-B3-1g's own REJECT-adjacent verdict (4/5 false positives) — unrelated
   to this diagnostic's outcome.
4. Does NOT mean "cheap follow-up ideas from a Relaxation Map are unreliable in general" —
   this is one specific metric failing one specific validation gate; the broader practice
   of naming and eventually trying cheap follow-ups (as in H-B3-1n) remains sound.

## Go/No-Go

**PARKED**, not REJECT — the underlying question (real delay vs. detection-method
artifact) is not falsified, only genuinely still open; this specific diagnostic method is
what gets set aside. The positive-control gate is exactly the kind of check that should
stop a plausible-looking but wrong answer before it gets reported as a finding — recorded
as a clean methodological null result, not a fabricated conclusion. Revival condition:
compare the expanding-tau TRAJECTORY itself (not raw value) between pH and doSat, per the
Relaxation Map above — a concrete, not-yet-attempted next step, not "someday."

## Pearl Registry Update

New row: the half-rise-date-of-raw-series metric does not track expanding-Kendall-tau
crossing dates even in known-good cases (77-day gap on Peter doSat) — any future diagnostic
in this project comparing "when a raw statistic changes" against "when a
trend/rank-based detection rule fires" should validate on a known case first, exactly as
this experiment's own pre-registered gate did, rather than assume the two track together.
