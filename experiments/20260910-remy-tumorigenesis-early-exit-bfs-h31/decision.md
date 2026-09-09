# decision.md — 20260910-remy-tumorigenesis-early-exit-bfs-h31

## Verdict: **CONFIRMED**

## Result Summary (`metrics/run.json`, 10 conditions)

| branch | k | classification | total states | early-exit at | savings |
|---|---|---|---|---|---|
| branch_1 | 1 | FRAGILE | 956 | 151 | 84.2% |
| branch_1 | 2 | FRAGILE | 954 | 149 | 84.4% |
| branch_1 | 3 | FRAGILE | 200 | 20 | 90.0% |
| branch_1 | 4 | FRAGILE | 111 | 14 | 87.4% |
| branch_1 | 5 | ROBUST | 2 | N/A (1 fate only) | N/A |
| branch_2 | 1-5 | (identical to branch_1, per H-B7-27/28's own isomorphism) | | | |

**8/8 FRAGILE conditions exceed the 50% kill-criterion savings bar by a wide margin (actual
84.2%-90.0%). 2/2 ROBUST conditions correctly show zero false positives** (only `PROLIFERATION`
ever found reachable, matching H-B7-22's own established classification exactly).

## Mandatory checks against claim.md's own Kill Criterion

- [x] Savings `>50%` for ALL 8 FRAGILE conditions — **PASS** (actual: 84.2%-90.0%)
- [x] No false positives on the 2 ROBUST conditions — **PASS**
- [x] Honest asymmetry documented, not silently omitted — **PASS**, see below

## Interpretation

Corrects an informal, never-formally-registered earlier finding ("H9-B: `n_states_visited` is a
cheap discriminator") that was circular on inspection — `n_states_visited` requires the SAME
exhaustive computation the classification itself needs, so it saves nothing. The genuinely cheaper
question — early-exit BFS — gives a real, substantial, structurally-explained saving (matching
H-B7-24's own point-of-no-return finding: the decisive commitment step happens within the first
2-5 steps, long before the ~100-1000-state reachable set is exhausted). This is real for the
FRAGILE side only. **`ROBUST` classification cannot be sped up this way** — confirming a condition
is `SCHEDULE_ROBUST` requires certainty that NO reachable state leads to the other fate, which by
definition requires exhausting the entire reachable set (visiting fewer states can never rule out
that an unvisited one reaches the missing fate). This is a genuine, structurally-forced asymmetry,
not an implementation gap.

**Practical implication:** for a much larger network where `n_states_visited` could be in the
millions, an early-exit BFS variant would give substantial real savings for confirming schedule-
fragility exists, but would offer NO speedup for confirming schedule-robustness — a useful,
honestly-scoped optimization, not a universal one.

## FL Step 8a — Independent Reviewer

Full-tier claim quantifying a computational-cost property — mandatory per FL Step 8a.
Context-asymmetric: reviewer given `claim.md` + `run.py` only, no reasoning chain. Scoped narrowly
to ONE reconstruction: independently rebuild `branch_1, k=3` (the largest percentage saving, 90.0%,
smallest total graph among the FRAGILE conditions, cheapest to fully verify) with a fresh,
independently-written BFS implementation (not calling this experiment's own
`bfs_with_early_exit_tracking`), confirming both the total state count (200) and the early-exit
count (20).

**Verdict: CONFIRMED-REAL.** Reviewer wrote a fully independent BFS (own `deque`-based level loop,
own visited-set tracking, own fate classifier checking `Growth_arrest` BEFORE `Proliferation` —
deliberately the OPPOSITE check order from this experiment's own `fate_of`, ruling out an
order-dependent bug coincidentally matching), reusing only `async_successors` as instructed.

- Independently computed: `total_visited=200`, `early_exit_count=20`, `fates_seen=['GROWTH_ARREST',
  'PROLIFERATION']`
- Exact match against committed `n_total_visited=200`, `n_visited_at_early_exit=20`

## Skeptic Concerns

No `[FALSIFIED]` concerns raised. Reviewer's independent BFS (deliberately using a different
fate-check ORDER than this experiment's own implementation, to rule out an order-dependent
coincidence) matched exactly — no dismiss/accept/mitigate entries needed.

## Caveats / What This Does NOT Mean

Per claim.md's own "What This Does NOT Mean" section — unchanged and reaffirmed:

1. Does NOT claim a speedup for `ROBUST` classification — explicitly the opposite.
2. Does NOT claim this generalizes beyond this specific model/release-state family.
3. Does NOT change any of H-B7-22's own already-committed classifications.
4. Does NOT validate the original informal `n_states_visited` framing — explicitly corrects it.

## MCID

Not applicable — exact computational-cost comparison, no statistical estimate.
