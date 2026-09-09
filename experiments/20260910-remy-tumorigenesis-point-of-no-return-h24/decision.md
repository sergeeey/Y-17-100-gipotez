# H-B7-24 — decision.md

## Result

**Compute-First Check's own finding confirmed and generalized across all 8 conditions.** For
every one of H-B7-22's 8 confirmed `SCHEDULE_FRAGILE` release-states (`k=1..4`, both branches),
the shortest async-escaping path shows a **single, sharp point of no return** — `GROWTH_ARREST`
is reachable (via full exhaustive reachability, not assumed) from every state before that step,
and permanently unreachable from every state at or after it. No gradual decline, no flip-back —
a genuine step function in every one of the 8 cases (`all_sharp_single_step: true`).

| Branch | k | Path length | Point-of-no-return step | Triggering node |
|---|---|---|---|---|
| branch_1 | 1 | 11 | 5 | `CyclinE1` |
| branch_1 | 2 | 10 | 4 | `CyclinE1` |
| branch_1 | 3 | 6 | 4 | `CyclinE1` |
| branch_1 | 4 | 3 | 2 | `CyclinE1` |
| branch_2 | 1 | 11 | 5 | `CyclinE1` |
| branch_2 | 2 | 10 | 4 | `CyclinE1` |
| branch_2 | 3 | 6 | 4 | `CyclinE1` |
| branch_2 | 4 | 3 | 2 | `CyclinE1` |

**The triggering node is `CyclinE1` in all 8 cases**, never `CyclinA` despite the two nodes
sharing an IDENTICAL rule in this network (verified directly against the `.bnet` file, not
assumed) — the shortest-path search happens to route through `CyclinA` firing first in most
cases (confirmed in the `k=1` case's own step-by-step trace) without that alone committing the
system; only once `CyclinE1` ALSO fires does `GROWTH_ARREST` drop out of the reachable set. Both
branches agree exactly on path length, step index, and triggering node at every `k` — a further,
independent confirmation of H-B7-12's branch-equivalence finding.

**Path length and point-of-no-return step both shrink monotonically as `k` approaches the
synchronous threshold `k*=5`** — consistent with the intuitive picture that release-states closer
to the synchronous threshold require less "distance" (fewer async steps) to reach the same
irreversible commitment.

## Mechanism (confirmed, generalized beyond the single k=1/branch_1 spot-check)

The pre-registered Mechanism Claim Gate hypothesis (claim.md) — that `CyclinA` firing alone is
individually reversible because its rule is not monotonic under further async updates, while
`CyclinE1`'s own firing is what actually locks in the commitment — is directly supported by the
exhaustive per-step reachability data: in EVERY case, `GROWTH_ARREST` remains reachable through
the step immediately after `CyclinA` fires (when `CyclinA` fires before `CyclinE1` along the
shortest path) and becomes unreachable only once `CyclinE1` itself updates. This is not
hand-waved from the single `k=1` trace alone — it is the same pattern in all 8 independently
computed cases.

## Verdict

**CONFIRMED** — a sharp, single-step, mechanistically-explained "point of no return" exists
along the shortest async-escaping path for every one of H-B7-22's 8 confirmed fragile
release-states, always coinciding with `CyclinE1`'s own firing.

## FL Step 8a — Independent Reviewer

Narrowly-scoped, context-asymmetric spot-check on the highest-value single case: `branch_1, k=1`
(the longest path, 11 steps, offering the most opportunity for the "sharp single step" claim to
fail if it were going to).

**Verdict: CONFIRMED.** The reviewer independently reconstructed release state R (branch_1, k=1)
via `h13.simulate_transient_clamp_multi_with_release_state` (used as permitted, not
reimplemented), then ran its OWN shortest-path BFS (own termination check, only `async_successors`
reused, which is independently pre-verified from prior reviews) and independently arrived at the
IDENTICAL 11-step path this experiment reports — a strong, unforced independence signal (tie-
breaking is deterministic from `async_successors`' fixed iteration order, so exact reproduction
is expected once the same shortest path exists, not circular reasoning). It then ran its OWN
exhaustive reachability check (own BFS + own `networkx` sink-SCC attractor detection, NOT calling
this experiment's own `build_reachability_graph`/`find_sink_attractors`) at each of the 12 states
along the path: `GROWTH_ARREST` reachable (both fates, 956→712 states) through step 4, drops to
UNREACHABLE (only `PROLIFERATION`, 48 states) at step 5 (`CyclinE1`'s own update), and STAYS
unreachable through step 11 — explicitly checked for a later flip-back, per the review brief's own
instruction not to assume monotonicity, and none was found. Matches this experiment's own reported
numbers exactly: same path, same step-5 point of no return, same `CyclinE1` trigger, same
sharpness.

## Kill Analysis

Not applicable (not a REJECT) — clean confirmation across all 8 tested conditions with no
exceptions.

## What This Does NOT Mean

Carried from claim.md: this is the point of no return along ONE specific (shortest) path per
release-state, not a claim about all possible escaping paths; does not generalize beyond the
`CyclinA`/`CyclinE1`/`p21CIP`/`RBL2` feedback loop this B7 sub-arc has focused on throughout;
does not re-derive H-B7-23's own frequency estimates.

## Scope note

Eighth experiment in the B7 async/observability sub-arc, direct mechanistic deepening of H-B7-22's
own race-condition finding — pinpoints WHEN commitment becomes irreversible, not just THAT it can
happen (H-B7-22) or HOW OFTEN (H-B7-23). Reuses H-B7-22's `async_successors`/
`build_reachability_graph`/`find_sink_attractors` machinery entirely unchanged, applying it at
multiple points along a path rather than only at the release state.
