# claim.md — 20260906-lakes-tda-ews-invariant-conjunction

**Graph node:** `H-B3-1h` (new, per Minimal Relaxation Rule) · **Bridge:** `B3-MAY-TDA` · **Tier:** Standard
**Parents:** `H-B3-1c` (V1, entropy+AR1) and `H-B3-1g` (total persistence+AR1)

> **Role of this experiment:** explicitly named in `H-B3-1g`'s own Relaxation Map: "Report BOTH entropy
> and total persistence together, flag a series as 'positive' only if BOTH invariants agree." **No new
> compute** — pure re-join of the two already-committed `metrics/run.json` files (V1 and V1g), exactly
> the same "V3-style" cheap-descriptive-synthesis pattern that produced the highest-value/cost finding
> in the whole bridge (`H-B3-1f`'s Paul doSat discovery).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same 9 series, joining V1's (entropy) and V1g's (total persistence) already-computed TDA crossings |
| **Falsifiable predicate** | Requiring BOTH invariants to independently cross (a conjunction rule) reduces the false-positive count below the 4/5 (V1g alone) / 5/5 (V1 alone) already observed, WITHOUT losing the one robust positive signal (Peter doSat) |
| **Measurable outcome** | Per-series: did entropy cross? did total persistence cross? does the conjunction (both) reduce false positives while preserving Peter doSat's signal? |

## Natural Language Statement

> "We test whether requiring agreement between two independently-computed topological invariants
> (persistence entropy from V1, total persistence from V1g) on the SAME 9 series reduces the
> false-positive count observed under either invariant alone, without losing Peter doSat's
> already-4-for-4-replicated positive signal."

## L0 Classification

**Descriptive** — re-joins two already-predictive experiments' outputs into a comparison; the
conjunction RULE itself could be operationalized as a new predictive claim in a FUTURE experiment with
its own kill_criterion, but this experiment characterizes what the conjunction would have shown on
already-collected data, per EstimandOps (a post-hoc join is evaluated on accuracy of characterization).

## What This Does NOT Mean

1. Does NOT constitute a validated NEW predictive detection rule — that would require pre-registering
   the conjunction rule BEFORE seeing this data and testing it on a held-out population, which this
   session's single fixed population of 9 series cannot provide (same in-sample-only limitation as
   every other `H-B3-1*` experiment in this arc).
2. Does NOT use IAAFT or detrend-null variants of total persistence — only the two already-computed
   AR(1)-null variants (V1 entropy, V1g total persistence) are joined here.

## MCID

Informative if the conjunction shows FEWER false positives than V1g alone (4/5) while Peter doSat's
signal survives requiring entropy agreement too (checking whether V1's entropy series ALSO showed a
signal on Peter doSat, which it did — entropy gave the identical +13-day lead in V1).
