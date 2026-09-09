# claim.md — 20260910-remy-tumorigenesis-early-exit-bfs-h31

**Graph node:** `H-B7-31` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Full
**Parent:** `H-B7-22` (exhaustive reachability, established `n_states_visited` as a perfect but
computationally EXPENSIVE discriminator of `SCHEDULE_FRAGILE` vs `SCHEDULE_ROBUST`). Formalizes and
quantifies an informal sci-hypothesis-skill finding from earlier this session ("H9-B: cheap
precursor") that was never properly registered — closes the ENTIRE original 5-item priority list
from the H-B7-26 redirect (item 5, the lowest priority, attempted last as intended).

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Comparing computational cost between two exact classification
procedures on a fully specified deterministic system. Not causal, not a statistical estimate.

## Origin and design rationale

**The honest problem with the original "H9-B" framing:** `n_states_visited` (H-B7-22's own
`graph.number_of_nodes()`) discriminates `SCHEDULE_FRAGILE` from `SCHEDULE_ROBUST` PERFECTLY
(956/954/200/111 for fragile vs `<=2` for robust) — but it is NOT actually a "cheap precursor" in
any meaningful sense: computing it REQUIRES first building the complete reachability graph via
exhaustive BFS, which is the SAME computation that already tells you the classification directly
(if both `PROLIFERATION` and `GROWTH_ARREST` sink states appear anywhere in that graph, the
condition is `FRAGILE`; if only one appears, it's `ROBUST`). Reporting `n_states_visited` as a
"cheap discriminator" was circular — the honest caveat this experiment names precisely.

**The genuinely cheaper question this experiment actually tests:** does an EARLY-EXIT variant of
the same BFS (stop as soon as BOTH `PROLIFERATION` and `GROWTH_ARREST` have been observed as
reachable, rather than exhausting the full state space) correctly and substantially reduce the
number of states visited for `FRAGILE` conditions, while never producing a false positive on
`ROBUST` conditions (where only one fate is ever reachable)?

**Compute-First Check (scratchpad, BEFORE building the full artifact):** ran a level-by-level BFS
tracking the exact state-visitation count at which both fates first become jointly reachable, for
all 10 of H-B7-26's own tested conditions (8 fragile `k=1..4` + 2 robust `k=5` positive control,
both branches):

```
branch  k  total  early_exit_at  savings
1       1  956    151            84.2%
1       2  954    149            84.4%
1       3  200    20             90.0%
1       4  111    14             87.4%
1       5  2      N/A (only 1 fate found)
(branch_2 identical, per H-B7-27/28's own confirmed isomorphism)
```

**84.2%-90.0% reduction in states visited for all 8 FRAGILE conditions, zero false positives on
the 2 ROBUST conditions.** This is a real, structurally EXPLAINED asymmetry (matching H-B7-24's own
point-of-no-return finding: the escape path's decisive step happens within the first 2-5 steps,
long before the full reachable set is exhausted) — not a coincidence.

**Minimal Relaxation Rule compliance:** reuses H-B7-22's own `async_successors` unchanged; the ONLY
change is the BFS termination condition (early-exit on dual-fate discovery vs exhaustive
completion). No new state space, no new transition model.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "Because H-B7-24 already proved a sharp single-step point-of-no-return
occurs within the first 2-5 steps along the shortest escaping path for every FRAGILE condition,
BOTH fates should become reachable from the release state very early in the BFS frontier expansion
— long before the full ~100-1000-state reachable set is exhausted — making an early-exit variant of
the same BFS a genuine, substantial computational shortcut specifically for FRAGILE conditions."

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same async reachability BFS H-B7-22 already runs, instrumented to record the exact state-visitation count at the moment both fates are jointly confirmed reachable |
| **Falsifiable predicate** | Does early-exit BFS terminate substantially before exhaustive completion for EVERY `SCHEDULE_FRAGILE` condition (i.e. a real, not marginal, reduction), while NEVER falsely reporting "both fates reachable" for a `SCHEDULE_ROBUST` condition? |
| **Measurable outcome** | Per-condition: `n_visited_at_early_exit` vs `n_total_visited`, percentage savings, and whether the ROBUST conditions correctly show only 1 fate (no early exit possible) |

## Kill Criterion (set BEFORE running the full formal artifact — Compute-First already ran)

- **Savings (mandatory):** for ALL 8 `FRAGILE` conditions (`k=1..4`, both branches), the early-exit
  state count must be substantially smaller than the exhaustive total (defined as `<50%` of total,
  a conservative bar well below the `84-90%` already observed) — REJECT/CRITERION_INVALID if any
  condition shows savings below this bar.
- **No false positives (mandatory):** for the `k=5` positive control (both branches,
  `SCHEDULE_ROBUST`), early-exit must NEVER report both fates reachable — only `PROLIFERATION`
  should ever be found, matching H-B7-22's own established classification.
- **Honest asymmetry statement (not a pass/fail check, but a required caveat):** this experiment
  does NOT claim any speedup for classifying `ROBUST` conditions — a `ROBUST` verdict fundamentally
  requires exhausting the entire reachable set (you can never be certain a distant unvisited state
  doesn't reach the other fate without visiting it), so the "cheap precursor" applies ONLY as a fast
  CONFIRMATION path for `FRAGILE`, never as a fast path to confirm `ROBUST`.

## What This Does NOT Mean

1. Does NOT claim a general speedup for the `ROBUST` classification — explicitly the opposite,
   this is a real, structurally-forced one-directional asymmetry, not a symmetric optimization.
2. Does NOT claim this generalizes to a DIFFERENT network or a DIFFERENT release-state family — only
   tested on H-B7-26's own 10 already-established conditions in this specific model.
3. Does NOT itself change H-B7-22's own already-committed classification of any condition — this is
   a computational-cost finding about HOW CHEAPLY the same classification can be reached for the
   FRAGILE side, not a new classification result.
4. Does NOT claim `n_states_visited` itself (the original informal "H9-B" framing) is a valid cheap
   discriminator — this experiment explicitly corrects that framing as circular, replacing it with
   the genuinely cheaper early-exit variant.

## MCID

Not applicable — exact computational-cost comparison on a fully specified deterministic system, no
statistical estimate.
