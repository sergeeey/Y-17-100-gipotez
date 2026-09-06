# claim.md — 20260906-lakes-tda-ews-diagram-distance-v1j

**Graph node:** `H-B3-1j` (new) · **Bridge:** `B3-MAY-TDA` · **Tier:** Standard
**Parent:** `H-B3-1g` (the "hard branch" recommendation, `claim.md`: "does NOT test a
bottleneck/Wasserstein-distance-based change-point statistic (a genuinely different FAMILY of TDA
change detection, comparing diagrams directly rather than summarizing each one) — a further, more
involved next step if this one is also uninformative"), and `B3-MAY-TDA`'s 2026-09-06 consolidation
note (`registry/graph.yaml`): "next step... bottleneck/Wasserstein-distance comparison of diagrams
directly — a genuinely different method FAMILY, not another parametric variant."

> **Role of this experiment:** every prior `H-B3-1*` variant (V1 through H-B3-1i) summarized EACH
> rolling window's persistence diagram into a single scalar (entropy or total persistence) BEFORE
> looking for a trend. This throws away the diagram's actual shape/structure at each step and can
> only ever detect a trend in that one summary number. This experiment instead computes, for each
> rolling window, the DISTANCE (Wasserstein-2, via `persim.wasserstein` — already an installed
> dependency of `ripser`, no new package needed) between that window's H1 diagram and a fixed
> REFERENCE diagram (the first valid window's diagram, representing the series' "starting"
> topological state). Rising distance-from-baseline is the natural EWS-style signal for this
> statistic: literal topological drift away from the starting regime, not a proxy scalar's trend.

## Why This Is a Genuinely Different Detection FAMILY, Not a Third Invariant

Entropy and total persistence (H-B3-1c/g) are both SUMMARY statistics of one diagram in isolation —
each diagram is reduced to one number before any comparison happens. A diagram distance metric instead
compares TWO diagrams directly, preserving information a scalar summary discards (e.g., two diagrams
with identical total persistence and identical entropy can still be very different in their actual
bar structure, and a distance metric between them would detect that difference; a scalar summary of
either alone cannot). This is the change explicitly named as needing "a new theoretical input, not a
parametric edit" (`H-B3-1f`'s original recommendation) — the FIRST experiment in this arc that is not
a Minimal-Relaxation-Rule single-assumption change from an existing sibling, but a structurally new
detection statistic. Framed relative to the arc's `null_results` precedent: this is exactly what
`H-B3-1f` predicted would be needed if the invariant axis alone (entropy → total persistence,
`H-B3-1g`) proved insufficient — which `H-B3-1g`/`H-B3-1h`/`H-B3-1i` have now shown (best case: 2/5
false positives via conjunction, still above the ≤1/5 PROMOTE bar).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 9 series as `H-B3-1c`–`i` |
| **Falsifiable predicate** | A rolling-window diagram-distance-from-baseline series, run through the SAME expanding-Kendall-tau + AR(1)-surrogate-null detection rule already validated in `V1`, produces a false-positive rate on the 5 negative controls strictly below the best scalar-summary result so far (2/5, `H-B3-1h`'s conjunction) |
| **Measurable outcome** | False-positive rate on the 5 negative controls; whether Peter doSat's lead (interpretable under AR(1)+total-persistence, absent under IAAFT+total-persistence) reappears, and with what sign/magnitude; whether the false-positive SET differs from every prior variant's |

## FL Step -3: Novelty / Prior-Art Check

`grep` of `null_results/INDEX.md` and `pearl_registry/INDEX.md`: no prior attempt in this project used
a diagram-distance statistic — every prior TDA statistic (`H-B3-1c` onward) was a single-diagram
scalar summary. `persim.wasserstein`/`persim.bottleneck` are standard, published TDA tools (Kerber,
Morozov & Nigmetov 2017 for the underlying algorithms; `persim` is part of the scikit-tda ecosystem),
not a novel invention — novel only in this pipeline's context.

## Baseline-Reference Design Choice (stated explicitly, pre-registered)

The reference diagram is the FIRST valid rolling window's diagram (earliest available topological
state), not a running "previous window" comparison. Rationale: a previous-window (frame-to-frame)
distance would be sensitive to noise at every step and is a fundamentally different, noisier signal
(more like a derivative than a level); a fixed-baseline distance is a more direct analogue of "how far
has the system's topology drifted from where it started," matching the intuition of every other EWS
statistic in this pipeline (variance/AC1 also implicitly compare against the series' own overall
scale/history, not step-to-step). If this baseline-referenced version is uninformative, a
previous-window version is the named Relaxation Map alternative (ONE assumption changed: reference
choice), not attempted here.

## Metric Choice: Wasserstein, Not Bottleneck (stated explicitly, pre-registered)

Bottleneck distance is a max-based metric (sensitive only to the single worst-matched pair of
features) and is known to be less sensitive to gradual, distributed topological change — exactly the
kind of slow drift an early-warning signal should detect. Wasserstein-2 (sum/integral-based) is more
sensitive to distributed change across the whole diagram, a better match for "gradual regime drift"
than "one dramatic outlier feature." Both are implemented by `persim` and equally cheap to compute; if
Wasserstein is uninformative, bottleneck is the named Relaxation Map alternative (ONE assumption
changed: metric choice).

## L0 Classification

**Predictive** — same as every prior variant with a real kill_criterion.

## Kill Criterion (set BEFORE running)

- **PROMOTE:** false-positive rate ≤ 1/5 with ≥1 surviving positive lead.
- **REJECT:** false-positive rate ≥ 4/5 (matching the scalar-summary variants' typical range).
- **LEAD:** false-positive rate strictly better than 2/5 (the best scalar-summary result, `H-B3-1h`)
  but worse than PROMOTE's ≤1/5, OR the false-positive SET differs meaningfully from every prior
  variant in a way that narrows the Loch Leven/Paul doSat open question.

## What This Does NOT Mean

1. Does NOT test a previous-window (frame-to-frame) distance variant — a further step if the
   fixed-baseline version is uninformative (see Baseline-Reference Design Choice above).
2. Does NOT test bottleneck distance — a further step if Wasserstein is uninformative (see Metric
   Choice above). Testing both at once in this same experiment would violate the Minimal Relaxation
   Rule relative to the scalar-summary family (two assumptions changed: statistic family AND metric).
3. If this ALSO produces a false-positive rate in the same 3-4/5 range as every scalar-summary
   variant, that would be strong evidence the specificity ceiling for this bridge lies in the
   detection RULE (expanding-Kendall-tau threshold crossing) or the underlying data itself, not in any
   choice of TDA statistic — a genuinely different, higher-value conclusion than another REJECT on its
   own, matching the Floor-Ceiling spirit even though no formal floor/ceiling arm is pre-registered
   here (this experiment does not introduce a new floor/ceiling population question — see Note below).

## MCID

Same bar as every prior variant: false-positive rate ≤ 1/5 with ≥1 surviving positive lead for
PROMOTE. Given the qualitatively different statistic family, ANY result strictly better than 2/5
(current best) would itself be informative even short of PROMOTE.
