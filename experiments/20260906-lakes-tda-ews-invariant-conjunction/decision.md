# decision.md — 20260906-lakes-tda-ews-invariant-conjunction

**Graph node:** `H-B3-1h` · **Date:** 2026-09-06

## Verdict

- [ ] PROMOTE
- [ ] REPEAT
- [ ] REJECT
- [x] **LEAD** — best specificity result in the entire B3 investigation so far; still short of the
  PROMOTE bar, but a genuine, well-motivated improvement, not a repeat

**Statement:** *Requiring agreement between two independently-computed TDA invariants (persistence
entropy from V1, total persistence from V1g), both using the same AR(1)-surrogate null, reduces the
TDA-crossing false-positive count on the 5 negative controls to 2/5 — lower than either invariant alone
(entropy: 3/5, total persistence: 4/5) — while Peter doSat's robust +13-day lead survives the
conjunction unchanged, and Peter pH's problematic 100-day-lag signal (introduced in `H-B3-1g`) is
naturally filtered out.*

## Evidence Summary (no new compute — pure re-join of V1 and V1g's committed results)

| Series | Role | Entropy crosses? | Total persistence crosses? | Conjunction (both)? | Lead (if any) |
|---|---|---|---|---|---|
| Lower Zurich | positive | yes | yes | **yes** | uninterpretable (no classical crossing) |
| Windermere | negative | no | yes | no | — |
| Loch Leven | negative | yes | yes | **yes → FP** | -2.7d (entropy) / 0d (total persistence) |
| Peter chl | positive | yes | yes | **yes** | uninterpretable (no classical crossing) |
| Peter pH | positive | **no** | yes | no | — (the 100-day-lag signal is filtered out) |
| Peter doSat | positive | yes | yes | **yes** | **+13d, identical under both invariants** |
| Paul chl | negative | yes | no | no | — |
| Paul pH | negative | no | yes | no | — |
| Paul doSat | negative | yes | yes | **yes → FP** | +30d (entropy) / +3d (total persistence) |

**Conjunction false positives: 2/5** (Loch Leven, Paul doSat) — down from 3/5 (entropy TDA-crossings
alone) and 4/5 (total persistence alone). **Conjunction positive signals: 3/3** positive cases show
conjunction agreement, though only Peter doSat's is interpretable (has a paired classical crossing to
compute a lead against).

## Why This Is the Best Result Yet, and Why It's Still Not PROMOTE

This is the lowest false-positive count found anywhere in the `B3-MAY-TDA` investigation across every
method tried (raw threshold, V1, V1', V2', V1g, now this conjunction) — genuinely earned by combining
two independently-motivated invariants, not by loosening the detection criterion. It also naturally
solves `H-B3-1g`'s own new problem (Peter pH's misleading late signal) as a side effect, since entropy
never agreed with it. **But 2/5 is still well above the pre-registered `H-B3-1c`-era MCID of ≤1/5** —
Loch Leven and Paul doSat remain false-positive under BOTH invariants, meaning whatever drives their
false signal is not specific to either invariant's particular sensitivity, and a conjunction cannot fix
a problem that both methods share.

## Kill Analysis (OSA)

### What Was Confirmed
- [x] Conjunction of independently-motivated TDA invariants is a real, working technique here — reduces
  false positives below either alone, not merely averaging them.
- [x] Peter doSat's signal is now supported at the highest level of scrutiny available in this session
  (4 individual variants + this conjunction, all agreeing).

### What Remains Unfixed
- [x] Loch Leven and Paul doSat false-positive under BOTH invariants — this is now the sharpest
  remaining open question in the bridge: what property do these two specific series share that NEITHER
  entropy NOR total persistence (nor 3 different null models tested earlier on entropy) can filter out?

### Relaxation Map
| Assumption | Modification | Note |
|---|---|---|
| Conjunction built only from AR(1)-null variants (V1, V1g) | Extend conjunction to include IAAFT-null and/or detrend-null total-persistence variants (not yet computed) | Would need 1-2 new real compute runs (~25 min each), not free like this join |
| Loch Leven / Paul doSat as the last 2 unexplained false positives | A focused single-series case study on just these two (what does their raw data actually look like around the false-crossing date?) | Cheapest possible next step — no new compute, just closer reading of already-collected data |
| Binary conjunction (both invariants must cross) | A weighted/scored combination instead of strict AND | Untested; strict AND is the simplest, most interpretable rule, chosen first per Occam's razor |

## What This Does NOT Mean

1. Does NOT constitute a validated, pre-registered predictive rule — the conjunction was formed by
   looking at both invariants' AR(1) results after they were already computed; a genuine test would
   need to pre-register the conjunction rule and test it on new data, which this fixed 9-series
   population cannot provide (same in-sample caveat as the whole `H-B3-1*` arc).
2. Does NOT mean the bridge is close to being usable in practice — 2/5 false positive is still far
   worse than a real early-warning system would need.
3. Does NOT explain why Loch Leven and Paul doSat resist every method tried — that remains the single
   most important open question for anyone continuing this bridge.

## Note on Floor-Ceiling (FL Step 4a)

Not applicable here, same reasoning as `H-B3-1f` (V3) and `H-B3-1g`: this is a descriptive re-join of
already-collected, already-floor-checked data (both V1 and V1g inherit V1's own validated per-series
AR(1) self-calibration) — no new compute, no new null model, nothing to re-float a floor/ceiling against.

## Pearl Card Update

**New information:** two specific series (Loch Leven, Paul doSat) have now resisted false-positive
correction under: 3 different null models (AR(1), IAAFT, detrend+IAAFT) AND 2 different TDA invariants
(entropy, total persistence) AND their conjunction. This is the most concentrated, most
method-independent false-positive evidence in the whole investigation — stronger than the earlier
"Paul doSat 4/4" finding (`H-B3-1f`) because it now also survives a genuinely different topological
invariant, not just different null models on the same invariant. Whatever produces this signal in these
two specific series is very likely a genuine, real, reproducible STRUCTURAL feature of their data — just
not the regime-shift signal the detector was built to find. Worth a dedicated look at what these two
series' raw dynamics actually look like, independent of any further detector-variant engineering.
